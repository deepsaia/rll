"""Generate data for Module 00 charts.

Produces CSV files consumed by the Docusaurus chart components:
  - random_agent_rewards.csv: episode rewards for a random CartPole agent
  - environment_comparison.csv: random agent performance across environments

Usage:
    python scripts/generate_m00_data.py
"""

import csv
from pathlib import Path

import gymnasium as gym
import numpy as np

OUTPUT_DIR = Path(__file__).parent.parent / "website" / "static" / "data" / "m00"


def generate_random_agent_rewards(
    env_name: str = "CartPole-v1",
    episodes: int = 200,
    seed: int = 42,
) -> list[dict]:
    """Run a random agent and record per-episode rewards."""
    env = gym.make(env_name)
    rng = np.random.default_rng(seed)
    rows = []
    for ep in range(episodes):
        obs, _ = env.reset(seed=int(rng.integers(0, 2**31)))
        total_reward = 0.0
        done = False
        steps = 0
        while not done:
            action = env.action_space.sample()
            obs, reward, terminated, truncated, _ = env.step(action)
            total_reward += reward
            steps += 1
            done = terminated or truncated
        rows.append({"episode": ep, "reward": total_reward, "steps": steps})
    env.close()
    return rows


def generate_environment_comparison(seed: int = 42) -> list[dict]:
    """Compare random agent performance across environments."""
    envs = [
        ("CartPole-v1", 100),
        ("MountainCar-v0", 50),
        ("Acrobot-v1", 50),
    ]
    rows = []
    for env_name, n_episodes in envs:
        env = gym.make(env_name)
        rng = np.random.default_rng(seed)
        rewards = []
        for _ in range(n_episodes):
            obs, _ = env.reset(seed=int(rng.integers(0, 2**31)))
            total_reward = 0.0
            done = False
            while not done:
                action = env.action_space.sample()
                obs, reward, terminated, truncated, _ = env.step(action)
                total_reward += reward
                done = terminated or truncated
            rewards.append(total_reward)
        env.close()
        rows.append({
            "environment": env_name,
            "mean_reward": round(float(np.mean(rewards)), 2),
            "std_reward": round(float(np.std(rewards)), 2),
            "min_reward": round(float(np.min(rewards)), 2),
            "max_reward": round(float(np.max(rewards)), 2),
            "max_possible": {"CartPole-v1": 500, "MountainCar-v0": -110, "Acrobot-v1": -100}.get(env_name, 0),
        })
    return rows


def write_csv(rows: list[dict], filename: str) -> None:
    path = OUTPUT_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {path}")


if __name__ == "__main__":
    write_csv(generate_random_agent_rewards(), "random_agent_rewards.csv")
    write_csv(generate_environment_comparison(), "environment_comparison.csv")
