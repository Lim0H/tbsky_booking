import logging

import asyncclick
from tbsky_booking.core import AppSettings
from tbsky_booking.repository import (
    AirPortsRepository,
    BaseFlightsRepository,
    CountriesRepository,
)

log = logging.getLogger(__file__)


@asyncclick.group("Flights fill repositories commands")
def fill_repositories_cli():
    pass


@fill_repositories_cli.command()
async def fill_repositories():
    repos: list[BaseFlightsRepository] = [
        CountriesRepository(user_id=AppSettings.users.DEFAULT_USER_ID),
        AirPortsRepository(user_id=AppSettings.users.DEFAULT_USER_ID),
    ]
    for repo in repos:
        log.info(f"Fill repository: {repo.__class__.__name__}")
        await repo.fill_repository()
