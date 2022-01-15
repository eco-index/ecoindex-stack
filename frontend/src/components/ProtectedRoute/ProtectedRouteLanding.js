import React from "react"
import { connect } from "react-redux"
import { useNavigate } from "react-router-dom"

function ProtectedRouteLanding({ user, userLoaded, isAuthenticated, component: Component, ...props }) {
  const isAuthed = isAuthenticated && Boolean(user?.email)
  const navigate = useNavigate()
  if (!isAuthed){
    navigate("/frontend/login")
  }
  return <Component {...props} />
}
export default connect((state) => ({
  user: state.auth.user,
  isAuthenticated: state.auth.isAuthenticated,
  userLoaded: state.auth.userLoadedß
}))(ProtectedRouteLanding)