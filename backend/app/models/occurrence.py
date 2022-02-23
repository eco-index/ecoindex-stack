from typing import Optional
import datetime

from app.models.core import IDModelMixin, CoreModel

class OccurrenceBase(CoreModel):
    """
    All common characteristics of occurrences
    """
    scientific_name: str
    observation_count: Optional [int]
    observation_date: datetime.date
    occurrence_latitude: Optional[float]
    occurrence_longitude: Optional[float]
    occurrence_elevation: Optional[float]
    occurrence_depth: Optional[float]
    taxon_rank: str
    infraspecific_epithet: Optional[str] 
    occurrence_species: Optional[str]
    occurrence_genus: Optional[str]
    occurrence_family: Optional[str]
    occurrence_order: Optional[str]
    occurrence_class: Optional[str]
    occurrence_phylum: Optional[str]
    occurrence_kingdom: Optional[str]

class OccurrenceCreate(OccurrenceBase):
    pass

class OccurrencePublic(IDModelMixin, OccurrenceBase):
    id: int

class OccurrenceJson(OccurrenceBase):
    observation_date: str