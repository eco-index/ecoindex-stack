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
          <Route path="/frontend/v2" element={<ProtectedRouteLanding component={LandingPage}/>} />
          <Route path="/frontend/v2/login" element={<LoginPage />} />
          <Route path="/frontend/v2/registration" element={<RegistrationPage />} />
          <Route path="/frontend/v2/*" element={<NotFoundPage />} />
          <Route path="/frontend/v2/retrievedata" element={<ProtectedRoute component ={RetrieveDataPage}/>} />
          <Route path="/frontend/v2/retrievemcidata" element={<ProtectedRoute component = {RetrieveMCIDataPage}/>} />
          <Route path="/frontend/v2/helppage" element={<HelpPage/>} />
          <Route path="/frontend/v2/usermanagement" element={<ProtectedRoute component = {UserManagementPage}/>} />
          <Route path="/frontend/v2/resetpassword" element = {<ResetPasswordPage/>} />
          <Route path="/frontend/v2/forgotpassword" element = {<ForgotPasswordPage/>} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
