from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException 
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

from app.models.occurrence import OccurrencePublic, OccurrenceCreate
from app.db.repositories.occurrence import OccurrenceRepository  
from app.api.dependencies.database import get_repository 
from app.models.security import UserInDB
from app.api.dependencies.auth import get_current_active_user
from app.models.role import Role

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

@router.post("/", response_model=OccurrencePublic, name="occurrence:create_occurrence", status_code=HTTP_201_CREATED)
async def create_new_occurrence(
    new_occurrence: OccurrenceCreate = Body(...),
    occurrence_repo: OccurrenceRepository = Depends(get_repository(OccurrenceRepository)),
    current_user: UserInDB = Depends(get_current_active_user),
) -> OccurrencePublic:
    if current_user.role == "GUEST":
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authorized to create occurrences."
        )
    created_occurrence = await occurrence_repo.create_occurrence(new_occurrence=new_occurrence)
    return created_occurrence