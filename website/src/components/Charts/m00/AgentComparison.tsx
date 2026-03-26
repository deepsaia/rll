import React from 'react';
import PlotlyChart from '../PlotlyChart';

/**
 * Compares random agent vs always-right agent on CartPole.
 * Used in exercise 3 solution.
 */
export default function AgentComparison(): React.JSX.Element {
  return (
    <PlotlyChart
      data={[
        {
          x: ['Random Agent', 'Always-Right Agent'],
          y: [22.1, 9.4],
          type: 'bar',
          marker: {
            color: ['#3f51b5', '#e53935'],
            line: {width: 1.5, color: ['#283593', '#b71c1c']},
          },
          text: ['~22 avg', '~9 avg'],
          textposition: 'outside',
          textfont: {size: 12, color: ['#3f51b5', '#e53935']},
          width: [0.5, 0.5],
          hovertemplate: '<b>%{x}</b><br>Avg reward: %{y:.1f}<extra></extra>',
        },
        {
          x: ['Random Agent', 'Always-Right Agent'],
          y: [500, 500],
          type: 'scatter',
          mode: 'lines',
          line: {color: '#4caf50', width: 1.5, dash: 'dash'},
          name: 'Max possible (500)',
        },
      ]}
      layout={{
        title: {text: 'Random vs Always-Right on CartPole-v1', font: {size: 14}},
        yaxis: {title: 'Average Reward', range: [0, 60], gridcolor: 'rgba(128,128,128,0.15)'},
        xaxis: {gridcolor: 'rgba(128,128,128,0.15)'},
        showlegend: false,
        height: 340,
        margin: {l: 50, r: 20, t: 45, b: 40},
        annotations: [{
          x: 1, y: 500, text: 'Max: 500', showarrow: false,
          font: {size: 11, color: '#4caf50'}, yshift: -12,
        }],
      }}
    />
  );
}
