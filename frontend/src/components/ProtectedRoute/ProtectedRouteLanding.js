import React from "react"
import { connect } from "react-redux"
import { useNavigate } from "react-router-dom"

function ProtectedRouteLanding({ user, userLoaded, isAuthenticated, component: Component, ...props }) {
  const isAuthed = isAuthenticated && Boolean(user?.email)
  const navigate = useNavigate()
  const {REACT_APP_PUBLIC_URL} = process.env
  if (!isAuthed){
    navigate({REACT_APP_PUBLIC_URL} +"/login")
  }
  return <Component {...props} />
}
export default connect((state) => ({
  user: state.auth.user,
  isAuthenticated: state.auth.isAuthenticated,
  userLoaded: state.auth.userLoadedß
}))(ProtectedRouteLanding)