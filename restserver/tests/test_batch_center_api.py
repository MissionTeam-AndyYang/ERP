# coding=utf8
import json
import sys
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.common.common import (
    EBatchExpiryStatusCode,
    EBatchRiskCode,
    EBatchRiskLevelCode,
    EBatchStageCode,
    EInventoryCategory,
    EItemCategory,
    EWorkflowTaskStatus,
    EWorkflowTaskType,
)
from package.dbwrapper.table import (
    CTableBatchNumber,
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
from package.restserver.api.v2.batches import CBatchCenterService


def build_session():
    obj_engine = create_engine("sqlite:///:memory:")
    for obj_table in [
        CTableInventoryRec.__table__,
        CTableInventoryDelta.__table__,
        CTableInventoryItemMonthStatistic.__table__,
        CTableInventoryMonthStatistic.__table__,
        CTableBatchNumber.__table__,
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


def seed_batch_center(obj_session):
    n_now = 1700000000
    obj_session.add_all([
        CTableInventoryRec(
            warehouse_no="WH-A",
            warehouse_displayName="倉A",
            ref_no="GRN-001",
            refCategory=1,
            date=n_now - 40 * 86400,
            category=EInventoryCategory.IN,
            batchNumber="B-RM-001",
            item_no="RM-001",
            item_name="原料A",
            itemCategory=EItemCategory.PM,
            itemType=1,
            unit=1,
            count=100,
            amount=1000,
        ),
        CTableInventoryRec(
            warehouse_no="WH-A",
            warehouse_displayName="倉A",
            ref_no="WO-001",
            refCategory=2,
            date=n_now - 5 * 86400,
            category=EInventoryCategory.OUT,
            batchNumber="B-RM-001",
            item_no="RM-001",
            item_name="原料A",
            itemCategory=EItemCategory.PM,
            itemType=1,
            unit=1,
            count=10,
            amount=100,
        ),
        CTableBatchNumber(
            date=n_now - 40 * 86400,
            no="B-RM-001",
            ref_no="GRN-001",
            refCategory=1,
            item_no="RM-001",
            item_name="原料A",
            itemCategory=EItemCategory.PM,
            itemSubCategory=11,
            itemType=1,
            unit=1,
            validDays=90,
            validDate=n_now + 20 * 86400,
            creator_no="EMP-001",
            creationTime=n_now - 40 * 86400,
        ),
        CTableMaterial(
            no="RM-001",
            category=EItemCategory.PM,
            subCategory=11,
            name="原料A",
            unitWarehouse=1,
        ),
        CTableShipWarehouseAlias(
            no="WH-A",
            name="倉A",
            category=2,
        ),
        CTableWarehouseInventoryReservation(
            no="RES-001",
            date=n_now,
            refCategory=9,
            ref_no="SHIP-001",
            warehouse_no="WH-A",
            itemCategory=EItemCategory.PM,
            item_no="RM-001",
            item_name="原料A",
            batchNumber="B-RM-001",
            unit=1,
            reservedQuantity=20,
            reservedValue=200,
            status=1,
            releaseTime=n_now + 86400,
        ),
        CTableWarehouseQualityHold(
            no="QH-001",
            date=n_now,
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
            reason="inspection",
            creationTime=n_now,
        ),
        CTableWarehousePalletMovement(
            no="PAL-001",
            date=n_now,
            refCategory=4,
            ref_no="IN-001",
            warehouse_no="WH-A",
            pallet_group_no="P-001",
            batchNumber="B-RM-001",
            itemCategory=EItemCategory.PM,
            item_no="RM-001",
            palletStatus=1,
            palletCount=2,
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
            dueTimestamp=n_now + 3600,
            taskStatus=EWorkflowTaskStatus.BLOCKED,
            ownerDepartment=5,
        ),
        CTableProductionData(
            work_order_no="WO-001",
            date=n_now,
            product_no="PRD-001",
        ),
        CTableProductionDataOutput(
            work_order_no="WO-001",
            process_order_no="PROC-001",
            time=n_now,
            action=1,
            group="G-001",
            item_no="RM-001",
            item_name="原料A",
            category=EItemCategory.PM,
            itemSubCategory=11,
            batch_number="B-RM-001",
            serial_no="S-001",
            unit=1,
            count=3,
        ),
    ])
    obj_session.commit()
    return n_now


def test_batch_center_dashboard_groups_item_and_risk_fields():
    obj_session = build_session()
    n_now = seed_batch_center(obj_session)
    dict_payload = CBatchCenterService()._CBatchCenterService__get_dashboard_with_session(
        obj_session, n_now, "Asia/Taipei", "", 0, 0, 0, "", "", "", "", "", "", 0, 50,
    )

    assert dict_payload["summary"]["stockItemCount"] == 1
    assert dict_payload["summary"]["stockBatchCount"] == 1
    assert dict_payload["summary"]["qualityHoldQuantity"] == 5.0
    assert dict_payload["summary"]["highRiskItemCount"] == 1
    dict_item = dict_payload["items"][0]
    assert dict_item["itemNo"] == "RM-001"
    assert dict_item["currentQuantity"] == 90.0
    assert dict_item["availableQuantity"] == 65.0
    assert dict_item["unit"] == 1
    assert dict_item["riskLevelCode"] == EBatchRiskLevelCode.HIGH_RISK
    assert dict_item["riskCode"] == EBatchRiskCode.QUALITY_HOLD
    assert dict_item["ownerDepartment"] == 5


def test_batch_center_distribution_returns_warehouse_stock_rows():
    obj_session = build_session()
    n_now = seed_batch_center(obj_session)
    dict_payload = CBatchCenterService()._CBatchCenterService__get_distribution_with_session(
        obj_session, "RM-001", n_now, "Asia/Taipei", "", 0, 0, 0, "", "", "", "", "", "", 0, 50,
    )

    assert dict_payload["item"]["itemNo"] == "RM-001"
    dict_rows = {
        dict_row["batchStageCode"]: dict_row
        for dict_row in dict_payload["batches"]
    }
    assert EBatchStageCode.QUALITY_HOLD in dict_rows
    assert EBatchStageCode.PRODUCTION_OUTPUT not in dict_rows
    assert dict_rows[EBatchStageCode.QUALITY_HOLD]["currentQuantity"] == 90.0
    assert dict_rows[EBatchStageCode.QUALITY_HOLD]["daysInStock"] == 40
    assert dict_rows[EBatchStageCode.QUALITY_HOLD]["expiryStatusCode"] == EBatchExpiryStatusCode.NEAR_EXPIRY
    assert dict_rows[EBatchStageCode.QUALITY_HOLD]["refNo"] == "GRN-001"
    assert dict_rows[EBatchStageCode.QUALITY_HOLD]["relatedDocuments"]
    assert isinstance(dict_rows[EBatchStageCode.QUALITY_HOLD]["batchStageCode"], str)


def test_batch_center_detail_returns_confirmed_child_datasets():
    obj_session = build_session()
    n_now = seed_batch_center(obj_session)
    dict_payload = CBatchCenterService()._CBatchCenterService__get_detail_with_session(
        obj_session, "B-RM-001", n_now, "Asia/Taipei",
    )

    assert dict_payload["batch"]["batchNo"] == "B-RM-001"
    assert dict_payload["batch"]["refNo"] == "GRN-001"
    assert dict_payload["stockByWarehouse"][0]["currentQuantity"] == 90.0
    assert dict_payload["inventoryRecords"][0]["refNo"] == "WO-001"
    assert dict_payload["reservations"][0]["reservationNo"] == "RES-001"
    assert dict_payload["qualityHolds"][0]["holdNo"] == "QH-001"
    assert dict_payload["palletMovements"][0]["movementNo"] == "PAL-001"
    assert dict_payload["tasks"][0]["taskId"] == "TASK-QA-001"


def test_batch_center_routes_return_api_envelope(monkeypatch):
    from flask import Flask

    from package.restserver.api.v2.batches import CBatchCenterService
    from package.restserver.api.v2.batches_uri import batches_v2

    def fake_get_dashboard(self, **dict_kwargs):
        return {"serverTimestamp": 1, "summary": {}, "items": [], "total": 0, "start": 0, "count": 0}

    def fake_get_distribution(self, **dict_kwargs):
        return {"item": {"itemNo": dict_kwargs.get("str_item_no")}, "batches": [], "total": 0, "start": 0, "count": 0}

    def fake_get_detail(self, **dict_kwargs):
        return {"batch": {"batchNo": dict_kwargs.get("str_batch_no")}, "stockByWarehouse": [], "inventoryRecords": [], "reservations": [], "qualityHolds": [], "palletMovements": [], "tasks": []}

    monkeypatch.setenv("TOKEN_ENABLED", "1")
    monkeypatch.setattr(CBatchCenterService, "get_dashboard", fake_get_dashboard)
    monkeypatch.setattr(CBatchCenterService, "get_distribution", fake_get_distribution)
    monkeypatch.setattr(CBatchCenterService, "get_detail", fake_get_detail)

    obj_app = Flask(__name__)
    obj_app.register_blueprint(batches_v2)
    obj_app.config["TESTING"] = True
    obj_client = obj_app.test_client()

    dict_headers = {"x-auth-token": "test-token", "x-timezone": "Asia/Taipei"}
    obj_dashboard_response = obj_client.get("/api/v2/batches/dashboard", headers=dict_headers)
    obj_distribution_response = obj_client.get("/api/v2/batches/items/RM-001/distribution", headers=dict_headers)
    obj_detail_response = obj_client.get("/api/v2/batches/B-RM-001/detail", headers=dict_headers)

    assert obj_dashboard_response.status_code == 200
    assert json.loads(obj_dashboard_response.data.decode("utf8"))["code"] == 0
    assert json.loads(obj_distribution_response.data.decode("utf8"))["payload"]["item"]["itemNo"] == "RM-001"
    assert json.loads(obj_detail_response.data.decode("utf8"))["payload"]["batch"]["batchNo"] == "B-RM-001"
