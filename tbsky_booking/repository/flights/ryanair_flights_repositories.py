from tbsky_booking.core import (
    RYANAIR_AVAILABLE_DATES_API_URL,
    RYANAIR_AVAILABLE_FLIGHTS_API_URL,
    RYANAIR_AVAILABLE_ROUTES_API_URL,
    FlightsSourceEnum,
)
from tbsky_booking.core.consts.flights import RYANAIR_HOME_URL
from tbsky_booking.schemas import (
    AvailableDate,
    AvailableDestination,
    FlightPath,
    FlightStep,
    FlightTrip,
    FlightTripParams,
)
from tbsky_booking.utils import get_value_from_dict, parse_time

from .base_flights_repositories import (
    BaseAvailableDates,
    BaseAvailableDestinations,
    BaseAvailableFlightTrips,
)

__all__ = [
    "RyanAirAvailableDates",
    "RyanAirAvailableDestinations",
    "RyanAirAvailableFlightTrips",
]


class RyanAirAvailableDates(BaseAvailableDates):

    async def get(
        self, origin_airport_iata: str, destination_airport_iata: str
    ) -> list[AvailableDate]:
        response = await self.requests_client.get(
            RYANAIR_AVAILABLE_DATES_API_URL.format_map(
                {
                    "origin": origin_airport_iata,
                    "destination": destination_airport_iata,
                }
            )
        )
        return [
            AvailableDate(
                date=x,
                origin_airport_iata=origin_airport_iata,
                destination_airport_iata=destination_airport_iata,
                source=FlightsSourceEnum.RYANAIR,
            )
            for x in response.json()
        ]


class RyanAirAvailableDestinations(BaseAvailableDestinations):
    async def get(self, airport_iata: str):
        response = await self.requests_client.get(
            RYANAIR_AVAILABLE_ROUTES_API_URL.format(airport_iata)
        )
        return [
            AvailableDestination(
                airport_iata=get_value_from_dict(x, "arrivalAirport.code", None),
                source=FlightsSourceEnum.RYANAIR,
            )
            for x in response.json()
            if get_value_from_dict(x, "arrivalAirport.code", None)
        ]


class RyanAirAvailableFlightTrips(BaseAvailableFlightTrips):

    def _get_flight_from_json(self, trips: dict[list[dict]]):
        result = []
        for first_trip in trips.get("dates", []):
            for flight in first_trip.get("flights", []):
                flight_date_in = flight["timeUTC"][0]
                flight_date_out = flight["timeUTC"][1]
                result.append(
                    FlightTrip(
                        date_in=flight_date_in,
                        date_out=flight_date_out,
                        flight_number=flight["flightNumber"],
                        origin_airport_iata=flight["segments"][0]["origin"],
                        destination_airport_iata=flight["segments"][-1]["destination"],
                        duration_m=parse_time(flight["duration"]),
                        steps=[
                            FlightStep(
                                origin_airport_iata=x["origin"],
                                destination_airport_iata=x["destination"],
                                date_in=x["timeUTC"][0],
                                date_out=x["timeUTC"][1],
                                flight_number=x.get("flightNumber"),
                            )
                            for x in flight["segments"][1:]
                        ],
                    )
                )
        return result

    async def get(
        self,
        flight_trip_params: FlightTripParams,
    ) -> list[FlightPath]:
        await self.requests_client.get(RYANAIR_HOME_URL)
        response = await self.requests_client.get(
            RYANAIR_AVAILABLE_FLIGHTS_API_URL,
            params={
                "ADT": flight_trip_params.adt,
                "TEEN": flight_trip_params.teen,
                "CHD": flight_trip_params.chd,
                "INF": flight_trip_params.inf,
                "Origin": flight_trip_params.origin_airport_iata,
                "Destination": flight_trip_params.destination_airport_iata,
                "promoCode": None,
                "IncludeConnectingFlights": False,
                "DateIn": (
                    str(flight_trip_params.date_out)
                    if flight_trip_params.date_out
                    else None
                ),
                "DateOut": str(flight_trip_params.date_in),
                "FlexDaysBeforeOut": 2,
                "FlexDaysOut": 2,
                "FlexDaysBeforeIn": 2,
                "FlexDaysIn": 2,
                "RoundTrip": bool(flight_trip_params.date_out),
                "ToUs": "AGREED",
            },
        )
        if response.is_client_error:
            message: str = response.json()["message"]
            if "Availability declined" == message:
                return []
            raise ValueError(response.text)

        json: dict = response.json()
        trips = json.get("trips", [])
        origin_trips: list[FlightTrip] = (
            self._get_flight_from_json(trips[0]) if len(trips) > 0 else []
        )
        destination_trips: list[FlightTrip] = (
            self._get_flight_from_json(trips[1]) if len(trips) > 1 else []
        )

        return [
            FlightPath(
                destination_airport_iata=flight_trip_params.destination_airport_iata,
                origin_airport_iata=flight_trip_params.origin_airport_iata,
                origin_trips=origin_trips,
                destination_trips=destination_trips,
                source=FlightsSourceEnum.RYANAIR,
            )
        ]
