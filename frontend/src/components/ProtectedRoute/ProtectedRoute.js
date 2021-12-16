import React from "react"
import { EuiGlobalToastList, EuiLoadingSpinner } from "@elastic/eui"
import { LoginPage } from "../../components"
import { connect } from "react-redux"
function ProtectedRoute({
  user,
  userLoaded,
  isAuthenticated,
  component: Component,
  redirectTitle = `Access Denied`,
  redirectMessage = `Authenticated users only. Login here or create a new account to view that page.`,
  ...props
}) {
  const [toasts, setToasts] = React.useState([
    {
      id: "auth-redirect-toast",
      title: redirectTitle,
      color: "warning",
      iconType: "alert",
      toastLifeTimeMs: 15000,
      text: <p>{redirectMessage}</p>
    }
  ])
  if (!userLoaded) return <EuiLoadingSpinner size="xl" />
  const isAuthed = isAuthenticated && Boolean(user?.email)
  if (!isAuthed) {
    return (
      <>
        <LoginPage />
        <EuiGlobalToastList
          toasts={toasts}
          dismissToast={() => setToasts([])}
          toastLifeTimeMs={15000}
          side="right"
          className="auth-toast-list"
        />
      </>
    )
  }
  return <Component {...props} />
}
export default connect((state) => ({
  user: state.auth.user,
  isAuthenticated: state.auth.isAuthenticated,
  userLoaded: state.auth.userLoaded
}))(ProtectedRoute)
