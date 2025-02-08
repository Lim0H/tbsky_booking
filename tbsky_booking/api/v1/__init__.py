from fastapi import APIRouter

from .bookings import bookings_router
from .flights import airports_router, countries_router, flights_router

routers: list[APIRouter] = [
    flights_router,
    bookings_router,
    countries_router,
    airports_router,
]
