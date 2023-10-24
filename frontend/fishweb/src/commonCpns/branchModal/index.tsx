import { Button, Form, Input, Modal, Select } from '@arco-design/web-react';
import React, { useRef } from 'react';
import { css } from '@emotion/css';
import './index.scss';
const FormItem = Form.Item;
const Option = Select.Option;
const options = [
  {
    id: 1,
    name: 'Master(defalut)',
  },
  {
    id: 2,
    name: 'dev',
  },
];
const BranchModal: React.FC<{
  visible: boolean;
  handleClickCloseModal: () => void;
  handleClickSubmitModal: (formData: any) => void;
}> = ({ visible, handleClickCloseModal, handleClickSubmitModal }) => {
  const formRef = useRef<any>();
  const handleCancelForm = () => {
    handleClickCloseModal();
    formRef.current.resetFields()
  };
  const [form] = Form.useForm();
  return (
    <Modal
      className="branch_modal_wrapper"
      title="Create a Branch"
      visible={visible}
      footer={null}
      onCancel={handleCancelForm}
    >
      <Form
        layout="vertical"
        className={css`
          width: 100%;
        `}
        form={form}
        ref={formRef}
        initialValues={{ branch: 1 }}
        autoComplete="off"
        onValuesChange={(v, vs) => {
          console.log(v, vs);
        }}
        onSubmit={(v) => {
          // console.log(v);
          handleClickSubmitModal(v);
          formRef.current.resetFields()
        }}
        validateMessages={{
          required: (_, { label }) =>
            ` ${label.substr(0, label.length - 1)} is required`,
        }}
      >
        <FormItem
          label="Create a branch based on this existing branch:"
          field="branch"
          className={css`
            padding: 0 24px;
            width: 100%;
            box-sizing: border-box;
          `}
          rules={[{ required: true }]}
        >
          <Select placeholder="Please select">
            {options.map((option, index) => (
              <Option key={option.id} value={option.id}>
                {option.name}
              </Option>
            ))}
          </Select>
        </FormItem>
        <FormItem
          label="Name of the new branch:"
          field="branchName"
          className={css`
            padding: 0 24px;
            width: 100%;
            box-sizing: border-box;
          `}
          rules={[{ required: true }]}
          style={{ marginBottom: 0 }}
        >
          <Input
            allowClear
            style={{ borderRadius: 8 }}
            placeholder="Please enter a name"
          ></Input>
        </FormItem>
        <FormItem
          className={css`
            display: flex;
            justify-content: flex-end;
            border-top: 1px solid var(--color-neutral-3);
            margin-top: 12px;
            padding-right: 12px;
            width: 100%;
            margin-bottom: 12px;
            box-sizing: border-box;
          `}
        >
          <Button
            className={css`
              border-radius: 8px;
              margin-top: 11px;
            `}
            onClick={handleCancelForm}
          >
            Cancel
          </Button>
          <Button
            type="primary"
            htmlType="submit"
            className={css`
              margin-left: 8px;
              border-radius: 8px;
              margin-top: 11px;
            `}
          >
            Create
          </Button>
        </FormItem>
      </Form>
    </Modal>
  );
};
export default BranchModal;
