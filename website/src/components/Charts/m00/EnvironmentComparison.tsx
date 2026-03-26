import React from 'react';
import PlotlyChart from '../PlotlyChart';

/**
 * Compares random agent performance across environments.
 * Used in the exercises section to show FrozenLake and CartPole side by side.
 */
export default function EnvironmentComparison(): React.JSX.Element {
  const envs = ['CartPole-v1', 'FrozenLake\n(slippery)', 'FrozenLake\n(not slippery)', 'LunarLander-v2'];
  const meanReward = [22.1, 0.014, 0.062, -178.4];
  const colors = ['#3f51b5', '#e53935', '#ff7043', '#7986cb'];
  const annotations = ['~22 / 500 max', '1.4% win rate', '6.2% win rate', '-178 / +200 max'];

  return (
    <PlotlyChart
      data={[
        {
          x: envs,
          y: meanReward,
          type: 'bar',
          marker: {color: colors, line: {width: 1.5, color: '#283593'}},
          text: annotations,
          textposition: 'outside',
          textfont: {size: 11},
          hovertemplate: '<b>%{x}</b><br>Mean reward: %{y:.2f}<extra></extra>',
        },
      ]}
      layout={{
        title: {text: 'Random Agent Performance Across Environments', font: {size: 14}},
        xaxis: {gridcolor: 'rgba(128,128,128,0.15)'},
        yaxis: {title: 'Mean Reward', gridcolor: 'rgba(128,128,128,0.15)'},
        showlegend: false,
        height: 360,
        margin: {l: 55, r: 20, t: 45, b: 60},
      }}
    />
  );
}
