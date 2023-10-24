export interface IShowWords {
  name: string;
  content: {
    tip: string;
    subTitle: string;
    isMulti: boolean;
    btnname: string;
    urls?: string[];
    urlsName?: string[];
    url?: string;
    isDataRepos?: boolean;
    type?:
      | 'text'
      | 'primary'
      | 'default'
      | 'secondary'
      | 'dashed'
      | 'outline'
      | undefined;
  }[];
}
export const showWords: IShowWords[] = [
  {
    name: 'Explore',
    content: [
      {
        tip: 'Explore the repo with AI Agents',
        subTitle: 'Use YORG AI',
        isMulti: true,
        btnname: 'Explore',
        urls: ['/show-chat', '/repo-overview'],
        urlsName: ['Chat', 'Repo overview'],
      },
      {
        tip: 'View repo files',
        subTitle: 'Use YORG AI',
        isMulti: false,
        btnname: 'View',
        url: '/repo-code-path',
      },
    ],
  },
  {
    name: 'Create',
    content: [
      {
        tip: 'Generate with Agents',
        subTitle: 'Use YORG AI',
        isMulti: true,
        btnname: 'Generate',
        urls: [
          '/buildWithAi',
          '/Codebase / Selected Repo / Building / Initial',
        ],
        urlsName: ['Build with Ai', 'Build manually'],
      },
      {
        tip: 'Open the repo in your External Editor',
        subTitle: 'special',
        isMulti: false,
        btnname: 'Open in external editor',
        url: '/',
      },
    ],
  },
  {
    name: 'Locate',
    content: [
      {
        tip: 'View the file of your repo in Finder',
        subTitle: 'Use your Finder',
        isMulti: false,
        btnname: 'Show in Finder',
        url: '/out',
      },
      {
        tip: 'Open the repo page on GitHub ',
        subTitle: 'Use your Browser ',
        isMulti: false,
        btnname: 'View on GitHub',
        url: '/out',
      },
    ],
  },
];
export const showDatabaseWords: IShowWords[] = [
  {
    name: 'Explore',
    content: [
      // hide after a while use ,don't delete
      // {
      //   tip: 'Explore the dataset with agents',
      //   subTitle: 'Use YORG AI',
      //   isMulti: false,
      //   btnname: 'Chat',
      //   url: '/repo-code-path',
      //   type: 'primary',
      // },
      {
        tip: 'View project files',
        subTitle: 'Use YORG AI',
        isMulti: false,
        btnname: 'View files',
        url: '/codepath/codeFile',
        type: 'secondary',
      },
    ],
  },
  {
    name: 'Create',
    content: [
      {
        tip: 'Generate report',
        subTitle: 'Use YORG AI',
        isMulti: false,
        btnname: 'Generate',
        url: '/codepath/chathistory',
        type: 'primary',
      },
    ],
  },
  {
    name: 'Your Data Reports',
    content: [
      {
        tip: 'Report 1',
        subTitle: '',
        isMulti: false,
        btnname: 'View',
        url: '/repo-code-path',
        type: 'secondary',
        isDataRepos: true,
      },
      {
        tip: 'Report 2',
        subTitle: '',
        isMulti: false,
        btnname: 'View',
        url: '/repo-code-path',
        type: 'secondary',
        isDataRepos: true,
      },
    ],
  },
];
