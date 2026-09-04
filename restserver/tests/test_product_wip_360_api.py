# coding=utf8
import os
import sys
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.common.common import EErrorCode, EItemCategory  # noqa: E402
from package.dbwrapper.table import CTableContract, CTableInproduct, CTableProduct, CTableTransItems  # noqa: E402
from package.restserver.api.v2.bom import CBomCenterService  # noqa: E402
from package.restserver.api.v2.items import CItemCenterService  # noqa: E402
from package.restserver.api.v2.product_wip_360 import (  # noqa: E402
    CProductWip360ModuleCode,
    CProductWip360OverviewService,
    CProductWip360StatusCode,
    CProductWip360WarningCode,
)
from package.restserver.api.v2.recipe_formula import CRecipeFormulaService  # noqa: E402
from package.restserver.api.v2.routing import CRoutingProcessFlowService  # noqa: E402
from package.restserver.api.v2.warehouse import CWarehouseInventoryService  # noqa: E402
from package.restserver.app import create_app  # noqa: E402


def build_session():
    obj_engine = create_engine("sqlite:///:memory:")
    for obj_table in [
        CTableProduct.__table__,
        CTableInproduct.__table__,
        CTableTransItems.__table__,
        CTableContract.__table__,
    ]:
        obj_table.create(bind=obj_engine)
    return sessionmaker(bind=obj_engine)()


def seed_product_wip_360(obj_session):
    obj_session.add_all([
        CTableProduct(no="FG-001", category=51, name="製成品A", unitShipping=111, unitWarehouse=2, unitProduct=2, version=3, comment="成品"),
        CTableInproduct(no="WIP-001", category=41, name="在製品A", unitShipping=0, unitWarehouse=2, unitProduct=2, comment="半成品"),
        CTableInproduct(no="WIP-ALONE", category=41, name="獨立在製品", unitShipping=0, unitWarehouse=2, unitProduct=2),
        CTableTransItems(no="TR-FG-001", name="客戶交易品A", category=5, company_no="CUS-001", company_displayName="客戶A", item_no="FG-001", item_name="製成品A"),
        CTableContract(no="CON-FG-001-OLD", item_no="TR-FG-001", date=1700000000, unit=2, price=11.11111, creationTime=1700000000),
        CTableContract(no="CON-FG-001", item_no="TR-FG-001", date=1800000000, unit=2, price=12.34567, creationTime=1800000000),
    ])
    obj_session.commit()


def patch_success_modules(monkeypatch):
    monkeypatch.setattr(CItemCenterService, "get_detail", lambda self, str_item_no, n_date=0, str_timezone="": {
        "item": {"itemNo": str_item_no, "masterStatusCode": "ready"},
        "inventorySummary": {"currentQuantity": 8.5},
    })
    monkeypatch.setattr(CWarehouseInventoryService, "get_inventory", lambda self, **kwargs: {
        "serverTimestamp": kwargs.get("n_date"),
        "total": 1,
        "count": 1,
        "results": [{
            "warehouseNo": "WH-A",
            "warehouseName": "主倉",
            "itemNo": kwargs.get("str_item_no"),
            "itemName": "製成品A",
            "itemCategory": kwargs.get("n_item_category"),
            "batchNo": "BN-FG-001",
            "currentQuantity": 8.5,
            "inventoryValue": 105,
            "unit": 2,
        }],
    })
    monkeypatch.setattr(CBomCenterService, "get_product_structure", lambda self, str_product_no, n_product_version=0, n_depth=3, n_effective_date=0: {
        "productStructure": {"productNo": str_product_no, "productVersion": n_product_version, "children": []},
        "warnings": [],
    })
    monkeypatch.setattr(CRecipeFormulaService, "get_by_product", lambda self, str_product_no, n_product_version=0, n_effective_date=0: {
        "recipeVersion": {"recipeNo": "BOM-FG-001", "recipeVersion": n_product_version},
        "warnings": [],
    })
    monkeypatch.setattr(CRoutingProcessFlowService, "get_current", lambda self, str_item_no, n_effective_date=0: {
        "routingVersion": {"routingVersionId": "RT-FG-001"},
        "sourceLineage": {"routingVersionSourceCode": "product_process"},
        "warnings": [],
    })


def build_payload(obj_session, str_item_no="FG-001", n_item_category=EItemCategory.PRODUCT):
    return CProductWip360OverviewService()._CProductWip360OverviewService__get_overview_with_session(
        obj_session,
        str_item_no,
        n_item_category,
        1800000000,
        1800000000,
        0,
        None,
        "Asia/Taipei",
    )


def readiness(dict_payload, str_module_code):
    return {
        dict_row["moduleCode"]: dict_row
        for dict_row in dict_payload["moduleReadiness"]
    }[str_module_code]


def test_product_complete_overview_uses_confirmed_module_contracts(monkeypatch):
    obj_session = build_session()
    seed_product_wip_360(obj_session)
    patch_success_modules(monkeypatch)

    dict_payload = build_payload(obj_session)

    assert dict_payload["subject"]["itemNo"] == "FG-001"
    assert dict_payload["productVersion"] == 3
    assert dict_payload["capabilityBoundary"]["readOnly"] is True
    assert dict_payload["capabilityBoundary"]["productWriteSupported"] is False
    assert readiness(dict_payload, CProductWip360ModuleCode.ITEM)["statusCode"] == CProductWip360StatusCode.COMPLETE
    assert readiness(dict_payload, CProductWip360ModuleCode.WAREHOUSE)["statusCode"] == CProductWip360StatusCode.COMPLETE
    assert dict_payload["inventoryOverview"]["currentQuantity"] == 8.5
    assert dict_payload["inventoryOverview"]["inventoryValue"] == 105
    assert dict_payload["transactionContext"]["transactionItems"][0]["contractNo"] == "CON-FG-001"
    assert dict_payload["transactionContext"]["transactionItems"][0]["tradePrice"] == 12.3457


def test_wip_partial_overview_keeps_bom_and_recipe_boundaries(monkeypatch):
    obj_session = build_session()
    seed_product_wip_360(obj_session)
    patch_success_modules(monkeypatch)

    dict_payload = build_payload(obj_session, "WIP-001", EItemCategory.INPRODUCT)

    assert dict_payload["subject"]["itemCategory"] == EItemCategory.INPRODUCT
    assert readiness(dict_payload, CProductWip360ModuleCode.BOM)["statusCode"] == CProductWip360StatusCode.PARTIAL
    assert readiness(dict_payload, CProductWip360ModuleCode.RECIPE)["statusCode"] == CProductWip360StatusCode.PARTIAL
    assert CProductWip360WarningCode.WIP_STRUCTURE_NOT_GOVERNED in [
        dict_warning["warningCode"] for dict_warning in dict_payload["warnings"]
    ]


def test_standalone_wip_partial_returns_missing_module_signals(monkeypatch):
    obj_session = build_session()
    seed_product_wip_360(obj_session)
    patch_success_modules(monkeypatch)
    monkeypatch.setattr(CWarehouseInventoryService, "get_inventory", lambda self, **kwargs: {"results": []})

    dict_payload = build_payload(obj_session, "WIP-ALONE", EItemCategory.INPRODUCT)

    assert readiness(dict_payload, CProductWip360ModuleCode.TRANSACTION_ITEM)["statusCode"] == CProductWip360StatusCode.UNAVAILABLE
    assert readiness(dict_payload, CProductWip360ModuleCode.WAREHOUSE)["statusCode"] == CProductWip360StatusCode.PARTIAL
    assert CProductWip360WarningCode.MISSING_TRANSACTION_ITEM in [
        dict_warning["warningCode"] for dict_warning in dict_payload["warnings"]
    ]
    assert CProductWip360WarningCode.MISSING_WAREHOUSE_STOCK in [
        dict_warning["warningCode"] for dict_warning in dict_payload["warnings"]
    ]


def test_not_found_returns_none(monkeypatch):
    obj_session = build_session()
    seed_product_wip_360(obj_session)
    patch_success_modules(monkeypatch)

    assert build_payload(obj_session, "FG-NOT-FOUND", EItemCategory.PRODUCT) is None


def test_invalid_category_returns_controlled_response(monkeypatch):
    os.environ["TOKEN_ENABLED"] = "1"
    obj_app = create_app()

    with obj_app.test_client() as obj_client:
        obj_response = obj_client.get(
            "/api/v2/product-wip-360/overview?itemNo=FG-001&itemCategory=1",
            headers={"x-auth-token": "token", "x-timezone": "Asia/Taipei"},
        )

    assert obj_response.status_code == 400
    assert obj_response.get_json()["code"] == EErrorCode.ERROR_INVAILD_PARAM


def test_module_unavailable_is_reported(monkeypatch):
    obj_session = build_session()
    seed_product_wip_360(obj_session)
    patch_success_modules(monkeypatch)

    def raise_item_error(self, str_item_no, n_date=0, str_timezone=""):
        raise RuntimeError("item module offline")

    monkeypatch.setattr(CItemCenterService, "get_detail", raise_item_error)

    dict_payload = build_payload(obj_session)

    assert readiness(dict_payload, CProductWip360ModuleCode.ITEM)["statusCode"] == CProductWip360StatusCode.ERROR
    assert CProductWip360WarningCode.MODULE_UNAVAILABLE in [
        dict_warning["warningCode"] for dict_warning in dict_payload["warnings"]
    ]


def test_routing_test_support_status_and_source_lineage_are_preserved(monkeypatch):
    obj_session = build_session()
    seed_product_wip_360(obj_session)
    patch_success_modules(monkeypatch)
    monkeypatch.setattr(CRoutingProcessFlowService, "get_current", lambda self, str_item_no, n_effective_date=0: {
        "routingVersion": {"routingVersionId": "RT-TEST"},
        "sourceLineage": {"routingVersionSourceCode": "test_support"},
        "warnings": [{"warningCode": CProductWip360WarningCode.TEST_SUPPORT_ONLY, "refNo": "RT-TEST"}],
    })

    dict_payload = build_payload(obj_session)

    assert readiness(dict_payload, CProductWip360ModuleCode.ROUTING)["statusCode"] == CProductWip360StatusCode.TEST_SUPPORT
    assert dict_payload["sourceLineage"]["routing"]["sourceCode"] == "test_support"
    assert CProductWip360WarningCode.TEST_SUPPORT_ONLY in [
        dict_warning["warningCode"] for dict_warning in dict_payload["warnings"]
    ]


def test_warning_propagation_from_child_modules(monkeypatch):
    obj_session = build_session()
    seed_product_wip_360(obj_session)
    patch_success_modules(monkeypatch)
    monkeypatch.setattr(CBomCenterService, "get_product_structure", lambda self, str_product_no, n_product_version=0, n_depth=3, n_effective_date=0: {
        "productStructure": {"productNo": str_product_no},
        "warnings": [{"warningCode": "missing_bom_child", "refNo": str_product_no}],
    })

    dict_payload = build_payload(obj_session)

    assert readiness(dict_payload, CProductWip360ModuleCode.BOM)["statusCode"] == CProductWip360StatusCode.PARTIAL
    assert "missing_bom_child" in [
        dict_warning["warningCode"] for dict_warning in dict_payload["warnings"]
    ]


def test_read_only_negative_control_rejects_post():
    obj_app = create_app()

    with obj_app.test_client() as obj_client:
        obj_response = obj_client.post(
            "/api/v2/product-wip-360/overview",
            json={},
            headers={"x-auth-token": "token", "x-timezone": "Asia/Taipei"},
        )

    assert obj_response.status_code == 405
