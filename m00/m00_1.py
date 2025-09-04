import gymnasium as gym

env = gym.make("CartPole-v1", render_mode="human")  # environment
state, info = env.reset()  # reset, returns initial state

for i in range(1000):
    action = env.action_space.sample()  # random action
    next_state, reward, terminated, truncated, info = env.step(action)

    if i % 10 == 0:
        print(f"State: {state} → Action: {action} → Next State: {next_state}, Reward: {reward}")
    if terminated or truncated:
        state, info = env.reset()

env.close()
