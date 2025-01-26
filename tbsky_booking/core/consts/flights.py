from enum import Enum, StrEnum, auto
from typing import TYPE_CHECKING, Any

from fast_flights import flights_pb2 as PB

if TYPE_CHECKING:
    PB: Any

__all__ = [
    "FlightsSourceEnum",
    "GoogleSeatEnum",
    "GoogleTripEnum",
    "SeatEnum",
    "MAP_GOOGLE_SEAT_ENUM",
    "RYANAIR_API_URL",
    "SeatNumberEnum",
    "RYANAIR_HOME_URL",
    "RYANAIR_AVAILABLE_ROUTES_API_URL",
    "RYANAIR_AVAILABLE_DATES_API_URL",
    "PassengerTypeEnum",
    "RYANAIR_AVAILABLE_FLIGHTS_API_URL",
]


class FlightsSourceEnum(StrEnum):
    GOOGLE = auto()
    RYANAIR = auto()


class GoogleTripEnum(Enum):
    ROUND_TRIP = PB.Trip.ROUND_TRIP
    ONE_WAY = PB.Trip.ONE_WAY
    MULTI_CITY = PB.Trip.MULTI_CITY


class GoogleSeatEnum(Enum):
    ECONOMY = PB.Seat.ECONOMY
    PREMIUM_ECONOMY = PB.Seat.PREMIUM_ECONOMY
    BUSINESS = PB.Seat.BUSINESS
    FIRST = PB.Seat.FIRST


class SeatEnum(str, Enum):
    ECONOMY = "economy"
    PREMIUM_ECONOMY = "premium-economy"
    BUSINESS = "business"
    FIRST = "first"


class PassengerTypeEnum(str, Enum):
    ADULT = "adult"
    CHILD = "child"
    INFANT = "infant"
    TEEN = "teen"


class SeatNumberEnum(str, Enum):
    # ECONOMY
    ZERO_TWO_A = "02A"
    ZERO_TWO_B = "02B"
    ZERO_TWO_C = "02C"
    ZERO_TWO_D = "02D"
    ZERO_TWO_E = "02E"
    ZERO_TWO_F = "02F"
    THREE_TWO_A = "32A"
    THREE_TWO_B = "32B"
    THREE_TWO_C = "32C"
    THREE_TWO_D = "32D"
    THREE_TWO_E = "32E"
    THREE_TWO_F = "32F"
    # PREMIUM_ECONOMY
    FOUR_TWO_A = "42A"
    FOUR_TWO_B = "42B"
    FOUR_TWO_C = "42C"
    FOUR_TWO_D = "42D"
    FOUR_TWO_E = "42E"
    FOUR_TWO_F = "42F"
    FIVE_TWO_A = "52A"
    FIVE_TWO_B = "52B"
    FIVE_TWO_C = "52C"
    FIVE_TWO_D = "52D"
    # BUSINESS
    SIX_TWO_A = "62A"
    SIX_TWO_B = "62B"
    SIX_TWO_C = "62C"
    SIX_TWO_D = "62D"
    SIX_TWO_E = "62E"
    SIX_TWO_F = "62F"
    # FIRST
    SEVEN_TWO_A = "72A"
    SEVEN_TWO_B = "72B"
    SEVEN_TWO_C = "72C"
    SEVEN_TWO_D = "72D"
    SEVEN_TWO_E = "72E"
    SEVEN_TWO_F = "72F"


MAP_GOOGLE_SEAT_ENUM = {
    SeatEnum.ECONOMY: GoogleSeatEnum.ECONOMY,
    SeatEnum.PREMIUM_ECONOMY: GoogleSeatEnum.PREMIUM_ECONOMY,
    SeatEnum.BUSINESS: GoogleSeatEnum.BUSINESS,
    SeatEnum.FIRST: GoogleSeatEnum.FIRST,
}


RYANAIR_HOME_URL = "https://www.ryanair.com/en/en"
RYANAIR_API_URL = "https://www.ryanair.com/api/"

RYANAIR_AVAILABLE_DATES_API_URL = (
    RYANAIR_API_URL + "farfnd/v4/oneWayFares/{origin}/{destination}/availabilities"
)
RYANAIR_AVAILABLE_ROUTES_API_URL = (
    RYANAIR_API_URL + "views/locate/searchWidget/routes/pl/airport/{}"
)
RYANAIR_AVAILABLE_FLIGHTS_API_URL = RYANAIR_API_URL + "booking/v4/en-en/availability"
