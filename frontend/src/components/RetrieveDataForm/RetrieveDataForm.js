import React from "react"
import { connect } from "react-redux"
import { Actions as occurrenceActions } from "../../redux/occurrence"
import {
  EuiButton,
  EuiFieldText,
  EuiForm,
  EuiFormRow,
  EuiSpacer,
  EuiSuperSelect,
  EuiDatePicker,
  EuiSplitPanel
} from "@elastic/eui"
import validation from "../../utils/validation"
import styled from "styled-components"
import { extractErrorMessages } from "../../utils/errors"

const RegistrationFormWrapper = styled.div`
  padding: 2rem;
`
function RetrieveDataForm({ occurrenceError, isLoading, requestData, retrieveData, data}) {
  const [form, setForm] = React.useState({
    classificationLevel: "",
    classificationName: "",
    year: "",
    startDate: "",
    endDate: "",
    locationType: "",
    locationName: ""
  })
  const [errors, setErrors] = React.useState({})
  const [hasSubmitted, setHasSubmitted] = React.useState(false) 
  const occurrenceErrorList = extractErrorMessages(occurrenceError) 
  
  const validateInput = (label, value) => {
    // grab validation function and run it on input if it exists
    // if it doesn't exists, just assume the input is valid
    const isValid = validation?.[label] ? validation?.[label]?.(value) : true
    // set an error if the validation function did NOT return true
    setErrors((errors) => ({ ...errors, [label]: !isValid }))
  }

  const handleInputChange = (label, value) => {
    validateInput(label, value)
    setForm((form) => ({ ...form, [label]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    // validate inputs before submitting
    Object.keys(form).forEach((label) => validateInput(label, form[label]))

    //if classificationName is selected but not a classification level
    if(form.classificationName && !form.classificationLevel){
      setErrors((errors) => ({ ...errors, form: `Please select a classification level.` }))
      return
    }
    //if classification level is selected but no classification name
    if(form.classificationLevel && !form.classificationName){
      form.classificationLevel = ""
    }
    if(!form.year){
      //if start date is selected but no end date, and vice versa
      if(form.startDate && !form.endDate){
        setErrors((errors) => ({ ...errors, form: `Please select an end date` }))
        return
      }
      if(form.endDate && !form.startDate){
        setErrors((errors) => ({ ...errors, form: `Please select a start date` }))
        return
      }
    }
    setHasSubmitted(true)

    const res = await requestData({
      classification_level: form.classificationLevel,
      classification_name: form.classificationName,
      year: form.year,
      startDate: form.startDate,
      endDate: form.endDate,
      location_name: form.locationName,
      location_type: form.locationType
    })
    if(res?.success) {
      const downloadID = data?.download_id
      //code for a popover with the link?
      const action = await retrieveData({download_id: downloadID}) 
      if(action?.success){
        const href = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = href
        link.setAttribute('download', 'download.csv') //or any other extension
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      }
    }
  }
  const getFormErrors = () => {
    const formErrors = []
    if (errors.form) {
      formErrors.push(errors.form)
    }
    if (hasSubmitted && occurrenceError.length) {
      return formErrors.concat(occurrenceErrorList)
    }
    return formErrors
  }

  

  return (
    <RegistrationFormWrapper>
      <EuiForm
        component="form"
        onSubmit={handleSubmit}
        // isInvalid={Boolean(getFormErrors().length)}
        // error={getFormErrors()}
      >
        <EuiFormRow
          label="Classification Level"
          isInvalid={Boolean(errors.email)}
        >
          <EuiSuperSelect
            options={[
              {
                value: 'phylum',
                inputDisplay: 'Phylum'
              },
              {
                value: 'kingdom',
                inputDisplay: 'Kingdom'
              },
              {
                value: 'class',
                inputDisplay: 'Class'
              },
              {
                value: 'order',
                inputDisplay: 'Order'
              },
              {
                value: 'family',
                inputDisplay: 'Family'
              },
              {
                value: 'genus',
                inputDisplay: 'Genus'
              },
              {
                value: 'species',
                inputDisplay: 'Species'
              }
            ]}
            valueOfSelected = {form.classificationLevel}
            onChange={(value) => handleInputChange("classificationLevel", value)}
            itemLayoutAlign="top"
            isInvalid={Boolean(errors.classificationLevel)}s
          />
        </EuiFormRow>
        <EuiFormRow
          label="Classification Name"
          helpText="Select a classification level and name to filter the data by."
        >
          <EuiFieldText
            value={form.classificationName}
            onChange={(e) => handleInputChange("classificationName", e.target.value)}
            isInvalid={Boolean(errors.classificationName)}
          />
        </EuiFormRow>
          <EuiFormRow
            label="Year"
            helpText="Enter either a year or a date range."
          >
            <EuiFieldText
              value={form.year}
              onChange={(e) => handleInputChange("year", e.target.value)}
              isInvalid={Boolean(errors.year)}
            />
          </EuiFormRow>
          <EuiFormRow
            label="Date Range"
            helpText="Enter either a year or a date range."
          >
            <EuiSplitPanel.Outer>
              <EuiSplitPanel.Inner>
                <EuiDatePicker
                  placeholder="Pick a start date"
                  value={form.startDate}
                  onChange={(e) => handleInputChange("startDate", e.target.value)}
                  isInvalid={Boolean(errors.startDate)}
                />
              </EuiSplitPanel.Inner>
              <EuiSplitPanel.Inner>
                <EuiDatePicker
                  placeholder="Pick a end date"
                  value={form.endDate}
                  onChange={(e) => handleInputChange("endDate", e.target.value)}
                  isInvalid={Boolean(errors.endDate)}
                />
              </EuiSplitPanel.Inner>
          </EuiSplitPanel.Outer>
        </EuiFormRow>
        <EuiFormRow label="Location Type"
          isInvalid={Boolean(errors.email)}
        >
          <EuiSuperSelect
            options={[
              {
                value: 'rohe',
                inputDisplay: 'Rohe'
              },
              {
                value: 'region',
                inputDisplay: 'Region'
              }
            ]}
            valueOfSelected = {form.locationType}
            onChange={(value) => handleInputChange("locationType", value)}
            itemLayoutAlign="top"
            isInvalid={Boolean(errors.classificationLevel)}s
          />
        </EuiFormRow>
        <EuiFormRow
          label="Location Name"
        >
              <EuiFieldText
                value={form.locationName}
                onChange={(e) => handleInputChange("locationName", e.target.value)}
                isInvalid={Boolean(errors.locationName)}
              />
        </EuiFormRow>
        <EuiSpacer />
        <EuiButton type="submit" isLoading={isLoading} fill>
          Submit
        </EuiButton>
      </EuiForm>
      <EuiSpacer size="xl" />
    </RegistrationFormWrapper>
  )
}

export default connect(state => ({
    occurenceError: state.occurrences.error,
    isLoading: state.occurrences.isLoading,
    data: state.occurrences.data,
  }),
  {
    requestData: occurrenceActions.requestData,
    retrieveData: occurrenceActions.retrieveData
  }
)(RetrieveDataForm)