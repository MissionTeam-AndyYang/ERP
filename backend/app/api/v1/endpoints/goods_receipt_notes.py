from flask import Blueprint

from app.api.v1.utils import get_db, json_response, parse_body, parse_pagination
from app.schemas.goods_receipt_notes import (
    GoodsReceiptNoteCreate,
    GoodsReceiptNoteList,
    GoodsReceiptNoteRead,
    GoodsReceiptNoteUpdate,
)
from app.services.goods_receipt_notes import (
    create_goods_receipt_note,
    delete_goods_receipt_note,
    get_goods_receipt_note_by_no,
    list_goods_receipt_notes,
    update_goods_receipt_note,
)

router = Blueprint("goods_receipt_notes", __name__)


@router.get("")
def read_goods_receipt_notes():
    skip, limit = parse_pagination()
    total, items = list_goods_receipt_notes(get_db(), skip=skip, limit=limit)
    payload = GoodsReceiptNoteList(
        total=total,
        items=[GoodsReceiptNoteRead.model_validate(item) for item in items],
    )
    return json_response(payload)


@router.post("")
def create_goods_receipt_note_endpoint():
    note = create_goods_receipt_note(get_db(), parse_body(GoodsReceiptNoteCreate))
    return json_response(GoodsReceiptNoteRead.model_validate(note), 201)


@router.get("/<no>")
def read_goods_receipt_note(no: str):
    note = get_goods_receipt_note_by_no(get_db(), no)
    return json_response(GoodsReceiptNoteRead.model_validate(note))


@router.patch("/<no>")
def update_goods_receipt_note_endpoint(no: str):
    note = update_goods_receipt_note(get_db(), no, parse_body(GoodsReceiptNoteUpdate))
    return json_response(GoodsReceiptNoteRead.model_validate(note))


@router.delete("/<no>")
def delete_goods_receipt_note_endpoint(no: str):
    delete_goods_receipt_note(get_db(), no)
    return json_response(None, 204)
