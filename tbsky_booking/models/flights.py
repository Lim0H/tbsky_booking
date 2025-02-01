from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ARRAY, Column, String
from sqlmodel import Field, Relationship

from tbsky_booking.api.v1 import bookings
from tbsky_booking.core import (
    BaseModel,
    BaseSchema,
    ForeignKeyType,
    PrimaryKeyType,
    make_primary_key,
)

if TYPE_CHECKING:
    from .bookings import Booking

__all__ = ["Country", "AirPort", "Flight", "FlightBase", "CountryBase", "AirPortBase"]


class CountryBase(BaseSchema):
    full_country_name: str = Field(unique=True)
    iso_code: Optional[str] = Field(default=None, unique=True)


class Country(CountryBase, BaseModel, table=True):
    __tablename__ = "countries"

    country_id: PrimaryKeyType = make_primary_key()

    dafif_code: list[str] = Field(
        default_factory=list, sa_column=Column(ARRAY(String()))
    )

    airports: list["AirPort"] = Relationship(
        back_populates="airport_country",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class AirPortBase(BaseSchema):
    airport_name: str
    airport_city: str


class AirPort(AirPortBase, BaseModel, table=True):
    __tablename__ = "airports"

    airport_id: PrimaryKeyType = make_primary_key()

    country_id: ForeignKeyType = Field(foreign_key="countries.country_id")

    airport_country: Country = Relationship(
        back_populates="airports",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    airport_iata: Optional[str] = Field(unique=True)
    airport_icao: Optional[str]
    latitude: float
    longitude: float
    altitude: float
    timezone: Optional[float]
    dst: str
    tz_database_timezone: str
    is_active: bool = Field(default=True)


class FlightBase(BaseSchema):
    date_in: datetime
    date_out: datetime
    duration_m: int | None = Field(default=None)


class Flight(BaseModel, FlightBase, table=True):
    __tablename__ = "flights"

    flight_id: PrimaryKeyType = make_primary_key()
    trip_key: str

    origin_airport_id: ForeignKeyType = Field(foreign_key="airports.airport_id")
    destination_airport_id: ForeignKeyType = Field(foreign_key="airports.airport_id")

    origin_airport: AirPort = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Flight.origin_airport_id==AirPort.airport_id",
            "lazy": "joined",
        },
    )
    destination_airport: AirPort = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Flight.destination_airport_id==AirPort.airport_id",
            "lazy": "joined",
        },
    )

    bookings: list["Booking"] = Relationship(
        back_populates="flight",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
