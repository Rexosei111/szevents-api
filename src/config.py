import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    authjwt_secret_key: str
    # jwt_expire_time: int
    # algorithm: str
    mongodb_url: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
