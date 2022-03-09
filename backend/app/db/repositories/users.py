from app.db.repositories.base import BaseRepository
from app.models.security import (
    UserInDB, 
    UserCreate, 
    UserUpdateRole, 
    UserDisable, 
    UserResetPassword
)
from fastapi import HTTPException, status
from pydantic import EmailStr
from passlib.context import CryptContext
from app.api.services import auth_service  
from databases import Database  
from typing import Optional, List


# User Repository Actions


# SQL Queries
GET_ALL_USERS_QUERY = """
    SELECT id, email, email_verified, disabled, role FROM users;
"""

REGISTER_NEW_USER_QUERY = """
    INSERT INTO users (email, password, salt)
    VALUES (:email, :password, :salt)
    RETURNING id, email, email_verified, password, salt, disabled, role;
"""

GET_USER_BY_EMAIL_QUERY = """
    SELECT * FROM users WHERE email = :email;
"""

UPDATE_USER_ROLE_QUERY="""
    UPDATE users SET role = :role WHERE email = :email RETURNING email, role;
"""

DISABLE_USER_QUERY="""
    UPDATE users SET disabled = True WHERE email = :email RETURNING email;
"""

ENABLE_USER_QUERY="""
    UPDATE users SET disabled = False WHERE email = :email RETURNING email;
"""

UPDATE_PASSWORD_QUERY="""
    UPDATE users SET password = :password, salt = :salt WHERE email = :email RETURNING email;
"""


class UserRepository(BaseRepository):
    """
    All database actions associated with the Users Table
    """
    def __init__(self, db: Database) -> None:
        super().__init__(db)
        self.auth_service = auth_service
    
    # Register new user action
    async def register_new_user(self, *, new_user: UserCreate) -> UserInDB:
         # make sure email isn't already taken
        if await self.get_user_by_email(email = new_user.email):
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "That email is already taken. Login with that email \
                    or register with another one."
            )
        user_hash_pw = self.auth_service.create_salt_and_hashed_password(
            plaintext_password = new_user.password
        )
        new_user_params = new_user.copy(update = user_hash_pw.dict())
        created_user = await self.db.fetch_one(
            query = REGISTER_NEW_USER_QUERY, 
            values = new_user_params.dict()
        )
        return UserInDB(**created_user)

    # Get user by email
    async def get_user_by_email(self, *, email: EmailStr) -> UserInDB:
        user_record = await self.db.fetch_one(
            query = GET_USER_BY_EMAIL_QUERY, 
            values = {"email": email}
        )
        if not user_record:
            return None
        return UserInDB(**user_record)
    
    # Authenticate user with password
    async def authenticate_user(self, *, email: EmailStr, password: str
            ) -> Optional[UserInDB]:
        # make sure user exists in db
        user = await self.get_user_by_email(email=email)
        if not user:
            return None
        # check that password matches
        if not self.auth_service.verify_password(
                password = password, 
                salt = user.salt, 
                hashed_pw = user.password
                ):
            return None
        return user

    # Update user role
    async def update_user_role(self, *, update_role_user: UserUpdateRole
            ) -> UserUpdateRole:
        user_record = await self.get_user_by_email(
            email = update_role_user.email
        )
        if not user_record:
            return None
        if (update_role_user.role != "ADMIN" 
                and update_role_user.role != "USER" 
                and update_role_user.role != "GUEST"):
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Not a valid user role"
            )
        updated_user = await self.db.fetch_one(
            query = UPDATE_USER_ROLE_QUERY, 
            values = {
                "email": update_role_user.email, 
                "role": update_role_user.role
            }
        )
        return updated_user
    
    # Updates user password given user, password, and reset token
    async def update_user_password(self, *, user: UserResetPassword
            ) -> UserInDB:
        email = self.auth_service.get_email_from_token(
            token = user.reset_token, 
            reset = True
        )
        if not await self.get_user_by_email(email = email):
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "User does not exist"
            )
        user_update = UserCreate(email = email, password = user.password)
        user_pw_update = self.auth_service.create_salt_and_hashed_password(
            plaintext_password = user.password
        )
        new_user_params = user_update.copy(update = user_pw_update.dict())
        updated_user = await self.db.fetch_one(
            query = UPDATE_PASSWORD_QUERY, 
            values = new_user_params.dict())
        return updated_user

    # Retrieves all users
    async def get_all_users(self) -> List[dict]:
        users = await self.db.fetch_all(query = GET_ALL_USERS_QUERY)
        if not users:
            return None
        return users
    
    # Switches user from disable to enabled or vice versa
    async def switch_disabled(self, *, user_disable: UserDisable
            ) -> UserDisable:
        user_record = await self.get_user_by_email(email = user_disable.email)
        if not user_record:
            return None
        query = ""
        if user_record.disabled:
            query = ENABLE_USER_QUERY
        else:
            query = DISABLE_USER_QUERY
        updated_user = await self.db.fetch_one(
            query = query, 
            values = {"email": user_record.email}
        )
        return updated_user
            

        
    
    