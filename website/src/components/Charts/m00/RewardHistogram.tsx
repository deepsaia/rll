import React, {useMemo} from 'react';
import PlotlyChart from '../PlotlyChart';

/**
 * Histogram of random agent episode rewards on CartPole.
 * Shows the distribution is right-skewed with most episodes < 50.
 */

function seededRandom(seed: number): () => number {
  let s = seed;
  return () => {
    s = (s * 1664525 + 1013904223) & 0xffffffff;
    return (s >>> 0) / 0xffffffff;
  };
}

export default function RewardHistogram(): React.JSX.Element {
  const rewards = useMemo(() => {
    const rng = seededRandom(42);
    return Array.from({length: 500}, () => {
      const steps = Math.floor(-Math.log(1 - rng()) * 22) + 8;
      return Math.min(steps, 500);
    });
  }, []);

  return (
    <PlotlyChart
      data={[
        {
          x: rewards,
          type: 'histogram',
          nbinsx: 30,
          marker: {color: 'rgba(63,81,181,0.7)', line: {color: '#3f51b5', width: 1}},
          hovertemplate: 'Reward: %{x}<br>Count: %{y}<extra></extra>',
        },
      ]}
      layout={{
        title: {text: 'Distribution of Random Agent Rewards (500 episodes)', font: {size: 14}},
        xaxis: {title: 'Episode Reward', gridcolor: 'rgba(128,128,128,0.15)'},
        yaxis: {title: 'Count', gridcolor: 'rgba(128,128,128,0.15)'},
        showlegend: false,
        height: 320,
        margin: {l: 50, r: 20, t: 40, b: 45},
      }}
    />
  );
}
