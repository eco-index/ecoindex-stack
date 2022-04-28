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
          <Route path="/frontendv2" element={<ProtectedRouteLanding component={LandingPage}/>} />
          <Route path="/frontendv2/login" element={<LoginPage />} />
          <Route path="/frontendv2/registration" element={<RegistrationPage />} />
          <Route path="/frontendv2/*" element={<NotFoundPage />} />
          <Route path="/frontendv2/retrievedata" element={<ProtectedRoute component ={RetrieveDataPage}/>} />
          <Route path="/frontendv2/retrievemcidata" element={<ProtectedRoute component = {RetrieveMCIDataPage}/>} />
          <Route path="/frontendv2/helppage" element={<HelpPage/>} />
          <Route path="/frontendv2/usermanagement" element={<ProtectedRoute component = {UserManagementPage}/>} />
          <Route path="/frontendv2/resetpassword" element = {<ResetPasswordPage/>} />
          <Route path="/frontendv2/forgotpassword" element = {<ForgotPasswordPage/>} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
