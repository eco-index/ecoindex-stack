import initialState from "./initialState"
export const ADD_TOAST = "@@ui/ADD_TOAST"
export const REMOVE_TOAST = "@@ui/REMOVE_TOAST"
export default function uiReducer(state = initialState.ui, action = {}) {
  switch (action.type) {
    case ADD_TOAST:
      return {
        ...state,
        toastList: [...state.toastList, action.toast],
      }
    case REMOVE_TOAST:
      return {
        ...state,
        toastList: state.toastList.filter((toast) => toast.id !== action.toastId),
      }
    default:
      return state
  }
}
export const Actions = {}
Actions.addToast = (toast) => {
  return (dispatch, getState) => {
    const { ui } = getState()
    const toastIds = ui.toastList.map((toast) => toast.id)
    if (toastIds.indexOf(toast.id) === -1) {
      dispatch({ type: ADD_TOAST, toast })
    }
  }
}
Actions.removeToast = (toast) => {
  return dispatch => {
    dispatch({ type: REMOVE_TOAST, toastId: toast.id })
  }
}
