from fastapi import Depends

from tbsky_booking.core import Base64Tools, get_user_id_by_access_token
from tbsky_booking.models import Booking, Flight
from tbsky_booking.models.bookings import BookingPassenger
from tbsky_booking.repository import (
    AirPortsRepository,
    BookingsRepository,
    FlightsRepository,
)
from tbsky_booking.schemas import BookingCreate

__all__ = ["BookingsService"]


class BookingsService:
    def __init__(
        self,
        bookings_repository: BookingsRepository = Depends(),
        flights_repository: FlightsRepository = Depends(),
        airports_repository: AirPortsRepository = Depends(),
        user_id: str = Depends(get_user_id_by_access_token),
    ):
        self.bookings_repository = bookings_repository
        self.flights_repository = flights_repository
        self.airports_repository = airports_repository
        self.user_id = user_id

    async def create_booking(self, booking_create: BookingCreate) -> Booking:
        async with self.flights_repository.async_session_factory() as db_session:
            if not (
                flight := await self.flights_repository.get_first(
                    params={"trip_key": booking_create.fligth.trip_key}
                )
            ):
                origin_airport = await self.airports_repository.get_one(
                    airport_iata=booking_create.fligth.origin_airport_iata
                )
                destination_airport = await self.airports_repository.get_one(
                    airport_iata=booking_create.fligth.destination_airport_iata
                )
                flight = await self.flights_repository.add(
                    Flight(
                        origin_airport_id=origin_airport.airport_id,
                        destination_airport_id=destination_airport.airport_id,
                        trip_key=Base64Tools.encode(booking_create.fligth.trip_key),
                    ),
                    session=db_session,
                    with_commmit=False,
                )
            booking = await self.bookings_repository.add(
                Booking(
                    user_id=self.user_id,
                    flight_id=flight.flight_id,
                    booking_passengers=[
                        BookingPassenger(**passenger.model_dump())
                        for passenger in booking_create.passengers
                    ],
                ),
                session=db_session,
                with_commmit=False,
            )
            await db_session.commit()
            return booking

    async def confirm_booking(self, booking_id: str) -> Booking:
        pass

    async def cancel_booking(self, booking_id: str) -> Booking:
        pass

    async def get_booking(self, booking_id: str) -> Booking:
        pass

    async def get_bookings(self) -> list[Booking]:
        pass
