import datetime

from app import models
from app.api import CreateOrderRequestModel
from app.db.setup import db_session
from app.stock_exchange import place_order
from app.types import Order


def process_create_order_request(order_request: CreateOrderRequestModel) -> Order:
    with db_session.begin() as db:
        db_order = models.Order(
            **order_request.dict(by_alias=True), created_at=datetime.datetime.utcnow()
        )
        db.add(db_order)
        db.flush()

        order = Order(**db_order.__dict__)
        place_order(order)

    return order
