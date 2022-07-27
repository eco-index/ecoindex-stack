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
          <Route path="/frontend/v1" element={<ProtectedRouteLanding component={LandingPage}/>} />
          <Route path="/frontend/v1/login" element={<LoginPage />} />
          <Route path="/frontend/v1/registration" element={<RegistrationPage />} />
          <Route path="/frontend/v1/*" element={<NotFoundPage />} />
          <Route path="/frontend/v1/retrievedata" element={<ProtectedRoute component ={RetrieveDataPage}/>} />
          <Route path="/frontend/v1/retrievemcidata" element={<ProtectedRoute component = {RetrieveMCIDataPage}/>} />
          <Route path="/frontend/v1/helppage" element={<HelpPage/>} />
          <Route path="/frontend/v1/usermanagement" element={<ProtectedRoute component = {UserManagementPage}/>} />
          <Route path="/frontend/v1/resetpassword" element = {<ResetPasswordPage/>} />
          <Route path="/frontend/v1/forgotpassword" element = {<ForgotPasswordPage/>} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
