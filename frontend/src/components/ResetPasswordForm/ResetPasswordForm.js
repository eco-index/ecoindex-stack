import React from "react"
import { connect } from "react-redux"
import { Actions as authActions} from "../../redux/auth"
import { useNavigate, useSearchParams } from "react-router-dom"
import { useToasts } from "../../hooks/ui/useToasts" 
import {
  EuiButton,
  EuiForm,
  EuiFormRow,
  EuiFieldPassword,
  EuiSpacer
} from "@elastic/eui"
import validation from "../../utils/validation"
import styled from "styled-components"
import { extractErrorMessages } from "../../utils/errors"
const ResetPasswordFormWrapper = styled.div`
  padding: 2rem;
`

function ResetPasswordForm({ authError, isLoading, updateUserPassword }) {
  const [searchParams, setSearchParams] = useSearchParams()
  const [token, setToken] = React.useState(
      searchParams.get("token")
  )
  const [form, setForm] = React.useState({
    password: "",
    passwordConfirm: ""
  })
  const [errors, setErrors] = React.useState({})
  const [hasSubmitted, setHasSubmitted] = React.useState(false) 
  const { addToast } = useToasts()
  const navigate = useNavigate()
  const authErrorList = extractErrorMessages(authError) 
  const {REACT_APP_PUBLIC_URL} = process.env
  // if the user is already authenticated, redirect them to the landing page
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
  const handlePasswordConfirmChange = (value) => {
    setErrors((errors) => ({
      ...errors,
      passwordConfirm: form.password !== value ? `Passwords do not match.` : null
    }))
    setForm((form) => ({ ...form, passwordConfirm: value }))
  }
  const handleSubmit = async (e) => {
    e.preventDefault()
    // validate inputs before submitting
    Object.keys(form).forEach((label) => validateInput(label, form[label]))
    // if any input hasn't been entered in, return early
    
    if (!Object.values(form).every((value) => Boolean(value))) {
      setErrors((errors) => ({ ...errors, form: `You must fill out all fields.` }))
      return
    }
    // some additional validation
    if (form.password !== form.passwordConfirm) {
      setErrors((errors) => ({ ...errors, form: `Passwords do not match.` }))
      return
    }
    setHasSubmitted(true)
    const action = await updateUserPassword({
      reset_token: token,
      password: form.password
    })
    if(action.success){
        addToast({
            id: `auth-toast-update-password-successful`,
            title: "Password Update Successful",
            color: "success",
            iconType: "alert",
            toastLifeTimeMs: 15000,
          })
          navigate({REACT_APP_PUBLIC_URL} + "/login")
    }
    else{
      setErrors((errors) => ({ ...errors, form: "Update password failed, please check input fields"}))
      setForm((form) => ({ ...form, password: "", passwordConfirm: "" }))
      return
    }

  }
  const getFormErrors = () => {
    const formErrors = []
    if (errors.form) {
      formErrors.push(errors.form)
    }
    if (hasSubmitted && authErrorList.length) {
      return formErrors.concat(authErrorList)
    }
    return formErrors
  }

  return (
    <ResetPasswordFormWrapper>
      <EuiForm
        component="form"
        onSubmit={handleSubmit}
        isInvalid={Boolean(getFormErrors().length)}
        error={getFormErrors()}
      >
        <EuiFormRow
          label="Password"
          helpText="Enter your password."
          isInvalid={Boolean(errors.password)}
          error={`Password must be at least 7 characters.`}
        >
          <EuiFieldPassword
            placeholder="••••••••••••"
            value={form.password}
            onChange={(e) => handleInputChange("password", e.target.value)}
            type="dual"
            aria-label="Enter your password."
            isInvalid={Boolean(errors.password)}
          />
        </EuiFormRow>
        <EuiFormRow
          label="Confirm password"
          helpText="Confirm your password."
          isInvalid={Boolean(errors.passwordConfirm)}
          error={`Passwords must match.`}
        >
          <EuiFieldPassword
            placeholder="••••••••••••"
            value={form.passwordConfirm}
            onChange={(e) => handlePasswordConfirmChange(e.target.value)}
            type="dual"
            aria-label="Confirm your password."
            isInvalid={Boolean(errors.passwordConfirm)}
          />
        </EuiFormRow>
        <EuiSpacer />
        <EuiButton type="submit" isLoading={isLoading} fill>
          Update Password
        </EuiButton>
      </EuiForm>
    </ResetPasswordFormWrapper>
  )
}

export default connect(
  (state) => ({
    authError: state.auth.error,
    isLoading: state.auth.isLoading,
    user: state.auth.user
  }),
  {
    updateUserPassword: authActions.updateUserPassword
  }
)(ResetPasswordForm)