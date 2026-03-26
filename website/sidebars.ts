import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  courseSidebar: [
    'index',
    'contents',
    {
      type: 'category',
      label: 'Modules',
      collapsed: false,
      items: [
        'modules/m00',
        'modules/m01',
        'modules/m02',
        'modules/m03',
        'modules/m04',
        'modules/m05',
        'modules/m06',
        'modules/m07',
        'modules/m08',
        'modules/m09',
        'modules/m10',
        'modules/m11',
        'modules/m12',
        'modules/m13',
        'modules/m14',
        'modules/m15',
      ],
    },
  ],
};

export default sidebars;
