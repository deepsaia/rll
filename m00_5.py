import gymnasium as gym
import matplotlib.pyplot as plt

env = gym.make("CartPole-v1", render_mode="rgb_array")
env.reset()

# Take one step and grab image
_, _, _, _, _ = env.step(env.action_space.sample())
frame = env.render()  # Returns RGB array

plt.imshow(frame)
plt.title("CartPole Frame")
plt.axis("off")
plt.show()

env.close()