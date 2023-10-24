import React, { useState } from 'react';
import './index.scss';
import '../../commonCpns/AddRepo/index.scss';
import {
  Breadcrumb,
  Radio,
  Button,
  Input,
  Pagination,
  Dropdown,
  Menu,
  Modal,
  Popover,
  Checkbox,
  Badge,
  Empty,
} from '@arco-design/web-react';
import {
  IconFilter,
  IconDown,
  IconApps,
  IconLoop,
  IconDelete,
  IconRefresh,
} from '@arco-design/web-react/icon';
import { CardItem } from '../../commonCpns/cardItem/cardItem';
import { ListView } from '../../commonCpns/listviewList/listviewList';
import {
  testArr,
  modelLine,
  listdata,
  modelLine3,
  modelLine4,
} from './constant';
import { CommonItemUI } from './itemUI';
import { DragPart } from '../../commonCpns/DragPart';
const SubMenu = Menu.SubMenu;
const RadioGroup = Radio.Group;
const BreadcrumbItem = Breadcrumb.Item;
const InputSearch = Input.Search;
interface IFilterItem {
  status:
    | 'error'
    | 'success'
    | 'warning'
    | 'processing'
    | 'default'
    | undefined;
  text: string;
  key: number;
}
const AllreposCardView: React.FC<{ type?: string }> = ({ type }) => {
  const [showList, setShowList] = useState('Card');
  const [isPopupVisible, setIsPopupVisible] = useState(false);
  const [loading1, setLoading1] = useState(false);
  const [showButtons, setShowButtons] = useState(false);
  const [listData, setListData] = useState(listdata);
  const [deleteItem, setDeleteItem] = useState([]);
  const isDatabase = type === 'database';
  const [modalKey, setModalKey] = useState('1000');
  const CheckboxGroup = Checkbox.Group;
  const handleSetShowButtons = (data: any, deleteItem: any) => {
    setShowButtons(data);
    setDeleteItem(deleteItem);
  };
  const handleDeleteListData = (keysToDelete: string[]) => {
    const updatedData = listData.filter(
      (item) => !keysToDelete.includes(item.key)
    );
    setListData(updatedData);
  };
  const cardView = (
    <>
      <div className="main_wrapper">
        {testArr.length === 0 && <Empty />}
        {testArr.length !== 0 &&
          testArr.map((item, idx) => (
            <CardItem
              key={idx}
              firstName={item.firstName}
              secondName={item.secondName}
              desc={item.desc}
              type={item.type}
              time={item.time}
            ></CardItem>
          ))}
      </div>
      <div className="page_container">
        <Pagination simple total={50} size="small" />
      </div>
    </>
  );
  const mainRender =
    showList === 'Card' ? (
      cardView
    ) : (
      <ListView onClickItem={handleSetShowButtons} data={listData} />
    );
  const dropList = (
    <Menu
      onClickMenuItem={(key: string) => {
        setIsPopupVisible(true);
        setModalKey(key);
        console.log('key', key);
      }}
    >
      {!isDatabase && <Menu.Item key="1000">GitHub (Private)</Menu.Item>}
      {!isDatabase && <Menu.Item key="1001">GitHub (Public)</Menu.Item>}
      {isDatabase && <Menu.Item key="2001">Cloud</Menu.Item>}
      <Menu.Item key={isDatabase ? '2000' : '1002'}>Local</Menu.Item>
    </Menu>
  );

  return (
    <div className={`main_page ${isPopupVisible ? 'popup-bg' : ''}`}>
      <div className="container">
        <div className="header">
          <Breadcrumb>
            <BreadcrumbItem>Codebase</BreadcrumbItem>
            <BreadcrumbItem>List of Repos</BreadcrumbItem>
          </Breadcrumb>
          <RadioGroup
            type="button"
            name="lang"
            defaultValue="Card"
            onChange={(value) => setShowList(value)}
          >
            <Radio value="Card">Card</Radio>
            <Radio value="List">List</Radio>
          </RadioGroup>
        </div>
        <div className="main">
          <div className="main_header">
            <div className="left_button">
              <Dropdown.Button
                type="primary"
                droplist={dropList}
                icon={<IconDown />}
                style={{ marginRight: '10px' }}
                onClick={() => {
                  setModalKey(isDatabase ? '2000' : '1000');
                  setIsPopupVisible(true);
                }}
              >
                {isDatabase ? 'Add Dataset' : 'Add Repo'}
              </Dropdown.Button>
              <Modal
                title={isDatabase ? 'Add Dataset' : 'Add Repo'}
                visible={isPopupVisible}
                onOk={() => setIsPopupVisible(false)}
                onCancel={() => setIsPopupVisible(false)}
                autoFocus={false}
                focusLock={true}
                mask={false}
                style={{ width: '600px' }}
                footer={
                  <>
                    <div className="extra_btn">
                      <div>
                        <Button
                          onClick={() => {
                            setIsPopupVisible(false);
                          }}
                        >
                          Manage Account
                        </Button>
                      </div>
                      <div className="switchBtn">
                        <Button
                          style={{ marginRight: '8px' }}
                          onClick={() => {
                            setIsPopupVisible(false);
                          }}
                        >
                          Cancel
                        </Button>
                        <Button
                          loading={loading1}
                          style={{ marginRight: '-8px' }}
                          onClick={() => {
                            setLoading1(true);
                            setTimeout(() => {
                              setLoading1(false);
                            }, 1500);
                          }}
                          type="primary"
                        >
                          Clone
                        </Button>
                      </div>
                    </div>
                  </>
                }
              >
                <div className="middle_view">
                  <div className="menu-demo" style={{ height: 427 }}>
                    <Menu
                      style={{ width: 180, height: '427px' }}
                      onClickSubMenu={(key: string) => {
                        setModalKey(key);
                      }}
                    >
                      {(isDatabase
                        ? ['Local', 'Cloud']
                        : ['GitHub (Private)', 'GitHub (Public)', 'Local']
                      ).map((itm, idx) => {
                        return (
                          <SubMenu
                            key={(isDatabase ? '200' : '100') + idx}
                            title={
                              <div
                                style={
                                  modalKey ===
                                  (isDatabase ? '200' : '100') + idx
                                    ? {
                                        color: 'blue',
                                      }
                                    : {}
                                }
                              >
                                <IconApps />
                                {itm}
                              </div>
                            }
                          ></SubMenu>
                        );
                      })}
                    </Menu>
                  </div>
                  {modalKey === '1000' && (
                    <div className="main_content">
                      <div className="content_top">
                        <div className="top_view">
                          Add a Private GitHub Repo
                        </div>
                        <div className="flex">
                          <InputSearch
                            allowClear
                            placeholder="Filter your repo"
                            style={{ width: 356 }}
                            className="btm_view"
                            // onChange={setInputValue}
                          />
                          <Button
                            icon={<IconRefresh />}
                            style={{ borderRadius: '8px', marginLeft: '10px' }}
                          />
                        </div>
                      </div>
                      <div className="content_bottom">
                        <CommonItemUI clist={modelLine} />
                        <CommonItemUI clist={modelLine} />
                        <CommonItemUI clist={modelLine} />
                      </div>
                    </div>
                  )}
                  {modalKey === '1001' && (
                    <div className="main_content">
                      <div className="content_top">
                        <div className="top_view">Add a Public GitHub Repo</div>
                        <div className="flex">
                          <InputSearch
                            allowClear
                            placeholder="Enter a Github URL"
                            style={{ width: 356 }}
                            className="btm_view"
                            // onChange={setInputValue}
                          />
                          <Button
                            icon={<IconRefresh />}
                            style={{ borderRadius: '8px', marginLeft: '10px' }}
                          />
                        </div>
                      </div>
                      <div className="content_bottom">
                        <CommonItemUI clist={modelLine} />
                      </div>
                    </div>
                  )}
                  {modalKey === '1002' && (
                    <div className="main_content">
                      <div className="content_top">
                        <div className="top_view">Enter local path</div>
                        <div className="flex">
                          <InputSearch
                            allowClear
                            placeholder="Enter a Github URL"
                            style={{ width: 356 }}
                            className="btm_view"
                            // onChange={setInputValue}
                          />
                          <Button
                            icon={<IconRefresh />}
                            style={{ borderRadius: '8px', marginLeft: '10px' }}
                          />
                        </div>
                      </div>
                      <DragPart />
                      <div className="content_bottom">
                        <CommonItemUI clist={modelLine} />
                      </div>
                    </div>
                  )}
                  {modalKey === '2000' && (
                    <div className="main_content">
                      <div className="content_top">
                        <div className="top_view">
                          Add data files by providing local path
                        </div>
                        <div className="flex">
                          <InputSearch
                            allowClear
                            placeholder="Select Local Path"
                            style={{ width: 356 }}
                            className="btm_view"
                            // onChange={setInputValue}
                          />
                          <Button
                            icon={<IconRefresh />}
                            style={{ borderRadius: '8px', marginLeft: '10px' }}
                          />
                        </div>
                      </div>
                      <DragPart />
                      <div className="content_bottom">
                        <CommonItemUI clist={modelLine3} />
                      </div>
                    </div>
                  )}
                  {modalKey === '2001' && (
                    <div className="main_content">
                      <div className="content_top">
                        <div className="top_view">
                          Add data files by importing from a warehouse
                        </div>
                        <div className="flex">
                          <InputSearch
                            allowClear
                            placeholder="Select one cloud warehouse"
                            style={{ width: 356 }}
                            className="btm_view"
                          />
                          <Button
                            icon={<IconRefresh />}
                            style={{ borderRadius: '8px', marginLeft: '10px' }}
                          />
                        </div>
                      </div>
                      <div className="content_bottom">
                        <CommonItemUI clist={modelLine4} />
                      </div>
                    </div>
                  )}
                </div>
              </Modal>
              <Popover
                content={
                  <div className="filterCard">
                    <div className="filterCardCol">
                      <div className="filterTitle">Status</div>
                      <Checkbox.Group direction="vertical">
                        {(
                          [
                            { status: 'success', text: 'Ready', key: 1001 },
                            { status: 'warning', text: 'Loading', key: 1002 },
                            { status: 'processing', text: 'Queued', key: 1003 },
                            { status: 'error', text: 'Failed', key: 1004 },
                          ] as IFilterItem[]
                        ).map((item) => {
                          return (
                            <Checkbox key={item.key} value={item.key}>
                              <Badge status={item.status} text={item.text} />
                            </Checkbox>
                          );
                        })}
                      </Checkbox.Group>
                    </div>
                    <div className="filterCardCol">
                      <div className="filterTitle">Location</div>
                      <CheckboxGroup
                        direction="vertical"
                        options={[
                          'Local',
                          'GitHub - Private',
                          'GitHub - Public',
                        ]}
                      />
                    </div>
                  </div>
                }
              >
                <Button type="outline" icon={<IconFilter />}>
                  Filter
                </Button>
              </Popover>
            </div>
            {deleteItem.length > 0 && (
              <div className="right_button">
                <Button type="text" icon={<IconLoop />}>
                  Resync
                </Button>
                <Button
                  type="text"
                  icon={<IconDelete />}
                  style={{ color: '#F53F3F' }}
                  onClick={() => {
                    handleDeleteListData(deleteItem);
                  }}
                >
                  Remove
                </Button>
              </div>
            )}

            <div className="right_search">
              <InputSearch
                allowClear
                placeholder="Enter keyword to search"
                style={{ width: 220 }}
              />
            </div>
          </div>
          {mainRender}
        </div>
      </div>
    </div>
  );
};

export { AllreposCardView };
