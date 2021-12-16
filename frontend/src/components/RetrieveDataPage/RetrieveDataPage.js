import React from "react"
import {
  EuiPage,
  EuiPageBody,
  EuiPageContent,
  EuiPageContentBody,
  EuiPageHeader,
  EuiPageHeaderSection,
} from "@elastic/eui"
import { RetrieveDataForm } from "../../components"
import styled from "styled-components"
const StyledEuiPage = styled(EuiPage)`
  flex: 1;
`
const StyledEuiPageHeader = styled(EuiPageHeader)`
  display: flex;
  justify-content: center;
  align-items: center;
`
const RetrieveDataTitle = styled.h1`
  font-size: 3rem;
  margin: 2rem 0;
`
export default function RetrieveDataPage() {
  return (
    <StyledEuiPage>
      <EuiPageBody component="section">
        <StyledEuiPageHeader>
          <EuiPageHeaderSection>
            <RetrieveDataTitle>Retrieve Data Form</RetrieveDataTitle>
          </EuiPageHeaderSection>
        </StyledEuiPageHeader>
        <EuiPageContent verticalPosition="center" horizontalPosition="center">
          <EuiPageContentBody>
            <RetrieveDataForm />
          </EuiPageContentBody>
        </EuiPageContent>
      </EuiPageBody>
    </StyledEuiPage>
  )
}
