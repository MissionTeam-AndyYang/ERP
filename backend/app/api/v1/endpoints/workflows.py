from flask import Blueprint

from app.api.v1.utils import get_db, json_response
from app.services.workflows import (
    get_order_to_production_workflow,
    get_order_to_warehouse_workflow,
    get_work_order_production_report_workflow,
)

router = Blueprint("workflows", __name__)


@router.get("/order-to-production/<product_order_no>")
def read_order_to_production_workflow(product_order_no: str):
    return json_response(get_order_to_production_workflow(get_db(), product_order_no))


@router.get("/order-to-warehouse/<product_order_no>")
def read_order_to_warehouse_workflow(product_order_no: str):
    return json_response(get_order_to_warehouse_workflow(get_db(), product_order_no))


@router.get("/work-order-production-report/<work_order_no>")
def read_work_order_production_report_workflow(work_order_no: str):
    return json_response(get_work_order_production_report_workflow(get_db(), work_order_no))
