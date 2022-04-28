import { configureStore, getDefaultMiddleware } from "@reduxjs/toolkit"
import rootReducer from "./rootReducer"
import { Actions as authActions } from "./auth"  

export default function configureReduxStore() {
  const store = configureStore({
    reducer: rootReducer,
    middleware: [...getDefaultMiddleware()],
  })

  store.dispatch(authActions.fetchUserFromToken())  
  
  // enable hot reloading in development
  if (process.env.NODE_ENV !== "production" && module.hot) {
    module.hot.accept("./rootReducer", () => store.replaceReducer(rootReducer))
  }
  
  return store
}