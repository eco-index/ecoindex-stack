import { combineReducers } from "redux"
import authReducer from "./auth"
import mciReducer from "./mci"
import occurrenceReducer from "./occurrence"
import uiReducer from "./ui"
const rootReducer = combineReducers({
  auth: authReducer,
  occurrences: occurrenceReducer,
  ui: uiReducer,
  mci: mciReducer
  // other reducers will go here later
})
export default rootReducer
