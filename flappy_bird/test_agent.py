# test_agent.py
"""
Test a trained agent on the Flappy Bird environment.
"""

import gymnasium as gym
from stable_baselines3 import PPO
from flappy_bird.flappy_bird_arcade import FlappyBirdEnv
import time

def main():
    # Create the environment
    env = FlappyBirdEnv(render_mode="human")
    
    # Load the trained model
    try:
        model = PPO.load("flappy_bird_ppo_best")
        print("Model loaded successfully!")
    except FileNotFoundError:
        print("Could not find 'flappy_bird_ppo' model. Make sure you've trained it first.")
        print("Run train_example.py to train a model.")
        return
    except Exception as e:
        print(f"Error loading model: {e}")
        return
    
    # Test the agent
    print("Starting agent test. Close the window or press Ctrl+C to stop.")
    
    obs, _ = env.reset()
    
    try:
        episode_count = 0
        total_scores = []
        
        while True:  # Continue until user closes window
            action, _states = model.predict(obs)
            obs, rewards, terminated, truncated, info = env.step(action)
            
            if terminated or truncated:
                score = info['score']
                episode_count += 1
                total_scores.append(score)
                avg_score = sum(total_scores) / len(total_scores)
                print(f"Game {episode_count} ended with score: {score}, Average: {avg_score:.2f}")
                
                # Reset for new episode
                obs, _ = env.reset()
                
                # Optional: exit after certain number of episodes
                if episode_count >= 100:
                    break
                    
    except KeyboardInterrupt:
        print("\nTesting interrupted by user.")
    except Exception as e:
        print(f"Error during testing: {e}")
    finally:
        # Print final statistics
        if total_scores:
            print(f"\nTest Results:")
            print(f"Episodes completed: {len(total_scores)}")
            print(f"Average score: {sum(total_scores) / len(total_scores):.2f}")
            print(f"Best score: {max(total_scores)}")
            print(f"Worst score: {min(total_scores)}")
        
        env.close()
        print("Environment closed.")

if __name__ == "__main__":
    main()