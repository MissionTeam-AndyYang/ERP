from flask import Blueprint

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

api_router = Blueprint("api_v1", __name__)
api_router.register_blueprint(health.router, url_prefix="/health")
api_router.register_blueprint(product_orders.router, url_prefix="/product-orders")
api_router.register_blueprint(purchase_requests.router, url_prefix="/purchase-requests")
api_router.register_blueprint(purchase_orders.router, url_prefix="/purchase-orders")
api_router.register_blueprint(goods_receipt_notes.router, url_prefix="/goods-receipt-notes")
api_router.register_blueprint(batch_numbers.router, url_prefix="/batch-numbers")
api_router.register_blueprint(inventory_records.router, url_prefix="/inventory-records")
api_router.register_blueprint(workflows.router, url_prefix="/workflows")
