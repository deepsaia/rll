# monitor_training.py
"""
Script to monitor training progress by reading the log files.
"""

from loguru import logger
import matplotlib.pyplot as plt
import pandas as pd
import re
import time
from IPython.display import clear_output

def parse_log_file(log_file_path):
    """Parse the log file to extract training metrics."""
    rewards = []
    timesteps = []
    
    with open(log_file_path, 'r') as f:
        for line in f:
            # Look for lines containing episode reward information
            match = re.search(r"Episode finished: Reward=([-\d\.]+), Mean reward \(last 100\)=[-\d\.]+, Timestep=(\d+)", line)
            if match:
                reward = float(match.group(1))
                timestep = int(match.group(2))
                rewards.append(reward)
                timesteps.append(timestep)
    
    return timesteps, rewards

def plot_training_progress(log_file_path):
    """Create a live-updating plot of training progress."""
    plt.figure(figsize=(12, 8))
    
    while True:
        try:
            timesteps, rewards = parse_log_file(log_file_path)
            
            if len(rewards) > 0:
                clear_output(wait=True)
                plt.clf()
                
                # Plot raw rewards
                plt.subplot(2, 1, 1)
                plt.plot(timesteps, rewards, alpha=0.7)
                plt.title('Episode Rewards During Training')
                plt.ylabel('Reward')
                plt.grid(True)
                
                # Plot smoothed rewards (rolling average)
                plt.subplot(2, 1, 2)
                window_size = min(50, len(rewards))
                if window_size > 0:
                    rolling_mean = pd.Series(rewards).rolling(window=window_size).mean()
                    plt.plot(timesteps, rolling_mean, color='red', linewidth=2)
                plt.title('Rolling Average of Episode Rewards (Window: {})'.format(window_size))
                plt.xlabel('Timestep')
                plt.ylabel('Average Reward')
                plt.grid(True)
                
                plt.tight_layout()
                plt.show()
            
            # Update every 10 seconds
            time.sleep(10)
            
        except KeyboardInterrupt:
            print("Monitoring stopped.")
            break
        except Exception as e:
            # Don't crash if there's an error parsing the file
            time.sleep(5)
            continue

if __name__ == "__main__":
    # Find the latest log file
    import glob
    log_files = glob.glob("flappy_bird_training_*.log")
    if log_files:
        latest_log = max(log_files, key=os.path.getctime)
        print(f"Monitoring {latest_log}")
        plot_training_progress(latest_log)
    else:
        print("No log files found. Start training first.")