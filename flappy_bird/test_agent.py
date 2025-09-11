# test_agent.py
"""
Test a trained agent on the Flappy Bird environment.
"""

import gymnasium as gym
from stable_baselines3 import PPO
from flappy_bird_arcade import FlappyBirdEnv

def main():
    # Create the environment
    env = FlappyBirdEnv(render_mode="human")
    
    # Load the trained model
    model = PPO.load("flappy_bird_ppo")
    
    # Test the agent
    obs, _ = env.reset()
    for _ in range(10000):
        action, _states = model.predict(obs)
        obs, rewards, terminated, truncated, info = env.step(action)
        
        if terminated or truncated:
            print(f"Game ended with score: {info['score']}")
            obs, _ = env.reset()
    
    env.close()

if __name__ == "__main__":
    main()