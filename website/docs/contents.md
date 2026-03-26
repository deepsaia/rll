---
sidebar_position: 2
title: Course Contents
---

# Course Roadmap

## Quick overview

1. **Foundations**: Setup, math prerequisites, bandits, MDPs, dynamic programming.
2. **Core model-free methods**: Monte Carlo, TD learning, Q-learning, SARSA (tabular to function approximation).
3. **Policy methods**: Policy gradients, REINFORCE, actor-critic.
4. **Deep RL**: DQN family, PPO, SAC, TD3.
5. **Practical skills**: Reward design, debugging, diagnostics, partial observability.
6. **Advanced topics**: Model-based RL, RLHF, multi-agent RL, sim-to-real.
7. **Research & capstone**: Paper reproduction, capstone project.

---

## Recommended resources

* **Sutton & Barto - *Reinforcement Learning: An Introduction*** - the standard theoretical text.
* **David Silver's RL course** - excellent lecture series mapping to Sutton & Barto.
* **OpenAI Spinning Up in Deep RL** - practical, tutorial-style with clean PyTorch code.
* **Stable-Baselines3 (SB3)** - production-quality implementations for experiments and baselines.

---

## Prerequisites

* **Math**: Linear algebra, multivariable calculus, probability, basics of optimization (SGD), Markov chains.
* **Coding**: Python (numpy), PyTorch, basics of experiments, logging, and plotting. Familiarity with Gymnasium is helpful.
* **Tools**: Git, venv/conda, Jupyter.

---

## Suggested schedule (flexible)

| Timeframe | Modules | Focus |
|-----------|---------|-------|
| Month 1 | 00-03 | Foundations, bandits, MDPs, DP |
| Month 2 | 04-06 | MC, TD, DQN, policy gradients |
| Month 3 | 07-08 | Modern deep RL, debugging |
| Month 4 | 09-11 | POMDPs, model-based, RLHF |
| Month 5 | 12-13 | Multi-agent, sim-to-real |
| Month 6 | 14-15 | Paper reproduction, capstone |

For real research-level mastery, expect 12+ months of focused work (reading papers + contributing code).

---

## Practical project ideas

1. **Classic RL pipeline**: DQN on Atari from scratch, compare with SB3 baseline.
2. **Robust continuous control**: Train SAC on MuJoCo-like tasks, test robustness to domain shifts.
3. **Offline RL**: Apply CQL on D4RL dataset vs behavior cloning.
4. **Sim2Real**: Train in sim, deploy to real robot (or sim-to-sim transfer).
5. **Paper reproduction**: Pick a NeurIPS/ICLR paper, reproduce, write up findings.

---

## Metrics of progress

* You can derive Bellman optimality and explain why Q-learning converges in tabular settings.
* You can implement DQN and PPO from scratch and reproduce basic results.
* You can tune hyperparameters and run robust multi-seed experiments.
* You can read a new RL paper and reproduce its primary experiment.
* You can deploy an RL model in a real-world loop or production simulator.
