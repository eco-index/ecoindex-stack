import React from "react"
import moment from "moment"
import { connect } from "react-redux"
import { useToasts } from "../../hooks/ui/useToasts" 
import { Actions as mciActions } from "../../redux/mci"
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
function RetrieveDataForm({ mciError, isLoading, requestData, retrieveData}) {
  const [form, setForm] = React.useState({
    // classificationLevel: "",
    // classificationName: "",
    indicator: "",
    startValue: "",
    endValue: "",
    year: "",
    startDate: "",
    endDate: "",
    locationType: "",
    locationName: "",
    riverCatchment: "",
    landcoverType: ""
  })
  const [errors, setErrors] = React.useState({})
  const [hasSubmitted, setHasSubmitted] = React.useState(false) 
  const mciErrorList = extractErrorMessages(mciError) 
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
    // if(form.classificationName && !form.classificationLevel){
    //   setErrors((errors) => ({ ...errors, form: `Please select a classification level.` }))
    //   return
    // }
    // //if classification level is selected but no classification name
    // if(form.classificationLevel && !form.classificationName){
    //   form.classificationLevel = ""
    //   setErrors((errors) => ({ ...errors, form: `Please specify a classification name` }))
    //   return
    // }
    if(form.startValue && form.endValue && !form.indicator){
      setErrors((errors) => ({ ...errors, form: `Please select an indicator type` }))
      return
    }
    if(form.startValue && !form.endValue){
      setErrors((errors) => ({ ...errors, form: `Please enter an end value` }))
      return
    }
    if(!form.startValue && form.endValue){
      setErrors((errors) => ({ ...errors, form: `Please enter a start value` }))
      return
    }
    if(form.endValue < form.startValue){
      setErrors((errors) => ({ ...errors, form: `Please enter a start value lower than the end value` }))
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
    var startValue = null
    var endValue = null
    if(form.startValue){
      startValue = form.startValue
    }
    if(form.endValue){
      endValue = form.endValue
    }
    var startDate = ""
    var endDate = ""
    if(form.startDate && form.endDate){
      startDate = moment(form.startDate).format('YYYY-MM-DD')
      endDate = moment(form.endDate).format('YYYY-MM-DD')
    }
    const res = await requestData({
      // classification_level: form.classificationLevel,
      // classification_name: form.classificationName,
      startValue: startValue,
      endValue: endValue,
      indicator: form.indicator,
      year: year,
      startDate: startDate,
      endDate: endDate,
      location_name: form.locationName,
      location_type: form.locationType,
      river_catchment: form.riverCatchment,
      landcover_type: form.landcoverType
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
        const href = window.URL.createObjectURL(new Blob([action.data]))
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
        setErrors((errors) => ({ ...errors, form: "Not authorised to retrieve data.  Please see FAQ"}))
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
    if (hasSubmitted && mciErrorList.length) {
      return formErrors.concat(mciErrorList)
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
          label="Indicator Type"
          isInvalid={Boolean(errors.email)}
        >
          <EuiSuperSelect
            options={[
              {
                value: 'MCI',
                inputDisplay: 'MCI'
              },
              {
                value: 'PercentageEPTTaxa',
                inputDisplay: 'Percentage EPT Taxa'
              },
              {
                value: 'QMCI',
                inputDisplay: 'QMCI'
              },
              {
                value: 'ASPM',
                inputDisplay: 'ASPM'
              },
              {
                value: 'TaxaRichness',
                inputDisplay: 'Taxa Richness'
              }
            ]}
            valueOfSelected = {form.indicator}
            onChange={(value) => handleInputChange("indicator", value)}
            itemLayoutAlign="top"
            isInvalid={Boolean(errors.indicator)}
          />
        </EuiFormRow>
        <EuiFormRow
          label="Value"
          helpText="Input a value range to filter the data by. NB: An indicator type must be selected."
        >
          <EuiSplitPanel.Outer>
              <EuiSplitPanel.Inner>
                <EuiFieldText
                  placeholder="Enter a starting value"
                  value={form.startValue}
                  onChange={(e) => handleInputChange("startValue", e.target.value)}
                  isInvalid={Boolean(errors.startValue)}
                />
              </EuiSplitPanel.Inner>
              <EuiSplitPanel.Inner>
                <EuiFieldText
                  placeholder="Enter an end value"
                  value={form.endValue}
                  onChange={(e) => handleInputChange("endValue", e.target.value)}
                  isInvalid={Boolean(errors.endValue)}
                />
              </EuiSplitPanel.Inner>
          </EuiSplitPanel.Outer>
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
        <EuiFormRow
          label="River Catchment"
        >
              <EuiFieldText
                value={form.riverCatchment}
                onChange={(e) => handleInputChange("riverCatchment", e.target.value)}
                isInvalid={Boolean(errors.riverCatchment)}
              />
        </EuiFormRow>
        <EuiFormRow
          label="Landcover Type"
        >
          <EuiSuperSelect
            options={[
              {
                value: 'Native vegetation',
                inputDisplay: 'Native vegetation'
              },
              {
                value: 'Pasture',
                inputDisplay: 'Pasture'
              },
              {
                value: 'Plantation forest',
                inputDisplay: 'Plantation forest'
              },
              {
                value: 'Urban',
                inputDisplay: 'Urban'
              }
            ]}
            valueOfSelected = {form.landcoverType}
            onChange={(value) => handleInputChange("landcoverType", value)}
            itemLayoutAlign="top"
            isInvalid={Boolean(errors.landcoverType)}
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
    occurenceError: state.mci.error,
    isLoading: state.mci.isLoading,
    data: state.mci.data,
  }),
  {
    requestData: mciActions.requestData,
    retrieveData: mciActions.retrieveData
  }
)(RetrieveDataForm)