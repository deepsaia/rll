import gymnasium as gym
import numpy as np

# Create a simple environment: FrozenLake (4x4 grid)
env = gym.make("FrozenLake-v1", is_slippery=False, render_mode="human")

# Reset environment
state, info = env.reset()

# Take a random action
for _ in range(10):
    action = env.action_space.sample()
    next_state, reward, terminated, truncated, info = env.step(action)

    print(f"State: {state} → Action: {action} → Next State: {next_state}, Reward: {reward}")

env.close()
