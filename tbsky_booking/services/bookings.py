from fastapi import Depends, HTTPException

from tbsky_booking.core import (
    Base64Tools,
    BookingStatusEnum,
    get_user_id_by_access_token,
)
from tbsky_booking.models import Booking, BookingPassenger, Flight
from tbsky_booking.repository import (
    AirPortsRepository,
    BookingPassengersRepository,
    BookingsRepository,
    FlightsRepository,
)
from tbsky_booking.schemas import BookingCreate, BookingPassengerEdit

__all__ = ["BookingsService"]


class BookingsService:
    def __init__(
        self,
        bookings_repository: BookingsRepository = Depends(),
        booking_passengers_repository: BookingPassengersRepository = Depends(),
        flights_repository: FlightsRepository = Depends(),
        airports_repository: AirPortsRepository = Depends(),
        user_id: str = Depends(get_user_id_by_access_token),
    ):
        self.bookings_repository = bookings_repository
        self.flights_repository = flights_repository
        self.airports_repository = airports_repository
        self.booking_passengers_repository = booking_passengers_repository
        self.user_id = user_id

    async def create_booking(self, booking_create: BookingCreate) -> Booking:
        if flight := (
            await self.flights_repository.get_first(
                params={"trip_key": booking_create.fligth.trip_key}
            )
        ):
            if exists_booking := (
                await self.bookings_repository.get_first(
                    params={
                        "flight_id": flight.flight_id,
                        "user_id": self.user_id,
                        "booking_status": [
                            BookingStatusEnum.CREATED,
                            BookingStatusEnum.CONFIRMED,
                        ],
                    }
                )
            ):
                raise HTTPException(
                    status_code=400,
                    detail=f'Booking with trip_key "{booking_create.fligth.trip_key}" already exists, booking_id: {exists_booking.booking_id}',
                )
        async with self.flights_repository.async_session_factory() as db_session:
            if not flight:
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

    async def edit_booking_before_confirm(
        self, booking_id: str, booking_passengers: list[BookingPassengerEdit]
    ) -> Booking:
        booking = await self.bookings_repository.get_one(
            params={"user_id": self.user_id, "booking_id": booking_id}
        )
        if booking.booking_status != BookingStatusEnum.CREATED:
            raise HTTPException(
                status_code=400,
                detail=f"Booking with id {booking_id} is not created",
            )
        map_booking_passengers = {
            booking_passenger.booking_passenger_id: booking_passenger
            for booking_passenger in booking.booking_passengers
        }
        async with (
            self.booking_passengers_repository.async_session_factory() as session
        ):
            for booking_passenger in booking_passengers:
                if booking_passenger_from_db := map_booking_passengers.get(
                    booking_passenger.booking_passenger_id
                ):
                    await self.booking_passengers_repository.merge(
                        booking_passenger_from_db, booking_passenger
                    )
            await session.refresh(booking)
            return booking

    async def confirm_booking(self, booking_id: str) -> Booking:
        booking = await self.bookings_repository.get_one(
            params={"user_id": self.user_id, "booking_id": booking_id}
        )
        booking.booking_status = BookingStatusEnum.CONFIRMED
        return await self.bookings_repository.edit(booking)

    async def cancel_booking(self, booking_id: str) -> Booking:
        booking = await self.bookings_repository.get_one(
            params={"user_id": self.user_id, "booking_id": booking_id}
        )
        booking.booking_status = BookingStatusEnum.CANCELLED
        return await self.bookings_repository.edit(booking)

    async def get_booking(self, booking_id: str) -> Booking:
        return await self.bookings_repository.get_one(
            params={"user_id": self.user_id, "booking_id": booking_id}
        )

    async def get_bookings(self) -> list[Booking]:
        return await self.bookings_repository.get(params={"user_id": self.user_id})
