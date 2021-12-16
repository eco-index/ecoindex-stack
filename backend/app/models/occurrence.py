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
    latitude: Optional[float] = 1.0
    longitude: Optional[float] = 1.0
    elevation: Optional[float] = 1.0
    depth: Optional[float] = 1.0
    taxon_rank: str
    infraspecific_epithet: Optional[str] = 'fish'
    species: Optional[str] = 'fish'
    genus: Optional[str] = 'fish'
    family: Optional[str] = 'fish'
    order: Optional[str] = 'fish'
    occurrence_class: Optional[str] = 'fish'
    phylum: Optional[str] = 'fish'
    kingdom: Optional[str] = 'fish'

class OccurrenceCreate(OccurrenceBase):
    pass

class OccurrencePublic(IDModelMixin, OccurrenceBase):
    id: int

class OccurrenceJson(OccurrenceBase):
    observation_date: str