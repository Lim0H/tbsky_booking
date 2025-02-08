from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_restful.cbv import cbv

from tbsky_booking.core import FlightsSourceEnum, PublicResource
from tbsky_booking.models import AirPort
from tbsky_booking.repository import AirPortsRepository, CountriesRepository
from tbsky_booking.schemas import (
    AirPortOut,
    CountryOut,
    FlightPath,
    FlightTripParamsExtend,
)
from tbsky_booking.services import GetFlightsFromSources
from tbsky_booking.utils import fast_cache_result

__all__ = ["flights_router", "countries_router", "airports_router"]

flights_router = APIRouter(prefix="/flights", tags=["Flights"])
countries_router = APIRouter(prefix="/countries", tags=["Countries"])
airports_router = APIRouter(prefix="/airports", tags=["Airports"])


def get_flights_from_sources(
    params: Annotated[FlightTripParamsExtend, Query()],
):
    return GetFlightsFromSources(params)


@cbv(flights_router)
class FlightsResource(PublicResource):
    get_flights_from_sources: GetFlightsFromSources = Depends(get_flights_from_sources)

    @flights_router.get("/{only_from}", response_model=list[FlightPath])
    @fast_cache_result
    async def get_only_from(
        self,
        only_from: FlightsSourceEnum,
    ):
        self.get_flights_from_sources.only_from = [only_from]
        return await self.get_flights_from_sources()

    @flights_router.get("/", response_model=list[FlightPath])
    @fast_cache_result
    async def get(
        self,
    ):
        return await self.get_flights_from_sources()


@cbv(countries_router)
class CountriesResource(PublicResource):
    @countries_router.get("/", response_model=list[CountryOut])
    async def get_countries(self, countries_repo: CountriesRepository = Depends()):
        return await countries_repo.get()


@cbv(airports_router)
class AirportsResource(PublicResource):
    @airports_router.get("/", response_model=list[AirPortOut])
    async def get_airports(self, airports_repo: AirPortsRepository = Depends()):
        return await airports_repo.get()

    @airports_router.get("/{country_id}", response_model=list[AirPortOut])
    async def get_airports_by_country(
        self,
        country_id: str,
        airports_repo: AirPortsRepository = Depends(),
    ):
        return await airports_repo.get(params={AirPort.country_id: country_id})
