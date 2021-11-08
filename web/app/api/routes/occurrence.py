from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException 
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from app.models.occurrence import OccurrencePublic, OccurrenceCreate
from app.db.repositories.occurrence import OccurrenceRepository  
from app.api.dependencies.database import get_repository 

router = APIRouter()

@router.get("/", name="occurrence:get_all_occurrences")
async def get_all_occurrences(occurrence_repo: OccurrenceRepository = Depends(get_repository(OccurrenceRepository))
) -> List[dict]:
    occurrences = await occurrence_repo.get_all_occurrences()
    if not occurrences:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No data found in occurrences.")
    return occurrences

@router.post("/", response_model=OccurrencePublic, name="occurrence:create_occurrence", status_code=HTTP_201_CREATED)
async def create_new_occurrence(
    new_occurrence: OccurrenceCreate = Body(...),
    occurrence_repo: OccurrenceRepository = Depends(get_repository(OccurrenceRepository)),
) -> OccurrencePublic:
    created_occurrence = await occurrence_repo.create_occurrence(new_occurrence=new_occurrence)
    return created_occurrence