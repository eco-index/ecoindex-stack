from app.db.repositories.base import BaseRepository
from app.models.filter import MCIFilter
from typing import List
import pandas as pd
import os
from datetime import datetime


GET_ALL_DATA_QUERY = """
    SELECT * FROM main.mci
"""

GET_DATA_BY_FILTER = """
    SELECT main.mci.id, main.mci.value, main.mci.indicator, main.mci.observation_date, main.mci.occurrence_latitude, main.mci.occurrence_longitude, main.mci.river_catchment, main.mci.landcover_type, main.mci.created_at, main.mci.updated_at
	FROM main.mci, main.mci_location, main.locationref
    WHERE main.mci.id = main.mci_location.mci_id
	AND main.mci_location.location_name = main.locationref.name"""

def buildLocationQueryLine(location_name: str, location_type: str) :
    query = "        AND "
    if(location_name):
        query += "main.mci_location.location_name = :location_name"
    if(location_type):
        query += "main.locationref.locationtype = :location_type"
    return query

def buildObservationDateQueryLine() :
    query = "        AND main.mci.observation_date >= :startDate AND main.mci.observation_date <= :endDate"
    return query

class MCIRepository(BaseRepository):
    """"
    All database actions associated with the Occurrence Table
    """
    async def get_all_data(self) -> List[dict]:    
        data = await self.db.fetch_all(query=GET_ALL_DATA_QUERY)
        if not data:
            return None
        return data

    async def get_data_by_filter(self, filter: MCIFilter):
        query = GET_DATA_BY_FILTER
        args = {}
        if not filter.startValue and not filter.endValue and not filter.indicator and not filter.startDate and not filter.endDate and (not filter.year or filter.year == 0)and not filter.location_name and not filter.location_type and not filter.landcover_type and not filter.river_catchment:
            mcidata = await self.get_all_data()
        else:
            if(filter.startValue) and (filter.endValue):
                query += "\n"
                query += "        AND main.mci.value >= :startValue AND main.mci.value <= :endValue"
                args["startValue"] = filter.startValue
                args["endValue"] = filter.endValue
            if(filter.indicator):
                query += "\n"
                query += "        AND LOWER(main.mci.indicator) = LOWER(:indicator)"
                args["indicator"] = filter.indicator
            if(filter.river_catchment):
                query += "\n"
                query += "        AND main.mci.river_catchment ~* :river_catchment"
                args["river_catchment"] = filter.river_catchment
            if(filter.landcover_type):
                query += "\n"
                query += "        AND main.mci.landcover_type ~* :landcover_type"
                args["landcover_type"] = filter.landcover_type
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
            mcidata = await self.db.fetch_all(query, args)
        i = 0
        path = "./mci_download/"
        while os.path.exists(path + f"file_{i}.csv"):  
            i += 1
        path = path + f"file_{i}.csv"
        download = pd.DataFrame(mcidata, columns=["id", "value", "indicator", "observation_date", "occurrence_latitude", "occurrence_longitude", "river_catchment", "landcover_type", "created_at", "updated_at"])
        download.to_csv(path, index=False)
        return i
    