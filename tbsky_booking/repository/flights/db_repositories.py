import csv
import logging
from itertools import groupby

from more_itertools import filter_map
from tbsky_booking.core import (
    OPEN_FLIGHTS_AIRPORTS_DATA,
    OPEN_FLIGHTS_COUNTRIES_DATA,
    OPEN_FLIGHTS_MAP_DATA,
    BaseDbRepository,
    OpenFlightsAirPortDict,
    OpenFlightsCountryDict,
)
from tbsky_booking.models import AirPort, Country, Flight
from tbsky_booking.utils import first_or_none

log = logging.getLogger(__file__)


class BaseFlightsRepository[T](BaseDbRepository[T]):
    async def fill_repository(self):
        raise NotImplementedError


__all__ = [
    "BaseFlightsRepository",
    "CountriesRepository",
    "AirPortsRepository",
    "FlightsRepository",
]


class CountriesRepository(BaseFlightsRepository[Country]):
    model = Country

    async def get_dict_list(self):
        countries = await self.get()
        return {country.full_country_name: [country] for country in countries}

    async def fill_repository(self):
        file = open(OPEN_FLIGHTS_COUNTRIES_DATA)
        csv_file = csv.DictReader(file)
        countries: list[Country] = []
        save_countries = await self.get_dict()
        for country_name, country_dicts_iter in groupby(
            filter_map(
                lambda x: (
                    None
                    if save_countries.get(x["name"])
                    else OpenFlightsCountryDict(**x)
                ),
                csv_file,
            ),
            lambda x: x["name"],
        ):
            country_dicts = [x for x in country_dicts_iter]
            country_dict = {
                "name": country_name,
                "iso_code": first_or_none(
                    [
                        x["iso_code"]
                        for x in country_dicts
                        if OPEN_FLIGHTS_MAP_DATA.get(x["iso_code"], x["iso_code"])
                    ]
                ),
                "dafif_code": [
                    x["dafif_code"]
                    for x in country_dicts
                    if OPEN_FLIGHTS_MAP_DATA.get(x["dafif_code"], x["dafif_code"])
                ],
            }

            countries.append(
                Country(
                    full_country_name=country_dict["name"],
                    iso_code=country_dict["iso_code"],
                    dafif_code=country_dict["dafif_code"],
                ),
            )
        await self.add_massive(countries)


class AirPortsRepository(BaseFlightsRepository[AirPort]):
    model = AirPort

    async def get_dict_list(self):
        airports = await self.get()
        return {airport.airport_iata: [airport] for airport in airports}

    async def fill_repository(self):
        country_repo = CountriesRepository()
        countries_dict = await country_repo.get_dict()
        save_airports = await self.get_dict()
        file = open(OPEN_FLIGHTS_AIRPORTS_DATA)
        csv_file = csv.DictReader(file)
        airports: list[AirPort] = []
        for airport_dict in filter_map(
            lambda x: (
                None if save_airports.get(x["IATA"]) else OpenFlightsAirPortDict(**x)
            ),
            csv_file,
        ):
            country = countries_dict.setdefault(
                airport_dict["Country"],
                Country(full_country_name=airport_dict["Country"]),
            )
            airports.append(
                AirPort(
                    airport_name=airport_dict["Name"],
                    airport_city=airport_dict["City"],
                    airport_iata=OPEN_FLIGHTS_MAP_DATA.get(
                        airport_dict["IATA"], airport_dict["IATA"]
                    ),
                    airport_icao=OPEN_FLIGHTS_MAP_DATA.get(
                        airport_dict["ICAO"], airport_dict["ICAO"]
                    ),
                    latitude=float(airport_dict["Latitude"]),
                    longitude=float(airport_dict["Longitude"]),
                    altitude=float(airport_dict["Altitude"]),
                    timezone=(
                        float(airport_dict["Timezone"])
                        if OPEN_FLIGHTS_MAP_DATA.get(
                            airport_dict["Timezone"], airport_dict["Timezone"]
                        )
                        else None
                    ),
                    airport_country=country,
                    dst=airport_dict["DST"],
                    tz_database_timezone=airport_dict["Tz_database_timezone"],
                ),
            )
        await self.add_massive(airports)


class FlightsRepository(BaseFlightsRepository[Flight]):
    model = Flight
