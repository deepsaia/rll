import numpy as np

# Define the MDP
class GridWorld:
    def __init__(self):
        self.states = [0, 1, 2, 3]          # 4 states
        self.actions = [0, 1, 2, 3]         # Up, Right, Down, Left
        self.goal = 3
        self.gamma = 0.9                    # Discount factor

        # Transition and reward model: P[s][a] = (s', r)
        self.P = {
            0: {  # State 0 (top-left)
                0: (0, 0),  # Up → stay
                1: (1, 0),  # Right → 1
                2: (2, 0),  # Down → 2
                3: (0, 0),  # Left → stay
            },
            1: {  # State 1 (top-right)
                0: (1, 0),
                1: (1, 0),  # Can't go right
                2: (3, 1),  # Down → goal! +1 reward
                3: (0, 0),  # Left → 0
            },
            2: {  # State 2 (bottom-left)
                0: (0, 0),
                1: (3, 1),  # Right → goal! +1 reward
                2: (2, 0),
                3: (2, 0),
            },
            3: {  # State 3 (goal)
                0: (3, 0),
                1: (3, 0),
                2: (3, 0),
                3: (3, 0),  # Stay in goal
            }
        }

    def reset(self):
        """Start at random non-goal state"""
        self.state = np.random.choice([0, 1, 2])
        return self.state, {}

    def step(self, action):
        """Execute action"""
        next_state, reward = self.P[self.state][action]
        self.state = next_state
        terminated = (next_state == self.goal)
        truncated = False
        info = {}
        return next_state, reward, terminated, truncated, info

    def render(self):
        grid = np.array(['⬜', '⬜', '⬜', '🏆']).reshape(2,2)
        pos = {0: (0,0), 1: (0,1), 2: (1,0), 3: (1,1)}
        agent_pos = [k for k,v in pos.items() if k == self.state][0]
        grid_display = grid.copy()
        if self.state != 3:
            i, j = pos[self.state]
            grid_display[i, j] = '🤖'
        print("\n".join(["".join(row) for row in grid_display]))

if __name__ == "__main__":
    env = GridWorld()
    state, info = env.reset()
    print(f"Start state: {state}")
    env.render()

    # Take a few steps
    for step in range(5):
        action = 1  # Always go right
        next_state, reward, terminated, truncated, info = env.step(action)
        print(f"Step {step+1}: Action=Right → State {next_state}, Reward={reward}")
        env.render()
        if terminated:
            print("🎉 Goal reached!")
            break