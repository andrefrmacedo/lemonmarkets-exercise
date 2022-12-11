from sqlalchemy import Column, DateTime, Float, Integer, String

from app.db.setup import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False)
    type = Column(String, nullable=False)
    side = Column(String, nullable=False)
    instrument = Column(String(12), nullable=False)
    limit_price = Column(Float(precision=2, decimal_return_scale=2), nullable=True)
    quantity = Column(Integer, nullable=False)
