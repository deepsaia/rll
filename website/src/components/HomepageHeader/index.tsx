import React from 'react';
import styles from './styles.module.css';

export default function HomepageHeader(): React.JSX.Element {
  return (
    <header className={styles.hero}>
      <div className={styles.heroInner}>
        <div className={styles.heroIcon}>&#x1F916;</div>
        <h1 className={styles.heroTitle}>Reinforcement Learning</h1>
        <p className={styles.heroSubtitle}>
          A hands-on, code-first guide - from bandits to PPO and beyond
        </p>
        <div className={styles.heroButtons}>
          <a className={styles.heroBtnPrimary} href="course/modules/m00">
            Start Learning
          </a>
          <a className={styles.heroBtnSecondary} href="course/contents">
            Course Roadmap
          </a>
        </div>
      </div>
      <div className={styles.heroWave} />
    </header>
  );
}
