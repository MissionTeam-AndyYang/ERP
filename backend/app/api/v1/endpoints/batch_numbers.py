from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
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


router = APIRouter()


@router.get("", response_model=BatchNumberList)
def read_batch_numbers(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> BatchNumberList:
    total, items = list_batch_numbers(db, skip=skip, limit=limit)
    return BatchNumberList(total=total, items=items)


@router.post("", response_model=BatchNumberRead, status_code=status.HTTP_201_CREATED)
def create_batch_number_endpoint(
    payload: BatchNumberCreate,
    db: Session = Depends(get_db),
) -> BatchNumberRead:
    return create_batch_number(db, payload)


@router.get("/{no}", response_model=BatchNumberRead)
def read_batch_number(
    no: str,
    db: Session = Depends(get_db),
) -> BatchNumberRead:
    return get_batch_number_by_no(db, no)


@router.patch("/{no}", response_model=BatchNumberRead)
def update_batch_number_endpoint(
    no: str,
    payload: BatchNumberUpdate,
    db: Session = Depends(get_db),
) -> BatchNumberRead:
    return update_batch_number(db, no, payload)


@router.delete("/{no}", status_code=status.HTTP_204_NO_CONTENT)
def delete_batch_number_endpoint(
    no: str,
    db: Session = Depends(get_db),
) -> Response:
    delete_batch_number(db, no)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
