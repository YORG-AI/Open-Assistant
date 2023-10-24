import { useState } from 'react';
import './chathistory.scss';
import { Input, Button, Avatar, List } from '@arco-design/web-react';
import {
  IconEdit,
  IconDelete,
  IconDown,
  IconLoading,
  IconCheck,
  IconClose,
  IconShrink,
  IconFullscreen,
  IconPlus,
  IconMoreVertical,
} from '@arco-design/web-react/icon';

const ChatHistorySpread = () => {
  const [dataSource, setDataSource] = useState(
    new Array(8).fill(null).map(() => ({
      title: 'Explain this script. Help me gain a better unders...',
      description: 'Sep 20, 2023  14:25',
      deleted: false,
      isEditing: false,
    }))
  );

  const [loading, setLoading] = useState(false);
  const [selectedRow, setSelectedRow] = useState(null);
  const [isEditing, setIsEditing] = useState(false); // 用于跟踪编辑状态的状态变量
  const [editedTitle, setEditedTitle] = useState('');
  const [isShrink, setisShrink] = useState(true);

  const render = (actions: any, item: any, index: any) => (
    <List.Item
      key={index}
      actions={actions}
      className={`list-item ${index === selectedRow ? 'selected' : ''} ${
        item.deleted ? 'deleted' : ''
      }`}
      onClick={() => handleSelectRow(index)}
    >
      <List.Item.Meta
        avatar={
          item.deleted ? (
            <Avatar shape="circle" style={{ background: 'red' }}>
              <IconDelete />
            </Avatar>
          ) : (
            <Avatar shape="circle">A</Avatar>
          )
        }
        title={
          item.isEditing ? ( // 当编辑时显示输入字段
            <Input
              disabled={false}
              value={editedTitle}
              onChange={(editedTitle) => setEditedTitle(editedTitle)}
            />
          ) : (
            item.title // 正常情况下显示标题
          )
        }
        description={item.isEditing ? '' : item?.description}
      />

      {index === selectedRow && !item.deleted ? (
        <>
          {item.isEditing ? ( // Display Save button during editing
            <div className="deleteIcon">
              <span
                className="list-demo-actions-icon adjustaa"
                onClick={() => handleSaveTitle(index)}
              >
                <IconCheck />
              </span>
            </div>
          ) : (
            <span // Display Edit button when not editing
              className="list-demo-actions-icon bdjust"
              onClick={() => handleEditTitle(index)}
            >
              <IconEdit />
            </span>
          )}
          {item.isEditing ? (
            // Display Save button during editing
            <div className="deleteIconb">
              <span
                className="list-demo-actions-icon adjustbb"
                onClick={() => handleSaveTitle(index)}
              >
                <IconClose />
              </span>
            </div>
          ) : (
            <span
              className="list-demo-actions-icon bdjustb"
              onClick={() => {
                handleDeleteRow(index);
              }}
            >
              <IconDelete />
            </span>
          )}
        </>
      ) : (
        // 根据 isDeleted 属性渲染不同的内容
        <>
          {item.isEditing ? (
            <div className="deleteIcon">
              <span
                className="list-demo-actions-icon adjust"
                onClick={() => {
                  handleConfirmDelete(index);
                }}
              >
                <IconCheck />
              </span>
              <span className="list-demo-actions-icon adjust">
                <IconClose
                  onClick={() => {
                    handleCancelDelete(index);
                  }}
                />
              </span>
            </div>
          ) : item.deleted ? (
            <div className="deleteIconn ">
              <span
                className="list-demo-actions-icon bdjust"
                onClick={() => {
                  handleConfirmDelete(index);
                }}
              >
                <IconCheck />
              </span>
              <span className="list-demo-actions-icon bdjustb">
                <IconClose
                  onClick={() => {
                    handleCancelDelete(index);
                  }}
                />
              </span>
            </div>
          ) : (
            ''
          )}
        </>
      )}
    </List.Item>
  );
  const handleEditTitle = (index: any) => {
    const newDataSource = [...dataSource];
    newDataSource[index].isEditing = true;
    setEditedTitle(newDataSource[index].title);
    setSelectedRow(index);
    setDataSource(newDataSource);
  };

  const handleSaveTitle = (index: any) => {
    const newDataSource = [...dataSource];
    newDataSource[index].title = editedTitle;
    newDataSource[index].isEditing = false;
    setDataSource(newDataSource);
    setSelectedRow(null);
  };
  const handleConfirmDelete = (index: any) => {
    // 复制当前数据源
    const newDataSource = [...dataSource];

    // 直接从数据源中删除数据项
    newDataSource.splice(index, 1);

    // 更新数据源
    setDataSource(newDataSource);

    // 解决异步问题
    setTimeout(() => {
      setSelectedRow(null);
    }, 0);
  };
  const handleCancelDelete = (index: any) => {
    // 复制当前数据源
    const newDataSource = [...dataSource];
    // 取消删除标志，恢复原始状态
    newDataSource[index].deleted = false;
    newDataSource[index].title =
      'Explain this script. Help me gain a better unders...';
    newDataSource[index].description = 'Sep 20, 2023  14:25';
    console.log(newDataSource[index]);
    // 更新数据源
    setDataSource(newDataSource);
  };
  const handleSelectRow = (index: any) => {
    setSelectedRow(index);
  };
  const handleDeleteRow = (index: any) => {
    console.log(index);

    const newDataSource = [...dataSource];

    newDataSource[index].deleted = true;
    newDataSource[index].title = 'Delete this record?';
    newDataSource[index].description = 'This action is irreversible.';
    console.log(newDataSource[index]);
    // 更新数据源
    setDataSource(newDataSource);
    //解决异步问题
    setTimeout(() => {
      setSelectedRow(null);
    }, 0);
  };

  const footer = (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        cursor: 'pointer',
        marginBottom: '10px',
      }}
      onClick={() => setLoading(!loading)}
      onKeyDown={(e) => {
        const keyCode = e.keyCode || e.which;
        if (keyCode === 13) {
          // enter
          setLoading(!loading);
        }
      }}
    >
      {loading ? (
        <span style={{ color: 'var(--color-text-3)' }}>
          <IconLoading
            style={{ marginRight: 8, color: 'rgb(var(--arcoblue-6))' }}
          />
          loading...
        </span>
      ) : (
        <span className="list-demo-actions-button" tabIndex={0}>
          More
          <IconDown style={{ marginLeft: 8 }} />
        </span>
      )}
    </div>
  );
  return (
    <div className="chathistspread">
      <div className="boxheader">
        <div className="btncon">
          <Button shape="circle" type="secondary" icon={<IconClose />} />
          {isShrink ? (
            <Button
              shape="circle"
              type="secondary"
              icon={<IconFullscreen />}
              onClick={() => {
                setisShrink(false);
              }}
            />
          ) : (
            <Button
              shape="circle"
              type="secondary"
              icon={<IconShrink />}
              onClick={() => {
                setisShrink(true);
              }}
            ></Button>
          )}
        </div>
        Chat History
        <div className="btncon">
          <Button
            style={{
              gap: '10px',
              width: '76px',
              borderRadius: '18px',
              background: '#fff',
            }}
            shape="square"
            type="secondary"
            icon={<IconDelete />}
          />
          <Button
            style={{
              gap: '10px',
              width: '76px',
              borderRadius: '18px',
              background: '#fff',
            }}
            shape="square"
            type="secondary"
            icon={<IconPlus />}
          />
        </div>
      </div>
      <div className="boxlist">
        <List
          className="list-demo-actions"
          style={{ width: 1068, marginBottom: 48 }}
          dataSource={dataSource}
          render={render.bind(null, [])}
          footer={footer}
        />
      </div>
    </div>
  );
};
export { ChatHistorySpread };
