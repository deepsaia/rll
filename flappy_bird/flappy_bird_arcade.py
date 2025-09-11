# flappy_bird_arcade.py
"""
Flappy Bird environment using Arcade library with Gymnasium interface.
"""

import time
import arcade
import numpy as np
import gymnasium as gym
from gymnasium import spaces
import random

# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.5
BIRD_JUMP = -8
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_SPAWN_INTERVAL = 150  # frames
FLOOR_HEIGHT = 100

class Bird:
    """Represents the bird in the game."""
    
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.width = 30
        self.height = 30
        self.alive = True
    
    def update(self):
        """Update bird position and velocity."""
        self.velocity += GRAVITY
        self.y += self.velocity
        
        # Check if bird hits the ground or ceiling
        if self.y <= FLOOR_HEIGHT + self.height / 2:
            self.y = FLOOR_HEIGHT + self.height / 2
            self.velocity = 0
            self.alive = False
        elif self.y >= SCREEN_HEIGHT - self.height / 2:
            self.y = SCREEN_HEIGHT - self.height / 2
            self.velocity = 0
    
    def jump(self):
        """Make the bird jump."""
        self.velocity = BIRD_JUMP


class Pipe:
    """Represents a pipe pair (top and bottom) in the game."""
    
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(PIPE_GAP, SCREEN_HEIGHT - FLOOR_HEIGHT - PIPE_GAP)
        self.passed = False
        self.width = 60
        
    def update(self):
        """Update pipe position."""
        self.x -= PIPE_SPEED
        
    def collides_with(self, bird):
        """Check if the pipe collides with the bird."""
        # Check if bird is within horizontal bounds of pipe
        if (bird.x + bird.width / 2 > self.x - self.width / 2 and 
            bird.x - bird.width / 2 < self.x + self.width / 2):
            
            # Check if bird is within vertical bounds of gap
            top_pipe_bottom = self.gap_y - PIPE_GAP / 2
            bottom_pipe_top = self.gap_y + PIPE_GAP / 2
            
            if (bird.y - bird.height / 2 < top_pipe_bottom or 
                bird.y + bird.height / 2 > bottom_pipe_top):
                return True
                
        return False


class FlappyBirdGame(arcade.Window):
    """Main game class using Arcade."""
    
    def __init__(self, width, height, render_mode="human"):
        super().__init__(width, height, "Flappy Bird", visible=(render_mode != "headless"))
        self.render_mode = render_mode
        self.bird = None
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.frame_count = 0
        
        # Set background color
        arcade.set_background_color(arcade.color.SKY_BLUE)
        
        # Create text objects for better performance
        self.score_text = arcade.Text("Score: 0", 10, SCREEN_HEIGHT - 30, arcade.color.BLACK, 24)
        self.game_over_text = arcade.Text("Game Over! Press R to restart", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 
                                        arcade.color.RED, 20, anchor_x="center")
        
        # Setup the game
        self.setup()
    
    def setup(self):
        """Set up the game."""
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.frame_count = 0
        
        # Add first pipe
        self.pipes.append(Pipe(SCREEN_WIDTH + 100))
    
    def on_update(self, delta_time):
        """Update the game state."""
        if self.game_over:
            return
            
        self.frame_count += 1
        
        # Update bird
        self.bird.update()
        
        # Update pipes
        for pipe in self.pipes:
            pipe.update()
            
            # Check collisions
            if pipe.collides_with(self.bird):
                self.bird.alive = False
                self.game_over = True
                
            # Check if pipe is passed
            if not pipe.passed and pipe.x + pipe.width / 2 < self.bird.x:
                pipe.passed = True
                self.score += 1
                
        # Remove off-screen pipes
        self.pipes = [pipe for pipe in self.pipes if pipe.x > -pipe.width / 2]
        
        # Add new pipes
        if self.frame_count % PIPE_SPAWN_INTERVAL == 0:
            self.pipes.append(Pipe(SCREEN_WIDTH + 100))
            
        # Check if bird is dead
        if not self.bird.alive:
            self.game_over = True
    
    def on_draw(self):
        """Render the game."""
        self.clear()
        
        # Draw floor
        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, FLOOR_HEIGHT, 
            arcade.color.DARK_BROWN
        )
        
        # Draw bird
        arcade.draw_lrbt_rectangle_filled(
            self.bird.x - self.bird.width / 2, 
            self.bird.x + self.bird.width / 2,
            self.bird.y - self.bird.height / 2,
            self.bird.y + self.bird.height / 2,
            arcade.color.YELLOW
        )
        
        # Draw eyes
        arcade.draw_circle_filled(self.bird.x + 8, self.bird.y + 8, 4, arcade.color.BLACK)
        
        # Draw beak
        points = [
            (self.bird.x + 15, self.bird.y),
            (self.bird.x + 25, self.bird.y + 5),
            (self.bird.x + 25, self.bird.y - 5)
        ]
        arcade.draw_polygon_filled(points, arcade.color.ORANGE)
        
        # Draw pipes
        for pipe in self.pipes:
            # Top pipe
            top_height = pipe.gap_y - PIPE_GAP / 2
            arcade.draw_lrbt_rectangle_filled(
                pipe.x - pipe.width / 2,
                pipe.x + pipe.width / 2,
                0, 
                top_height,
                arcade.color.GREEN
            )
            
            # Bottom pipe
            bottom_y = pipe.gap_y + PIPE_GAP / 2
            arcade.draw_lrbt_rectangle_filled(
                pipe.x - pipe.width / 2,
                pipe.x + pipe.width / 2,
                bottom_y, 
                SCREEN_HEIGHT,
                arcade.color.GREEN
            )
        
        # Update and draw score text
        self.score_text.text = f"Score: {self.score}"
        self.score_text.draw()
        
        # Draw game over message
        if self.game_over:
            self.game_over_text.draw()
    
    def on_key_press(self, key, modifiers):
        """Handle key presses."""
        if key == arcade.key.SPACE or key == arcade.key.UP:
            if not self.game_over:
                self.bird.jump()
        elif key == arcade.key.R:
            self.setup()
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
    
    def get_observation(self):
        """Get the current observation for RL agent."""
        # Find the next pipe
        next_pipe = None
        for pipe in self.pipes:
            if pipe.x + pipe.width / 2 > self.bird.x:
                next_pipe = pipe
                break
                
        if next_pipe is None:
            # If no pipe found, create a dummy one far away
            next_pipe_x = self.bird.x + SCREEN_WIDTH
            gap_y = SCREEN_HEIGHT // 2
        else:
            next_pipe_x = next_pipe.x
            gap_y = next_pipe.gap_y
            
        # Calculate horizontal distance to next pipe
        pipe_dist = next_pipe_x - self.bird.x
        
        # Get pipe gap positions
        pipe_top = gap_y - PIPE_GAP / 2
        pipe_bottom = gap_y + PIPE_GAP / 2
        
        return np.array([
            self.bird.y,
            self.bird.velocity,
            pipe_dist,
            pipe_top,
            pipe_bottom
        ], dtype=np.float32)
    
    def get_info(self):
        """Get additional info."""
        return {
            'score': self.score,
            'bird_alive': self.bird.alive
        }
    
    def step(self, action):
        """Execute one time step."""
        # Apply action
        if action == 1:  # Jump
            self.bird.jump()
            
        # Update game state
        self.on_update(1/60)
        
        # Get observation
        observation = self.get_observation()
        
        # Calculate reward
        reward = 0.1  # Small survival reward
        
        # Additional reward for passing pipes
        current_score = self.score
        if hasattr(self, '_prev_score'):
            if current_score > self._prev_score:
                reward += 10.0  # Reward for passing a pipe
        self._prev_score = current_score
        
        # Penalty for dying
        if not self.bird.alive:
            reward = -10.0
            
        # Get info
        info = self.get_info()
        
        # Check if done
        terminated = not self.bird.alive
        truncated = False
        
        return observation, reward, terminated, truncated, info
    
    def reset(self):
        """Reset the game."""
        self.setup()
        observation = self.get_observation()
        info = self.get_info()
        return observation, info


class FlappyBirdEnv(gym.Env):
    """
    Flappy Bird Gymnasium environment using Arcade for rendering.
    
    Observation Space:
        - bird_y: vertical position of bird
        - bird_velocity: vertical velocity of bird
        - next_pipe_dist_to_bird: horizontal distance to next pipe
        - next_pipe_top: y position of top of next pipe gap
        - next_pipe_bottom: y position of bottom of next pipe gap
    
    Action Space:
        - 0: Do nothing
        - 1: Jump
    """
    
    metadata = {
        'render_modes': ['human', 'rgb_array', 'headless'],
        'render_fps': 60,
    }
    
    def __init__(self, render_mode=None):
        super().__init__()
        
        self.render_mode = render_mode
        self.game_window = None
        
        # Define action and observation space
        self.action_space = spaces.Discrete(2)  # 0: do nothing, 1: jump
        
        # Observation space: [bird_y, bird_vel, pipe_dist, pipe_top, pipe_bottom]
        self.observation_space = spaces.Box(
            low=np.array([0, -10, 0, 0, 0]),
            high=np.array([SCREEN_HEIGHT, 10, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_HEIGHT]),
            dtype=np.float32
        )
        
        # Initialize game window only for human rendering mode
        if render_mode == "human":
            self.game_window = FlappyBirdGame(SCREEN_WIDTH, SCREEN_HEIGHT, render_mode)
        else:
            # For non-human modes, we'll use a headless approach
            self.game_state = None
            self.reset()
    
    def _create_game_state(self):
        """Create a new game state for headless mode."""
        return {
            'bird': Bird(),
            'pipes': [],
            'score': 0,
            'game_over': False,
            'frame_count': 0
        }
    
    def _update_game_state(self, state, action):
        """Update the game state based on action."""
        # Apply action
        if action == 1:  # Jump
            state['bird'].jump()
            
        # Update bird
        state['bird'].update()
        
        # Update pipes
        for pipe in state['pipes']:
            pipe.update()
            
            # Check collisions
            if pipe.collides_with(state['bird']):
                state['bird'].alive = False
                state['game_over'] = True
                
            # Check if pipe is passed
            if not pipe.passed and pipe.x + pipe.width / 2 < state['bird'].x:
                pipe.passed = True
                state['score'] += 1
                
        # Remove off-screen pipes
        state['pipes'] = [pipe for pipe in state['pipes'] if pipe.x > -pipe.width / 2]
        
        # Add new pipes
        state['frame_count'] += 1
        if state['frame_count'] % PIPE_SPAWN_INTERVAL == 0:
            state['pipes'].append(Pipe(SCREEN_WIDTH + 100))
            
        # Check if bird is dead
        if not state['bird'].alive:
            state['game_over'] = True
            
        return state
    
    def _get_observation_from_state(self, state):
        """Get observation from game state."""
        # Find the next pipe
        next_pipe = None
        for pipe in state['pipes']:
            if pipe.x + pipe.width / 2 > state['bird'].x:
                next_pipe = pipe
                break
                
        if next_pipe is None:
            # If no pipe found, create a dummy one far away
            next_pipe_x = state['bird'].x + SCREEN_WIDTH
            gap_y = SCREEN_HEIGHT // 2
        else:
            next_pipe_x = next_pipe.x
            gap_y = next_pipe.gap_y
            
        # Calculate horizontal distance to next pipe
        pipe_dist = next_pipe_x - state['bird'].x
        
        # Get pipe gap positions
        pipe_top = gap_y - PIPE_GAP / 2
        pipe_bottom = gap_y + PIPE_GAP / 2
        
        return np.array([
            state['bird'].y,
            state['bird'].velocity,
            pipe_dist,
            pipe_top,
            pipe_bottom
        ], dtype=np.float32)
    
    def _get_info_from_state(self, state):
        """Get info from game state."""
        return {
            'score': state['score'],
            'bird_alive': state['bird'].alive
        }
    
    def reset(self, seed=None, options=None):
        """Reset the environment."""
        super().reset(seed=seed)
        
        if self.render_mode == "human":
            # For human rendering mode, ensure the game window is properly initialized and reset
            if self.game_window is None:
                self.game_window = FlappyBirdGame(SCREEN_WIDTH, SCREEN_HEIGHT, self.render_mode)
            # Reset the game window state directly instead of calling reset()
            self.game_window.setup()
            
            # Get observation and info from the game window
            observation = self._get_observation_from_game_window()
            info = {
                'score': self.game_window.score,
                'bird_alive': self.game_window.bird.alive
            }
            return observation, info
        else:
            # Headless mode
            self.game_state = self._create_game_state()
            self.game_state['pipes'].append(Pipe(SCREEN_WIDTH + 100))
            
            observation = self._get_observation_from_state(self.game_state)
            info = self._get_info_from_state(self.game_state)
            return observation, info
    
    def step(self, action):
        """Execute one time step."""
        if self.render_mode == "human":
            # In human mode, we need to apply the action and update the game directly
            if self.game_window is None:
                raise RuntimeError("Game window not initialized")
                
            # Apply action to the bird
            if action == 1:  # Jump
                self.game_window.bird.jump()
                
            # Update game state (using a fixed delta_time)
            self.game_window.on_update(1/60)
            
            # Get observation
            observation = self._get_observation_from_game_window()
            
            # Calculate reward
            reward = 0.1  # Small survival reward
            
            # Additional reward for passing pipes
            current_score = self.game_window.score
            if hasattr(self, '_prev_score'):
                if current_score > self._prev_score:
                    reward += 10.0  # Reward for passing a pipe
            self._prev_score = current_score
            
            # Penalty for dying
            if not self.game_window.bird.alive:
                reward = -10.0
                
            # Get info
            info = {
                'score': self.game_window.score,
                'bird_alive': self.game_window.bird.alive
            }
            
            # Check if done
            terminated = not self.game_window.bird.alive
            truncated = False
            
            # For human rendering, we need to ensure the display is updated
            if self.render_mode == "human":
                # Process events and draw
                self.game_window.switch_to()
                self.game_window.dispatch_events()
                self.game_window.clear()
                self.game_window.on_draw()
                self.game_window.flip()
                
            return observation, reward, terminated, truncated, info
        else:
            # Headless mode - update our internal game state
            self.game_state = self._update_game_state(self.game_state, action)
            
            # Get observation
            observation = self._get_observation_from_state(self.game_state)
            
            # Calculate reward
            reward = 0.1  # Small survival reward
            
            # Additional reward for passing pipes
            current_score = self.game_state['score']
            if hasattr(self, '_prev_score'):
                if current_score > self._prev_score:
                    reward += 10.0  # Reward for passing a pipe
            self._prev_score = current_score
            
            # Penalty for dying
            if not self.game_state['bird'].alive:
                reward = -10.0
                
            # Get info
            info = self._get_info_from_state(self.game_state)
            
            # Check if done
            terminated = not self.game_state['bird'].alive
            truncated = False
            
            return observation, reward, terminated, truncated, info

    def _get_observation_from_game_window(self):
        """Get observation from the game window (human mode)."""
        # Find the next pipe
        next_pipe = None
        for pipe in self.game_window.pipes:
            if pipe.x + pipe.width / 2 > self.game_window.bird.x:
                next_pipe = pipe
                break
                
        if next_pipe is None:
            # If no pipe found, create a dummy one far away
            next_pipe_x = self.game_window.bird.x + SCREEN_WIDTH
            gap_y = SCREEN_HEIGHT // 2
        else:
            next_pipe_x = next_pipe.x
            gap_y = next_pipe.gap_y
            
        # Calculate horizontal distance to next pipe
        pipe_dist = next_pipe_x - self.game_window.bird.x
        
        # Get pipe gap positions
        pipe_top = gap_y - PIPE_GAP / 2
        pipe_bottom = gap_y + PIPE_GAP / 2
        
        return np.array([
            self.game_window.bird.y,
            self.game_window.bird.velocity,
            pipe_dist,
            pipe_top,
            pipe_bottom
        ], dtype=np.float32)
    
    def render(self):
        """Render the environment."""
        if self.render_mode == "human" and self.game_window:
            # Let the Arcade event loop handle rendering
            pass
        elif self.render_mode == "rgb_array":
            # This would require capturing the screen as an array
            pass
            
    def close(self):
        """Close the environment."""
        if self.game_window:
            self.game_window.close()
            self.game_window = None


# Example usage
if __name__ == "__main__":
    # Create the environment with human rendering for visualization
    env = FlappyBirdEnv(render_mode="human")
    
    # Run a simple demonstration
    observation, info = env.reset()
    
    try:
        # Start the Arcade event loop which will handle all rendering and updates
        arcade.run()
    except KeyboardInterrupt:
        print("Closing environment...")
    finally:
        env.close()
