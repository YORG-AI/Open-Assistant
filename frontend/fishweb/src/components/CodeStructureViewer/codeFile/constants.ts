import { TableColumnProps } from "@arco-design/web-react";

export const columns: TableColumnProps[] = [
    {
      title: 'Name',
      dataIndex: 'name',
      headerCellStyle: {
        display: 'flex',
        width: '276px',
        flexDirection: 'column',
        alignItems: 'flexStart',
      },
    },
  
    {
      title: 'Last commit message',
      dataIndex: 'address',
      headerCellStyle: {
        width: '595.8px',
        flexDirection: 'column',
        alignItems: 'flexStart',
        flex: '1',
      },
    },
    {
      title: 'Last commit time',
      dataIndex: 'email',
      headerCellStyle: {
        display: 'flex',
        width: '160.196px',
        flexDirection: 'column',
        alignItems: 'flexStart',
      },
    },
  ];
export const data = [
    {
      key: '1',
      name: 'Jane Doe',
      address: 'Initial',
      email: 'Now',
    },
    {
      key: '2',
      name: 'Alisa Ross',
      address: 'Initial',
      email: '2 hours ago',
    },
    {
      key: '3',
      name: 'Kevin Sandra',
      address: 'Added English readme',
      email: '2 hours ago',
    },
    {
      key: '4',
      name: 'Ed Hellen',
      address: 'Initial',
      email: '2 hours ago',
    },
    {
      key: '5',
      name: 'William Smith',
      address: 'Node setup',
      email: '2 hours ago',
    },
    {
      key: '6',
      name: 'William Smith',
      salary: 27000,
      address: 'Added OpenAI Node',
      email: '2 hours ago',
    },
  ];