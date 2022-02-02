import React from "react"
import moment from "moment"
import { connect } from "react-redux"
import { useToasts } from "../../hooks/ui/useToasts" 
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

const RetrieveDataFormWrapper = styled.div`
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
  const { addToast } = useToasts()
  
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
      setErrors((errors) => ({ ...errors, form: `Please specify a classification name` }))
      return
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
      if(form.endDate < form.startDate){
        setErrors((errors) => ({ ...errors, form: `Select a start date before the end date`}))
        return
      }
    }
    setHasSubmitted(true)
    var year = 0
    if(form.year){
      year = form.year
    }
    var startDate = ""
    var endDate = ""
    if(form.startDate && form.endDate){
      startDate = moment(form.startDate).format('YYYY-MM-DD')
      endDate = moment(form.endDate).format('YYYY-MM-DD')
    }
    const res = await requestData({
      classification_level: form.classificationLevel,
      classification_name: form.classificationName,
      year: year,
      startDate: startDate,
      endDate: endDate,
      location_name: form.locationName,
      location_type: form.locationType
    })
    if(res.success) {
      const downloadID = res.data?.download_id
      const action = await retrieveData({download_id: downloadID}) 
      if(action.success) {
        addToast({
          id: `auth-toast-download-successful`,
          title: "Data Retrieval Successful",
          color: "success",
          iconType: "alert",
          toastLifeTimeMs: 15000,
          text: "Download should begin momentarily",
        })
        const href = window.URL.createObjectURL(new Blob([data]))
        const link = document.createElement('a')
        link.href = href
        link.setAttribute('download', 'download.csv') //or any other extension
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        //redirect
      }
      else{
          setErrors((errors) => ({ ...errors, form: "Submission failed, please check input fields"}))
        return
      }
    }
    else{
      if(res.error.status === 401){
        setErrors((errors) => ({ ...errors, form: "Not authorised to retrieve occurrences.  Please see FAQ"}))
      }
      else{
        setErrors((errors) => ({ ...errors, form: res.error.status}))
      }
      return
    }
  }
  const getFormErrors = () => {
    const formErrors = []
    if (errors.form) {
      formErrors.push(errors.form)
    }
    if (hasSubmitted && occurrenceErrorList.length) {
      return formErrors.concat(occurrenceErrorList)
    }
    return formErrors
  }

  

  return (
    <RetrieveDataFormWrapper>
      <EuiForm
        component="form"
        onSubmit={handleSubmit}
        isInvalid={Boolean(getFormErrors().length)}
        error={getFormErrors()}
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
                  dateFormat="YYYY-MM-DD"
                  selected={form.startDate}
                  onChange={(selected) => handleInputChange("startDate", selected)}
                  isInvalid={Boolean(errors.startDate)}
                />
              </EuiSplitPanel.Inner>
              <EuiSplitPanel.Inner>
                <EuiDatePicker
                  placeholder="Pick a end date"
                  dateFormat="YYYY-MM-DD"
                  selected={form.endDate}
                  onChange={(selected) => handleInputChange("endDate", selected)}
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
    </RetrieveDataFormWrapper>
  )
}

export default connect(
  (state) => ({
    occurenceError: state.occurrences.error,
    isLoading: state.occurrences.isLoading,
    data: state.occurrences.data,
  }),
  {
    requestData: occurrenceActions.requestData,
    retrieveData: occurrenceActions.retrieveData
  }
)(RetrieveDataForm)