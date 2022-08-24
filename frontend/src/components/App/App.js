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
          <Route path="/frontendv1" element={<ProtectedRouteLanding component={LandingPage}/>} />
          <Route path="/frontendv1/login" element={<LoginPage />} />
          <Route path="/frontendv1/registration" element={<RegistrationPage />} />
          <Route path="/frontendv1/*" element={<NotFoundPage />} />
          <Route path="/frontendv1/retrievedata" element={<ProtectedRoute component ={RetrieveDataPage}/>} />
          <Route path="/frontendv1/retrievemcidata" element={<ProtectedRoute component = {RetrieveMCIDataPage}/>} />
          <Route path="/frontendv1/helppage" element={<HelpPage/>} />
          <Route path="/frontendv1/usermanagement" element={<ProtectedRoute component = {UserManagementPage}/>} />
          <Route path="/frontendv1/resetpassword" element = {<ResetPasswordPage/>} />
          <Route path="/frontendv1/forgotpassword" element = {<ForgotPasswordPage/>} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
