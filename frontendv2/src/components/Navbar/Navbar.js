import React from "react"
import { connect } from "react-redux"
import { useToasts } from "../../hooks/ui/useToasts" 
import { Actions as authActions } from "../../redux/auth"
import {
  EuiAvatar,
  EuiIcon,
  EuiHeader,
  EuiHeaderSection,
  EuiHeaderSectionItem,
  EuiHeaderSectionItemButton,
  EuiHeaderLinks,
  EuiHeaderLink,
} from "@elastic/eui"
import { Link, useNavigate } from "react-router-dom"
import loginIcon from "../../assets/img/loginIcon.svg"
import styled from "styled-components"

const LogoSection = styled(EuiHeaderLink)`
  padding: 0 2rem;
`


function Navbar({ user, logUserOut, isAuthenticated, ...props }) {
  const navigate = useNavigate()
  const { addToast } = useToasts()
  const handleLogout = () => {
    addToast({
      id: `auth-toast-loggedout`,
      title: `Logged Out Successfully`,
      color: "Success",
      iconType: "alert",
      toastLifeTimeMs: 15000,
    })
    navigate("/frontendv2/login")
    logUserOut()
  }
  
  const loginButton = () => {
    if (user?.email && isAuthenticated) {
      return (
        <EuiHeaderSectionItemButton onClick={() => { handleLogout();} }>
            <EuiAvatar size="l" color="#1E90FF" name="login" imageUrl={loginIcon}/>
        </EuiHeaderSectionItemButton>
      )
    }
    return (
      <EuiHeaderSectionItemButton>
          <Link to="/frontendv2/login">
            <EuiAvatar size="l" color="#1E90FF" name="login" imageUrl={loginIcon}/>
          </Link>
      </EuiHeaderSectionItemButton>
    )
  }

  return (
    <EuiHeader style={props.style || {}}>
      <EuiHeaderSection>
        <EuiHeaderSectionItem border="right">
          <LogoSection href="/frontendv2">
            <EuiIcon type="database" color="#1E90FF" size="l" /> Eco-index Datastore
          </LogoSection>
        </EuiHeaderSectionItem>
        <EuiHeaderSectionItem border="right">
          <EuiHeaderLinks aria-label="app navigation links">
            <EuiHeaderLink iconType="download" href="/frontendv2/retrievedata">
              Retrieve Occurrences
            </EuiHeaderLink>
            <EuiHeaderLink iconType="download" href="/frontendv2/retrievemcidata">
              Retrieve MCI Data
            </EuiHeaderLink>
            <EuiHeaderLink iconType="help" href="/frontendv2/helppage">
              Help
            </EuiHeaderLink>
            <EuiHeaderLink iconType="wrench" href="/frontendv2/usermanagement">
              User Management
            </EuiHeaderLink>
          </EuiHeaderLinks>
        </EuiHeaderSectionItem>
      </EuiHeaderSection>
      <EuiHeaderSection>
          {loginButton()}
      </EuiHeaderSection>
    </EuiHeader>
  )
}
export default connect((state) => ({ 
  user: state.auth.user, 
  isAuthenticated: state.auth.isAuthenticated 
}), {
  logUserOut: authActions.logUserOut
})(Navbar)
