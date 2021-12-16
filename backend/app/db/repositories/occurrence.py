from app.db.repositories.base import BaseRepository
from app.models.filter import Filter
from typing import List
import pandas as pd
import os
from datetime import datetime


GET_ALL_OCCURRENCES_QUERY = """
    SELECT * FROM main.occurrence
"""

GET_OCCURRENCES_BY_FILTER = """
    SELECT * FROM main.occurrence 
    JOIN main.location
        ON main.occurrence.id = main.location.occurrence_id
    JOIN main.locationref
        ON main.location.location_name = main.locationref.name
    WHERE"""

def buildClassificationQueryLine(num_query: int):
    if(num_query):
        query = "        AND :classification_level = :classification_name"
    else:
        query = "        :classification_level = :classification_name"
    return query

def buildLocationQueryLine(location_name: str, location_type: str, num_query: int) :
    if(num_query):
        query = "        AND "
    else:
        query = "        "
    if(location_name):
        query += "main.location.location_name = :location_name"
    if(location_type):
        query += "main.locationref.locationtype = :location_type"
    return query

def buildObservationDateQueryLine(num_query) :
    if(num_query):
        query = "        AND observation_date >= :startDate AND observation_date <= :endDate"
    else:
        query = "        observation_date >= :startDate AND observation_date <= :endDate"
    return query

class OccurrenceRepository(BaseRepository):
    """"
    All database actions associated with the Occurrence Table
    """
    async def get_all_occurrences(self) -> List[dict]:    
        occurrences = await self.db.fetch_all(query=GET_ALL_OCCURRENCES_QUERY)
        if not occurrences:
            return None
        return occurrences

    async def get_occurrences_by_filter(self, filter: Filter):
        query = GET_OCCURRENCES_BY_FILTER
        numquery = 0
        args = {}
        if(filter.classification_level) and (filter.classification_name):
            if(filter.classification_level in ["phylum", "kingdom", "class", "order", "family", "genus", "species"]):
                query += "\n"
                query += buildClassificationQueryLine(numquery)
                args["classification_level"] = filter.classification_level
                numquery = numquery + 1
        if(filter.year) or ((filter.startDate) and (filter.endDate)):
            if (filter.year):
                filter.startDate = str(filter.year) + "-01-01"
                filter.endDate = str(filter.year) + "-12-31"
            startDate = datetime.strptime(filter.startDate, '%Y-%m-%d')
            endDate = datetime.strptime(filter.endDate, '%Y-%m-%d')
            query += "\n"
            query += buildObservationDateQueryLine(numquery)
            args["startDate"] = startDate
            args["endDate"] = endDate
            numquery = numquery + 1
        if(filter.location_name):
            query += "\n"
            query += buildLocationQueryLine(filter.location_name, "", numquery)
            args["location_name"] = filter.location_name
            numquery = numquery + 1
        if(filter.location_type):
            query += "\n"
            query += buildLocationQueryLine("", filter.location_type, numquery)
            args["location_type"] = filter.location_type
            numquery = numquery + 1
        occurrences = await self.db.fetch_all(query, args)
        i = 0
        path = "./occurrence_download/"
        while os.path.exists(path + f"file_{i}.csv"):  
            i += 1
        path = path + f"file_{i}.csv"
        download = pd.DataFrame(occurrences)
        download.to_csv(path)
        return i
    
    # async def get_occurrences_by_year(self, *, year: int):
    #     startdate = year + "-01-01"
    #     endDate = year + "-12-31"
    #     query_values = {
    #         startdate,
    #         endDate
    #     }
    #     occurrences = await self.db.fetch_all(query=GET_OCCURRENCES_BY_DATE_RANGE, values=query_values)
    #     return occurrences
    
    # async def get_occurrences_by_date_range(self, *, startDate: str, endDate: str):
    #     query_values = {
    #         startDate,
    #         endDate
    #     }
    #     occurrences = await self.db.fetch_all(query=GET_OCCURRENCES_BY_DATE_RANGE, values=query_values)
    #     return occurrences
    
    # async def get_occurrences_by_classification(self, *, classification_level: str, classification_name: str):
    #     query = buildClassificationQueryLine(classification_level, classification_name)
    #     occurrences = await self.db.fetch_all(query=query)
    #     return occurrences