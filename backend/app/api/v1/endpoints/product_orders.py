from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.product_orders import (
    ProductOrderCreate,
    ProductOrderList,
    ProductOrderRead,
    ProductOrderUpdate,
)
from app.services.product_orders import (
    create_product_order,
    delete_product_order,
    get_product_order_by_no,
    list_product_orders,
    update_product_order,
)


router = APIRouter()


@router.get("", response_model=ProductOrderList)
def read_product_orders(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> ProductOrderList:
    total, items = list_product_orders(db, skip=skip, limit=limit)
    return ProductOrderList(total=total, items=items)


@router.post("", response_model=ProductOrderRead, status_code=status.HTTP_201_CREATED)
def create_product_order_endpoint(
    payload: ProductOrderCreate,
    db: Session = Depends(get_db),
) -> ProductOrderRead:
    return create_product_order(db, payload)


@router.get("/{no}", response_model=ProductOrderRead)
def read_product_order(
    no: str,
    db: Session = Depends(get_db),
) -> ProductOrderRead:
    return get_product_order_by_no(db, no)


@router.patch("/{no}", response_model=ProductOrderRead)
def update_product_order_endpoint(
    no: str,
    payload: ProductOrderUpdate,
    db: Session = Depends(get_db),
) -> ProductOrderRead:
    return update_product_order(db, no, payload)


@router.delete("/{no}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_order_endpoint(
    no: str,
    db: Session = Depends(get_db),
) -> Response:
    delete_product_order(db, no)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
