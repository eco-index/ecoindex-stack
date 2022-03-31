import os
import pandas as pd
from typing import List
from datetime import datetime

from fastapi import HTTPException
from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY
)

from app.db.repositories.base import BaseRepository
from app.models.filter import Filter
from app.models.occurrence import OccurrenceCreate, OccurrencePublic


# Occurrence Repository Actions


# SQL Queries
GET_ALL_OCCURRENCES_QUERY = """
    SELECT * FROM main.occurrence
"""

GET_OCCURRENCES_BY_FILTER_QUERY = """
    SELECT main.occurrence.id, main.occurrence.scientific_name, \
        main.occurrence.observation_count, main.occurrence.observation_date, \
        main.occurrence.occurrence_latitude, \
        main.occurrence.occurrence_longitude, \
        main.occurrence.occurrence_elevation, \
        main.occurrence.occurrence_depth, main.occurrence.taxon_rank, \
        main.occurrence.infraspecific_epithet, \
        main.occurrence.occurrence_species, main.occurrence.occurrence_genus, \
        main.occurrence.occurrence_family, main.occurrence.occurrence_order, \
        main.occurrence.occurrence_class, main.occurrence.occurrence_phylum, \
        main.occurrence.occurrence_kingdom, main.occurrence.created_at, \
        main.occurrence.updated_at
	FROM main.occurrence 
    LEFT JOIN main.location ON main.occurrence.id = main.location.occurrence_id
    LEFT JOIN main.locationref ON main.location.location_name = \
        main.locationref.name"""

INSERT_OCCURRENCE_QUERY = """
    INSERT INTO main.occurrence (scientific_name, observation_count, \
        observation_date, occurrence_latitude, occurrence_longitude, 
        occurrence_elevation, occurrence_depth, taxon_rank, \
        infraspecific_epithet, occurrence_species, occurrence_genus, \
        occurrence_family, occurrence_order, occurrence_class, \
        occurrence_phylum, occurrence_kingdom)
    VALUES (:scientific_name, :observation_count, :observation_date, \
        :occurrence_latitude, :occurrence_longitude, :occurrence_elevation, \
        :occurrence_depth, :taxon_rank, :infraspecific_epithet, \
        :occurrence_species, :occurrence_genus, :occurrence_family, \
        :occurrence_order, :occurrence_class, :occurrence_phylum, \
        :occurrence_kingdom)
    RETURNING id, scientific_name, observation_count, observation_date, \
        occurrence_latitude, occurrence_longitude, occurrence_elevation, \
        occurrence_depth, taxon_rank, infraspecific_epithet,\
        occurrence_species, occurrence_genus, occurrence_family, \
        occurrence_order, occurrence_class, occurrence_phylum\
        occurrence_kingdom, created_at, updated_at

"""

GET_OCCURRENCE_BY_ID = """
    SELECT id, scientific_name, observation_count, observation_date, \
        occurrence_latitude, occurrence_longitude, occurrence_elevation, \
        occurrence_depth, taxon_rank, infraspecific_epithet,\
        occurrence_species, occurrence_genus, occurrence_family, \
        occurrence_order, occurrence_class, occurrence_phylum\
        occurrence_kingdom, created_at, updated_at
    FROM main.occurrence
    WHERE id = :id
"""

ADD_LOCATION_QUERY = """
    INSERT INTO main.locationref (name, polygon, locationtype)
    VALUES (:name, :polygon, :locationtype)
    RETURNING name
"""

RETRIEVE_LOCATION_QUERY = """
    SELECT name FROM main.locationref WHERE name = :name
"""

# Classification query builder
def buildClassificationQueryLine(classification_level: str, first: bool):
    if(first):
        query = "        WHERE"
    else:
        query = "        AND"
    if classification_level == 'phylum':
        query += " main.occurrence.occurrence_phylum ~* \
            :classification_name"
    if classification_level == 'kingdom':
        query += " main.occurrence.occurrence_kingdom ~* \
            :classification_name"
    if classification_level == 'order':
        query += " main.occurrence.occurrence_order ~* \
            :classification_name"
    if classification_level == 'class':
        query += " main.occurrence.occurrence_class ~* \
            :classification_name"
    if classification_level == 'family':
        query += " main.occurrence.occurrence_family ~* \
            :classification_name"
    if classification_level == 'genus':
        query += " main.occurrence.occurrence_genus ~* \
            :classification_name"
    if classification_level == 'species':
        query += " main.occurrence.occurrence_species ~* \
            :classification_name"
    if not classification_level:
        query += " main.occurrence.scientific_name ~* \
            :classification_name"
    return query

# Location Query Builder
def buildLocationQueryLine(location_name: str, location_type: str, first: bool):
    if(first):
        query = "        WHERE"
    else:
        query = "        AND"
    if(location_name):
        query += " LOWER(main.location.location_name) = \
            LOWER(:location_name)"
    if(location_type):
        query += " LOWER(main.locationref.locationtype) = \
            LOWER(:location_type)"
    return query

# Observation date query builder
def buildObservationDateQueryLine(first: bool):
    if(first):
        query = "        WHERE"
    else:
        query = "        AND"
    query += " main.occurrence.observation_date >= :startDate AND \
        main.occurrence.observation_date <= :endDate"
    return query


class OccurrenceRepository(BaseRepository):
    """"
    All database actions associated with the Occurrence Table
    """
    # Returns all data
    async def get_all_occurrences(self) -> List[dict]:    
        occurrences = await self.db.fetch_all(query=GET_ALL_OCCURRENCES_QUERY)
        if not occurrences:
            return None
        return occurrences
    
    # Creates Occurrence for Testing Purposes
    async def create_occurrence(self, occurrence: OccurrenceCreate
            ) -> OccurrencePublic:
        occurrence = await self.db.fetch_one(
            query = INSERT_OCCURRENCE_QUERY,
            values = occurrence.dict()
        )
        return OccurrencePublic(**occurrence)
    
    # Checks for occurrence by id for Testing Purposes
    async def get_occurrence_by_id(self, id: int) -> OccurrencePublic:
        occurrence = await self.db.fetch_one(
            query = GET_OCCURRENCE_BY_ID,
            values = { 'id' : id }
        )
        return occurrence

    # Creates download by filter given and returns download id
    async def get_occurrences_by_filter(self, filter: Filter) -> List[dict]:
        query = GET_OCCURRENCES_BY_FILTER_QUERY
        args = {}
        first = True
        # If no filter, returns all data
        if ((not filter.classification_level)
                and (not filter.classification_name)
                and (not filter.startDate)
                and (not filter.endDate)
                and ((not filter.year) or (filter.year == 0))
                and (not filter.location_name)
                and (not filter.location_type)):
            occurrences = await self.get_all_occurrences()
        # Build query based on filter
        else:
            if(filter.classification_name):
                if(filter.classification_level):
                    classification_level = filter.classification_level.casefold()
                    if(classification_level not in ["phylum", "kingdom", "class", 
                            "order", "family", "genus", "species"]):
                        raise HTTPException(
                            status_code = HTTP_422_UNPROCESSABLE_ENTITY,
                            detail = "Not a valid classification level"
                        )
                    else:
                        query += "\n"
                        query += buildClassificationQueryLine(
                            classification_level = classification_level,
                            first = first)              
                        args["classification_name"] = filter.classification_name
                        first = False
                else:
                    query += "\n"
                    query += buildClassificationQueryLine(
                        classification_level = filter.classification_level,
                        first = first)              
                    args["classification_name"] = filter.classification_name
                    first = False
            if(filter.year) and (filter.year != 0):
                filter.startDate = str(filter.year) + "-01-01"
                filter.endDate = str(filter.year) + "-12-31"              
            if(filter.startDate) and (filter.endDate):
                try:
                    startDate = datetime.strptime(filter.startDate, '%Y-%m-%d')
                    endDate = datetime.strptime(filter.endDate, '%Y-%m-%d')
                except ValueError:
                    raise HTTPException(
                        status_code = HTTP_422_UNPROCESSABLE_ENTITY,
                        detail = "Not a valid date format"
                    )
                query += "\n"
                query += buildObservationDateQueryLine(first = first)
                args["startDate"] = startDate
                args["endDate"] = endDate
                first = False
            if(filter.location_name):
                query += "\n"
                query += buildLocationQueryLine(
                    location_name = filter.location_name, 
                    location_type = "",
                    first = first)
                args["location_name"] = filter.location_name
                first = False
            if(filter.location_type):
                location_type = filter.location_type.casefold()
                if(location_type not in ["region", "rohe"]):
                    raise HTTPException(
                        status_code = HTTP_422_UNPROCESSABLE_ENTITY,
                        detail = "Not a valid location type"
                    )
                else:
                    query += "\n"
                    query += buildLocationQueryLine(
                        location_name = "", 
                        location_type = location_type,
                        first = first)
                    args["location_type"] = location_type
                    first = False
            occurrences = await self.db.fetch_all(query, args)
        return occurrences

    # Create filtered download file
    async def create_filtered_download(self, filter: Filter):
        i = 0
        occurrences = await self.get_occurrences_by_filter(filter = filter)
        # Finds latest download number
        path = "./occurrence_download/"
        while os.path.exists(path + f"file_{i}.csv"):  
            i += 1
        path = path + f"file_{i}.csv"
        # Saves download file
        download = pd.DataFrame(occurrences, columns=[
            "id", 
            "scientific_name", 
            "observation_count", 
            "observation_date", 
            "occurrence_latitude", 
            "occurrence_longitude", 
            "occurrence_elevation", 
            "occurrence_depth", 
            "taxon_rank", 
            "infraspecific_epithet", 
            "occurrence_species", 
            "occurrence_genus", 
            "occurrence_family", 
            "occurrence_order", 
            "occurrence_class", 
            "occurrence_phylum", 
            "occurrence_kingdom", 
            "created_at", 
            "updated_at"])
        download.to_csv(path, index=False)
        # Returns download id
        return i
    
    async def add_location(self, name: str, polygon: str, location_type: str):
        location_exists = await self.db.fetch_one(
            query = RETRIEVE_LOCATION_QUERY,
            values = {
                'name': name
            }
        )
        if not location_exists:
            args = {
                'name' : name,
                'polygon' : polygon,
                'locationtype' : location_type
            }
            location = await self.db.fetch_one(
                query = ADD_LOCATION_QUERY,
                values = args
            )
            return location
        else:
            return None
        
        