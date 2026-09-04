# coding=utf8
import sys
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.common.common import (  # noqa: E402
    EBomVersionState,
    EItemCategory,
    ERoutingSourceCode,
    ERoutingStatusCode,
    ERoutingWarningCode,
)
from package.dbwrapper.table import (  # noqa: E402
    CTableInproduct,
    CTableProcess,
    CTableProcessCapacity,
    CTableProcessFlow,
    CTableProduct,
    CTableProductBOMSpec,
    CTableProductProcess,
    CTableProductSpec,
)
from package.restserver.api.v2.routing import CRoutingProcessFlowService  # noqa: E402
from package.restserver.app import create_app  # noqa: E402


def build_session():
    obj_engine = create_engine("sqlite:///:memory:")
    for obj_table in [
        CTableProduct.__table__,
        CTableInproduct.__table__,
        CTableProductProcess.__table__,
        CTableProcessFlow.__table__,
        CTableProcess.__table__,
        CTableProcessCapacity.__table__,
        CTableProductSpec.__table__,
        CTableProductBOMSpec.__table__,
    ]:
        obj_table.create(bind=obj_engine)
    return sessionmaker(bind=obj_engine)()


def seed_routing(obj_session):
    obj_session.add_all([
        CTableProduct(no="FG-001", category=2, name="測試製成品", unitProduct=111, version=2),
        CTableInproduct(no="WIP-001", category=1, name="測試在製品", unitProduct=2),
        CTableProductProcess(no="RT-FG-001-V1", item_no="FG-001", version=1, date=1700000000),
        CTableProductProcess(no="RT-FG-001-V2", item_no="FG-001", version=2, date=1800000000),
        CTableProductProcess(no="RT-WIP-001-V1", item_no="WIP-001", version=1, date=1700000000),
        CTableProcessFlow(no="STEP-2", product_process_no="RT-FG-001-V1", order=2, oneProcess=2, secProcess=1),
        CTableProcessFlow(no="STEP-1", product_process_no="RT-FG-001-V1", order=1, oneProcess=1, secProcess=1),
        CTableProcessFlow(no="STEP-WIP-1", product_process_no="RT-WIP-001-V1", order=1, oneProcess=1, secProcess=2),
        CTableProcess(no="PROC-PREP-MIX", oneProcess=1, secProcess=1, comment="routing.process.preparation_mix"),
        CTableProcess(no="PROC-PROC-COAT", oneProcess=2, secProcess=1, comment="routing.process.processing_coat"),
        CTableProcessCapacity(date=1700000000, oneProcess=1, secProcess=1, unit=111, hourlyOutput=120.125, laborCount=3),
        CTableProductSpec(
            product_no="FG-001",
            product_version=1,
            bom_no="BOM-FG-001",
            bom_version=1,
            level=1,
            item_type=1,
            item_no="WIP-001",
            count=1,
            unit=2,
            weight=10.0,
        ),
        CTableProductBOMSpec(
            product_no="FG-001",
            product_version=1,
            level=1,
            bom2_no="PKG-FG-001",
            count=12,
            unit=111,
            weight=3.5,
        ),
    ])
    obj_session.commit()


def test_routing_dashboard_returns_product_and_wip_versions():
    obj_session = build_session()
    seed_routing(obj_session)

    dict_payload = CRoutingProcessFlowService()._CRoutingProcessFlowService__get_dashboard_with_session(
        obj_session, "", "", 1700000000, 0, 50,
    )

    assert dict_payload["summary"]["itemCount"] == 2
    assert dict_payload["summary"]["routingVersionCount"] == 3
    assert {dict_row["itemCategory"] for dict_row in dict_payload["routingVersions"]} == {
        EItemCategory.PRODUCT,
        EItemCategory.INPRODUCT,
    }
    assert dict_payload["capabilityBoundary"]["routingWriteSupported"] is False


def test_routing_versions_resolve_effective_and_future_versions():
    obj_session = build_session()
    seed_routing(obj_session)

    dict_payload = CRoutingProcessFlowService()._CRoutingProcessFlowService__get_versions_with_session(
        obj_session, "FG-001", 1700000000,
    )

    dict_state_by_version = {
        dict_row["routingVersion"]: dict_row["versionStateCode"]
        for dict_row in dict_payload["versions"]
    }
    assert dict_state_by_version[1] == EBomVersionState.EFFECTIVE
    assert dict_state_by_version[2] == EBomVersionState.FUTURE


def test_routing_steps_are_ordered_and_include_references():
    obj_session = build_session()
    seed_routing(obj_session)

    dict_payload = CRoutingProcessFlowService()._CRoutingProcessFlowService__get_steps_with_session(
        obj_session, "RT-FG-001-V1", 1700000000,
    )

    assert [dict_row["stepId"] for dict_row in dict_payload["steps"]] == ["STEP-1", "STEP-2"]
    assert dict_payload["routingVersion"]["routingStatusCode"] == ERoutingStatusCode.PARTIAL
    assert dict_payload["steps"][0]["processNo"] == "PROC-PREP-MIX"
    assert dict_payload["steps"][0]["processLabel"] == "routing.process.preparation_mix"
    assert dict_payload["steps"][0]["recipeReference"]["established"] is True
    assert dict_payload["steps"][0]["recipeReference"]["recipeNo"] == "BOM-FG-001"
    assert dict_payload["steps"][0]["packagingContext"]["established"] is True
    assert dict_payload["steps"][0]["standardPerformance"]["governed"] is True
    assert dict_payload["steps"][0]["standardPerformance"]["hourlyOutput"] == 120.13
    assert dict_payload["steps"][1]["standardPerformance"]["governed"] is False
    assert ERoutingWarningCode.RESOURCE_ELIGIBILITY_NOT_GOVERNED in [
        dict_row["warningCode"] for dict_row in dict_payload["warnings"]
    ]
    assert dict_payload["sourceLineage"]["routingVersionSourceCode"] == ERoutingSourceCode.PRODUCT_PROCESS


def test_routing_current_selects_effective_version():
    obj_session = build_session()
    seed_routing(obj_session)

    dict_payload = CRoutingProcessFlowService()._CRoutingProcessFlowService__get_current_with_session(
        obj_session, "FG-001", 1700000000,
    )

    assert dict_payload["routingVersion"]["routingVersionId"] == "RT-FG-001-V1"
    assert dict_payload["routingVersion"]["versionStateCode"] == EBomVersionState.EFFECTIVE


def test_routing_missing_steps_returns_controlled_warning():
    obj_session = build_session()
    obj_session.add(CTableProduct(no="FG-MISS", category=1, name="缺工序製成品", unitProduct=111, version=1))
    obj_session.add(CTableProductProcess(no="RT-MISS", item_no="FG-MISS", version=1, date=1700000000))
    obj_session.commit()

    dict_payload = CRoutingProcessFlowService()._CRoutingProcessFlowService__get_steps_with_session(
        obj_session, "RT-MISS", 1700000000,
    )

    assert dict_payload["routingVersion"]["routingStatusCode"] == ERoutingStatusCode.MISSING
    assert dict_payload["steps"] == []
    assert ERoutingWarningCode.MISSING_STEPS in [
        dict_row["warningCode"] for dict_row in dict_payload["warnings"]
    ]


def test_routing_routes_reject_post_mutation(monkeypatch):
    monkeypatch.setenv("TOKEN_ENABLED", "1")
    obj_app = create_app()
    obj_client = obj_app.test_client()

    obj_response = obj_client.post(
        "/api/v2/routing/dashboard",
        headers={"x-timezone": "Asia/Taipei", "x-auth-token": "ERP2_NON_PRODUCTION_READ_VALIDATION"},
    )

    assert obj_response.status_code == 405


def test_routing_falls_back_to_test_support_surface_when_formal_tables_are_missing():
    obj_engine = create_engine("sqlite:///:memory:")
    obj_session = sessionmaker(bind=obj_engine)()
    obj_session.execute(text("""
        CREATE VIEW v_test_support_routing_process_flow_readonly AS
        SELECT
            'TS-ROUTE-SD-001' AS test_support_route_id,
            'PRD-SD-001' AS product_no,
            'Shared DEV Product Fixture A' AS product_name,
            1 AS product_version,
            'BOM-SD-001' AS bom_no,
            'Shared DEV BOM Fixture A' AS bom_display_name,
            1 AS bom_version,
            'Shared DEV synthetic routing / process flow fixture' AS process_flow_label,
            'TS-STEP-SD-001' AS test_support_step_id,
            10 AS step_sequence,
            'Synthetic material preparation visibility step' AS step_label,
            'MAT-SD-001' AS input_ref,
            'INP-SD-001' AS output_ref,
            'NON-PRODUCTION ACCEPTANCE TEST SUPPORT' AS nonproduction_classification,
            'Read-only acceptance-test support; not Routing write or Process Master source' AS evidence_boundary,
            'Derived from existing Shared DEV product_spec, bom, and bom_item fixture identities' AS source_lineage_ref,
            'Warn: synthetic process flow test support only' AS warning_behavior,
            'Read-only Backend / Frontend acceptance retest support' AS acceptance_use
        UNION ALL
        SELECT
            'TS-ROUTE-SD-001',
            'PRD-SD-001',
            'Shared DEV Product Fixture A',
            1,
            'BOM-SD-001',
            'Shared DEV BOM Fixture A',
            1,
            'Shared DEV synthetic routing / process flow fixture',
            'TS-STEP-SD-002',
            20,
            'Synthetic product composition visibility step',
            'INP-SD-001',
            'PRD-SD-001',
            'NON-PRODUCTION ACCEPTANCE TEST SUPPORT',
            'Read-only acceptance-test support; not Routing write or Process Master source',
            'Derived from existing Shared DEV product_spec, bom, and bom_item fixture identities',
            'Warn: synthetic process flow test support only',
            'Read-only Backend / Frontend acceptance retest support'
    """))
    obj_session.execute(text("""
        CREATE VIEW v_test_support_routing_source_lineage_warnings AS
        SELECT
            'TS-ROUTE-SD-001' AS test_support_route_id,
            'NON-PRODUCTION ACCEPTANCE TEST SUPPORT' AS nonproduction_classification,
            'Derived from existing Shared DEV product_spec, bom, and bom_item fixture identities' AS source_lineage_ref,
            'Show warning when no governed production routing source exists; do not imply target schema' AS warning_behavior,
            'NOT_TARGET_SCHEMA_NOT_PRODUCTION_NOT_SOURCE_OF_TRUTH' AS boundary_label
    """))
    obj_session.commit()

    obj_service = CRoutingProcessFlowService()
    dict_dashboard = obj_service._CRoutingProcessFlowService__get_dashboard_with_session(
        obj_session, "", "", 1700000000, 0, 50,
    )
    dict_steps = obj_service._CRoutingProcessFlowService__get_steps_with_session(
        obj_session, "TS-ROUTE-SD-001", 1700000000,
    )

    assert dict_dashboard["summary"]["routingVersionCount"] == 1
    assert dict_dashboard["routingVersions"][0]["routingVersionId"] == "TS-ROUTE-SD-001"
    assert dict_dashboard["routingVersions"][0]["stepCount"] == 2
    assert dict_dashboard["routingVersions"][0]["warningCodes"] == [ERoutingWarningCode.TEST_SUPPORT_ONLY]
    assert [dict_row["stepId"] for dict_row in dict_steps["steps"]] == ["TS-STEP-SD-001", "TS-STEP-SD-002"]
    assert dict_steps["sourceLineage"]["routingVersionSourceCode"] == ERoutingSourceCode.TEST_SUPPORT
    assert ERoutingWarningCode.TEST_SUPPORT_ONLY in [dict_row["warningCode"] for dict_row in dict_steps["warnings"]]
