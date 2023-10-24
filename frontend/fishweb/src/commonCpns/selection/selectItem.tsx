import { css } from '@emotion/css';
import { Input, Link, Modal, Select } from '@arco-design/web-react';
import PropTypes from 'prop-types';
import { IconSettings } from '@arco-design/web-react/icon';
import { useState } from 'react';
import { options1, options2 } from './constants';
interface SelectItemProps {
  suffixBtn?: JSX.Element;
  tig: string;
  subtitle: string;
}
const Option = Select.Option;
const SelectItem: React.FC<SelectItemProps> = ({
  suffixBtn,
  tig,
  subtitle,
}) => {
  const [visible, setVisible] = useState(false);

  return (
    <div
      className={css`
        display: flex;
        width: 613px;
        height: 68px;
        box-sizing: border-box;
        padding: 12px 24px;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid var(--color-border-2, #e5e6eb);
      `}
    >
      <div
        className={css`
          display: flex;
          flex-direction: column;
          align-items: flex-start;
        `}
      >
        <div
          className={css`
            color: var(--color-text-1, #1d2129);
            /* 14/CN-Medium */
            font-family: PingFang SC;
            font-size: 14px;
            font-style: normal;
            font-weight: 500;
            line-height: 22px; /* 157.143% */
          `}
        >
          {tig ?? ''}
        </div>
        <div>
          {subtitle === 'special' ? (
            <span>
              Use your
              <Link
                href="#"
                onClick={() => {
                  setVisible(true);
                }}
              >
                preferred external editor <IconSettings />
              </Link>
            </span>
          ) : (
            subtitle
          )}
        </div>
      </div>

      <div
        className={css`
          display: flex;
          height: 36px;
          align-items: center;
          border-radius: 6px;
          border: 1px solid var(--primary-2, #bedaff);
          background: var(--primary-5, #4080ff);
        `}
      >
        {suffixBtn}
      </div>
      <Modal
        title="Choose external editor"
        visible={visible}
        okText="Update"
        cancelText="Cancel"
        onOk={() => setVisible(false)}
        onCancel={() => setVisible(false)}
      >
        <div style={{ padding: '12px 24px' }}>
          <p>Choose your preferred external editor</p>
          <Select placeholder="Master (Default)" allowClear>
            {options1.map((option, index) => (
              <Option key={option} value={option}>
                {option}
              </Option>
            ))}
          </Select>
          <p>Choose your preferred shell</p>
          <Select placeholder="Master (Default)" allowClear>
            {options2.map((option, index) => (
              <Option key={option} value={option}>
                {option}
              </Option>
            ))}
          </Select>
        </div>
      </Modal>
    </div>
  );
};
SelectItem.propTypes = {
  suffixBtn: PropTypes.any,
  tig: PropTypes.any,
  subtitle: PropTypes.any,
};
export { SelectItem };
