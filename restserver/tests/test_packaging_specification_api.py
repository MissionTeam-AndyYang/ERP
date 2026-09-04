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
from package.dbwrapper.table import (  # noqa: E402
    CTableBOM2,
    CTableBOM2Number,
    CTableInproduct,
    CTableProduct,
    CTableProductBOMSpec,
    CTableProductSpec,
)
from package.restserver.api.v2.packaging_specification import (  # noqa: E402
    CPackagingSpecificationService,
    CPackagingSpecificationStatusCode,
    CPackagingSpecificationWarningCode,
)
from package.restserver.app import create_app  # noqa: E402


def build_session():
    obj_engine = create_engine("sqlite:///:memory:")
    for obj_table in [
        CTableProduct.__table__,
        CTableInproduct.__table__,
        CTableProductSpec.__table__,
        CTableProductBOMSpec.__table__,
        CTableBOM2Number.__table__,
        CTableBOM2.__table__,
    ]:
        obj_table.create(bind=obj_engine)
    return sessionmaker(bind=obj_engine)()


def seed_packaging(obj_session):
    obj_session.add_all([
        CTableProduct(no="FG-001", category=51, name="製成品A", unitShipping=101, unitWarehouse=101, unitProduct=101, version=2),
        CTableProduct(no="FG-PARTIAL", category=51, name="缺明細製成品", unitShipping=101, unitWarehouse=101, unitProduct=101, version=1),
        CTableInproduct(no="WIP-001", category=41, name="在製品A", unitShipping=101, unitWarehouse=101, unitProduct=101),
        CTableProductSpec(product_no="FG-001", product_version=2, bom_no="BOM-RM-001", bom_version=1, level=1, item_type=1, item_no="WIP-001", count=1, unit=101, weight=5),
        CTableProductBOMSpec(product_no="FG-001", product_version=2, level=1, bom2_no="PKG-FG-001", count=12, unit=101, weight=3.5),
        CTableProductBOMSpec(product_no="FG-PARTIAL", product_version=1, level=1, bom2_no="PKG-MISSING-LINE", count=6, unit=101, weight=1.5),
        CTableBOM2Number(no="PKG-FG-001", displayName="箱規A", unit=101, weight=3.5, bom_no="FG-001", bom_version=2),
        CTableBOM2Number(no="PKG-MISSING-LINE", displayName="缺明細箱規", unit=101, weight=1.5, bom_no="FG-PARTIAL", bom_version=1),
        CTableBOM2(parent_no="PKG-FG-001", parent_name="箱規A", child_category=2, child_id="MAT-PKG-001", child_name="紙箱", childUnit=101, count=1, childUnit2=101, weight=0.3, length=0, expectedLoss=0.02, actualLoss=0.01, processCount=1),
        CTableBOM2(parent_no="PKG-FG-001", parent_name="箱規A", child_category=2, child_id="MAT-PKG-002", child_name="標籤", childUnit=101, count=2, childUnit2=101, weight=0.1, length=0, expectedLoss=0, actualLoss=0, processCount=2),
    ])
    obj_session.commit()


def build_payload(obj_session, str_item_no, n_item_category, n_product_version=0):
    return CPackagingSpecificationService()._CPackagingSpecificationService__get_overview_with_session(
        obj_session,
        str_item_no,
        n_item_category,
        n_product_version,
        1700000000,
        "Asia/Taipei",
    )


def test_product_packaging_complete():
    obj_session = build_session()
    seed_packaging(obj_session)

    dict_payload = build_payload(obj_session, "FG-001", EItemCategory.PRODUCT)

    assert dict_payload["subject"]["itemNo"] == "FG-001"
    assert dict_payload["summary"]["packagingSpecCount"] == 1
    assert dict_payload["summary"]["materialLineCount"] == 2
    assert dict_payload["moduleReadiness"][0]["statusCode"] == CPackagingSpecificationStatusCode.COMPLETE
    assert dict_payload["packagingSpecs"][0]["packagingBomNo"] == "PKG-FG-001"
    assert dict_payload["packagingSpecs"][0]["lineCount"] == 2
    assert dict_payload["capabilityBoundary"]["readOnly"] is True
    assert dict_payload["capabilityBoundary"]["packagingWriteSupported"] is False


def test_product_packaging_partial_when_lines_missing():
    obj_session = build_session()
    seed_packaging(obj_session)

    dict_payload = build_payload(obj_session, "FG-PARTIAL", EItemCategory.PRODUCT)

    assert dict_payload["summary"]["packagingSpecCount"] == 1
    assert dict_payload["packagingSpecs"][0]["lineSourceCode"] == "not_recorded"
    assert dict_payload["moduleReadiness"][0]["statusCode"] == CPackagingSpecificationStatusCode.PARTIAL
    assert CPackagingSpecificationWarningCode.MISSING_PACKAGING_BOM_LINES in [
        dict_warning["warningCode"] for dict_warning in dict_payload["warnings"]
    ]


def test_wip_packaging_visibility_is_partial_from_downstream_product():
    obj_session = build_session()
    seed_packaging(obj_session)

    dict_payload = build_payload(obj_session, "WIP-001", EItemCategory.INPRODUCT)

    assert dict_payload["subject"]["itemCategory"] == EItemCategory.INPRODUCT
    assert dict_payload["summary"]["packagingSpecCount"] == 1
    assert dict_payload["packagingSpecs"][0]["wipNo"] == "WIP-001"
    assert dict_payload["moduleReadiness"][0]["statusCode"] == CPackagingSpecificationStatusCode.PARTIAL
    assert CPackagingSpecificationWarningCode.WIP_PACKAGING_CONTEXT_FROM_DOWNSTREAM_PRODUCT in [
        dict_warning["warningCode"] for dict_warning in dict_payload["warnings"]
    ]


def test_not_found_returns_none():
    obj_session = build_session()
    seed_packaging(obj_session)

    assert build_payload(obj_session, "FG-NOT-FOUND", EItemCategory.PRODUCT) is None


def test_invalid_category_returns_controlled_response():
    os.environ["TOKEN_ENABLED"] = "1"
    obj_app = create_app()

    with obj_app.test_client() as obj_client:
        obj_response = obj_client.get(
            "/api/v2/packaging-specification/overview?itemNo=FG-001&itemCategory=1",
            headers={"x-auth-token": "token", "x-timezone": "Asia/Taipei"},
        )

    assert obj_response.status_code == 400
    assert obj_response.get_json()["code"] == EErrorCode.ERROR_INVAILD_PARAM


def test_module_unavailable_isolated(monkeypatch):
    obj_session = build_session()
    seed_packaging(obj_session)

    def raise_module_error(self, obj_session, str_item_no, n_item_category, n_product_version):
        raise RuntimeError("packaging module unavailable")

    monkeypatch.setattr(CPackagingSpecificationService, "_CPackagingSpecificationService__query_packaging_specs", raise_module_error)

    dict_payload = build_payload(obj_session, "FG-001", EItemCategory.PRODUCT)

    assert dict_payload["moduleReadiness"][0]["statusCode"] == CPackagingSpecificationStatusCode.ERROR
    assert dict_payload["warnings"][0]["warningCode"] == CPackagingSpecificationWarningCode.MODULE_UNAVAILABLE


def test_read_only_negative_control_rejects_post():
    obj_app = create_app()

    with obj_app.test_client() as obj_client:
        obj_response = obj_client.post(
            "/api/v2/packaging-specification/overview",
            json={},
            headers={"x-auth-token": "token", "x-timezone": "Asia/Taipei"},
        )

    assert obj_response.status_code == 405
