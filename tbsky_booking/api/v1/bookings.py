from typing import Annotated

import orjson
from fastapi import APIRouter, Body, Depends, Path
from fastapi_restful.cbv import cbv

from tbsky_booking.core import ProtectedResource, PublicSafelyBase64Tools
from tbsky_booking.schemas import (
    BookingCreate,
    BookingPassengerCreate,
    BookingPassengerOneOut,
    FlightPath,
)
from tbsky_booking.services import BookingsService

__all__ = ["bookings_router"]

bookings_router = APIRouter(prefix="/bookings", tags=["Bookings"])


def get_flight_path(
    trip_key: Annotated[str, Path()],
) -> FlightPath:
    model_json = PublicSafelyBase64Tools.decode(trip_key)
    model_dict = orjson.loads(model_json)
    model_dict["trip_key"] = trip_key
    return FlightPath(**model_dict)


@cbv(bookings_router)
class BookingsResource(ProtectedResource):
    bookings_service: BookingsService = Depends()

    @bookings_router.post("/{trip_key}")
    async def create_booking(
        self,
        fligth_path: Annotated[FlightPath, Depends(get_flight_path)],
        booking_passengers: Annotated[list[BookingPassengerCreate], Body()],
    ):
        return await self.bookings_service.create_booking(
            BookingCreate(fligth=fligth_path, passengers=booking_passengers)
        )
