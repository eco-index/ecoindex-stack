import string
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import SECRET_KEY, API_PREFIX
from app.models.security import UserInDB
from app.api.dependencies.database import get_repository
from app.db.repositories.users import UserRepository
from app.api.services import auth_service

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{API_PREFIX}/users/login/token/"
    )


# Get user from token held in Oauth2 scheme
async def get_user_from_token(
        *,
        token: str = Depends(oauth2_scheme),
        user_repo: UserRepository = Depends(get_repository(UserRepository)),
        ) -> Optional[UserInDB]:
    try:
        email = auth_service.get_email_from_token(
            token=token, 
            secret_key=str(SECRET_KEY)
            )
        user = await user_repo.get_user_by_email(email=email)
    except Exception as e:
        raise e
    return user


# Get current active user from token
def get_current_active_user(
        current_user: UserInDB = Depends(get_user_from_token)
        ) -> Optional[UserInDB]:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="No authenticated user.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Not an active user.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


# Check if user is authorised and if not raise http 401
def check_user_authorised(
        current_user: UserInDB,
        detail: string
        ) -> Optional[UserInDB]:
    if current_user.role=="GUEST":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )
    return current_user


# Checks if user is admin and if not raise http 401
def check_user_admin(
        current_user: UserInDB,
        detail: string
        ) -> Optional[UserInDB]:
    if current_user.role != "ADMIN" and current_user.role != "SUPER_ADMIN":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )
    return current_user