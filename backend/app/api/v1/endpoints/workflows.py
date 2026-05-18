from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.workflows import (
    OrderToProductionWorkflow,
    OrderToWarehouseWorkflow,
    WorkOrderProductionReportWorkflow,
)
from app.services.workflows import (
    get_order_to_production_workflow,
    get_order_to_warehouse_workflow,
    get_work_order_production_report_workflow,
)


router = APIRouter()


@router.get(
    "/order-to-production/{product_order_no}",
    response_model=OrderToProductionWorkflow,
)
def read_order_to_production_workflow(
    product_order_no: str,
    db: Session = Depends(get_db),
) -> OrderToProductionWorkflow:
    return get_order_to_production_workflow(db, product_order_no)


@router.get(
    "/order-to-warehouse/{product_order_no}",
    response_model=OrderToWarehouseWorkflow,
)
def read_order_to_warehouse_workflow(
    product_order_no: str,
    db: Session = Depends(get_db),
) -> OrderToWarehouseWorkflow:
    return get_order_to_warehouse_workflow(db, product_order_no)


@router.get(
    "/work-order-production-report/{work_order_no}",
    response_model=WorkOrderProductionReportWorkflow,
)
def read_work_order_production_report_workflow(
    work_order_no: str,
    db: Session = Depends(get_db),
) -> WorkOrderProductionReportWorkflow:
    return get_work_order_production_report_workflow(db, work_order_no)
