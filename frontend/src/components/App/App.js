import React from "react"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import {
  HelpPage,
  LandingPage,
  Layout,
  LoginPage,
  NotFoundPage,
  ProtectedRoute,  
  ProtectedRouteLanding,
  RegistrationPage,
  RetrieveDataPage
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
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
