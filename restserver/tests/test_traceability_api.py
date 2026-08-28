# coding=utf8
import sys
import time
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.common.common import (
    EInventoryCategory,
    EItemCategory,
    EOutputCategory,
    ETraceRiskCode,
    ETraceRiskLevelCode,
    ETraceStepTypeCode,
    ETraceStatusCode,
    EWorkflowTaskStatus,
    EWorkflowTaskType,
)
from package.dbwrapper.table import (
    CTableBatchNumber,
    CTableGoodsReceiptNote,
    CTableInventoryDelta,
    CTableInventoryItemMonthStatistic,
    CTableInventoryMonthStatistic,
    CTableInventoryRec,
    CTableItemSafetyStock,
    CTableMaterial,
    CTableProductionData,
    CTableProductionDataInput,
    CTableProductionDataOutput,
    CTableShipWarehouse,
    CTableShipWarehouseAlias,
    CTableShipWarehouseContract,
    CTableWarehouseInventoryReservation,
    CTableWarehousePalletMovement,
    CTableWarehouseQualityHold,
    CTableWarehouseRiskRule,
    CTableWorkflowTaskEvent,
    CTableWorkflowTaskState,
)
from package.restserver.api.v2.trace import CTraceabilityService


def build_session():
    obj_engine = create_engine("sqlite:///:memory:")
    for obj_table in [
        CTableInventoryRec.__table__,
        CTableInventoryDelta.__table__,
        CTableInventoryItemMonthStatistic.__table__,
        CTableInventoryMonthStatistic.__table__,
        CTableBatchNumber.__table__,
        CTableGoodsReceiptNote.__table__,
        CTableMaterial.__table__,
        CTableItemSafetyStock.__table__,
        CTableShipWarehouseAlias.__table__,
        CTableShipWarehouse.__table__,
        CTableShipWarehouseContract.__table__,
        CTableWarehouseInventoryReservation.__table__,
        CTableWarehouseQualityHold.__table__,
        CTableWarehousePalletMovement.__table__,
        CTableWarehouseRiskRule.__table__,
        CTableWorkflowTaskState.__table__,
        CTableWorkflowTaskEvent.__table__,
        CTableProductionData.__table__,
        CTableProductionDataInput.__table__,
        CTableProductionDataOutput.__table__,
    ]:
        obj_table.create(bind=obj_engine)
    return sessionmaker(bind=obj_engine)()


def seed_traceability(obj_session):
    n_now = int(time.time())
    obj_session.add_all([
        CTableShipWarehouseAlias(no="WH-A", name="倉A", category=2),
        CTableMaterial(no="RM-001", category=EItemCategory.PM, subCategory=11, name="原料A", unitWarehouse=1),
        CTableBatchNumber(
            date=n_now - 20 * 86400,
            no="B-RM-001",
            ref_no="GRN-001",
            refCategory=1,
            item_no="RM-001",
            item_name="原料A",
            itemCategory=EItemCategory.PM,
            itemSubCategory=11,
            itemType=1,
            unit=1,
            expectedCount=100,
            checkedCount=100,
            validDays=90,
            validDate=n_now + 70 * 86400,
            creationTime=n_now - 20 * 86400,
        ),
        CTableGoodsReceiptNote(
            no="GRN-001",
            purchase_order_no="PO-001",
            date=n_now - 20 * 86400,
            category=1,
            item_no="RM-001",
            item_name="原料A",
            itemCategory=EItemCategory.PM,
            itemSubCategory=11,
            unit=1,
            expectedCount=100,
            checkedCount=100,
            amount=1000,
            creationTime=n_now - 20 * 86400,
        ),
        CTableGoodsReceiptNote(
            no="GRN-002",
            purchase_order_no="PO-002",
            date=n_now - 30 * 86400,
            category=1,
            item_no="RM-002",
            item_name="過期原料",
            itemCategory=EItemCategory.PM,
            itemSubCategory=11,
            unit=1,
            expectedCount=10,
            checkedCount=10,
            amount=100,
            creationTime=n_now - 30 * 86400,
        ),
        CTableBatchNumber(
            date=n_now - 10 * 86400,
            no="B-WIP-001",
            ref_no="WO-001",
            refCategory=2,
            item_no="WIP-001",
            item_name="半成品A",
            itemCategory=EItemCategory.INPRODUCT,
            itemSubCategory=41,
            itemType=1,
            unit=1,
            expectedCount=45,
            checkedCount=45,
            validDays=30,
            validDate=n_now + 20 * 86400,
            creationTime=n_now - 10 * 86400,
        ),
        CTableBatchNumber(
            date=n_now - 5 * 86400,
            no="B-FG-001",
            ref_no="WO-002",
            refCategory=2,
            item_no="FG-001",
            item_name="製成品A",
            itemCategory=EItemCategory.PRODUCT,
            itemSubCategory=51,
            itemType=1,
            unit=1,
            expectedCount=40,
            checkedCount=40,
            validDays=180,
            validDate=n_now + 175 * 86400,
            creationTime=n_now - 5 * 86400,
        ),
        CTableBatchNumber(
            date=n_now - 30 * 86400,
            no="B-EXPIRED-001",
            ref_no="GRN-002",
            refCategory=1,
            item_no="RM-002",
            item_name="過期原料",
            itemCategory=EItemCategory.PM,
            itemSubCategory=11,
            itemType=1,
            unit=1,
            expectedCount=10,
            checkedCount=10,
            validDays=5,
            validDate=n_now - 25 * 86400,
            creationTime=n_now - 30 * 86400,
        ),
        CTableInventoryRec(
            warehouse_no="WH-A",
            warehouse_displayName="倉A",
            ref_no="GRN-001",
            refCategory=1,
            date=n_now - 20 * 86400,
            category=EInventoryCategory.IN,
            batchNumber="B-RM-001",
            item_no="RM-001",
            item_name="原料A",
            itemCategory=EItemCategory.PM,
            itemType=1,
            unit=1,
            count=90,
            amount=900,
        ),
        CTableInventoryRec(
            warehouse_no="WH-A",
            warehouse_displayName="倉A",
            ref_no="GRN-002",
            refCategory=1,
            date=n_now - 30 * 86400,
            category=EInventoryCategory.IN,
            batchNumber="B-EXPIRED-001",
            item_no="RM-002",
            item_name="過期原料",
            itemCategory=EItemCategory.PM,
            itemType=1,
            unit=1,
            count=10,
            amount=100,
        ),
        CTableWarehouseQualityHold(
            no="QH-001",
            date=n_now - 1 * 86400,
            refCategory=8,
            ref_no="QC-001",
            warehouse_no="WH-A",
            itemCategory=EItemCategory.PM,
            item_no="RM-001",
            item_name="原料A",
            batchNumber="B-RM-001",
            unit=1,
            holdQuantity=5,
            holdValue=50,
            status=1,
            creationTime=n_now - 1 * 86400,
        ),
        CTableWorkflowTaskState(
            taskId="TASK-QA-001",
            module=5,
            taskType=EWorkflowTaskType.QUALITY,
            refCategory=8,
            ref_no="QC-001",
            itemCategory=EItemCategory.PM,
            item_no="RM-001",
            item_name="原料A",
            batchNumber="B-RM-001",
            warehouse_no="WH-A",
            expectedQuantity=5,
            unit=1,
            dueTimestamp=n_now,
            taskStatus=EWorkflowTaskStatus.PENDING,
            ownerDepartment=5,
            creationTime=n_now - 1 * 86400,
        ),
        CTableProductionData(work_order_no="WO-001", date=n_now - 10 * 86400, product_no="WIP-001", product_name="半成品A"),
        CTableProductionDataInput(
            work_order_no="WO-001",
            process_order_no="PROC-001",
            group="G-001",
            time=n_now - 10 * 86400,
            action=1,
            item_no="RM-001",
            item_name="原料A",
            category=EItemCategory.PM,
            itemSubCategory=11,
            batch_number="B-RM-001",
            serial_no="S-IN-001",
            unit=1,
            count=55,
        ),
        CTableProductionDataInput(
            work_order_no="WO-001",
            process_order_no="PROC-001",
            group="G-001",
            time=n_now - 10 * 86400,
            action=1,
            item_no="RM-001",
            item_name="原料A",
            category=EItemCategory.PM,
            itemSubCategory=11,
            batch_number="B-RM-001",
            serial_no="S-IN-001-B",
            unit=1,
            count=5,
        ),
        CTableProductionDataInput(
            work_order_no="WO-001",
            process_order_no="PROC-001",
            group="G-001",
            time=n_now - 10 * 86400,
            action=1,
            item_no="PK-001",
            item_name="物料A",
            category=EItemCategory.MA,
            itemSubCategory=21,
            batch_number="B-PK-001",
            serial_no="S-IN-001-PK",
            unit=1,
            count=7,
        ),
        CTableProductionDataOutput(
            work_order_no="WO-001",
            process_order_no="PROC-001",
            group="G-001",
            time=n_now - 10 * 86400,
            action=1,
            item_no="WIP-001",
            item_name="半成品A",
            category=EOutputCategory.INPRODUCT,
            itemSubCategory=41,
            batch_number="B-WIP-001",
            serial_no="S-OUT-001",
            unit=1,
            count=45,
        ),
        CTableProductionDataOutput(
            work_order_no="WO-001",
            process_order_no="PROC-001",
            group="G-001",
            time=n_now - 10 * 86400,
            action=1,
            item_no="WIP-001",
            item_name="半成品A",
            category=EOutputCategory.INPRODUCT,
            itemSubCategory=41,
            batch_number="B-WIP-001",
            serial_no="S-OUT-001-B",
            unit=1,
            count=5,
        ),
        CTableProductionData(work_order_no="WO-002", date=n_now - 5 * 86400, product_no="FG-001", product_name="製成品A"),
        CTableProductionDataInput(
            work_order_no="WO-002",
            process_order_no="PROC-002",
            group="G-001",
            time=n_now - 5 * 86400,
            action=1,
            item_no="WIP-001",
            item_name="半成品A",
            category=EItemCategory.INPRODUCT,
            itemSubCategory=41,
            batch_number="B-WIP-001",
            serial_no="S-IN-002",
            unit=1,
            count=40,
        ),
        CTableProductionDataOutput(
            work_order_no="WO-002",
            process_order_no="PROC-002",
            group="G-001",
            time=n_now - 5 * 86400,
            action=1,
            item_no="FG-001",
            item_name="製成品A",
            category=EOutputCategory.PRODUCT,
            itemSubCategory=51,
            batch_number="B-FG-001",
            serial_no="S-OUT-002",
            unit=1,
            count=40,
        ),
    ])
    obj_session.commit()
    return n_now


def test_trace_dashboard_returns_confirmed_fields():
    obj_session = build_session()
    seed_traceability(obj_session)
    dict_payload = CTraceabilityService()._CTraceabilityService__get_dashboard_with_session(
        obj_session, "Asia/Taipei", "", 0, "", "", "", "", 0, 50,
    )

    assert dict_payload["summary"]["traceableBatchCount"] >= 3
    assert dict_payload["summary"]["highRiskTraceCount"] >= 1
    assert dict_payload["total"] == 4
    dict_records = {dict_row["batchNo"]: dict_row for dict_row in dict_payload["records"]}
    assert dict_records["B-RM-001"]["traceStatusCode"] == ETraceStatusCode.COMPLETE
    assert dict_records["B-RM-001"]["riskCode"] == ETraceRiskCode.QUALITY_HOLD
    assert dict_records["B-EXPIRED-001"]["riskLevelCode"] == ETraceRiskLevelCode.HIGH_RISK
    assert dict_records["B-EXPIRED-001"]["riskCode"] == ETraceRiskCode.EXPIRED


def test_trace_batch_overview_builds_multilevel_steps():
    obj_session = build_session()
    seed_traceability(obj_session)
    dict_payload = CTraceabilityService()._CTraceabilityService__get_batch_overview_with_session(
        obj_session, "B-RM-001", "Asia/Taipei",
    )

    assert dict_payload["batch"]["batchNo"] == "B-RM-001"
    assert dict_payload["batch"]["traceStatusCode"] == ETraceStatusCode.COMPLETE
    assert "nodes" not in dict_payload
    assert "edges" not in dict_payload
    assert "timeline" not in dict_payload
    lst_steps = dict_payload["traceSteps"]
    assert any(dict_step["stepTypeCode"] == ETraceStepTypeCode.RECEIPT and dict_step["refNo"] == "GRN-001" for dict_step in lst_steps)
    dict_production_steps = {dict_step["refNo"]: dict_step for dict_step in lst_steps if dict_step["stepTypeCode"] == ETraceStepTypeCode.PRODUCTION}
    assert "WO-001" in dict_production_steps
    assert "WO-002" in dict_production_steps
    assert any(dict_item["batchNo"] == "B-RM-001" for dict_item in dict_production_steps["WO-001"]["inputItems"])
    assert any(dict_item["batchNo"] == "B-WIP-001" for dict_item in dict_production_steps["WO-001"]["outputItems"])
    assert len([dict_item for dict_item in dict_production_steps["WO-001"]["inputItems"] if dict_item["batchNo"] == "B-RM-001"]) == 1
    assert len([dict_item for dict_item in dict_production_steps["WO-001"]["outputItems"] if dict_item["batchNo"] == "B-WIP-001"]) == 1
    assert next(dict_item for dict_item in dict_production_steps["WO-001"]["inputItems"] if dict_item["batchNo"] == "B-RM-001")["quantity"] == 60.0
    assert next(dict_item for dict_item in dict_production_steps["WO-001"]["outputItems"] if dict_item["batchNo"] == "B-WIP-001")["quantity"] == 50.0
    assert all(dict_item["itemCategory"] != EItemCategory.MA for dict_item in dict_production_steps["WO-001"]["inputItems"])
    assert any(dict_item["batchNo"] == "B-WIP-001" for dict_item in dict_production_steps["WO-002"]["inputItems"])
    assert any(dict_item["batchNo"] == "B-FG-001" for dict_item in dict_production_steps["WO-002"]["outputItems"])


def test_trace_batch_overview_finished_goods_traces_upstream_to_material_receipt():
    obj_session = build_session()
    seed_traceability(obj_session)
    dict_payload = CTraceabilityService()._CTraceabilityService__get_batch_overview_with_session(
        obj_session, "B-FG-001", "Asia/Taipei",
    )

    assert dict_payload["batch"]["batchNo"] == "B-FG-001"
    lst_steps = dict_payload["traceSteps"]
    assert any(dict_step["stepTypeCode"] == ETraceStepTypeCode.RECEIPT and dict_step["refNo"] == "GRN-001" for dict_step in lst_steps)
    dict_production_steps = {dict_step["refNo"]: dict_step for dict_step in lst_steps if dict_step["stepTypeCode"] == ETraceStepTypeCode.PRODUCTION}
    assert "WO-001" in dict_production_steps
    assert "WO-002" in dict_production_steps
    set_input_batches = {
        dict_item["batchNo"]
        for dict_step in dict_production_steps.values()
        for dict_item in dict_step["inputItems"]
    }
    set_output_batches = {
        dict_item["batchNo"]
        for dict_step in dict_production_steps.values()
        for dict_item in dict_step["outputItems"]
    }
    assert {"B-RM-001", "B-WIP-001"}.issubset(set_input_batches)
    assert {"B-WIP-001", "B-FG-001"}.issubset(set_output_batches)


def test_trace_batch_overview_keeps_focus_output_when_work_order_has_sibling_outputs():
    obj_session = build_session()
    n_now = seed_traceability(obj_session)
    obj_session.add_all([
        CTableBatchNumber(
            date=n_now - 5 * 86400,
            no="B-FG-OTHER",
            ref_no="WO-002",
            refCategory=2,
            item_no="FG-OTHER",
            item_name="製成品B",
            itemCategory=EItemCategory.PRODUCT,
            itemSubCategory=51,
            itemType=1,
            unit=1,
            expectedCount=12,
            checkedCount=12,
            validDays=180,
            validDate=n_now + 175 * 86400,
            creationTime=n_now - 5 * 86400,
        ),
        CTableProductionDataInput(
            work_order_no="WO-002",
            process_order_no="PROC-OTHER",
            group="G-OTHER",
            time=n_now - 5 * 86400,
            action=1,
            item_no="RM-OTHER",
            item_name="不相關原料",
            category=EItemCategory.PM,
            itemSubCategory=11,
            batch_number="B-RM-OTHER",
            serial_no="S-IN-OTHER",
            unit=1,
            count=12,
        ),
        CTableProductionDataOutput(
            work_order_no="WO-002",
            process_order_no="PROC-OTHER",
            group="G-OTHER",
            time=n_now - 5 * 86400,
            action=1,
            item_no="FG-OTHER",
            item_name="製成品B",
            category=EItemCategory.PRODUCT,
            itemSubCategory=51,
            batch_number="B-FG-OTHER",
            serial_no="S-OUT-OTHER",
            unit=1,
            count=12,
        ),
    ])
    obj_session.commit()

    dict_payload = CTraceabilityService()._CTraceabilityService__get_batch_overview_with_session(
        obj_session, "B-FG-001", "Asia/Taipei",
    )

    lst_steps = dict_payload["traceSteps"]
    set_output_batches = {
        dict_item["batchNo"]
        for dict_step in lst_steps
        for dict_item in dict_step["outputItems"]
    }
    assert "B-FG-001" in set_output_batches
    assert "B-FG-OTHER" not in set_output_batches


def test_trace_batch_overview_finished_goods_filters_same_scope_sibling_output():
    obj_session = build_session()
    n_now = seed_traceability(obj_session)
    obj_session.add_all([
        CTableBatchNumber(
            date=n_now - 5 * 86400,
            no="B-FG-SIBLING",
            ref_no="WO-002",
            refCategory=2,
            item_no="FG-SIBLING",
            item_name="同製程旁支製成品",
            itemCategory=EItemCategory.PRODUCT,
            itemSubCategory=51,
            itemType=1,
            unit=1,
            expectedCount=8,
            checkedCount=8,
            validDays=180,
            validDate=n_now + 175 * 86400,
            creationTime=n_now - 5 * 86400,
        ),
        CTableProductionDataOutput(
            work_order_no="WO-002",
            process_order_no="PROC-002",
            group="G-001",
            time=n_now - 5 * 86400,
            action=1,
            item_no="FG-SIBLING",
            item_name="同製程旁支製成品",
            category=EOutputCategory.PRODUCT,
            itemSubCategory=51,
            batch_number="B-FG-SIBLING",
            serial_no="S-OUT-SIBLING",
            unit=1,
            count=8,
        ),
    ])
    obj_session.commit()

    dict_payload = CTraceabilityService()._CTraceabilityService__get_batch_overview_with_session(
        obj_session, "B-FG-001", "Asia/Taipei",
    )

    set_output_batches = {
        dict_item["batchNo"]
        for dict_step in dict_payload["traceSteps"]
        for dict_item in dict_step["outputItems"]
    }
    assert "B-FG-001" in set_output_batches
    assert "B-FG-SIBLING" not in set_output_batches


def test_trace_batch_overview_keeps_output_when_process_order_is_missing_on_output():
    obj_session = build_session()
    n_now = seed_traceability(obj_session)
    obj_session.add_all([
        CTableBatchNumber(
            date=n_now - 2 * 86400,
            no="B-FG-NO-PROC",
            ref_no="WO-NO-PROC",
            refCategory=2,
            item_no="FG-NO-PROC",
            item_name="缺製程單製成品",
            itemCategory=EItemCategory.PRODUCT,
            itemSubCategory=51,
            itemType=1,
            unit=1,
            expectedCount=18,
            checkedCount=18,
            validDays=180,
            validDate=n_now + 178 * 86400,
            creationTime=n_now - 2 * 86400,
        ),
        CTableProductionData(work_order_no="WO-NO-PROC", date=n_now - 2 * 86400, product_no="FG-NO-PROC", product_name="缺製程單製成品"),
        CTableProductionDataInput(
            work_order_no="WO-NO-PROC",
            process_order_no="PROC-NO-PROC",
            group="group_1",
            time=n_now - 2 * 86400,
            action=1,
            item_no="WIP-001",
            item_name="半成品A",
            category=EItemCategory.INPRODUCT,
            itemSubCategory=41,
            batch_number="B-WIP-001",
            serial_no="S-IN-NO-PROC",
            unit=1,
            count=20,
        ),
        CTableProductionDataOutput(
            work_order_no="WO-NO-PROC",
            process_order_no="",
            group="group_1",
            time=n_now - 2 * 86400,
            action=1,
            item_no="FG-NO-PROC",
            item_name="缺製程單製成品",
            category=EOutputCategory.PRODUCT,
            itemSubCategory=51,
            batch_number="B-FG-NO-PROC",
            serial_no="S-OUT-NO-PROC",
            unit=1,
            count=18,
        ),
    ])
    obj_session.commit()

    dict_payload = CTraceabilityService()._CTraceabilityService__get_batch_overview_with_session(
        obj_session, "B-FG-NO-PROC", "Asia/Taipei",
    )

    dict_step = next(
        dict_step for dict_step in dict_payload["traceSteps"]
        if dict_step["refNo"] == "WO-NO-PROC"
    )
    assert any(dict_item["batchNo"] == "B-WIP-001" for dict_item in dict_step["inputItems"])
    assert any(dict_item["batchNo"] == "B-FG-NO-PROC" for dict_item in dict_step["outputItems"])


def test_trace_batch_overview_raw_material_keeps_output_when_counterpart_process_order_is_missing():
    obj_session = build_session()
    n_now = seed_traceability(obj_session)
    obj_session.add_all([
        CTableBatchNumber(
            date=n_now - 3 * 86400,
            no="B-RM-PROC-MISMATCH",
            ref_no="GRN-PROC-MISMATCH",
            refCategory=1,
            item_no="RM-PROC-MISMATCH",
            item_name="製程單不一致原料",
            itemCategory=EItemCategory.PM,
            itemSubCategory=11,
            itemType=1,
            unit=1,
            expectedCount=30,
            checkedCount=30,
            validDays=90,
            validDate=n_now + 87 * 86400,
            creationTime=n_now - 3 * 86400,
        ),
        CTableGoodsReceiptNote(
            no="GRN-PROC-MISMATCH",
            purchase_order_no="PO-PROC-MISMATCH",
            date=n_now - 3 * 86400,
            category=1,
            item_no="RM-PROC-MISMATCH",
            item_name="製程單不一致原料",
            itemCategory=EItemCategory.PM,
            itemSubCategory=11,
            unit=1,
            expectedCount=30,
            checkedCount=30,
            amount=300,
            creationTime=n_now - 3 * 86400,
        ),
        CTableBatchNumber(
            date=n_now - 2 * 86400,
            no="B-FG-PROC-MISMATCH",
            ref_no="WO-PROC-MISMATCH",
            refCategory=2,
            item_no="FG-PROC-MISMATCH",
            item_name="製程單不一致製成品",
            itemCategory=EItemCategory.PRODUCT,
            itemSubCategory=51,
            itemType=1,
            unit=1,
            expectedCount=25,
            checkedCount=25,
            validDays=180,
            validDate=n_now + 178 * 86400,
            creationTime=n_now - 2 * 86400,
        ),
        CTableProductionData(work_order_no="WO-PROC-MISMATCH", date=n_now - 2 * 86400, product_no="FG-PROC-MISMATCH", product_name="製程單不一致製成品"),
        CTableProductionDataInput(
            work_order_no="WO-PROC-MISMATCH",
            process_order_no="PROC-PROC-MISMATCH",
            group="group_2",
            time=n_now - 2 * 86400,
            action=1,
            item_no="RM-PROC-MISMATCH",
            item_name="製程單不一致原料",
            category=EItemCategory.PM,
            itemSubCategory=11,
            batch_number="B-RM-PROC-MISMATCH",
            serial_no="S-IN-PROC-MISMATCH",
            unit=1,
            count=28,
        ),
        CTableProductionDataOutput(
            work_order_no="WO-PROC-MISMATCH",
            process_order_no="",
            group="group_2",
            time=n_now - 2 * 86400,
            action=1,
            item_no="FG-PROC-MISMATCH",
            item_name="製程單不一致製成品",
            category=EOutputCategory.PRODUCT,
            itemSubCategory=51,
            batch_number="B-FG-PROC-MISMATCH",
            serial_no="S-OUT-PROC-MISMATCH",
            unit=1,
            count=25,
        ),
    ])
    obj_session.commit()

    dict_payload = CTraceabilityService()._CTraceabilityService__get_batch_overview_with_session(
        obj_session, "B-RM-PROC-MISMATCH", "Asia/Taipei",
    )

    dict_step = next(
        dict_step for dict_step in dict_payload["traceSteps"]
        if dict_step["refNo"] == "WO-PROC-MISMATCH"
    )
    assert any(dict_item["batchNo"] == "B-RM-PROC-MISMATCH" for dict_item in dict_step["inputItems"])
    assert any(dict_item["batchNo"] == "B-FG-PROC-MISMATCH" for dict_item in dict_step["outputItems"])


def test_trace_batch_overview_raw_material_filters_unrelated_downstream_inputs():
    obj_session = build_session()
    n_now = seed_traceability(obj_session)
    obj_session.add_all([
        CTableBatchNumber(
            date=n_now - 7 * 86400,
            no="B-RM-SIDE",
            ref_no="GRN-SIDE",
            refCategory=1,
            item_no="RM-SIDE",
            item_name="非查詢原料",
            itemCategory=EItemCategory.PM,
            itemSubCategory=11,
            itemType=1,
            unit=1,
            expectedCount=20,
            checkedCount=20,
            validDays=90,
            validDate=n_now + 80 * 86400,
            creationTime=n_now - 7 * 86400,
        ),
        CTableProductionDataInput(
            work_order_no="WO-002",
            process_order_no="PROC-002",
            group="G-001",
            time=n_now - 5 * 86400,
            action=1,
            item_no="RM-SIDE",
            item_name="非查詢原料",
            category=EItemCategory.PM,
            itemSubCategory=11,
            batch_number="B-RM-SIDE",
            serial_no="S-IN-SIDE",
            unit=1,
            count=3,
        ),
    ])
    obj_session.commit()

    dict_payload = CTraceabilityService()._CTraceabilityService__get_batch_overview_with_session(
        obj_session, "B-RM-001", "Asia/Taipei",
    )

    set_input_batches = {
        dict_item["batchNo"]
        for dict_step in dict_payload["traceSteps"]
        for dict_item in dict_step["inputItems"]
    }
    assert "B-RM-001" in set_input_batches
    assert "B-WIP-001" in set_input_batches
    assert "B-RM-SIDE" not in set_input_batches


def test_trace_batch_overview_keeps_output_when_group_has_extra_spaces():
    obj_session = build_session()
    n_now = seed_traceability(obj_session)
    obj_session.add_all([
        CTableBatchNumber(
            date=n_now - 2 * 86400,
            no="B-FG-GROUP-SPACE",
            ref_no="WO-GROUP-SPACE",
            refCategory=2,
            item_no="FG-GROUP-SPACE",
            item_name="群組空白製成品",
            itemCategory=EItemCategory.PRODUCT,
            itemSubCategory=51,
            itemType=1,
            unit=1,
            expectedCount=18,
            checkedCount=18,
            validDays=180,
            validDate=n_now + 178 * 86400,
            creationTime=n_now - 2 * 86400,
        ),
        CTableProductionData(work_order_no="WO-GROUP-SPACE", date=n_now - 2 * 86400, product_no="FG-GROUP-SPACE", product_name="群組空白製成品"),
        CTableProductionDataInput(
            work_order_no="WO-GROUP-SPACE",
            process_order_no="",
            group=" group_1 ",
            time=n_now - 2 * 86400,
            action=1,
            item_no="WIP-GROUP-SPACE",
            item_name="群組空白半成品",
            category=EItemCategory.INPRODUCT,
            itemSubCategory=41,
            batch_number="B-WIP-GROUP-SPACE",
            serial_no="S-IN-GROUP-SPACE",
            unit=1,
            count=20,
        ),
        CTableProductionDataOutput(
            work_order_no="WO-GROUP-SPACE",
            process_order_no="",
            group="group_1",
            time=n_now - 2 * 86400,
            action=1,
            item_no="FG-GROUP-SPACE",
            item_name="群組空白製成品",
            category=EOutputCategory.PRODUCT,
            itemSubCategory=51,
            batch_number="B-FG-GROUP-SPACE",
            serial_no="S-OUT-GROUP-SPACE",
            unit=1,
            count=18,
        ),
    ])
    obj_session.commit()

    dict_payload = CTraceabilityService()._CTraceabilityService__get_batch_overview_with_session(
        obj_session, "B-FG-GROUP-SPACE", "Asia/Taipei",
    )

    dict_step = next(
        dict_step for dict_step in dict_payload["traceSteps"]
        if dict_step["stepId"] == "production:WO-GROUP-SPACE::"
    )
    assert any(dict_item["batchNo"] == "B-WIP-GROUP-SPACE" for dict_item in dict_step["inputItems"])
    assert any(dict_item["batchNo"] == "B-FG-GROUP-SPACE" for dict_item in dict_step["outputItems"])


def test_trace_batch_overview_raw_material_does_not_expand_after_finished_goods_output():
    obj_session = build_session()
    n_now = seed_traceability(obj_session)
    obj_session.add_all([
        CTableProductionDataInput(
            work_order_no="WO-AFTER-FG",
            process_order_no="PROC-AFTER-FG",
            group="group_2",
            time=n_now - 1 * 86400,
            action=1,
            item_no="FG-001",
            item_name="製成品A",
            category=EOutputCategory.PRODUCT,
            itemSubCategory=51,
            batch_number="B-FG-001",
            serial_no="S-IN-AFTER-FG",
            unit=1,
            count=5,
        ),
        CTableProductionDataOutput(
            work_order_no="WO-AFTER-FG",
            process_order_no="PROC-AFTER-FG",
            group="group_2",
            time=n_now - 1 * 86400,
            action=1,
            item_no="FG-AFTER-FG",
            item_name="不應展開製成品",
            category=EOutputCategory.PRODUCT,
            itemSubCategory=51,
            batch_number="B-FG-AFTER-FG",
            serial_no="S-OUT-AFTER-FG",
            unit=1,
            count=5,
        ),
    ])
    obj_session.commit()

    dict_payload = CTraceabilityService()._CTraceabilityService__get_batch_overview_with_session(
        obj_session, "B-RM-001", "Asia/Taipei",
    )

    set_step_ids = {dict_step["stepId"] for dict_step in dict_payload["traceSteps"]}
    assert "production:WO-AFTER-FG::" not in set_step_ids


def test_trace_batch_overview_uses_batch_header_category_for_output_rows():
    obj_session = build_session()
    n_now = seed_traceability(obj_session)
    obj_session.add_all([
        CTableBatchNumber(
            date=n_now - 3 * 86400,
            no="B-RM-OUTPUT-ZERO",
            ref_no="GRN-OUTPUT-ZERO",
            refCategory=1,
            item_no="RM-OUTPUT-ZERO",
            item_name="產出類別異常原料",
            itemCategory=EItemCategory.PM,
            itemSubCategory=11,
            itemType=1,
            unit=1,
            expectedCount=30,
            checkedCount=30,
            validDays=90,
            validDate=n_now + 87 * 86400,
            creationTime=n_now - 3 * 86400,
        ),
        CTableBatchNumber(
            date=n_now - 2 * 86400,
            no="B-FG-OUTPUT-ZERO",
            ref_no="WO-OUTPUT-ZERO",
            refCategory=2,
            item_no="FG-OUTPUT-ZERO",
            item_name="產出類別異常製成品",
            itemCategory=EItemCategory.PRODUCT,
            itemSubCategory=51,
            itemType=1,
            unit=1,
            expectedCount=25,
            checkedCount=25,
            validDays=180,
            validDate=n_now + 178 * 86400,
            creationTime=n_now - 2 * 86400,
        ),
        CTableProductionData(work_order_no="WO-OUTPUT-ZERO", date=n_now - 2 * 86400, product_no="FG-OUTPUT-ZERO", product_name="產出類別異常製成品"),
        CTableProductionDataInput(
            work_order_no="WO-OUTPUT-ZERO",
            process_order_no="PROC-OUTPUT-ZERO",
            group="group_1",
            time=n_now - 2 * 86400,
            action=1,
            item_no="RM-OUTPUT-ZERO",
            item_name="產出類別異常原料",
            category=EItemCategory.PM,
            itemSubCategory=11,
            batch_number="B-RM-OUTPUT-ZERO",
            serial_no="S-IN-OUTPUT-ZERO",
            unit=1,
            count=28,
        ),
        CTableProductionDataOutput(
            work_order_no="WO-OUTPUT-ZERO",
            process_order_no="PROC-OUTPUT-ZERO",
            group="group_1",
            time=n_now - 2 * 86400,
            action=1,
            item_no="FG-OUTPUT-ZERO",
            item_name="產出類別異常製成品",
            category=0,
            itemSubCategory=51,
            batch_number="B-FG-OUTPUT-ZERO",
            serial_no="S-OUT-OUTPUT-ZERO",
            unit=1,
            count=25,
        ),
        CTableProductionDataInput(
            work_order_no="WO-AFTER-OUTPUT-ZERO",
            process_order_no="PROC-AFTER-OUTPUT-ZERO",
            group="group_2",
            time=n_now - 1 * 86400,
            action=1,
            item_no="FG-OUTPUT-ZERO",
            item_name="產出類別異常製成品",
            category=EItemCategory.PRODUCT,
            itemSubCategory=51,
            batch_number="B-FG-OUTPUT-ZERO",
            serial_no="S-IN-AFTER-OUTPUT-ZERO",
            unit=1,
            count=5,
        ),
        CTableProductionDataOutput(
            work_order_no="WO-AFTER-OUTPUT-ZERO",
            process_order_no="PROC-AFTER-OUTPUT-ZERO",
            group="group_2",
            time=n_now - 1 * 86400,
            action=1,
            item_no="FG-SHOULD-NOT-EXPAND",
            item_name="不應展開",
            category=0,
            itemSubCategory=51,
            batch_number="B-FG-SHOULD-NOT-EXPAND",
            serial_no="S-OUT-AFTER-OUTPUT-ZERO",
            unit=1,
            count=5,
        ),
    ])
    obj_session.commit()

    dict_payload = CTraceabilityService()._CTraceabilityService__get_batch_overview_with_session(
        obj_session, "B-RM-OUTPUT-ZERO", "Asia/Taipei",
    )

    dict_step = next(
        dict_step for dict_step in dict_payload["traceSteps"]
        if dict_step["refNo"] == "WO-OUTPUT-ZERO"
    )
    assert any(
        dict_item["batchNo"] == "B-FG-OUTPUT-ZERO" and dict_item["itemCategory"] == EItemCategory.PRODUCT
        for dict_item in dict_step["outputItems"]
    )
    set_step_ids = {dict_step["stepId"] for dict_step in dict_payload["traceSteps"]}
    assert "production:WO-AFTER-OUTPUT-ZERO::" not in set_step_ids


def test_trace_batch_overview_downstream_only_enqueues_inproduct_outputs():
    obj_session = build_session()
    n_now = seed_traceability(obj_session)
    obj_session.add_all([
        CTableBatchNumber(
            date=n_now - 3 * 86400,
            no="B-RM-UNKNOWN-OUTPUT",
            ref_no="GRN-UNKNOWN-OUTPUT",
            refCategory=1,
            item_no="RM-UNKNOWN-OUTPUT",
            item_name="未知產出原料",
            itemCategory=EItemCategory.PM,
            itemSubCategory=11,
            itemType=1,
            unit=1,
            expectedCount=30,
            checkedCount=30,
            validDays=90,
            validDate=n_now + 87 * 86400,
            creationTime=n_now - 3 * 86400,
        ),
        CTableProductionData(work_order_no="WO-UNKNOWN-OUTPUT", date=n_now - 2 * 86400, product_no="FG-UNKNOWN-OUTPUT", product_name="未知產出"),
        CTableProductionDataInput(
            work_order_no="WO-UNKNOWN-OUTPUT",
            process_order_no="PROC-UNKNOWN-OUTPUT",
            group="group_1",
            time=n_now - 2 * 86400,
            action=1,
            item_no="RM-UNKNOWN-OUTPUT",
            item_name="未知產出原料",
            category=EItemCategory.PM,
            itemSubCategory=11,
            batch_number="B-RM-UNKNOWN-OUTPUT",
            serial_no="S-IN-UNKNOWN-OUTPUT",
            unit=1,
            count=28,
        ),
        CTableProductionDataOutput(
            work_order_no="WO-UNKNOWN-OUTPUT",
            process_order_no="PROC-UNKNOWN-OUTPUT",
            group="group_1",
            time=n_now - 2 * 86400,
            action=1,
            item_no="UNKNOWN-OUTPUT",
            item_name="未知產出",
            category=0,
            itemSubCategory=0,
            batch_number="B-UNKNOWN-OUTPUT",
            serial_no="S-OUT-UNKNOWN-OUTPUT",
            unit=1,
            count=25,
        ),
        CTableProductionDataInput(
            work_order_no="WO-AFTER-UNKNOWN-OUTPUT",
            process_order_no="PROC-AFTER-UNKNOWN-OUTPUT",
            group="group_2",
            time=n_now - 1 * 86400,
            action=1,
            item_no="UNKNOWN-OUTPUT",
            item_name="未知產出",
            category=0,
            itemSubCategory=0,
            batch_number="B-UNKNOWN-OUTPUT",
            serial_no="S-IN-AFTER-UNKNOWN-OUTPUT",
            unit=1,
            count=5,
        ),
    ])
    obj_session.commit()

    dict_payload = CTraceabilityService()._CTraceabilityService__get_batch_overview_with_session(
        obj_session, "B-RM-UNKNOWN-OUTPUT", "Asia/Taipei",
    )

    set_step_ids = {dict_step["stepId"] for dict_step in dict_payload["traceSteps"]}
    assert "production:WO-UNKNOWN-OUTPUT::" in set_step_ids
    assert "production:WO-AFTER-UNKNOWN-OUTPUT::" not in set_step_ids


def test_trace_batch_overview_wip_root_is_not_expanded_in_v1():
    obj_session = build_session()
    seed_traceability(obj_session)
    dict_payload = CTraceabilityService()._CTraceabilityService__get_batch_overview_with_session(
        obj_session, "B-WIP-001", "Asia/Taipei",
    )

    assert dict_payload["batch"]["batchNo"] == "B-WIP-001"
    assert dict_payload["batch"]["traceStatusCode"] == ETraceStatusCode.UNKNOWN
    assert dict_payload["traceSteps"] == []


def test_trace_dashboard_does_not_build_overview_steps(monkeypatch):
    obj_session = build_session()
    seed_traceability(obj_session)

    def fail_build_steps(*args, **kwargs):
        raise AssertionError("dashboard must not build full trace steps")

    monkeypatch.setattr(CTraceabilityService, "_CTraceabilityService__build_trace_steps", fail_build_steps)
    dict_payload = CTraceabilityService()._CTraceabilityService__get_dashboard_with_session(
        obj_session, "Asia/Taipei", "", 0, "", "", "", "", 0, 2,
    )

    assert dict_payload["total"] == 4
    assert dict_payload["count"] == 2
    assert "nodes" not in dict_payload["records"][0]


def test_trace_batch_overview_invalid_batch_returns_none():
    obj_session = build_session()
    seed_traceability(obj_session)
    dict_payload = CTraceabilityService()._CTraceabilityService__get_batch_overview_with_session(
        obj_session, "NOT-FOUND", "Asia/Taipei",
    )

    assert dict_payload is None
