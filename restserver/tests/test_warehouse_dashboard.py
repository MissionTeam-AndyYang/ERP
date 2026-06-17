# coding=utf8
import json
import sys
from datetime import date
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.common.common import (
    EDepartment,
    EInventoryCategory,
    EInventoryDeltaKind,
    EItemCategory,
    EWarehouseRiskType,
    EWorkflowTaskStatus,
    EWorkflowTaskType,
)
from package.dbwrapper.table import (
    CTableBatchNumber,
    CTableInventoryDelta,
    CTableInventoryItemMonthStatistic,
    CTableInventoryRec,
    CTableItemSafetyStock,
    CTableMaterial,
    CTableShipWarehouse,
    CTableShipWarehouseAlias,
    CTableShipWarehouseContract,
    CTableWarehouseInventoryReservation,
    CTableWarehousePalletMovement,
    CTableWarehouseQualityHold,
    CTableWarehouseRiskRule,
    CTableWorkflowTaskState,
)
from package.restserver.api.v2.warehouse import (
    CWarehouseDashboardService,
    CWarehouseInventoryService,
    CWarehouseTaskService,
)


def build_session():
    obj_engine = create_engine("sqlite:///:memory:")
    for obj_table in [
        CTableInventoryRec.__table__,
        CTableInventoryDelta.__table__,
        CTableInventoryItemMonthStatistic.__table__,
        CTableBatchNumber.__table__,
        CTableMaterial.__table__,
        CTableShipWarehouseAlias.__table__,
        CTableShipWarehouse.__table__,
        CTableShipWarehouseContract.__table__,
        CTableWarehouseInventoryReservation.__table__,
        CTableWarehouseQualityHold.__table__,
        CTableWarehousePalletMovement.__table__,
        CTableItemSafetyStock.__table__,
        CTableWarehouseRiskRule.__table__,
        CTableWorkflowTaskState.__table__,
    ]:
        obj_table.create(bind=obj_engine)
    return sessionmaker(bind=obj_engine)()


def seed_dashboard_base(obj_session):
    n_now = 1700000000
    obj_session.add_all([
        CTableInventoryRec(
            warehouse_no="WH-A",
            warehouse_displayName="A倉",
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
            warehouse_displayName="A倉",
            ref_no="GRN-FUTURE",
            refCategory=1,
            date=n_now + 86400,
            category=EInventoryCategory.IN,
            batchNumber="B-RM-001",
            item_no="RM-001",
            item_name="原料A",
            itemCategory=EItemCategory.PM,
            itemType=1,
            unit=1,
            count=500,
            amount=5000,
        ),
        CTableInventoryRec(
            warehouse_no="WH-A",
            warehouse_displayName="A倉",
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
        CTableInventoryItemMonthStatistic(
            warehouse_no="WH-A",
            warehouse_displayName="Aå€‰",
            date=date(2023, 10, 31),
            timezone="Asia/Taipei",
            kind=EInventoryDeltaKind.BATCHNO,
            category=EItemCategory.PM,
            specified_no="B-RM-001",
            specified_name="B-RM-001",
            specified_ref_no="RM-001",
            specified_ref_name="åŽŸæ–™A",
            unit=1,
            startCount=0,
            startAmount=0,
            inCount=80,
            inAmount=800,
            endCount=80,
            endAmount=800,
            creationTime=n_now,
        ),
        CTableInventoryDelta(
            warehouse_no="WH-A",
            warehouse_displayName="Aå€‰",
            date=date(2023, 11, 15),
            timezone="Asia/Taipei",
            kind=EInventoryDeltaKind.BATCHNO,
            category=EItemCategory.PM,
            specified_no="B-RM-001",
            specified_name="B-RM-001",
            specified_ref_no="RM-001",
            specified_ref_name="åŽŸæ–™A",
            in_ref_id=["GRN-001"],
            out_ref_id=["WO-001"],
            inPurchaseCount=0,
            inPurchaseAmount=0,
            inCount=20,
            inAmount=200,
            outCount=10,
            outAmount=100,
            creationTime=n_now,
        ),
        CTableBatchNumber(
            no="B-RM-001",
            ref_no="PO-001",
            item_no="RM-001",
            item_name="原料A",
            itemCategory=EItemCategory.PM,
            itemSubCategory=11,
            itemType=1,
            unit=1,
            validDays=90,
            validDate=n_now + 20 * 86400,
        ),
        CTableMaterial(
            no="RM-001",
            category=EItemCategory.PM,
            subCategory=11,
            name="原料A",
            unitWarehouse=1,
        ),
        CTableWarehouseInventoryReservation(
            no="RES-001",
            date=n_now,
            refCategory=2,
            ref_no="WO-001",
            warehouse_no="WH-A",
            itemCategory=EItemCategory.PM,
            item_no="RM-001",
            item_name="原料A",
            batchNumber="B-RM-001",
            unit=1,
            reservedQuantity=20,
            unitCost=10,
            reservedValue=200,
            status=1,
            releaseTime=n_now + 86400,
        ),
        CTableWarehouseQualityHold(
            no="QH-001",
            date=n_now,
            refCategory=3,
            ref_no="GRN-001",
            warehouse_no="WH-A",
            itemCategory=EItemCategory.PM,
            item_no="RM-001",
            item_name="原料A",
            batchNumber="B-RM-001",
            unit=1,
            holdQuantity=5,
            unitCost=10,
            holdValue=50,
            status=1,
        ),
        CTableWarehousePalletMovement(
            no="PAL-001",
            date=n_now,
            warehouse_no="WH-A",
            itemCategory=EItemCategory.PM,
            item_no="RM-001",
            batchNumber="B-RM-001",
            palletStatus=1,
            palletCount=2,
        ),
        CTableWarehousePalletMovement(
            no="PAL-002",
            date=n_now,
            warehouse_no="WH-A",
            itemCategory=EItemCategory.PM,
            item_no="RM-001",
            batchNumber="B-RM-001",
            palletStatus=2,
            palletCount=1,
        ),
        CTableItemSafetyStock(
            no="SS-001",
            itemCategory=EItemCategory.PM,
            item_no="RM-001",
            item_name="原料A",
            warehouse_no="WH-A",
            unit=1,
            safetyStock=80,
            effectiveDate=n_now - 86400,
            status=1,
        ),
        CTableShipWarehouseAlias(no="WH-A", name="A倉", type=1),
        CTableShipWarehouse(no="SW-A", name="A倉板位", maxCapacity=10),
        CTableShipWarehouse(no="SW-SHIP", name="物流板位", maxCapacity=99),
        CTableShipWarehouseContract(
            no="SWC-001",
            date=n_now,
            sw_alias_no="WH-A",
            item_no="SW-A",
            category=2,
        ),
        CTableShipWarehouseContract(
            no="SWC-SHIP-001",
            date=n_now,
            sw_alias_no="WH-A",
            item_no="SW-SHIP",
            category=1,
        ),
        CTableWorkflowTaskState(
            taskId="TASK-IN-001",
            module=7,
            taskType=EWorkflowTaskType.INBOUND,
            refCategory=3,
            ref_no="GRN-001",
            itemCategory=EItemCategory.PM,
            item_no="RM-001",
            item_name="原料A",
            batchNumber="B-RM-001",
            warehouse_no="WH-A",
            expectedQuantity=100,
            processedQuantity=0,
            unit=1,
            palletCount=2,
            dueTimestamp=n_now + 3600,
            taskStatus=EWorkflowTaskStatus.PENDING,
            ownerDepartment=EDepartment.WAREHOUSE,
        ),
        CTableWorkflowTaskState(
            taskId="TASK-OUT-001",
            module=7,
            taskType=EWorkflowTaskType.OUTBOUND,
            refCategory=2,
            ref_no="WO-001",
            itemCategory=EItemCategory.PM,
            item_no="RM-001",
            item_name="原料A",
            batchNumber="B-RM-001",
            warehouse_no="WH-A",
            expectedQuantity=20,
            processedQuantity=5,
            unit=1,
            palletCount=1,
            dueTimestamp=n_now + 7200,
            taskStatus=EWorkflowTaskStatus.PARTIAL,
            ownerDepartment=EDepartment.PRODUCTION,
        ),
    ])
    obj_session.commit()
    return n_now


def test_dashboard_service_builds_warehouse_summary():
    obj_session = build_session()
    n_now = seed_dashboard_base(obj_session)

    dict_payload = CWarehouseDashboardService().get_dashboard(
        n_date=n_now,
        str_timezone="Asia/Taipei",
        str_warehouse_no="WH-A",
        n_item_category=EItemCategory.PM,
        b_include_inventory=True,
        obj_session=obj_session,
    )

    assert dict_payload["summary"]["totalInventoryValue"] == 900.0
    assert dict_payload["summary"]["reservedInventoryValue"] == 200.0
    assert dict_payload["summary"]["qualityHoldInventoryValue"] == 50.0
    assert dict_payload["summary"]["availableInventoryValue"] == 650.0
    assert dict_payload["summary"]["totalPallets"] == 10.0
    assert dict_payload["summary"]["usedPallets"] == 2.0
    assert dict_payload["summary"]["reservedPallets"] == 1.0
    assert dict_payload["summary"]["availablePallets"] == 7.0
    assert dict_payload["summary"]["pendingInboundCount"] == 1
    assert dict_payload["summary"]["pendingOutboundCount"] == 1
    assert dict_payload["range"]["date"] == "2023-11-15"
    assert dict_payload["range"]["startTimestamp"] == 1699977600
    assert dict_payload["range"]["endTimestamp"] == 1700063999

    dict_category = dict_payload["inventoryValueByCategory"][0]
    assert dict_category["inventoryValue"] == 900.0
    assert dict_category["availableValue"] == 650.0
    assert dict_category["palletCount"] == 2.0

    dict_inventory = dict_payload["inventory"][0]
    assert dict_inventory["currentQuantity"] == 90.0
    assert dict_inventory["reservedQuantity"] == 20.0
    assert dict_inventory["qualityHoldQuantity"] == 5.0
    assert dict_inventory["availableQuantity"] == 65.0


def test_dashboard_service_uses_record_fallback_for_missing_stat_rows():
    obj_session = build_session()
    n_now = seed_dashboard_base(obj_session)
    obj_session.add_all([
        CTableInventoryRec(
            warehouse_no="WH-A",
            warehouse_displayName="Aå€‰",
            ref_no="GRN-002",
            refCategory=1,
            date=n_now - 2 * 86400,
            category=EInventoryCategory.IN,
            batchNumber="B-RM-002",
            item_no="RM-002",
            item_name="Fallback Material",
            itemCategory=EItemCategory.PM,
            itemType=1,
            unit=1,
            count=30,
            amount=300,
        ),
        CTableBatchNumber(
            no="B-RM-002",
            ref_no="PO-002",
            item_no="RM-002",
            item_name="Fallback Material",
            itemCategory=EItemCategory.PM,
            itemSubCategory=12,
            itemType=1,
            unit=1,
            validDays=120,
            validDate=n_now + 80 * 86400,
        ),
        CTableMaterial(
            no="RM-002",
            category=EItemCategory.PM,
            subCategory=12,
            name="Fallback Material",
            unitWarehouse=1,
        ),
    ])
    obj_session.commit()

    dict_payload = CWarehouseDashboardService().get_dashboard(
        n_date=n_now,
        str_timezone="Asia/Taipei",
        str_warehouse_no="WH-A",
        n_item_category=EItemCategory.PM,
        b_include_inventory=True,
        obj_session=obj_session,
    )

    assert dict_payload["summary"]["totalInventoryValue"] == 1200.0
    dict_inventory_by_item = {
        dict_row["itemNo"]: dict_row
        for dict_row in dict_payload["inventory"]
    }
    assert dict_inventory_by_item["RM-001"]["currentQuantity"] == 90.0
    assert dict_inventory_by_item["RM-002"]["currentQuantity"] == 30.0
    assert dict_inventory_by_item["RM-002"]["inventoryValue"] == 300.0


def test_dashboard_service_builds_risk_alerts():
    obj_session = build_session()
    n_now = seed_dashboard_base(obj_session)

    dict_payload = CWarehouseDashboardService().get_dashboard(
        n_date=n_now,
        str_warehouse_no="WH-A",
        n_item_category=EItemCategory.PM,
        obj_session=obj_session,
    )

    lst_risk_types = [dict_row["riskType"] for dict_row in dict_payload["riskAlerts"]]
    assert EWarehouseRiskType.TURNOVER_OVER_30_DAYS in lst_risk_types
    assert EWarehouseRiskType.SHELF_LIFE_LT_ONE_THIRD in lst_risk_types
    assert EWarehouseRiskType.BELOW_SAFETY_STOCK in lst_risk_types
    for dict_risk in dict_payload["riskAlerts"]:
        assert "message" not in dict_risk
        assert "recommendedAction" not in dict_risk
        assert dict_risk["messageCode"].startswith("warehouse.risk.")
        assert dict_risk["recommendedActionCode"].startswith("warehouse.action.")
        assert "currentQuantity" in dict_risk["messageParams"]


def test_inventory_service_returns_confirmed_inventory_dataset():
    obj_session = build_session()
    n_now = seed_dashboard_base(obj_session)

    dict_payload = CWarehouseInventoryService().get_inventory(
        n_date=n_now,
        str_timezone="Asia/Taipei",
        str_warehouse_no="WH-A",
        n_item_category=EItemCategory.PM,
        obj_session=obj_session,
    )

    assert dict_payload["total"] == 1
    dict_inventory = dict_payload["results"][0]
    assert dict_inventory["inventoryId"] == "WH-A|RM-001|B-RM-001|"
    assert dict_inventory["itemSubCategory"] == 11
    assert dict_inventory["itemType"] == 1
    assert dict_inventory["currentQuantity"] == 90.0
    assert dict_inventory["reservedQuantity"] == 20.0
    assert dict_inventory["qualityHoldQuantity"] == 5.0
    assert dict_inventory["availableQuantity"] == 65.0
    assert dict_inventory["inventoryValue"] == 900.0
    assert dict_inventory["availableValue"] == 650.0
    assert dict_inventory["palletCount"] == 2.0
    assert dict_inventory["qualityStatus"] == "hold"
    assert dict_inventory["sourceNo"] == "GRN-001"
    assert EWarehouseRiskType.BELOW_SAFETY_STOCK in dict_inventory["riskTypes"]


def test_task_service_returns_confirmed_task_dataset():
    obj_session = build_session()
    seed_dashboard_base(obj_session)

    dict_payload = CWarehouseTaskService().get_tasks(
        str_timezone="Asia/Taipei",
        str_warehouse_no="WH-A",
        obj_session=obj_session,
    )

    assert dict_payload["total"] == 2
    assert dict_payload["count"] == 2
    assert dict_payload["results"][0]["taskId"] == "TASK-IN-001"
    assert dict_payload["results"][0]["warehouseName"] == "A倉"
    assert dict_payload["results"][0]["remainingQuantity"] == 100.0
    assert dict_payload["results"][1]["taskId"] == "TASK-OUT-001"
    assert dict_payload["results"][1]["remainingQuantity"] == 15.0


def test_inventory_and_tasks_routes_return_existing_api_envelope(monkeypatch):
    from flask import Flask

    from package.restserver.api.v2.warehouse_uri import warehouse_v2

    def fake_get_inventory(self, **dict_kwargs):
        return {
            "serverTimestamp": 1700000000,
            "timezone": "Asia/Taipei",
            "total": 1,
            "count": 1,
            "start": 0,
            "results": [{"inventoryId": "WH-A|RM-001|B-RM-001|"}],
        }

    def fake_get_tasks(self, **dict_kwargs):
        return {
            "serverTimestamp": 1700000000,
            "timezone": "Asia/Taipei",
            "total": 1,
            "count": 1,
            "start": 0,
            "results": [{"taskId": "TASK-IN-001"}],
        }

    monkeypatch.setenv("TOKEN_ENABLED", "1")
    monkeypatch.setattr(CWarehouseInventoryService, "get_inventory", fake_get_inventory)
    monkeypatch.setattr(CWarehouseTaskService, "get_tasks", fake_get_tasks)

    obj_app = Flask(__name__)
    obj_app.register_blueprint(warehouse_v2)
    obj_client = obj_app.test_client()

    obj_inventory_response = obj_client.get(
        "/api/v2/warehouse/inventory",
        headers={"x-auth-token": "test-token", "x-timezone": "Asia/Taipei"},
    )
    obj_tasks_response = obj_client.get(
        "/api/v2/warehouse/tasks",
        headers={"x-auth-token": "test-token", "x-timezone": "Asia/Taipei"},
    )

    assert obj_inventory_response.status_code == 200
    dict_inventory_data = json.loads(obj_inventory_response.data.decode("utf8"))
    assert dict_inventory_data["code"] == 0
    assert dict_inventory_data["payload"]["results"][0]["inventoryId"] == "WH-A|RM-001|B-RM-001|"

    assert obj_tasks_response.status_code == 200
    dict_tasks_data = json.loads(obj_tasks_response.data.decode("utf8"))
    assert dict_tasks_data["code"] == 0
    assert dict_tasks_data["payload"]["results"][0]["taskId"] == "TASK-IN-001"


def test_dashboard_route_returns_existing_api_envelope(monkeypatch):
    from flask import Flask

    from package.restserver.api.v2.warehouse_uri import warehouse_v2

    def fake_get_dashboard(self, **dict_kwargs):
        return {
            "serverTimestamp": 1700000000,
            "summary": {"totalInventoryValue": 100.0},
            "inventoryValueByCategory": [],
            "capacityByWarehouse": [],
            "riskAlerts": [],
            "pendingTasks": [],
            "valueTrend": [],
            "inventory": [],
        }

    monkeypatch.setenv("TOKEN_ENABLED", "1")
    monkeypatch.setattr(CWarehouseDashboardService, "get_dashboard", fake_get_dashboard)

    obj_app = Flask(__name__)
    obj_app.register_blueprint(warehouse_v2)
    obj_client = obj_app.test_client()

    obj_response = obj_client.get(
        "/api/v2/warehouse/dashboard?includeInventory=true",
        headers={"x-auth-token": "test-token", "x-timezone": "Asia/Taipei"},
    )

    assert obj_response.status_code == 200
    dict_data = json.loads(obj_response.data.decode("utf8"))
    assert dict_data["code"] == 0
    assert dict_data["message"] == "success"
    assert dict_data["payload"]["summary"]["totalInventoryValue"] == 100.0
