from app.db.repositories.base import BaseRepository
from app.models.occurrence import OccurrencePublic, OccurrenceCreate

CREATE_OCCURRENCE_QUERY = """
    INSERT INTO main.occurrence (scientific_name, observation_count, observation_date, taxon_rank)
    VALUES (:scientific_name, :observation_count, :observation_date, :taxon_rank)
    RETURNING id, scientific_name, observation_count, observation_date, taxon_rank;
"""

GET_ALL_OCCURRENCES_QUERY = """
    SELECT *
    FROM main.occurrence
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

    async def get_all_occurrences(self) -> OccurrencePublic:    
        occurrence = await self.db.fetch_all(query=GET_ALL_OCCURRENCES_QUERY)
        if not occurrence:
            return None
        return OccurrencePublic(occurrence)

    # async def get_cleaning_by_id(self, *, id: int) -> CleaningInDB:
    #     cleaning = await self.db.fetch_one(query=GET_CLEANING_BY_ID_QUERY, values={"id": id})
    #     if not cleaning:
    #         return None
    #     return CleaningInDB(**cleaning)
