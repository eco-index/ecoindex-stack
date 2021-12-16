from typing import Optional, List
from pydantic import EmailStr, constr
from app.models.core import DateTimeModelMixin, IDModelMixin, CoreModel
from app.core.config import JWT_AUDIENCE, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta

# User Classes

class User(CoreModel):
    email: Optional[EmailStr]
    username: Optional[str]
    email_verified: bool = False
    disabled: bool = False
    role: str = "GUEST"

class UserCreate(CoreModel):
    """
    Email, username, and password are required for registering a new user
    """
    email: EmailStr
    password: constr(min_length=7, max_length=100)
    username: constr(min_length=3, regex="^[a-zA-Z0-9_-]+$")

class UserUpdate(CoreModel):
    """
    Users are allowed to update their email and/or username
    """
    email: Optional[EmailStr]
    username: Optional[constr(min_length=3, regex="^[a-zA-Z0-9_-]+$")]

class UserUpdateRole(CoreModel):
    """
    For Admins to update User Role
    """
    email: EmailStr
    role: str

class UserPasswordUpdate(CoreModel):
    """
    Users can change their password
    """
    password: constr(min_length=7, max_length=100)
    salt: str

class UserInDB(IDModelMixin, DateTimeModelMixin, User):
    password: str
    salt: str

class AccessToken(CoreModel):
    access_token: str
    token_type: str
    
class UserPublic(IDModelMixin, DateTimeModelMixin, User):
    access_token: Optional[AccessToken]

class JWTMeta(CoreModel):
    iss: str = "ecoindex.io"
    aud: str = JWT_AUDIENCE
    iat: float = datetime.timestamp(datetime.utcnow())
    exp: float = datetime.timestamp(datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

class JWTCreds(CoreModel):
    """
    How we'll identify users
    """
    sub: EmailStr
    username: str

class JWTPayload(JWTMeta, JWTCreds):
    """
    JWT Payload right before it's encoded - combine meta and username
    """
    pass


