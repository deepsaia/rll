import gymnasium as gym
import numpy as np
import time

# Create a simple environment
env = gym.make("CartPole-v1", render_mode="human")

# Reset the environment
state, info = env.reset()
print("Initial state:", state)
print("Info:", info)
print("Action space:", env.action_space)
print("Observation space:", env.observation_space)

# Run a random agent for 100 steps
for step in range(100):
    action = env.action_space.sample()  # Random action
    state, reward, terminated, truncated, info = env.step(action)
    print(f"Step {step}: Action={action}, State={state}, Reward={reward}")
    
    # Break if episode ends
    if terminated or truncated:
        print("Episode ended. Resetting...")
        state, info = env.reset()
    
    # Slow down so we can see
    time.sleep(0.02)

env.close()
print("Test complete!")