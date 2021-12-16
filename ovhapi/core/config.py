"""
https://pydantic-docs.helpmanual.io/usage/settings/
"""
import os
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Ovh training API"
    OS_REGION_LIST: List[str] = ["BHS5", "GRA7", "SBG5"]
    OS_CLIENT_DICT = {}
    OS_USER = os.environ.get("OS_USER")
    OS_PASSWORD = os.environ.get("OS_PASSWORD")


settings = Settings()
