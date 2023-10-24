import {
  Button,
  Dropdown,
  Menu,
  Modal,
  Select,
  Tabs,
} from '@arco-design/web-react';
import {
  IconArrowLeft,
  IconArrowRight,
  IconCodeSquare,
  IconDown,
  IconTool,
} from '@arco-design/web-react/icon';
import { FC, useEffect, useState } from 'react';
import './index.scss';
import { useLocation } from 'react-router-dom';
import { topButtonTypeAtom } from '../../page/allAtom';
import { useAtom } from 'jotai';
export const TopOperation: FC = () => {
  const [topButtonType, setTopButtonType] = useAtom(topButtonTypeAtom);
  const [visible, setVisible] = useState(false);
  const Option = Select.Option;
  const location = useLocation();
  useEffect(() => {
    // setTopButtonType(3);
    console.log(location.pathname.includes('codepath'));
    if (location.pathname.includes('codepath')) {
      setTopButtonType(2);
    }
  }, [location]);
  console.log('state右侧', topButtonType);
  return (
    <div className="topOperationStyle">
      <div className="topOperationStyle-left">
        <div className="topOperationStyle-left-icon">
          <IconArrowLeft className="iconLeft" />
          <IconArrowRight className="iconRignt" />
        </div>
        {topButtonType === 3 && (
          <div className="topOperationStyle-left-tabs">
            <div>
              <IconCodeSquare />
              All Files
            </div>
            <div className="active">
              <IconTool />
              Workspace
            </div>
          </div>
        )}
      </div>
      {topButtonType === 2 && (
        <div className="topOperationStyle-right">
          <Button type="outline" className="marginRight10">
            Explore
          </Button>
          <Button type="primary">Analyze</Button>
        </div>
      )}
      {topButtonType === 3 && (
        <div className="topOperationStyle-right">
          <Button
            type="primary"
            onClick={() => {
              setVisible(true);
            }}
          >
            Save changes
          </Button>
        </div>
      )}
      <Modal
        title="Save"
        visible={visible}
        footer={
          <div>
            <Button className="marginRight10">Cancel</Button>
            <Dropdown.Button
              type="primary"
              droplist={
                <Menu>
                  <Menu.Item
                    key="1"
                    onClick={() => {
                      setVisible(false);
                    }}
                  >
                    Save{' '}
                  </Menu.Item>
                  <Menu.Item
                    key="2"
                    onClick={() => {
                      // to file path
                      setVisible(false);
                    }}
                  >
                    Save and exit
                  </Menu.Item>
                </Menu>
              }
              icon={<IconDown />}
            >
              Save changes
            </Dropdown.Button>
          </div>
        }
        onOk={() => setVisible(false)}
        onCancel={() => setVisible(false)}
      >
        <div className="modalStyle">
          <div>Save all the files to this pathway:</div>
          <Select placeholder="Please select">
            <Option key={1} value={1}>
              111
            </Option>
          </Select>
        </div>
      </Modal>
    </div>
  );
};
