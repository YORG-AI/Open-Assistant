import { css } from '@emotion/css';
import {
  Input,
  Button,
  Avatar,
  Dropdown,
  Menu,
  Divider,
} from '@arco-design/web-react';
import { IconDown, IconPen } from '@arco-design/web-react/icon';
import { SelectItem } from './selectItem';
import { FC } from 'react';
import { IShowWords } from '../../page/CodebaseDetail/constant';
import { useNavigate } from 'react-router-dom';

const dropList = (urls: string[], urlsName: string[]) => (
  <Menu>
    {urlsName.map((itm, idx) => (
      <Menu.Item
        key="1"
        onClick={() => {
          console.log('urls', urls[idx]);
        }}
      >
        {itm}
      </Menu.Item>
    ))}
  </Menu>
);

const SelectTion: FC<{
  rowContent: IShowWords;
}> = ({ rowContent }) => {
  const navigate = useNavigate();

  return (
    <div
      className={css`
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        border-radius: 8px;
        border: 1px solid var(--color-border-2, #e5e6eb);
        border-bottom: none;
      `}
    >
      {rowContent.content.map((item, key) => {
        if (item.isMulti) {
          return (
            <SelectItem
              suffixBtn={
                <Dropdown.Button
                  type="primary"
                  droplist={dropList(item.urls!, item.urlsName!)}
                  icon={<IconDown />}
                >
                  {item.btnname}
                </Dropdown.Button>
              }
              tig={item.tip}
              key={key}
              subtitle={item.subTitle}
            />
          );
        } else {
          return (
            <SelectItem
              suffixBtn={
                item.isDataRepos ? (
                  <div>
                    <span>14 minutes ago</span>
                    <Button
                      type={item.type ?? 'primary'}
                      style={{ margin: '0 10px' }}
                      onClick={() => {
                        navigate(item.url ?? '');
                      }}
                    >
                      {item.btnname}
                    </Button>
                    <Button
                      type={item.type ?? 'primary'}
                      icon={<IconPen />}
                      onClick={() => {
                        navigate(item.url ?? '');
                      }}
                    />
                  </div>
                ) : (
                  <Button
                    type={item.type ?? 'primary'}
                    onClick={() => {
                      navigate(item.url ?? '');
                    }}
                  >
                    {item.btnname}
                  </Button>
                )
              }
              tig={item.tip}
              key={key}
              subtitle={item.subTitle}
            />
          );
        }
      })}
    </div>
  );
};
export { SelectTion };
