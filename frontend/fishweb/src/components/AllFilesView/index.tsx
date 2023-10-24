import React, { ReactNode, useEffect, useState } from 'react';
import { css } from '@emotion/css';
import './index.scss';
import { Tabs, Table } from '@arco-design/web-react';
import { IconLayout } from '@arco-design/web-react/icon';
import { columns, data } from '../CodeStructureViewer/codeFile/constants';
import eventBus from '../Sidebar/evnets';
import { useScreen } from './context';

const TabPane = Tabs.TabPane;

const AllFilesView: React.FC<{
  children?: ReactNode;
}> = (props) => {
  const { currentScreen, setCurrentScreen } = useScreen();
  const [screens, setScreens] = useState<
    Array<{ tabData: any[]; selectKey: string }>
  >([{ tabData: [], selectKey: '0-0' }]);
  const [isSplitScreen, setIsSplitScreen] = useState(false);

  const toggleSplitScreen = () => {
    setIsSplitScreen(!isSplitScreen);
    setScreens((prevScreens) => {
      const newScreens = [...prevScreens, { tabData: [], selectKey: '0-0' }];
      setCurrentScreen(newScreens.length - 1);
      return newScreens;
    });
  };

  const handleClickTabIem = (key: string, screenIndex: number) => {
    let newScreens = [...screens];
    newScreens[screenIndex].selectKey = key;
    setScreens(newScreens);
    eventBus.emit(`clickTabItem-${screenIndex}`, key);
  };

  const onClickTreeItem = (data: any, screenIndex: number) => {
    let { title, key, content } = data;
    let newScreens = [...screens];
    if (!hasDuplicateKey(newScreens[screenIndex].tabData, key)) {
      let obj = {
        title,
        key,
        content
      };
      newScreens[screenIndex].tabData.push(obj);
      setScreens(newScreens);
    } else {
      console.log('Item with the same key already exists');
    }
    newScreens[screenIndex].selectKey = key;
    setScreens(newScreens);
  };

  function hasDuplicateKey(array: any, keyToFind: any) {
    const duplicateItem = array.find((item: any) => {
      return item.key === keyToFind;
    });
    return duplicateItem;
  }

  useEffect(() => {
    screens.forEach((_, index) => {
      eventBus.on(`clickTreeItem-${index}`, (data: any) =>
        onClickTreeItem(data, index)
      );
    });

    return () => {
      screens.forEach((_, index) => {
        eventBus.removeListener(`clickTreeItem-${index}`, (data: any) =>
          onClickTreeItem(data, index)
        );
      });
    };
  }, [screens]);

  const handleDeleteTab = (key: any, screenIndex: number) => {
    let newScreens = [...screens];
    newScreens[screenIndex].tabData = newScreens[screenIndex].tabData.filter(
      (item) => item.key !== key
    );
    setScreens(newScreens);
    if (
      key === newScreens[screenIndex].selectKey &&
      newScreens[screenIndex].tabData.length > 0
    ) {
      newScreens[screenIndex].selectKey =
        newScreens[screenIndex].tabData[
          newScreens[screenIndex].tabData.length - 1
        ].key;
      setScreens(newScreens);
    }
  };

  return (
    <div className="all_file_center_container">
      {screens.map((screen, index) => (
        <div
          key={index}
          className="all_file_center_main"
          onFocus={() => setCurrentScreen(index)}
        >
          <Tabs
            editable
            type="card"
            activeTab={screen.selectKey}
            onDeleteTab={(key) => handleDeleteTab(key, index)}
            onChange={(key) => handleClickTabIem(key, index)}
            size="large"
            style={{ width: '100%' }}
            // onAddTab={() => handleAddTab(index)}
            showAddButton={true}
            onClickTab={(key) => handleClickTabIem(key, index)}
            addButton={
              <IconLayout
                className="screensplit_btn"
                onClick={toggleSplitScreen}
              />
            }
          >
            {screen.tabData.map((x, i) => (
              <TabPane destroyOnHide key={x.key} title={x.title}>
                {props.children}
                {/* <Table columns={columns} data={data} pagination={false} /> */}
                {x.content}
              </TabPane>
            ))}
          </Tabs>
        </div>
      ))}
    </div>
  );
};

export default AllFilesView;
