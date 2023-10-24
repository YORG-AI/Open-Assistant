import {
  IconCode,
  IconDashboard,
  IconSettings,
  IconStorage,
  IconMosaic,
} from '@arco-design/web-react/icon';
export const logoPic = (
  <svg width="14" height="14" viewBox="0 0 48 48" fill="none">
    <path
      d="M23 8h2v2h-2V8zM23 23h2v2h-2v-2zM23 38h2v2h-2v-2z"
      fill="#4E5969"
    />
    <path
      d="M23 8h2v2h-2V8zM23 23h2v2h-2v-2zM23 38h2v2h-2v-2z"
      stroke="#4E5969"
      stroke-width="2"
    />
    <path
      d="M37 8h2v2h-2V8zM37 23h2v2h-2v-2zM37 38h2v2h-2v-2z"
      fill="#4E5969"
    />
    <path
      d="M37 8h2v2h-2V8zM37 23h2v2h-2v-2zM37 38h2v2h-2v-2z"
      stroke="#4E5969"
      stroke-width="2"
    />
    <path d="M9 8h2v2H9V8zM9 23h2v2H9v-2zM9 38h2v2H9v-2z" fill="#4E5969" />
    <path
      d="M9 8h2v2H9V8zM9 23h2v2H9v-2zM9 38h2v2H9v-2z"
      stroke="#4E5969"
      stroke-width="2"
    />
  </svg>
);
export const logoMinPic = (
  <svg
    width="22"
    height="22"
    viewBox="0 0 37 34"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M0 0H2.92969L13.7812 19.4531L24.9609 0H27.6562L15.0938 21.7969V33.5156H12.6328V21.7969L0 0Z"
      fill="#6AA1FF"
    />
    <path
      d="M36.0938 0L32.5781 10.1953H29.8828L33.3984 0H36.0938Z"
      fill="#6AA1FF"
    />
  </svg>
);
export const sideData = [
  {
    key: '1000',
    text: 'Dashboard',
    compo: <IconDashboard />,
    url: 'dashboard',
  },
  {
    key: '1001',
    text: 'Codebase',
    compo: <IconCode />,
    url: '/codebase',
  },
  { key: '1002', text: 'Database', compo: <IconStorage />, url: '/database' },
  {
    key: '1003',
    text: 'Integrations',
    compo: (
      <span style={{ marginRight: '14px', display: 'inline-block' }}>
        {logoPic}
      </span>
    ),
    url: '',
  },
  { key: '1004', text: 'Settings', compo: <IconSettings />, url: '/bb' },
];
