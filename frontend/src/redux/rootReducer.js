import { combineReducers } from "redux"
import authReducer from "./auth"
import occurrenceReducer from "./occurrence"
const rootReducer = combineReducers({
  auth: authReducer,
  occurrences: occurrenceReducer
  // other reducers will go here later
})
export default rootReducer
