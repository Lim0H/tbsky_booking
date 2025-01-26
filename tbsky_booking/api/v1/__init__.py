from fastapi import APIRouter

from .bookings import bookings_router
from .flights import flights_router

routers: list[APIRouter] = [flights_router, bookings_router]
