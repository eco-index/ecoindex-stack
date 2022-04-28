import React from "react"
import { EuiLoadingSpinner } from "@elastic/eui"
import { useToasts } from "../../hooks/ui/useToasts" 
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
  const { addToast } = useToasts()
  const isAuthed = isAuthenticated && Boolean(user?.email)
  React.useEffect(() => {
    if (userLoaded && !isAuthed) {
      addToast({
        id: `auth-toast-redirect`,
        title: redirectTitle,
        color: "warning",
        iconType: "alert",
        toastLifeTimeMs: 15000,
        text: redirectMessage,
      })
    }
  }, [userLoaded, isAuthed, addToast, redirectTitle, redirectMessage])

  if (!userLoaded) return <EuiLoadingSpinner size="xl" />

  if (!isAuthed) {
    return (
      <>
        <LoginPage />
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
