
import React from "react"
import ReactDOM from "react-dom"
import { Provider } from "react-redux"  
import { App } from "./components"
import configureReduxStore from "./redux/store" 
const store = configureReduxStore()  
ReactDOM.render(
  <React.StrictMode>
    <Provider store={store}>  
      <App />
    </Provider>  
  </React.StrictMode>,
  document.getElementById("root")
)
