from typing import Union, Type, Optional

import pytest
from httpx import AsyncClient
from fastapi import FastAPI, HTTPException
import jwt
from starlette.status import ( 
    HTTP_201_CREATED, 
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED
)

from pydantic import ValidationError
from starlette.datastructures import Secret
from databases import Database

from app.core.config import (
    SECRET_KEY, 
    ALGORITHM, 
    JWT_AUDIENCE, 
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.models.security import UserInDB, UserPublic
from app.db.repositories.users import UserRepository
from app.api.services import auth_service

pytestmark = pytest.mark.asyncio

class TestUserRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient
            ) -> None:
        new_user = {"email": "test@email.io", "password": "testpassword"}
        res = await client.post(
            app.url_path_for("users:register_new_user"), 
            json = { "new_user": new_user }
        )
        assert res.status_code != HTTP_404_NOT_FOUND


class TestUserRegistration:
    async def test_users_saved_password_is_hashed_and_has_salt(
            self,
            app: FastAPI,
            client: AsyncClient,
            db: Database,
            ) -> None:
        user_repo = UserRepository(db)
        new_user = {
            "email": "beyonce@knowles.io", 
            "password": "destinyschild"
        }
        # send post request to create user and ensure it is successful
        res = await client.post(
            app.url_path_for("users:register_new_user"), 
            json={ "new_user": new_user }
        )
        assert res.status_code == HTTP_201_CREATED
        # ensure that the users password is hashed in the db
        # and that we can verify it using our auth service
        user_in_db = await user_repo.get_user_by_email(
            email = new_user["email"]
        )
        assert user_in_db is not None
        assert user_in_db.salt is not None and user_in_db.salt != "123"        
        assert user_in_db.password != new_user["password"]
        assert auth_service.verify_password(
            password = new_user["password"], 
            salt = user_in_db.salt, 
            hashed_pw = user_in_db.password,
        )

    async def test_users_can_register_successfully(
            self, 
            app: FastAPI, 
            client: AsyncClient,
            db: Database,
            ) -> None:
        user_repo = UserRepository(db)
        new_user = {
            "email": "shakira@shakira.io", 
            "password": "chantaje"}
        # make sure user doesn't exist yet
        user_in_db = await user_repo.get_user_by_email(
            email = new_user["email"]
        )
        assert user_in_db is None        
        # send post request to create user and ensure it is successful
        res = await client.post(
            app.url_path_for("users:register_new_user"), 
            json = { "new_user": new_user }
        )
        assert res.status_code == HTTP_201_CREATED
        # ensure that the user now exists in the db
        user_in_db = await user_repo.get_user_by_email(email=new_user["email"])
        assert user_in_db is not None
        assert user_in_db.email == new_user["email"]
        # check that the user returned in the response is equal to in database
        created_user = UserPublic(**res.json()).dict(exclude={
            "access_token", 
            "created_at", 
            "updated_at"
            })  
        assert created_user == user_in_db.dict(exclude={
            "password", 
            "salt", 
            "created_at", 
            "updated_at"
            })

    @pytest.mark.parametrize(
        "attr, value, status_code",
        (
            ("email", "shakira@shakira.io", 400),            
            ("email", "invalid_email@one@two.io", 422),
            ("password", "short", 422)
        )
    )
    async def test_user_registration_fails_when_credentials_are_taken(
            self, 
            app: FastAPI, 
            client: AsyncClient,
            attr: str,
            value: str,
            status_code: int,
            ) -> None: 
        new_user = {
            "email": "nottaken@email.io", 
            "username": "not_taken_username", 
            "password": "freepassword"
        }
        new_user[attr] = value
        res = await client.post(
            app.url_path_for("users:register_new_user"), 
            json = { "new_user": new_user }
        )
        assert res.status_code == status_code
    
class TestAuthTokens:
    async def test_can_create_access_token_successfully(
            self, test_user: UserInDB
            ) -> None:
        access_token = auth_service.create_token_for_user(
            user = test_user,
            secret_key = str(SECRET_KEY),
            audience = JWT_AUDIENCE,
            expires_in = ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        creds = jwt.decode(
            access_token, 
            str(SECRET_KEY), 
            audience = JWT_AUDIENCE, 
            algorithms = [ALGORITHM]
        )
        assert creds.get("sub") is not None
        assert creds["sub"] == test_user.email
        assert creds["aud"] == JWT_AUDIENCE

    async def test_token_missing_user_is_invalid(self) -> None:
        access_token = auth_service.create_token_for_user(
            user = None,
            secret_key = str(SECRET_KEY),
            audience = JWT_AUDIENCE,
            expires_in = ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        with pytest.raises(jwt.PyJWTError):
            jwt.decode(
                access_token, 
                str(SECRET_KEY), 
                audience=JWT_AUDIENCE, 
                algorithms=[ALGORITHM]
            )

    @pytest.mark.parametrize(
        "secret_key, jwt_audience, exception",
        (
            ("wrong-secret", JWT_AUDIENCE, jwt.InvalidSignatureError),
            (None, JWT_AUDIENCE, jwt.InvalidSignatureError),
            (SECRET_KEY, "othersite:auth", jwt.InvalidAudienceError),
            (SECRET_KEY, None, ValidationError),
        )
    )

    async def test_invalid_token_content_raises_error(
        self,
        test_user: UserInDB,
        secret_key: Union[str, Secret],
        jwt_audience: str,
        exception: Type[BaseException],
    ) -> None:
        with pytest.raises(exception):
            access_token = auth_service.create_token_for_user(
                user = test_user,
                secret_key = str(secret_key),
                audience = jwt_audience,
                expires_in = ACCESS_TOKEN_EXPIRE_MINUTES,
            )
            jwt.decode(
                access_token, 
                str(SECRET_KEY), 
                audience=JWT_AUDIENCE, 
                algorithms=[ALGORITHM]
            )
    
    @pytest.mark.parametrize(
        "secret, wrong_token",
        (
            (SECRET_KEY, "asdf"),  # use wrong token
            (SECRET_KEY, ""),  # use wrong token
            (SECRET_KEY, None),  # use wrong token
            ("ABC123", "use correct token"),  # use wrong secret
        ),
    )
    async def test_error_when_token_or_secret_is_wrong(
            self,
            test_user: UserInDB,
            secret: Union[Secret, str],
            wrong_token: Optional[str],
            ) -> None:
        token = auth_service.create_token_for_user(
            user = test_user, 
            secret_key = str(SECRET_KEY)
        )
        if wrong_token == "use correct token":
            wrong_token = token
        with pytest.raises(HTTPException):
            email = auth_service.get_email_from_token(
                token = wrong_token, 
                secret_key = str(secret)
            )   

class TestUserLogin:
    async def test_user_can_login_successfully_and_receives_valid_token(
            self, app: FastAPI, client: AsyncClient, test_user: UserInDB,
            ) -> None:
        client.headers["content-type"] = "application/x-www-form-urlencoded"
        login_data = {
            "username": test_user.email,
            "password": "heatcavslakers",  # insert user's plaintext password
        }
        res = await client.post(
            app.url_path_for("users:login_email_and_password"), 
            data = login_data
        )
        assert res.status_code == HTTP_200_OK
        # check that token exists in response and has user encoded within it
        token = res.json().get("access_token")
        creds = jwt.decode(
            token, 
            str(SECRET_KEY), 
            audience = JWT_AUDIENCE,
            algorithms=[ALGORITHM]
        )
        assert "sub" in creds
        assert creds["sub"] == test_user.email
        # check that token is proper type
        assert "token_type" in res.json()
        assert res.json().get("token_type") == "bearer"

    @pytest.mark.parametrize(
        "credential, wrong_value, status_code",
        (
            ("email", "wrong@email.com", 401),
            ("email", None, 422),
            ("email", "notemail", 401),
            ("password", "wrongpassword", 401),
            ("password", None, 422),
        ),
    )

    async def test_user_with_wrong_creds_doesnt_receive_token(
            self,
            app: FastAPI,
            client: AsyncClient,
            test_user: UserInDB,
            credential: str,
            wrong_value: str,
            status_code: int,
            ) -> None:
        client.headers["content-type"] = "application/x-www-form-urlencoded"
        user_data = test_user.dict()
        # insert user's plaintext password
        user_data["password"] = "heatcavslakers"  
        user_data[credential] = wrong_value
        login_data = {
            "username": user_data["email"],
            # insert password from parameters
            "password": user_data["password"],  
        }
        res = await client.post(
            app.url_path_for("users:login_email_and_password"), 
            data = login_data
        )
        assert res.status_code == status_code
        assert "access_token" not in res.json()
   

class TestUserMe:
    async def test_authenticated_user_can_retrieve_own_data(
            self, 
            app: FastAPI, 
            authorized_client: AsyncClient, 
            test_user: UserInDB,
            ) -> None:
        res = await authorized_client.get(
            app.url_path_for("users:get_current_user")
        )
        assert res.status_code == HTTP_200_OK
        user = UserPublic(**res.json())
        assert user.email == test_user.email
        assert user.id == test_user.id

    async def test_user_cannot_access_own_data_if_not_authenticated(
            self, app: FastAPI, client: AsyncClient, test_user: UserInDB,
            ) -> None:
        res = await client.get(app.url_path_for("users:get_current_user"))
        assert res.status_code == HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "jwt_prefix", (
            ("",), 
            ("value",), 
            ("Token",), 
            ("JWT",), 
            ("Swearer",),
        )
    )

    async def test_user_cannot_access_own_data_with_incorrect_jwt_prefix(
            self, 
            app: FastAPI, 
            client: AsyncClient, 
            test_user: UserInDB, 
            jwt_prefix: str,
            ) -> None:
        token = auth_service.create_token_for_user(
            user = test_user, 
            secret_key=str(SECRET_KEY)
        )
        res = await client.get(
            app.url_path_for("users:get_current_user"), 
            headers={"Authorization": f"{jwt_prefix} {token}"}
        )
        assert res.status_code == HTTP_401_UNAUTHORIZED
