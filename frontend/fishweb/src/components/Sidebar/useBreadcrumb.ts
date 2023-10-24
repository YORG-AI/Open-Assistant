import { useState, useEffect } from 'react'
import { findNodeTitles } from './util';
import { TreeData } from './constant'
import eventBus from './evnets'
import { useScreen } from '../AllFilesView/context';
export function useBreadcrumb() {
  const { currentScreen } = useScreen();
  const [breadcrumbData, setBreadcrumbData] = useState<any[]>([]);
  const [selectedNodeKey, setSelectedNodeKey] = useState<any[]>(['0-0']);
  const onHandleSelectedTree = (data: any[], value: string[]) => {
    setSelectedNodeKey(value);
    setBreadcrumbData(data);
  };
  useEffect(() => {
    // 在 selectedNodeKey 发生变化时更新面包屑路径
    const data = findNodeTitles(TreeData, selectedNodeKey.toString());
    setBreadcrumbData(data);
  }, [selectedNodeKey]);
  const onClickTabItem = (key: string) => {
    setSelectedNodeKey([key])
  }
  useEffect(() => {
    eventBus.on(`clickTabItem-${currentScreen}`, onClickTabItem);
    return () => {
      if (eventBus) {
        eventBus.removeListener(`clickTabItem-${currentScreen}`, onClickTabItem);
      }
    };
  }, []);
  const handleBreadcrumbClick = (item: any, index: number) => {
    // 检查是否可以点击当前路径项
    if (index < breadcrumbData.length - 1) {
      // 更新当前所选节点的键
      const obj = breadcrumbData[index];
      setSelectedNodeKey([obj.key]);
      eventBus.emit(
        `clickTreeItem-${currentScreen}`,
        item
      );
    }
  };
  return { onHandleSelectedTree, breadcrumbData, selectedNodeKey, handleBreadcrumbClick }
}