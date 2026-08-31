# coding=utf8
import sys
import time
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.common.common import (  # noqa: E402
    EInventoryCategory,
    EItemCategory,
    EItemMaintenanceRiskCode,
    EItemMaintenanceSuggestionTypeCode,
    EItemMasterStatusCode,
)
from package.dbwrapper.table import (  # noqa: E402
    CTableBOM,
    CTableBOMItem,
    CTableBatchNumber,
    CTableGoods,
    CTableInproduct,
    CTableInproductBOMSpec,
    CTableInventoryDelta,
    CTableInventoryItemMonthStatistic,
    CTableInventoryMonthStatistic,
    CTableInventoryRec,
    CTableItemSafetyStock,
    CTableMaterial,
    CTableProduct,
    CTableProductBOMSpec,
    CTableProductSpec,
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
from package.restserver.api.v2.items import CItemCenterService  # noqa: E402


def build_session():
    obj_engine = create_engine("sqlite:///:memory:")
    for obj_table in [
        CTableInventoryRec.__table__,
        CTableInventoryDelta.__table__,
        CTableInventoryItemMonthStatistic.__table__,
        CTableInventoryMonthStatistic.__table__,
        CTableBatchNumber.__table__,
        CTableMaterial.__table__,
        CTableInproduct.__table__,
        CTableProduct.__table__,
        CTableGoods.__table__,
        CTableBOM.__table__,
        CTableBOMItem.__table__,
        CTableInproductBOMSpec.__table__,
        CTableProductSpec.__table__,
        CTableProductBOMSpec.__table__,
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


def seed_item_center(obj_session):
    n_now = int(time.time())
    obj_session.add_all([
        CTableShipWarehouseAlias(no="WH-A", name="倉A", category=2),
        CTableMaterial(
            no="RM-001",
            category=EItemCategory.PM,
            subCategory=11,
            name="原料A",
            unitWarehouse=1,
            unitProduct=1,
            creationTime=n_now - 1000,
        ),
        CTableMaterial(
            no="RM-NOSTOCK",
            category=EItemCategory.PM,
            subCategory=11,
            name="無庫存訊號原料",
            unitWarehouse=1,
            unitProduct=1,
            creationTime=n_now - 900,
        ),
        CTableInproduct(
            no="WIP-001",
            category=41,
            name="半成品A",
            unitWarehouse=1,
            unitProduct=1,
            creationTime=n_now - 800,
        ),
        CTableProduct(
            no="FG-001",
            category=51,
            name="製成品A",
            unitWarehouse=1,
            unitProduct=1,
            version=1,
            creationTime=n_now - 700,
        ),
        CTableProduct(
            no="FG-MISSING-BOM",
            category=51,
            name="缺BOM製成品",
            unitWarehouse=1,
            unitProduct=1,
            version=1,
            creationTime=n_now - 600,
        ),
        CTableGoods(
            no="GOODS-001",
            category=1,
            subCategory=61,
            name="貨品A",
            unitWarehouse=0,
            unitProduct=1,
            creationTime=n_now - 500,
        ),
        CTableBatchNumber(
            date=n_now - 500,
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
            validDate=n_now + 100000,
            validDays=90,
            creationTime=n_now - 500,
        ),
        CTableInventoryRec(
            date=n_now - 400,
            category=EInventoryCategory.IN,
            item_no="RM-001",
            item_name="原料A",
            itemCategory=EItemCategory.PM,
            itemType=1,
            batchNumber="B-RM-001",
            warehouse_no="WH-A",
            warehouse_displayName="倉A",
            unit=1,
            count=80,
            creationTime=n_now - 400,
        ),
        CTableBOM(no="BOM-001", displayName="BOM A", date=n_now - 300, unit=1, weight=100, version=1, creationTime=n_now - 300),
        CTableBOMItem(bom_no="BOM-001", item_no="RM-001", item_name="原料A", unit=1, weight=20, creationTime=n_now - 300),
        CTableProductSpec(product_no="FG-001", product_version=1, bom_no="BOM-001", bom_version=1, level=1, item_type=1, item_no="WIP-001", count=1, unit=1, weight=50),
        CTableInproductBOMSpec(inproduct_no="WIP-001", category=1, item_no="RM-001", item_version=1, bom12_no="BOM-001", count=1, unit=1, weight=20),
    ])
    obj_session.commit()
    return n_now


def test_items_dashboard_returns_confirmed_fields():
    obj_session = build_session()
    n_now = seed_item_center(obj_session)

    dict_payload = CItemCenterService()._CItemCenterService__get_dashboard_with_session(
        obj_session, n_now, "Asia/Taipei", "", 0, 0, 0, "", False, False, 0, 50,
    )

    assert dict_payload["summary"]["totalItemCount"] == 6
    assert dict_payload["summary"]["activeItemCount"] == 6
    assert dict_payload["summary"]["finishedGoodsCount"] == 2
    assert dict_payload["summary"]["maintenanceItemCount"] == 3
    dict_items = {dict_row["itemNo"]: dict_row for dict_row in dict_payload["items"]}
    assert dict_items["RM-001"]["hasStock"] is True
    assert dict_items["RM-001"]["currentQuantity"] == 80.0
    assert dict_items["RM-001"]["batchCount"] == 1
    assert dict_items["RM-001"]["bomCount"] == 2
    assert dict_items["FG-001"]["masterStatusCode"] == EItemMasterStatusCode.READY
    assert dict_items["FG-MISSING-BOM"]["maintenanceRiskCode"] == EItemMaintenanceRiskCode.MISSING_BOM
    assert dict_items["RM-NOSTOCK"]["maintenanceRiskCode"] == EItemMaintenanceRiskCode.MISSING_STOCK_SIGNAL
    assert dict_items["GOODS-001"]["maintenanceRiskCode"] == EItemMaintenanceRiskCode.MISSING_UNIT


def test_items_dashboard_filters_and_paginates_items():
    obj_session = build_session()
    n_now = seed_item_center(obj_session)

    dict_payload = CItemCenterService()._CItemCenterService__get_dashboard_with_session(
        obj_session, n_now, "Asia/Taipei", "", EItemCategory.PM, 0, 0, EItemMasterStatusCode.MAINTENANCE_NEEDED, False, False, 0, 10,
    )

    assert dict_payload["total"] == 1
    assert dict_payload["items"][0]["itemNo"] == "RM-NOSTOCK"


def test_items_dashboard_has_stock_filter():
    obj_session = build_session()
    n_now = seed_item_center(obj_session)

    dict_payload = CItemCenterService()._CItemCenterService__get_dashboard_with_session(
        obj_session, n_now, "Asia/Taipei", "", 0, 0, 0, "", True, False, 0, 10,
    )

    assert dict_payload["total"] == 1
    assert dict_payload["items"][0]["itemNo"] == "RM-001"


def test_items_detail_returns_inventory_bom_batches_and_suggestions():
    obj_session = build_session()
    n_now = seed_item_center(obj_session)

    dict_payload = CItemCenterService()._CItemCenterService__get_detail_with_session(
        obj_session, "RM-001", n_now, "Asia/Taipei",
    )

    assert dict_payload["item"]["itemNo"] == "RM-001"
    assert dict_payload["item"]["masterStatusCode"] == EItemMasterStatusCode.READY
    assert dict_payload["inventorySummary"]["currentQuantity"] == 80.0
    assert dict_payload["inventorySummary"]["batchCount"] == 1
    assert dict_payload["bomUsage"][0]["bomNo"] == "BOM-001"
    assert dict_payload["bomUsage"][0]["quantity"] == 20.0
    assert dict_payload["recentBatches"][0]["batchNo"] == "B-RM-001"
    assert dict_payload["maintenanceSuggestions"] == []


def test_items_detail_returns_maintenance_suggestion_for_missing_bom():
    obj_session = build_session()
    n_now = seed_item_center(obj_session)

    dict_payload = CItemCenterService()._CItemCenterService__get_detail_with_session(
        obj_session, "FG-MISSING-BOM", n_now, "Asia/Taipei",
    )

    assert dict_payload["item"]["maintenanceRiskCode"] == EItemMaintenanceRiskCode.MISSING_BOM
    assert dict_payload["maintenanceSuggestions"][0]["suggestionTypeCode"] == EItemMaintenanceSuggestionTypeCode.MISSING_BOM


def test_items_detail_not_found_returns_none():
    obj_session = build_session()
    seed_item_center(obj_session)

    dict_payload = CItemCenterService()._CItemCenterService__get_detail_with_session(
        obj_session, "NOT-FOUND", 0, "Asia/Taipei",
    )

    assert dict_payload is None
