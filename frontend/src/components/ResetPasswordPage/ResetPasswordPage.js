import React from "react"
import {
  EuiPage,
  EuiPageBody,
  EuiPageContent,
  EuiPageContentBody,
  EuiPageHeader,
  EuiPageHeaderSection,
} from "@elastic/eui"
import { ResetPasswordForm} from "../../components"
import styled from "styled-components"
const StyledEuiPage = styled(EuiPage)`
  flex: 1;
`
const StyledEuiPageHeader = styled(EuiPageHeader)`
  display: flex;
  justify-content: center;
  align-items: center;
`
const ResetPasswordTitle = styled.h1`
  font-size: 3rem;
  margin: 2rem 0;
`
export default function ResetPasswordPage() {
  return (
    <StyledEuiPage>
      <EuiPageBody component="section">
        <StyledEuiPageHeader>
          <EuiPageHeaderSection>
            <ResetPasswordTitle>Reset Password</ResetPasswordTitle>
          </EuiPageHeaderSection>
        </StyledEuiPageHeader>
        <EuiPageContent verticalPosition="center" horizontalPosition="center">
          <EuiPageContentBody>
            <ResetPasswordForm/>
          </EuiPageContentBody>
        </EuiPageContent>
      </EuiPageBody>
    </StyledEuiPage>
  )
}
