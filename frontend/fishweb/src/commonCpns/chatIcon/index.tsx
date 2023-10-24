import { Dropdown, Menu } from '@arco-design/web-react';
import {
  IconMessage,
  IconCustomerService,
  IconPen,
} from '@arco-design/web-react/icon';
import { css } from '@emotion/css';
import React, { useRef } from 'react';
const ChatIcon: React.FC = () => {
  const refMenuItemClicked = useRef<null | string>(null);
  const dropList = (
    <Menu
      onClickMenuItem={(key) => {
        refMenuItemClicked.current = key;
      }}
    >
      <Menu.Item key="1">
        <IconCustomerService style={{ marginRight: 8 }} />
        Explain this script
      </Menu.Item>
      <Menu.Item key="2">
        <IconPen style={{ marginRight: 8 }} />
        Generate Code
      </Menu.Item>
    </Menu>
  );
  return (
    <Dropdown droplist={dropList} position="tr" trigger="click">
      <div
        className={css`
          width: 56px;
          height: 56px;
          background: rgb(var(--arcoblue-2));
          border-radius: 50%;
          display: flex;
          justify-content: center;
          align-items: center;
          cursor: pointer;
        `}
      >
        <IconMessage
          style={{ width: 24, height: 24, color: 'var(--color-neutral-8)' }}
        />
      </div>
    </Dropdown>
  );
};
export default ChatIcon;
