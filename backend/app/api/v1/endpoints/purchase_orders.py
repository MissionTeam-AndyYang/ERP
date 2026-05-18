from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.purchase_orders import (
    PurchaseOrderCreate,
    PurchaseOrderList,
    PurchaseOrderRead,
    PurchaseOrderUpdate,
)
from app.services.purchase_orders import (
    create_purchase_order,
    delete_purchase_order,
    get_purchase_order_by_no,
    list_purchase_orders,
    update_purchase_order,
)


router = APIRouter()


@router.get("", response_model=PurchaseOrderList)
def read_purchase_orders(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> PurchaseOrderList:
    total, items = list_purchase_orders(db, skip=skip, limit=limit)
    return PurchaseOrderList(total=total, items=items)


@router.post("", response_model=PurchaseOrderRead, status_code=status.HTTP_201_CREATED)
def create_purchase_order_endpoint(
    payload: PurchaseOrderCreate,
    db: Session = Depends(get_db),
) -> PurchaseOrderRead:
    return create_purchase_order(db, payload)


@router.get("/{no}", response_model=PurchaseOrderRead)
def read_purchase_order(
    no: str,
    db: Session = Depends(get_db),
) -> PurchaseOrderRead:
    return get_purchase_order_by_no(db, no)


@router.patch("/{no}", response_model=PurchaseOrderRead)
def update_purchase_order_endpoint(
    no: str,
    payload: PurchaseOrderUpdate,
    db: Session = Depends(get_db),
) -> PurchaseOrderRead:
    return update_purchase_order(db, no, payload)


@router.delete("/{no}", status_code=status.HTTP_204_NO_CONTENT)
def delete_purchase_order_endpoint(
    no: str,
    db: Session = Depends(get_db),
) -> Response:
    delete_purchase_order(db, no)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
