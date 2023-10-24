import { FC, ReactNode } from 'react';
import { Button } from '@arco-design/web-react';
import {
  IconArrowRight,
  IconFile,
  IconList,
} from '@arco-design/web-react/icon';
interface ChatFileCardProps {
  children: ReactNode;
  pre?: ReactNode; // 指定 children 属性的类型为 ReactNode
}
type RoleFile = 'userupload' | 'agentgenerate';
const ChatFileCard: FC<ChatFileCardProps> = ({ children, pre }) => {
  return (
    <div>
      <Button>
        {pre}
        <IconFile />
        {children}
        <IconArrowRight />
      </Button>
    </div>
  );
};
const FileDetailIcon = () => {
  return (
    <div>
      <Button>
        <IconList />
        Details
      </Button>
    </div>
  );
};
const FileRoleCard = (props: { RoleFile: RoleFile }) => {
  const { RoleFile } = props;
  const userMark = <div className="userMark">|</div>;
  const agentMark = <div className="agentMark">|</div>;
  return (
    <div>
      <ChatFileCard pre={RoleFile === 'userupload' ? userMark : agentMark}>
        openai.py
      </ChatFileCard>
    </div>
  );
};
export { ChatFileCard, FileDetailIcon, FileRoleCard };
