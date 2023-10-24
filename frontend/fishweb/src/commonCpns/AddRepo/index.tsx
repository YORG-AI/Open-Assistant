import React, { useState } from 'react';
import './index.scss';
import { Button, Menu, Input } from '@arco-design/web-react';
import { IconApps } from '@arco-design/web-react/icon';
// import { CardItem } from "../../commonCpns/cardItem/cardItem";
// import { CardMenu } from "../../commonCpns/cardMenu";
// import { ListView } from "../../commonCpns/listviewList/listviewList";
import { ReactComponent as Logo } from '../../assets/logo.svg';
import { ReactComponent as Close } from '../../assets/icons/Close.svg';
const MenuItem = Menu.Item;
const SubMenu = Menu.SubMenu;
const MenuItemGroup = Menu.ItemGroup;
const InputSearch = Input.Search;
const AddRepo: React.FC = () => {
  return (
    <div className="main_view">
      <div className="nav">
        <div className="nav_text">Add Repo</div>
        <div className="nav_icon">
          <Button shape="circle" type="secondary" icon={<Close />} />
        </div>
      </div>
      <div className="middle_view">
        <div className="menu-demo" style={{ height: 427 }}>
          <Menu
            style={{ width: 180, height: '427px' }}
            // defaultOpenKeys={["0"]}
            // defaultSelectedKeys={["0_1"]}
          >
            <SubMenu
              key="0"
              title={
                <>
                  <IconApps /> GitHub (Private)
                </>
              }
            ></SubMenu>
            <SubMenu
              key="1"
              title={
                <>
                  <IconApps /> GitHub (Public)
                </>
              }
            >
              <MenuItem key="1_0">Menu 1</MenuItem>
              <MenuItem key="1_1">Menu 2</MenuItem>
              <MenuItem key="1_2">Menu 3</MenuItem>
            </SubMenu>
            <SubMenu
              key="2"
              title={
                <>
                  <IconApps /> Local
                </>
              }
            >
              <MenuItemGroup key="2_0" title="Menu Group 1">
                <MenuItem key="2_0_0">Menu 1</MenuItem>
                <MenuItem key="2_0_1">Menu 2</MenuItem>
              </MenuItemGroup>
              <MenuItemGroup key="2_1" title="Menu Group 1">
                <MenuItem key="2_1_0">Menu 3</MenuItem>
                <MenuItem key="2_1_1">Menu 4</MenuItem>
              </MenuItemGroup>
            </SubMenu>
          </Menu>
        </div>
        <div className="main_content">
          <div className="content_top">
            <div className="top_view">Add a Private GitHub Repo</div>
            <InputSearch
              allowClear
              placeholder="Go to file"
              style={{ width: 216, backgroundColor: '#f7f8fa' }}
              className="btm_view"
              // onChange={setInputValue}
            />
            {/* <Button icon={<IconPlus />} style={{ borderRadius: "8px" }} /> */}
          </div>
          <div className="content_bottom"></div>
        </div>
      </div>
    </div>
  );
};

export { AddRepo };
