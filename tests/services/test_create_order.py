import pytest

from app.db.setup import db_session
from app.models import Order
from app.schemas import CreateOrderRequestModel
from app.services.create_order import process_create_order_request
from app.stock_exchange import OrderPlacementError


@pytest.fixture
def order_request() -> CreateOrderRequestModel:
    return CreateOrderRequestModel(
        type="market",
        side="sell",
        instrument="ABCDEFGHIJKL",
        limit_price=0,
        quantity=1,
    )


def test_process_create_order_request_should_create_order_when_stock_exchange_call_successful(
    place_order_mock, order_request
):
    process_create_order_request(order_request)

    with db_session.begin() as db:
        orders = db.query(Order).all()
        created_order = orders[0]

        assert len(orders) == 1
        assert created_order.instrument == "ABCDEFGHIJKL"
        assert created_order.type == "market"
        assert created_order.side == "sell"
        assert created_order.quantity == 1
        assert created_order.limit_price == 0


def test_process_create_order_request_should_not_create_order_when_stock_exchange_call_not_successful(
    place_order_mock, order_request
):
    place_order_mock.side_effect = OrderPlacementError()
    with pytest.raises(OrderPlacementError):
        process_create_order_request(order_request)

    with db_session.begin() as db:
        orders = db.query(Order).all()

        assert len(orders) == 0
