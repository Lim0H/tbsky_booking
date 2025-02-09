import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from tbsky_booking.api import init_fastapi_server
from tbsky_booking.core import (
    get_async_engine,
    get_user_id_by_access_token,
)


@pytest.fixture
def app() -> FastAPI:
    return init_fastapi_server()


@pytest.fixture
def user_id() -> str:
    return "user_id"


@pytest.fixture(scope="session")
async def db_session():
    from tbsky_booking import models  # noqa

    async_engine = get_async_engine()
    async with async_engine.begin() as async_conn:
        from sqlmodel import SQLModel

        await async_conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with async_engine.begin() as async_conn:
        from sqlmodel import SQLModel

        await async_conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture
def client(app: FastAPI, user_id, db_session) -> TestClient:
    app.dependency_overrides[get_user_id_by_access_token] = lambda: user_id
    return TestClient(app)
