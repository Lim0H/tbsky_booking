from tbsky_booking.core import PrimaryKeyType
from tbsky_booking.models import (
    BookingBase,
    BookingPassengerBase,
    BookingPassengerSecretBase,
)

from .flights import FlightOut, FlightPath

__all__ = [
    "BookingOneOut",
    "BookingManyOut",
    "BookingPassengerOneOut",
    "BookingPassengerManyOut",
    "BookingCreate",
    "BookingPassengerEdit",
    "BookingPassengerCreate",
]


class BookingPassengerOneOut(BookingPassengerSecretBase):
    pass


class BookingOneOut(BookingBase):
    booking_id: PrimaryKeyType
    flight: FlightOut
    booking_passengers: list[BookingPassengerOneOut]


class BookingPassengerManyOut(BookingPassengerBase):
    pass


class BookingManyOut(BookingBase):
    booking_id: PrimaryKeyType
    booking_passengers: list[BookingPassengerManyOut]


class BookingPassengerCreate(BookingPassengerSecretBase):
    pass


class BookingPassengerEdit(BookingPassengerSecretBase):
    booking_passenger_id: PrimaryKeyType


class BookingCreate(BookingBase):
    flight: FlightPath
    booking_passengers: list[BookingPassengerCreate]
