from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

PROJECT_NAME = "ecoindex"
VERSION = "1.0.0"
API_PREFIX = "/api/v1"

SECRET_KEY = config("SECRET_KEY", cast = Secret)
POSTGRES_USER = config("POSTGRES_USER", cast = str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast = Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast = str, default = "db")
POSTGRES_PORT = config("POSTGRES_PORT", cast = str, default = "5432")
POSTGRES_DB = config("POSTGRES_DB", cast = str)
POSTGRES_TEST_DB = config("POSTGRES_TEST_DB", cast = str)
ALGORITHM = config("ALGORITHM", cast = str)
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    cast = int,
    default = 7 * 24 * 60  # one week
)
RESET_TOKEN_EXPIRE_MINUTES=config(
    "RESET_TOKEN_EXPIRE_MINUTES",
    cast = int,
    default = 24 * 60 # one day
)
JWT_AUDIENCE_RESET = config("JWT_AUDIENCE_RESET", cast = str, 
                            default = "ecoindex:reset")
JWT_AUDIENCE = config("JWT_AUDIENCE", cast = str, default = "ecoindex:auth")
JWT_TOKEN_PREFIX = config("JWT_TOKEN_PREFIX", cast = str, default = "Bearer")

PASSWORD_URL = config("PASSWORD_URL", cast = str)

MAIL_USERNAME = config('MAIL_USERNAME', cast = str)
MAIL_PASSWORD = config('MAIL_PASSWORD', cast = str)
MAIL_FROM = config('MAIL_FROM', cast = str)
MAIL_PORT = config('MAIL_PORT', cast = str)
MAIL_SERVER = config('MAIL_SERVER', cast = str)
MAIL_FROM_NAME = config('MAIL_FROM_NAME', cast = str)

DATABASE_URL = config(
    "DATABASE_URL",
    cast = DatabaseURL,
    default = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@\
              {POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

TEST_DATABASE_URL = config(
    "TEST_DATABASE_URL",
    cast = DatabaseURL,
    default = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@\
              {POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_TEST_DB}"
)

SERVER_URL = config(
    "SERVER_URL",
    cast = DatabaseURL,
    default = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@\
              {POSTGRES_SERVER}:{POSTGRES_PORT}"
)
