import React from "react"
import {
  EuiPage,
  EuiPageBody,
  EuiPageContent,
  EuiPageContentBody,
  EuiPageHeader,
  EuiPageHeaderSection,
} from "@elastic/eui"
import { RegistrationForm } from "../../components"
import styled from "styled-components"
const StyledEuiPage = styled(EuiPage)`
  flex: 1;
`
const StyledEuiPageHeader = styled(EuiPageHeader)`
  display: flex;
  justify-content: center;
  align-items: center;
`
const RegistrationTitle = styled.h1`
  font-size: 3rem;
  margin: 2rem 0;
`
export default function RegistrationPage() {
  return (
    <StyledEuiPage>
      <EuiPageBody component="section">
        <StyledEuiPageHeader>
          <EuiPageHeaderSection>
            <RegistrationTitle>Sign Up</RegistrationTitle>
          </EuiPageHeaderSection>
        </StyledEuiPageHeader>
        <EuiPageContent verticalPosition="center" horizontalPosition="center">
          <EuiPageContentBody>
            <RegistrationForm />
          </EuiPageContentBody>
        </EuiPageContent>
      </EuiPageBody>
    </StyledEuiPage>
  )
}
