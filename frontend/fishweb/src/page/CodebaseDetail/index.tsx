import './index.scss';
import { FC, useReducer, useState } from 'react';
import { useParams } from 'react-router-dom';
import { CommitForm } from '../../commonCpns/commitForm/commitForm';
import { Dropdown, Menu, Input, Button } from '@arco-design/web-react';
import {
  IconLock,
  IconDown,
  IconPlus,
  IconCopy,
  IconBranch,
  IconLoop,
} from '@arco-design/web-react/icon';
import { SelectTion } from '../../commonCpns/selection/selection';
import { CommonItemUI } from '../AllreposCardView/itemUI';
import { modelLine, modelLine2 } from '../AllreposCardView/constant';
import { showDatabaseWords, showWords } from './constant';
import FileCheckBox from '../../components/FileCheckBox';
import { options } from '../../components/FileCheckBox/constant';
import BranchModal from '../../commonCpns/branchModal';
import { branchReducer, initialState } from './reducer';
const InputSearch = Input.Search;
export const CodebaseDetail: FC<{ type?: string }> = ({ type }) => {
  const isDatabase = type === 'database';
  let { id } = useParams();
  const [dropStatus, setDropStatus] = useState<boolean>(false);
  const [state, dispatch] = useReducer(branchReducer, initialState);
  const [num, setNum] = useState<number>(-1);
  const [checkBoxList, setCheckBoxList] = useState<any[]>([]);
  const [showModal, setShowModal] = useState<boolean>(false);
  const handleChangeDropdown = (visible: boolean, num: number) => {
    setDropStatus(visible);
    setNum(num);
  };
  const handleChangeCheckBoxList = (value: any[]) => {
    setCheckBoxList(value);
  };
  const handleClickAdd = () => {
    if (num === 2) {
      setShowModal(true);
    }
  };
  const onHandleClickCloseModal = () => {
    setShowModal(false);
  };
  const onHandleClickSubmitModal = (formData: any) => {
    // console.log(formData);
    setShowModal(false);
    dispatch({ type: 'FORM_SUBMIT', branch: formData.branchName });
  };
  const adddropList = (
    <Menu onClickMenuItem={(key) => {}}>
      <Menu.Item key="1">
        <IconCopy style={{ marginRight: 8 }} />
        Clone Repo
      </Menu.Item>
      {/* <Menu.Item key="2">
        <IconPlus style={{ marginRight: 8 }} />
        Create New Repo
      </Menu.Item> */}
    </Menu>
  );
  const dropList = (
    <div
      className="dropshow"
      style={{
        borderBottomLeftRadius: num === 2 ? 0 : '',
        width: num === 2 ? '350px' : '',
      }}
    >
      <div className="searchTop">
        <InputSearch
          allowClear
          placeholder="filter"
          style={{
            backgroundColor: 'var(--color-neutral-1)',
            borderRadius: '6px',
            border: '1px solid var(--color-neutral-3)',
            flex: 1,
          }}

          // onChange={setInputValue}
        />
        <Dropdown
          droplist={num === 1 ? adddropList : ''}
          position="br"
          trigger="click"
        >
          <Button
            onClick={handleClickAdd}
            icon={<IconPlus />}
            style={{
              borderRadius: '6px',
              border: '1px solid var(--color-neutral-3)',
            }}
          />
        </Dropdown>
      </div>
      <div className="lineblock">
        {num === 2 ? (
          <CommonItemUI clist={modelLine2} needChangeIcon />
        ) : (
          <CommonItemUI clist={modelLine} />
        )}
      </div>
      {/* <div className="lineblock">
        {num === 2 ? (
          <CommonItemUI clist={modelLine2} needChangeIcon />
        ) : (
          <CommonItemUI clist={modelLine} />
        )}
      </div> */}
    </div>
  );
  return (
    <div className="mainbox">
      <div className="main_contain">
        {isDatabase ? (
          <div className="navbar">
            <Dropdown
              droplist={dropList}
              position="bl"
              trigger="click"
              defaultPopupVisible
              onVisibleChange={(e) => handleChangeDropdown(e, 1)}
            >
              <div
                className="selectBox"
                style={{
                  backgroundColor:
                    dropStatus && num === 1 ? 'var(--color-neutral-1)' : '',
                  borderBottomColor:
                    dropStatus && num === 1 ? 'var(--color-neutral-1)' : '',
                }}
              >
                <div className="boxcontain" style={{ color: '#4080FF' }}>
                  <IconLock
                    style={{ color: dropStatus && num === 1 ? '#4E5969' : '' }}
                  />
                  <div className="boxtext">
                    <div
                      className="texttop"
                      style={{
                        color: dropStatus && num === 1 ? '#4E5969' : '',
                      }}
                    >
                      Current Database
                    </div>
                    <div className="textbom">YORG / new-backend</div>
                  </div>
                </div>
                <div className="dropicon">
                  <IconDown />
                </div>
              </div>
            </Dropdown>
            <div className="selectBox">
              <div className="boxcontain" style={{ color: '#4080FF' }}>
                <IconLoop />
                <div className="boxtext">
                  <div className="texttop" style={{ color: '#1d2129' }}>
                    Fetch origin
                  </div>
                  <div className="textbom" style={{ color: '#4080FF' }}>
                    Last fetched 26mins ago
                  </div>
                </div>
              </div>
              <div className="dropicon">
                <IconDown />
              </div>
            </div>
          </div>
        ) : (
          <div className="navbar">
            <Dropdown
              droplist={dropList}
              position="bl"
              trigger="click"
              defaultPopupVisible
              onVisibleChange={(e) => handleChangeDropdown(e, 1)}
            >
              <div
                className="selectBox"
                style={{
                  backgroundColor:
                    dropStatus && num === 1 ? 'var(--color-neutral-1)' : '',
                  borderBottomColor:
                    dropStatus && num === 1 ? 'var(--color-neutral-1)' : '',
                }}
              >
                <div className="boxcontain" style={{ color: '#4080FF' }}>
                  <IconLock
                    style={{ color: dropStatus && num === 1 ? '#4E5969' : '' }}
                  />
                  <div className="boxtext">
                    <div
                      className="texttop"
                      style={{
                        color: dropStatus && num === 1 ? '#4E5969' : '',
                      }}
                    >
                      Current Repository
                    </div>
                    <div className="textbom">YORG / new-backend</div>
                  </div>
                </div>
                <div className="dropicon">
                  <IconDown />
                </div>
              </div>
            </Dropdown>
            <Dropdown
              droplist={dropList}
              position="bl"
              trigger="click"
              defaultPopupVisible
              onVisibleChange={(e) => handleChangeDropdown(e, 2)}
              popupVisible={(dropStatus && num === 2) || showModal}
            >
              <div
                className="selectBox"
                style={{
                  backgroundColor:
                    dropStatus && num === 2 ? 'var(--color-neutral-1)' : '',
                }}
              >
                <div className="boxcontain" style={{ color: '#4080FF' }}>
                  <IconBranch
                    style={{ color: dropStatus && num === 2 ? '#4E5969' : '' }}
                  />
                  <div className="boxtext">
                    <div
                      className="texttop"
                      style={{
                        color: dropStatus && num === 2 ? '#4E5969' : '',
                      }}
                    >
                      Current Branch
                    </div>
                    <div className="textbom">{state.branch}</div>
                  </div>
                </div>
                <div className="dropicon">
                  <IconDown />
                </div>
              </div>
            </Dropdown>
            <div className="selectBox">
              <div className="boxcontain" style={{ color: '#4080FF' }}>
                <IconLoop />
                <div className="boxtext">
                  <div className="texttop" style={{ color: '#1d2129' }}>
                    Fetch origin
                  </div>
                  <div className="textbom" style={{ color: '#4080FF' }}>
                    Last fetched 26mins ago
                  </div>
                </div>
              </div>
              <div className="dropicon">
                <IconDown />
              </div>
            </div>
          </div>
        )}

        <div className="bomview">
          <div
            className="overlay-mask"
            style={{
              display:
                (dropStatus && num === 2) || showModal ? 'block' : 'none',
            }}
          ></div>
          {/* 遮罩层 */}
          {!isDatabase && (
            <div className="main_left">
              <div className="top_btn">
                <div
                  className="btn_text"
                  style={{ color: options.length > 0 ? '#4080ff' : '' }}
                >
                  {options.length} Changed Files
                </div>
              </div>
              <div className="mid_content">
                <FileCheckBox
                  onChangeCheckBoxList={handleChangeCheckBoxList}
                ></FileCheckBox>
              </div>
              <div>
                <CommitForm
                  controllButtonDisabled={
                    checkBoxList.length > 0 ? false : true
                  }
                />
              </div>
            </div>
          )}
          <div className="main_mid">
            {(isDatabase?showDatabaseWords:showWords).map((itm, idx) => {
              return (
                <div className="mid_contop" key={idx}>
                  <div className="selecttionTitle">{itm.name}</div>
                  <SelectTion rowContent={itm} />
                </div>
              );
            })}
          </div>
          <div className="main_right">
            {/* <div className="right-content">{id}</div> */}
          </div>
        </div>
      </div>
      <BranchModal
        visible={showModal}
        handleClickCloseModal={onHandleClickCloseModal}
        handleClickSubmitModal={onHandleClickSubmitModal}
      ></BranchModal>
    </div>
  );
};
