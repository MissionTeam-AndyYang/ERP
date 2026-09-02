# coding=utf8
import json
import sys
from pathlib import Path


RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.common.common import (
    EInventoryCategory,
    EInventoryReadPermissionCode,
    EItemCategory,
)
from package.dbwrapper.table import CTableInventoryRec
from package.restserver.api.v2.inventory import CInventoryReadService
from test_warehouse_dashboard import build_session, seed_dashboard_base


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
