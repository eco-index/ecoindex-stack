from typing import Optional
import datetime

from app.models.core import IDModelMixin, CoreModel

class MCIBase(CoreModel):
    """
    All common characteristics of occurrences
    """
    value: float
    indicator: str
    observation_date: datetime.date
    occurrence_latitude: Optional[float]
    occurrence_longitude: Optional[float]
    river_catchment: Optional[str]
    landcover_type: Optional[str]


class MCICreate(MCIBase):
    pass

class MCIPublic(IDModelMixin, MCIBase):
    id: int

class MCIJson(MCIBase):
    observation_date: str