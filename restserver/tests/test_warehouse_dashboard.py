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
    EDepartment,
    EInventoryCategory,
    EItemCategory,
    EWarehouseRiskType,
    EWorkflowTaskStatus,
    EWorkflowTaskType,
)
from package.dbwrapper.table import (
    CTableBatchNumber,
    CTableInventoryRec,
    CTableItemSafetyStock,
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
    CWarehouseInventoryLotService,
)


def build_session():
    obj_engine = create_engine("sqlite:///:memory:")
    for obj_table in [
        CTableInventoryRec.__table__,
        CTableBatchNumber.__table__,
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
            date=n_now - 40 * 86400,
            category=EInventoryCategory.IN,
            batchNumber="B-RM-001",
            item_no="RM-001",
            item_name="原料A",
            itemCategory=EItemCategory.PM,
            unit=1,
            count=100,
            amount=1000,
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
            unit=1,
            count=10,
            amount=100,
        ),
        CTableBatchNumber(
            no="B-RM-001",
            ref_no="PO-001",
            item_no="RM-001",
            item_name="原料A",
            itemCategory=EItemCategory.PM,
            unit=1,
            validDays=90,
            validDate=n_now + 20 * 86400,
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
            safetyStock=95,
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

    dict_category = dict_payload["inventoryValueByCategory"][0]
    assert dict_category["inventoryValue"] == 900.0
    assert dict_category["availableValue"] == 650.0
    assert dict_category["palletCount"] == 2.0

    dict_inventory = dict_payload["inventory"][0]
    assert dict_inventory["currentQuantity"] == 90.0
    assert dict_inventory["reservedQuantity"] == 20.0
    assert dict_inventory["qualityHoldQuantity"] == 5.0
    assert dict_inventory["availableQuantity"] == 65.0


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
        assert "Ã" not in dict_risk["message"]
        assert "Â" not in dict_risk["message"]
        assert "Ã" not in dict_risk["recommendedAction"]
        assert "Â" not in dict_risk["recommendedAction"]
    assert "此批庫存迴轉週期超過 30 天。" in [
        dict_risk["message"] for dict_risk in dict_payload["riskAlerts"]
    ]


def test_inventory_lot_service_returns_list_and_detail():
    obj_session = build_session()
    n_now = seed_dashboard_base(obj_session)

    dict_payload = CWarehouseInventoryLotService().get_lots(
        n_date=n_now,
        str_timezone="Asia/Taipei",
        str_warehouse_no="WH-A",
        n_item_category=EItemCategory.PM,
        str_sort="inventoryValue",
        obj_session=obj_session,
    )

    assert dict_payload["total"] == 1
    assert dict_payload["summary"]["lotCount"] == 1
    assert dict_payload["summary"]["totalInventoryValue"] == 900.0
    assert dict_payload["summary"]["totalAvailableValue"] == 650.0
    dict_lot = dict_payload["results"][0]
    assert dict_lot["lotKey"] == "WH-A|RM-001|B-RM-001"
    assert dict_lot["currentQuantity"] == 90.0
    assert dict_lot["reservedQuantity"] == 20.0
    assert dict_lot["qualityHoldQuantity"] == 5.0
    assert dict_lot["availableQuantity"] == 65.0
    assert dict_lot["palletCount"] == 2.0
    assert dict_lot["openTaskCount"] == 2
    assert EWarehouseRiskType.BELOW_SAFETY_STOCK in dict_lot["riskTypes"]

    dict_detail = CWarehouseInventoryLotService().get_lot_detail(
        str_lot_key=dict_lot["lotKey"],
        n_date=n_now,
        str_timezone="Asia/Taipei",
        obj_session=obj_session,
    )

    assert dict_detail["lot"]["lotKey"] == "WH-A|RM-001|B-RM-001"
    assert len(dict_detail["sourceDocuments"]) == 2
    assert dict_detail["reservations"][0]["reservationNo"] == "RES-001"
    assert dict_detail["qualityHolds"][0]["holdNo"] == "QH-001"
    assert len(dict_detail["palletMovements"]) == 2
    assert len(dict_detail["workflowTasks"]) == 2


def test_inventory_lot_route_returns_existing_api_envelope(monkeypatch):
    from flask import Flask

    from package.restserver.api.v2.warehouse_uri import warehouse_v2

    def fake_get_lots(self, **dict_kwargs):
        return {
            "serverTimestamp": 1700000000,
            "timezone": "Asia/Taipei",
            "total": 1,
            "count": 1,
            "start": 0,
            "summary": {"lotCount": 1},
            "results": [{"lotKey": "WH-A|RM-001|B-RM-001"}],
        }

    monkeypatch.setenv("TOKEN_ENABLED", "1")
    monkeypatch.setattr(CWarehouseInventoryLotService, "get_lots", fake_get_lots)

    obj_app = Flask(__name__)
    obj_app.register_blueprint(warehouse_v2)
    obj_client = obj_app.test_client()

    obj_response = obj_client.get(
        "/api/v2/warehouse/inventory/lots",
        headers={"x-auth-token": "test-token", "x-timezone": "Asia/Taipei"},
    )

    assert obj_response.status_code == 200
    dict_data = json.loads(obj_response.data.decode("utf8"))
    assert dict_data["code"] == 0
    assert dict_data["message"] == "success"
    assert dict_data["payload"]["summary"]["lotCount"] == 1


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
