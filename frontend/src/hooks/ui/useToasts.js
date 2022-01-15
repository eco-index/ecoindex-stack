import { useDispatch, useSelector, shallowEqual } from "react-redux"
import { Actions as uiActions } from "../../redux/ui"
export const useToasts = () => {
  const dispatch = useDispatch()
  const toasts = useSelector((state) => state.ui.toastList, shallowEqual)
  const addToast = (toast) => dispatch(uiActions.addToast(toast))
  const removeToast = (toastId) => dispatch(uiActions.removeToast(toastId))
  return { toasts, addToast, removeToast }
}