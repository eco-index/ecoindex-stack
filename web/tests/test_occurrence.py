import pytest
import json

from httpx import AsyncClient
from fastapi import FastAPI

from starlette.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
)
from app.models.occurrence import OccurrencePublic, OccurrenceCreate, OccurrenceJson
        
    # @pytest.mark.parametrize(
    #     "id, status_code",
    #     (
    #         (500, 404),
    #         (-1, 404),
    #         (None, 422),
    #     ),
    # )
    # async def test_wrong_id_returns_error(
    #     self, app: FastAPI, client: AsyncClient, id: int, status_code: int
    # ) -> None:
    #     res = await client.get(app.url_path_for("cleanings:get-cleaning-by-id", id=id))
    #     assert res.status_code == status_code


# decorate all tests with @pytest.mark.asyncio
pytestmark = pytest.mark.asyncio  

@pytest.fixture
def new_occurrence():
    return OccurrenceJson(
        scientific_name='fake scientific name',
        observation_date='2020-10-19',
        taxon_rank='fake taxon rank'
    )

class TestOccurrenceRoutes:
    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("occurrence:create_occurrence"), json={})
        assert res.status_code != HTTP_404_NOT_FOUND

class TestCreateOccurrence:
    async def test_valid_input_creates_occurrence(
        self, app: FastAPI, client: AsyncClient, new_occurrence: OccurrenceJson
    ) -> None:
        print(new_occurrence.dict())
        res = await client.post(
            app.url_path_for("occurrence:create_occurrence"), json=new_occurrence.dict()
        )
        assert res.status_code == HTTP_201_CREATED
        created_occurrence = OccurrenceJson(**res.json())
        assert created_occurrence == new_occurrence

    @pytest.mark.parametrize(
        "invalid_payload, status_code",
        (
            (None, 422),
            ({}, 422),
            ({"scientific_name": "test_name"}, 422),
            ({"observation_count": 2}, 422),
            ({"scientific_name": "test_name", "taxon_rank": "test"}, 422),
        ),
    )
    async def test_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncClient, invalid_payload: dict, status_code: int
    ) -> None:
        res = await client.post(
            app.url_path_for("occurrence:create_occurrence"), json={"new_occurrence": invalid_payload}
        )
        assert res.status_code == status_code

class TestGetOccurrence:
    async def test_get_all_occurrences(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.get(app.url_path_for("occurrence:get_all_occurrences"))
        assert res.status_code == HTTP_200_OK

