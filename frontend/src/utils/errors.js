export const errorFieldToMessageMapping = {
    email: "Please enter a valid email.",
    username: "Please enter a username consisting of only letters, numbers, underscores, and dashes.",
    password: "Please choose a password with at least 7 characters."
  }
  export const parseErrorDetail = (errorDetail) => {
    let errorMessage = "Something went wrong. Contact support."
    if (Array.isArray(errorDetail?.loc)) {
      // error with a path parameter and probably isn't a client issue
      if (errorDetail.loc[0] === "path") return errorMessage
      // error with a query parameter and also is probably not the client's fault
      if (errorDetail.loc[0] === "query") return errorMessage
      // because we use FastAPI's `Body(..., embed)` for all post requests
      // this should be an array of length 3, with shape: ["body", "new_user", "email"]
      if (errorDetail.loc[0] === "body") {
        const invalidField = errorDetail.loc[2]
        if (errorFieldToMessageMapping[invalidField]) {
          errorMessage = errorFieldToMessageMapping[invalidField]
        } else if (errorDetail?.msg) {
          errorMessage = errorDetail.msg
        }
      }
    }
    return errorMessage
  }
  export const extractErrorMessages = (error) => {
    const errorList = []
    // if we just pass in a string, use that
    if (typeof error === "string") errorList.push(error)
    // in the case that we raised the error ourselves with FastAPI's HTTPException,
    // just use the message passed from the backend.
    if (typeof error?.detail === "string") errorList.push(error.detail)
    // in the case that there's a validation error in the request body, path parameters, or query parameters
    // we'll get an array of error issues here:
    if (Array.isArray(error?.detail)) {
      error.detail.forEach((errorDetail) => {
        const errorMessage = parseErrorDetail(errorDetail)
        errorList.push(errorMessage)
      })
    }
    return errorList
  }
  