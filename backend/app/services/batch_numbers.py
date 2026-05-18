from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.ewdb import BatchNumber, GoodsReceiptNote
from app.schemas.batch_numbers import BatchNumberCreate, BatchNumberUpdate


def list_batch_numbers(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 50,
) -> tuple[int, list[BatchNumber]]:
    total = db.scalar(select(func.count()).select_from(BatchNumber)) or 0
    items = list(
        db.scalars(
            select(BatchNumber).order_by(BatchNumber.id.desc()).offset(skip).limit(limit)
        ).all()
    )
    return total, items


def get_batch_number_by_no(db: Session, no: str) -> BatchNumber:
    batch_number = db.scalar(select(BatchNumber).where(BatchNumber.no == no))
    if batch_number is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Batch number '{no}' was not found.",
        )
    return batch_number


def _ensure_goods_receipt_note_exists(db: Session, ref_no: str | None) -> None:
    if not ref_no:
        return
    goods_receipt_note = db.scalar(select(GoodsReceiptNote).where(GoodsReceiptNote.no == ref_no))
    if goods_receipt_note is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Goods receipt note '{ref_no}' was not found.",
        )


def create_batch_number(db: Session, payload: BatchNumberCreate) -> BatchNumber:
    existing = db.scalar(select(BatchNumber).where(BatchNumber.no == payload.no))
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Batch number '{payload.no}' already exists.",
        )

    _ensure_goods_receipt_note_exists(db, payload.ref_no)
    batch_number = BatchNumber(**payload.model_dump())
    db.add(batch_number)
    db.commit()
    db.refresh(batch_number)
    return batch_number


def update_batch_number(
    db: Session,
    no: str,
    payload: BatchNumberUpdate,
) -> BatchNumber:
    batch_number = get_batch_number_by_no(db, no)
    data = payload.model_dump(exclude_unset=True)

    next_no = data.get("no")
    if next_no and next_no != no:
        existing = db.scalar(select(BatchNumber).where(BatchNumber.no == next_no))
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Batch number '{next_no}' already exists.",
            )

    if "ref_no" in data:
        _ensure_goods_receipt_note_exists(db, data["ref_no"])

    for field, value in data.items():
        setattr(batch_number, field, value)

    db.commit()
    db.refresh(batch_number)
    return batch_number


def delete_batch_number(db: Session, no: str) -> None:
    batch_number = get_batch_number_by_no(db, no)
    db.delete(batch_number)
    db.commit()
