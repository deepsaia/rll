# RL

---

# Quick roadmap (high level)

1. Foundations: Problem setup, MDPs, dynamic programming, tabular algorithms.
2. Core model-free methods: Monte Carlo, TD, Q-learning, SARSA (tabular → function approximation).
3. Policy methods: Policy gradients, REINFORCE, actor-critic.
4. Deep RL: DQN family, DDPG, PPO, A3C/IMPALA, SAC.
5. Advanced topics: model-based RL, exploration, offline RL, hierarchical/meta RL, multi-agent RL, safety/robustness.
6. Research & production: RL at scale, reproducibility, benchmarking, papers and open problems.

---

# Recommended canonical resources (start here)

* **Sutton & Barto — *Reinforcement Learning: An Introduction*** — the standard theoretical text for fundamentals. ([andrew.cmu.edu][1], [Stanford University][2])
* **David Silver’s RL course (video + notes)** — excellent lecture sequence that maps to Sutton & Barto and explains intuition and algorithms. ([David Silver][3], [GitHub][4])
* **OpenAI “Spinning Up in Deep RL”** — practical, tutorial-style resource with clean PyTorch-ish code, great for learning how to implement and debug deep RL algorithms. ([spinningup.openai.com][5], [GitHub][6])
* **Stable-Baselines3 (SB3)** — production-quality implementations of many modern RL algorithms (useful for experiments and baselines). ([stable-baselines3.readthedocs.io][7], [GitHub][8])
* **Survey papers (e.g., Arulkumaran et al. 2017/2018)** — compact historical overview and taxonomy of deep RL approaches. ([arXiv][9], [cs.columbia.edu][10])

---

# Prerequisites

* **Math:** linear algebra (vectors, matrices, eigen stuff), multivariable calculus (gradients), probability (expectations, distributions, conditional), basics of optimization (SGD), and Markov chains.
* **Coding:** Python (numpy), PyTorch (or TensorFlow), basics of creating experiments, logging, and plotting. Familiarity with OpenAI Gym (or similar envs) is helpful.
* **Tools:** Git, conda/venv, Jupyter, Docker (optional), and familiarity with GitHub for reading code.

---

# Detailed syllabus with projects & exercises

### Module 0 — Setup & tiny warmups (1 week)

* Install Python, set up conda env, install PyTorch, Gym, Stable-Baselines3, and Spinning Up repo.
* Tiny tasks: implement a small random agent for CartPole-v1 (Gym) and log episode rewards.

**Why:** get tooling right before deep dives.

---

### Module 1 — Foundations & MDPs (1–2 weeks)

* Topics: MDP definition (states, actions, rewards, transitions, discounting), return, episodic vs continuing, Bellman equation, value functions.
* Read: Sutton & Barto chapters on MDPs and value functions. ([Stanford University][2])
* Exercise: implement **Value Iteration** and **Policy Iteration** on a small GridWorld. Prove Bellman optimality backup.

**Milestone:** You can derive Bellman equations and implement DP solvers.

---

### Module 2 — Tabular model-free methods (2–3 weeks)

* Topics: Monte-Carlo prediction/control, Temporal-Difference (TD(0)), SARSA, Q-learning, eligibility traces (TD(λ)).
* Hands-on: implement **ε-greedy Q-learning** for FrozenLake and CartPole (discrete). Compare MC vs TD learning curves.
* Reading: Sutton & Barto chapters on model-free learning.

**Milestone:** You can implement tabular Q-learning and analyze convergence behaviors.

---

### Module 3 — Function approximation & stability (2–3 weeks)

* Topics: linear function approx, feature engineering, instability of naïve function-approximation with off-policy updates, gradient-TD methods (overview).
* Hands-on: use a small neural network (PyTorch) to approximate Q(s,a) for a continuous-state environment (MountainCar). Observe divergence issues and mitigation (replay buffer, target network).
* Read: relevant sections in Sutton & Barto and tutorials from Spinning Up. ([spinningup.openai.com][5], [Stanford University][2])

**Milestone:** You understand why naive bootstrapping + function approximation can diverge and how practical tricks help.

---

### Module 4 — Value-based deep RL (3–4 weeks)

* Topics: Deep Q-Network (DQN), experience replay, target networks, Double DQN, dueling networks, prioritized replay.
* Hands-on project: implement a DQN on Atari/CartPole from scratch (or follow Spinning Up / OpenAI pseudocode), then run SB3’s DQN for comparison. ([spinningup.openai.com][5], [stable-baselines3.readthedocs.io][7])
* Read: DQN paper, follow-up improvements (Double DQN, Dueling DQN papers).

**Milestone:** Train a DQN that achieves nontrivial performance on a Gym task.

---

### Module 5 — Policy gradient & actor-critic (3–4 weeks)

* Topics: REINFORCE, baseline subtraction, variance reduction, Actor-Critic, A2C/A3C, Trust Region Policy Optimization (TRPO), Proximal Policy Optimization (PPO).
* Hands-on: implement REINFORCE and a simple Actor-Critic; then run SB3’s PPO and compare. Use continuous-control envs (Pendulum, Hopper in MuJoCo or similar). ([stable-baselines3.readthedocs.io][7], [GitHub][6])

**Milestone:** You can implement policy gradient and actor-critic algorithms and understand trade-offs.

---

### Module 6 — Off-policy continuous control & modern methods (3–4 weeks)

* Topics: DDPG, TD3, Soft Actor-Critic (SAC), sample efficiency, stability for continuous actions.
* Hands-on: run SB3/other implementations for SAC/TD3 on continuous control benchmarks; attempt to tune hyperparameters for sample efficiency. ([stable-baselines3.readthedocs.io][7])

**Milestone:** You can train a continuous-control policy that performs decently and understand hyperparameter sensitivity.

---

### Module 7 — Advanced topics (4–6+ weeks — pick subtopics)

Pick several and dive deep:

* **Model-based RL:** learning dynamics models, planning (MPC), imagination-augmented agents.
* **Exploration & intrinsic motivation:** curiosity, RND, count-based methods.
* **Offline (batch) RL:** learning from fixed datasets (CQL, BRAC).
* **Hierarchical RL & meta-RL:** options, FeUdal networks, MAML-style meta-learning.
* **Multi-agent RL (MARL).**
* **Safety, robustness, and interpretability.**

**Hands-on:** replicate a recent paper’s experiment (pick one from OpenAI/DeepMind/ICLR/NeurIPS). Use Spinning Up reading lists and survey papers to pick targets. ([spinningup.openai.com][5], [arXiv][9])

**Milestone:** You can read a modern RL paper and reproduce its core experiment or baseline.

---

### Module 8 — Research & production (ongoing)

* Topics: scaling RL (distributed training), reproducibility, benchmarks (Atari, DM Control Suite), logging & evaluation, sim2real transfer for robotics.
* Tools: RLlib, Acme, Stable-Baselines3, Hydra for configs, Weights & Biases or TensorBoard for logging. ([stable-baselines3.readthedocs.io][7])

**Milestone:** Launch scalable experiments, run hyperparameter sweeps, and produce reproducible results.

---

# Suggested 6-month schedule (flexible)

* Months 0–1: Modules 0–2 (foundations + tabular).
* Months 1–3: Modules 3–5 (function approx, DQN, policy gradients).
* Months 3–5: Module 6 + initial advanced topics.
* Months 5–6+: Modules 7–8, research reproduction, capstone project.

If you want mastery faster, increase time per week and do more parallel coding/reading. For real research-level mastery expect \~12+ months of focused work (reading papers + contributing code).

---

# Practical projects (capstone ideas)

1. **Classic RL pipeline:** from scratch DQN on Atari (or simplified analog), compare with SB3 baseline.
2. **Robust continuous control:** train SAC on a MuJoCo-like task and test robustness to domain shifts.
3. **Offline RL project:** apply CQL on D4RL dataset and compare to behavior cloning and offline TD3.
4. **Sim2Real robotics:** train in sim, deploy to a small real robot (or sim-to-sim transfer experiments).
5. **Reproduce a NeurIPS/ICLR paper** and write a short blog: methods, bugs encountered, results.

---

# Coding workflow & best practices

* Start with **Spinning Up** implementations and tests. ([spinningup.openai.com][5])
* Use **Stable-Baselines3** as a reliable implementation baseline for experiments. ([stable-baselines3.readthedocs.io][7])
* Log experiments (WandB/TensorBoard), fix random seeds, and run multiple seeds to estimate variance.
* Keep hyperparameter config files (Hydra/YAML), and write unit tests for core components (replay buffer, networks).
* Be wary of compute: RL experiments can be expensive. Start small, profile, then scale.

---

# Papers & reading sequence (starter list)

* Sutton & Barto (book) — foundations. ([Stanford University][2])
* David Silver course (lecture videos/notes) — mapping intuition to math. ([David Silver][3], [GitHub][4])
* Mnih et al., DQN (2015) and followups (Double DQN, prioritized replay).
* Schulman et al., TRPO / PPO papers.
* Lillicrap et al., DDPG; Fujimoto et al., TD3; Haarnoja et al., SAC.
* Surveys: Arulkumaran et al. (2017/2018). ([arXiv][9], [cs.columbia.edu][10])

---

# Recommended hands-on reading + code order

1. Quick read: Spinning Up tutorials and follow their “Start here” exercises. ([spinningup.openai.com][5])
2. Implement tabular algorithms from Sutton & Barto. ([Stanford University][2])
3. Implement a DQN following Spinning Up or David Silver notes. ([David Silver][3], [spinningup.openai.com][5])
4. Move to actor-critic and PPO implementations. Use SB3 to sanity-check. ([stable-baselines3.readthedocs.io][7])

---

# How I suggest you start *right now* (immediate plan)

1. Clone these repos: Spinning Up repo, Stable-Baselines3 repo, and David Silver notes repo. ([GitHub][6])
2. Run the Spinning Up “first algorithm” tutorial (REINFORCE or a simple policy gradient) on CartPole. Observe logs. ([spinningup.openai.com][5])
3. Implement tabular Value Iteration for a small GridWorld — this will cement Bellman backups. (I can drop sample code if you want.)

---

# Metrics of progress (how to measure mastery)

* You can derive and explain Bellman optimality and why Q-learning converges in tabular settings.
* You can implement DQN and PPO from scratch and reproduce basic results.
* You can tune hyperparameters and run robust multi-seed experiments.
* You can read a new RL paper and reproduce its primary experiment or build a reasonable variant.
* You can deploy an RL model in a real-world loop or production simulator.

---

# Caveats & gotchas

* **Reproducibility problem:** RL results vary a lot with seeds, hyperparams, and implementation details. Always run multiple seeds. ([stable-baselines3.readthedocs.io][7])
* **Sample inefficiency:** many model-free deep RL methods require huge numbers of environment steps. Consider model-based or offline methods for sample-limited settings. ([arXiv][9])

---

If you like this plan I’ll do one of the following *now* (pick one, or tell me which and I’ll do it):

* A) Produce a week-by-week 12-week calendar with daily tasks and exact reading/code targets.
* B) Drop a ready-to-run **starter notebook** that implements Value Iteration + tabular Q-learning (with runnable code you can copy).
* C) Give a concise “first 7 exercises” coding list with templates and expected outputs (good if you want to jump into code).

Which one do you want me to do *right now*?

[1]: https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf?utm_source=chatgpt.com "Reinforcement Learning"
[2]: https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf?utm_source=chatgpt.com "Reinforcement Learning: An Introduction"
[3]: https://davidstarsilver.wordpress.com/teaching/?utm_source=chatgpt.com "David Silver: Teaching"
[4]: https://github.com/dalmia/David-Silver-Reinforcement-learning?utm_source=chatgpt.com "dalmia/David-Silver-Reinforcement-learning"
[5]: https://spinningup.openai.com/en/latest/?utm_source=chatgpt.com "Welcome to Spinning Up in Deep RL! — Spinning Up ... - OpenAI"
[6]: https://github.com/openai/spinningup?utm_source=chatgpt.com "openai/spinningup: An educational resource to help ..."
[7]: https://stable-baselines3.readthedocs.io/?utm_source=chatgpt.com "Stable-Baselines3 Docs - Reliable Reinforcement Learning ..."
[8]: https://github.com/DLR-RM/stable-baselines3?utm_source=chatgpt.com "DLR-RM/stable-baselines3"
[9]: https://arxiv.org/abs/1708.05866?utm_source=chatgpt.com "A Brief Survey of Deep Reinforcement Learning"
[10]: https://www.cs.columbia.edu/~allen/S19/deep_rl.pdf?utm_source=chatgpt.com "A Brief Survey of Deep Reinforcement Learning"





# Structure 2

Absolutely! Let’s begin an **interactive, hands-on journey** from the **very basics to mastery in Reinforcement Learning**, with **module-wise learning**, **clear explanations**, and **Python code examples for every concept**.

We’ll build understanding step-by-step, reinforce each idea with code, and gradually scale up to deep RL and real-world applications.

---

# 🚀 Reinforcement Learning: A Complete Journey  
**From Zero to Mastery**  
*With Python Code at Every Step*

---

## 📚 Course Structure: 10 Modules

| Module | Topic | Goal |
|-------|------|------|
| **0** | Setup & Tools | Get ready to code RL |
| **1** | Introduction & MDPs | Understand the RL framework |
| **2** | Policies, Value Functions & Bellman Equations | Learn the math behind decisions |
| **3** | Dynamic Programming | Solve known environments |
| **4** | Monte Carlo Methods | Learn from episodes |
| **5** | Temporal Difference (TD) Learning | Learn online, step-by-step |
| **6** | Function Approximation & DQN | Scale to large spaces with neural nets |
| **7** | Policy Gradient & Actor-Critic | Learn policies directly |
| **8** | Advanced Deep RL (PPO, SAC, DDPG) | Master modern algorithms |
| **9** | Capstone Project | Build and train your own RL agent |

---

Let’s begin!

---

## 🔹 Module 0: Setup & Tools

### Goal:
Set up your environment and get familiar with basic tools.

### Concepts:
- Python, NumPy, Gymnasium (formerly OpenAI Gym)

### Install:
```bash
pip install gymnasium numpy matplotlib
```

### Code: Test Your First Environment

```python
import gymnasium as gym
import numpy as np

# Create a simple environment: FrozenLake (4x4 grid)
env = gym.make("FrozenLake-v1", is_slippery=False, render_mode="human")

# Reset environment
state, info = env.reset()

# Take a random action
action = env.action_space.sample()
next_state, reward, terminated, truncated, info = env.step(action)

print(f"State: {state} → Action: {action} → Next State: {next_state}, Reward: {reward}")
env.close()
```

> ✅ **Try it**: Run this. You’ll see a tiny grid world where the agent moves.

> 🧠 **Note**: `is_slippery=False` means actions are deterministic. Later, we’ll enable slipperiness for realism.

---

## 🔹 Module 1: Introduction to RL & MDPs

### Goal:
Understand the core RL framework: **Agent, Environment, States, Actions, Rewards, MDPs**.

### Key Concepts:
- **Markov Decision Process (MDP)**: A 5-tuple (S, A, P, R, γ)
- **States (S)**: All possible situations
- **Actions (A)**: Choices the agent can make
- **Transitions P(s'|s,a)**: Probability of next state
- **Rewards R(s,a,s')**: Feedback from environment
- **Discount γ**: How much we value future rewards

### Example: Deterministic Grid World (2x2)

Let’s define a **tiny MDP** manually.

```python
# Manual MDP: 2x2 Grid World
# States: 0,1,2,3 (top-left to bottom-right)
# Actions: 0=Left, 1=Down, 2=Right, 3=Up
# Goal: Reach state 3 (bottom-right)

import numpy as np

# Transition: deterministic
# P[action][from_state] = (to_state, reward)
P = {
    0: {0: (0, 0), 1: (1, 0), 2: (2, 0), 3: (3, 0)},  # Left
    1: {0: (2, 0), 1: (3, 1), 2: (2, 0), 3: (3, 0)},  # Down (reward at 1→3)
    2: {0: (1, 0), 1: (1, 0), 2: (3, 1), 3: (3, 0)},  # Right (reward at 2→3)
    3: {0: (0, 0), 1: (0, 0), 2: (2, 0), 3: (1, 0)}   # Up
}

# But this is messy. Let's use gym instead!
```

Better: Use `gym` to access clean MDPs.

### Code: Inspect FrozenLake MDP

```python
env = gym.make("FrozenLake-v1", is_slippery=False)

print("Action space:", env.action_space)      # Discrete(4): 0=Left, 1=Down, 2=Right, 3=Up
print("State space:", env.observation_space)  # Discrete(16): 4x4 grid

# Get transition dynamics (only in some environments)
# For FrozenLake, transitions are deterministic if is_slippery=False

env.reset()
print("Initial state:", env.state)  # Hidden, but we can track it
```

> 🧠 **Insight**: In RL, we usually **don’t know P and R** — we have to learn them!

---

## 🔹 Module 2: Policies, Value Functions & Bellman Equations

### Goal:
Understand how agents evaluate and improve behavior.

### Key Concepts:
- **Policy π(a|s)**: Probability of taking action `a` in state `s`
- **Value Function V(s)**: Expected total discounted reward from state `s`
- **Q-Function Q(s,a)**: Expected return taking action `a` in state `s`
- **Bellman Equation**:
  \[
  V(s) = \sum_a \pi(a|s) \sum_{s',r} P(s',r|s,a) [r + \gamma V(s')]
  \]

### Code: Evaluate a Random Policy

Let’s estimate \( V(s) \) by simulation.

```python
def evaluate_policy(env, policy, gamma=0.99, n_episodes=1000):
    V = np.zeros(env.observation_space.n)
    counts = np.zeros(env.observation_space.n)

    for _ in range(n_episodes):
        state, info = env.reset()
        done = False
        episode_states = []
        episode_rewards = []

        while not done:
            episode_states.append(state)
            action = policy[state]
            state, reward, terminated, truncated, info = env.step(action)
            episode_rewards.append(reward)
            done = terminated or truncated

        # Compute returns for each state
        G = 0
        for i in range(len(episode_states) - 1, -1, -1):
            G = episode_rewards[i] + gamma * G
            s = episode_states[i]
            V[s] += G
            counts[s] += 1

    # Average
    for s in range(len(V)):
        if counts[s] > 0:
            V[s] /= counts[s]
    return V

# Define a random policy (e.g., always move right)
policy = [2] * 16  # 2 = Right

V = evaluate_policy(env, policy)
print("Value function:", V.reshape(4,4))
```

> 🧠 **Note**: This is **Monte Carlo Policy Evaluation** — learning from episodes.

---

## 🔹 Module 3: Dynamic Programming (DP)

### Goal:
Solve MDPs when you know the full model (P and R).

### Key Algorithms:
- **Policy Evaluation**: Compute \( V^\pi(s) \)
- **Policy Iteration**: Improve policy iteratively
- **Value Iteration**: Find optimal \( V^* \) directly

### Code: Policy Evaluation (Iterative)

```python
def policy_evaluation(env, policy, gamma=0.99, theta=1e-8):
    V = np.zeros(env.observation_space.n)
    while True:
        delta = 0
        for s in range(env.observation_space.n):
            v = V[s]
            a = policy[s]
            # One-step lookahead
            total = 0
            for prob, next_state, reward, done in env.P[s][a]:
                total += prob * (reward + gamma * V[next_state])
            V[s] = total
            delta = max(delta, abs(v - V[s]))
        if delta < theta:
            break
    return V
```

### Code: Policy Iteration

```python
def policy_iteration(env, gamma=0.99):
    policy = np.random.choice(env.action_space.n, size=env.observation_space.n)
    
    while True:
        # Step 1: Evaluate policy
        V = policy_evaluation(env, policy, gamma)
        
        # Step 2: Improve policy
        policy_stable = True
        for s in range(env.observation_space.n):
            old_action = policy[s]
            # Find best action
            q_values = np.zeros(env.action_space.n)
            for a in range(env.action_space.n):
                for prob, next_state, reward, done in env.P[s][a]:
                    q_values[a] += prob * (reward + gamma * V[next_state])
            policy[s] = np.argmax(q_values)
            if old_action != policy[s]:
                policy_stable = False
                
        if policy_stable:
            break
    return policy, V
```

> ✅ Run it on `FrozenLake-v1` (non-slippery) — you’ll get an optimal policy!

---

## 🔹 Module 4: Monte Carlo (MC) Methods

### Goal:
Learn from **complete episodes** without knowing the model.

### Key Idea:
Estimate \( V(s) \) by averaging returns after visiting state `s`.

### Code: Monte Carlo First-Visit Policy Evaluation

```python
def mc_prediction(env, policy, n_episodes=5000, gamma=0.99):
    V = np.zeros(env.observation_space.n)
    returns = {s: [] for s in range(env.observation_space.n)}

    for _ in range(n_episodes):
        # Generate episode
        state, info = env.reset()
        episode = []
        done = False
        visited = set()

        while not done:
            action = policy[state]
            next_state, reward, terminated, truncated, info = env.step(action)
            episode.append((state, reward))
            state = next_state
            done = terminated or truncated

        # Compute returns
        G = 0
        for t in range(len(episode) - 1, -1, -1):
            s, r = episode[t]
            G = r + gamma * G
            if s not in visited:  # First visit
                returns[s].append(G)
                V[s] = np.mean(returns[s])
                visited.add(s)
    return V
```

> 🧠 MC works for episodic tasks (e.g., games) but not infinite ones.

---

## 🔹 Module 5: Temporal Difference (TD) Learning

### Goal:
Learn **online**, one step at a time.

### Algorithms:
- **TD(0)**: Bootstrapped value update
- **SARSA**: On-policy TD for Q
- **Q-Learning**: Off-policy TD (learns optimal Q)

### Code: TD(0) Prediction

```python
def td_prediction(env, policy, alpha=0.1, n_episodes=1000, gamma=0.99):
    V = np.zeros(env.observation_space.n)
    for _ in range(n_episodes):
        state, info = env.reset()
        done = False
        while not done:
            action = policy[state]
            next_state, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            # TD update
            V[state] += alpha * (reward + gamma * V[next_state] - V[state])
            state = next_state
    return V
```

### Code: Q-Learning (Tabular)

```python
def q_learning(env, alpha=0.1, epsilon=0.1, n_episodes=5000, gamma=0.99):
    Q = np.zeros((env.observation_space.n, env.action_space.n))
    
    for _ in range(n_episodes):
        state, info = env.reset()
        done = False
        
        while not done:
            # ε-greedy
            if np.random.random() < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(Q[state])
                
            next_state, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            # Q-learning update
            best_next_q = np.max(Q[next_state])
            td_target = reward + gamma * best_next_q
            td_error = td_target - Q[state, action]
            Q[state, action] += alpha * td_error

            state = next_state
            
    # Extract policy
    policy = np.argmax(Q, axis=1)
    return policy, Q
```

> ✅ Run this on `FrozenLake` — it will learn to reach the goal!

---

## 🔹 Module 6: Function Approximation & Deep Q-Network (DQN)

### Goal:
Scale RL to large/continuous spaces using **neural networks**.

### Key Ideas:
- Replace Q-table with a neural network: \( \hat{Q}(s,a; \theta) \)
- Use **experience replay** and **target network**

### Code: DQN for CartPole (PyTorch)

Install: `pip install torch gymnasium`

```python
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque

class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, output_dim)
        )
    
    def forward(self, x):
        return self.fc(x)

# Replay Buffer
class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

# DQN Agent
env = gym.make("CartPole-v1")
n_actions = env.action_space.n
n_states = env.observation_space.shape[0]

policy_net = DQN(n_states, n_actions)
target_net = DQN(n_states, n_actions)
target_net.load_state_dict(policy_net.state_dict())
optimizer = optim.Adam(policy_net.parameters(), lr=1e-3)
replay_buffer = ReplayBuffer()

def select_action(state, epsilon):
    if random.random() < epsilon:
        return env.action_space.sample()
    with torch.no_grad():
        return policy_net(torch.tensor(state).float().unsqueeze(0)).argmax().item()

# Training loop
episodes = 500
batch_size = 64
gamma = 0.99
epsilon = 1.0

for episode in range(episodes):
    state, info = env.reset()
    total_reward = 0
    done = False
    
    while not done:
        action = select_action(state, epsilon)
        next_state, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        total_reward += reward
        
        replay_buffer.push(state, action, reward, next_state, done)
        state = next_state
        
        # Train
        if len(replay_buffer.buffer) >= batch_size:
            batch = replay_buffer.sample(batch_size)
            states, actions, rewards, next_states, dones = zip(*batch)
            
            states = torch.tensor(np.array(states)).float()
            actions = torch.tensor(actions).long()
            rewards = torch.tensor(rewards).float()
            next_states = torch.tensor(np.array(next_states)).float()
            dones = torch.tensor(dones).float()
            
            current_q = policy_net(states).gather(1, actions.unsqueeze(1)).squeeze()
            next_q = target_net(next_states).max(1)[0]
            target_q = rewards + gamma * next_q * (1 - dones)
            
            loss = nn.MSELoss()(current_q, target_q.detach())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    
    # Update epsilon
    epsilon = max(0.01, epsilon * 0.99)
    
    # Update target network
    if episode % 10 == 0:
        target_net.load_state_dict(policy_net.state_dict())
    
    if episode % 50 == 0:
        print(f"Episode {episode}, Reward: {total_reward}, Epsilon: {epsilon:.2f}")

print("DQN Training Complete!")
```

> 🎉 This agent will learn to balance the pole!

---

## 🔹 Module 7: Policy Gradient & Actor-Critic

### Goal:
Learn **policies directly** using gradients.

### Algorithms:
- **REINFORCE**
- **Actor-Critic**

### Code: REINFORCE (Monte Carlo Policy Gradient)

```python
import torch
import torch.nn as nn
import torch.optim as optim

class PolicyNet(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(PolicyNet, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, output_dim),
            nn.Softmax(dim=-1)
        )
    
    def forward(self, x):
        return self.fc(x)

# Initialize
env = gym.make("CartPole-v1")
policy_net = PolicyNet(env.observation_space.shape[0], env.action_space.n)
optimizer = optim.Adam(policy_net.parameters(), lr=1e-3)

def reinforce(episodes=500):
    for episode in range(episodes):
        state, info = env.reset()
        log_probs = []
        rewards = []
        done = False
        
        while not done:
            state_tensor = torch.tensor(state).float()
            probs = policy_net(state_tensor)
            action_dist = torch.distributions.Categorical(probs)
            action = action_dist.sample()
            
            log_prob = action_dist.log_prob(action)
            log_probs.append(log_prob)
            
            state, reward, terminated, truncated, info = env.step(action.item())
            rewards.append(reward)
            done = terminated or truncated
        
        # Compute returns
        G = 0
        returns = []
        for r in reversed(rewards):
            G = r + 0.99 * G
            returns.insert(0, G)
        
        # Normalize returns
        returns = torch.tensor(returns)
        returns = (returns - returns.mean()) / (returns.std() + 1e-9)
        
        # Policy gradient update
        policy_loss = []
        for log_prob, G in zip(log_probs, returns):
            policy_loss.append(-log_prob * G)
        policy_loss = torch.stack(policy_loss).sum()
        
        optimizer.zero_grad()
        policy_loss.backward()
        optimizer.step()
        
        if episode % 50 == 0:
            print(f"Episode {episode}, Total Reward: {sum(rewards)}")

reinforce()
```

---

## 🔹 Module 8: Advanced Deep RL

Now you're ready for:
- **PPO** (most widely used)
- **SAC** (best for continuous control)
- **DDPG/TD3** (for robotics)

Use **Stable-Baselines3** to train them quickly:

```bash
pip install stable-baselines3[extra]
```

```python
from stable_baselines3 import PPO

env = gym.make("CartPole-v1")
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10_000)
model.save("ppo_cartpole")

# Test
obs, info = env.reset()
for _ in range(1000):
    action, _ = model.predict(obs)
    obs, reward, done, truncated, info = env.step(action)
    if done or truncated:
        break
```

---

## 🔹 Module 9: Capstone Project Ideas

Choose one:
1. **Train an agent to play Atari Breakout**
2. **Solve LunarLander with PPO**
3. **Build a custom grid world with obstacles**
4. **Multi-agent predator-prey simulation**
5. **Robot arm control using SAC**

---

## 🔹 Module 10: Mastery & Beyond

Now explore:
- **Offline RL** (BCQ, CQL)
- **Hierarchical RL**
- **Meta-RL**
- **RL + LLMs**
- **Real robotics (ROS + RL)**

---

# 🏁 Next Steps

We’ve built a **complete, code-first RL curriculum**.

Let’s now **dive deeper into each module** interactively.

👉 **Tell me**:
- Which module would you like to **explore first in detail**?
- Do you want to **run code together** (I’ll guide you)?
- Or jump to **DQN or PPO**?

Let’s keep building, one step at a time. 🚀