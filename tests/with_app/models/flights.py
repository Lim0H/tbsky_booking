import factory
from factory.alchemy import SQLAlchemyModelFactory

from tbsky_booking.models import AirPort, Country, Flight

__all__ = ["FlightFactory", "AirPortFactory", "CountryFactory"]


class CountryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Country

    dafif_code = factory.List([factory.Faker("country_code")])
    full_country_name = factory.Faker("country_code")
    iso_code = factory.Faker("country_code")


class AirPortFactory(SQLAlchemyModelFactory):
    class Meta:
        model = AirPort

    airport_name = factory.Faker("city")
    airport_city = factory.Faker("city")
    airport_country = factory.SubFactory(CountryFactory)

    airport_iata = None
    airport_icao = None
    latitude = 0
    longitude = 0
    altitude = 0
    timezone = None
    dst = factory.Faker("timezone")
    tz_database_timezone = factory.Faker("timezone")


class FlightFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Flight

    trip_key = ""
    origin_airport = factory.SubFactory(AirPortFactory)
    destination_airport = factory.SubFactory(AirPortFactory)

    date_in = factory.Faker("date_object")
    date_out = factory.Faker("date_object")
    duration_m = None
