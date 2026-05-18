from typing import Any

from pydantic import BaseModel, Field


class WorkflowRecord(BaseModel):
    table: str
    exists: bool
    id: int | None = None
    no: str | None = None
    label: str | None = None
    fields: dict[str, Any] = Field(default_factory=dict)


class OrderToProductionWorkflow(BaseModel):
    product_order_no: str
    complete: bool
    missing_steps: list[str]
    quotation: WorkflowRecord
    contract: WorkflowRecord
    product_order: WorkflowRecord
    aps_quantity: WorkflowRecord
    work_order: WorkflowRecord
    process_order: WorkflowRecord
    process_labor: list[WorkflowRecord]


class OrderToWarehouseWorkflow(BaseModel):
    product_order_no: str
    complete: bool
    missing_steps: list[str]
    product_order: WorkflowRecord
    purchase_request: WorkflowRecord
    purchase_request_items: list[WorkflowRecord]
    purchase_order: WorkflowRecord
    goods_receipt_note: WorkflowRecord
    batch_number: WorkflowRecord
    inventory_records: list[WorkflowRecord]


class WorkOrderProductionReportWorkflow(BaseModel):
    work_order_no: str
    complete: bool
    missing_steps: list[str]
    work_order: WorkflowRecord
    production_data: WorkflowRecord
    production_data_inputs: list[WorkflowRecord]
    production_data_outputs: list[WorkflowRecord]
    production_data_reuses: list[WorkflowRecord]
    production_data_machines: list[WorkflowRecord]
    production_data_labors: list[WorkflowRecord]
