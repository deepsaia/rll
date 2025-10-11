import gymnasium as gym
import matplotlib.pyplot as plt

def run_and_log(episodes=100):
    env = gym.make("CartPole-v1")
    rewards = []
    total_reward = 0
    for ep in range(episodes):
        obs, info = env.reset()
        done = False
        while not done:
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            done = terminated or truncated
        rewards.append(total_reward)
    
    env.close()
    return rewards

rewards = run_and_log(200)
plt.plot(rewards)
plt.xlabel("Episode")
plt.ylabel("Total reward")
plt.title("Random Agent on CartPole")
plt.show()
