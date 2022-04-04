from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import (
    HTTP_201_CREATED, 
    HTTP_401_UNAUTHORIZED, 
    HTTP_404_NOT_FOUND,
    HTTP_503_SERVICE_UNAVAILABLE
)

from app.api.services import auth_service, email_service
from app.core.config import PASSWORD_URL
from app.models.security import (
    User, 
    UserCreate, 
    AccessToken, 
    UserPublic, 
    UserInDB,
    UserUpdateRole,
    UserDisable,
    UserUpdate,
    UserResetPassword
)
from app.models.email import EmailSchema
from app.api.dependencies.database import get_repository
from app.api.dependencies.auth import (
    get_current_active_user,
    check_user_admin
)
from app.db.repositories.users import UserRepository



# User API Router

router = APIRouter()


# GET method, returns currently authenticated user if one exists
@router.get("/me/", response_model = UserPublic, 
            name = "users:get_current_user")
async def get_currently_authenticated_user(
        current_user: UserInDB = Depends(get_current_active_user)
        ) -> UserPublic:
    return current_user


# POST method, registers new user
@router.post("/", response_model = UserPublic, name = "users:register_new_user", 
             status_code=HTTP_201_CREATED)
async def register_new_user(
        new_user: UserCreate = Body(..., embed = True),
        user_repo: UserRepository = Depends(get_repository(UserRepository)),
        ) -> User:
    # Attempts to register new user
    created_user = await user_repo.register_new_user(new_user = new_user)
    # Creates access token for new user
    access_token = AccessToken(
        access_token = 
            auth_service.create_token_for_user(user = created_user), 
        token_type = "bearer"
    )
    # Returns new user and access token
    return UserPublic(**created_user.dict(), access_token=access_token)


# POST method, logs in user from OAuth2 form and returns access token
@router.post("/login/token/", response_model = AccessToken, 
             name = "users:login_email_and_password")
async def user_login_with_email_and_password(
        user_repo: UserRepository = Depends(get_repository(UserRepository)),
        form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
        ) -> AccessToken:
    # Attempts to authenticate user
    user = await user_repo.authenticate_user(
        email = form_data.username, 
        password = form_data.password
    )
    # If unable to, will raise exception
    if not user:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail = "Authentication was unsuccessful.",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    # Returns access token
    access_token = AccessToken(
        access_token = auth_service.create_token_for_user(user = user), 
        token_type = "bearer"
    )
    return access_token


# PUT method, updates a user's role
@router.put("/updaterole", response_model = UserUpdateRole, 
            name = "users:update_role")
async def update_role_of_user(
        current_user: UserInDB = Depends(get_current_active_user), 
        update_role_user: UserUpdateRole = Body(..., embed = True), 
        user_repo: UserRepository = Depends(get_repository(UserRepository))
        ) -> User:
    # Checks if current user is authorised
    check_user_admin(
        current_user = current_user, 
        detail = "Not authorized to update roles."
    )
    # Updates role of user specified
    updated_role_user = await user_repo.update_user_role(
        update_role_user = update_role_user
    )
    return updated_role_user


# GET method, returns all users
@router.get("/", name = "users:get_all_users")
async def get_all_users(
        user_repo: UserRepository = Depends(get_repository(UserRepository)),
        current_user: UserInDB = Depends(get_current_active_user),
        ) -> List[dict]:
    # Checks if authorised to retrieve users
    check_user_admin(
        current_user = current_user, 
        detail = "Not authorized to retrieve users"
    )
    # Gets all users
    users = await user_repo.get_all_users()
    # If no users found, returns exception
    if not users:
        raise HTTPException(
            status_code = HTTP_404_NOT_FOUND, 
            detail = "No users found"
        )
    # Returns users
    return users


# PUT method, enable or disable a user
@router.put("/disableuser", name = "users:enable_or_disable_user")
async def enable_or_disable_user(
        current_user: UserInDB = Depends(get_current_active_user),
        user_repo: UserRepository = Depends(get_repository(UserRepository)),
        user: UserDisable = Body(..., embed = True)
        ) -> UserDisable:
    # Check if authorised
    check_user_admin(
        current_user = current_user, 
        detail = "Not authorized to disable or enable users"
    )
    # Switch enabled to disabled or vice versa
    switch_disabled_user = await user_repo.switch_disabled(user_disable = user)
    # Returns user
    return switch_disabled_user


# PUT method, create and send forgot password email
@router.put("/forgotpassword", name = "users:forgot_password")
async def forgot_password(
        user_repo: UserRepository = Depends(get_repository(UserRepository)),
        user: UserUpdate = Body(..., embed = True)
        ) -> UserUpdate:
    # Gets user by email
    current_user = await user_repo.get_user_by_email(email = user.email)
    # If no user found, raises error
    if not current_user:
        raise HTTPException(
            status_code = HTTP_404_NOT_FOUND,
            detail = "No user found"
        )
    # Creates a reset token and associated link
    reset_token = auth_service.create_token_for_user(
        user = current_user,
        reset = True
    )
    link = PASSWORD_URL + reset_token
    # Creates email template
    params = {
            'title': 'Eco-index Password Reset',
            'greeting': 'Greetings!',
            'content': 'A request has been received to change the password for \
                your account for the <b>Eco-index Datastore.</b> <br><br>If you\
                 did not initiate this request, please contact us immediately \
                at <i>ecoindex‑dev@gmail.com</i> <br><br>The link to reset your\
                 password is as below: </p>',
            'link': link,
            'linktitle': 'Reset Password'
        }
    title = 'Reset Password Eco-index'
    emails = { user.email }
    email = EmailSchema(subject = title, email = emails, body = params)
    # Sends email
    res = await email_service.send_email_async(email)
    # Checks if sending was successful and if not, raises error
    if not res:      
        raise HTTPException(
            status_code = HTTP_503_SERVICE_UNAVAILABLE,
            detail = "Email could not be sent"
        )
    return user


# PUT method, resets password based on reset token
@router.put("/resetpassword", name = "users:reset_password")
async def reset_password(   
        user_repo: UserRepository = Depends(get_repository(UserRepository)),
        user_reset_password: UserResetPassword = Body(..., embed = True)
        ) -> UserPublic:
    # Attempts to update user password with user, new password, and token
    user = await user_repo.update_user_password(user = user_reset_password)
    return user

