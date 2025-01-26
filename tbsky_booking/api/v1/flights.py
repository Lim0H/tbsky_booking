from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_restful.cbv import cbv

from tbsky_booking.core import FlightsSourceEnum, PublicResource
from tbsky_booking.schemas import FlightTripParamsExtend
from tbsky_booking.schemas.flights import FlightPath
from tbsky_booking.services import GetFlightsFromSources
from tbsky_booking.utils import fast_cache_result

__all__ = ["flights_router"]

flights_router = APIRouter(prefix="/flights", tags=["Flights"])


def get_flights_from_sources(
    params: Annotated[FlightTripParamsExtend, Query()],
):

    return GetFlightsFromSources(params)


@cbv(flights_router)
class GetFlightsResource(PublicResource):
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
