from typing import List, Optional

from fastapi import APIRouter, HTTPException

from ovhapi import openstack_helper
from ovhapi.core.config import settings
from ovhapi.exceptions import ObjectNotFoundException
from ovhapi.log import LOGGER
from ovhapi.models import Server

api_router = APIRouter()


@api_router.get("/server", response_model=List[Server])
async def list_server(region: Optional[str] = None, do_async: Optional[bool] = False) -> List[Server]:
    """
    List all servers in region.
    :param region: Region. If None, we list in all regions
    :param do_async: List server in async way or not
    :return: List of Server
    """
    LOGGER.debug(f"List all our openstack servers with region = {region}")
    region_list = []
    if region is not None:
        region_list.append(region)
    else:
        region_list = settings.OS_REGION_LIST
    try:
        return [server for server in await openstack_helper.get_server_list(region_list=region_list, do_async=do_async)]
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Region not found")


@api_router.get("/server/{server_id}", response_model=Server)
async def get_server(server_id, region: str = "BHS5") -> Server:
    LOGGER.debug(f"Getting openstack server with id {server_id} within region {region}")
    try:
        server = openstack_helper.get_server(server_id=server_id, region=region)
        print(server)
        return server
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Region not found")
