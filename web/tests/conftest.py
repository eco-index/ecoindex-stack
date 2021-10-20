import warnings
import os

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI

from httpx import AsyncClient
from databases import Database

import alembic
from alembic.config import Config

from app.models.occurrence import OccurrenceCreate, OccurrencePublic
from app.db.repositories.occurrence import OccurrenceRepository

# Apply migrations at beginning and end of testing session
@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")

# Create a new application for testing
@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.api.server import get_application
    return  get_application()

# Grab a reference to our database when needed
@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db
    
# Make requests in our tests
@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"}
        ) as client:
            yield client

@pytest.fixture
async def test_occurrence(db: Database) -> OccurrencePublic:
    occurrence_repo = OccurrenceRepository(db)
    new_occurrence = OccurrenceCreate(
        scientific_name="fake scientific name",
        observation_count=1,
        observation_date=2020-10-19,
        taxon_rank='fake taxon rank'
    )
    return await occurrence_repo.create_occurrence(new_occurrence=new_occurrence)