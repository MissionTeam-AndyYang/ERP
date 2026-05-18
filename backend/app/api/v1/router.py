from fastapi import APIRouter

from app.api.v1.endpoints import (
    batch_numbers,
    goods_receipt_notes,
    health,
    inventory_records,
    product_orders,
    purchase_orders,
    purchase_requests,
    workflows,
)

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(product_orders.router, prefix="/product-orders", tags=["product-orders"])
api_router.include_router(
    purchase_requests.router,
    prefix="/purchase-requests",
    tags=["purchase-requests"],
)
api_router.include_router(
    purchase_orders.router, prefix="/purchase-orders", tags=["purchase-orders"]
)
api_router.include_router(
    goods_receipt_notes.router,
    prefix="/goods-receipt-notes",
    tags=["goods-receipt-notes"],
)
api_router.include_router(batch_numbers.router, prefix="/batch-numbers", tags=["batch-numbers"])
api_router.include_router(
    inventory_records.router,
    prefix="/inventory-records",
    tags=["inventory-records"],
)
api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
