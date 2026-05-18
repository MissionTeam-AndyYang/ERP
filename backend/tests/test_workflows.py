from collections.abc import Generator

from sqlalchemy.orm import Session

from app.main import app
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


def seed_order_to_production_workflow(db: Session) -> None:
    db.add_all(
        [
            Quotation(id=1, no="Q-001", item_no="FG-001", item_name="Ã¥â€ Â·Ã¥â€¡ÂÃ¦Â°Â´Ã©Â¤Æ’"),
            Contract(
                id=1,
                no="C-001",
                ref_no="Q-001",
                date=20260517,
                displayName="Ã¥Â®Â¢Ã¦Ë†Â¶Ã¥ÂË†Ã§Â´â€ž",
            ),
            ProductOrder(
                id=1,
                no="SO-001",
                ref_no="C-001",
                item_no="FG-001",
                item_name="Ã¥â€ Â·Ã¥â€¡ÂÃ¦Â°Â´Ã©Â¤Æ’",
                count=1200,
                expectedDate=20260520,
            ),
            ApsQuantity(
                id=1,
                no="APS-001",
                product_order_no="SO-001",
                oneProcess=1,
                secProcess=1,
                item_no="FG-001",
                item_name="Ã¥â€ Â·Ã¥â€¡ÂÃ¦Â°Â´Ã©Â¤Æ’",
                amount=1200,
                minutes=480,
            ),
            WorkOrder(
                id=1,
                no="WO-001",
                product_order_no="SO-001",
                aps_no="APS-001",
                product_no="FG-001",
                product_name="Ã¥â€ Â·Ã¥â€¡ÂÃ¦Â°Â´Ã©Â¤Æ’",
                production_line_no="LINE-001",
            ),
            ProcessOrder(
                id=1,
                no="PROC-001",
                work_order_no="WO-001",
                item_no="FG-001",
                item_name="Ã¥â€ Â·Ã¥â€¡ÂÃ¦Â°Â´Ã©Â¤Æ’",
                expectedCount=1200,
            ),
            ProcessLabor(
                id=1,
                work_order_no="WO-001",
                employee_no="EMP-001",
                production_line_no="LINE-001",
                station_no="ST-001",
            ),
        ]
    )
    db.commit()


def test_order_to_production_workflow_returns_complete_chain(db_session: Session) -> None:
    seed_order_to_production_workflow(db_session)

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.config["TEST_DB_SESSION"] = db_session
    try:
        response = app.test_client().get("/api/v1/workflows/order-to-production/SO-001")
    finally:
        app.config.pop("TEST_DB_SESSION", None)

    assert response.status_code == 200
    payload = response.json
    assert payload["complete"] is True
    assert payload["missing_steps"] == []
    assert payload["quotation"]["no"] == "Q-001"
    assert payload["contract"]["fields"]["ref_no"] == "Q-001"
    assert payload["product_order"]["fields"]["ref_no"] == "C-001"
    assert payload["aps_quantity"]["fields"]["product_order_no"] == "SO-001"
    assert payload["work_order"]["fields"]["aps_no"] == "APS-001"
    assert payload["process_order"]["fields"]["work_order_no"] == "WO-001"
    assert payload["process_labor"][0]["fields"]["employee_no"] == "EMP-001"


def test_order_to_production_workflow_reports_missing_steps(db_session: Session) -> None:
    db_session.add(ProductOrder(id=2, no="SO-002", item_name="Ã¦Å“ÂªÃ¦Å½â€™Ã§Â¨â€¹Ã¨Â¨â€šÃ¥â€“Â®"))
    db_session.commit()

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.config["TEST_DB_SESSION"] = db_session
    try:
        response = app.test_client().get("/api/v1/workflows/order-to-production/SO-002")
    finally:
        app.config.pop("TEST_DB_SESSION", None)

    assert response.status_code == 200
    payload = response.json
    assert payload["complete"] is False
    assert payload["missing_steps"] == [
        "quotation",
        "contract",
        "aps_quantity",
        "work_order",
        "process_order",
        "process_labor",
    ]


def seed_order_to_warehouse_workflow(db: Session) -> None:
    db.add_all(
        [
            ProductOrder(
                id=10,
                no="SO-WH-001",
                item_no="FG-002",
                item_name="Ã¥â€ Â·Ã¥â€¡ÂÃ¥Å’â€¦Ã¥Â­Â",
                count=800,
                expectedDate=20260521,
            ),
            PurchaseRequest(
                id=10,
                no="PR-001",
                product_order_no="SO-WH-001",
                date=20260517,
            ),
            PurchaseRequestItem(
                id=10,
                purchase_request_no="PR-001",
                item_no="MAT-001",
                count=100,
                expectedDate=20260518,
            ),
            PurchaseOrder(
                id=10,
                no="PO-001",
                purchase_request_no="PR-001",
                item_no="MAT-001",
                item_name="Ã©ÂºÂµÃ§Â²â€°",
                count=100,
                amount=25000,
            ),
            GoodsReceiptNote(
                id=10,
                no="GRN-001",
                purchase_order_no="PO-001",
                item_no="MAT-001",
                item_name="Ã©ÂºÂµÃ§Â²â€°",
                expectedCount=100,
                checkedCount=100,
                amount=25000,
            ),
            BatchNumber(
                id=10,
                no="BATCH-001",
                ref_no="GRN-001",
                item_no="MAT-001",
                item_name="Ã©ÂºÂµÃ§Â²â€°",
                expectedCount=100,
                checkedCount=100,
                validDate=20260817,
            ),
            InventoryRecord(
                id=10,
                ref_no="GRN-001",
                warehouse_no="WH-001",
                batchNumber="BATCH-001",
                item_no="MAT-001",
                item_name="Ã©ÂºÂµÃ§Â²â€°",
                count=100,
                amount=25000,
            ),
        ]
    )
    db.commit()


def test_order_to_warehouse_workflow_returns_complete_chain(db_session: Session) -> None:
    seed_order_to_warehouse_workflow(db_session)

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.config["TEST_DB_SESSION"] = db_session
    try:
        response = app.test_client().get("/api/v1/workflows/order-to-warehouse/SO-WH-001")
    finally:
        app.config.pop("TEST_DB_SESSION", None)

    assert response.status_code == 200
    payload = response.json
    assert payload["complete"] is True
    assert payload["missing_steps"] == []
    assert payload["product_order"]["no"] == "SO-WH-001"
    assert payload["purchase_request"]["no"] == "PR-001"
    assert payload["purchase_request_items"][0]["fields"]["item_no"] == "MAT-001"
    assert payload["purchase_order"]["fields"]["purchase_request_no"] == "PR-001"
    assert payload["goods_receipt_note"]["fields"]["purchase_order_no"] == "PO-001"
    assert payload["batch_number"]["fields"]["ref_no"] == "GRN-001"
    assert payload["inventory_records"][0]["fields"]["batchNumber"] == "BATCH-001"


def test_order_to_warehouse_workflow_reports_missing_steps(db_session: Session) -> None:
    db_session.add(
        ProductOrder(id=11, no="SO-WH-002", item_name="Ã¦Å“ÂªÃ¦Å½Â¡Ã¨Â³Â¼Ã¨Â¨â€šÃ¥â€“Â®")
    )
    db_session.commit()

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.config["TEST_DB_SESSION"] = db_session
    try:
        response = app.test_client().get("/api/v1/workflows/order-to-warehouse/SO-WH-002")
    finally:
        app.config.pop("TEST_DB_SESSION", None)

    assert response.status_code == 200
    payload = response.json
    assert payload["complete"] is False
    assert payload["missing_steps"] == [
        "purchase_request",
        "purchase_request_items",
        "purchase_order",
        "goods_receipt_note",
        "batch_number",
        "inventory_records",
    ]


def seed_work_order_production_report_workflow(db: Session) -> None:
    db.add_all(
        [
            WorkOrder(
                id=20,
                no="WO-RPT-001",
                product_order_no="SO-RPT-001",
                product_no="FG-003",
                product_name="Ã¥â€ Â·Ã¥â€¡ÂÃ©Â¥â€¦Ã©Â Â­",
                production_line_no="LINE-002",
                processCount=500,
                processTime=360,
            ),
            ProductionData(
                id=20,
                work_order_no="WO-RPT-001",
                product_order_no="SO-RPT-001",
                product_no="FG-003",
                product_name="Ã¥â€ Â·Ã¥â€¡ÂÃ©Â¥â€¦Ã©Â Â­",
                date=20260517,
                production_line_no="LINE-002",
                materialLoss=3.5,
            ),
            ProductionDataInput(
                id=20,
                work_order_no="WO-RPT-001",
                process_order_no="PROC-RPT-001",
                group="G-RPT-001",
                action=1,
                item_no="MAT-002",
                item_name="Ã©ÂºÂµÃ§Â²â€°",
                batch_number="BATCH-IN-001",
                serial_no="S-IN-001",
                count=260,
            ),
            ProductionDataOutput(
                id=20,
                work_order_no="WO-RPT-001",
                process_order_no="PROC-RPT-001",
                group="G-RPT-001",
                action=1,
                item_no="FG-003",
                item_name="Ã¥â€ Â·Ã¥â€¡ÂÃ©Â¥â€¦Ã©Â Â­",
                batch_number="BATCH-OUT-001",
                serial_no="S-OUT-001",
                valid_date_no="VD-001",
                count=500,
            ),
            ProductionDataReuse(
                id=20,
                work_order_no="WO-RPT-001",
                process_order_no="PROC-RPT-001",
                group="G-RPT-001",
                action=1,
                item_no="INP-001",
                item_name="Ã¥ÂÂ¯Ã¥â€ºÅ¾Ã¦â€Â¶Ã©ÂºÂµÃ¥Å“Ëœ",
                category=1,
                batch_number="BATCH-REUSE-001",
                serial_no="S-REUSE-001",
                count=8,
            ),
            ProductionDataMachine(
                id=20,
                work_order_no="WO-RPT-001",
                equipment_no="EQ-001",
                equipment_name="Ã¦â€ÂªÃ¦â€¹Å’Ã¦Â©Å¸",
                action="RUN",
                speed=120,
                temperature=22.5,
            ),
            ProductionDataLabor(
                id=20,
                work_order_no="WO-RPT-001",
                employee_no="EMP-002",
                employee_name="Ã§Å½â€¹Ã¥Â°ÂÃ¦ËœÅ½",
                station_no="ST-002",
                stationStage=1,
                action=1,
                startTime=202605170800,
                endTime=202605171200,
                hours=4,
            ),
        ]
    )
    db.commit()


def test_work_order_production_report_workflow_returns_complete_chain(
    db_session: Session,
) -> None:
    seed_work_order_production_report_workflow(db_session)

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.config["TEST_DB_SESSION"] = db_session
    try:
        response = app.test_client().get(
            "/api/v1/workflows/work-order-production-report/WO-RPT-001"
        )
    finally:
        app.config.pop("TEST_DB_SESSION", None)

    assert response.status_code == 200
    payload = response.json
    assert payload["complete"] is True
    assert payload["missing_steps"] == []
    assert payload["work_order"]["no"] == "WO-RPT-001"
    assert payload["production_data"]["fields"]["materialLoss"] == 3.5
    assert payload["production_data_inputs"][0]["fields"]["batch_number"] == "BATCH-IN-001"
    assert payload["production_data_outputs"][0]["fields"]["batch_number"] == "BATCH-OUT-001"
    assert payload["production_data_reuses"][0]["fields"]["batch_number"] == "BATCH-REUSE-001"
    assert payload["production_data_machines"][0]["fields"]["equipment_no"] == "EQ-001"
    assert payload["production_data_labors"][0]["fields"]["employee_no"] == "EMP-002"


def test_work_order_production_report_workflow_reports_missing_steps(
    db_session: Session,
) -> None:
    db_session.add(
        WorkOrder(id=21, no="WO-RPT-002", product_name="Ã¦Å“ÂªÃ¥â€ºÅ¾Ã¥Â Â±Ã¥Â·Â¥Ã¥â€“Â®")
    )
    db_session.commit()

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.config["TEST_DB_SESSION"] = db_session
    try:
        response = app.test_client().get(
            "/api/v1/workflows/work-order-production-report/WO-RPT-002"
        )
    finally:
        app.config.pop("TEST_DB_SESSION", None)

    assert response.status_code == 200
    payload = response.json
    assert payload["complete"] is False
    assert payload["missing_steps"] == [
        "production_data",
        "production_data_inputs",
        "production_data_outputs",
        "production_data_machines",
        "production_data_labors",
    ]
