export const initialState = {
  branch: 'master',
};
export const branchReducer = (state: { branch: string; }, action: { type: string; branch: string }) => {
  switch (action.type) {
    case 'FORM_SUBMIT':
      return { ...state, branch: action.branch };
    default:
      return state;
  }
};
