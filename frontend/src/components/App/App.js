import React from "react"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import {
  ForgotPasswordPage,
  HelpPage,
  LandingPage,
  Layout,
  LoginPage,
  NotFoundPage,
  ProtectedRoute,  
  ProtectedRouteLanding,
  RegistrationPage,
  ResetPasswordPage,
  RetrieveDataPage,
  RetrieveMCIDataPage,
  UserManagementPage
} from "../../components"
export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          const { REACT_APP_PUBLIC_URL } = process.env;
          <Route path={REACT_APP_PUBLIC_URL} element={<ProtectedRouteLanding component={LandingPage}/>} />
          <Route path={REACT_APP_PUBLIC_URL + "/login"} element={<LoginPage />} />
          <Route path={REACT_APP_PUBLIC_URL + "/registration"} element={<RegistrationPage />} />
          <Route path={REACT_APP_PUBLIC_URL + "/*"} element={<NotFoundPage />} />
          <Route path={REACT_APP_PUBLIC_URL + "/retrievedata"} element={<ProtectedRoute component ={RetrieveDataPage}/>} />
          <Route path={REACT_APP_PUBLIC_URL + "/retrievemcidata"} element={<ProtectedRoute component = {RetrieveMCIDataPage}/>} />
          <Route path={REACT_APP_PUBLIC_URL + "/helppage"} element={<HelpPage/>} />
          <Route path={REACT_APP_PUBLIC_URL + "/usermanagement"} element={<ProtectedRoute component = {UserManagementPage}/>} />
          <Route path={REACT_APP_PUBLIC_URL + "/resetpassword"} element = {<ResetPasswordPage/>} />
          <Route path={REACT_APP_PUBLIC_URL + "/forgotpassword"} element = {<ForgotPasswordPage/>} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
