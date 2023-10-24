import { css } from '@emotion/css';
import { Input, Button, Avatar } from '@arco-design/web-react';
// import { Avatar } from "@arco-design/web-react/icon";
const TextArea = Input.TextArea;

const CommitForm = (props: {controllButtonDisabled?:boolean}) => {
  const {controllButtonDisabled} = props
  return (
    <div
      className={css`
        /* position: absolute; */
        left: 300px;
        width: 280px;
        /* box-sizing: border-box; */
        display: flex;
        padding: 16px 12px;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        align-self: stretch;
        border-radius: 0px 0px 8px 8px;
        border-top: 1px solid var(--color-border-1, #f2f3f5);
      `}
    >
      <div
        className={css`
          display: flex;
          justify-content: center;
          align-items: flex-start;
          gap: 10px;
          align-self: stretch;
        `}
      >
        <Avatar size={32}>Arco</Avatar>
        <div
          className={css`
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            flex: 1 0 0;
            border-radius: 2px;
          `}
        >
          <Input
            style={{ width: 214 }}
            allowClear
            placeholder="Please Enter something"
          />
        </div>
      </div>

      <div
        className={css`
          display: flex;
          flex-direction: column;
          align-items: flex-start;
          align-self: stretch;
        `}
      >
        <TextArea
          placeholder="Please enter ..."
          style={{
            minHeight: 64,
            width: 256,
            border: '1px solid var(--color-border-2, #e5e6eb)',
            borderRadius: '2px',
          }}
        />
      </div>

      <div
        className={css`
          display: flex;
          padding: 7px 0px;
          /* justify-content: center; */
          /* align-items: center; */
          gap: 8px;
          align-self: stretch;
        `}
      >
        <Button
          type="primary"
          disabled={controllButtonDisabled}
          className={css`
            border-radius: 6px;
            border: 1px solid var(--primary-1, #e8f3ff);
            background: var(--btn-brand-dis, #94bfff);
            width: 256px;
          `}
        >
          Commit to Master
        </Button>
      </div>
    </div>
  );
};
export { CommitForm };
