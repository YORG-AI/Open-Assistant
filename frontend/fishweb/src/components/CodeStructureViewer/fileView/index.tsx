import React, { ReactNode, useEffect, useState } from 'react';
import { css } from '@emotion/css';
import './index.scss';
import { Breadcrumb, Button, Result, Tabs } from '@arco-design/web-react';
import {
  IconUnorderedList,
  IconMindMapping,
  IconCopy,
  IconPlayArrow,
  IconFile,
  IconInfoCircle,
  IconBulb,
} from '@arco-design/web-react/icon';
import OmsViewMarkdown from '../../OmsViewMarkdown';
import {
  textContent,
  markdown,
  markdown2,
} from '../../../page/IndvFileView/contant';
import '../../OmsViewMarkdown/markdown.scss';
import { useScreen } from '../../AllFilesView/context';
import eventBus from '../../Sidebar/evnets';
const TabPane = Tabs.TabPane;
const subTitle = (
  <div style={{ margin: '24px 0' }}>
    If you are satisfied with the report, click Generate. <br />
    Otherwise, please tell agent how it could improve.
  </div>
);
const FileView: React.FC<{
  children: ReactNode;
}> = (props) => {
  const { currentScreen, setCurrentScreen } = useScreen();
  const [code, setCode] = useState<string>(textContent);
  const [activeKey, setActiveKey] = useState<string>('1');
  const onClickTreeItem = (data: any) => {
    let { title, key } = data;
    setCode(title);
  };
  useEffect(() => {
    eventBus.on(`clickTreeItem-${currentScreen}`, (data: any) =>
      onClickTreeItem(data)
    );

    return () => {
      eventBus.removeListener(`clickTreeItem-${currentScreen}`, (data: any) =>
        onClickTreeItem(data)
      );
    };
  }, []);
  return (
    <div className="center_main_container">
      <div className="center_main_cover">
        {props.children}
        <div className="center_main">
          <Tabs size="large" activeTab={activeKey} onChange={setActiveKey}>
            <TabPane
              key="1"
              title={
                <span>
                  <IconUnorderedList style={{ marginRight: 8 }} />
                  Code
                </span>
              }
            >
              <div className="test">
                <OmsViewMarkdown textContent={code} />
              </div>
            </TabPane>
            <TabPane
              key="2"
              style={{ padding: '0 12px' }}
              title={
                <span>
                  <IconMindMapping style={{ marginRight: 8 }} />
                  Result
                </span>
              }
            >
              <div className="test">
                <OmsViewMarkdown textContent={markdown} />
              </div>
            </TabPane>
            <TabPane
              key="3"
              style={{ padding: '0 12px' }}
              title={
                <span>
                  <IconFile style={{ marginRight: 6 }} />
                  Report
                </span>
              }
            >
              <div className="test">
                <OmsViewMarkdown textContent={markdown2} />
              </div>
            </TabPane>
          </Tabs>
          {activeKey === '1' && (
            <Button
              type="primary"
              icon={<IconPlayArrow />}
              className="run_btn"
              onClick={() => setActiveKey('2')}
            >
              Run
            </Button>
          )}

          {/* Nothing generated yet -------------- */}
          {/* <Result
            className={css`
              position: absolute;
              top: 50%;
              left: 50%;
              transform: translate(-50%, -50%);
            `}
            icon={
              <IconInfoCircle
                style={{
                  color: 'var(--color-neutral-4)',
                  width: 48,
                  height: 48,
                }}
              />
            }
            status={null}
            title="Nothing generated yet"
          ></Result> */}
          {/* No report generated yet -------------- */}
          {/* <Result
            className={css`
              position: absolute;
              top: 50%;
              left: 50%;
              transform: translate(-50%, -50%);
            `}
            icon={
              <IconInfoCircle
                style={{
                  color: 'rgb(var(--orange-6))',
                  width: 48,
                  height: 48,
                }}
              />
            }
            status={null}
            title="No report generated yet"
            subTitle={subTitle}
            extra={[
              <Button
                key="back"
                type="outline"
                icon={<IconBulb />}
                style={{ borderRadius: 6 }}
              >
                Generate
              </Button>,
            ]}
          ></Result> */}
        </div>
      </div>
    </div>
  );
};
export default FileView;
