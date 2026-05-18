from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
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


router = APIRouter()


@router.get("", response_model=InventoryRecordList)
def read_inventory_records(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> InventoryRecordList:
    total, items = list_inventory_records(db, skip=skip, limit=limit)
    return InventoryRecordList(total=total, items=items)


@router.post("", response_model=InventoryRecordRead, status_code=status.HTTP_201_CREATED)
def create_inventory_record_endpoint(
    payload: InventoryRecordCreate,
    db: Session = Depends(get_db),
) -> InventoryRecordRead:
    return create_inventory_record(db, payload)


@router.get("/{record_id}", response_model=InventoryRecordRead)
def read_inventory_record(
    record_id: int,
    db: Session = Depends(get_db),
) -> InventoryRecordRead:
    return get_inventory_record_by_id(db, record_id)


@router.patch("/{record_id}", response_model=InventoryRecordRead)
def update_inventory_record_endpoint(
    record_id: int,
    payload: InventoryRecordUpdate,
    db: Session = Depends(get_db),
) -> InventoryRecordRead:
    return update_inventory_record(db, record_id, payload)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory_record_endpoint(
    record_id: int,
    db: Session = Depends(get_db),
) -> Response:
    delete_inventory_record(db, record_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
