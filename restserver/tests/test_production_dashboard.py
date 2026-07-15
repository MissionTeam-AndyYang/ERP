# coding=utf8
import json
import sys
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.common.common import EDepartment
from package.dbwrapper.table import (
    Base,
    CTableAPSQuantityItem,
    CTableEmployee,
    CTableInventoryRec,
    CTableLaborWage,
    CTableProcessLabor,
    CTableProductionData,
    CTableProductionDataInput,
    CTableProductionDataLabor,
    CTableProductionDataMachine,
    CTableProductionDataOutput,
    CTableProductionDataReuse,
    CTableProductLine,
    CTableProductOrder,
    CTableProductionLineDailyCapacity,
    CTableProductionLineDowntime,
    CTableWorkOrder,
)
from package.restserver.api.v2.production import CProductionDashboardService


def build_session():
    obj_engine = create_engine("sqlite:///:memory:")
    lst_tables = [
        CTableAPSQuantityItem,
        CTableEmployee,
        CTableInventoryRec,
        CTableLaborWage,
        CTableProcessLabor,
        CTableProductionData,
        CTableProductionDataInput,
        CTableProductionDataLabor,
        CTableProductionDataMachine,
        CTableProductionDataOutput,
        CTableProductionDataReuse,
        CTableProductLine,
        CTableProductOrder,
        CTableProductionLineDailyCapacity,
        CTableProductionLineDowntime,
        CTableWorkOrder,
    ]
    for obj_table in lst_tables:
        obj_table.__table__.create(bind=obj_engine)
    return sessionmaker(bind=obj_engine)()


def seed_production(obj_session):
    n_now = 1700000000
    n_day = n_now - (n_now % 86400)
    obj_session.add_all([
        CTableProductLine(no="LINE-01", name="烘焙線", oneProcess=1, secProcess=3),
        CTableProductionLineDailyCapacity(
            no="CAP-OLD", effectiveDate=n_day - 86400 * 3,
            production_line_no="LINE-01", availableMinutes=600, status=1,
        ),
        CTableProductionLineDailyCapacity(
            no="CAP-NEW", effectiveDate=n_day - 86400,
            production_line_no="LINE-01", availableMinutes=480, status=1,
        ),
        CTableProductionLineDowntime(
            no="DOWN-01", production_line_no="LINE-01",
            startTime=n_day + 60 * 60, endTime=n_day + 2 * 60 * 60,
            durationMinutes=60, reasonType=1, status=2,
        ),
        CTableProductOrder(no="SO-01", item_no="PRODUCT-01", item_name="餅乾"),
        CTableEmployee(no="EMP-01", name="王技師", type=1, level=1),
        CTableLaborWage(date=n_day - 86400, type=1, level=1, hourly=200),
        CTableWorkOrder(
            no="WO-01", date=n_now, product_order_no="SO-01", aps_no="APS-01",
            product_no="PRODUCT-01", product_name="餅乾", output_item_no="PRODUCT-01",
            output_item_name="餅乾", production_line_no="LINE-01", oneProcess=1,
            secProcess=3, startTime=n_now, endTime=n_now + 3600,
            processUnit=101, processTime=240, processCount=100,
            laborCount=1, creator_no="EMP-01",
        ),
        CTableAPSQuantityItem(
            product_order_no="SO-01", output_item_no="PRODUCT-01",
            oneProcess=1, secProcess=3, item_no="MATERIAL-01",
            item_name="麵粉", itemCategory=1, unit=2, count=100,
        ),
        CTableProcessLabor(
            work_order_no="WO-01", employee_no="EMP-01",
            production_line_no="LINE-01",
        ),
        CTableProductionData(
            work_order_no="WO-01", product_order_no="SO-01", date=n_now,
            production_line_no="LINE-01", product_no="PRODUCT-01",
            product_name="餅乾", materialLoss=3,
        ),
        CTableProductionDataInput(
            work_order_no="WO-01", process_order_no="PO-INPUT",
            time=n_now + 60, action=1, item_no="MATERIAL-01",
            item_name="麵粉", category=1, unit=2, count=100,
        ),
        CTableProductionDataOutput(
            work_order_no="WO-01", process_order_no="PO-OUTPUT",
            time=n_now + 1800, action=1, item_no="PRODUCT-01",
            item_name="餅乾", category=2, batch_number="BATCH-01",
            unit=101, count=100, valid_date=n_now + 86400 * 30,
        ),
        CTableProductionDataLabor(
            work_order_no="WO-01", employee_no="EMP-01", employee_name="王技師",
            employee_type=1, employee_level=1, action=1, startTime=n_now,
            endTime=n_now + 1800, hours=2,
        ),
        CTableProductionDataMachine(
            work_order_no="WO-01", time=n_now + 120,
            equipment_no="MACHINE-01", equipment_name="烤箱", action=1,
            speed=10, temperature=180,
        ),
        CTableInventoryRec(
            ref_no="WO-01", category=1, source=5, batchNumber="BATCH-01",
            item_no="PRODUCT-01", itemCategory=5, count=100,
        ),
    ])
    obj_session.commit()
    return n_now


def test_production_dashboard_calculates_capacity_and_metrics():
    obj_session = build_session()
    n_now = seed_production(obj_session)
    dict_payload = CProductionDashboardService()._CProductionDashboardService__get_dashboard_with_session(
        obj_session, n_now, "UTC", "7d", "", 0, 0, "", "", "", "", "", 0, 50,
    )

    assert dict_payload["summary"]["scheduledWorkOrderCount"] == 1
    assert dict_payload["todayWorkOrders"][0]["status"] == "completed"
    assert dict_payload["todayWorkOrders"][0]["completedQuantity"] == 100.0
    assert dict_payload["scheduleByLine"][0]["baseCapacityMinutes"] == 480
    assert dict_payload["scheduleByLine"][0]["downtimeMinutes"] == 60
    assert dict_payload["scheduleByLine"][0]["dailyCapacityMinutes"] == 420
    assert dict_payload["productionMetrics"][0]["actualInputQuantity"] == 100.0
    assert dict_payload["productionMetrics"][0]["materialLossQuantity"] == 3.0
    assert dict_payload["productionMetrics"][0]["laborCost"] == 400
    assert dict_payload["productionMetrics"][0]["unitLaborCost"] == 4.0
    assert any(dict_row["alertType"] == "capacity_downtime" for dict_row in dict_payload["alerts"])


def test_production_dashboard_returns_unknown_material_when_requirement_is_not_issued():
    obj_session = build_session()
    n_now = seed_production(obj_session)
    obj_session.query(CTableProductionDataInput).delete()
    obj_session.commit()
    dict_payload = CProductionDashboardService()._CProductionDashboardService__get_dashboard_with_session(
        obj_session, n_now, "UTC", "7d", "", 0, 0, "", "", "", "", "", 0, 50,
    )
    assert dict_payload["todayWorkOrders"][0]["materialStatus"] == "unknown"
    assert any(dict_row["alertType"] == "material_shortage" for dict_row in dict_payload["alerts"])


def test_production_dashboard_route_uses_standard_envelope(monkeypatch):
    from flask import Flask
    from package.restserver.api.v2.production_uri import production_v2

    monkeypatch.setenv("TOKEN_ENABLED", "1")
    monkeypatch.setattr(
        CProductionDashboardService,
        "get_dashboard",
        lambda self, **dict_kwargs: {"total": 0, "start": 0, "count": 0, "todayWorkOrders": []},
    )
    obj_app = Flask(__name__)
    obj_app.register_blueprint(production_v2)
    dict_response = obj_app.test_client().get(
        "/api/v2/production/dashboard",
        headers={"x-auth-token": "test-token", "x-timezone": "Asia/Taipei"},
    )
    assert dict_response.status_code == 200
    dict_body = json.loads(dict_response.data.decode("utf8"))
    assert dict_body["code"] == 0
    assert dict_body["payload"]["count"] == 0


def test_production_work_order_detail_route_uses_confirmed_path(monkeypatch):
    from flask import Flask
    from package.restserver.api.v2.production_uri import production_v2

    monkeypatch.setenv("TOKEN_ENABLED", "1")
    monkeypatch.setattr(
        CProductionDashboardService,
        "get_work_order_detail",
        lambda self, str_work_order_no, n_date, str_timezone: {
            "workOrder": {"workOrderNo": str_work_order_no},
            "materials": [], "mesEvents": [], "outputs": [],
            "reuseAndWaste": [], "labor": [], "machines": [], "relatedDocuments": [],
        },
    )
    obj_app = Flask(__name__)
    obj_app.register_blueprint(production_v2)
    dict_response = obj_app.test_client().get(
        "/api/v2/production/work-orders/WO-01/detail",
        headers={"x-auth-token": "test-token", "x-timezone": "UTC"},
    )
    assert dict_response.status_code == 200
    dict_body = json.loads(dict_response.data.decode("utf8"))
    assert dict_body["code"] == 0
    assert dict_body["payload"]["workOrder"]["workOrderNo"] == "WO-01"
