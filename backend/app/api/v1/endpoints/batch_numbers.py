from flask import Blueprint

from app.api.v1.utils import get_db, json_response, parse_body, parse_pagination
from app.schemas.batch_numbers import (
    BatchNumberCreate,
    BatchNumberList,
    BatchNumberRead,
    BatchNumberUpdate,
)
from app.services.batch_numbers import (
    create_batch_number,
    delete_batch_number,
    get_batch_number_by_no,
    list_batch_numbers,
    update_batch_number,
)

router = Blueprint("batch_numbers", __name__)


@router.get("")
def read_batch_numbers():
    skip, limit = parse_pagination()
    total, items = list_batch_numbers(get_db(), skip=skip, limit=limit)
    payload = BatchNumberList(
        total=total,
        items=[BatchNumberRead.model_validate(item) for item in items],
    )
    return json_response(payload)


@router.post("")
def create_batch_number_endpoint():
    batch_number = create_batch_number(get_db(), parse_body(BatchNumberCreate))
    return json_response(BatchNumberRead.model_validate(batch_number), 201)


@router.get("/<no>")
def read_batch_number(no: str):
    batch_number = get_batch_number_by_no(get_db(), no)
    return json_response(BatchNumberRead.model_validate(batch_number))


@router.patch("/<no>")
def update_batch_number_endpoint(no: str):
    batch_number = update_batch_number(get_db(), no, parse_body(BatchNumberUpdate))
    return json_response(BatchNumberRead.model_validate(batch_number))


@router.delete("/<no>")
def delete_batch_number_endpoint(no: str):
    delete_batch_number(get_db(), no)
    return json_response(None, 204)
