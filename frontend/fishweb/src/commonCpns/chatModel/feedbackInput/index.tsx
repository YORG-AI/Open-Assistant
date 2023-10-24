import './index.scss';
import { Input } from '@arco-design/web-react';
const InputTextArea = Input.TextArea;

const FeedbackInput = () => {
  return (
    <div className="feedbackinput">
      <div className="title">Please help us improve !</div>
      <InputTextArea
        style={{ height: 96 }}
        autoSize={false}
        placeholder="What was the issue with this answer? 
How could it be improved?"
      ></InputTextArea>
      <div className="footer">
        <div className="footer_left">Choose Again</div>
        <div className="footer_right">Skip</div>
      </div>
    </div>
  );
};
export { FeedbackInput };
