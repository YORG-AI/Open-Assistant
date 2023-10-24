import { css } from '@emotion/css';
import { useState } from 'react';
import { Empty, Table, TableColumnProps } from '@arco-design/web-react';

const columns: TableColumnProps[] = [
  {
    title: 'Repo Title',
    dataIndex: 'name',
    headerCellStyle: {
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'flexStart',
      alignSelf: 'stretch',
    },
  },

  {
    title: 'Current Branch',
    dataIndex: 'current',
    headerCellStyle: {
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'flexStart',
      alignSelf: 'stretch',
    },
  },
  {
    title: 'Repo Location',
    dataIndex: 'location',
    headerCellStyle: {
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'flexStart',
      alignSelf: 'stretch',
    },
  },
  {
    title: 'Status',
    dataIndex: 'status',
    headerCellStyle: {
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'flexStart',
      alignSelf: 'stretch',
    },
  },
  {
    title: 'Last Updated',
    dataIndex: 'email',
    headerCellStyle: {
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'flexStart',
      alignSelf: 'stretch',
    },
  },
  {
    title: 'Action',
    dataIndex: 'action',
    headerCellStyle: {
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'flexStart',
      alignSelf: 'stretch',
    },
  },
];

const ListView = (props: any) => {
  const [selectedItem, setSelectedItem] = useState(null);
  const handleRowClick = (selectedRowKeys: any) => {
    // 设置选中项
    // setSelectedItem(record);
    // 显示按钮
    props.onClickItem(true, selectedRowKeys);
  };
  return (
    <div
      className={css`
        margin-top: 24px;
        display: flex;
        align-items: flex-start;
        align-self: stretch;
      `}
    >
      {props.data.length > 0 ? (
        <Table
          columns={columns}
          data={props.data}
          style={{ width: '1140px' }}
          pagination={false}
          rowSelection={{
            type: 'checkbox',
            onChange: (selectedRowKeys, selectedRows) => {
              console.log(selectedRowKeys, selectedRows);
              handleRowClick(selectedRowKeys);
            },
          }}
          onRow={(record) => ({
            onClick: () => {
              // handleRowClick(record), console.log(record);
            },
          })}
        ></Table>
      ) : (
        <Empty />
      )}
    </div>
  );
};
export { ListView };
