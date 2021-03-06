import os  
import logging 

from fastapi import FastAPI
from databases import Database

from app.core.config import TEST_DATABASE_URL, DATABASE_URL

logger = logging.getLogger(__name__)

async def connect_to_db(app: FastAPI) -> None:
    DB_URL =  TEST_DATABASE_URL if os.environ.get("TESTING") else DATABASE_URL
    # these can be configured in config as well
    database = Database(DB_URL, min_size=2, max_size=10)  
    
    try:
        await database.connect()
        app.state._db = database
    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")

async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()
    except Exception as e:
        logger.warn("--- DB DISCONNECT ERROR ---")
        logger.warn(e)
        logger.warn("--- DB DISCONNECT ERROR ---")
