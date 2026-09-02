# coding=utf8
import json
import sys
from pathlib import Path

from sqlalchemy import create_engine, text


RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.common.common import (
    EInventoryCategory,
    EInventoryReadPermissionCode,
    EItemCategory,
)
from package.dbwrapper.table import CTableInventoryRec
from package.restserver.api.v2.inventory import CInventoryReadService, CInventoryStagingReadService
from test_warehouse_dashboard import build_session, seed_dashboard_base


def build_staging_engine():
    obj_engine = create_engine("sqlite:///:memory:")
    lst_sql = [
        """
        CREATE TABLE np_xwalk_uom (
          xwalk_uom_id TEXT PRIMARY KEY,
          source_uom TEXT,
          candidate_canonical_uom_code TEXT,
          display_uom TEXT,
          conversion_allowed INTEGER
        )
        """,
        """
        CREATE TABLE np_xwalk_item_identity (
          xwalk_item_identity_id TEXT PRIMARY KEY,
          source_item_code TEXT,
          candidate_canonical_item_code TEXT,
          source_item_name TEXT
        )
        """,
        """
        CREATE TABLE np_xwalk_lot_identity (
          xwalk_lot_identity_id TEXT PRIMARY KEY,
          source_lot_code TEXT,
          candidate_lot_code TEXT,
          item_xwalk_id TEXT,
          lot_identity_status TEXT,
          source_provenance_ref TEXT
        )
        """,
        """
        CREATE TABLE np_stg_inventory_balance_snapshot (
          stg_balance_snapshot_id TEXT PRIMARY KEY,
          package_id TEXT,
          source_record_id TEXT,
          source_system TEXT,
          warehouse_code TEXT,
          location_code TEXT,
          item_xwalk_id TEXT,
          lot_xwalk_id TEXT,
          uom_xwalk_id TEXT,
          source_quantity REAL,
          source_uom TEXT,
          display_quantity REAL,
          display_uom TEXT,
          candidate_canonical_uom_code TEXT,
          canonical_quantity REAL,
          snapshot_business_date TEXT,
          source_event_timestamp TEXT,
          validation_state TEXT,
          source_provenance_ref TEXT
        )
        """,
        """
        CREATE TABLE np_stg_inventory_movement (
          stg_inventory_movement_id TEXT PRIMARY KEY,
          package_id TEXT,
          source_movement_id TEXT,
          source_system TEXT,
          movement_type TEXT,
          source_document_ref TEXT,
          warehouse_code TEXT,
          from_location_code TEXT,
          to_location_code TEXT,
          item_xwalk_id TEXT,
          lot_xwalk_id TEXT,
          uom_xwalk_id TEXT,
          source_quantity REAL,
          source_uom TEXT,
          display_quantity REAL,
          display_uom TEXT,
          candidate_canonical_uom_code TEXT,
          canonical_quantity REAL,
          movement_business_date TEXT,
          source_event_timestamp TEXT,
          technical_loaded_at TEXT,
          validation_state TEXT,
          source_provenance_ref TEXT
        )
        """,
        """
        CREATE TABLE np_stg_lot_snapshot (
          stg_lot_snapshot_id TEXT PRIMARY KEY,
          package_id TEXT,
          source_lot_snapshot_id TEXT,
          source_system TEXT,
          lot_xwalk_id TEXT,
          item_xwalk_id TEXT,
          uom_xwalk_id TEXT,
          warehouse_code TEXT,
          location_code TEXT,
          source_lot_status TEXT,
          source_quantity REAL,
          source_uom TEXT,
          display_quantity REAL,
          display_uom TEXT,
          candidate_canonical_uom_code TEXT,
          canonical_quantity REAL,
          snapshot_business_date TEXT,
          source_event_timestamp TEXT,
          validation_state TEXT,
          source_provenance_ref TEXT
        )
        """,
        """
        CREATE TABLE np_val_slice_validation_result (
          val_result_id TEXT PRIMARY KEY,
          validation_scope TEXT,
          target_table_name TEXT,
          target_record_key TEXT,
          validation_state TEXT,
          severity TEXT,
          validation_message TEXT
        )
        """,
    ]
    with obj_engine.begin() as obj_connection:
        for str_sql in lst_sql:
            obj_connection.execute(text(str_sql))
        obj_connection.execute(text("INSERT INTO np_xwalk_uom VALUES ('UOM-1', '公斤', 'KG', '公斤', 0)"))
        obj_connection.execute(text("INSERT INTO np_xwalk_item_identity VALUES ('ITEM-1', 'WHINV-FG-001', 'WHINV-FG-001', '測試製成品')"))
        obj_connection.execute(text("INSERT INTO np_xwalk_item_identity VALUES ('ITEM-2', 'WHINV-MAT-001', 'WHINV-MAT-001', '測試原料')"))
        obj_connection.execute(text("INSERT INTO np_xwalk_lot_identity VALUES ('LOT-1', 'WHINV-FG-LOT-001', 'WHINV-FG-LOT-001', 'ITEM-1', 'MAPPED', 'SYNTHETIC_NON_PRODUCTION::LOT-1')"))
        obj_connection.execute(text("INSERT INTO np_xwalk_lot_identity VALUES ('LOT-2', 'WHINV-MAT-LOT-001', 'WHINV-MAT-LOT-001', 'ITEM-2', 'MAPPED', 'SYNTHETIC_NON_PRODUCTION::LOT-2')"))
        obj_connection.execute(text(
            """
            INSERT INTO np_stg_inventory_balance_snapshot VALUES
            ('BAL-1', 'PKG-1', 'SRC-BAL-1', 'SYNTHETIC_WH_INV_INT_TEST', 'WH-SYN-01', 'LOC-A', 'ITEM-1', 'LOT-1', 'UOM-1', 125.5, '公斤', 125.5, '公斤', 'KG', NULL, '2026-09-02', NULL, 'READY_FOR_READ_ONLY_API', 'SYNTHETIC_NON_PRODUCTION::BAL-1'),
            ('BAL-ZERO', 'PKG-1', 'SRC-BAL-0', 'SYNTHETIC_WH_INV_INT_TEST', 'WH-SYN-01', 'LOC-Z', 'ITEM-2', 'LOT-2', 'UOM-1', 0, '公斤', 0, '公斤', 'KG', NULL, '2026-09-02', NULL, 'READY_FOR_READ_ONLY_API', 'SYNTHETIC_NON_PRODUCTION::BAL-0')
            """
        ))
        obj_connection.execute(text(
            """
            INSERT INTO np_stg_inventory_movement VALUES
            ('MOV-1', 'PKG-1', 'SRC-MOV-1', 'SYNTHETIC_WH_INV_INT_TEST', 'RECEIPT', 'SYN-DOC-001', 'WH-SYN-01', NULL, 'LOC-A', 'ITEM-1', 'LOT-1', 'UOM-1', 125.5, '公斤', 125.5, '公斤', 'KG', NULL, '2026-09-02', '2026-09-02 09:00:00', '2026-09-02 09:01:00', 'READY_FOR_READ_ONLY_API', 'SYNTHETIC_NON_PRODUCTION::MOV-1'),
            ('MOV-2', 'PKG-1', 'SRC-MOV-2', 'SYNTHETIC_WH_INV_INT_TEST', 'ISSUE', 'SYN-DOC-002', 'WH-SYN-01', 'LOC-A', 'LOC-B', 'ITEM-1', 'LOT-1', 'UOM-1', 5, '公斤', 5, '公斤', 'KG', NULL, '2026-09-03', '2026-09-03 09:00:00', '2026-09-03 09:01:00', 'READY_FOR_READ_ONLY_API', 'SYNTHETIC_NON_PRODUCTION::MOV-2')
            """
        ))
        obj_connection.execute(text(
            """
            INSERT INTO np_stg_lot_snapshot VALUES
            ('LOT-SNAP-1', 'PKG-1', 'SRC-LOT-1', 'SYNTHETIC_WH_INV_INT_TEST', 'LOT-1', 'ITEM-1', 'UOM-1', 'WH-SYN-01', 'LOC-A', 'AVAILABLE_DISPLAY_ONLY', 125.5, '公斤', 125.5, '公斤', 'KG', NULL, '2026-09-02', NULL, 'READY_FOR_READ_ONLY_API', 'SYNTHETIC_NON_PRODUCTION::LOT-SNAP-1'),
            ('LOT-SNAP-ZERO', 'PKG-1', 'SRC-LOT-0', 'SYNTHETIC_WH_INV_INT_TEST', 'LOT-2', 'ITEM-2', 'UOM-1', 'WH-SYN-01', 'LOC-B', 'AVAILABLE_DISPLAY_ONLY', 0, '公斤', 0, '公斤', 'KG', NULL, '2026-09-02', NULL, 'READY_FOR_READ_ONLY_API', 'SYNTHETIC_NON_PRODUCTION::LOT-SNAP-0')
            """
        ))
        obj_connection.execute(text("INSERT INTO np_val_slice_validation_result VALUES ('VAL-1', 'ROW_COUNT', 'np_stg_inventory_balance_snapshot', 'BAL-1', 'PASS_VERIFIED', 'INFO', 'ok')"))
    return obj_engine


def test_inventory_staging_balances_read_np_tables_and_filter_zero_quantity():
    obj_engine = build_staging_engine()
    with obj_engine.connect() as obj_connection:
        dict_payload = CInventoryStagingReadService()._get_balances_with_connection(
            obj_connection=obj_connection,
            n_date=1798848000,
            str_timezone="Asia/Taipei",
            str_warehouse_no="WH-SYN-01",
        )

    assert dict_payload["permissionCode"] == EInventoryReadPermissionCode.WH_INV_READ
    assert dict_payload["total"] == 1
    assert dict_payload["count"] == 1
    dict_balance = dict_payload["balances"][0]
    assert dict_balance["balanceId"] == "BAL-1"
    assert dict_balance["itemNo"] == "WHINV-FG-001"
    assert dict_balance["lotCode"] == "WHINV-FG-LOT-001"
    assert dict_balance["currentQuantity"] == 125.5
    assert dict_balance["availableQuantity"] == 125.5
    assert dict_balance["unit"] == "公斤"
    assert dict_balance["candidateCanonicalUomCode"] == "KG"
    assert dict_balance["sourceProvenanceRef"] == "SYNTHETIC_NON_PRODUCTION::BAL-1"


def test_inventory_staging_movements_support_date_range_and_paging():
    obj_engine = build_staging_engine()
    with obj_engine.connect() as obj_connection:
        dict_payload = CInventoryStagingReadService()._get_movements_with_connection(
            obj_connection=obj_connection,
            str_timezone="UTC",
            str_start_date="2026-09-02",
            str_end_date="2026-09-02",
            str_warehouse_no="WH-SYN-01",
            n_start=0,
            n_count=10,
        )

    assert dict_payload["permissionCode"] == EInventoryReadPermissionCode.WH_INV_READ
    assert dict_payload["range"]["period"] == "custom"
    assert dict_payload["total"] == 1
    dict_movement = dict_payload["movements"][0]
    assert dict_movement["movementId"] == "MOV-1"
    assert dict_movement["category"] == "RECEIPT"
    assert dict_movement["source"] == "NP_STAGING"
    assert dict_movement["quantity"] == 125.5
    assert dict_movement["unit"] == "公斤"
    assert dict_movement["refNo"] == "SYN-DOC-001"


def test_inventory_staging_lots_read_np_tables_and_filter_zero_quantity():
    obj_engine = build_staging_engine()
    with obj_engine.connect() as obj_connection:
        dict_payload = CInventoryStagingReadService()._get_lots_with_connection(
            obj_connection=obj_connection,
            n_date=1798848000,
            str_timezone="Asia/Taipei",
            str_keyword="製成品",
        )

    assert dict_payload["permissionCode"] == EInventoryReadPermissionCode.WH_INV_READ
    assert dict_payload["total"] == 1
    dict_lot = dict_payload["lots"][0]
    assert dict_lot["lotKey"] == "LOT-SNAP-1"
    assert dict_lot["lotCode"] == "WHINV-FG-LOT-001"
    assert dict_lot["currentQuantity"] == 125.5
    assert dict_lot["availableQuantity"] == 125.5
    assert dict_lot["unit"] == "公斤"
    assert dict_lot["candidateCanonicalUomCode"] == "KG"


def test_inventory_staging_lot_trace_is_bounded_to_np_lot_relationships():
    obj_engine = build_staging_engine()
    with obj_engine.connect() as obj_connection:
        dict_payload = CInventoryStagingReadService()._get_lot_trace_with_connection(
            obj_connection=obj_connection,
            str_lot_code="WHINV-FG-LOT-001",
            str_timezone="Asia/Taipei",
        )

    assert dict_payload["permissionCode"] == EInventoryReadPermissionCode.WH_INV_READ
    assert dict_payload["batch"]["batchNo"] == "WHINV-FG-LOT-001"
    assert dict_payload["batch"]["itemNo"] == "WHINV-FG-001"
    assert dict_payload["batch"]["unit"] == "公斤"
    assert [dict_row["stepId"] for dict_row in dict_payload["traceSteps"]] == ["MOV-1", "MOV-2"]
    assert all(dict_row["sourceProvenanceRef"].startswith("SYNTHETIC_NON_PRODUCTION") for dict_row in dict_payload["traceSteps"])


def test_inventory_read_service_staging_mode_bypasses_formal_db_manager(monkeypatch):
    from package.restserver.api.v2 import inventory as inventory_module

    dict_seen = {}

    class CFailingDBMgr(object):
        def __enter__(self):
            raise AssertionError("formal DB manager should not be opened in staging mode")

    def fake_get_balances(self, **dict_kwargs):
        dict_seen.update(dict_kwargs)
        return {"permissionCode": EInventoryReadPermissionCode.WH_INV_READ, "balances": [], "total": 0, "start": 0, "count": 0}

    monkeypatch.setenv("ERP2_WH_INV_STAGING_MODE", "1")
    monkeypatch.setattr(inventory_module, "CDBMgr", CFailingDBMgr)
    monkeypatch.setattr(inventory_module.CInventoryStagingReadService, "get_balances", fake_get_balances)

    dict_payload = CInventoryReadService().get_balances(str_timezone="Asia/Taipei")

    assert dict_payload["permissionCode"] == EInventoryReadPermissionCode.WH_INV_READ
    assert dict_seen["str_timezone"] == "Asia/Taipei"


def test_inventory_read_balances_preserve_uom_option_b_and_permission():
    obj_session = build_session()
    n_now = seed_dashboard_base(obj_session)

    dict_payload = CInventoryReadService()._get_balances_with_session(
        obj_session=obj_session,
        n_date=n_now,
        str_timezone="Asia/Taipei",
        str_warehouse_no="WH-A",
        n_item_category=EItemCategory.PM,
    )

    assert dict_payload["permissionCode"] == EInventoryReadPermissionCode.WH_INV_READ
    assert dict_payload["total"] == 1
    dict_balance = dict_payload["balances"][0]
    assert dict_balance["balanceId"] == "WH-A|RM-001|B-RM-001|"
    assert dict_balance["lotCode"] == "B-RM-001"
    assert dict_balance["currentQuantity"] == 90.0
    assert dict_balance["availableQuantity"] == 65.0
    assert dict_balance["unit"] == 1
    assert "unitName" not in dict_balance


def test_inventory_read_movements_filters_and_pages_from_inventory_records():
    obj_session = build_session()
    n_now = seed_dashboard_base(obj_session)

    dict_payload = CInventoryReadService()._get_movements_with_session(
        obj_session=obj_session,
        n_date=n_now,
        str_timezone="Asia/Taipei",
        str_warehouse_no="WH-A",
        n_item_category=EItemCategory.PM,
        str_item_no="RM-001",
        str_lot_code="B-RM-001",
        n_start=0,
        n_count=1,
    )

    assert dict_payload["permissionCode"] == EInventoryReadPermissionCode.WH_INV_READ
    assert dict_payload["total"] == 2
    assert dict_payload["count"] == 1
    dict_movement = dict_payload["movements"][0]
    assert dict_movement["lotCode"] == "B-RM-001"
    assert dict_movement["category"] in [EInventoryCategory.IN, EInventoryCategory.OUT]
    assert dict_movement["unit"] == 1
    assert "unitName" not in dict_movement


def test_inventory_read_movements_support_local_date_range():
    obj_session = build_session()
    n_now = seed_dashboard_base(obj_session)
    obj_session.add(
        CTableInventoryRec(
            warehouse_no="WH-A",
            warehouse_displayName="倉A",
            ref_no="OLD",
            refCategory=1,
            date=n_now - 400 * 86400,
            category=EInventoryCategory.IN,
            batchNumber="B-OLD",
            item_no="RM-001",
            item_name="原料A",
            itemCategory=EItemCategory.PM,
            unit=1,
            count=1,
            amount=10,
        )
    )
    obj_session.commit()

    dict_payload = CInventoryReadService()._get_movements_with_session(
        obj_session=obj_session,
        str_timezone="UTC",
        str_start_date="2023-10-01",
        str_end_date="2023-11-14",
        str_warehouse_no="WH-A",
    )

    assert dict_payload["range"]["period"] == "custom"
    assert dict_payload["total"] == 2
    assert all(dict_row["lotCode"] == "B-RM-001" for dict_row in dict_payload["movements"])


def test_inventory_read_lots_preserve_stock_and_uom_dataset():
    obj_session = build_session()
    n_now = seed_dashboard_base(obj_session)

    dict_payload = CInventoryReadService()._get_lots_with_session(
        obj_session=obj_session,
        n_date=n_now,
        str_timezone="Asia/Taipei",
        str_warehouse_no="WH-A",
        n_item_category=EItemCategory.PM,
    )

    assert dict_payload["permissionCode"] == EInventoryReadPermissionCode.WH_INV_READ
    assert dict_payload["total"] == 1
    dict_lot = dict_payload["lots"][0]
    assert dict_lot["lotKey"] == "WH-A|RM-001|B-RM-001"
    assert dict_lot["lotCode"] == "B-RM-001"
    assert dict_lot["currentQuantity"] == 90.0
    assert dict_lot["unit"] == 1
    assert "unitName" not in dict_lot


def test_inventory_read_routes_are_get_only_and_preserve_error_contract(monkeypatch):
    from package.restserver.app import create_app
    from package.restserver.api.v2 import inventory as inventory_module

    monkeypatch.setenv("TOKEN_ENABLED", "1")
    monkeypatch.setattr(
        inventory_module.CInventoryReadService,
        "get_balances",
        lambda self, **dict_kwargs: {
            "permissionCode": EInventoryReadPermissionCode.WH_INV_READ,
            "balances": [],
            "total": 0,
            "start": 0,
            "count": 0,
        },
    )
    obj_app = create_app()
    obj_client = obj_app.test_client()

    obj_get_response = obj_client.get(
        "/api/v2/inventory/balances",
        headers={"x-auth-token": "test-token", "x-timezone": "Asia/Taipei"},
    )
    assert obj_get_response.status_code == 200
    dict_response = json.loads(obj_get_response.data.decode("utf-8"))
    assert sorted(dict_response.keys()) == ["code", "message", "payload"]
    assert dict_response["payload"]["permissionCode"] == EInventoryReadPermissionCode.WH_INV_READ

    obj_post_response = obj_client.post(
        "/api/v2/inventory/balances",
        headers={"x-auth-token": "test-token", "x-timezone": "Asia/Taipei"},
    )
    assert obj_post_response.status_code == 405


def test_inventory_read_lot_trace_uses_trace_service(monkeypatch):
    from package.restserver.api.v2.inventory import CInventoryLotTrace
    from package.restserver.api.v2 import inventory as inventory_module

    dict_seen = {}

    def fake_get_batch_overview(self, str_batch_no, str_timezone=""):
        dict_seen["lot"] = str_batch_no
        dict_seen["timezone"] = str_timezone
        return {
            "serverTimestamp": 1700000000,
            "batch": {"batchNo": str_batch_no, "unit": 1},
            "traceSteps": [],
        }

    monkeypatch.setattr(
        inventory_module.CTraceabilityService,
        "get_batch_overview",
        fake_get_batch_overview,
    )

    n_status_code, n_code, str_message, dict_payload = CInventoryLotTrace().get(
        str_timezone="Asia/Taipei",
        str_id="B-RM-001",
    )

    assert n_status_code == 200
    assert n_code == 0
    assert str_message == "success"
    assert dict_seen == {"lot": "B-RM-001", "timezone": "Asia/Taipei"}
    assert dict_payload["permissionCode"] == EInventoryReadPermissionCode.WH_INV_READ
