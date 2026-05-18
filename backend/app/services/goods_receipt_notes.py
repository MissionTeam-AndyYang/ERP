from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.ewdb import GoodsReceiptNote, PurchaseOrder
from app.schemas.goods_receipt_notes import GoodsReceiptNoteCreate, GoodsReceiptNoteUpdate


def list_goods_receipt_notes(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 50,
) -> tuple[int, list[GoodsReceiptNote]]:
    total = db.scalar(select(func.count()).select_from(GoodsReceiptNote)) or 0
    items = list(
        db.scalars(
            select(GoodsReceiptNote).order_by(GoodsReceiptNote.id.desc()).offset(skip).limit(limit)
        ).all()
    )
    return total, items


def get_goods_receipt_note_by_no(db: Session, no: str) -> GoodsReceiptNote:
    goods_receipt_note = db.scalar(select(GoodsReceiptNote).where(GoodsReceiptNote.no == no))
    if goods_receipt_note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Goods receipt note '{no}' was not found.",
        )
    return goods_receipt_note


def _ensure_purchase_order_exists(db: Session, purchase_order_no: str | None) -> None:
    if not purchase_order_no:
        return
    purchase_order = db.scalar(select(PurchaseOrder).where(PurchaseOrder.no == purchase_order_no))
    if purchase_order is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Purchase order '{purchase_order_no}' was not found.",
        )


def create_goods_receipt_note(
    db: Session,
    payload: GoodsReceiptNoteCreate,
) -> GoodsReceiptNote:
    existing = db.scalar(select(GoodsReceiptNote).where(GoodsReceiptNote.no == payload.no))
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Goods receipt note '{payload.no}' already exists.",
        )

    _ensure_purchase_order_exists(db, payload.purchase_order_no)
    goods_receipt_note = GoodsReceiptNote(**payload.model_dump())
    db.add(goods_receipt_note)
    db.commit()
    db.refresh(goods_receipt_note)
    return goods_receipt_note


def update_goods_receipt_note(
    db: Session,
    no: str,
    payload: GoodsReceiptNoteUpdate,
) -> GoodsReceiptNote:
    goods_receipt_note = get_goods_receipt_note_by_no(db, no)
    data = payload.model_dump(exclude_unset=True)

    next_no = data.get("no")
    if next_no and next_no != no:
        existing = db.scalar(select(GoodsReceiptNote).where(GoodsReceiptNote.no == next_no))
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Goods receipt note '{next_no}' already exists.",
            )

    if "purchase_order_no" in data:
        _ensure_purchase_order_exists(db, data["purchase_order_no"])

    for field, value in data.items():
        setattr(goods_receipt_note, field, value)

    db.commit()
    db.refresh(goods_receipt_note)
    return goods_receipt_note


def delete_goods_receipt_note(db: Session, no: str) -> None:
    goods_receipt_note = get_goods_receipt_note_by_no(db, no)
    db.delete(goods_receipt_note)
    db.commit()
