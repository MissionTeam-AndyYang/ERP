from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.purchase_requests import (
    PurchaseRequestCreate,
    PurchaseRequestItemCreate,
    PurchaseRequestList,
    PurchaseRequestRead,
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


router = APIRouter()


@router.get("", response_model=PurchaseRequestList)
def read_purchase_requests(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> PurchaseRequestList:
    total, items = list_purchase_requests(db, skip=skip, limit=limit)
    return PurchaseRequestList(total=total, items=items)


@router.post("", response_model=PurchaseRequestRead, status_code=status.HTTP_201_CREATED)
def create_purchase_request_endpoint(
    payload: PurchaseRequestCreate,
    db: Session = Depends(get_db),
) -> PurchaseRequestRead:
    return create_purchase_request(db, payload)


@router.get("/{no}", response_model=PurchaseRequestRead)
def read_purchase_request(
    no: str,
    db: Session = Depends(get_db),
) -> PurchaseRequestRead:
    return get_purchase_request_read_by_no(db, no)


@router.patch("/{no}", response_model=PurchaseRequestRead)
def update_purchase_request_endpoint(
    no: str,
    payload: PurchaseRequestUpdate,
    db: Session = Depends(get_db),
) -> PurchaseRequestRead:
    return update_purchase_request(db, no, payload)


@router.delete("/{no}", status_code=status.HTTP_204_NO_CONTENT)
def delete_purchase_request_endpoint(
    no: str,
    db: Session = Depends(get_db),
) -> Response:
    delete_purchase_request(db, no)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{no}/items", response_model=PurchaseRequestRead, status_code=status.HTTP_201_CREATED)
def add_purchase_request_item_endpoint(
    no: str,
    payload: PurchaseRequestItemCreate,
    db: Session = Depends(get_db),
) -> PurchaseRequestRead:
    return add_purchase_request_item(db, no, payload)


@router.delete("/{no}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_purchase_request_item_endpoint(
    no: str,
    item_id: int,
    db: Session = Depends(get_db),
) -> Response:
    delete_purchase_request_item(db, no, item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
