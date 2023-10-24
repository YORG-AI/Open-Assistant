import React, { useState } from 'react';
import './index.scss';

import { ChatHistory } from '../../commonCpns/chathistory/chathistory';

const ChatHistoryView: React.FC = () => {
  return (
    <div className="chatHistoryView">
      <ChatHistory />;
    </div>
  );
};

export { ChatHistoryView };
