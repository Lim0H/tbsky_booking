from typing import Optional, TypedDict

__all__ = [
    "OpenFlightsCountryDict",
    "OpenFlightsAirPortDict",
]


class OpenFlightsCountryDict(TypedDict):
    name: str  # Full name of the country or territory.
    iso_code: Optional[
        str
    ]  # Unique two-letter ISO 3166-1 code for the country or territory.
    dafif_code: Optional[
        str
    ]  # FIPS country codes as used in DAFIF.Obsolete and primarily of historical interested.


class OpenFlightsAirPortDict(TypedDict):
    Airport_ID: str
    Name: str
    City: str
    Country: str
    IATA: str
    ICAO: str
    Latitude: float
    Longitude: float
    Altitude: float
    Timezone: float
    DST: str
    Tz_database_timezone: str
    Type: str
    Source: str  # Source of this data. "OurAirports" for data sourced from OurAirports, "Legacy" for old data not matched to OurAirports (mostly DAFIF), "User" for unverified user contributions. In airports.csv, only source=OurAirports is included.
