import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from tbsky_booking.api import init_fastapi_server


@pytest.fixture
def app() -> FastAPI:
    return init_fastapi_server()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
