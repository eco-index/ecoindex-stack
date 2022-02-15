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
  UserManagementPage
} from "../../components"
export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/frontend" element={<ProtectedRouteLanding component={LandingPage}/>} />
          <Route path="/frontend/login" element={<LoginPage />} />
          <Route path="/frontend/registration" element={<RegistrationPage />} />
          <Route path="/frontend/*" element={<NotFoundPage />} />
          <Route path="/frontend/retrievedata" element={<ProtectedRoute component ={RetrieveDataPage}/>} />
          <Route path="/frontend/helppage" element={<HelpPage/>} />
          <Route path="/frontend/usermanagement" element={<ProtectedRoute component = {UserManagementPage}/>} />
          <Route path="/frontend/resetpassword" element = {<ResetPasswordPage/>} />
          <Route path="/frontend/forgotpassword" element = {<ForgotPasswordPage/>} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
