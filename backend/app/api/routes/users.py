from fastapi import APIRouter

from fastapi import Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from typing import List

from app.api.services import auth_service, email_service
from app.core.config import PASSWORD_URL

from app.models.security import User, UserCreate, UserUpdate, AccessToken, UserPublic, UserInDB, UserUpdateRole, UserDisable, UserResetPassword
from app.models.email import EmailSchema
from app.api.dependencies.database import get_repository
from app.api.dependencies.auth import get_current_active_user
from app.db.repositories.users import UserRepository

router = APIRouter()

@router.get("/me/", response_model=UserPublic, name="users:get_current_user")
async def get_currently_authenticated_user(current_user: UserInDB = Depends(get_current_active_user)) -> UserPublic:
    return current_user

@router.post("/", response_model=UserPublic, name="users:register_new_user", status_code=HTTP_201_CREATED)
async def register_new_user(
    new_user: UserCreate = Body(..., embed=True),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> User:
    created_user = await user_repo.register_new_user(new_user=new_user)
    access_token = AccessToken(
        access_token=auth_service.create_access_token_for_user(user=created_user), token_type="bearer"
    )
    return UserPublic(**created_user.dict(), access_token=access_token)

@router.post("/login/token/", response_model=AccessToken, name="users:login_email_and_password")
async def user_login_with_email_and_password(
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
) -> AccessToken:
    user = await user_repo.authenticate_user(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Authentication was unsuccessful.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = AccessToken(access_token=auth_service.create_access_token_for_user(user=user), token_type="bearer")
    return access_token

@router.put("/updaterole", response_model=UserUpdateRole, name="users:update_role")
async def update_role_of_user(
    current_user: UserInDB = Depends(get_current_active_user), 
    update_role_user: UserUpdateRole = Body(..., embed=True), 
    user_repo: UserRepository = Depends(get_repository(UserRepository))
    ) -> User:
    if current_user.role != "ADMIN" and current_user.role != "SUPER_ADMIN":
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authorized to update roles."
        )
    updated_role_user = await user_repo.update_user_role(update_role_user=update_role_user)
    return updated_role_user
    
@router.get("/")
async def get_all_users(
    user_repo: UserRepository= Depends(get_repository(UserRepository)),
    current_user: UserInDB = Depends(get_current_active_user),
) -> List[dict]:
    if current_user.role == "GUEST" or current_user.role == "USER":
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authorized to retrieve users"
        )
    users = await user_repo.get_all_users()
    if not users:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No users found")
    return users

@router.put("/disableuser", name="users:enable_or_disable_user")
async def enable_or_disable_user(
    current_user: UserInDB = Depends(get_current_active_user),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    user: UserDisable = Body(..., embed=True)
) -> UserDisable:
    if current_user.role != "ADMIN" and current_user.role != "SUPER_ADMIN":
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authorized to disable or enable users"
        )
    switch_disabled_user = await user_repo.switch_disabled(user_disable=user)
    return switch_disabled_user

@router.put("/forgotpassword", name="users:forgot_password")
async def forgot_password(
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    user: UserUpdate = Body(..., embed=True)
) -> UserUpdate:
    current_user = await user_repo.get_user_by_email(email=user.email)
    if not current_user:
        raise HTTPException(
            status_code = HTTP_404_NOT_FOUND,
            detail="No user found"
        )
    reset_token = auth_service.create_reset_token(user=current_user)
    link = PASSWORD_URL+reset_token
    params = {
            'title': 'Eco-index Password Reset',
            'greeting': 'Greetings!',
            'content': 'A request has been received to change the password for your account for the <b>Eco-index Datastore.</b> <br><br>If you did not initiate this request, please contact us immediately at <i>ecoindex‑dev@gmail.com</i> <br><br>The link to reset your password is as below: </p>',
            'link': link,
            'linktitle': 'Reset Password'
        }
    title = 'Reset Password Eco-index'
    emails = { user.email }
    email = EmailSchema(subject = title, email = emails, body = params)
    res = await email_service.send_email_async(email)
    if(res):
        return user
    else:
        raise HTTPException(
            status_code = HTTP_404_NOT_FOUND,
            detail="Email could not be sent"
        )


@router.put("/resetpassword", name= "users:reset_password")
async def reset_password(   
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    user_reset_password: UserResetPassword =  Body(..., embed=True)
) -> UserPublic:
    user = await user_repo.update_user_password(user=user_reset_password)
    return user

