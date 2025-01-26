__all__ = [
    "OPEN_FLIGHTS_COUNTRIES_DATA",
    "OPEN_FLIGHTS_FOLDER_NAME",
    "OPEN_FLIGHTS_MAP_DATA",
    "OPEN_FLIGHTS_AIRPORTS_DATA",
]

OPEN_FLIGHTS_FOLDER_NAME = "openflights_data"
OPEN_FLIGHTS_COUNTRIES_DATA = f"./{OPEN_FLIGHTS_FOLDER_NAME}/countries.csv"
OPEN_FLIGHTS_AIRPORTS_DATA = f"./{OPEN_FLIGHTS_FOLDER_NAME}/airports.csv"

OPEN_FLIGHTS_MAP_DATA = {
    "\\N": None,
    "\\\\N": None,
    "N": False,
    "Y": True,
    "": None,
    " ": None,
    "y": True,
    "n": False,
}
