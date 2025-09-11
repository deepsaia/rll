# train_example.py
"""
Example of training an agent on the Flappy Bird environment with enhanced logging.
"""

import gymnasium as gym
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.env_checker import check_env
import time
from loguru import logger
from tqdm import tqdm
import os

from flappy_bird.flappy_bird_arcade import FlappyBirdEnv

# Configure loguru
logger.add("flappy_bird/flappy_bird_training_{time}.log", rotation="500 MB")

# Custom callback for tracking episode rewards and other metrics
class TrainingCallback(BaseCallback):
    def __init__(self, verbose=0):
        super().__init__(verbose)
        self.episode_rewards = []
        self.episode_lengths = []
        self.current_episode_reward = 0
        self.tqdm_progress = None
        self.best_mean_reward = -np.inf
        
    def _on_training_start(self) -> None:
        # Initialize tqdm progress bar
        total_steps = self.model.n_steps * self.model.n_epochs * (self.model.n_steps // self.model.n_steps + 1)
        # Since we can't get num_timesteps from DummyVecEnv, let's just use the total timesteps parameter
        self.tqdm_progress = tqdm(total=self.locals.get('total_timesteps', 100000), 
                                 desc="Training Progress", unit="steps")
        
    def _on_step(self) -> bool:
        # Get reward from the most recent step
        if hasattr(self.training_env, 'envs'):
            # Vectorized environment case
            rewards = self.locals['rewards']
            dones = self.locals['dones']
        else:
            # Single environment case
            rewards = [self.locals['rewards']]
            dones = [self.locals['dones']]
            
        # Accumulate rewards and track completed episodes
        for i in range(len(rewards)):
            self.current_episode_reward += rewards[i]
            if dones[i]:
                self.episode_rewards.append(self.current_episode_reward)
                self.episode_lengths.append(self.num_timesteps)
                
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
                
        # Update progress bar
        if self.tqdm_progress:
            self.tqdm_progress.update(1)
            
        return True
    
    def _on_training_end(self) -> None:
        if self.tqdm_progress:
            self.tqdm_progress.close()
            
        # Final summary
        if self.episode_rewards:
            final_mean_reward = np.mean(self.episode_rewards[-100:])
            logger.info(f"Training completed! Final mean reward (last 100 episodes): {final_mean_reward:.2f}")
            logger.info(f"Best mean reward achieved: {self.best_mean_reward:.2f}")
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
    callback = TrainingCallback(verbose=1)
    
    # Log training parameters
    logger.info("Starting Flappy Bird training with following parameters:")
    logger.info(f"Algorithm: PPO")
    logger.info(f"Total timesteps: 100,000")
    logger.info(f"Learning rate: 0.0003")
    logger.info(f"Gamma: 0.99")
    logger.info(f"Using {'GPU' if model.device.type == 'cuda' else 'CPU'} for training")
    
    # Start timer
    start_time = time.time()
    
    try:
        # Train the agent
        logger.info("Beginning training...")
        model.learn(
            total_timesteps=100000,
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