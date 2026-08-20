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
    ETraceEventTypeCode,
    ETraceRelationTypeCode,
    ETraceRiskCode,
    ETraceRiskLevelCode,
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
        CTableProductionDataOutput(
            work_order_no="WO-001",
            process_order_no="PROC-001",
            group="G-001",
            time=n_now - 10 * 86400,
            action=1,
            item_no="WIP-001",
            item_name="半成品A",
            category=EItemCategory.INPRODUCT,
            itemSubCategory=41,
            batch_number="B-WIP-001",
            serial_no="S-OUT-001",
            unit=1,
            count=45,
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
            category=EItemCategory.PRODUCT,
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


def test_trace_batch_overview_builds_multilevel_graph():
    obj_session = build_session()
    seed_traceability(obj_session)
    dict_payload = CTraceabilityService()._CTraceabilityService__get_batch_overview_with_session(
        obj_session, "B-RM-001", "Asia/Taipei",
    )

    assert dict_payload["batch"]["batchNo"] == "B-RM-001"
    assert dict_payload["batch"]["traceStatusCode"] == ETraceStatusCode.COMPLETE
    set_node_ids = {dict_node["nodeId"] for dict_node in dict_payload["nodes"]}
    assert "batch:B-RM-001" in set_node_ids
    assert "batch:B-WIP-001" in set_node_ids
    assert "batch:B-FG-001" in set_node_ids
    assert any(dict_node["nodeTypeCode"] == "receipt" and dict_node["refNo"] == "GRN-001" for dict_node in dict_payload["nodes"])
    set_relations = {dict_edge["relationTypeCode"] for dict_edge in dict_payload["edges"]}
    assert ETraceRelationTypeCode.RECEIVED_AS in set_relations
    assert ETraceRelationTypeCode.CONSUMED_BY in set_relations
    assert ETraceRelationTypeCode.PRODUCED_AS in set_relations
    set_events = {dict_event["eventTypeCode"] for dict_event in dict_payload["timeline"]}
    assert ETraceEventTypeCode.RECEIPT in set_events
    assert ETraceEventTypeCode.PRODUCTION_INPUT in set_events
    assert ETraceEventTypeCode.PRODUCTION_OUTPUT in set_events
    assert ETraceEventTypeCode.QUALITY_HOLD in set_events


def test_trace_batch_overview_finished_goods_traces_upstream_to_material_receipt():
    obj_session = build_session()
    seed_traceability(obj_session)
    dict_payload = CTraceabilityService()._CTraceabilityService__get_batch_overview_with_session(
        obj_session, "B-FG-001", "Asia/Taipei",
    )

    assert dict_payload["batch"]["batchNo"] == "B-FG-001"
    set_node_ids = {dict_node["nodeId"] for dict_node in dict_payload["nodes"]}
    assert "batch:B-FG-001" in set_node_ids
    assert "batch:B-WIP-001" in set_node_ids
    assert "batch:B-RM-001" in set_node_ids
    assert any(dict_node["nodeTypeCode"] == "receipt" and dict_node["refNo"] == "GRN-001" for dict_node in dict_payload["nodes"])
    set_events = {dict_event["eventTypeCode"] for dict_event in dict_payload["timeline"]}
    assert ETraceEventTypeCode.RECEIPT in set_events
    assert ETraceEventTypeCode.PRODUCTION_INPUT in set_events
    assert ETraceEventTypeCode.PRODUCTION_OUTPUT in set_events


def test_trace_dashboard_does_not_build_overview_graph(monkeypatch):
    obj_session = build_session()
    seed_traceability(obj_session)

    def fail_build_graph(*args, **kwargs):
        raise AssertionError("dashboard must not build full trace graph")

    monkeypatch.setattr(CTraceabilityService, "_CTraceabilityService__build_trace_graph", fail_build_graph)
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
