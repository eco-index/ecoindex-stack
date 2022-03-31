import json
import time
import os
import pandas as pd
import io
from typing import Tuple

import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from starlette.status import (
    HTTP_200_OK
)
from databases import Database

from app.models.occurrence import OccurrencePublic
from app.models.filter import Filter
from app.db.repositories.occurrence import OccurrenceRepository

# decorate all tests with @pytest.mark.asyncio
pytestmark = pytest.mark.asyncio  

class TestGetOccurrence:
    async def test_get_all_occurrences(
            self, 
            app: FastAPI, 
            authorized_client: AsyncClient,
            test_occurrence: OccurrencePublic
            ) -> None:
        res = await authorized_client.get(
            app.url_path_for('occurrence:get_all_occurrences')
        )
        assert res.status_code == HTTP_200_OK

class TestCreateOccurrenceFilter:
    async def test_can_create_empty_filter_download(
            self,
            app: FastAPI,
            db: Database,
            test_occurrence: OccurrencePublic,
            authorized_client: AsyncClient
            ) -> None:
        filter = Filter()
        previous_download = './occurrence_download/file_0.csv'
        if(os.path.exists(previous_download)):
            os.remove(previous_download)
        occurrence_repo = OccurrenceRepository(db)
        occurrences = await occurrence_repo.get_occurrences_by_filter(
            filter = filter)
        for rec in occurrences: 
            print(tuple(rec.values()))
        assert occurrences
        res = await authorized_client.post(
            app.url_path_for('occurrence:create_occurrence_download'),
            data = filter.json()
        )
        print(filter.json())
        id = res.json().get('download_id')
        print(id)
        path = './occurrence_download/' + f'file_{id}.csv'
        assert os.path.exists(path)
        res = await authorized_client.get(
            app.url_path_for(
                'occurrence:retrieve_download',
                download_id = id
            )
        )
        data = res.content
        df = pd.read_csv(io.StringIO(data.decode('utf-8')))
        assert not df.empty
        assert df.columns[0] == 'id'
    
    @pytest.mark.parametrize(
        'ex_classification_level, ex_classification_name, ex_year, \
            ex_startDate, ex_endDate, ex_location_name, ex_location_type, \
            status_code, returns',
            (
                ("Kingdom", "Animalia", 0, "", "", "", "", 201, True),
                ("", "Branta canadensis", 0, "", "", "", "", 201, True),
                ("Family", "Notafamily", 0, "", "", "", "", 201, False),
                ("NotaCLevel", "Animalia", 0, "", "", "","", 422, False),
                ("", "", 2015, "", "", "", "", 201, True),
                ("", "", 2007, "", "", "", "", 201, False),
                ("", "", 2015, "2007-10-15", "2007-10-16", "", "", 201, True),
                ("", "", 2007, "2015-05-20", "2015-05-22", "", "", 201, False),
                ("", "", 0, "NotaDate", "NotaDate", "", "", 422, False),
                ("", "", 0, "", "", "Canterbury Region", "region", 201, True),
                ("", "", 0, "", "", "Waikato Region", "region", 201, False),
                ("", "", 0, "", "", "Not a region", "notalocation", 422, False),
                ("Kingdom", "Animalia", 0, "2015-05-20", "2015-05-22", \
                    "Canterbury Region", "region", 201, True)
            )
        )
    
    async def test_filter_categories(
            self,
            app: FastAPI,
            authorized_client: AsyncClient,
            test_occurrence: OccurrencePublic,
            db: Database,
            ex_classification_level: str,
            ex_classification_name: str,
            ex_year: int,
            ex_startDate: str,
            ex_endDate: str,
            ex_location_name: str,
            ex_location_type: str,
            status_code: int,
            returns: bool,
            ) -> None:     
        previous_download = './occurrence_download/file_0.csv'
        if(os.path.exists(previous_download)):
            os.remove(previous_download)
        filter = Filter(
            classification_level = ex_classification_level,
            classification_name = ex_classification_name,
            year = ex_year,
            startDate = ex_startDate,
            endDate = ex_endDate,
            location_name = ex_location_name,
            location_type = ex_location_type
        )
        print(filter.json())
        occurrence_repo = OccurrenceRepository(db)
        occurrence = await occurrence_repo.get_all_occurrences()
        for rec in occurrence: 
            print(tuple(rec.values()))
        if(returns):
            occurrences = await occurrence_repo.get_occurrences_by_filter(
                filter = filter)
            for rec in occurrences: 
                print(tuple(rec.values()))
            assert occurrences
        new_filter = {
            "classification_level": ex_classification_level,
            "classification_name": ex_classification_name,
            "year": ex_year,
            "startDate": ex_startDate,
            "endDate": ex_endDate,
            "location_name": ex_location_name,
            "location_type": ex_location_type
        }
        print(json.dumps(new_filter))
        res = await authorized_client.post(
            app.url_path_for('occurrence:create_occurrence_download'),
            data = filter.json()
        )
        assert res.status_code == status_code    
        if status_code == 201:
            download_id = res.json().get('download_id')
            print(download_id)
            path = './occurrence_download/' + f'file_{download_id}.csv'
            assert os.path.exists(path)
            res = await authorized_client.get(
                app.url_path_for(
                    'occurrence:retrieve_download',
                    download_id = download_id
                )
            )
            content = res.content
            df = pd.read_csv(io.StringIO(content.decode('utf-8')))
            assert df.columns[0] == 'id'
            assert (not df.empty) is returns
            


        

