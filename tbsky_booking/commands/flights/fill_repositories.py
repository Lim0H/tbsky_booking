import asyncclick

from tbsky_booking.repository import (
    AirPortsRepository,
    BaseFlightsRepository,
    CountriesRepository,
    FlightsRepository,
)


@asyncclick.group("Flights fill repositories commands")
def fill_repositories_cli():
    pass


@fill_repositories_cli.command()
async def fill_repositories():
    repos: list[BaseFlightsRepository] = [
        CountriesRepository(),
        AirPortsRepository(),
    ]
    for repo in repos:
        await repo.fill_repository()
