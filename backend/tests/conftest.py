import warnings
import os

import pytest
from fastapi import FastAPI
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from databases import Database
import alembic
from alembic.config import Config

from app.api.services import auth_service
from app.models.security import UserInDB, UserCreate, UserUpdateRole
from app.db.repositories.users import UserRepository
from app.core.config import JWT_TOKEN_PREFIX, TEST_DATABASE_URL

# Apply migrations at beginning and end of testing session
@pytest.fixture(scope = "session")
def apply_migrations():
    warnings.filterwarnings("ignore", category = DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")
    
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")

# Create a new application for testing
@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.api.server import get_application
    
    return get_application()

# Grab a reference to our database when needed
@pytest.fixture
async def db(app: FastAPI) -> Database:
    db = Database(TEST_DATABASE_URL, min_size=2, max_size=10)  
    await db.connect()
    yield db
    db.disconnect()
    
# Make requests in our tests
@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app = app, 
            base_url = "http://testserver", 
            headers = {"Content-Type": "application/json"}
        ) as client:
            yield client

@pytest.fixture
async def test_user(db: Database) -> UserInDB:
    new_user = UserCreate(
        email = "lebron@james.io",
        password = "heatcavslakers",
    )
    user_repo = UserRepository(db)
    existing_user = await user_repo.get_user_by_email(email = new_user.email)
    if existing_user:
        return existing_user
    userindb = await user_repo.register_new_user(new_user = new_user)
    updateroleuser = UserUpdateRole(
        email = userindb.email,
        role = "USER"
    )
    await user_repo.update_user_role(update_role_user = updateroleuser)
    return userindb


@pytest.fixture
def authorized_client(client: AsyncClient, test_user: UserInDB) -> AsyncClient:
    access_token = auth_service.create_token_for_user(user = test_user)

    client.headers = {
        **client.headers,
        "Authorization": f"{JWT_TOKEN_PREFIX} {access_token}",
    }
    return client