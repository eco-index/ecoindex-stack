from app.db.repositories.base import BaseRepository
from app.models.occurrence import OccurrencePublic, OccurrenceCreate
from fastapi.logger import logger
from typing import List



CREATE_OCCURRENCE_QUERY = """
    INSERT INTO main.occurrence (scientific_name, observation_count, observation_date, occurrence_latitude, occurrence_longitude, occurrence_elevation, occurrence_depth, taxon_rank, infraspecific_epithet, occurrence_species, occurrence_genus, occurrence_family, occurrence_order, occurrence_class, occurrence_phylum, occurrence_kingdom)
    VALUES (:scientific_name, :observation_count, :observation_date, :latitude, :longitude, :elevation, :depth, :taxon_rank, :infraspecific_epithet, :species, :genus, :family, :order, :occurrence_class, :phylum, :kingdom)
    RETURNING id, scientific_name, observation_count, observation_date, occurrence_latitude, occurrence_longitude, occurrence_elevation, occurrence_depth, taxon_rank, infraspecific_epithet, occurrence_species, occurrence_genus, occurrence_family, occurrence_order, occurrence_class, occurrence_phylum, occurrence_kingdom;
"""

GET_ALL_OCCURRENCES_QUERY = """
    SELECT * FROM main.occurrence
"""

# GET_CLEANING_BY_ID_QUERY = """
#     SELECT id, name, description, price, cleaning_type
#     FROM cleanings
#     WHERE id = :id;
# """

class OccurrenceRepository(BaseRepository):
    """"
    All database actions associated with the Occurrence Table
    """
    async def create_occurrence(self, *, new_occurrence: OccurrenceCreate) -> OccurrencePublic:
        query_values = new_occurrence.dict()
        occurrence = await self.db.fetch_one(query=CREATE_OCCURRENCE_QUERY, values=query_values)
        return OccurrencePublic(**occurrence)

    async def get_all_occurrences(self) -> List[dict]:    
        occurrences = await self.db.fetch_all(query=GET_ALL_OCCURRENCES_QUERY)
        if not occurrences:
            return None
        return occurrences


    # async def get_cleaning_by_id(self, *, id: int) -> CleaningInDB:
    #     cleaning = await self.db.fetch_one(query=GET_CLEANING_BY_ID_QUERY, values={"id": id})
    #     if not cleaning:
    #         return None
    #     return CleaningInDB(**cleaning)
