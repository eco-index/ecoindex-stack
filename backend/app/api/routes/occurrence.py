from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import StreamingResponse
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
import os

from app.models.occurrence import OccurrencePublic
from app.db.repositories.occurrence import OccurrenceRepository  
from app.api.dependencies.database import get_repository 
from app.models.security import UserInDB
from app.api.dependencies.auth import get_current_active_user
from app.models.filter import Filter

router = APIRouter()

@router.get("/", name="occurrence:get_all_occurrences")
async def get_all_occurrences(
    occurrence_repo: OccurrenceRepository = Depends(get_repository(OccurrenceRepository)),
    current_user: UserInDB = Depends(get_current_active_user),
) -> List[dict]:
    if current_user.role == "GUEST":
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authorized to retrieve occurrences."
        )
    occurrences = await occurrence_repo.get_all_occurrences()
    if not occurrences:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No data found in occurrences.")
    return occurrences

@router.post("/", name="occurrence:create_occurrence_download", status_code=HTTP_201_CREATED)
async def create_occurrence_download(
    filter: Filter = Body(...),
    occurrence_repo: OccurrenceRepository = Depends(get_repository(OccurrenceRepository)),
    current_user: UserInDB = Depends(get_current_active_user),
) -> OccurrencePublic:
    if current_user.role == "GUEST":
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authorized to create occurrences."
        )
    res = await occurrence_repo.get_occurrences_by_filter(filter)
    payload = {
        "download_id" : res
    }
    return payload

@router.get("/download/{download_id}", name="occurrence:retrieve_download")
async def get_download_by_id(
    download_id: int,
    current_user: UserInDB = Depends(get_current_active_user)
):
    if current_user.role == "GUEST":
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authorized to retrieve downloads."
        )

    path = "./occurrence_download/" + f"file_{download_id}.csv"
    if not os.path.exists(path):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No download of this id found"
        )
    def datafile():
        with open(path, mode="rb") as file:
            yield from file
    response = StreamingResponse(datafile(), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    return response

        
