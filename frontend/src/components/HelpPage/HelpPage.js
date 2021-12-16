import React from "react"
import {
  EuiPage,
  EuiPageBody,
  EuiFlexGroup,
  EuiFlexItem
} from "@elastic/eui"
import styled from "styled-components"
const StyledEuiPage = styled(EuiPage)`
  flex: 1;
  padding-bottom: 5rem;
`
const LandingTitle = styled.h1`
  font-size: 3rem;
  margin: 2rem 0;
`

export default function LandingPage() {
  return (
    <StyledEuiPage>
      <EuiPageBody component="section">
        <EuiFlexGroup direction="column" alignItems="center">
          <EuiFlexItem>
            <LandingTitle>FAQ</LandingTitle>
          </EuiFlexItem>
        </EuiFlexGroup>
      </EuiPageBody>
    </StyledEuiPage>
  )
}
