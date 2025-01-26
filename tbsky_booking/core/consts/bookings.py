from enum import Enum, auto

__all__ = ["BookingStatusEnum"]


class BookingStatusEnum(str, Enum):
    CREATED = auto()
    CONFIRMED = auto()
    CANCELLED = auto()
