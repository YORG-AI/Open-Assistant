import { css } from '@emotion/css';
import './UserChatItem.scss';
import { IconEdit } from '@arco-design/web-react/icon';

import { Fragment, useEffect, useRef, useState } from 'react';
import { ChatBlockHeader } from '../chatblock/chatblockheader';

const UserChatItem = ({ children }: { children?: string }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedText, setEditedText] = useState(children || '');
  const [isShow, setIsShow] = useState(true); // 在父组件中定义状态

  // 定义一个回调函数，用于接收子组件传递的状态值
  const handleArrowClick = (newIsShow: any) => {
    setIsShow(newIsShow);
  };
  const ref = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (ref.current !== null) {
      ref.current.style.height = '0px';
      ref.current.style.height = ref.current.scrollHeight + 'px';
    }
  }, [ref, editedText, isEditing]);

  return (
    <div className="UserChatItem">
      <ChatBlockHeader onArrowClick={handleArrowClick} />

      {isShow ? (
        <>
          <div className="chatText">
            {!isEditing ? (
              <Fragment>{editedText}</Fragment>
            ) : (
              <textarea
                ref={ref}
                value={editedText}
                onChange={(e) => {
                  setEditedText(e.target.value);
                }}
                className="textarea"
              />
            )}
            <div className="text_icon">
              <IconEdit
                style={{ color: '#4E5969', cursor: 'pointer' }}
                onClick={() => {
                  setIsEditing(!isEditing);
                }}
              />
            </div>
          </div>
        </>
      ) : (
        ''
      )}
    </div>
  );
};

export { UserChatItem };
