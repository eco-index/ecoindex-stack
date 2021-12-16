import React from "react"
import {
  EuiPage,
  EuiPageBody,
  EuiPageContent,
  EuiPageContentBody,
  EuiPageHeader,
  EuiPageHeaderSection
} from "@elastic/eui"
import { LoginForm } from "../../components"
import styled from "styled-components"
const StyledEuiPage = styled(EuiPage)`
  flex: 1;
`
const StyledEuiPageHeader = styled(EuiPageHeader)`
  display: flex;
  justify-content: center;
  align-items: center;
`
const LandingTitle = styled.h1`
  font-size: 3.5rem;
  margin: 2rem 0;
`
export default function LoginPage() {
  return (
    <StyledEuiPage>
      <EuiPageBody component="section">
        <StyledEuiPageHeader>
          <EuiPageHeaderSection>
            <LandingTitle>Eco-index Datastore</LandingTitle>
          </EuiPageHeaderSection>
        </StyledEuiPageHeader>
        <EuiPageContent verticalPosition="center" horizontalPosition="center">
          <EuiPageContentBody>
            <LoginForm />
          </EuiPageContentBody>
        </EuiPageContent>
      </EuiPageBody>
    </StyledEuiPage>
  )
}