import React from 'react';
import Layout from '@theme/Layout';
import HomepageHeader from '@site/src/components/HomepageHeader';
import ModuleCards from '@site/src/components/ModuleCards';
import styles from './index.module.css';

export default function Home(): React.JSX.Element {
  return (
    <Layout
      title="Reinforcement Learning — A Learning Journey"
      description="A hands-on, code-first guide to Reinforcement Learning"
    >
      <HomepageHeader />
      <main className={styles.main}>
        <section className={styles.features}>
          <div className={styles.featureGrid}>
            <div className={styles.feature}>
              <div className={styles.featureIcon}>&#x1F4BB;</div>
              <h3>Code-First</h3>
              <p>Every concept has runnable Python. No hand-waving — you'll implement RL algorithms from scratch.</p>
            </div>
            <div className={styles.feature}>
              <div className={styles.featureIcon}>&#x1F4D0;</div>
              <h3>Just Enough Math</h3>
              <p>Clear explanations with rendered equations. Enough rigor to understand why things work.</p>
            </div>
            <div className={styles.feature}>
              <div className={styles.featureIcon}>&#x1F30D;</div>
              <h3>Real-World Examples</h3>
              <p>From game AI to robotics to LLM alignment — see how RL solves actual problems.</p>
            </div>
          </div>
        </section>

        <section className={styles.modules}>
          <h2 className={styles.sectionTitle}>16 Modules, Zero to Mastery</h2>
          <p className={styles.sectionSubtitle}>
            A structured path from bandits and MDPs to PPO, RLHF, multi-agent RL, and beyond.
          </p>
          <ModuleCards />
        </section>

        <section className={styles.cta}>
          <div className={styles.ctaInner}>
            <h2>Ready to train your first agent?</h2>
            <p>All you need is Python 3.12+ and a willingness to watch training curves for longer than is healthy.</p>
            <a href="course/modules/m00" className={styles.ctaButton}>
              Get Started
            </a>
          </div>
        </section>
      </main>
    </Layout>
  );
}
