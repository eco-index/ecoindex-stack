import warnings
import os
import csv
import sys

import pytest
from fastapi import FastAPI
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from databases import Database
import alembic
from alembic.config import Config

from app.api.services import auth_service
from app.models.security import UserInDB, UserCreate, UserUpdateRole
from app.models.occurrence import OccurrencePublic, OccurrenceCreate
from app.db.repositories.occurrence import OccurrenceRepository
from app.db.repositories.users import UserRepository
from app.core.config import JWT_TOKEN_PREFIX, TEST_DATABASE_URL, DATABASE_URL

# Apply migrations at beginning and end of testing session
@pytest.fixture(scope = "session")
def apply_migrations():
    warnings.filterwarnings("ignore", category = DeprecationWarning)
    os.environ["TESTING"] = "0"
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
    await db.disconnect()
    
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
async def test_occurrence(db: Database) -> OccurrencePublic:
    occurrence_repo = OccurrenceRepository(db)
    new_occurrence = OccurrenceCreate(
        scientific_name = 'Branta canadensis maxima Delacour, 1951', 
        observation_count = 1, 
        observation_date =  '2015-05-22',
        occurrence_latitude = -43.486205,
        occurrence_longitude = 172.697703, 
        occurrence_elevation = 0.0,
        occurrence_depth = 0.0,
        taxon_rank = 'SUBSPECIES',
        infraspecific_epithet = '',
        occurrence_species =  'Branta canadensis',
        occurrence_genus = 'Branta',
        occurrence_family = 'Anatidae',
        occurrence_order = 'Anseriformes',
        occurrence_class = 'Aves',
        occurrence_phylum = 'Chordata',
        occurrence_kingdom = 'Animalia'
    )
    csv.field_size_limit(sys.maxsize)
    location_file = csv.DictReader(open(
        "./location_data/regional_council_boundaries_clipped.csv"
    ))
    for row in location_file:
        name = row['name']
        polygon = row['polygon']
        type = row['locationtype']
        await occurrence_repo.add_location(
            name = name,
            polygon = polygon,
            location_type = type
        )
    occurrence = await occurrence_repo.get_occurrence_by_id(id = 1)
    if occurrence:
        return occurrence
    occurrence = await occurrence_repo.create_occurrence(
        occurrence = new_occurrence
    )
    return occurrence

@pytest.fixture
def authorized_client(client: AsyncClient, test_user: UserInDB) -> AsyncClient:
    access_token = auth_service.create_token_for_user(user = test_user)

    client.headers = {
        **client.headers,
        "Authorization": f"{JWT_TOKEN_PREFIX} {access_token}",
    }
    return client