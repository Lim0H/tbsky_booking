import factory
import factory.fuzzy
from factory.alchemy import SQLAlchemyModelFactory

from tbsky_booking.core.consts.flights import SeatNumberEnum
from tbsky_booking.models import Booking, BookingPassenger
from tests.with_app.models.flights import FlightFactory

__all__ = ["BookingFactory", "BookingPassengerFactory"]


class BookingPassengerFactory(SQLAlchemyModelFactory):
    class Meta:
        model = BookingPassenger

    first_name: str = factory.Faker("first_name")
    last_name: str = factory.Faker("last_name")

    seat_number = factory.fuzzy.FuzzyChoice(list(SeatNumberEnum))
    passport_number = factory.Faker("ssn")
    passport_expire_date = factory.Faker("date_object")


class BookingFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Booking

    booking_id = factory.Faker("uuid4")

    # booking_passengers = factory.List(
    #     [
    #         factory.SubFactory(
    #             BookingPassenger, booking_id=factory.SelfAttribute("...booking_id")
    #         )
    #         for _ in range(2)
    #     ]
    # )
    flight = factory.SubFactory(FlightFactory)
