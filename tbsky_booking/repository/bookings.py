from tbsky_booking.core import BaseDbRepository
from tbsky_booking.models import Booking, BookingPassenger

__all__ = ["BookingsRepository", "BookingPassengersRepository"]


class BookingPassengersRepository(BaseDbRepository[BookingPassenger]):
    model = BookingPassenger


class BookingsRepository(BaseDbRepository[Booking]):
    model = Booking
