from unittest.mock import ANY

import pytest
from fastapi import status

from app.db.setup import db_session
from app.models import Order
from app.stock_exchange import OrderPlacementError


@pytest.fixture
def valid_request_body():
    return {
        "type": "market",
        "side": "buy",
        "instrument": "123456789012",
        "limit_price": 0,
        "quantity": 1,
    }


def test_create_order_should_return_201_when_successfully_created(
    client, place_order_mock, valid_request_body
):
    expected_response_body = {
        "type": "market",
        "created_at": ANY,
        "side": "buy",
        "instrument": "123456789012",
        "limit_price": 0,
        "quantity": 1,
    }

    response = client.post("/orders", json=valid_request_body)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == expected_response_body


def test_create_order_should_return_500_when_something_fails(
    client, place_order_mock, valid_request_body
):
    place_order_mock.side_effect = OrderPlacementError()
    expected_response_body = {
        "message": "Internal server error while placing the order"
    }

    response = client.post("/orders", json=valid_request_body)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == expected_response_body


def test_create_order_should_save_order_in_db_when_successful(
    client, place_order_mock, valid_request_body
):
    client.post("/orders", json=valid_request_body)

    with db_session.begin() as db:
        orders = db.query(Order).all()
        created_order = orders[0]

        assert len(orders) == 1
        assert created_order.instrument == "123456789012"
        assert created_order.type == "market"
        assert created_order.side == "buy"
        assert created_order.quantity == 1
        assert created_order.limit_price == 0


def test_create_order_should_not_save_order_in_db_when_not_successful(
    client, place_order_mock, valid_request_body
):
    place_order_mock.side_effect = OrderPlacementError()
    client.post("/orders", json=valid_request_body)

    with db_session.begin() as db:
        orders = db.query(Order).all()

        assert len(orders) == 0
