from fastapi import APIRouter

from app.api.routes.occurrence import router as occurrence_router
from app.api.routes.users import router as users_router
from app.api.routes.mcidata import router as mci_router


router = APIRouter()


router.include_router(occurrence_router, prefix = "/occurrence", 
                      tags = ["occurrence"])
router.include_router(users_router, prefix = "/users", tags = ["users"])
router.include_router(mci_router, prefix = "/mci", tags = ["mci"])

