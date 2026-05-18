from flask import Blueprint

from app.api.v1.utils import get_db, json_response, parse_body, parse_pagination
from app.schemas.purchase_orders import (
    PurchaseOrderCreate,
    PurchaseOrderList,
    PurchaseOrderRead,
    PurchaseOrderUpdate,
)
from app.services.purchase_orders import (
    create_purchase_order,
    delete_purchase_order,
    get_purchase_order_by_no,
    list_purchase_orders,
    update_purchase_order,
)

router = Blueprint("purchase_orders", __name__)


@router.get("")
def read_purchase_orders():
    skip, limit = parse_pagination()
    total, items = list_purchase_orders(get_db(), skip=skip, limit=limit)
    payload = PurchaseOrderList(
        total=total,
        items=[PurchaseOrderRead.model_validate(item) for item in items],
    )
    return json_response(payload)


@router.post("")
def create_purchase_order_endpoint():
    purchase_order = create_purchase_order(get_db(), parse_body(PurchaseOrderCreate))
    return json_response(PurchaseOrderRead.model_validate(purchase_order), 201)


@router.get("/<no>")
def read_purchase_order(no: str):
    purchase_order = get_purchase_order_by_no(get_db(), no)
    return json_response(PurchaseOrderRead.model_validate(purchase_order))


@router.patch("/<no>")
def update_purchase_order_endpoint(no: str):
    purchase_order = update_purchase_order(get_db(), no, parse_body(PurchaseOrderUpdate))
    return json_response(PurchaseOrderRead.model_validate(purchase_order))


@router.delete("/<no>")
def delete_purchase_order_endpoint(no: str):
    delete_purchase_order(get_db(), no)
    return json_response(None, 204)
