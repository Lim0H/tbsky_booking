import asyncio
from datetime import datetime, timedelta
from itertools import chain
from typing import Awaitable, Optional

from more_itertools import filter_map

from tbsky_booking.core import FlightsSourceEnum, FunctorGetService
from tbsky_booking.repository import (
    BaseAvailableFlightTrips,
    GoogleAvailableFlightTrips,
    RyanAirAvailableFlightTrips,
)
from tbsky_booking.schemas import FlightPath, FlightTripParams, FlightTripParamsExtend

__all__ = ["GetFlightsFromSources"]


class GetFlightsFromSources(FunctorGetService[FlightPath]):
    def __init__(
        self,
        flight_trip_params: FlightTripParamsExtend,
        only_from: Optional[list[FlightsSourceEnum]] = None,
    ):
        self.flight_trip_params = flight_trip_params
        self.only_from = only_from or list(FlightsSourceEnum)
        super().__init__(flight_trip_params)

    _map_sources: dict[FlightsSourceEnum, type[BaseAvailableFlightTrips]] = {
        FlightsSourceEnum.GOOGLE: GoogleAvailableFlightTrips,
        FlightsSourceEnum.RYANAIR: RyanAirAvailableFlightTrips,
    }

    def get_flights_getters(self):
        repos = filter_map(
            lambda kv: kv[1]() if kv[0] in self.only_from else None,
            self._map_sources.items(),
        )
        getters: list[Awaitable[list[FlightPath]]] = []
        use_flex_days_before_in = (
            self.flight_trip_params.flex_days_before_in
            and (datetime.now().date() - self.flight_trip_params.date_in).days
            > self.flight_trip_params.flex_days_before_in
            and datetime.now().date() != self.flight_trip_params.date_in
        )
        use_flex_days_after_in = (
            self.flight_trip_params.flex_days_before_in
            and datetime.now().date() != self.flight_trip_params.date_in
        )
        for repo in repos:
            if use_flex_days_before_in:
                for i in range(self.flight_trip_params.flex_days_before_in):
                    getters.append(
                        repo(
                            FlightTripParams(
                                origin_airport_iata=self.flight_trip_params.origin_airport_iata,
                                destination_airport_iata=self.flight_trip_params.destination_airport_iata,
                                date_in=self.flight_trip_params.date_in
                                - timedelta(days=i + 1),
                                date_out=(
                                    self.flight_trip_params.date_out
                                    - timedelta(days=i + 1)
                                    if self.flight_trip_params.date_out
                                    else None
                                ),
                                adt=self.flight_trip_params.adt,
                                chd=self.flight_trip_params.chd,
                                inf=self.flight_trip_params.inf,
                                teen=self.flight_trip_params.teen,
                                max_stops=self.flight_trip_params.max_stops,
                                seat=self.flight_trip_params.seat,
                            )
                        )
                    )
            if use_flex_days_after_in:
                for i in range(self.flight_trip_params.flex_days_after_in):
                    getters.append(
                        repo(
                            FlightTripParams(
                                origin_airport_iata=self.flight_trip_params.origin_airport_iata,
                                destination_airport_iata=self.flight_trip_params.destination_airport_iata,
                                date_in=self.flight_trip_params.date_in
                                + timedelta(days=i + 1),
                                date_out=(
                                    self.flight_trip_params.date_out
                                    + timedelta(days=i + 1)
                                    if self.flight_trip_params.date_out
                                    else None
                                ),
                                adt=self.flight_trip_params.adt,
                                chd=self.flight_trip_params.chd,
                                inf=self.flight_trip_params.inf,
                                teen=self.flight_trip_params.teen,
                                max_stops=self.flight_trip_params.max_stops,
                                seat=self.flight_trip_params.seat,
                            )
                        )
                    )
            getters.append(repo(self.flight_trip_params))
        return getters

    async def get(
        self,
    ):
        return list(chain(*(await asyncio.gather(*self.get_flights_getters()))))
