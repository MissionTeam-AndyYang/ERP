from flask import Blueprint

from app.api.v1.utils import get_db, json_response, parse_body, parse_pagination
from app.schemas.inventory_records import (
    InventoryRecordCreate,
    InventoryRecordList,
    InventoryRecordRead,
    InventoryRecordUpdate,
)
from app.services.inventory_records import (
    create_inventory_record,
    delete_inventory_record,
    get_inventory_record_by_id,
    list_inventory_records,
    update_inventory_record,
)

router = Blueprint("inventory_records", __name__)


@router.get("")
def read_inventory_records():
    skip, limit = parse_pagination()
    total, items = list_inventory_records(get_db(), skip=skip, limit=limit)
    payload = InventoryRecordList(
        total=total,
        items=[InventoryRecordRead.model_validate(item) for item in items],
    )
    return json_response(payload)


@router.post("")
def create_inventory_record_endpoint():
    inventory_record = create_inventory_record(get_db(), parse_body(InventoryRecordCreate))
    return json_response(InventoryRecordRead.model_validate(inventory_record), 201)


@router.get("/<int:record_id>")
def read_inventory_record(record_id: int):
    inventory_record = get_inventory_record_by_id(get_db(), record_id)
    return json_response(InventoryRecordRead.model_validate(inventory_record))


@router.patch("/<int:record_id>")
def update_inventory_record_endpoint(record_id: int):
    inventory_record = update_inventory_record(
        get_db(), record_id, parse_body(InventoryRecordUpdate)
    )
    return json_response(InventoryRecordRead.model_validate(inventory_record))


@router.delete("/<int:record_id>")
def delete_inventory_record_endpoint(record_id: int):
    delete_inventory_record(get_db(), record_id)
    return json_response(None, 204)
