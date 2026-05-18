from flask import Blueprint

from app.api.v1.utils import get_db, json_response, parse_body, parse_pagination
from app.schemas.product_orders import (
    ProductOrderCreate,
    ProductOrderList,
    ProductOrderRead,
    ProductOrderUpdate,
)
from app.services.product_orders import (
    create_product_order,
    delete_product_order,
    get_product_order_by_no,
    list_product_orders,
    update_product_order,
)

router = Blueprint("product_orders", __name__)


@router.get("")
def read_product_orders():
    skip, limit = parse_pagination()
    total, items = list_product_orders(get_db(), skip=skip, limit=limit)
    payload = ProductOrderList(
        total=total,
        items=[ProductOrderRead.model_validate(item) for item in items],
    )
    return json_response(payload)


@router.post("")
def create_product_order_endpoint():
    product_order = create_product_order(get_db(), parse_body(ProductOrderCreate))
    return json_response(ProductOrderRead.model_validate(product_order), 201)


@router.get("/<no>")
def read_product_order(no: str):
    product_order = get_product_order_by_no(get_db(), no)
    return json_response(ProductOrderRead.model_validate(product_order))


@router.patch("/<no>")
def update_product_order_endpoint(no: str):
    product_order = update_product_order(get_db(), no, parse_body(ProductOrderUpdate))
    return json_response(ProductOrderRead.model_validate(product_order))


@router.delete("/<no>")
def delete_product_order_endpoint(no: str):
    delete_product_order(get_db(), no)
    return json_response(None, 204)
