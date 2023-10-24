import { Button, Input, Dropdown, Menu } from '@arco-design/web-react';
import {
  IconClose,
  IconFullscreen,
  IconShrink,
  IconPlus,
  IconLeft,
  IconSend,
  IconMessage,
  IconPlayArrow,
  IconWechat,
  IconEdit,
  IconPause,
  IconPauseCircle,
  IconCloseCircle,
  IconLoop,
} from '@arco-design/web-react/icon';
import { UserChatItem } from './UserChatItem';
import './index.scss';
import { useState } from 'react';
import { AgentChatItem } from './AgentChatItem';
import { ChatFileCard, FileRoleCard } from './chatFileCard';
const ChatModel = () => {
  const [isShrink, setisShink] = useState(true);
  const [inputText, setInputText] = useState('');
  const [chatHistory, setChatHistory] = useState<
    { text: string; isUser: boolean }[]
  >([]);
  const [ispopup, setIspopup] = useState(false);

  const handleInputChange = (e: any) => {
    console.log(e);
    setInputText(e);
  };

  const handleSubmit = () => {
    if (inputText?.trim() !== '') {
      // 创建新的聊天记录对象并添加到聊天历史中
      const newChatItem = {
        text: inputText,
        isUser: true, // 假设用户发送的消息
      };
      setChatHistory([...chatHistory, newChatItem]);
      setInputText(''); // 清空输入框
    }
  };
  return (
    <div className="chatblock">
      <div className="chat_header">
        <div className="header-left">
          <Button shape="circle" type="secondary" icon={<IconClose />} />
          {isShrink ? (
            <Button
              shape="circle"
              type="secondary"
              icon={<IconFullscreen />}
              // onClick={() => {
              //   setisShrink(false);
              // }}
            />
          ) : (
            <Button
              shape="circle"
              type="secondary"
              icon={<IconShrink />}
              // onClick={() => {
              //   setisShrink(true);
              // }}
            ></Button>
          )}
        </div>
        <div className="header-mid">
          <IconLeft />
          Chat History
        </div>

        <div className="header-right">
          <Dropdown
            position="bl"
            trigger="click"
            droplist={
              <Menu>
                <Menu.Item key="1" className="popupitem">
                  <IconMessage />
                  Explain Code
                </Menu.Item>
                <Menu.Item key="2" className="popupitem">
                  <IconEdit />
                  Generate Code
                </Menu.Item>
              </Menu>
            }
          >
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
          </Dropdown>
        </div>
      </div>
      <div className="chat_content">
        {/* 动态渲染聊天记录 */}
        {chatHistory.map((chatItem, index) => {
          if (chatItem.isUser) {
            return <UserChatItem key={index}>{chatItem.text}</UserChatItem>;
          } else {
            return <AgentChatItem key={index}>{chatItem.text}</AgentChatItem>;
          }
        })}
      </div>
      <div className="chat_footer">
        <Input
          allowClear
          style={{ width: 426, height: 48 }}
          suffix={
            <Button
              style={{
                width: 34,
                height: 34,
                padding: 5,
              }}
              onClick={handleSubmit}
            >
              <IconSend style={{ textAlign: 'center' }} />
            </Button>
          }
          placeholder="Please enter"
          value={inputText}
          onPressEnter={handleSubmit}
          //很关键 卡我好久 记得看onchange传的props类型，只有string的，没有event type
          onChange={(inputText) => {
            handleInputChange(inputText);
          }}
        />
      </div>
      <div className="chat_footer_btnbox">
        <div className="chat_footer_btngroup ">
          <Button type="secondary" style={{ width: 122 }}>
            <IconMessage />
            Intervene
          </Button>
          <Button type="secondary" style={{ width: 288 }}>
            <IconPlayArrow />
            Nest Step
          </Button>
        </div>
      </div>
      <div className="chat_footer_btngroup ">
        <Button type="secondary">
          <IconPauseCircle />
          Pause
        </Button>
        <Button type="secondary">
          <IconCloseCircle />
          Stop
        </Button>
        <Button type="secondary">
          <IconLoop />
          Regenerate
        </Button>
      </div>
      <ChatFileCard>openai.py</ChatFileCard>
      {/* <FileRoleCard RoleFile="userupload"></FileRoleCard> */}
    </div>
  );
};
export { ChatModel };
