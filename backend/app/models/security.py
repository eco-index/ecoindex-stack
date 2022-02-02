from typing import Optional, List
from pydantic import EmailStr, constr
from app.models.core import DateTimeModelMixin, IDModelMixin, CoreModel
from app.core.config import JWT_AUDIENCE, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta

# User Classes

class User(CoreModel):
    email: Optional[EmailStr]
    email_verified: bool = False
    disabled: bool = False
    role: str = "GUEST"

class UserCreate(CoreModel):
    """
    Email, and password are required for registering a new user
    """
    email: EmailStr
    password: constr(min_length=7, max_length=100)

class UserUpdate(CoreModel):
    """
    Users are allowed to update their email
    """
    email: Optional[EmailStr]

class UserUpdateRole(CoreModel):
    """
    For Admins to update User Role
    User, Admin, or Guest
    """
    email: EmailStr
    role: str

class UserDisable(CoreModel):
    """
    For Admins to enable or disable users
    """
    email: EmailStr

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

class JWTPayload(JWTMeta, JWTCreds):
    """
    JWT Payload right before it's encoded - combine meta and email
    """
    pass


