from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import ApiError
from app.models.ewdb import PurchaseOrder, PurchaseRequest
from app.schemas.purchase_orders import PurchaseOrderCreate, PurchaseOrderUpdate


def list_purchase_orders(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 50,
) -> tuple[int, list[PurchaseOrder]]:
    total = db.scalar(select(func.count()).select_from(PurchaseOrder)) or 0
    items = list(
        db.scalars(
            select(PurchaseOrder).order_by(PurchaseOrder.id.desc()).offset(skip).limit(limit)
        ).all()
    )
    return total, items


def get_purchase_order_by_no(db: Session, no: str) -> PurchaseOrder:
    purchase_order = db.scalar(select(PurchaseOrder).where(PurchaseOrder.no == no))
    if purchase_order is None:
        raise ApiError(404, f"Purchase order '{no}' was not found.")
    return purchase_order


def _ensure_purchase_request_exists(db: Session, purchase_request_no: str | None) -> None:
    if not purchase_request_no:
        return
    purchase_request = db.scalar(
        select(PurchaseRequest).where(PurchaseRequest.no == purchase_request_no)
    )
    if purchase_request is None:
        raise ApiError(400, f"Purchase request '{purchase_request_no}' was not found.")


def create_purchase_order(db: Session, payload: PurchaseOrderCreate) -> PurchaseOrder:
    existing = db.scalar(select(PurchaseOrder).where(PurchaseOrder.no == payload.no))
    if existing is not None:
        raise ApiError(409, f"Purchase order '{payload.no}' already exists.")

    _ensure_purchase_request_exists(db, payload.purchase_request_no)
    purchase_order = PurchaseOrder(**payload.model_dump())
    db.add(purchase_order)
    db.commit()
    db.refresh(purchase_order)
    return purchase_order


def update_purchase_order(
    db: Session,
    no: str,
    payload: PurchaseOrderUpdate,
) -> PurchaseOrder:
    purchase_order = get_purchase_order_by_no(db, no)
    data = payload.model_dump(exclude_unset=True)

    next_no = data.get("no")
    if next_no and next_no != no:
        existing = db.scalar(select(PurchaseOrder).where(PurchaseOrder.no == next_no))
        if existing is not None:
            raise ApiError(409, f"Purchase order '{next_no}' already exists.")

    if "purchase_request_no" in data:
        _ensure_purchase_request_exists(db, data["purchase_request_no"])

    for field, value in data.items():
        setattr(purchase_order, field, value)

    db.commit()
    db.refresh(purchase_order)
    return purchase_order


def delete_purchase_order(db: Session, no: str) -> None:
    purchase_order = get_purchase_order_by_no(db, no)
    db.delete(purchase_order)
    db.commit()
