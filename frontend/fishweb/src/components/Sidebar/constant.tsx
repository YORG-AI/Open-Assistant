import { Table, TreeSelect } from '@arco-design/web-react';
import { ReactNode } from 'react';
import { columns, data } from '../CodeStructureViewer/codeFile/constants';
const TreeNode = TreeSelect.Node;
interface TreeNode {
  title: React.ReactNode;
  key: string;
  type: 'folder' | 'file'; // 添加 type 属性表示节点类型
  content?: string | ReactNode; // 文件内容
  children?: TreeNode[];
}

const table = <Table columns={columns} data={data} pagination={false} />;
export const TreeData: TreeNode[] = [
  {
    title: 'new_backend',
    content: table,
    key: '0-0',
    type: 'folder',
    children: [
      {
        title: 'document',
        content: <h1>document</h1>,
        key: '0-0-2',
        type: 'folder',
        children: [
          {
            title: 'main.py',
            key: '0-0-2-1',
            content: <h1>main.py</h1>,
            type: 'file',
            children: [
              {
                title: 'Leafsss 0-0-2',
                key: '0-0-2-1-0',
                type: 'file',
                content: <h1>Leafsss 0-0-2</h1>
              },
            ],
          },
          {
            title: 'readme.md',
            key: '0-0-2-2',
            type: 'file',
            content: <h1>readme.md</h1>
          },
          {
            title: 'component.py',
            key: '0-0-2-3',
            type: 'file',
            content: <h1>component.py</h1>
          },
          {
            title: 'node_setup.py',
            key: '0-0-2-4',
            type: 'folder',
            content: <h1>node_setup.py</h1>,
            children: [
              {
                title: 'nodes',
                key: '0-0-2-4-0',
                content: table,
                type: 'folder',
                children: [
                  {
                    title: 'openai.py',
                    key: '0-0-2-2-0-0',
                    content: <h1>openai.py</h1>,
                    type: 'file',
                  },
                  {
                    title: 'claude.py',
                    key: '0-0-2-2-0-1',
                    content: <h1>claude.py</h1>,
                    type: 'file',
                  },
                ],
              },
            ],
          },
        ],
      },
      {
        title: 'docker',
        key: '0-0-3',
        type: 'folder',
        content: table,
        children: [
          {
            title: 'Leaf',
            key: '0-0-3-1',
            type: 'file',
            content: <h1>Leaf</h1>,
          },
          {
            title: 'Leaf',
            key: '0-0-3-2',
            type: 'folder',
            content: <h1>Leaf</h1>,
            children: [
              {
                title: 'Leafsss 0-0-2',
                key: '0-0-3-2-0',
                type: 'file',
                content: <h1>Leafsss 0-0-2</h1>,
              },
            ],
          },
        ],
      },
      {
        title: 'llm_files',
        key: '0-0-4',
        type: 'folder',
        content: table,
        children: [
          {
            title: 'Leaf',
            key: '0-0-4-1',
            type: 'file',
            content: <h1>Leaf</h1>,
          },
        ],
      },
    ],
  },
  {
    title: 'new_backend',
    key: '0-1',
    type: 'folder',
    content: table
  },
];
