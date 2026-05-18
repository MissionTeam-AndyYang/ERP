from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
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


router = APIRouter()


@router.get("", response_model=GoodsReceiptNoteList)
def read_goods_receipt_notes(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> GoodsReceiptNoteList:
    total, items = list_goods_receipt_notes(db, skip=skip, limit=limit)
    return GoodsReceiptNoteList(total=total, items=items)


@router.post("", response_model=GoodsReceiptNoteRead, status_code=status.HTTP_201_CREATED)
def create_goods_receipt_note_endpoint(
    payload: GoodsReceiptNoteCreate,
    db: Session = Depends(get_db),
) -> GoodsReceiptNoteRead:
    return create_goods_receipt_note(db, payload)


@router.get("/{no}", response_model=GoodsReceiptNoteRead)
def read_goods_receipt_note(
    no: str,
    db: Session = Depends(get_db),
) -> GoodsReceiptNoteRead:
    return get_goods_receipt_note_by_no(db, no)


@router.patch("/{no}", response_model=GoodsReceiptNoteRead)
def update_goods_receipt_note_endpoint(
    no: str,
    payload: GoodsReceiptNoteUpdate,
    db: Session = Depends(get_db),
) -> GoodsReceiptNoteRead:
    return update_goods_receipt_note(db, no, payload)


@router.delete("/{no}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goods_receipt_note_endpoint(
    no: str,
    db: Session = Depends(get_db),
) -> Response:
    delete_goods_receipt_note(db, no)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
