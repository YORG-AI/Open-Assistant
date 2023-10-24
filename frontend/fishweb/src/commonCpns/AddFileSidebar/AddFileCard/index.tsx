import { Tag } from '@arco-design/web-react';
import React, { FC, ReactNode, useState } from 'react';
import './index.scss';
import {
  IconClose,
  IconEye,
  IconEyeInvisible,
  IconFile,
} from '@arco-design/web-react/icon';
interface AddFileCardProps {
  cardTop: string;
  lines: number;
  children: ReactNode;
}
const AddFileCard: FC<AddFileCardProps> = ({ cardTop, lines, children }) => {
  const [isShowTip, setIsShowTip] = useState(true);
  return (
    <div className="addfileCard">
      <div className="cardTop">{cardTop}</div>
      <div className="cardBtm">
        <div className="tagboxleft">
          <Tag>
            <IconFile />2 ranges
          </Tag>
          {isShowTip ? <text className="linestyle">{lines} lines</text> : ''}
        </div>
        <div className="tagboxright">
          {isShowTip ? (
            <>
              <IconEye
                onClick={() => {
                  setIsShowTip(false);
                }}
              />
              {children}
            </>
          ) : (
            <IconEyeInvisible
              onClick={() => {
                setIsShowTip(true);
              }}
            />
          )}
        </div>
      </div>
    </div>
  );
};
export { AddFileCard };
