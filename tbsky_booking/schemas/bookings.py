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
    "BookingPassengerCreate",
]


class BookingPassengerOneOut(BookingPassengerSecretBase):
    pass


class BookingOneOut(BookingBase):
    booking_id: PrimaryKeyType
    fligth: FlightOut
    passengers: list[BookingPassengerOneOut]


class BookingPassengerManyOut(BookingPassengerBase):
    pass


class BookingManyOut(BookingBase):
    booking_id: PrimaryKeyType
    passengers: list[BookingPassengerManyOut]


class BookingPassengerCreate(BookingPassengerBase):
    pass


class BookingCreate(BookingBase):
    fligth: FlightPath
    passengers: list[BookingPassengerCreate]
