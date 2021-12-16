import React from "react"
import { connect } from "react-redux"
import { Actions as authActions, FETCHING_USER_FROM_TOKEN_SUCCESS } from "../../redux/auth"
import { useNavigate } from "react-router-dom"
import {
  EuiButton,
  EuiCheckbox,
  EuiFieldText,
  EuiForm,
  EuiFormRow,
  EuiFieldPassword,
  EuiSpacer
} from "@elastic/eui"
import { Link } from "react-router-dom"
import validation from "../../utils/validation"
import { htmlIdGenerator } from "@elastic/eui/lib/services"
import styled from "styled-components"
import { extractErrorMessages } from "../../utils/errors"
const RegistrationFormWrapper = styled.div`
  padding: 2rem;
`
const NeedAccountLink = styled.span`
  font-size: 0.8rem;
`
function RegistrationForm({ authError, user, isLoading, isAuthenticated, registerUser }) {
  const [form, setForm] = React.useState({
    username: "",
    email: "",
    password: "",
    passwordConfirm: ""
  })
  const [agreedToTerms, setAgreedToTerms] = React.useState(false)
  const [errors, setErrors] = React.useState({})
  const [hasSubmitted, setHasSubmitted] = React.useState(false) 
  const navigate = useNavigate()
  const authErrorList = extractErrorMessages(authError) 
  // if the user is already authenticated, redirect them to the landing page
  React.useEffect(() => {
    if (user?.email && isAuthenticated) {
      navigate("/frontend")
    }
  }, [user, navigate, isAuthenticated])
  const validateInput = (label, value) => {
    // grab validation function and run it on input if it exists
    // if it doesn't exists, just assume the input is valid
    const isValid = validation?.[label] ? validation?.[label]?.(value) : true
    // set an error if the validation function did NOT return true
    setErrors((errors) => ({ ...errors, [label]: !isValid }))
  }
  const setAgreedToTermsCheckbox = (e) => {
    setAgreedToTerms(e.target.checked)
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
    if (!agreedToTerms) {
      setErrors((errors) => ({ ...errors, form: `You must agree to the terms and conditions.` }))
      return
    }
    setHasSubmitted(true)
    const action = await registerUser({
      username: form.username,
      email: form.email,
      password: form.password
    })
    if (action?.type !== FETCHING_USER_FROM_TOKEN_SUCCESS) {
      setForm((form) => ({ ...form, password: "", passwordConfirm: "" }))
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
    <RegistrationFormWrapper>
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
        <EuiFormRow
          label="Username"
          helpText="Choose a username consisting solely of letters, numbers, underscores, and dashes."
          isInvalid={Boolean(errors.username)}
          error={`Please enter a valid username.`}
        >
          <EuiFieldText
            icon="user"
            placeholder="your_username"
            value={form.username}
            onChange={(e) => handleInputChange("username", e.target.value)}
            aria-label="Choose a username consisting of letters, numbers, underscores, and dashes."
            isInvalid={Boolean(errors.username)}
          />
        </EuiFormRow>
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
        <EuiCheckbox
          id={htmlIdGenerator()()}
          label="I agree to the terms and conditions."
          checked={agreedToTerms}
          onChange={(e) => setAgreedToTermsCheckbox(e)}
        />
        <EuiSpacer />
        <EuiButton type="submit" isLoading={isLoading} fill>
          Sign Up
        </EuiButton>
      </EuiForm>
      <EuiSpacer size="xl" />
      <NeedAccountLink>
        Already have an account? Log in <Link to="/frontend/login">here</Link>.
      </NeedAccountLink>
    </RegistrationFormWrapper>
  )
}

export default connect(
  (state) => ({
    authError: state.auth.error,
    isLoading: state.auth.isLoading,
    isAuthenticated: state.auth.isAuthenticated,
    user: state.auth.user
  }),
  {
    registerUser: authActions.registerNewUser
  }
)(RegistrationForm)