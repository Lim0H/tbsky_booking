from typing import Annotated

import orjson
from fastapi import APIRouter, Body, Depends, Path
from fastapi_restful.cbv import cbv

from tbsky_booking.core import ProtectedResource, PublicSafelyBase64Tools
from tbsky_booking.schemas import (
    BookingCreate,
    BookingManyOut,
    BookingOneOut,
    BookingPassengerCreate,
    BookingPassengerEdit,
    FlightPath,
)
from tbsky_booking.services import BookingsService

__all__ = ["bookings_router"]

bookings_router = APIRouter(prefix="/bookings", tags=["Bookings"])


def get_flight_path(
    trip_key: Annotated[str, Path()],
) -> FlightPath:
    model_json = PublicSafelyBase64Tools.decode(trip_key)
    trip_key = PublicSafelyBase64Tools.crypto.decrypt(trip_key)
    model_dict = orjson.loads(model_json)
    model_dict["trip_key"] = trip_key
    return FlightPath(**model_dict)


@cbv(bookings_router)
class BookingsResource(ProtectedResource):
    bookings_service: BookingsService = Depends()

    @bookings_router.post("/{trip_key}", status_code=201, response_model=BookingOneOut)
    async def create_booking(
        self,
        fligth_path: Annotated[FlightPath, Depends(get_flight_path)],
        booking_passengers: Annotated[list[BookingPassengerCreate], Body()],
    ):
        return await self.bookings_service.create_booking(
            BookingCreate(fligth=fligth_path, passengers=booking_passengers)
        )

    @bookings_router.patch("/{booking_id}", response_model=BookingOneOut)
    async def edit_before_confirm_booking(
        self,
        booking_id: Annotated[str, Path()],
        booking_passengers: Annotated[list[BookingPassengerEdit], Body()],
    ):
        return await self.bookings_service.edit_booking_before_confirm(
            booking_id=booking_id, booking_passengers=booking_passengers
        )

    @bookings_router.post("/{booking_id}", response_model=BookingOneOut)
    async def confirm_booking(
        self,
        booking_id: Annotated[str, Path()],
    ):
        return await self.bookings_service.confirm_booking(booking_id)

    @bookings_router.delete("/{booking_id}", response_model=BookingOneOut)
    async def cancel_booking(
        self,
        booking_id: Annotated[str, Path()],
    ):
        return await self.bookings_service.cancel_booking(booking_id)

    @bookings_router.get("/{booking_id}", response_model=BookingOneOut)
    async def get_booking(
        self,
        booking_id: Annotated[str, Path()],
    ):
        return await self.bookings_service.get_booking(booking_id)

    @bookings_router.get("/", response_model=list[BookingManyOut])
    async def get_bookings(
        self,
    ):
        return await self.bookings_service.get_bookings()
