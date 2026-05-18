from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.ewdb import ProductOrder, PurchaseRequest, PurchaseRequestItem
from app.schemas.purchase_requests import (
    PurchaseRequestCreate,
    PurchaseRequestItemCreate,
    PurchaseRequestRead,
    PurchaseRequestUpdate,
)


def _read_model(db: Session, purchase_request: PurchaseRequest) -> PurchaseRequestRead:
    items = list(
        db.scalars(
            select(PurchaseRequestItem)
            .where(PurchaseRequestItem.purchase_request_no == purchase_request.no)
            .order_by(PurchaseRequestItem.id.asc())
        ).all()
    )
    return PurchaseRequestRead.model_validate(
        {
            **purchase_request.__dict__,
            "items": items,
        }
    )


def list_purchase_requests(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 50,
) -> tuple[int, list[PurchaseRequestRead]]:
    total = db.scalar(select(func.count()).select_from(PurchaseRequest)) or 0
    rows = list(
        db.scalars(
            select(PurchaseRequest).order_by(PurchaseRequest.id.desc()).offset(skip).limit(limit)
        ).all()
    )
    return total, [_read_model(db, row) for row in rows]


def get_purchase_request_by_no(db: Session, no: str) -> PurchaseRequest:
    purchase_request = db.scalar(select(PurchaseRequest).where(PurchaseRequest.no == no))
    if purchase_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Purchase request '{no}' was not found.",
        )
    return purchase_request


def get_purchase_request_read_by_no(db: Session, no: str) -> PurchaseRequestRead:
    return _read_model(db, get_purchase_request_by_no(db, no))


def create_purchase_request(
    db: Session,
    payload: PurchaseRequestCreate,
) -> PurchaseRequestRead:
    existing = db.scalar(select(PurchaseRequest).where(PurchaseRequest.no == payload.no))
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Purchase request '{payload.no}' already exists.",
        )

    if payload.product_order_no:
        product_order = db.scalar(
            select(ProductOrder).where(ProductOrder.no == payload.product_order_no)
        )
        if product_order is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product order '{payload.product_order_no}' was not found.",
            )

    data = payload.model_dump(exclude={"items"})
    purchase_request = PurchaseRequest(**data)
    db.add(purchase_request)

    for item in payload.items:
        db.add(
            PurchaseRequestItem(
                purchase_request_no=payload.no,
                **item.model_dump(),
            )
        )

    db.commit()
    db.refresh(purchase_request)
    return _read_model(db, purchase_request)


def update_purchase_request(
    db: Session,
    no: str,
    payload: PurchaseRequestUpdate,
) -> PurchaseRequestRead:
    purchase_request = get_purchase_request_by_no(db, no)
    data = payload.model_dump(exclude_unset=True)

    next_no = data.get("no")
    if next_no and next_no != no:
        existing = db.scalar(select(PurchaseRequest).where(PurchaseRequest.no == next_no))
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Purchase request '{next_no}' already exists.",
            )
        items = list(
            db.scalars(
                select(PurchaseRequestItem).where(PurchaseRequestItem.purchase_request_no == no)
            ).all()
        )
        for item in items:
            item.purchase_request_no = next_no

    product_order_no = data.get("product_order_no")
    if product_order_no:
        product_order = db.scalar(select(ProductOrder).where(ProductOrder.no == product_order_no))
        if product_order is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product order '{product_order_no}' was not found.",
            )

    for field, value in data.items():
        setattr(purchase_request, field, value)

    db.commit()
    db.refresh(purchase_request)
    return _read_model(db, purchase_request)


def add_purchase_request_item(
    db: Session,
    no: str,
    payload: PurchaseRequestItemCreate,
) -> PurchaseRequestRead:
    purchase_request = get_purchase_request_by_no(db, no)
    db.add(PurchaseRequestItem(purchase_request_no=purchase_request.no, **payload.model_dump()))
    db.commit()
    db.refresh(purchase_request)
    return _read_model(db, purchase_request)


def delete_purchase_request_item(db: Session, no: str, item_id: int) -> None:
    get_purchase_request_by_no(db, no)
    item = db.scalar(
        select(PurchaseRequestItem).where(
            PurchaseRequestItem.id == item_id,
            PurchaseRequestItem.purchase_request_no == no,
        )
    )
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Purchase request item '{item_id}' was not found.",
        )
    db.delete(item)
    db.commit()


def delete_purchase_request(db: Session, no: str) -> None:
    purchase_request = get_purchase_request_by_no(db, no)
    items = list(
        db.scalars(
            select(PurchaseRequestItem).where(PurchaseRequestItem.purchase_request_no == no)
        ).all()
    )
    for item in items:
        db.delete(item)
    db.delete(purchase_request)
    db.commit()
