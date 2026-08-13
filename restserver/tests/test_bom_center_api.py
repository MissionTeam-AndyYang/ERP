# coding=utf8
import sys
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.common.common import EBomVersionState
from package.dbwrapper.table import CTableBOM, CTableBOMItem, CTableInproduct, CTableProduct, CTableProductSpec
from package.restserver.api.v2.bom import CBomCenterService


def build_session():
    obj_engine = create_engine("sqlite:///:memory:")
    for obj_table in [
        CTableBOM.__table__,
        CTableBOMItem.__table__,
        CTableInproduct.__table__,
        CTableProduct.__table__,
        CTableProductSpec.__table__,
    ]:
        obj_table.create(bind=obj_engine)
    return sessionmaker(bind=obj_engine)()


def seed_bom_center(obj_session):
    n_now = 1700000000
    obj_session.add_all([
        CTableBOM(
            no="BOM-001", displayName="餅乾原料配方",
            version=1, date=n_now - 86400 * 10, unit=2,
            weight=1.234, comment="歷史版本",
        ),
        CTableBOM(
            no="BOM-001", displayName="餅乾原料配方",
            version=2, date=n_now - 86400, unit=2,
            weight=1.567, comment="目前版本",
        ),
        CTableBOM(
            no="BOM-001", displayName="餅乾原料配方",
            version=3, date=n_now + 86400 * 5, unit=2,
            weight=1.789, comment="未來版本",
        ),
        CTableBOM(
            no="BOM-002", displayName="蛋糕原料配方",
            version=1, date=0, unit=2,
            weight=2.0, comment="日期未定",
        ),
        CTableBOMItem(
            bom_no="BOM-001", item_no="MAT-001",
            item_name="麵粉", unit=2, weight=0.65,
        ),
        CTableBOMItem(
            bom_no="BOM-001", item_no="MAT-002",
            item_name="砂糖", unit=2, weight=0.18,
        ),
        CTableBOMItem(
            bom_no="BOM-002", item_no="MAT-003",
            item_name="蛋粉", unit=2, weight=0.25,
        ),
        CTableProduct(
            no="PRD-001", category=2, name="餅乾禮盒",
            unitShipping=111, unitWarehouse=111, unitProduct=111,
            version=2,
        ),
        CTableInproduct(
            no="INP-001", category=1, name="餅乾內包",
            unitShipping=101, unitWarehouse=101, unitProduct=101,
        ),
        CTableProductSpec(
            product_no="PRD-001", product_version=2,
            bom_no="BOM-001", bom_version=2, level=1,
            item_type=1, item_no="INP-001", count=12,
            unit=101, weight=0.5,
        ),
        CTableProductSpec(
            product_no="PRD-001_1", product_version=2,
            bom_no="BOM-001", bom_version=2, level=2,
            item_type=2, item_no="PRD-001", count=1,
            unit=111, weight=6.0,
        ),
        CTableProductSpec(
            product_no="PRD-001_1", product_version=2,
            bom_no="BOM-001", bom_version=2, level=2,
            item_type=1, item_no="INP-001", count=3,
            unit=101, weight=1.5,
        ),
    ])
    obj_session.commit()
    return n_now


def test_bom_center_dashboard_returns_version_rows_and_state_counts():
    obj_session = build_session()
    n_now = seed_bom_center(obj_session)
    dict_payload = CBomCenterService()._CBomCenterService__get_dashboard_with_session(
        obj_session, n_now, "", "", "", 0, 50,
    )

    assert dict_payload["summary"] == {
        "bomCount": 2,
        "versionCount": 4,
        "effectiveVersionCount": 1,
        "futureVersionCount": 1,
        "historicalVersionCount": 1,
    }
    assert dict_payload["total"] == 4
    dict_rows = {
        (dict_row["bomNo"], dict_row["version"]): dict_row
        for dict_row in dict_payload["items"]
    }
    assert dict_rows[("BOM-001", 2)]["versionStateCode"] == EBomVersionState.EFFECTIVE
    assert dict_rows[("BOM-001", 3)]["versionStateCode"] == EBomVersionState.FUTURE
    assert dict_rows[("BOM-001", 1)]["versionStateCode"] == EBomVersionState.HISTORICAL
    assert dict_rows[("BOM-001", 2)]["itemCount"] == 2
    assert dict_rows[("BOM-001", 2)]["linkedProductCount"] == 1


def test_bom_center_dashboard_filters_keyword_and_state():
    obj_session = build_session()
    n_now = seed_bom_center(obj_session)
    dict_payload = CBomCenterService()._CBomCenterService__get_dashboard_with_session(
        obj_session, n_now, "砂糖", "", EBomVersionState.EFFECTIVE, 0, 50,
    )

    assert dict_payload["summary"]["bomCount"] == 1
    assert dict_payload["summary"]["versionCount"] == 1
    assert dict_payload["items"][0]["bomNo"] == "BOM-001"
    assert dict_payload["items"][0]["version"] == 2


def test_bom_center_detail_defaults_to_effective_version_and_loads_relations():
    obj_session = build_session()
    n_now = seed_bom_center(obj_session)
    dict_payload = CBomCenterService()._CBomCenterService__get_detail_with_session(
        obj_session, "BOM-001", 0, n_now,
    )

    assert dict_payload["bom"]["version"] == 2
    assert dict_payload["bom"]["versionStateCode"] == EBomVersionState.EFFECTIVE
    assert [dict_row["itemNo"] for dict_row in dict_payload["items"]] == ["MAT-001", "MAT-002"]
    assert [dict_row["productNo"] for dict_row in dict_payload["linkedProducts"]] == ["PRD-001"]
    dict_linked_product = dict_payload["linkedProducts"][0]
    assert dict_linked_product["productName"] == "餅乾禮盒"
    assert dict_linked_product["productCategory"] == 2
    assert "level" not in dict_linked_product
    assert [dict_row["itemName"] for dict_row in dict_linked_product["contents"]] == ["餅乾內包", "餅乾禮盒"]
    assert [dict_row["version"] for dict_row in dict_payload["versions"]] == [3, 2, 1]


def test_bom_center_detail_supports_specific_version_and_not_found():
    obj_session = build_session()
    n_now = seed_bom_center(obj_session)
    dict_payload = CBomCenterService()._CBomCenterService__get_detail_with_session(
        obj_session, "BOM-001", 3, n_now,
    )

    assert dict_payload["bom"]["version"] == 3
    assert dict_payload["bom"]["versionStateCode"] == EBomVersionState.FUTURE
    assert CBomCenterService()._CBomCenterService__get_detail_with_session(
        obj_session, "BOM-404", 0, n_now,
    ) is None
