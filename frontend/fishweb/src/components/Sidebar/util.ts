// 辅助函数：根据tree节点的 key 查找节点及其父级节点的标题
export const findNodeTitles = (nodes: any[], key: string) => {
  const titles: any[] = [];
  const findNode = (nodeData: any[]) => {
    for (const node of nodeData) {
      if (node.key === key) {
        titles.unshift({ key: node.key, title: node.title, content: node.content }); // 在数组开头插入标题
        return true;
      }
      if (node.children && findNode(node.children)) {
        titles.unshift({ key: node.key, title: node.title, content: node.content }); // 在数组开头插入标题
        return true;
      }
    }
    return false;
  };
  findNode(nodes);
  return titles;
};