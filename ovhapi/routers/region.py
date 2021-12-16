from typing import List

from fastapi import APIRouter

from ovhapi.core.config import settings
from ovhapi.log import LOGGER

api_router = APIRouter()


@api_router.get("/region", response_model=List[str])
async def list_region() -> List[str]:
    """
    List all available regions
    :return: List of all available region
    """
    LOGGER.debug(f"List all our openstack region")
    return list(settings.OS_REGION_LIST)
