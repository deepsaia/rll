# train_agent.py
"""
Example of training an agent on the Flappy Bird environment with enhanced logging using only loguru.
"""

import gymnasium as gym
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.env_checker import check_env
import time
from loguru import logger
import os

from flappy_bird.flappy_bird_arcade import FlappyBirdEnv

# Configure loguru
logger.add("flappy_bird/flappy_bird_training_{time}.log", rotation="500 MB")

# Custom callback for tracking episode rewards and other metrics
class TrainingCallback(BaseCallback):
    def __init__(self, total_timesteps, verbose=0):
        super().__init__(verbose)
        self.episode_rewards = []
        self.current_episode_reward = 0
        self.best_mean_reward = -np.inf
        self.total_timesteps = total_timesteps
        self.last_log_step = 0
        self.log_interval = max(1000, total_timesteps // 100)  # Log at least 100 times during training
        
    def _on_step(self) -> bool:
        # Get reward from the most recent step
        if "rewards" in self.locals:
            rewards = self.locals['rewards']
            dones = self.locals['dones']
            
            # Accumulate rewards and track completed episodes
            for i in range(len(rewards)):
                self.current_episode_reward += rewards[i]
                if dones[i]:
                    self.episode_rewards.append(self.current_episode_reward)
                    
                    # Log episode info
                    mean_reward = np.mean(self.episode_rewards[-100:]) if len(self.episode_rewards) >= 100 else np.mean(self.episode_rewards)
                    logger.info(f"Episode finished: Reward={self.current_episode_reward:.2f}, "
                               f"Mean reward (last 100)={mean_reward:.2f}, Timestep={self.num_timesteps}")
                    
                    # Save best model
                    if mean_reward > self.best_mean_reward:
                        self.best_mean_reward = mean_reward
                        self.model.save("flappy_bird_ppo_best")
                        logger.info(f"New best model saved with mean reward: {mean_reward:.2f}")
                        
                    self.current_episode_reward = 0
        
        # Log training progress at regular intervals
        if self.num_timesteps - self.last_log_step >= self.log_interval:
            progress_percent = (self.num_timesteps / self.total_timesteps) * 100
            if self.episode_rewards:
                current_mean = np.mean(self.episode_rewards[-100:]) if len(self.episode_rewards) >= 100 else np.mean(self.episode_rewards)
                logger.info(f"Training progress: {progress_percent:.1f}% | "
                           f"Timestep: {self.num_timesteps:,}/{self.total_timesteps:,} | "
                           f"Recent mean reward: {current_mean:.2f}")
            else:
                logger.info(f"Training progress: {progress_percent:.1f}% | "
                           f"Timestep: {self.num_timesteps:,}/{self.total_timesteps:,} | "
                           f"No episodes completed yet")
                           
            self.last_log_step = self.num_timesteps
            
        return True
    
    def _on_training_end(self) -> None:
        # Final summary
        if self.episode_rewards:
            final_mean_reward = np.mean(self.episode_rewards[-100:])
            logger.success(f"Training completed! Final mean reward (last 100 episodes): {final_mean_reward:.2f}")
            logger.success(f"Best mean reward achieved: {self.best_mean_reward:.2f}")
            logger.info(f"Total episodes completed: {len(self.episode_rewards)}")


def main():
    # Create the environment in headless mode for faster training
    env = FlappyBirdEnv(render_mode="headless")
    
    # Optional: Check environment for common errors
    try:
        check_env(env)
        logger.success("Environment passed gymnasium's environment check")
    except Exception as e:
        logger.error(f"Environment check failed: {e}")
    
    total_timesteps = 100000
    
    # Set up the PPO agent
    model = PPO(
        "MlpPolicy",
        env,
        verbose=0,  # We'll handle our own logging
        learning_rate=0.0003,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.01,
        # tensorboard_log="./flappy_bird_tensorboard/"
    )
    
    # Create callback instance
    callback = TrainingCallback(total_timesteps=total_timesteps, verbose=1)
    
    # Log training parameters
    logger.info("Starting Flappy Bird training with following parameters:")
    logger.info(f"Algorithm: [bold]PPO[/]")
    logger.info(f"Total timesteps: [bold]{total_timesteps:,}[/]")
    logger.info(f"Learning rate: [bold]{0.0003}[/]")
    logger.info(f"Gamma: [bold]{0.99}[/]")
    device_str = 'GPU' if model.device.type == 'cuda' else 'CPU'
    logger.info(f"Using [bold]{device_str}[/] for training")
    
    # Start timer
    start_time = time.time()
    
    try:
        # Train the agent
        logger.info("Beginning training...")
        model.learn(
            total_timesteps=total_timesteps,
            callback=callback,
            tb_log_name="PPO"
        )
        
        # Calculate and log training duration
        training_duration = time.time() - start_time
        logger.success(f"Training completed in {training_duration/60:.2f} minutes")
        
    except KeyboardInterrupt:
        logger.warning("Training interrupted by user")
    except Exception as e:
        logger.error(f"Training failed with error: {e}")
        raise
    
    finally:
        # Save the final model
        model.save("flappy_bird_ppo_final")
        logger.info("Final model saved as 'flappy_bird_ppo_final'")
        
        # Close the environment
        env.close()
        logger.info("Environment closed")


if __name__ == "__main__":
    main()