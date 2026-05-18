from flask import Blueprint

from app.api.v1.utils import get_db, json_response, parse_body, parse_pagination
from app.schemas.purchase_requests import (
    PurchaseRequestCreate,
    PurchaseRequestItemCreate,
    PurchaseRequestList,
    PurchaseRequestUpdate,
)
from app.services.purchase_requests import (
    add_purchase_request_item,
    create_purchase_request,
    delete_purchase_request,
    delete_purchase_request_item,
    get_purchase_request_read_by_no,
    list_purchase_requests,
    update_purchase_request,
)

router = Blueprint("purchase_requests", __name__)


@router.get("")
def read_purchase_requests():
    skip, limit = parse_pagination()
    total, items = list_purchase_requests(get_db(), skip=skip, limit=limit)
    return json_response(PurchaseRequestList(total=total, items=items))


@router.post("")
def create_purchase_request_endpoint():
    purchase_request = create_purchase_request(get_db(), parse_body(PurchaseRequestCreate))
    return json_response(purchase_request, 201)


@router.get("/<no>")
def read_purchase_request(no: str):
    return json_response(get_purchase_request_read_by_no(get_db(), no))


@router.patch("/<no>")
def update_purchase_request_endpoint(no: str):
    purchase_request = update_purchase_request(get_db(), no, parse_body(PurchaseRequestUpdate))
    return json_response(purchase_request)


@router.delete("/<no>")
def delete_purchase_request_endpoint(no: str):
    delete_purchase_request(get_db(), no)
    return json_response(None, 204)


@router.post("/<no>/items")
def add_purchase_request_item_endpoint(no: str):
    purchase_request = add_purchase_request_item(
        get_db(), no, parse_body(PurchaseRequestItemCreate)
    )
    return json_response(purchase_request, 201)


@router.delete("/<no>/items/<int:item_id>")
def delete_purchase_request_item_endpoint(no: str, item_id: int):
    delete_purchase_request_item(get_db(), no, item_id)
    return json_response(None, 204)
