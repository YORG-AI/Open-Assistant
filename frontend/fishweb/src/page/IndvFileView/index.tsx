import React, { useEffect, useState } from 'react';
import { css } from '@emotion/css';
import { Breadcrumb, Typography, Input } from '@arco-design/web-react';
import { IconCopy } from '@arco-design/web-react/icon';
import { SideBar } from '../../components/Sidebar';
import OmsViewMarkdown from '../../components/OmsViewMarkdown';
import ChatIcon from '../../commonCpns/chatIcon';
import './index.scss';
import '../../components/OmsViewMarkdown/markdown.scss';
import { useBreadcrumb } from '../../components/Sidebar/useBreadcrumb';
import { textContent } from './contant';
const BreadcrumbItem = Breadcrumb.Item;
const InputSearch = Input.Search;
const IndvFileView: React.FC = () => {
  const {
    onHandleSelectedTree,
    breadcrumbData,
    selectedNodeKey,
    handleBreadcrumbClick,
  } = useBreadcrumb();
  return (
    <div className="flex" style={{ width: '100%' }}>
      <SideBar
        handleSelectedTree={onHandleSelectedTree}
        selectedNodeKey={selectedNodeKey}
      />
      <div
        className={css`
          /* width: 1112px; */
          box-sizing: border-box;
          display: flex;
          padding: 12px;
          flex-direction: column;
          align-items: flex-start;
          gap: 16px;
          flex: 1 0 0;
          align-self: stretch;
          background: #f7f8fa;
        `}
      >
        <div
          className={css`
            display: flex;
            /* width: 1080px; */
            align-items: center;
            gap: 6px;
            align-self: stretch;
            display: flex;
            height: 32px;
            justify-content: space-between;
            align-items: center;
            align-self: stretch;
          `}
        >
          <Breadcrumb>
            {breadcrumbData.map((item, index) => (
              <BreadcrumbItem
                key={item.key}
                // onClick={() => handleBreadcrumbClick(index)}
                // className={index < breadcrumbData.length - 1 ? 'clickable' : ''}
              >
                {item.title}
                {/* {index === breadcrumbData.length - 1 ? (
                  <IconCopy style={{ marginLeft: 8 }} />
                ) : (
                  ''
                )} */}
              </BreadcrumbItem>
            ))}
            <BreadcrumbItem>
              <IconCopy />
            </BreadcrumbItem>
          </Breadcrumb>
          <div
            className={css`
              display: flex;
              align-items: center;
            `}
          >
            <Typography.Text>701 lines（700 Ioc）· 272.8 kB</Typography.Text>
            <div
              className={css`
                width: 220px;
                margin-left: 16px;
              `}
            >
              <InputSearch
                allowClear
                placeholder="Enter keyword to search"
                style={{ background: '#fff' }}
              />
            </div>
          </div>
        </div>
        <div
          className={css`
            /* width: 1080px; */
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            flex: 1 0 0;
            align-self: stretch;
            border-radius: 12px;
            border: 1px solid var(--color-border-2, #283fb3);
            background: #fff;
            width: 100%;
            overflow-x: hidden;
            overflow-y: auto;
          `}
        >
          <div className="test">
            <OmsViewMarkdown textContent={textContent} />
          </div>
        </div>
      </div>
      <div
        className={css`
          position: fixed;
          bottom: 32px;
          right: 34px;
        `}
      >
        <ChatIcon />
      </div>
    </div>
  );
};
export default IndvFileView;
