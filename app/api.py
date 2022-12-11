from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from app.schemas import CreateOrderRequestModel, CreateOrderResponseModel
from app.services.create_order import process_create_order_request
from app.stock_exchange import OrderPlacementError

app = FastAPI()


@app.post(
    "/orders",
    status_code=201,
    response_model=CreateOrderResponseModel,
    response_model_by_alias=True,
    responses={
        status.HTTP_201_CREATED: {"description": "Order placed successfully"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error while placing order"
        },
    },
)
async def create_order(model: CreateOrderRequestModel):
    try:
        order_created = process_create_order_request(model)
        return order_created
    except OrderPlacementError or ValueError:
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error while placing the order"},
        )
