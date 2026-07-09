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

from package.common.common import EPaymentType, EUnit
from package.dbwrapper.table import (
    CTableGoodsReceiptNote,
    CTableOrderPayment,
    CTablePayment,
    CTableProductOrder,
    CTableProductionData,
    CTablePurchaseOrder,
    CTablePurchaseRequest,
    CTableShippingOrder,
    CTableWorkOrder,
)
from package.restserver.api.v2.orders import COrdersDashboardService


def build_session():
    obj_engine = create_engine("sqlite:///:memory:")
    for obj_table in [
        CTablePayment.__table__,
        CTableProductOrder.__table__,
        CTableShippingOrder.__table__,
        CTablePurchaseRequest.__table__,
        CTablePurchaseOrder.__table__,
        CTableGoodsReceiptNote.__table__,
        CTableWorkOrder.__table__,
        CTableProductionData.__table__,
        CTableOrderPayment.__table__,
    ]:
        obj_table.create(bind=obj_engine)
    return sessionmaker(bind=obj_engine)()


def seed_orders_base(obj_session):
    n_now = 1700000000
    obj_session.add_all([
        CTableProductOrder(
            no="SO-001",
            date=n_now - 5 * 86400,
            item_no="COOKIE-001",
            item_name="é¤…ä¹¾ç¦®ç›’",
            item_ref_no="CUST-001",
            item_ref_displayName="æ¸¬è©¦å®¢æˆ¶",
            unit=EUnit.BOX,
            price=20,
            count=10000,
            amount=200000,
            expectedDate=n_now + 3 * 86400,
            payment_type=EPaymentType.MONTH,
            payment_date=10,
            payment_period=30,
            comment="cookie order",
            creationTime=n_now - 6 * 86400,
        ),
        CTablePurchaseRequest(
            no="PR-001",
            product_order_no="SO-001",
            date=n_now - 4 * 86400,
            item_no="RM-COOKIE",
            unit=EUnit.KILOGRAM,
            count=100,
            expectedDate=n_now - 2 * 86400,
        ),
        CTablePurchaseOrder(
            no="PO-001",
            purchase_request_no="PR-001",
            date=n_now - 4 * 86400,
            item_no="RM-COOKIE",
            item_name="é¤…ä¹¾åŽŸæ–™",
            unit=EUnit.KILOGRAM,
            count=100,
            amount=30000,
        ),
        CTableGoodsReceiptNote(
            no="GR-001",
            purchase_order_no="PO-001",
            date=n_now - 3 * 86400,
            item_no="RM-COOKIE",
            item_name="é¤…ä¹¾åŽŸæ–™",
            unit=EUnit.KILOGRAM,
            expectedCount=60,
            checkedCount=60,
        ),
        CTableGoodsReceiptNote(
            no="GR-002",
            purchase_order_no="PO-001",
            date=n_now - 2 * 86400,
            item_no="RM-COOKIE",
            item_name="é¤…ä¹¾åŽŸæ–™",
            unit=EUnit.KILOGRAM,
            expectedCount=40,
            checkedCount=40,
        ),
        CTableWorkOrder(
            no="WO-001",
            date=n_now - 2 * 86400,
            product_order_no="SO-001",
            product_no="COOKIE-001",
            product_name="é¤…ä¹¾ç¦®ç›’",
            processCount=5000,
            laborCount=8,
        ),
        CTableWorkOrder(
            no="WO-002",
            date=n_now - 1 * 86400,
            product_order_no="SO-001",
            product_no="COOKIE-001",
            product_name="é¤…ä¹¾ç¦®ç›’",
            processCount=5000,
            laborCount=8,
        ),
        CTableProductionData(
            work_order_no="WO-001",
            product_order_no="SO-001",
            customer_no="CUST-001",
            product_no="COOKIE-001",
            product_name="é¤…ä¹¾ç¦®ç›’",
            date=n_now - 1 * 86400,
        ),
        CTableShippingOrder(
            no="SH-001",
            product_order_no="SO-001",
            date=n_now - 3600,
            item_no="COOKIE-001",
            item_name="é¤…ä¹¾ç¦®ç›’",
            unit=EUnit.BOX,
            expectedCount=5000,
            checkedCount=5000,
            amount=100000,
        ),
        CTableOrderPayment(
            no="AR-001",
            group_no="AR-G-001",
            date=n_now,
            ref_no="SO-001",
            ref_sub_no="SH-001",
            item_ref_no="CUST-001",
            item_ref_displayName="æ¸¬è©¦å®¢æˆ¶",
            paymentType=EPaymentType.MONTH,
            month=date(2023, 11, 1),
            amount=100000,
            totalAmount=100000,
            balance=100000,
        ),
    ])
    obj_session.commit()
    return n_now


def test_orders_dashboard_service_returns_confirmed_dataset():
    obj_session = build_session()
    n_now = seed_orders_base(obj_session)

    dict_payload = COrdersDashboardService()._get_dashboard_with_session(
        n_date=n_now,
        str_timezone="Asia/Taipei",
        str_period="30d",
        obj_session=obj_session,
    )

    assert dict_payload["summary"]["openOrderCount"] == 1
    assert dict_payload["summary"]["commitmentRate"] == 0.0
    assert dict_payload["summary"]["paymentRiskCount"] == 1
    assert dict_payload["summary"]["totalOrderAmount"] == 200000
    assert dict_payload["commitmentChecks"] == []

    dict_order = dict_payload["orders"][0]
    assert dict_order["orderNo"] == "SO-001"
    assert dict_order["quantity"] == 10000.0
    assert dict_order["shipmentSummary"]["shipmentCount"] == 1
    assert dict_order["shipmentSummary"]["shippedQuantity"] == 5000.0
    assert dict_order["shipmentSummary"]["shippingStatus"] == "partial_shipped"
    assert dict_order["stage"] == "in_production"
    assert dict_order["commitmentDecision"] == "deferred"
    assert dict_order["productionFeasibility"] == "deferred"
    assert dict_order["materialStatus"] == "ready"
    assert dict_order["productionStatus"] == "in_progress"
    assert dict_order["paymentStatus"] == "unpaid"

    dict_shipment = dict_payload["shipments"][0]
    assert dict_shipment["shippingOrderNo"] == "SH-001"
    assert dict_shipment["paymentType"] == "monthly"
    assert dict_shipment["paymentDueTimestamp"] > 0

    dict_payment = dict_payload["paymentSignals"][0]
    assert dict_payment["paymentNo"] == "AR-001"
    assert dict_payment["remainingAmount"] == 100000
    assert dict_payment["paymentRisk"] == "unpaid"


def test_orders_fulfillment_service_returns_workflow_steps():
    obj_session = build_session()
    n_now = seed_orders_base(obj_session)

    dict_payload = COrdersDashboardService()._get_fulfillment_with_session(
        str_order_no="SO-001",
        n_date=n_now,
        str_timezone="Asia/Taipei",
        obj_session=obj_session,
    )

    dict_steps = {
        dict_row["stepCode"]: dict_row
        for dict_row in dict_payload["workflow"]
    }
    assert dict_steps["order_received"]["status"] == "done"
    assert dict_steps["purchase_readiness"]["refNo"] == "PO-001"
    assert dict_steps["warehouse_readiness"]["refNo"] == "GR-001,GR-002"
    assert dict_steps["production"]["refNo"] == "WO-001,WO-002"
    assert dict_steps["production"]["status"] == "in_progress"
    assert dict_steps["shipping"]["refNo"] == "SH-001"
    assert dict_steps["shipping"]["status"] == "in_progress"
    assert dict_steps["payment"]["refNo"] == "AR-001"

    dict_dependencies = {
        dict_row["area"]: dict_row
        for dict_row in dict_payload["dependencies"]
    }
    assert dict_dependencies["inventory"]["status"] == "ready"
    assert dict_dependencies["payment"]["status"] == "pending"


def test_orders_routes_return_existing_api_envelope(monkeypatch):
    from flask import Flask

    from package.restserver.api.v2.orders_uri import orders_v2

    def fake_get_dashboard(self, **dict_kwargs):
        return {
            "serverTimestamp": 1700000000,
            "summary": {"openOrderCount": 1},
            "orders": [{"orderNo": "SO-001"}],
            "shipments": [],
            "commitmentChecks": [],
            "deliveryRisks": [],
            "marginSignals": [],
            "paymentSignals": [],
        }

    def fake_get_fulfillment(self, **dict_kwargs):
        return {
            "orderNo": dict_kwargs.get("str_order_no"),
            "workflow": [{"stepCode": "order_received"}],
            "dependencies": [],
        }

    monkeypatch.setenv("TOKEN_ENABLED", "1")
    monkeypatch.setattr(COrdersDashboardService, "get_dashboard", fake_get_dashboard)
    monkeypatch.setattr(COrdersDashboardService, "get_fulfillment", fake_get_fulfillment)

    obj_app = Flask(__name__)
    obj_app.register_blueprint(orders_v2)
    obj_client = obj_app.test_client()

    obj_dashboard_response = obj_client.get(
        "/api/v2/orders/dashboard",
        headers={"x-auth-token": "test-token", "x-timezone": "Asia/Taipei"},
    )
    obj_fulfillment_response = obj_client.get(
        "/api/v2/orders/SO-001/fulfillment",
        headers={"x-auth-token": "test-token", "x-timezone": "Asia/Taipei"},
    )

    assert obj_dashboard_response.status_code == 200
    dict_dashboard = json.loads(obj_dashboard_response.data.decode("utf8"))
    assert dict_dashboard["code"] == 0
    assert dict_dashboard["payload"]["summary"]["openOrderCount"] == 1

    assert obj_fulfillment_response.status_code == 200
    dict_fulfillment = json.loads(obj_fulfillment_response.data.decode("utf8"))
    assert dict_fulfillment["code"] == 0
    assert dict_fulfillment["payload"]["orderNo"] == "SO-001"
