import React, { useState } from 'react';
import { Checkbox } from '@arco-design/web-react';
import { options } from './constant';
import { css } from '@emotion/css';
import './index.scss';
interface FileCheckBoxProps {
  onChangeCheckBoxList?: (value: any[]) => void;
}
const FileCheckBox: React.FC<FileCheckBoxProps> = (props) => {
  const { onChangeCheckBoxList } = props;
  const [selectedRows, setSelectedRows] = useState<any>([]);
  const handleChangeCheckBoxGroup = (value: any[], e: Event) => {
    // console.log(value);
    onChangeCheckBoxList && onChangeCheckBoxList(value);
    setSelectedRows(value);
  };
  return (
    <div className="fileCheckBox_wrapper">
      <Checkbox.Group direction="vertical" onChange={handleChangeCheckBoxGroup}>
        {options.map((item) => {
          return (
            <Checkbox
              key={item.value}
              value={item.value}
              className={css`
                display: flex;
              `}
              style={{
                background: selectedRows.includes(item.value)
                  ? 'rgb(var(--arcoblue-2))'
                  : '',
              }}
            >
              <div className="file_checkBox_main">
                <div className="file_checkBox_label">{item.label}</div>
                <div className="custom-checkbox-card-mask">
                  <div className="custom-checkbox-card-mask-dot"></div>
                </div>
              </div>
            </Checkbox>
          );
        })}
      </Checkbox.Group>
    </div>
  );
};
export default FileCheckBox;
