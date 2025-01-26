import dateparser
from fast_flights import FlightData, Passengers, TFSData, get_flights_from_filter
from timeout_function_decorator import timeout

from tbsky_booking.core import MAP_GOOGLE_SEAT_ENUM, FlightsSourceEnum, GoogleTripEnum
from tbsky_booking.schemas import FlightPath, FlightTrip, FlightTripParams
from tbsky_booking.utils import to_async

from .base_flights_repositories import BaseAvailableFlightTrips

__all__ = [
    "GoogleAvailableFlightTrips",
]


class GoogleAvailableFlightTrips(BaseAvailableFlightTrips):
    @to_async
    def _get_flight_data(self, search_filter: TFSData):
        return timeout(15)(get_flights_from_filter)(
            filter=search_filter,
            mode="fallback",
        )

    async def get(
        self,
        flight_trip_params: FlightTripParams,
    ) -> list[FlightPath]:
        flight_data = [
            FlightData(
                from_airport=flight_trip_params.origin_airport_iata,
                to_airport=flight_trip_params.destination_airport_iata,
                date=str(flight_trip_params.date_in),
                max_stops=flight_trip_params.max_stops,
            )
        ]
        trip = GoogleTripEnum.ONE_WAY
        if flight_trip_params.date_out:
            flight_data.append(
                FlightData(
                    from_airport=flight_trip_params.destination_airport_iata,
                    to_airport=flight_trip_params.origin_airport_iata,
                    date=str(flight_trip_params.date_out),
                    max_stops=flight_trip_params.max_stops,
                )
            )
            trip = GoogleTripEnum.ROUND_TRIP
        search_filter = TFSData(
            flight_data=flight_data,
            seat=MAP_GOOGLE_SEAT_ENUM[flight_trip_params.seat].value,
            trip=trip.value,
            passengers=Passengers(
                adults=flight_trip_params.adt,
                children=flight_trip_params.chd + flight_trip_params.teen,
                infants_on_lap=flight_trip_params.inf,
            ),
        )
        try:
            result_from_google = await self._get_flight_data(
                search_filter=search_filter,
            )
        except Exception:
            return []

        available_flight_trips = [
            FlightPath(
                airline_name=trip.name,
                origin_airport_iata=flight_trip_params.origin_airport_iata,
                destination_airport_iata=flight_trip_params.destination_airport_iata,
                origin_trips=[
                    FlightTrip(
                        date_in=dateparser.parse(trip.departure),
                        date_out=dateparser.parse(trip.arrival),
                        origin_airport_iata=flight_trip_params.origin_airport_iata,
                        destination_airport_iata=flight_trip_params.destination_airport_iata,
                        steps_count=trip.stops,
                        duration_m=(
                            (
                                dateparser.parse(trip.departure)
                                - dateparser.parse(trip.departure)
                            ).total_seconds()
                            // 60
                            if dateparser.parse(trip.departure)
                            and dateparser.parse(trip.departure)
                            else None  # type: ignore
                        ),
                    )
                ],
                destination_trips=[],
                source=FlightsSourceEnum.GOOGLE,
            )
            for trip in result_from_google.flights
        ]

        return available_flight_trips
