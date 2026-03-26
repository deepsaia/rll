import React, {type ReactNode} from 'react';
import styles from './styles.module.css';

interface Props {
  label?: string;
  children: ReactNode;
}

export default function CollapsibleOutput({label = 'Expected Output', children}: Props): React.JSX.Element {
  return (
    <details className={styles.container}>
      <summary className={styles.summary}>
        <span className={styles.icon}>&#x25B6;</span>
        <span className={styles.label}>{label}</span>
      </summary>
      <div className={styles.content}>
        {children}
      </div>
    </details>
  );
}
