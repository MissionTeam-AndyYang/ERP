from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ewdb import (
    ApsQuantity,
    BatchNumber,
    Contract,
    GoodsReceiptNote,
    InventoryRecord,
    ProcessLabor,
    ProcessOrder,
    ProductionData,
    ProductionDataInput,
    ProductionDataLabor,
    ProductionDataMachine,
    ProductionDataOutput,
    ProductionDataReuse,
    ProductOrder,
    PurchaseOrder,
    PurchaseRequest,
    PurchaseRequestItem,
    Quotation,
    WorkOrder,
)
from app.schemas.workflows import (
    OrderToProductionWorkflow,
    OrderToWarehouseWorkflow,
    WorkflowRecord,
    WorkOrderProductionReportWorkflow,
)


def _record(
    table: str,
    row: Any | None,
    *,
    label_attr: str | None = None,
    fields: tuple[str, ...] = (),
) -> WorkflowRecord:
    if row is None:
        return WorkflowRecord(table=table, exists=False)

    return WorkflowRecord(
        table=table,
        exists=True,
        id=getattr(row, "id", None),
        no=getattr(row, "no", None),
        label=getattr(row, label_attr, None) if label_attr else None,
        fields={field: getattr(row, field, None) for field in fields},
    )


def get_order_to_production_workflow(
    db: Session,
    product_order_no: str,
) -> OrderToProductionWorkflow:
    product_order = db.scalar(select(ProductOrder).where(ProductOrder.no == product_order_no))

    contract = None
    quotation = None
    if product_order and product_order.ref_no:
        contract = db.scalar(select(Contract).where(Contract.no == product_order.ref_no))
        if contract and contract.ref_no:
            quotation = db.scalar(select(Quotation).where(Quotation.no == contract.ref_no))

    aps_quantity = db.scalar(
        select(ApsQuantity).where(ApsQuantity.product_order_no == product_order_no)
    )
    work_order = db.scalar(select(WorkOrder).where(WorkOrder.product_order_no == product_order_no))

    process_order = None
    process_labor_rows: list[ProcessLabor] = []
    if work_order:
        process_order = db.scalar(
            select(ProcessOrder).where(ProcessOrder.work_order_no == work_order.no)
        )
        process_labor_rows = list(
            db.scalars(
                select(ProcessLabor).where(ProcessLabor.work_order_no == work_order.no)
            ).all()
        )

    required_steps = {
        "quotation": quotation,
        "contract": contract,
        "product_order": product_order,
        "aps_quantity": aps_quantity,
        "work_order": work_order,
        "process_order": process_order,
        "process_labor": process_labor_rows,
    }
    missing_steps = [name for name, value in required_steps.items() if not value]

    return OrderToProductionWorkflow(
        product_order_no=product_order_no,
        complete=not missing_steps,
        missing_steps=missing_steps,
        quotation=_record(
            "quotation",
            quotation,
            label_attr="item_name",
            fields=("date", "item_no", "item_ref_no", "item_ref_displayName"),
        ),
        contract=_record(
            "contract",
            contract,
            label_attr="displayName",
            fields=("date", "ref_no", "item_no", "item_name", "item_ref_no"),
        ),
        product_order=_record(
            "product_order",
            product_order,
            label_attr="item_name",
            fields=("date", "ref_no", "count", "expectedDate", "item_ref_displayName"),
        ),
        aps_quantity=_record(
            "aps_quantity",
            aps_quantity,
            label_attr="item_name",
            fields=("product_order_no", "oneProcess", "secProcess", "amount", "minutes"),
        ),
        work_order=_record(
            "work_order",
            work_order,
            label_attr="product_name",
            fields=("product_order_no", "aps_no", "production_line_no", "startTime", "endTime"),
        ),
        process_order=_record(
            "process_order",
            process_order,
            label_attr="item_name",
            fields=("work_order_no", "refProcess", "expectedCount", "count"),
        ),
        process_labor=[
            _record(
                "process_labor",
                row,
                fields=("work_order_no", "employee_no", "production_line_no", "station_no"),
            )
            for row in process_labor_rows
        ],
    )


def get_order_to_warehouse_workflow(
    db: Session,
    product_order_no: str,
) -> OrderToWarehouseWorkflow:
    product_order = db.scalar(select(ProductOrder).where(ProductOrder.no == product_order_no))
    purchase_request = db.scalar(
        select(PurchaseRequest).where(PurchaseRequest.product_order_no == product_order_no)
    )

    purchase_request_items: list[PurchaseRequestItem] = []
    purchase_order = None
    goods_receipt_note = None
    batch_number = None
    inventory_records: list[InventoryRecord] = []

    if purchase_request:
        purchase_request_items = list(
            db.scalars(
                select(PurchaseRequestItem).where(
                    PurchaseRequestItem.purchase_request_no == purchase_request.no
                )
            ).all()
        )
        purchase_order = db.scalar(
            select(PurchaseOrder).where(PurchaseOrder.purchase_request_no == purchase_request.no)
        )

    if purchase_order:
        goods_receipt_note = db.scalar(
            select(GoodsReceiptNote).where(GoodsReceiptNote.purchase_order_no == purchase_order.no)
        )

    if goods_receipt_note:
        batch_number = db.scalar(
            select(BatchNumber).where(BatchNumber.ref_no == goods_receipt_note.no)
        )

    if batch_number:
        inventory_records = list(
            db.scalars(
                select(InventoryRecord).where(InventoryRecord.batchNumber == batch_number.no)
            ).all()
        )

    required_steps = {
        "product_order": product_order,
        "purchase_request": purchase_request,
        "purchase_request_items": purchase_request_items,
        "purchase_order": purchase_order,
        "goods_receipt_note": goods_receipt_note,
        "batch_number": batch_number,
        "inventory_records": inventory_records,
    }
    missing_steps = [name for name, value in required_steps.items() if not value]

    return OrderToWarehouseWorkflow(
        product_order_no=product_order_no,
        complete=not missing_steps,
        missing_steps=missing_steps,
        product_order=_record(
            "product_order",
            product_order,
            label_attr="item_name",
            fields=("date", "ref_no", "count", "expectedDate", "item_ref_displayName"),
        ),
        purchase_request=_record(
            "purchase_request",
            purchase_request,
            fields=("product_order_no", "date", "creator_no"),
        ),
        purchase_request_items=[
            _record(
                "purchase_request_item",
                row,
                label_attr="item_no",
                fields=("purchase_request_no", "item_no", "unit", "count", "expectedDate"),
            )
            for row in purchase_request_items
        ],
        purchase_order=_record(
            "purchase_order",
            purchase_order,
            label_attr="item_name",
            fields=("purchase_request_no", "date", "item_ref_no", "count", "amount"),
        ),
        goods_receipt_note=_record(
            "goods_receipt_note",
            goods_receipt_note,
            label_attr="item_name",
            fields=("purchase_order_no", "date", "expectedCount", "checkedCount", "amount"),
        ),
        batch_number=_record(
            "batch_number",
            batch_number,
            label_attr="item_name",
            fields=("ref_no", "date", "expectedCount", "checkedCount", "validDate"),
        ),
        inventory_records=[
            _record(
                "inventory_record",
                row,
                label_attr="item_name",
                fields=("ref_no", "warehouse_no", "batchNumber", "count", "amount"),
            )
            for row in inventory_records
        ],
    )


def get_work_order_production_report_workflow(
    db: Session,
    work_order_no: str,
) -> WorkOrderProductionReportWorkflow:
    work_order = db.scalar(select(WorkOrder).where(WorkOrder.no == work_order_no))
    production_data = db.scalar(
        select(ProductionData).where(ProductionData.work_order_no == work_order_no)
    )
    production_data_inputs = list(
        db.scalars(
            select(ProductionDataInput).where(ProductionDataInput.work_order_no == work_order_no)
        ).all()
    )
    production_data_outputs = list(
        db.scalars(
            select(ProductionDataOutput).where(ProductionDataOutput.work_order_no == work_order_no)
        ).all()
    )
    production_data_reuses = list(
        db.scalars(
            select(ProductionDataReuse).where(ProductionDataReuse.work_order_no == work_order_no)
        ).all()
    )
    production_data_machines = list(
        db.scalars(
            select(ProductionDataMachine).where(
                ProductionDataMachine.work_order_no == work_order_no
            )
        ).all()
    )
    production_data_labors = list(
        db.scalars(
            select(ProductionDataLabor).where(ProductionDataLabor.work_order_no == work_order_no)
        ).all()
    )

    required_steps = {
        "work_order": work_order,
        "production_data": production_data,
        "production_data_inputs": production_data_inputs,
        "production_data_outputs": production_data_outputs,
        "production_data_machines": production_data_machines,
        "production_data_labors": production_data_labors,
    }
    missing_steps = [name for name, value in required_steps.items() if not value]

    return WorkOrderProductionReportWorkflow(
        work_order_no=work_order_no,
        complete=not missing_steps,
        missing_steps=missing_steps,
        work_order=_record(
            "work_order",
            work_order,
            label_attr="product_name",
            fields=(
                "product_order_no",
                "aps_no",
                "production_line_no",
                "processCount",
                "processTime",
            ),
        ),
        production_data=_record(
            "production_data",
            production_data,
            label_attr="product_name",
            fields=(
                "work_order_no",
                "product_order_no",
                "date",
                "production_line_no",
                "materialLoss",
            ),
        ),
        production_data_inputs=[
            _record(
                "production_data_input",
                row,
                label_attr="item_name",
                fields=("work_order_no", "process_order_no", "batch_number", "count", "action"),
            )
            for row in production_data_inputs
        ],
        production_data_outputs=[
            _record(
                "production_data_output",
                row,
                label_attr="item_name",
                fields=("work_order_no", "process_order_no", "batch_number", "count", "action"),
            )
            for row in production_data_outputs
        ],
        production_data_reuses=[
            _record(
                "production_data_reuse",
                row,
                label_attr="item_name",
                fields=("work_order_no", "process_order_no", "batch_number", "count", "action"),
            )
            for row in production_data_reuses
        ],
        production_data_machines=[
            _record(
                "production_data_machine",
                row,
                label_attr="equipment_name",
                fields=("work_order_no", "equipment_no", "time", "action", "speed", "temperature"),
            )
            for row in production_data_machines
        ],
        production_data_labors=[
            _record(
                "production_data_labor",
                row,
                label_attr="employee_name",
                fields=(
                    "work_order_no",
                    "employee_no",
                    "station_no",
                    "startTime",
                    "endTime",
                    "hours",
                ),
            )
            for row in production_data_labors
        ],
    )
