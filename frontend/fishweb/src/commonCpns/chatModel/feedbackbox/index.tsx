import './index.scss';
import { Button } from '@arco-design/web-react';
import { IconThumbDown, IconThumbUp } from '@arco-design/web-react/icon';

const FeedbackBox = () => {
  return (
    <div className="feedback">
      <div className="content">
        <div className="text">How would you rate this response?</div>
        <div className="btn">
          <Button type="outline">
            <IconThumbUp />
            Good
          </Button>
          <Button type="outline" status="danger">
            <IconThumbDown />
            Bad
          </Button>
        </div>
      </div>
    </div>
  );
};
export { FeedbackBox };
