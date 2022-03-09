
from typing import Optional
from datetime import datetime, timedelta  

import bcrypt
import jwt
from fastapi import HTTPException, status
from pydantic import ValidationError
from passlib.context import CryptContext

from app.core.config import (
    SECRET_KEY, 
    ALGORITHM, 
    JWT_AUDIENCE, 
    JWT_AUDIENCE_RESET, 
    ACCESS_TOKEN_EXPIRE_MINUTES, 
    RESET_TOKEN_EXPIRE_MINUTES
)
from app.models.security import (
    UserPasswordUpdate, 
    UserInDB, 
    JWTMeta, 
    JWTCreds, 
    JWTPayload
)


# Auth Service Class

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthException(BaseException):
    """
    Custom auth exception that can be modified later on.
    """
    pass


class AuthService:
    

    # Salt and Hashed Password Actions
    def create_salt_and_hashed_password(
            self, *, plaintext_password: str
            ) -> UserPasswordUpdate:
        salt = self.generate_salt()
        hashed_password = self.hash_password(
            password = plaintext_password, 
            salt = salt)
        return UserPasswordUpdate(salt = salt, password = hashed_password)

    def generate_salt(self) -> str:
        return bcrypt.gensalt().decode()

    def hash_password(self, *, password: str, salt: str) -> str:
        return pwd_context.hash(password + salt)

    def verify_password(self, *, password: str, salt: str, hashed_pw: str
            ) -> bool:
        return pwd_context.verify(password + salt, hashed_pw)


    # Creates access or reset token for user
    def create_token_for_user(
            self,
            *,
            user: UserInDB,
            secret_key: str = str(SECRET_KEY),
            audience: str = JWT_AUDIENCE,
            expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES,
            reset: bool = False
            ) -> str:
        # Sets parameters if generating reset token
        if reset:
            audience = JWT_AUDIENCE_RESET
            expires_in = RESET_TOKEN_EXPIRE_MINUTES
        # If no user, returns none
        if not user or not isinstance(user, UserInDB):
            return None
        # Sets token parameters
        jwt_meta = JWTMeta(
            aud = audience,
            iat = datetime.timestamp(datetime.utcnow()),
            exp = datetime.timestamp(datetime.utcnow() 
                + timedelta(minutes = expires_in))
        )
        jwt_creds = JWTCreds(sub = user.email)
        token_payload = JWTPayload(
            **jwt_meta.dict(),
            **jwt_creds.dict(),
        )
        # Creates token
        access_token = jwt.encode(
            token_payload.dict(), 
            secret_key, 
            algorithm = ALGORITHM
        )
        # Returns token
        return access_token

    
    # Retrieves email from access or reset token
    def get_email_from_token(
            self, 
            *, 
            token: str, 
            secret_key: str, 
            reset: bool = False,
            audience: str = JWT_AUDIENCE
            ) -> Optional[str]:
        # Sets parameters for if reset token
        if reset:
            audience = JWT_AUDIENCE_RESET
        # Attempts to decode token
        try:
            decoded_token = jwt.decode(
                token, 
                str(secret_key), 
                audience = audience, 
                algorithms = [ALGORITHM]
            )
            payload = JWTPayload(**decoded_token)
        # If exception raised, returns unauthorised error
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Could not validate token credentials.",
                headers = {"WWW-Authenticate": "Bearer"},
            )
        # Returns email from token
        return payload.sub