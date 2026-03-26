import React, {useMemo} from 'react';
import PlotlyChart from '../PlotlyChart';

/**
 * Simulates a random agent on CartPole and plots episode rewards.
 * Uses a seeded PRNG so the chart is deterministic across renders.
 * CartPole random agent typically scores 15-50 per episode.
 */

function seededRandom(seed: number): () => number {
  let s = seed;
  return () => {
    s = (s * 1664525 + 1013904223) & 0xffffffff;
    return (s >>> 0) / 0xffffffff;
  };
}

function simulateRandomCartPole(episodes: number, seed: number): number[] {
  const rng = seededRandom(seed);
  const rewards: number[] = [];
  for (let ep = 0; ep < episodes; ep++) {
    // CartPole random agent: geometric-ish distribution, mean ~22
    const steps = Math.floor(-Math.log(1 - rng()) * 22) + 8;
    rewards.push(Math.min(steps, 500));
  }
  return rewards;
}

function rollingAverage(data: number[], window: number): number[] {
  return data.map((_, i) => {
    const start = Math.max(0, i - window + 1);
    const slice = data.slice(start, i + 1);
    return slice.reduce((a, b) => a + b, 0) / slice.length;
  });
}

export default function RandomAgentRewards(): React.JSX.Element {
  const {episodes, rewards, rolling} = useMemo(() => {
    const n = 200;
    const r = simulateRandomCartPole(n, 42);
    return {
      episodes: Array.from({length: n}, (_, i) => i),
      rewards: r,
      rolling: rollingAverage(r, 20),
    };
  }, []);

  return (
    <PlotlyChart
      data={[
        {
          x: episodes,
          y: rewards,
          type: 'scatter',
          mode: 'markers',
          marker: {color: 'rgba(63,81,181,0.3)', size: 4},
          name: 'Episode reward',
        },
        {
          x: episodes,
          y: rolling,
          type: 'scatter',
          mode: 'lines',
          line: {color: '#3f51b5', width: 2.5},
          name: 'Rolling avg (20)',
        },
        {
          x: [0, 199],
          y: [500, 500],
          type: 'scatter',
          mode: 'lines',
          line: {color: '#4caf50', width: 1.5, dash: 'dash'},
          name: 'Max possible (500)',
        },
      ]}
      layout={{
        title: {text: 'Random Agent on CartPole-v1', font: {size: 15}},
        xaxis: {title: 'Episode', gridcolor: 'rgba(128,128,128,0.15)'},
        yaxis: {title: 'Total Reward', range: [0, 100], gridcolor: 'rgba(128,128,128,0.15)'},
        legend: {x: 0.02, y: 0.98, bgcolor: 'transparent'},
        height: 380,
      }}
    />
  );
}
