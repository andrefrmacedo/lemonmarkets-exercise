import pytest as pytest
from sqlalchemy import MetaData
from starlette.testclient import TestClient

from app.api import app
from app.db.setup import Base, engine

meta = MetaData()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def db_clean() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield


@pytest.fixture
def place_order_mock(mocker) -> None:
    yield mocker.patch("app.services.create_order.place_order")
