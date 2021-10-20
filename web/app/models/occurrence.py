from typing import Optional
from enum import Enum
import datetime

from app.models.core import IDModelMixin, CoreModel

# class CleaningType(str, Enum):
#     dust_up = "dust_up"
#     spot_clean = "spot_clean"
#     full_clean = "full_clean"

class OccurrenceBase(CoreModel):
    """
    All common characteristics of occurrences
    """
    scientific_name: str
    observation_count: int
    observation_date: datetime.date
    latitude: Optional[float]
    longitude: Optional[float]
    elevation: Optional[float]
    depth: Optional[float]
    taxon_rank: str
    infraspecific_epithet: Optional[str]
    species: Optional[str]
    genus: Optional[str]
    family: Optional[str]
    order: Optional[str]
    occurrence_class: Optional[str]
    phylum: Optional[str]
    kingdom: Optional[str]

class OccurrenceCreate(OccurrenceBase):
    pass

class OccurrencePublic(IDModelMixin, OccurrenceBase):
    pass