import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

const config: Config = {
  title: 'RL Learning Course',
  tagline: 'From Zero to RL Mastery — with code at every step',
  favicon: 'img/favicon.svg',

  future: {
    v4: true,
  },

  url: 'https://deepsaia.github.io',
  baseUrl: '/rll/',

  organizationName: 'deepsaia',
  projectName: 'rll',
  trailingSlash: false,

  onBrokenLinks: 'throw',

  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  clientModules: [
    './src/clientModules/progressTracking.ts',
  ],

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/course',
          sidebarPath: './sidebars.ts',
          remarkPlugins: [remarkMath],
          rehypePlugins: [rehypeKatex],
          editUrl: 'https://github.com/deepsaia/rll/tree/main/website/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css',
      type: 'text/css',
      integrity: 'sha384-nB0miv6/jRmo5YCBER1ssBmHKhG4YTYacKEZLfsHpYmZOJJn5JTay6SKNEP7vIAh',
      crossorigin: 'anonymous',
    },
  ],

  themeConfig: {
    colorMode: {
      defaultMode: 'dark',
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'RL Learning',
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'courseSidebar',
          position: 'left',
          label: 'Course',
        },
        {
          href: 'https://github.com/deepsaia/rll',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Course',
          items: [
            {label: 'Home', to: '/'},
            {label: 'Modules', to: '/course'},
            {label: 'Contents', to: '/course/contents'},
          ],
        },
        {
          title: 'Resources',
          items: [
            {label: 'GitHub', href: 'https://github.com/deepsaia/rll'},
            {label: 'Spinning Up', href: 'https://spinningup.openai.com'},
            {label: 'Stable-Baselines3', href: 'https://stable-baselines3.readthedocs.io'},
          ],
        },
      ],
      copyright: `Copyright ${new Date().getFullYear()} Deepak. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
