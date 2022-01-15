import React from "react"
import { Helmet } from "react-helmet"
import { Navbar } from "../../components"
import { EuiGlobalToastList } from "@elastic/eui"  
import { useToasts } from "../../hooks/ui/useToasts" 
import styled, { ThemeProvider } from "styled-components"
import euiVars from "@elastic/eui/dist/eui_theme_light.json"
import "@elastic/eui/dist/eui_theme_light.css"
import "../../assets/css/fonts.css"
import "../../assets/css/override.css"
const customTheme = {
  ...euiVars,
  euiTitleColor: "dodgerblue",
}
const StyledLayout = styled.div`
  width: 100%;
  max-width: 100vw;
  min-height: 100vh;
  background: rgb(224, 228, 234);
  display: flex;
  flex-direction: column;
`
const StyledMain = styled.main`
  min-height: calc(100vh - ${(props) => props.theme.euiHeaderHeight} - 1px);
  display: flex;
  flex-direction: column;
  & h1 {
    color: ${(props) => props.theme.euiTitleColor};
  }
`
export default function Layout({ children }) {
  const { toasts, removeToast } = useToasts()  

  return (
    <React.Fragment>
      <Helmet>
        <meta charSet="utf-8" />
        <title>Eco-index Datastore</title>
        <link rel="canonical" href="https://ecoindex-datastore.com" />
      </Helmet>
      <ThemeProvider theme={customTheme}>
        <StyledLayout>
          <Navbar />
          <StyledMain>{children}</StyledMain>
          <EuiGlobalToastList
            toasts={toasts}
            dismissToast={(toastId) => removeToast(toastId)}
            toastLifeTimeMs={15000}
            side="right"
            className="auth-toast-list"
          />
        </StyledLayout>
      </ThemeProvider>
    </React.Fragment>
  )
}