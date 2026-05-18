from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import ApiError
from app.models.ewdb import ProductOrder
from app.schemas.product_orders import ProductOrderCreate, ProductOrderUpdate


def list_product_orders(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 50,
) -> tuple[int, list[ProductOrder]]:
    total = db.scalar(select(func.count()).select_from(ProductOrder)) or 0
    items = list(
        db.scalars(
            select(ProductOrder).order_by(ProductOrder.id.desc()).offset(skip).limit(limit)
        ).all()
    )
    return total, items


def get_product_order_by_no(db: Session, no: str) -> ProductOrder:
    product_order = db.scalar(select(ProductOrder).where(ProductOrder.no == no))
    if product_order is None:
        raise ApiError(404, f"Product order '{no}' was not found.")
    return product_order


def create_product_order(db: Session, payload: ProductOrderCreate) -> ProductOrder:
    existing = db.scalar(select(ProductOrder).where(ProductOrder.no == payload.no))
    if existing is not None:
        raise ApiError(409, f"Product order '{payload.no}' already exists.")

    product_order = ProductOrder(**payload.model_dump())
    db.add(product_order)
    db.commit()
    db.refresh(product_order)
    return product_order


def update_product_order(
    db: Session,
    no: str,
    payload: ProductOrderUpdate,
) -> ProductOrder:
    product_order = get_product_order_by_no(db, no)
    data = payload.model_dump(exclude_unset=True)

    next_no = data.get("no")
    if next_no and next_no != no:
        existing = db.scalar(select(ProductOrder).where(ProductOrder.no == next_no))
        if existing is not None:
            raise ApiError(409, f"Product order '{next_no}' already exists.")

    for field, value in data.items():
        setattr(product_order, field, value)

    db.commit()
    db.refresh(product_order)
    return product_order


def delete_product_order(db: Session, no: str) -> None:
    product_order = get_product_order_by_no(db, no)
    db.delete(product_order)
    db.commit()
