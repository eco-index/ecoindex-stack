import os
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import StreamingResponse
from starlette.status import (
    HTTP_201_CREATED, 
    HTTP_404_NOT_FOUND
)

from app.db.repositories.occurrence import OccurrenceRepository  
from app.models.security import UserInDB
from app.api.dependencies.database import get_repository 
from app.api.dependencies.auth import (
    get_current_active_user,
    check_user_authorised
)
from app.models.filter import Filter


# Occurrence API Router 

router = APIRouter()


# GET method, returns all occurrence data if authorised and data exists
@router.get("/", name = "occurrence:get_all_occurrences")
async def get_all_occurrences(
        occurrence_repo: OccurrenceRepository = 
            Depends(get_repository(OccurrenceRepository)),
        current_user: UserInDB = Depends(get_current_active_user),
        ) -> List[dict]:
    # Checks if authorised role
    check_user_authorised(
        current_user = current_user,
        detail = "Not authorised to retrieve data"
        )
    # Retrieves data
    occurrences = await occurrence_repo.get_all_occurrences()
    # If no data exists, returns error
    if not occurrences:
        raise HTTPException(
            status_code = HTTP_404_NOT_FOUND, 
            detail = "No data found in occurrences."
        )
    return occurrences


# POST method, will create download based on filter sent through
@router.post("/", name = "occurrence:create_occurrence_download", 
             status_code = HTTP_201_CREATED)
async def create_occurrence_download(
        filter: Filter = Body(...),
        occurrence_repo: OccurrenceRepository = 
            Depends(get_repository(OccurrenceRepository)),
        current_user: UserInDB = Depends(get_current_active_user),
        ):
    # Checks if authorised role
    check_user_authorised(
        current_user = current_user,
        detail = "Not authorized to create data download."
        )
    # Create data download based on filter and retrieve id
    id = await occurrence_repo.get_occurrences_by_filter(filter)
    # Returns download id
    payload = {
        "download_id" : id
    }
    return payload


# GET method, will retrieve downlaod based on id if authorised
@router.get("/download/{download_id}", name = "occurrence:retrieve_download")
async def get_download_by_id(
        download_id: int,
        current_user: UserInDB = Depends(get_current_active_user)
        ):
    # Checks if authorised role
    check_user_authorised(
        current_user = current_user,
        detail = "Not authorized to retrieve downloads."
        )
    # Retrieves download file from filepath
    path = "./occurrence_download/" + f"file_{download_id}.csv"
    if not os.path.exists(path):
        raise HTTPException(
            status_code = HTTP_404_NOT_FOUND,
            detail = "No download of this id found"
        )
    # Returns download file in csv format
    def datafile():
        with open(path, mode = "rb") as file:
            yield from file
    response = StreamingResponse(datafile(), media_type = "text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    return response

        
