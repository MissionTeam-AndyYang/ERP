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
    CTableInventoryMonthStatistic,
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
    CTableWorkflowTaskEvent,
    CTableWorkflowTaskState,
)
from package.restserver.api.v2.warehouse import (
    CWarehouseDashboardService,
    CWarehouseInventoryLotService,
    CWarehouseInventoryService,
    CWarehouseTaskWorkbenchService,
    CWarehouseTaskService,
)


def build_session():
    obj_engine = create_engine("sqlite:///:memory:")
    for obj_table in [
        CTableInventoryRec.__table__,
        CTableInventoryDelta.__table__,
        CTableInventoryItemMonthStatistic.__table__,
        CTableInventoryMonthStatistic.__table__,
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
        CTableWorkflowTaskEvent.__table__,
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
            date=n_now - 40 * 86400,
            no="B-RM-001",
            ref_no="PO-001",
            refCategory=1,
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
        CTableWorkflowTaskEvent(
            taskId="TASK-OUT-001",
            eventCode="workflow.task.created",
            eventTimestamp=n_now - 3600,
            fromStatus=None,
            toStatus=EWorkflowTaskStatus.PENDING,
            fromDepartment=None,
            toDepartment=EDepartment.WAREHOUSE,
            actorId="system",
            actorName="System",
            refCategory=2,
            ref_no="WO-001",
            ref_sub_no="",
            warehouse_no="WH-A",
            item_no="RM-001",
            batchNumber="B-RM-001",
            quantity=20,
            unit=1,
            note="created",
            creationTime=n_now - 3600,
            updateTime=n_now - 3600,
        ),
        CTableWorkflowTaskEvent(
            taskId="TASK-OUT-001",
            eventCode="workflow.task.started",
            eventTimestamp=n_now - 1800,
            fromStatus=EWorkflowTaskStatus.PENDING,
            toStatus=EWorkflowTaskStatus.PARTIAL,
            fromDepartment=EDepartment.WAREHOUSE,
            toDepartment=EDepartment.PRODUCTION,
            actorId="u001",
            actorName="Warehouse Lead",
            refCategory=2,
            ref_no="WO-001",
            ref_sub_no="",
            warehouse_no="WH-A",
            item_no="RM-001",
            batchNumber="B-RM-001",
            quantity=5,
            unit=1,
            note="started",
            creationTime=n_now - 1800,
            updateTime=n_now - 1800,
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
    assert dict_category["trend7Days"] == -10.0
    assert len(dict_payload["valueTrend"]) == 7
    assert dict_payload["valueTrend"][0]["date"] == "2023-11-09"
    assert dict_payload["valueTrend"][-1]["date"] == "2023-11-15"
    assert dict_payload["valueTrend"][-1]["inventoryValue"] == 900.0

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


def test_dashboard_service_uses_record_refresh_when_delta_date_is_stale():
    obj_session = build_session()
    n_now = seed_dashboard_base(obj_session)

    dict_payload = CWarehouseDashboardService().get_dashboard(
        n_date=n_now + 2 * 86400,
        str_timezone="Asia/Taipei",
        str_warehouse_no="WH-A",
        n_item_category=EItemCategory.PM,
        b_include_inventory=True,
        obj_session=obj_session,
    )

    assert dict_payload["summary"]["totalInventoryValue"] == 5900.0
    dict_inventory = dict_payload["inventory"][0]
    assert dict_inventory["currentQuantity"] == 590.0
    assert dict_inventory["inventoryValue"] == 5900.0


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
    assert "sourceType" not in dict_inventory
    assert dict_inventory["sourceNo"] == "PO-001"
    assert dict_inventory["sourceRefCategory"] == 1
    assert EWarehouseRiskType.BELOW_SAFETY_STOCK in dict_inventory["riskTypes"]


def test_inventory_lot_service_returns_confirmed_lot_dataset():
    obj_session = build_session()
    n_now = seed_dashboard_base(obj_session)

    dict_payload = CWarehouseInventoryLotService().get_lots(
        n_date=n_now,
        str_timezone="Asia/Taipei",
        str_warehouse_no="WH-A",
        n_item_category=EItemCategory.PM,
        obj_session=obj_session,
    )

    assert dict_payload["total"] == 1
    assert dict_payload["summary"]["lotCount"] == 1
    assert dict_payload["summary"]["itemCount"] == 1
    assert dict_payload["summary"]["totalInventoryValue"] == 900.0
    assert dict_payload["summary"]["pendingTaskCount"] == 2

    dict_lot = dict_payload["results"][0]
    assert dict_lot["lotKey"] == "WH-A|RM-001|B-RM-001"
    assert dict_lot["currentQuantity"] == 90.0
    assert dict_lot["reservedQuantity"] == 20.0
    assert dict_lot["qualityHoldQuantity"] == 5.0
    assert dict_lot["availableQuantity"] == 65.0
    assert dict_lot["unitCost"] == 10.0
    assert dict_lot["palletCount"] == 2.0
    assert dict_lot["openTaskCount"] == 2
    assert dict_lot["refNo"] == "PO-001"
    assert dict_lot["refCategory"] == 1
    assert EWarehouseRiskType.BELOW_SAFETY_STOCK in dict_lot["riskTypes"]
    assert "lastSourceNo" not in dict_lot
    assert "lastSourceCategory" not in dict_lot


def test_inventory_services_apply_direct_filters_before_enrichment():
    obj_session = build_session()
    n_now = seed_dashboard_base(obj_session)
    obj_session.add_all([
        CTableInventoryRec(
            warehouse_no="WH-A",
            warehouse_displayName="A倉",
            ref_no="GRN-002",
            refCategory=1,
            date=n_now - 2 * 86400,
            category=EInventoryCategory.IN,
            batchNumber="B-RM-002",
            item_no="RM-002",
            item_name="原料B",
            itemCategory=EItemCategory.PM,
            itemType=1,
            unit=1,
            count=30,
            amount=300,
        ),
        CTableBatchNumber(
            no="B-RM-002",
            ref_no="PO-002",
            refCategory=1,
            item_no="RM-002",
            item_name="原料B",
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
            name="原料B",
            unitWarehouse=1,
        ),
    ])
    obj_session.commit()

    dict_inventory = CWarehouseInventoryService().get_inventory(
        n_date=n_now,
        str_timezone="Asia/Taipei",
        str_warehouse_no="WH-A",
        n_item_category=EItemCategory.PM,
        str_item_no="RM-002",
        obj_session=obj_session,
    )
    assert dict_inventory["total"] == 1
    assert dict_inventory["results"][0]["itemNo"] == "RM-002"
    assert dict_inventory["results"][0]["batchNo"] == "B-RM-002"

    dict_lots = CWarehouseInventoryLotService().get_lots(
        n_date=n_now,
        str_timezone="Asia/Taipei",
        str_warehouse_no="WH-A",
        n_item_category=EItemCategory.PM,
        str_item_no="RM-002",
        obj_session=obj_session,
    )
    assert dict_lots["total"] == 1
    assert dict_lots["summary"]["lotCount"] == 1
    assert dict_lots["summary"]["totalInventoryValue"] == 300.0
    assert dict_lots["summary"]["pendingTaskCount"] == 0
    assert dict_lots["results"][0]["itemNo"] == "RM-002"
    assert dict_lots["results"][0]["refNo"] == "PO-002"


def test_inventory_lot_detail_returns_tracking_datasets():
    obj_session = build_session()
    n_now = seed_dashboard_base(obj_session)

    dict_payload = CWarehouseInventoryLotService().get_lot_detail(
        n_date=n_now,
        str_timezone="Asia/Taipei",
        str_warehouse_no="WH-A",
        str_item_no="RM-001",
        str_batch_no="B-RM-001",
        obj_session=obj_session,
    )

    assert dict_payload["lot"]["lotKey"] == "WH-A|RM-001|B-RM-001"
    assert dict_payload["lot"]["currentQuantity"] == 90.0
    assert len(dict_payload["inventoryRecords"]) == 2
    assert dict_payload["inventoryRecords"][0]["refNo"] == "GRN-001"
    assert dict_payload["inventoryRecords"][0]["category"] == EInventoryCategory.IN
    assert dict_payload["inventoryRecords"][0]["quantity"] == 100.0
    assert "direction" not in dict_payload["inventoryRecords"][0]
    assert "signedQuantity" not in dict_payload["inventoryRecords"][0]
    assert dict_payload["inventoryRecords"][1]["category"] == EInventoryCategory.OUT
    assert dict_payload["inventoryRecords"][1]["quantity"] == 10.0

    assert dict_payload["reservations"][0]["reservationNo"] == "RES-001"
    assert dict_payload["reservations"][0]["refCategory"] == 2
    assert dict_payload["reservations"][0]["refNo"] == "WO-001"
    assert dict_payload["qualityHolds"][0]["holdNo"] == "QH-001"
    assert dict_payload["qualityHolds"][0]["holdQuantity"] == 5.0
    assert len(dict_payload["palletMovements"]) == 2
    assert dict_payload["palletMovements"][0]["movementNo"] == "PAL-001"
    assert len(dict_payload["workflowTasks"]) == 2
    assert dict_payload["workflowTasks"][0]["taskId"] == "TASK-IN-001"


def test_zero_quantity_batches_are_filtered_from_inventory_and_risks():
    obj_session = build_session()
    n_now = seed_dashboard_base(obj_session)
    obj_session.add_all([
        CTableInventoryItemMonthStatistic(
            warehouse_no="WH-A",
            warehouse_displayName="Aå€‰",
            date=date(2023, 10, 31),
            timezone="Asia/Taipei",
            kind=EInventoryDeltaKind.BATCHNO,
            category=EItemCategory.PM,
            specified_no="B-ZERO",
            specified_name="B-ZERO",
            specified_ref_no="RM-ZERO",
            specified_ref_name="Zero Material",
            unit=1,
            startCount=0,
            startAmount=0,
            inCount=0,
            inAmount=0,
            endCount=0,
            endAmount=0,
            creationTime=n_now,
        ),
        CTableBatchNumber(
            date=n_now - 40 * 86400,
            no="B-ZERO",
            ref_no="PO-ZERO",
            refCategory=1,
            item_no="RM-ZERO",
            item_name="Zero Material",
            itemCategory=EItemCategory.PM,
            itemSubCategory=11,
            itemType=1,
            unit=1,
            validDays=90,
            validDate=n_now + 20 * 86400,
        ),
        CTableItemSafetyStock(
            no="SS-ZERO",
            itemCategory=EItemCategory.PM,
            item_no="RM-ZERO",
            item_name="Zero Material",
            warehouse_no="WH-A",
            unit=1,
            safetyStock=80,
            effectiveDate=n_now - 86400,
            status=1,
        ),
    ])
    obj_session.commit()

    dict_dashboard = CWarehouseDashboardService().get_dashboard(
        n_date=n_now,
        str_timezone="Asia/Taipei",
        str_warehouse_no="WH-A",
        n_item_category=EItemCategory.PM,
        b_include_inventory=True,
        obj_session=obj_session,
    )
    assert all(dict_row["batchNo"] != "B-ZERO" for dict_row in dict_dashboard["inventory"])
    assert all(dict_row["batchNo"] != "B-ZERO" for dict_row in dict_dashboard["riskAlerts"])

    dict_inventory = CWarehouseInventoryService().get_inventory(
        n_date=n_now,
        str_timezone="Asia/Taipei",
        str_warehouse_no="WH-A",
        n_item_category=EItemCategory.PM,
        obj_session=obj_session,
    )
    assert all(dict_row["batchNo"] != "B-ZERO" for dict_row in dict_inventory["results"])


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


def test_task_workbench_service_returns_confirmed_dataset():
    obj_session = build_session()
    n_now = seed_dashboard_base(obj_session)

    dict_payload = CWarehouseTaskWorkbenchService().get_task_workbench(
        n_date=n_now,
        str_timezone="Asia/Taipei",
        str_date_range="today",
        str_warehouse_no="WH-A",
        obj_session=obj_session,
    )

    assert dict_payload["total"] == 2
    assert dict_payload["summary"]["openTaskCount"] == 2
    assert dict_payload["summary"]["inboundTaskCount"] == 1
    assert dict_payload["summary"]["outboundTaskCount"] == 1
    assert dict_payload["lanes"][0]["laneCode"] == "inbound"
    assert dict_payload["results"][0]["refNo"] == "GRN-001"
    assert "sourceNo" not in dict_payload["results"][0]
    assert dict_payload["results"][1]["taskId"] == "TASK-OUT-001"
    assert dict_payload["results"][1]["availableQuantity"] == 65.0
    assert dict_payload["results"][1]["reservedQuantity"] == 20.0
    assert dict_payload["results"][1]["qualityHoldQuantity"] == 5.0
    assert dict_payload["results"][1]["nextActionCode"] == "warehouse.task.prepareOutbound"


def test_task_workbench_detail_returns_related_lots_and_timeline():
    obj_session = build_session()
    n_now = seed_dashboard_base(obj_session)

    dict_payload = CWarehouseTaskWorkbenchService().get_task_detail(
        n_date=n_now,
        str_timezone="Asia/Taipei",
        str_task_id="TASK-OUT-001",
        obj_session=obj_session,
    )

    assert dict_payload["task"]["taskId"] == "TASK-OUT-001"
    assert dict_payload["task"]["refNo"] == "WO-001"
    assert dict_payload["quantity"]["remainingQuantity"] == 15.0
    assert dict_payload["quantity"]["availableQuantity"] == 65.0
    assert len(dict_payload["relatedLots"]) == 1
    assert dict_payload["relatedLots"][0]["lotKey"] == "WH-A|RM-001|B-RM-001"
    assert dict_payload["sourceRefs"] == [{
        "refCategory": 2,
        "refNo": "WO-001",
        "refSubNo": "",
        "descriptionCode": "warehouse.source.inventory",
    }]
    assert len(dict_payload["timeline"]) == 2
    assert dict_payload["timeline"][0]["eventCode"] == "workflow.task.created"
    assert dict_payload["timeline"][1]["status"] == EWorkflowTaskStatus.PARTIAL


def test_task_workbench_detail_returns_empty_payload_when_task_missing():
    obj_session = build_session()
    seed_dashboard_base(obj_session)

    dict_payload = CWarehouseTaskWorkbenchService().get_task_detail(
        str_task_id="MISSING-TASK",
        obj_session=obj_session,
    )

    assert dict_payload == {
        "task": {},
        "quantity": {},
        "relatedLots": [],
        "sourceRefs": [],
        "timeline": [],
    }


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

    def fake_get_task_workbench(self, **dict_kwargs):
        return {
            "serverTimestamp": 1700000000,
            "timezone": "Asia/Taipei",
            "total": 1,
            "count": 1,
            "start": 0,
            "results": [{"taskId": "TASK-OUT-001"}],
        }

    def fake_get_task_detail(self, **dict_kwargs):
        return {
            "task": {"taskId": dict_kwargs.get("str_task_id")},
            "quantity": {},
            "relatedLots": [],
            "sourceRefs": [],
            "timeline": [],
        }

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

    def fake_get_lot_detail(self, **dict_kwargs):
        return {
            "lot": {"lotKey": "%s|%s|%s" % (
                dict_kwargs.get("str_warehouse_no"),
                dict_kwargs.get("str_item_no"),
                dict_kwargs.get("str_batch_no"),
            )},
            "inventoryRecords": [],
            "reservations": [],
            "qualityHolds": [],
            "palletMovements": [],
            "workflowTasks": [],
        }

    monkeypatch.setenv("TOKEN_ENABLED", "1")
    monkeypatch.setattr(CWarehouseInventoryService, "get_inventory", fake_get_inventory)
    monkeypatch.setattr(CWarehouseInventoryLotService, "get_lots", fake_get_lots)
    monkeypatch.setattr(CWarehouseInventoryLotService, "get_lot_detail", fake_get_lot_detail)
    monkeypatch.setattr(CWarehouseTaskService, "get_tasks", fake_get_tasks)
    monkeypatch.setattr(CWarehouseTaskWorkbenchService, "get_task_workbench", fake_get_task_workbench)
    monkeypatch.setattr(CWarehouseTaskWorkbenchService, "get_task_detail", fake_get_task_detail)

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
    obj_lots_response = obj_client.get(
        "/api/v2/warehouse/inventory/lots",
        headers={"x-auth-token": "test-token", "x-timezone": "Asia/Taipei"},
    )
    obj_lot_detail_response = obj_client.get(
        "/api/v2/warehouse/inventory/lots/wh/WH-A/item/RM-001/batch/B-RM-001",
        headers={"x-auth-token": "test-token", "x-timezone": "Asia/Taipei"},
    )
    obj_task_workbench_response = obj_client.get(
        "/api/v2/warehouse/task-workbench",
        headers={"x-auth-token": "test-token", "x-timezone": "Asia/Taipei"},
    )
    obj_task_detail_response = obj_client.get(
        "/api/v2/warehouse/task-workbench/tasks/TASK-OUT-001",
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

    assert obj_lots_response.status_code == 200
    dict_lots_data = json.loads(obj_lots_response.data.decode("utf8"))
    assert dict_lots_data["code"] == 0
    assert dict_lots_data["payload"]["results"][0]["lotKey"] == "WH-A|RM-001|B-RM-001"

    assert obj_lot_detail_response.status_code == 200
    dict_lot_detail_data = json.loads(obj_lot_detail_response.data.decode("utf8"))
    assert dict_lot_detail_data["code"] == 0
    assert dict_lot_detail_data["payload"]["lot"]["lotKey"] == "WH-A|RM-001|B-RM-001"

    assert obj_task_workbench_response.status_code == 200
    dict_task_workbench_data = json.loads(obj_task_workbench_response.data.decode("utf8"))
    assert dict_task_workbench_data["code"] == 0
    assert dict_task_workbench_data["payload"]["results"][0]["taskId"] == "TASK-OUT-001"

    assert obj_task_detail_response.status_code == 200
    dict_task_detail_data = json.loads(obj_task_detail_response.data.decode("utf8"))
    assert dict_task_detail_data["code"] == 0
    assert dict_task_detail_data["payload"]["task"]["taskId"] == "TASK-OUT-001"


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
