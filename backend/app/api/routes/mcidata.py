import os
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import StreamingResponse
from starlette.status import (
    HTTP_201_CREATED, 
    HTTP_404_NOT_FOUND
)

from app.db.repositories.mci import MCIRepository  
from app.models.security import UserInDB
from app.api.dependencies.database import get_repository 
from app.api.dependencies.auth import (
    get_current_active_user,
    check_user_authorised
)
from app.models.filter import MCIFilter


# MCI API Router

router = APIRouter()


# GET method, returns all MCI data if MCI data exists
@router.get("/", name = "mcidata:get_all_mci_data")
async def get_all_mci_data(
        mci_repo: MCIRepository = Depends(get_repository(MCIRepository)),
        current_user: UserInDB = Depends(get_current_active_user),
        ) -> List[dict]:
    # Checks if authorised role
    check_user_authorised(
        current_user = current_user,
        detail = "Not authorised to retrieve data"
        )
    # Retrieves data
    mcidata = await mci_repo.get_all_data()
    # If no data exists, returns error
    if not mcidata:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, 
            detail="No data found for MCI."
        )
    return mcidata


# POST method, will create a download based on a filter sent through
@router.post("/", name = "mcidata:create_mci_download", 
             status_code = HTTP_201_CREATED)
async def create_mci_download(
        filter: MCIFilter = Body(...),
        mci_repo: MCIRepository = Depends(get_repository(MCIRepository)),
        current_user: UserInDB = Depends(get_current_active_user),
        ):
    # Checks if authorised role
    check_user_authorised(
        current_user = current_user,
        detail = "Not authorized to create data download."
        )
    # Create data download based on filter and retrieve id
    id = await mci_repo.get_data_by_filter(filter)
    # Returns download id
    payload = {
        "download_id" : id
    }
    return payload


# GET method, will retrieve download based on id if authorised
@router.get("/download/{download_id}", name = "mcidata:retrieve_mci_download")
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
    path = "./mci_download/" + f"file_{download_id}.csv"
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

        
