import React from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

interface Props {
  data: Record<string, unknown>[];
  layout?: Record<string, unknown>;
  config?: Record<string, unknown>;
  style?: React.CSSProperties;
}

const defaultLayout: Record<string, unknown> = {
  autosize: true,
  margin: {l: 55, r: 30, t: 40, b: 50},
  font: {family: 'system-ui, -apple-system, sans-serif', size: 13},
  paper_bgcolor: 'transparent',
  plot_bgcolor: 'transparent',
  xaxis: {gridcolor: 'rgba(128,128,128,0.15)', zerolinecolor: 'rgba(128,128,128,0.25)'},
  yaxis: {gridcolor: 'rgba(128,128,128,0.15)', zerolinecolor: 'rgba(128,128,128,0.25)'},
};

const defaultConfig: Record<string, unknown> = {
  responsive: true,
  displayModeBar: true,
  modeBarButtonsToRemove: ['lasso2d', 'select2d', 'autoScale2d'],
  displaylogo: false,
};

export default function PlotlyChart({data, layout, config, style}: Props): React.JSX.Element {
  return (
    <BrowserOnly fallback={<div style={{height: 350, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--ifm-color-emphasis-500)'}}>Loading chart...</div>}>
      {() => {
        const Plot = require('react-plotly.js').default;
        const merged = {...defaultLayout, ...layout};
        return (
          <div style={{borderRadius: 12, overflow: 'hidden', border: '1px solid var(--ifm-color-emphasis-200)', marginBottom: '1.5rem', ...style}}>
            <Plot
              data={data}
              layout={merged}
              config={{...defaultConfig, ...config}}
              useResizeHandler
              style={{width: '100%', height: layout?.height || 380}}
            />
          </div>
        );
      }}
    </BrowserOnly>
  );
}
