import { Menu } from '@arco-design/web-react';
import { FC, useEffect, useReducer, useState } from 'react';
import { useNavigate } from 'react-router';
import { isFoldAtom } from '../../page/allAtom';
import { logoMinPic, sideData } from './constant';
import { useAtom } from 'jotai';

import './index.scss';
const MenuItem = Menu.Item;

const CardMenu: FC = () => {
  const navigate = useNavigate();
  const [isFold, setIsFold] = useAtom(isFoldAtom);
  return (
    <div className="menu_list">
      <div className="menu-demo">
        <Menu
          style={{ height: '100%' }}
          hasCollapseButton
          collapse={isFold}
          defaultOpenKeys={['0']}
          defaultSelectedKeys={['0_1']}
          onCollapseChange={(collapse: boolean) => setIsFold(collapse)}
          onClickMenuItem={(key: string) => {
            const routeUrl = sideData.filter((itm) => itm.key === key)[0].url;
            navigate(routeUrl);
          }}
        >
          <div key="0_2">
            {!isFold ? <div className="logo">YORG</div> : logoMinPic}
          </div>
          {sideData.map((itm) => {
            return (
              <MenuItem key={itm.key} className="menu-item">
                {itm.compo}
                <span style={{ paddingLeft: '10px' }}>{itm.text} </span>
              </MenuItem>
            );
          })}
        </Menu>
      </div>
    </div>
  );
};

export { CardMenu };
