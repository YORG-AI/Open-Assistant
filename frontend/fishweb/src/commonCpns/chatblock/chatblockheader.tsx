import { useState } from 'react';
import './index.scss';
import { Avatar, Breadcrumb, Button } from '@arco-design/web-react';
import { IconDown, IconUp } from '@arco-design/web-react/icon';
const BreadcrumbItem = Breadcrumb.Item;

const ChatBlockHeader = ({ onArrowClick }: { onArrowClick: any }) => {
  const [isshow, setIsShow] = useState(true);
  const handleArrowClick = () => {
    setIsShow(!isshow);
    onArrowClick(!isshow); // 调用父组件传递的回调函数并传递状态值
  };
  return (
    <div className="cardheader">
      <div className="headerbox">
        <div className="boxleft">
          <Avatar />
          <BreadcrumbItem href="#">ATAH</BreadcrumbItem>
          <BreadcrumbItem>uploaded:</BreadcrumbItem>
        </div>
        <div className="boxright" onClick={handleArrowClick}>
          {isshow ? <IconDown /> : <IconUp />}
        </div>
      </div>
    </div>
  );
};
const ChatErrorHeader = () => {
  return (
    <div className="cardheader error">
      <div className="headerbox">
        <div className="boxleft">
          <Avatar />
          An error occured
        </div>
        <div className="boxright">
          <Button type="text">Regenerate</Button>
        </div>
      </div>
    </div>
  );
};
export { ChatBlockHeader, ChatErrorHeader };
