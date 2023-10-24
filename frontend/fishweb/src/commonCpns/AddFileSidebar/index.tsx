import { useState, useRef } from 'react';
import { Button } from '@arco-design/web-react';
import './index.scss';
import { IconPlus, IconClose } from '@arco-design/web-react/icon';
import { AddFileCard } from './AddFileCard';

const AddFileSidebar = () => {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [fileContents, setFileContents] = useState<string[]>([]); // 用于存储文件内容
  const [fileLineCounts, setFileLineCounts] = useState<number[]>([]); // 用于存储文件行数
  const fileInputRef = useRef<HTMLInputElement>(null);
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log('first');
    const newFiles = e.target.files;
    if (newFiles) {
      // 检查文件类型，这里假设只允许代码类型文件
      // console.log(file.type);
      const validFiles = Array.from(newFiles);
      setSelectedFiles((prevFiles) => [...prevFiles, ...validFiles]);
      // if (
      //   file.type === 'text/javascript' ||
      //   file.type === 'text/x-python-script'
      // ) {

      // } else {
      //   alert('只能上传代码类型文件（例如.js或.py文件）');
      // }

      // 使用FileReader读取文件内容并存储
      const promises = validFiles.map((file) => {
        return new Promise<string>((resolve, reject) => {
          const reader = new FileReader();
          reader.onload = (event) => {
            if (event.target) {
              resolve(event.target.result as string);
            } else {
              reject(new Error('无法读取文件内容'));
            }
          };
          reader.onerror = (error) => {
            reject(error);
          };
          reader.readAsText(file);
        });
      });
      // 批量处理文件读取
      Promise.all(promises)
        .then((contents) => {
          setFileContents((prevContents) => [...prevContents, ...contents]);
          // 计算每个文件的行数并存储
          const lineCounts = contents.map((content) => {
            const lines = content.split('\n');
            return lines.length;
          });
          setFileLineCounts((prevLineCounts) => [
            ...prevLineCounts,
            ...lineCounts,
          ]);
        })
        .catch((error) => {
          console.error('文件读取错误:', error);
        });
    }
  };

  const handleChooseFile = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };
  const handleRemoveFile = (indexToRemove: number) => {
    setSelectedFiles((prevFiles) =>
      prevFiles.filter((_, index) => index !== indexToRemove)
    );
    setFileContents((prevContents) =>
      prevContents.filter((_, index) => index !== indexToRemove)
    );
    setFileLineCounts((prevLineCounts) =>
      prevLineCounts.filter((_, index) => index !== indexToRemove)
    );
  };
  return (
    <div className="addfileSidebar">
      <div
        className="wrapper"
        style={{
          justifyContent: `${selectedFiles.length > 0 ? 'flex-start' : ''}`,
        }}
      >
        {/* {selectedFiles.map((file, index) => (
          <AddFileCard
            key={index}
            cardTop={file.name}
            lines={fileLineCounts[index]}
          />
        ))} */}
        {selectedFiles.length > 0 ? (
          // <div className="selected-file">
          //   Selected Files:
          //   {selectedFiles.map((file, index) => (
          //     <li key={index}>
          //       {file.name} - {file.type}
          //       <div>Line Count: {fileLineCounts[index]}</div>
          //       {/* <pre>{fileContents[index]}</pre> */}
          //     </li>
          //   ))}
          // </div>
          selectedFiles.map((file, index) => (
            <AddFileCard
              key={index}
              cardTop={file.name}
              lines={fileLineCounts[index]}
            >
              <IconClose onClick={() => handleRemoveFile(index)} />
            </AddFileCard>
          ))
        ) : (
          <div className="state-empty">No Files are added yet.</div>
        )}
        <div>
          <label className="file-upload-button">
            <input
              type="file"
              ref={fileInputRef}
              accept=".js,.py"
              style={{ display: 'none' }}
              onChange={handleFileChange}
              multiple // 允许多选文件
            />
            <Button type="secondary" onClick={handleChooseFile}>
              <IconPlus />
              Add Files
            </Button>
          </label>
        </div>
      </div>
    </div>
  );
};
export { AddFileSidebar };
