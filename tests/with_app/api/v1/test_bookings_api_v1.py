import pytest
from fastapi.testclient import TestClient

from tbsky_booking.models import Booking
from tbsky_booking.repository import BookingsRepository
from tests.with_app.models.bookings import BookingFactory


class TestBookingsResource:
    @pytest.mark.asyncio
    async def test_get_bookings(self, client: TestClient):
        # given
        # when
        response = client.get("api/v1/bookings/")
        # then
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_get_booking(self, client: TestClient, user_id: str):
        # given
        booking_repo = BookingsRepository(user_id=user_id)
        booking: Booking = BookingFactory.build(user_id=user_id)
        await booking_repo.add(booking)
        # when
        response = client.get(f"api/v1/bookings/{booking.booking_id}")
        # then
        assert response.status_code == 200
        assert response.json()["booking_id"] == str(booking.booking_id)

    async def test_confirm_booking(self, client: TestClient, user_id: str):
        # given
        booking_repo = BookingsRepository(user_id=user_id)
        booking: Booking = BookingFactory.build(user_id=user_id)
        await booking_repo.add(booking)
        # when
        response = client.post(f"api/v1/bookings/{booking.booking_id}/confirm")
        # then
        assert response.status_code == 200
        assert response.json()["booking_id"] == str(booking.booking_id)

    async def test_cancel_booking(self, client: TestClient, user_id: str):
        # given
        booking_repo = BookingsRepository(user_id=user_id)
        booking: Booking = BookingFactory.build(user_id=user_id)
        await booking_repo.add(booking)
        # when
        response = client.delete(f"api/v1/bookings/{booking.booking_id}")
        # then
        assert response.status_code == 200
        assert response.json()["booking_id"] == str(booking.booking_id)
