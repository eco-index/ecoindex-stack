from fastapi import APIRouter
from app.api.routes.occurrence import router as occurrence_router

router = APIRouter()

router.include_router(occurrence_router, prefix="/occurrence", tags=["occurrence"])
