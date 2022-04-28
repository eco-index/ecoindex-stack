import React from "react"
import { connect } from "react-redux"
import { Actions as authActions} from "../../redux/auth"
import { useNavigate } from "react-router-dom"
import { useToasts } from "../../hooks/ui/useToasts" 
import {
  EuiButton,
  EuiForm,
  EuiFormRow,
  EuiFieldText,
  EuiSpacer
} from "@elastic/eui"
import validation from "../../utils/validation"
import styled from "styled-components"
import { extractErrorMessages } from "../../utils/errors"
const ForgotPasswordFormWrapper = styled.div`
  padding: 2rem;
`

function ForgotPasswordForm({ authError, isLoading, resetPasswordRequest }) {
  const [form, setForm] = React.useState({
    email: ""
  })
  const [errors, setErrors] = React.useState({})
  const [hasSubmitted, setHasSubmitted] = React.useState(false) 
  const { addToast } = useToasts()
  const navigate = useNavigate()
  const authErrorList = extractErrorMessages(authError) 
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
  const handleSubmit = async (e) => {
    e.preventDefault()
    // validate inputs before submitting
    Object.keys(form).forEach((label) => validateInput(label, form[label]))
    // if any input hasn't been entered in, return early
    
    if (!Object.values(form).every((value) => Boolean(value))) {
      setErrors((errors) => ({ ...errors, form: `Please enter a valid email.` }))
      return
    }
    setHasSubmitted(true)
    const action = await resetPasswordRequest({
      email: form.email
    })
    if(action.success){
        addToast({
            id: `auth-toast-reset-password-successful`,
            title: "Reset Password Request Successful",
            color: "success",
            iconType: "alert",
            toastLifeTimeMs: 15000,
            text: "Please check your email for a reset password link"
        })
        navigate("/frontendv2/login")
    }
    else{
      setErrors((errors) => ({ ...errors, form: "Please enter a valid email."}))
      return
    }

  }
  const getFormErrors = () => {
    const formErrors = []
    if (errors.form) {
      formErrors.push(errors.form)
    }
    return formErrors
  }

  return (
    <ForgotPasswordFormWrapper>
      <EuiForm
        component="form"
        onSubmit={handleSubmit}
        isInvalid={Boolean(getFormErrors().length)}
        error={getFormErrors()}
      >
        <EuiFormRow
          label="Email"
          helpText="Enter the email associated with your account."
          isInvalid={Boolean(errors.email)}
          error={`Please enter a valid email.`}
        >
          <EuiFieldText
            icon="email"
            placeholder="user@gmail.com"
            value={form.email}
            onChange={(e) => handleInputChange("email", e.target.value)}
            aria-label="Enter the email associated with your account."
            isInvalid={Boolean(errors.email)}
          />
        </EuiFormRow>
        <EuiSpacer />
        <EuiButton type="submit" isLoading={isLoading} fill>
          Reset Password
        </EuiButton>
      </EuiForm>
    </ForgotPasswordFormWrapper>
  )
}

export default connect(
  (state) => ({
    authError: state.auth.error,
    isLoading: state.auth.isLoading,
    user: state.auth.user
  }),
  {
    resetPasswordRequest: authActions.resetPasswordRequest
  }
)(ForgotPasswordForm)