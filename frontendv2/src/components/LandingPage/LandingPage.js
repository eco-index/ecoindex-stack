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
  font-size: 3.5rem;
  margin: 2rem 0;
`

export default function LandingPage() {
  return (
    <StyledEuiPage>
      <EuiPageBody component="section">
        <EuiFlexGroup direction="column" alignItems="center">
          <EuiFlexItem>
            <LandingTitle>Eco-index Datastore V2</LandingTitle>
          </EuiFlexItem>
        </EuiFlexGroup>
      </EuiPageBody>
    </StyledEuiPage>
  )
}
