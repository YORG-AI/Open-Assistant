import React, { MouseEvent } from 'react';
import './cardItem.scss';
import {
  IconFolder,
  IconMoreVertical,
  IconLoading,
  IconCheckCircle,
  IconCloseCircle,
  IconPlayCircle,
  IconLoop,
  IconDelete,
} from '@arco-design/web-react/icon';
import { Card, Tag, Button, Dropdown, Menu } from '@arco-design/web-react';
import { useLocation, useNavigate } from 'react-router-dom';
interface MyCardInterFace {
  firstName: string;
  secondName: string;
  desc: string;
  type: number;
  time: number;
}
const CardItem: React.FC<MyCardInterFace> = (props) => {
  const location = useLocation();
  const isDatabase = location.pathname.includes('database');
  const { firstName, secondName, desc, time, type }: MyCardInterFace = props;
  const dropList = (
    <Menu>
      <Menu.Item key="1" style={{ color: '#6AA1FF' }}>
        <IconLoop />
        Resync
      </Menu.Item>
      <Menu.Item key="2" style={{ color: 'red' }}>
        <IconDelete />
        Remove
      </Menu.Item>
    </Menu>
  );
  const navigate = useNavigate();
  return (
    <Card
      className="my_card"
      onClick={() => {
        navigate(isDatabase ? '/database/detail/1' : '/codebase/detail/1');
      }}
    >
      <div className="c_header">
        <div className="c_avatar">
          <IconFolder />
        </div>
        <div className="c_title">
          <span className="first_name">{firstName}</span>
          <span> / </span>
          <span className="second_name">{secondName}</span>
        </div>
      </div>
      <div className="c_desc">{desc}</div>
      <div className="c_tag_controller">
        {type === 1 && (
          <Tag
            style={{ marginRight: 8 }}
            className="success_tag"
            icon={<IconCheckCircle style={{ color: '#00B42A' }} />}
          >
            Ready
          </Tag>
        )}
        {type === 2 && (
          <Tag
            style={{ marginRight: 8 }}
            className="loading_tag"
            icon={<IconLoading style={{ color: '#FF7D00' }} />}
          >
            Loading: 84%
          </Tag>
        )}
        {type === 3 && (
          <Tag
            style={{ marginRight: 8 }}
            className="queued_tag"
            icon={<IconPlayCircle style={{ color: '#0FC6C2' }} />}
          >
            Queued
          </Tag>
        )}
        {type === 4 && (
          <Tag
            style={{ marginRight: 8 }}
            className="fail_tag"
            icon={<IconCloseCircle style={{ color: '#F53F3F' }} />}
          >
            Failed
          </Tag>
        )}
        <div className="time">{time} min ago</div>
        <div className="button_group">
          {/* <Button type="outline" size="mini">
            View
          </Button> */}
          <Dropdown droplist={dropList} position="bl">
            <Button
              size="mini"
              type="outline"
              onClick={(e: Event) => e.stopPropagation()}
              icon={<IconMoreVertical />}
              style={{ marginLeft: 8 }}
              className="moreIcon"
            ></Button>
          </Dropdown>
        </div>
      </div>
    </Card>
  );
};
export { CardItem };
