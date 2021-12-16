import openstack
from fastapi import FastAPI

from ovhapi.core.config import settings
from ovhapi.log import LOGGER, setup_logger
from .routers import server, region, mon

setup_logger(LOGGER)
app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(server.api_router)
app.include_router(region.api_router)
app.include_router(mon.api_router)


@app.on_event("startup")
def init_openstack_client():
    """
    Init one openstack client for each region in conf
    :return: None
    """
    for region in settings.OS_REGION_LIST:
        LOGGER.debug(f"Setting up openstack client for region {region}")
        settings.OS_CLIENT_DICT[region] = openstack.connect(region_name=region, cloud="demo")
