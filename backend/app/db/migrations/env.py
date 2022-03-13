import pathlib
import sys
import os  
import logging
from logging.config import fileConfig

import alembic
from sqlalchemy import engine_from_config, create_engine, pool
from psycopg2 import DatabaseError

# Append app directory for importing config
sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from app.core.config import DATABASE_URL, TEST_DATABASE_URL, POSTGRES_TEST_DB 


# Alembic Environment File


# Alembic Config object, which provides access to values within the .ini file
config = alembic.context.config

# Interpret the config file for logging
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")


# Online Migrations
def run_migrations_online() -> None:

    if os.environ.get("TESTING"):
        DB_URL = str(TEST_DATABASE_URL)  
    else:
        str(DATABASE_URL)

    # Handle testing config for migrations
    if os.environ.get("TESTING"):
        # Connect to primary db
        default_engine = create_engine(str(DATABASE_URL), 
                                       isolation_level = "AUTOCOMMIT")
        # Drop testing db if it exists and create a fresh one
        with default_engine.connect() as default_conn:
            default_conn.execute(
                f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE \
                datname='{POSTGRES_TEST_DB}'"
            )
            default_conn.execute(f"DROP DATABASE IF EXISTS {POSTGRES_TEST_DB}")
            default_conn.execute(f"CREATE DATABASE {POSTGRES_TEST_DB}")
        # Reconnect to TestDB and create postGIS extension
        default_engine = create_engine(
            str(TEST_DATABASE_URL), 
            isolation_level = "AUTOCOMMIT"
        )
        with default_engine.connect() as default_conn:
            default_conn.execute("CREATE EXTENSION postgis;")
            default_conn.execute("CREATE EXTENSION postgis_topology;")

    connectable = config.attributes.get("connection", None)
    config.set_main_option("sqlalchemy.url", DB_URL)  

    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix = "sqlalchemy.",
            poolclass = pool.NullPool,
        )
        
    with connectable.connect() as connection:
        alembic.context.configure(
            connection = connection,
            include_schemas = True,
            version_table_schema = "metadata",
            target_metadata = None
        )

        connection.execute('CREATE SCHEMA IF NOT EXISTS metadata')

        with alembic.context.begin_transaction():
            alembic.context.run_migrations()


# Offline Migrations
def run_migrations_offline() -> None:
    
    # Check if testing
    if os.environ.get("TESTING"):
        raise DatabaseError("Running testing migrations offline currently \
            not permitted.")
        
    alembic.context.configure(url = str(DATABASE_URL))
    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


# Run migrations
if alembic.context.is_offline_mode():
    logger.info("Running migrations offline")
    run_migrations_offline()
else:
    logger.info("Running migrations online")
    run_migrations_online()
