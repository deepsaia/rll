# train_example.py
"""
Example of training an agent on the Flappy Bird environment with rich and loguru integration.
"""

import gymnasium as gym
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.env_checker import check_env
import time
from loguru import logger
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TaskProgressColumn
from rich.logging import RichHandler
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
import sys

from flappy_bird.flappy_bird_arcade import FlappyBirdEnv

# Configure loguru to use rich handler for better console output
logger.remove()  # Remove default handler
console = Console()
logger.add(RichHandler(console=console, markup=True), format="{message}")

# Global variables for the live display
progress = None
live_display = None
main_progress_task = None
episode_table = None

class TrainingCallback(BaseCallback):
    def __init__(self, total_timesteps, verbose=0):
        super().__init__(verbose)
        self.episode_rewards = []
        self.current_episode_reward = 0
        self.best_mean_reward = -np.inf
        self.total_timesteps = total_timesteps
        self.episodes_completed = 0
        
        # Create progress bar using rich
        global progress, main_progress_task
        if progress is None:
            progress = Progress(
                TextColumn("[blue]Training"),
                BarColumn(),
                "[progress.percentage]{task.percentage:>3.1f}%",
                "•",
                TaskProgressColumn(),
                "•",
                TimeRemainingColumn(),
                console=console
            )
            main_progress_task = progress.add_task("Training", total=total_timesteps)
    
    def _on_training_start(self) -> None:
        # Initialize the live display layout
        global live_display, episode_table
        
        # Create a table for episode statistics
        episode_table = Table(title="Episode Statistics")
        episode_table.add_column("Metric", style="cyan")
        episode_table.add_column("Value", justify="right", style="green")
        
        # Create layout
        layout = Layout(name="root")
        
        # Divide into two parts: top for logs, bottom for progress
        layout.split_column(
            Layout(name="upper", ratio=8),
            Layout(name="progress", ratio=2)
        )
        
        # Further divide upper section
        layout["upper"].split_row(
            Layout(name="logs", ratio=7),
            Layout(name="stats", ratio=3)
        )
        
        # Update layouts
        layout["progress"].update(Panel(progress, title="Progress", border_style="blue"))
        layout["stats"].update(Panel(episode_table, title="Stats", border_style="green"))
        
        # Start live display
        if live_display is None:
            live_display = Live(layout, console=console, auto_refresh=True)
            live_display.start()
    
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
                    self.episodes_completed += 1
                    
                    # Log episode info
                    mean_reward = np.mean(self.episode_rewards[-100:]) if len(self.episode_rewards) >= 100 else np.mean(self.episode_rewards)
                    logger.info(f"Episode [bold green]{self.episodes_completed}[/] finished: Reward=[bold]{self.current_episode_reward:.2f}[/], Mean reward (last 100)=[bold]{mean_reward:.2f}[/]")
                    
                    # Save best model
                    if mean_reward > self.best_mean_reward:
                        self.best_mean_reward = mean_reward
                        self.model.save("flappy_bird_ppo_best")
                        logger.success(f"New best model saved with mean reward: {mean_reward:.2f}")
                        
                    self.current_episode_reward = 0
                    
                    # Update stats table
                    if episode_table and len(self.episode_rewards) > 0:
                        current_mean = np.mean(self.episode_rewards[-100:]) if len(self.episode_rewards) >= 100 else np.mean(self.episode_rewards)
                        episode_table.box = None
                        episode_table.columns.clear()
                        episode_table.add_column("Metric", style="cyan")
                        episode_table.add_column("Value", justify="right", style="green")
                        episode_table.add_row("Episodes", str(self.episodes_completed))
                        episode_table.add_row("Current Reward", f"{self.episode_rewards[-1]:.2f}")
                        episode_table.add_row("Mean (100)", f"{current_mean:.2f}")
                        episode_table.add_row("Best Mean", f"{self.best_mean_reward:.2f}")
        
        # Update progress bar
        if progress and main_progress_task is not None:
            # Calculate how many steps to update
            new_completed = min(self.num_timesteps, self.total_timesteps)
            current_completed = progress.tasks[main_progress_task].completed
            if new_completed > current_completed:
                progress.update(main_progress_task, completed=new_completed)
            
        return True
    
    def _on_training_end(self) -> None:
        # Final update to progress
        if progress and main_progress_task is not None:
            progress.update(main_progress_task, completed=self.total_timesteps)
        
        # Final summary
        if self.episode_rewards:
            final_mean_reward = np.mean(self.episode_rewards[-100:])
            logger.success(f"[bold]Training completed![/] Final mean reward (last 100 episodes): [bold]{final_mean_reward:.2f}[/]")
            logger.success(f"Best mean reward achieved: [bold]{self.best_mean_reward:.2f}[/]")
            logger.info(f"Total episodes completed: [bold]{len(self.episode_rewards)}[/]")


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
    
    total_timesteps = 100000
    
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
        logger.success(f"Training completed in [bold]{training_duration/60:.2f}[/] minutes")
        
    except KeyboardInterrupt:
        logger.warning("Training interrupted by user")
    except Exception as e:
        logger.error(f"Training failed with error: {e}")
        raise
    
    finally:
        # Stop the live display
        global live_display
        if live_display:
            live_display.stop()
        
        # Save the final model
        model.save("flappy_bird_ppo_final")
        logger.info("Final model saved as '[bold]flappy_bird_ppo_final[/]'")
        
        # Close the environment
        env.close()
        logger.info("Environment closed")


if __name__ == "__main__":
    main()