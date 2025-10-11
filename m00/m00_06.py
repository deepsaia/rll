import gymnasium as gym
import numpy as np

def run_random_agent(env_name, max_episodes=5, max_steps=200):
    # Create environment
    env = gym.make(env_name, render_mode="human")
    total_rewards = []

    for episode in range(max_episodes):
        state, info = env.reset()
        episode_reward = 0
        print(f"\n--- Episode {episode + 1} ---")
        print(f"Initial state: {state}")

        for step in range(max_steps):
            # Choose random action
            action = env.action_space.sample()
            
            # Step the environment
            next_state, reward, terminated, truncated, info = env.step(action)
            episode_reward += reward

            # Log
            if step % 50 == 0:
                print(f"  Step {step}: Action={action}, State={next_state}, Reward={reward}")

            # Update state
            state = next_state

            # Check if episode is done
            if terminated or truncated:
                print(f"  Episode ended after {step + 1} steps. Total reward: {episode_reward}")
                break

        total_rewards.append(episode_reward)

    env.close()
    print(f"\nAverage reward over {max_episodes} episodes: {np.mean(total_rewards):.2f}")
    return total_rewards

# Run it
# rewards = run_random_agent("CartPole-v1")
rewards = run_random_agent("FrozenLake-v1")

import matplotlib.pyplot as plt

plt.plot(rewards, marker='o')
plt.title("Random Agent Performance")
plt.xlabel("Episode")
plt.ylabel("Total Reward")
plt.grid(True)
plt.show()