import { FC, useEffect, useState } from 'react';
import { IconCheck } from '@arco-design/web-react/icon';
import './index.scss';
export const CommonItemUI: FC<{
  clist: {
    name: string;
    czlist: {
      id: number;
      icon: JSX.Element;
      text: string;
      time?: string;
    }[];
  }[];
  needChangeIcon?: boolean;
  // handleSelectedLine?: (selectedLine:number)=>void;
}> = ({ clist, needChangeIcon }) => {
  const [selectedLine, setSelectedLine] = useState<number | null>(null);
  const handleClick = (id: number) => {
    console.log(id, selectedLine);
    setSelectedLine(id === selectedLine ? null : id);
    // console.log(selectedLine);
  };
  useEffect(() => {
    console.log('当前选中库', selectedLine);
    // handleSelectedLine && handleSelectedLine(selectedLine as number)
  }, [selectedLine]);
  return (
    <>
      {clist.map((item) => (
        <>
          <div className="toptitle" key={item.name}>
            {item.name}
          </div>
          {item.czlist.map((items) => (
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
              }}
              className={`line ${items.id === selectedLine ? 'active' : ''}`}
              key={items.id}
              onClick={() => handleClick(items.id)}
            >
              <div style={{ display: 'flex', alignItems: 'center' }}>
                {items.id === selectedLine && needChangeIcon ? (
                  <IconCheck />
                ) : (
                  items.icon
                )}{' '}
                {items.text}
              </div>
              {items.time && <span>{items.time}</span>}
            </div>
          ))}
        </>
      ))}
    </>
  );
};

export const isAcceptFile = (file: File, accept: string) => {
  if (accept && file) {
    const accepts = Array.isArray(accept)
      ? accept
      : accept
          .split(',')
          .map((x) => x.trim())
          .filter((x) => x);
    const fileExtension =
      file.name.indexOf('.') > -1 ? file.name.split('.').pop() : '';
    return accepts.some((type) => {
      const text = type && type.toLowerCase();
      const fileType = (file.type || '').toLowerCase();
      if (text === fileType) {
        // 类似excel文件这种
        // 比如application/vnd.ms-excel和application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
        // 本身就带有.字符的，不能走下面的.jpg等文件扩展名判断处理
        // 所以优先对比input的accept类型和文件对象的type值
        return true;
      }
      if (new RegExp('/*').test(text)) {
        // image/* 这种通配的形式处理
        const regExp = new RegExp('/.*$');
        return fileType.replace(regExp, '') === text.replace(regExp, '');
      }
      if (new RegExp('..*').test(text)) {
        // .jpg 等后缀名
        return text === `.${fileExtension && fileExtension.toLowerCase()}`;
      }
      return false;
    });
  }
  return !!file;
};
