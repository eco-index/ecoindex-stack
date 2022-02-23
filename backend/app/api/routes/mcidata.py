from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import StreamingResponse
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
import os

from app.db.repositories.mci import MCIRepository  
from app.api.dependencies.database import get_repository 
from app.models.security import UserInDB
from app.api.dependencies.auth import get_current_active_user
from app.models.filter import MCIFilter

router = APIRouter()

@router.get("/", name="mcidata:get_all_mci_data")
async def get_all_mci_data(
    mci_repo: MCIRepository = Depends(get_repository(MCIRepository)),
    current_user: UserInDB = Depends(get_current_active_user),
) -> List[dict]:
    if current_user.role == "GUEST":
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authorized to retrieve data."
        )
    mcidata = await mci_repo.get_all_data()
    if not mcidata:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No data found for MCI.")
    return mcidata

@router.post("/", name="mcidata:create_mci_download", status_code=HTTP_201_CREATED)
async def create_mci_download(
    filter: MCIFilter = Body(...),
    mci_repo: MCIRepository = Depends(get_repository(MCIRepository)),
    current_user: UserInDB = Depends(get_current_active_user),
):
    if current_user.role == "GUEST":
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authorized to create data download."
        )
    res = await mci_repo.get_data_by_filter(filter)
    payload = {
        "download_id" : res
    }
    return payload

@router.get("/download/{download_id}", name="mcidata:retrieve_mci_download")
async def get_download_by_id(
    download_id: int,
    current_user: UserInDB = Depends(get_current_active_user)
):
    if current_user.role == "GUEST":
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authorized to retrieve downloads."
        )

    path = "./mci_download/" + f"file_{download_id}.csv"
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

        
