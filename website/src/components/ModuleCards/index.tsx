import React from 'react';
import styles from './styles.module.css';

interface ModuleInfo {
  id: string;
  title: string;
  description: string;
  icon: string;
}

const modules: ModuleInfo[] = [
  {id: 'm00', title: 'Introduction', description: 'Why RL matters, setup your lab, run your first agent', icon: '\u{1F6E0}\u{FE0F}'},
  {id: 'm01', title: 'Math Foundations', description: 'Probability, linear algebra, calculus for RL', icon: '\u{1F4D0}'},
  {id: 'm02', title: 'Multi-Armed Bandits', description: 'Exploration vs exploitation, UCB, Thompson sampling', icon: '\u{1F3B0}'},
  {id: 'm03', title: 'MDPs & Dynamic Programming', description: 'Bellman equations, value/policy iteration', icon: '\u{1F4CA}'},
  {id: 'm04', title: 'MC & TD Methods', description: 'Monte Carlo, SARSA, Q-learning, eligibility traces', icon: '\u{1F3AF}'},
  {id: 'm05', title: 'Function Approximation & DQN', description: 'Neural networks for value functions, replay buffers', icon: '\u{1F9E0}'},
  {id: 'm06', title: 'Policy Gradients', description: 'REINFORCE, actor-critic, advantage estimation', icon: '\u{1F4C8}'},
  {id: 'm07', title: 'Modern Deep RL', description: 'PPO, SAC, TD3 — the algorithms that actually work', icon: '\u{1F680}'},
  {id: 'm08', title: 'Reward Design & Debugging', description: 'Reward shaping, diagnostics, why your agent is broken', icon: '\u{1F527}'},
  {id: 'm09', title: 'Partial Observability', description: 'POMDPs, recurrent policies, generalization', icon: '\u{1F576}\u{FE0F}'},
  {id: 'm10', title: 'Model-Based RL', description: 'World models, planning, Dyna, MuZero', icon: '\u{1F30D}'},
  {id: 'm11', title: 'RLHF & LLM Alignment', description: 'Reward models, PPO for language, DPO', icon: '\u{1F4AC}'},
  {id: 'm12', title: 'Multi-Agent RL', description: 'Cooperation, competition, communication', icon: '\u{1F465}'},
  {id: 'm13', title: 'Sim-to-Real & Production', description: 'Domain randomization, deployment, safety', icon: '\u{1F3ED}'},
  {id: 'm14', title: 'Paper Reproduction', description: 'Pick a paper, reproduce it, understand the gaps', icon: '\u{1F4DD}'},
  {id: 'm15', title: 'Capstone', description: 'Your portfolio project — design, build, evaluate', icon: '\u{1F3C6}'},
];

export default function ModuleCards(): React.JSX.Element {
  return (
    <div className={styles.grid}>
      {modules.map((mod) => (
        <a key={mod.id} href={`course/modules/${mod.id}`} className={styles.card}>
          <div className={styles.cardIcon}>{mod.icon}</div>
          <div className={styles.cardBody}>
            <div className={styles.cardLabel}>{mod.id.toUpperCase()}</div>
            <h3 className={styles.cardTitle}>{mod.title}</h3>
            <p className={styles.cardDesc}>{mod.description}</p>
          </div>
        </a>
      ))}
    </div>
  );
}
