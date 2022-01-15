import { combineReducers } from "redux"
import authReducer from "./auth"
import occurrenceReducer from "./occurrence"
import uiReducer from "./ui"
const rootReducer = combineReducers({
  auth: authReducer,
  occurrences: occurrenceReducer,
  ui: uiReducer,
  // other reducers will go here later
})
export default rootReducer
