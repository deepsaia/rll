import mlflow
import gymnasium as gym
import torch
import torch.nn as nn
import pandas as pd
import onnx
import numpy as np
import mlflow.models.signature as mlsig
from mlflow.types import Schema, ColSpec
import psutil
import platform
import time

GPU_AVAILABLE = False
try:
    import nvidia_smi
except ImportError:
    nvidia_smi = None
    print("nvidia-ml-py not installed, skipping GPU metrics")
else:
    try:
        nvidia_smi.nvmlInit()
        GPU_AVAILABLE = platform.system() in ["Linux", "Windows"]
    except Exception as e:
        print(f"GPU metrics unavailable: {e}")
        GPU_AVAILABLE = False

class Policy(nn.Module):
    def __init__(self, obs_dim, act_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, 32),
            nn.ReLU(),
            nn.Linear(32, act_dim)
        )

    def forward(self, x):
        return self.net(x)

mlflow.set_tracking_uri("./mlruns")
mlflow.set_experiment("rl-local")

def log_system_metrics(step: int, step_time: float):
    """Log CPU, memory, and GPU usage at each step."""
    mlflow.log_metric("system/cpu_percent", psutil.cpu_percent(), step=step)
    mlflow.log_metric("system/memory_percent", psutil.virtual_memory().percent, step=step)
    mlflow.log_metric("system/step_duration_sec", step_time, step=step)

    if GPU_AVAILABLE:
        try:
            handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
            util = nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
            mem = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
            mlflow.log_metric("system/gpu_util", util.gpu, step=step)
            mlflow.log_metric("system/gpu_mem_util", mem.used / mem.total * 100, step=step)
        except Exception as e:
            print(f"Skipping GPU metrics at step {step}: {e}")



class Policy(nn.Module):
    def __init__(self, obs_dim, act_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, 32),
            nn.ReLU(),
            nn.Linear(32, act_dim)
        )

    def forward(self, x):
        return self.net(x)

@mlflow.trace
def select_action(model, obs):
    obs_tensor = torch.tensor(obs, dtype=torch.float32)
    logits = model(obs_tensor)
    return torch.argmax(logits).item()


@mlflow.trace
def rollout(env, model, max_steps=100):
    obs, _ = env.reset()
    total_reward = 0
    start_episode = time.time()  # Track episode duration
    for step in range(max_steps):
        step_start = time.time()
        action = select_action(model, obs)
        obs, reward, terminated, truncated, _ = env.step(action)

        # Log reward and system metrics
        mlflow.log_metric("reward", reward, step=step)
        step_time = time.time() - step_start
        mlflow.log_metric("training/step_duration_sec", step_time, step=step)
        log_system_metrics(step, step_time)

        total_reward += reward
        if terminated or truncated:
            break

    episode_time = time.time() - start_episode
    mlflow.log_metric("training/episode_duration_sec", episode_time)

    return total_reward, step


@mlflow.trace
def evaluate(env, model, n_episodes=5, max_steps=200):
    results = []
    for ep in range(n_episodes):
        obs, _ = env.reset()
        total_reward, steps = 0, 0
        done = False
        while not done and steps < max_steps:
            action = select_action(model, obs)
            obs, reward, terminated, truncated, _ = env.step(action)
            total_reward += reward
            steps += 1
            done = terminated or truncated
        results.append({"episode": ep, "total_reward": total_reward, "steps": steps})
    return pd.DataFrame(results)


def train():
    run_start = time.time()  # Track total run time
    with mlflow.start_run(run_name="cartpole-onnx") as run:
        env = gym.make("CartPole-v1")
        model = Policy(env.observation_space.shape[0], env.action_space.n)

        # Training rollout (toy)
        total_reward, steps = rollout(env, model)
        mlflow.log_metric("episode_total_reward", total_reward)
        mlflow.log_params({"env": "CartPole-v1", "steps": steps})

        # Export ONNX model (batch dim 1)
        dummy_input = torch.randn(1, env.observation_space.shape[0])
        onnx_path = "policy.onnx"
        torch.onnx.export(
            model, dummy_input, onnx_path,
            input_names=["obs"], output_names=["logits"],
            dynamo=True
        )

        onnx_model = onnx.load(onnx_path)

        input_example = pd.DataFrame(
            np.random.randn(1, env.observation_space.shape[0]).astype(np.float32),
            columns=[f"obs_{i}" for i in range(env.observation_space.shape[0])]
        )

        input_schema = Schema([ColSpec("float", f"obs_{i}") for i in range(env.observation_space.shape[0])])
        output_schema = Schema([ColSpec("float", f"logit_{i}") for i in range(env.action_space.n)])
        signature = mlsig.ModelSignature(inputs=input_schema, outputs=output_schema)

        mlflow.onnx.log_model(
            onnx_model=onnx_model,
            name="CartPolePolicyONNX",
            input_example=input_example,
            signature=signature
        )

        # Evaluation phase
        eval_df = evaluate(env, model, n_episodes=10)
        mlflow.log_table(eval_df, artifact_file="evaluation/eval_results.json")

        # Total training time
        run_time = time.time() - run_start
        mlflow.log_metric("training/total_run_time_sec", run_time)

        print("Evaluation results:")
        print(eval_df)
        print(f"Run ID: {run.info.run_id}")
        print("Model registered under name: CartPolePolicyONNX")


if __name__ == "__main__":
    train()
