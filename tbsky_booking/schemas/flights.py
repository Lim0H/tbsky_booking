from datetime import date, datetime
from typing import Optional

from pydantic import Field, model_validator

from tbsky_booking.core import (
    BaseSchema,
    FlightsSourceEnum,
    PrimaryKeyType,
    PublicSafelyBase64Tools,
    SeatEnum,
)
from tbsky_booking.models import AirPortBase, CountryBase, FlightBase

__all__ = [
    "AvailableDate",
    "AvailableDestination",
    "FlightPath",
    "FlightTrip",
    "FlightTripParamsExtend",
    "FlightStep",
    "FlightTripParams",
    "CountryOut",
    "AirPortOut",
    "FlightOut",
]


class CountryOut(CountryBase):
    pass


class AirPortOut(AirPortBase):
    airport_country: CountryOut


class FlightOut(FlightBase):
    flight_id: PrimaryKeyType
    origin_airport: AirPortOut
    destination_airport: AirPortOut


class BaseSourceSchema(BaseSchema):
    source: FlightsSourceEnum


class AvailableDate(BaseSourceSchema):
    date: date
    origin_airport_iata: str
    destination_airport_iata: str


class AvailableDestination(BaseSourceSchema):
    airport_iata: str


class FlightStep(BaseSchema):
    date_in: datetime | None
    date_out: datetime | None
    origin_airport_iata: str
    destination_airport_iata: str
    flight_number: Optional[str] = Field(default=None)


class FlightTrip(FlightStep):
    duration_m: int | None = Field(default=None)
    flight_number: Optional[str] = Field(default=None)
    steps: list["FlightStep"] = Field(default_factory=list)
    steps_count: int = Field(default=0)


class FlightPath(BaseSourceSchema):
    trip_key: str = Field(default="")
    airline_name: Optional[str] = Field(default=None)
    origin_airport_iata: str
    destination_airport_iata: str
    origin_trips: list[FlightTrip]
    destination_trips: list[FlightTrip]

    @model_validator(mode="after")
    def validate_model(self):
        if self.origin_airport_iata == self.destination_airport_iata:
            raise ValueError("origin_airport_iata == destination_airport_iata")
        if not self.trip_key:
            self.trip_key = PublicSafelyBase64Tools.encode(self.model_dump_json())
        return self


class FlightTripParams(BaseSchema):
    origin_airport_iata: str
    destination_airport_iata: str
    date_in: date = Field(default_factory=lambda: datetime.now().date())
    date_out: Optional[date] = Field(default=None)
    adt: int = Field(default=0)
    chd: int = Field(default=0)
    inf: int = Field(default=0)
    teen: int = Field(default=0)
    max_stops: Optional[int] = Field(default=None, ge=1, le=5)
    seat: SeatEnum = Field(default=SeatEnum.ECONOMY)

    @model_validator(mode="after")
    def validate_model(self):
        if self.origin_airport_iata == self.destination_airport_iata:
            raise ValueError("origin_airport_iata == destination_airport_iata")
        if all((not x for x in [self.adt, self.chd, self.inf, self.teen])):
            raise ValueError("Must be choice one person")
        if self.adt + self.chd + self.inf + self.teen > 6:
            raise ValueError("Max 6 persons in search")
        if self.adt != (self.chd) and self.chd > 0:
            raise ValueError("must be adt == chd")
        if self.date_in < datetime.now().date():
            raise ValueError("date_in < now")
        if self.date_in == self.date_out:
            raise ValueError("date_in == date_out")
        return self


class FlightTripParamsExtend(FlightTripParams):
    flex_days_before_in: int = Field(default=2, ge=0, le=4)
    flex_days_after_in: int = Field(default=2, ge=0, le=4)
