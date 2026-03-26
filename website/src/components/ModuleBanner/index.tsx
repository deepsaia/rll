import React from 'react';
import styles from './styles.module.css';

interface Props {
  moduleNumber: string;
  title: string;
  icon: string;
}

const MODULE_ICONS: Record<string, string> = {
  '00': '\u{1F6E0}\u{FE0F}',
  '01': '\u{1F4D0}',
  '02': '\u{1F3B0}',
  '03': '\u{1F4CA}',
  '04': '\u{1F3AF}',
  '05': '\u{1F9E0}',
  '06': '\u{1F4C8}',
  '07': '\u{1F680}',
  '08': '\u{1F527}',
  '09': '\u{1F576}\u{FE0F}',
  '10': '\u{1F30D}',
  '11': '\u{1F4AC}',
  '12': '\u{1F465}',
  '13': '\u{1F3ED}',
  '14': '\u{1F4DD}',
  '15': '\u{1F3C6}',
};

export function getModuleInfo(title: string): {moduleNumber: string; moduleName: string; icon: string} | null {
  const match = title.match(/^Module\s+(\d{2}):\s*(.+)$/i);
  if (!match) return null;
  const moduleNumber = match[1];
  const moduleName = match[2];
  const icon = MODULE_ICONS[moduleNumber] || '\u{1F4D6}';
  return {moduleNumber, moduleName, icon};
}

export default function ModuleBanner({moduleNumber, title, icon}: Props): React.JSX.Element {
  return (
    <div className={styles.banner}>
      <div className={styles.bannerIcon}>{icon}</div>
      <div className={styles.bannerText}>
        <span className={styles.bannerLabel}>Module {moduleNumber}</span>
        <span className={styles.bannerTitle}>{title}</span>
      </div>
    </div>
  );
}
