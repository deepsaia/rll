import wandb
import gymnasium as gym
import torch
import torch.nn as nn
import pandas as pd
import onnx
import numpy as np
import psutil
import platform
import time
import os

# GPU Detection (same as before)
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

# Ensure API key is available
if "WANDB_API_KEY" not in os.environ:
    raise EnvironmentError(
        "WANDB_API_KEY environment variable is not set. "
        "Please set it before running this script.\n"
        "Example: export WANDB_API_KEY=your_api_key_here"
    )

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


def log_system_metrics(step: int, step_time: float):
    """Log CPU, memory, and GPU usage at each step."""
    wandb.log({
        "system/cpu_percent": psutil.cpu_percent(),
        "system/memory_percent": psutil.virtual_memory().percent,
        "system/step_duration_sec": step_time,
    })

    if GPU_AVAILABLE:
        try:
            handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
            util = nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
            mem = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
            wandb.log({
                "system/gpu_util": util.gpu,
                "system/gpu_mem_util": mem.used / mem.total * 100,
            })
        except Exception as e:
            print(f"Skipping GPU metrics at step {step}: {e}")


def select_action(model, obs):
    """Select action using policy (logged manually since wandb has no @trace)"""
    obs_tensor = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)  # Add batch dim
    logits = model(obs_tensor)
    action = torch.argmax(logits).item()
    # Optional: Log logits for inspection (useful for debugging)
    wandb.log({"policy/logits": logits.detach().cpu().numpy().flatten().tolist()}, step=wandb.run.step)
    return action


def rollout(env, model, max_steps=100):
    obs, _ = env.reset()
    total_reward = 0
    start_episode = time.time()

    for step in range(max_steps):
        step_start = time.time()
        action = select_action(model, obs)
        obs, reward, terminated, truncated, _ = env.step(action)

        # Log per-step metrics
        wandb.log({
            "reward": reward,
            "training/step_duration_sec": time.time() - step_start,
        })

        log_system_metrics(step, time.time() - step_start)

        total_reward += reward
        if terminated or truncated:
            break

    episode_time = time.time() - start_episode
    wandb.log({"training/episode_duration_sec": episode_time})

    return total_reward, step


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
    run_start = time.time()

    # Initialize wandb run
    wandb.init(
        project="rl-local",
        name="cartpole-onnx",
        config={
            "env": "CartPole-v1",
            "model_architecture": "Linear(32)-ReLU-Linear",
            "optimizer": "none (random init)",
            "max_steps": 100,
            "eval_episodes": 10,
        },
        tags=["cartpole", "onnx", "baseline"],
        notes="Baseline policy trained with random weights, logging system metrics and ONNX export."
    )

    # Setup environment and model
    env = gym.make("CartPole-v1")
    model = Policy(env.observation_space.shape[0], env.action_space.n)

    # Optionally watch model for gradient flow (if you later add training)
    # wandb.watch(model, log="all", log_freq=10)

    # Training rollout (toy: random policy)
    total_reward, steps = rollout(env, model, max_steps=100)
    wandb.log({
        "episode_total_reward": total_reward,
        "training/steps_taken": steps
    })

    # Export ONNX model
    dummy_input = torch.randn(1, env.observation_space.shape[0])
    onnx_path = "policy.onnx"
    torch.onnx.export(
        model, dummy_input, onnx_path,
        input_names=["obs"], output_names=["logits"],
        dynamo=True
    )

    # Load ONNX to validate
    onnx_model = onnx.load(onnx_path)
    onnx.checker.check_model(onnx_model)

    # Create input example for signature (as in MLflow)
    input_example = pd.DataFrame(
        np.random.randn(1, env.observation_space.shape[0]).astype(np.float32),
        columns=[f"obs_{i}" for i in range(env.observation_space.shape[0])]
    )

    # Define schema for model card (optional metadata)
    input_schema = [f"obs_{i}" for i in range(env.observation_space.shape[0])]
    output_schema = [f"logit_{i}" for i in range(env.action_space.n)]

    # Save ONNX as artifact
    artifact = wandb.Artifact("cartpole-policy-onnx", type="model")
    artifact.add_file(onnx_path)
    artifact.metadata.update({
        "input_shape": [1, env.observation_space.shape[0]],
        "output_shape": [1, env.action_space.n],
        "input_columns": input_schema,
        "output_columns": output_schema,
        "framework": "PyTorch -> ONNX",
        "exported_with": "torch.onnx.export",
        "dynamo": True
    })
    wandb.log_artifact(artifact)

    # Evaluation phase
    eval_df = evaluate(env, model, n_episodes=10)
    print("Evaluation results:")
    print(eval_df)

    # Log evaluation table to wandb
    eval_table = wandb.Table(dataframe=eval_df)
    wandb.log({"evaluation/results": eval_table})

    # Total runtime
    run_time = time.time() - run_start
    wandb.log({"training/total_run_time_sec": run_time})

    print(f"Run ID: {wandb.run.id}")
    print("Model exported and logged as artifact: cartpole-policy-onnx")

    # Finish run
    wandb.log({"_flush": True})
    wandb.finish()

if __name__ == "__main__":
    train()
