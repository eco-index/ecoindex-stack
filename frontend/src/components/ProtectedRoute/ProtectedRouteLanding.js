import React from "react"
import { LoginPage } from "../../components"
import { connect } from "react-redux"
function ProtectedRouteLanding({ user, userLoaded, isAuthenticated, component: Component, ...props }) {
  const isAuthed = isAuthenticated && Boolean(user?.email)
  if (!isAuthed) return <LoginPage />
  return <Component {...props} />
}
export default connect((state) => ({
  user: state.auth.user,
  isAuthenticated: state.auth.isAuthenticated,
  userLoaded: state.auth.userLoaded
}))(ProtectedRouteLanding)