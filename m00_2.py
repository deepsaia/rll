import gymnasium as gym
import numpy as np

class RandomAgent:
    def __init__(self, action_space):
        self.action_space = action_space
    
    def act(self, obs):
        return self.action_space.sample()  # pick random action

def run_random_agent(episodes=5):
    env = gym.make("CartPole-v1", render_mode="human")
    agent = RandomAgent(env.action_space)

    for ep in range(episodes):
        obs, info = env.reset()
        total_reward = 0
        done = False
        while not done:
            action = agent.act(obs)
            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            done = terminated or truncated
        print(f"Episode {ep+1} reward: {total_reward}")
    
    env.close()

if __name__ == "__main__":
    run_random_agent()
