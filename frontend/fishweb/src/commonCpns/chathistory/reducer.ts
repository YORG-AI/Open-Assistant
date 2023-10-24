import { useReducer } from 'react';

const initialState = {
  isShrink: true,
  // 其他可能的状态
};

function chatReducer(state: any, action: any) {
  switch (action.type) {
    case 'TOGGLE_SHRINK':
      return { ...state, isShrink: !state.isShrink };
    // 处理其他操作
    default:
      return state;
  }
}

export function useChatReducer() {
  return useReducer(chatReducer, initialState);
}
