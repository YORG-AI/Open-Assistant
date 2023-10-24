import { Link, Route, Routes } from 'react-router-dom';
import { DataBaseInitView } from '../../page/DataBaseInitView';
import { SideBar } from '../Sidebar';
import { CodeFile } from './codeFile';
import FileView from './fileView/index';
import './index.scss';
import { useBreadcrumb } from '../Sidebar/useBreadcrumb';
import { Breadcrumb, Typography } from '@arco-design/web-react';
import { css } from '@emotion/css';
import { IconCopy } from '@arco-design/web-react/icon';
import { useState, useEffect } from 'react';
import AllFilesView from '../AllFilesView';
import { ChatHistoryView } from '../../page/ChatHistoryView/ChatHistoryView';
import { useChatReducer } from '../../commonCpns/chathistory/reducer';
import { ChatHistory } from '../../commonCpns/chathistory/chathistory';
const BreadcrumbItem = Breadcrumb.Item;
const CodeStructureViewer = () => {
  const {
    onHandleSelectedTree,
    breadcrumbData,
    selectedNodeKey,
    handleBreadcrumbClick,
  } = useBreadcrumb();
  const [isAllFiles, setIsAllFiles] = useState<boolean>(true);
  const [chatState, dispatch] = useChatReducer();
  const { isShrink } = chatState;
  //测试用
  // useEffect(() => {
  //   console.log(isShrink);
  // });
  return (
    <div className="flexStyle">
      <SideBar
        handleSelectedTree={onHandleSelectedTree}
        selectedNodeKey={selectedNodeKey}
      />
      <Routes>
        <Route path="/" element={<CodeFile />}></Route>
        <Route path="/codeFile" element={<CodeFile />}></Route>
        <Route
          path="/databastinit"
          element={
            <div style={{ display: 'flex', flex: 1 }}>
              {isAllFiles ? (
                <AllFilesView>
                  <div className="all_files_view_container">
                    <div className="all_files_view_bread_wrapper">
                      <Breadcrumb>
                        {breadcrumbData.map((item, index) => (
                          <BreadcrumbItem
                            key={item.key}
                            // onClick={() => handleBreadcrumbClick(index)}
                            // className={
                            //   index < breadcrumbData.length - 1
                            //     ? 'clickable'
                            //     : ''
                            // }
                          >
                            {item.title}
                            {index === breadcrumbData.length - 1 ? (
                              <IconCopy style={{ marginLeft: 8 }} />
                            ) : (
                              ''
                            )}
                          </BreadcrumbItem>
                        ))}
                      </Breadcrumb>
                    </div>
                    <Typography.Text style={{ marginRight: 12 }}>
                      272.8 kB
                    </Typography.Text>
                  </div>
                </AllFilesView>
              ) : (
                <FileView>
                  <div className="file_view_container">
                    <Breadcrumb>
                      {breadcrumbData.map((item, index) => (
                        <BreadcrumbItem
                          key={item.key}
                          onClick={() => handleBreadcrumbClick(item,index)}
                          className={
                            index < breadcrumbData.length - 1 ? 'clickable' : ''
                          }
                        >
                          {item.title}
                          {index === breadcrumbData.length - 1 ? (
                            <IconCopy style={{ marginLeft: 8 }} />
                          ) : (
                            ''
                          )}
                        </BreadcrumbItem>
                      ))}
                    </Breadcrumb>
                  </div>
                </FileView>
              )}
              <DataBaseInitView />
            </div>
          }
        />
        <Route
          path="/chatHistory"
          element={
            <div style={{ display: 'flex', flex: 1 }}>
              <div className="midbox">
                {isShrink ? (
                  isAllFiles ? (
                    <AllFilesView>
                      <div
                        className={css`
                          display: flex;
                          justify-content: space-between;
                          align-items: center;
                        `}
                      >
                        <div
                          className={css`
                            margin: 6px 0;
                            margin-left: 12px;
                          `}
                        >
                          <Breadcrumb>
                            {breadcrumbData.map((item, index) => (
                              <BreadcrumbItem
                                key={item.key}
                                onClick={() => handleBreadcrumbClick(item,index)}
                                className={
                                  index < breadcrumbData.length - 1
                                    ? 'clickable'
                                    : ''
                                }
                              >
                                {item.title}
                                {index === breadcrumbData.length - 1 ? (
                                  <IconCopy style={{ marginLeft: 8 }} />
                                ) : (
                                  ''
                                )}
                              </BreadcrumbItem>
                            ))}
                          </Breadcrumb>
                        </div>
                        <Typography.Text style={{ marginRight: 12 }}>
                          272.8 kB
                        </Typography.Text>
                      </div>
                    </AllFilesView>
                  ) : (
                    <FileView>
                      <div
                        className={css`
                          margin-top: 12px;
                          margin-bottom: 9px;
                        `}
                      >
                        <Breadcrumb>
                          {breadcrumbData.map((item, index) => (
                            <BreadcrumbItem
                              key={item.key}
                              onClick={() => handleBreadcrumbClick(item,index)}
                              className={
                                index < breadcrumbData.length - 1
                                  ? 'clickable'
                                  : ''
                              }
                            >
                              {item.title}
                              {index === breadcrumbData.length - 1 ? (
                                <IconCopy style={{ marginLeft: 8 }} />
                              ) : (
                                ''
                              )}
                            </BreadcrumbItem>
                          ))}
                        </Breadcrumb>
                      </div>
                    </FileView>
                  )
                ) : (
                  ''
                )}
              </div>

              <div
                className={`right-box ${isShrink ? 'shrink-transition' : ''}`}
                style={{ flex: 1 }}
              >
                <ChatHistory chatState={chatState} dispatch={dispatch} />
              </div>
            </div>
          }
        />
      </Routes>
    </div>
  );
};
export { CodeStructureViewer };
