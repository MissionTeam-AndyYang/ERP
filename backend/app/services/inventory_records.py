from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.ewdb import BatchNumber, InventoryRecord
from app.schemas.inventory_records import InventoryRecordCreate, InventoryRecordUpdate


def list_inventory_records(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 50,
) -> tuple[int, list[InventoryRecord]]:
    total = db.scalar(select(func.count()).select_from(InventoryRecord)) or 0
    items = list(
        db.scalars(
            select(InventoryRecord).order_by(InventoryRecord.id.desc()).offset(skip).limit(limit)
        ).all()
    )
    return total, items


def get_inventory_record_by_id(db: Session, record_id: int) -> InventoryRecord:
    inventory_record = db.get(InventoryRecord, record_id)
    if inventory_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory record '{record_id}' was not found.",
        )
    return inventory_record


def _ensure_batch_number_exists(db: Session, batch_number_no: str | None) -> None:
    if not batch_number_no:
        return
    batch_number = db.scalar(select(BatchNumber).where(BatchNumber.no == batch_number_no))
    if batch_number is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Batch number '{batch_number_no}' was not found.",
        )


def create_inventory_record(
    db: Session,
    payload: InventoryRecordCreate,
) -> InventoryRecord:
    _ensure_batch_number_exists(db, payload.batchNumber)
    inventory_record = InventoryRecord(**payload.model_dump())
    db.add(inventory_record)
    db.commit()
    db.refresh(inventory_record)
    return inventory_record


def update_inventory_record(
    db: Session,
    record_id: int,
    payload: InventoryRecordUpdate,
) -> InventoryRecord:
    inventory_record = get_inventory_record_by_id(db, record_id)
    data = payload.model_dump(exclude_unset=True)

    if "batchNumber" in data:
        _ensure_batch_number_exists(db, data["batchNumber"])

    for field, value in data.items():
        setattr(inventory_record, field, value)

    db.commit()
    db.refresh(inventory_record)
    return inventory_record


def delete_inventory_record(db: Session, record_id: int) -> None:
    inventory_record = get_inventory_record_by_id(db, record_id)
    db.delete(inventory_record)
    db.commit()
