from datetime import date
from typing import Optional

from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import Field, Relationship

from tbsky_booking.core import (
    BaseModel,
    BaseSchema,
    BookingStatusEnum,
    ForeignKeyType,
    PassengerTypeEnum,
    PrimaryKeyType,
    SeatEnum,
    SeatNumberEnum,
    make_primary_key,
)

from .flights import Flight

__all__ = [
    "Booking",
    "BookingPassenger",
    "BookingPassengerBase",
    "BookingBase",
    "BookingPassengerSecretBase",
]


class BookingPassengerBase(BaseSchema):
    first_name: str
    last_name: str

    seat: SeatEnum = Field(default=SeatEnum.ECONOMY)

    seat_number: SeatNumberEnum
    passenger_type: PassengerTypeEnum = Field(default=PassengerTypeEnum.ADULT)


class BookingPassengerSecretBase(BookingPassengerBase):
    email: Optional[EmailStr]
    phone_number: Optional[PhoneNumber]
    passport_number: str
    passport_expire_date: date


class BookingPassenger(BookingPassengerSecretBase, BaseModel, table=True):
    __tablename__ = "booking_passengers"

    booking_passenger_id: PrimaryKeyType = make_primary_key()
    booking_id: ForeignKeyType = Field(foreign_key="bookings.booking_id")

    booking: "Booking" = Relationship()


class BookingBase(BaseSchema):
    booking_status: BookingStatusEnum = Field(default=BookingStatusEnum.CREATED)


class Booking(BookingBase, BaseModel, table=True):
    __tablename__ = "bookings"

    booking_id: PrimaryKeyType = make_primary_key()
    flight_id: ForeignKeyType = Field(foreign_key="flights.flight_id")

    user_id: str
    flight: Flight = Relationship()
    booking_passengers: list["BookingPassenger"] = Relationship()
