import { ReactComponent as Lock } from '../../assets/icons/Lock.svg';
import { Tag, Badge, Link, Button } from '@arco-design/web-react';
import { ReactComponent as LinkSvg } from '../../assets/icons/Link.svg';
import { IconLoop, IconDelete } from '@arco-design/web-react/icon';
import { css } from '@emotion/css';
const testArr = [
  {
    id: 1,
    firstName: 'YORG',
    secondName: 'new-backend',
    desc: 'The Multi-Agent Framework: Given one line Requirement, return PRD, Design, ...',
    type: 1,
    time: 24,
  },
  {
    id: 2,
    firstName: 'YORG',
    secondName: 'new-backend',
    desc: 'The Multi-Agent Framework: Given one line Requirement, return PRD, Design, ...',
    type: 1,
    time: 24,
  },
  {
    id: 3,
    firstName: 'YORG',
    secondName: 'new-backend',
    desc: 'The Multi-Agent Framework: Given one line Requirement, return PRD, Design, ...',
    type: 1,
    time: 24,
  },
  {
    id: 4,
    firstName: 'YORG',
    secondName: 'new-backend',
    desc: 'The Multi-Agent Framework: Given one line Requirement, return PRD, Design, ...',
    type: 2,
    time: 24,
  },
  {
    id: 5,
    firstName: 'OpenAI',
    secondName: 'Whisper',
    desc: 'This repo does not have an intro.',
    type: 3,
    time: 4,
  },
  {
    id: 6,
    firstName: 'YORG',
    secondName: 'new-backend',
    desc: 'The Multi-Agent Framework: Given one line Requirement, return PRD, Design, ...',
    type: 1,
    time: 24,
  },
  {
    id: 7,
    firstName: 'geekan',
    secondName: 'MetaGPT',
    desc: 'This repo does not have an intro.',
    type: 4,
    time: 24,
  },
  {
    id: 8,
    firstName: 'geekan',
    secondName: 'MetaGPT',
    desc: 'This repo does not have an intro.',
    type: 4,
    time: 24,
  },
  {
    id: 9,
    firstName: 'YORG',
    secondName: 'new-backend',
    desc: 'The Multi-Agent Framework: Given one line Requirement, return PRD, Design, ...',
    type: 1,
    time: 24,
  },
  {
    id: 10,
    firstName: 'OpenAI',
    secondName: 'Whisper',
    desc: 'This repo does not have an intro.',
    type: 3,
    time: 4,
  },
  {
    id: 11,
    firstName: 'OpenAI',
    secondName: 'Whisper',
    desc: 'This repo does not have an intro.',
    type: 3,
    time: 4,
  },
  {
    id: 12,
    firstName: 'geekan',
    secondName: 'MetaGPT',
    desc: 'This repo does not have an intro.',
    type: 4,
    time: 24,
  },
];

const modelLine = [
  {
    name: 'YORG',
    czlist: [
      {
        id: 1,
        icon: <Lock />,
        text: 'ATAH/yorg',
      },
      {
        id: 2,
        icon: <Lock />,
        text: 'ATAH/yorg',
      },
      {
        id: 3,
        icon: <Lock />,
        text: 'ATAH/yorg',
      },
    ],
  },
];
const modelLine2 = [
  {
    name: 'MetaGPT',
    czlist: [
      {
        id: 1,
        icon: <Lock />,
        text: 'ATAH/yorg',
        time: '2 days ago',
      },
      {
        id: 2,
        icon: <Lock />,
        text: 'ATAH/yorg',
        time: '2 days ago',
      },
      {
        id: 3,
        icon: <Lock />,
        text: 'ATAH/yorg',
        time: '2 days ago',
      },
    ],
  },
];
const modelLine3 = [
  {
    name: 'Result',
    czlist: [
      {
        id: 1,
        icon: <Lock />,
        text: 'ATAH/yorg',
        time: '2 days ago',
      },
      {
        id: 2,
        icon: <Lock />,
        text: 'ATAH/yorg',
        time: '2 days ago',
      },
      {
        id: 3,
        icon: <Lock />,
        text: 'ATAH/yorg',
        time: '2 days ago',
      },
    ],
  },
];
const modelLine4 = [
  {
    name: 'Result',
    czlist: [
      {
        id: 1,
        icon: <Lock />,
        text: 'ATAH/yorg',
        time: '2 days ago',
      },
    ],
  },
];
const listdata = [
  {
    key: '1',
    // empty: <DragDotVertical />,
    name: 'GitHub / Github_Desktop_legacy...',
    current: <Tag>master</Tag>,
    location: (
      <div
        className={css`
          display: flex;
          align-items: center;
          gap: 8px;
          align-self: stretch;
        `}
      >
        GitHub
        <LinkSvg />
      </div>
    ),
    status: <Badge status="success" text="Ready" />,
    email: 'Now',
    action: (
      <div
        className={css`
          display: flex;
          align-items: center;
          align-self: stretch;
        `}
      >
        <Link href="#">View</Link>
        <Button type="text" icon={<IconLoop />}></Button>
        <Button
          type="text"
          icon={<IconDelete />}
          style={{ color: '#F53F3F' }}
        ></Button>
      </div>
    ),
  },
  {
    key: '2',
    name: 'GitHub / Github_Desktop_legacy...',
    current: <Tag>master</Tag>,
    location: (
      <div
        className={css`
          display: flex;
          align-items: center;
          gap: 8px;
          align-self: stretch;
        `}
      >
        GitHub
        <LinkSvg />
      </div>
    ),
    status: <Badge status="success" text="Ready" />,
    email: '2 hours ago',
    action: (
      <div
        className={css`
          display: flex;
          align-items: center;
          /* align-self: stretch; */
        `}
      >
        <Link href="#">View</Link>
        <Button type="text" icon={<IconLoop />}></Button>
        <Button
          type="text"
          icon={<IconDelete />}
          style={{ color: '#F53F3F' }}
        ></Button>
      </div>
    ),
  },
  {
    key: '3',
    name: 'Kevin Sandra',
    current: <Tag>master</Tag>,
    location: (
      <div
        className={css`
          display: flex;
          align-items: center;
          gap: 8px;
          align-self: stretch;
        `}
      >
        GitHub
        <LinkSvg />
      </div>
    ),
    status: <Badge status="success" text="Ready" />,
    email: '2 hours ago',
  },
  {
    key: '4',
    name: 'Ed Hellen',
    current: <Tag>master</Tag>,
    location: (
      <div
        className={css`
          display: flex;
          align-items: center;
          gap: 8px;
          align-self: stretch;
        `}
      >
        GitHub
        <LinkSvg />
      </div>
    ),
    status: <Badge status="success" text="Ready" />,
    email: '2 hours ago',
  },
  {
    key: '5',
    name: 'William Smith',
    current: <Tag>master</Tag>,
    location: (
      <div
        className={css`
          display: flex;
          align-items: center;
          gap: 8px;
          align-self: stretch;
        `}
      >
        GitHub
        <LinkSvg />
      </div>
    ),
    status: <Badge status="success" text="Ready" />,
    email: '2 hours ago',
  },
  {
    key: '6',
    name: 'William Smith',
    salary: 27000,
    current: <Tag>master</Tag>,
    location: (
      <div
        className={css`
          display: flex;
          align-items: center;
          gap: 8px;
          align-self: stretch;
        `}
      >
        GitHub
        <LinkSvg />
      </div>
    ),
    status: <Badge status="success" text="Loading:20%" />,
    email: '2 hours ago',
  },
];
export { testArr, modelLine, modelLine2, modelLine3, modelLine4, listdata };
