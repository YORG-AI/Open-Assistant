import './AgentChatItem.scss';
import { IconCopy, IconQuote } from '@arco-design/web-react/icon';

import { Fragment, useEffect, useRef, useState } from 'react';
import { ChatBlockHeader } from '../chatblock/chatblockheader';

const AgentChatItem = ({ children }: { children?: string }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedText, setEditedText] = useState(children || '');
  const [isShow, setIsShow] = useState(true); // 在父组件中定义状态

  // 定义一个回调函数，用于接收子组件传递的状态值
  const handleArrowClick = (newIsShow: any) => {
    setIsShow(newIsShow);
  };
  const ref = useRef<HTMLTextAreaElement>(null);
  // 创建一个隐藏的文本输入框
  const copyInputRef = useRef<HTMLInputElement>(null);
  useEffect(() => {
    if (ref.current !== null) {
      ref.current.style.height = '0px';
      ref.current.style.height = ref.current.scrollHeight + 'px';
    }
  }, [ref, editedText, isEditing]);
  const handleCopyText = () => {
    if (copyInputRef.current) {
      copyInputRef.current.value = editedText;
      copyInputRef.current.select();
      document.execCommand('copy');
      copyInputRef.current.setSelectionRange(0, 0); // 取消选中文本
    }
  };
  return (
    <div className="AgentChatItem">
      <ChatBlockHeader onArrowClick={handleArrowClick} />
      {isShow ? (
        <>
          <div className="chatText">
            <Fragment>{editedText}</Fragment>
            <div className="text_icon">
              <IconQuote style={{ color: '#4E5969', cursor: 'pointer' }} />
              <IconCopy
                style={{ color: '#4E5969', cursor: 'pointer' }}
                onClick={handleCopyText}
              />
            </div>
          </div>
        </>
      ) : (
        ''
      )}
      {/* 隐藏的文本输入框用于复制文本到剪贴板 */}
      <input
        type="text"
        ref={copyInputRef}
        style={{ position: 'absolute', left: '-9999px', top: '-9999px' }}
        readOnly
      />
    </div>
  );
};

export { AgentChatItem };
