import { Upload } from "@arco-design/web-react";
import { IconPlus } from "@arco-design/web-react/icon";

export const DragPart = () => {
  return (
    <div>
      <div>or, scan a folder (.git folder)</div>
      <Upload
        action="/"
        onChange={(fileList, file) => {
          console.log(fileList, file);
        }}
        style={{
          width: '380px',
          height: '148px',
          padding: '10px 0',
        }}
      >
        <div className="trigger">
          <IconPlus style={{ marginBottom: '24px' }} />
          <div>Click or drag your folder here</div>
          <div style={{ color: '#C9CDD4' }}>
            Only directories with a .git folder can be uploaded.
          </div>
        </div>
      </Upload>
    </div>
  );
};
