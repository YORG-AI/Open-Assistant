import { FC } from 'react';
import { css } from '@emotion/css';
import {
  Breadcrumb,
  Table,
  Pagination,
  Typography,
  Input,
  Menu,
  Dropdown,
} from '@arco-design/web-react';
import {
  IconCopy,
  IconFile,
  IconFolder,
  IconDown,
} from '@arco-design/web-react/icon';
import { columns, data } from './constants';
const BreadcrumbItem = Breadcrumb.Item;
const InputSearch = Input.Search;
const dropList = (
  <Menu>
    <Menu.Item key="1">
      <IconFile style={{ marginRight: 8 }} />
      Add a file
    </Menu.Item>
    <Menu.Item key="2">
      <IconFolder style={{ marginRight: 8 }} />
      Add a folder
    </Menu.Item>
  </Menu>
);
export const CodeFile: FC = () => {
  return (
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
          <BreadcrumbItem>Home</BreadcrumbItem>
          <BreadcrumbItem href="#">Channel</BreadcrumbItem>
          <BreadcrumbItem>News</BreadcrumbItem>
          <IconCopy />
        </Breadcrumb>
        <div>
          <Typography.Text>272.8 kB</Typography.Text>
        </div>
      </div>
      <div
        className={css`
          /* width: 1080px; */
          box-sizing: border-box;
          display: flex;
          padding: 24px;
          flex-direction: column;
          align-items: flex-start;
          gap: 24px;
          flex: 1 0 0;
          align-self: stretch;
          border-radius: 12px;
          border: 1px solid var(--color-border-2, #283fb3);
          background: #fff;
        `}
      >
        <div
          className={css`
            display: flex;
            justify-content: space-between;
            align-items: center;
            align-self: stretch;
          `}
        >
          <div
            className={css`
              display: flex;
              justify-content: flex-end;
              align-items: center;
              gap: 12px;
              border-radius: 8px;
            `}
          >
            <Dropdown.Button
              type="primary"
              droplist={dropList}
              trigger="click"
              icon={<IconDown />}
            >
              Add
            </Dropdown.Button>
          </div>
          <div
            className={css`
              display: flex;
              justify-content: space-between;
              width: 220px;
              align-items: center;
            `}
          >
            <InputSearch allowClear placeholder="Enter keyword to search" />
          </div>
        </div>
        <div
          className={css`
            display: flex;
            align-items: flex-start;
            align-self: stretch;
          `}
        >
          <Table
            columns={columns}
            data={data}
            // style={{ width: '1032px' }}
            renderPagination={() => (
              <div className="page_container">
                <Pagination simple total={50} size="small" />
              </div>
            )}
          ></Table>
        </div>
      </div>
    </div>
  );
};
