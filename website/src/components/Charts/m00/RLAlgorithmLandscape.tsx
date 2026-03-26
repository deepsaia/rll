import React from 'react';
import PlotlyChart from '../PlotlyChart';

/**
 * Shows how different RL algorithm families compare on key axes.
 * Data is illustrative/representative, not from a specific benchmark.
 */
export default function RLAlgorithmLandscape(): React.JSX.Element {
  const algorithms = [
    'Random', 'Q-Learning', 'DQN', 'REINFORCE', 'A2C', 'PPO', 'SAC', 'MuZero',
  ];
  // Illustrative scores: sample efficiency (higher = fewer samples needed)
  const sampleEfficiency = [1, 5, 4, 3, 5, 6, 7, 9];
  // Final performance (higher = better)
  const performance = [1, 4, 6, 5, 6, 8, 9, 10];
  // Module where you learn it
  const modules = ['00', '04', '05', '06', '06', '07', '07', '10'];

  return (
    <PlotlyChart
      data={[
        {
          x: sampleEfficiency,
          y: performance,
          text: algorithms.map((a, i) => `${a}<br>Module ${modules[i]}`),
          mode: 'markers+text',
          type: 'scatter',
          textposition: 'top center',
          textfont: {size: 11},
          marker: {
            size: algorithms.map((_, i) => 14 + i * 2),
            color: sampleEfficiency.map((_, i) => i),
            colorscale: 'Blues',
            showscale: false,
            line: {width: 1.5, color: '#3f51b5'},
          },
          hovertemplate: '<b>%{text}</b><br>Sample efficiency: %{x}<br>Performance: %{y}<extra></extra>',
        },
      ]}
      layout={{
        title: {text: 'RL Algorithm Landscape (Illustrative)', font: {size: 15}},
        xaxis: {
          title: 'Sample Efficiency',
          range: [0, 11],
          gridcolor: 'rgba(128,128,128,0.15)',
        },
        yaxis: {
          title: 'Final Performance',
          range: [0, 11.5],
          gridcolor: 'rgba(128,128,128,0.15)',
        },
        showlegend: false,
        height: 420,
      }}
    />
  );
}
