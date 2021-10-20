from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException 
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from app.models.occurrence import OccurrencePublic, OccurrenceCreate
from app.db.repositories.occurrence import OccurrenceRepository  
from app.api.dependencies.database import get_repository 

router = APIRouter()

@router.get("/")
async def get_all_occurrences(
    occurrence_repo: OccurrenceRepository = Depends(get_repository(OccurrenceRepository))
) -> OccurrencePublic:
    occurrence = await occurrence_repo.get_all_occurrences()
    if not occurrence:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No data found in occurrences.")
    return occurrence

# @router.get("/{id}/", response_model=OccurrencePublic, name="cleanings:get-cleaning-by-id")
# async def get_cleaning_by_id(
#   id: int, cleanings_repo: OccurrenceRepository = Depends(get_repository(OccurrenceRepository))
# ) -> OccurrencePublic:
#     cleaning = await cleanings_repo.get_cleaning_by_id(id=id)
#     if not cleaning:
#         raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No cleaning found with that id.")
#     return cleaning

@router.post("/", response_model=OccurrencePublic, name="occurrence:create_occurrence", status_code=HTTP_201_CREATED)
async def create_new_occurrence(
    new_occurrence: OccurrenceCreate = Body(..., embed=True),
    occurrence_repo: OccurrenceRepository = Depends(get_repository(OccurrenceRepository)),
) -> OccurrencePublic:
    created_occurrence = await occurrence_repo.create_occurrence(new_occurrence=new_occurrence)
    return created_occurrence