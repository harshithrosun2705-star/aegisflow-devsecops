from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title="SentinelOps Demo API",
    description="Backend application protected by the SentinelOps DevSecOps platform",
    version="1.0.0",
)


# --------------------------------------------------
# Data Model
# --------------------------------------------------

class OrderCreate(BaseModel):
    product: str = Field(
        min_length=2,
        max_length=100
    )

    quantity: int = Field(
        gt=0,
        le=100
    )


# Temporary in-memory database
orders = {}


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "service": "sentinelops-api",
        "version": "1.0.0",
        "status": "running",
    }


# --------------------------------------------------
# Health Endpoints
# --------------------------------------------------

@app.get("/health/live")
def liveness():
    return {
        "status": "alive"
    }


@app.get("/health/ready")
def readiness():
    return {
        "status": "ready"
    }


# --------------------------------------------------
# Create Order
# --------------------------------------------------

@app.post(
    "/orders",
    status_code=status.HTTP_201_CREATED
)
def create_order(order: OrderCreate):

    order_id = str(uuid4())

    new_order = {
        "order_id": order_id,
        "product": order.product,
        "quantity": order.quantity,
    }

    orders[order_id] = new_order

    return new_order


# --------------------------------------------------
# Get All Orders
# --------------------------------------------------

@app.get("/orders")
def get_orders():
    return {
        "total": len(orders),
        "orders": list(orders.values()),
    }


# --------------------------------------------------
# Get Specific Order
# --------------------------------------------------

@app.get("/orders/{order_id}")
def get_order(order_id: str):

    if order_id not in orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return orders[order_id]


# --------------------------------------------------
# Delete Order
# --------------------------------------------------

@app.delete(
    "/orders/{order_id}",
    status_code=status.HTTP_200_OK
)
def delete_order(order_id: str):

    if order_id not in orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    deleted_order = orders.pop(order_id)

    return {
        "message": "Order deleted successfully",
        "order": deleted_order,
    }
