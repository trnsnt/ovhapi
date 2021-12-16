import asyncio
from functools import lru_cache
from typing import List, Any, Dict

import httpx
from openstack.exceptions import ResourceNotFound

from ovhapi.core.config import settings
from ovhapi.exceptions import ObjectNotFoundException
from ovhapi.log import LOGGER


def get_server(server_id: str, region: str):
    """Get server with id = server_id"""
    openstack_client = settings.OS_CLIENT_DICT.get(region)
    if openstack_client is None:
        LOGGER.debug(f"Region {region} does not exist")
        raise ObjectNotFoundException()
    try:
        return openstack_client.compute.get_server(server_id).to_dict()
    except ResourceNotFound:
        raise ObjectNotFoundException()


async def get_server_list(region_list: List[str], do_async: bool = False):
    """List openstack server in all region of region_list"""
    if not do_async:
        return get_server_list_sync(region_list=region_list)
    return await get_server_list_async(region_list=region_list)


def get_server_list_sync(region_list: List[str]) -> List[Any]:
    """List all server in a sync way"""
    server_list = []
    LOGGER.debug(f"Listing server in region {region_list}")
    for region in region_list:
        openstack_client = settings.OS_CLIENT_DICT.get(region)
        if openstack_client is None:
            LOGGER.debug(f"Region {region} does not exist")
            raise ObjectNotFoundException()
        server_list += openstack_client.compute.servers()
    return [server.to_dict() for server in server_list]


async def get_server_list_async(region_list: List[str]) -> List[Dict[str, Any]]:
    """List all server in an async way"""
    token = _get_token()
    session = httpx.AsyncClient()
    server_list = await asyncio.gather(
        *[call_url(session, token=token, url=_get_url(region=region)) for region in region_list]
    )
    await session.aclose()
    flat_list = [item for sublist in server_list for item in sublist]
    return flat_list


async def call_url(session, token: str, url: str):
    """Async HTTP call"""
    response = await session.request(method="GET", url=url, headers={"X-Auth-Token": token})
    return response.json().get("servers")


@lru_cache
def _get_token() -> str:
    response = httpx.post(
        "https://auth.cloud.ovh.net/v3/auth/tokens",
        headers={"Content-Type": "application/json"},
        json={
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "name": settings.OS_USER,
                            "domain": {"id": "default"},
                            "password": settings.OS_PASSWORD,
                        }
                    },
                }
            }
        },
    )
    return response.headers["X-Subject-Token"]


def _get_url(region):
    """
    Get openstack url for a given region
    """
    return f"https://compute.{region}.cloud.ovh.net/v2/servers"
