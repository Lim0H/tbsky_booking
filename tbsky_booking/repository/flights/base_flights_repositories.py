from tbsky_booking.core import BaseGetRestApiRepository
from tbsky_booking.schemas import (
    AvailableDate,
    AvailableDestination,
    FlightPath,
    FlightTripParams,
)

__all__ = [
    "BaseAvailableDates",
    "BaseAvailableDestinations",
    "BaseAvailableFlightTrips",
]


class BaseAvailableDates(BaseGetRestApiRepository[AvailableDate]):
    async def get(
        self, origin_airport_iata: str, destination_airport_iata: str
    ) -> list[AvailableDate]:
        raise NotImplementedError


class BaseAvailableDestinations(BaseGetRestApiRepository[AvailableDestination]):
    async def get(self, airport_iata: str) -> list[AvailableDate]:
        raise NotImplementedError


class BaseAvailableFlightTrips(BaseGetRestApiRepository[FlightPath]):
    async def get(
        self,
        flight_trip_params: FlightTripParams,
    ):
        raise NotImplementedError
