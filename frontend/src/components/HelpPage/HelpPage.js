import React from "react"
import {
  EuiPage,
  EuiPageBody,
  EuiPageHeader,
  EuiPageContent,
  EuiPageHeaderSection,
  EuiPageContentBody,
  EuiText,
  EuiSpacer
} from "@elastic/eui"
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
font-size: 3rem;
margin: 2rem 0;
`
const FAQTitle = styled.h3`
font-size: 1.2rem;
font-weight: bold;
`

export default function LandingPage() {
  return (
    <StyledEuiPage>
      <EuiPageBody component="section">
        <StyledEuiPageHeader>
          <EuiPageHeaderSection>
            <LandingTitle>FAQ</LandingTitle>
          </EuiPageHeaderSection>
        </StyledEuiPageHeader>
        <EuiPageContent verticalPosition="top" horizontalPosition="center">
          <EuiPageContentBody>
            <FAQTitle>Creating an Account</FAQTitle>
            <EuiSpacer size="s"/>
            <EuiText>
              <p>
                Accounts can be created <a href="/frontend/registration">here</a><br />
                Please note that accounts will need to be approved before data retrieval is possible.<br />
                To request approval, please send an email to konnyb@waikato.ac.nz 
              </p>
            </EuiText>
            <EuiSpacer size="l"/>
            <FAQTitle>Retrieving Data</FAQTitle>
              <EuiSpacer size="s"/>
              <EuiText>
                <p>
                  Classification Level and name is based on the GBIF taxonomy as found <a href="https://www.gbif.org/dataset/d7dddbf4-2cf0-4f39-9b2a-bb099caae36c" target="_blank" rel="noreferrer">here</a><br />
                  Regional boundaries are based on Regional Council boundaries provided by <a href = "https://datafinder.stats.govt.nz/layer/104254-regional-council-2020-generalised">Stats NZ</a><br />
                  Iwi boundaries are as provided by <a href = "https://hub.arcgis.com/datasets/TPK::layer-iwi-areasofinterest/explore?location=-40.038265%2C-8.471169%2C6.24">Te Puna Kōkiri</a><br />
                  MCI data has been retrieved from <a href = "https://www.lawa.org.nz/download-data/">LAWA</a> categorised by river catchments
                </p>
              </EuiText>
            <EuiSpacer size = "l"/>
            <FAQTitle>Data License</FAQTitle>
            <EuiSpacer size = "s"/>
            <EuiText>
              <p>
                Data has been retrieved from the following datasets under creative commons licensing:
                <ul>
                  <li>eBird Observation Dataset</li>
                  <li>NZ National Vegetation Survey occurrence data (Landcare Research)</li>
                  <li>iNaturalist Research-grade Observations</li>
                  <li>Macrophyte Lake Data (NIWA)</li>
                  <li>NZ Biodiversity Monitoring Network</li>
                  <li>NZ Freshwater Fish Database (NIWA)</li>
                  <li>River Ecology Monitoring 2006-2020 (LAWA)</li>
                </ul>
              </p>
            </EuiText>
          </EuiPageContentBody>
        </EuiPageContent>
      </EuiPageBody>
    </StyledEuiPage>
  )
}
