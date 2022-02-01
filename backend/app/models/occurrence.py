from typing import Optional
import datetime

from app.models.core import IDModelMixin, CoreModel

class OccurrenceBase(CoreModel):
    """
    All common characteristics of occurrences
    """
    scientific_name: str
    observation_count: Optional [int] = 1
    observation_date: datetime.date
    occurrence_latitude: Optional[float] = 1.0
    occurrence_longitude: Optional[float] = 1.0
    occurrence_elevation: Optional[float] = 1.0
    occurrence_depth: Optional[float] = 1.0
    taxon_rank: str
    infraspecific_epithet: Optional[str] = 'fish'
    occurrence_species: Optional[str] = 'fish'
    occurrence_genus: Optional[str] = 'fish'
    occurrence_family: Optional[str] = 'fish'
    occurrence_order: Optional[str] = 'fish'
    occurrence_class: Optional[str] = 'fish'
    occurrence_phylum: Optional[str] = 'fish'
    occurrence_kingdom: Optional[str] = 'fish'

class OccurrenceCreate(OccurrenceBase):
    pass

class OccurrencePublic(IDModelMixin, OccurrenceBase):
    id: int

class OccurrenceJson(OccurrenceBase):
    observation_date: str