import os
import pandas as pd
from typing import List
from datetime import datetime

from app.db.repositories.base import BaseRepository
from app.models.filter import Filter


# Occurrence Repository Actions


# SQL Queries
GET_ALL_OCCURRENCES_QUERY = """
    SELECT * FROM main.occurrence
"""

GET_OCCURRENCES_BY_FILTER = """
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
	FROM main.occurrence, main.location, main.locationref
    WHERE main.occurrence.id = main.location.occurrence_id
	AND main.location.location_name = main.locationref.name"""

# Classification query builder
def buildClassificationQueryLine(classification_level: str):
    if classification_level == 'phylum':
        query = "        AND main.occurrence.occurrence_phylum ~* \
            :classification_name"
    if classification_level == 'kingdom':
        query = "        AND main.occurrence.occurrence_kingdom ~* \
            :classification_name"
    if classification_level == 'order':
        query = "        AND main.occurrence.occurrence_order ~* \
            :classification_name"
    if classification_level == 'class':
        query = "        AND main.occurrence.occurrence_class ~* \
            :classification_name"
    if classification_level == 'family':
        query = "        AND main.occurrence.occurrence_family ~* \
            :classification_name"
    if classification_level == 'genus':
        query = "        AND main.occurrence.occurrence_genus ~* \
            :classification_name"
    if classification_level == 'species':
        query = "        AND main.occurrence.occurrence_species ~* \
            :classification_name"
    return query

# Location Query Builder
def buildLocationQueryLine(location_name: str, location_type: str) :
    query = ""
    if(location_name):
        query += "        AND LOWER(main.location.location_name) = \
            LOWER(:location_name)"
    if(location_type):
        query += "        AND LOWER(main.locationref.locationtype) = \
            LOWER(:location_type)"
    return query

# Observation date query builder
def buildObservationDateQueryLine() :
    query = "        AND main.occurrence.observation_date >= :startDate AND \
        observation_date <= :endDate"
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

    # Creates download by filter given and returns download id
    async def get_occurrences_by_filter(self, filter: Filter):
        query = GET_OCCURRENCES_BY_FILTER
        args = {}
        # If no filter, returns all data
        if (not filter.classification_level 
                and not filter.classification_name 
                and not filter.startDate 
                and not filter.endDate 
                and (not filter.year or filter.year == 0)
                and not filter.location_name 
                and not filter.location_type):
            occurrences = await self.get_all_occurrences()
        # Build query based on filter
        else:
            if(filter.classification_level) and (filter.classification_name):
                classification_level = filter.classification_level.casefold()
                if(classification_level in ["phylum", "kingdom", "class", 
                        "order", "family", "genus", "species"]):
                    query += "\n"
                    query += buildClassificationQueryLine(classification_level)              
                    args["classification_name"] = filter.classification_name
            if(filter.year) and (filter.year != 0):
                filter.startDate = str(filter.year) + "-01-01"
                filter.endDate = str(filter.year) + "-12-31"              
            if(filter.startDate) and (filter.endDate):
                startDate = datetime.strptime(filter.startDate, '%Y-%m-%d')
                endDate = datetime.strptime(filter.endDate, '%Y-%m-%d')
                query += "\n"
                query += buildObservationDateQueryLine()
                args["startDate"] = startDate
                args["endDate"] = endDate
            if(filter.location_name):
                query += "\n"
                query += buildLocationQueryLine(filter.location_name, "")
                args["location_name"] = filter.location_name
            if(filter.location_type):
                query += "\n"
                query += buildLocationQueryLine("", filter.location_type)
                args["location_type"] = filter.location_type
            occurrences = await self.db.fetch_all(query, args)
        i = 0
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