from fastapi import APIRouter

from fastapi import Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from app.api.services import auth_service

from app.models.security import User, UserCreate, AccessToken, UserPublic, UserInDB
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