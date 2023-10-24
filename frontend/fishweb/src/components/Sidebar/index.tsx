import { css } from '@emotion/css';
import './index.scss';
import React, { useState, useEffect } from 'react';
import {
  Tree,
  TreeSelect,
  Input,
  Typography,
  Button,
} from '@arco-design/web-react';
import {
  IconPlus,
  IconArrowLeft,
  IconFile,
  IconFolder,
} from '@arco-design/web-react/icon';

import { ReactComponent as CaretDown } from '../../assets/icons/caretDown.svg';
import { ReactComponent as Compass } from '../../assets/icons/compass.svg';
import { ReactComponent as MindMapping } from '../../assets/icons/mindMapping.svg';
import { findNodeTitles } from './util';
import { TreeData } from './constant';
import eventBus from './evnets';
import { useScreen } from '../AllFilesView/context';

const InputSearch = Input.Search;

function searchData(inputValue: any) {
  const loop = (data: any) => {
    const result: any[] = [];
    data.forEach((item: any) => {
      if (item.title.toLowerCase().indexOf(inputValue.toLowerCase()) > -1) {
        result.push({ ...item });
      } else if (item.children) {
        const filterData = loop(item.children);

        if (filterData.length) {
          result.push({ ...item, children: filterData });
        }
      }
    });
    return result;
  };

  return loop(TreeData);
}
const SideBar: React.FC<{
  handleSelectedTree?: (breadcrumbData: any[], value: string[]) => void;
  selectedNodeKey?: any[];
}> = ({ handleSelectedTree, selectedNodeKey }) => {
  const { currentScreen } = useScreen();
  const [checked, setChecked] = useState(true);
  const [treeData, setTreeData] = useState(TreeData);
  const [inputValue, setInputValue] = useState('');
  const [activeIndex, setActiveIndex] = useState(null);
  const handleDivClick = (index: any) => {
    setActiveIndex(index);
  };
  useEffect(() => {
    if (!inputValue) {
      setTreeData(TreeData);
    } else {
      const result = searchData(inputValue);
      setTreeData(result);
    }
  }, [inputValue]);
  return (
    <div
      className={css`
        display: flex;
        width: 280px;
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
        padding-left: 15px;
        align-self: stretch;
        border-right: 1px solid var(--color-border-2, #e5e6eb);
        background: #f7f8fa;
      `}
    >
      <div
        className={css`
          display: flex;
          height: 56px;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          padding-bottom: 5px;
          border-bottom: 1px solid var(--color-border-2, #e5e6eb);
        `}
      >
        <div
          className={css`
            display: flex;
            width: 280px;
            padding: 6px 8px 6px 12px;
            align-items: center;
            gap: 10px;
          `}
        >
          <IconArrowLeft />
          <Typography.Text>Dashboard</Typography.Text>
        </div>
      </div>

      <div
        className={css`
          display: flex;
          width: 280px;
          padding: 12px 8px 4px 12px;
          align-items: center;
          color: ${activeIndex === 0 ? '#165dff' : ''};
        `}
        onClick={() => handleDivClick(0)}
      >
        <MindMapping
          style={{ fill: activeIndex === 0 ? '#165dff' : '#4E5969' }}
        />
        <div
          className={css`
            display: flex;
            padding-left: 8px;
            flex-direction: column;
            justify-content: center;
            align-items: flex-start;
            flex: 1 0 0;
          `}
        >
          Structure
        </div>
      </div>
      <div
        className={css`
          display: flex;
          width: 280px;
          padding: 3px 8px 16px 12px;
          align-items: center;
          color: ${activeIndex === 1 ? '#165dff' : ''};
          margin-bottom: 25px;
          border-bottom: 1px solid var(--color-border-2, #e5e6eb);
        `}
        onClick={() => handleDivClick(1)}
      >
        <Compass style={{ fill: activeIndex === 1 ? '#165dff' : '#4E5969' }} />
        <div
          className={css`
            display: flex;
            padding-left: 8px;
            flex-direction: column;
            justify-content: center;
            align-items: flex-start;
            flex: 1 0 0;
          `}
        >
          Insights
        </div>
      </div>

      <div
        className={css`
          display: flex;
          margin-top: -20px;
          margin-bottom: -8px;
          padding: 0px 12px;
          align-items: flex-start;
          gap: 12px;
          align-self: stretch;
        `}
      >
        <InputSearch
          allowClear
          placeholder="Go to file"
          style={{ width: 216, backgroundColor: '#f7f8fa' }}
          className={css`
            border-radius: 188px;
          `}
          onChange={setInputValue}
        />
        <Button icon={<IconPlus />} style={{ borderRadius: '8px' }} />
      </div>

      <div
        className={css`
          display: flex;
          padding: 16px 8px;
          flex-direction: column;
          align-self: stretch;
        `}
      >
        <Tree
          defaultExpandedKeys={['0-0', '0-1']}
          defaultSelectedKeys={['0-0-0', '0-0-1']}
          selectedKeys={selectedNodeKey}
          onSelect={(value, info) => {
            // console.log(selectedNodeKey);
            console.log('Current screen:', currentScreen);
            const breadcrumbData = findNodeTitles(treeData, value[0]);
            handleSelectedTree && handleSelectedTree(breadcrumbData, value);
            eventBus.emit(
              `clickTreeItem-${currentScreen}`,
              info.node.props.dataRef
              // currentScreen
            );
            // console.log(currentScreen);
          }}
          onExpand={(keys, info) => {
            console.log(keys, info);
          }}
          treeData={treeData}
          showLine={checked}
          icons={{ switcherIcon: <CaretDown /> }}
          renderTitle={({ dataRef }) => {
            // console.log(dataRef);
            if (inputValue) {
              const index = (dataRef?.title as string)
                .toLowerCase()
                .indexOf(inputValue.toLowerCase());

              if (index === -1) {
                return dataRef?.title;
              }

              const prefix = (dataRef?.title as string).substr(0, index);
              const suffix = (dataRef?.title as string).substr(
                index + inputValue.length
              );
              console.log(prefix);
              return (
                <span>
                  {prefix}
                  <span style={{ color: 'var(--color-primary-light-4)' }}>
                    {(dataRef?.title as string).substr(
                      index,
                      inputValue.length
                    )}
                  </span>
                  {suffix}
                </span>
              );
            }
            return (
              <div>
                {dataRef?.type === 'folder' ? (
                  <IconFolder className="treeTitle" />
                ) : (
                  <IconFile className="treeTitle" />
                )}
                {dataRef?.title}
              </div>
            );
          }}
        ></Tree>
      </div>
      <div
        className={css`
          width: 280px;
          height: 180px;
          background: #f7f8fa;
        `}
      ></div>
    </div>
  );
};

export { SideBar };
