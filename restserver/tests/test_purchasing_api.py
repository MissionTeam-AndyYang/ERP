# coding=utf8
import sys
from pathlib import Path


RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.restserver.api.v2 import purchasing


class _FakePurchasingService(object):
    def __init__(self, str_timezone):
        self.str_timezone = str_timezone

    def get_dashboard(self):
        return {"endpoint": "dashboard"}

    def get_delivery_risk(self):
        return {"endpoint": "delivery-risk"}

    def get_receipts(self):
        return {"endpoint": "receipts"}

    def get_suppliers(self):
        return {"endpoint": "suppliers"}

    def get_detail(self, str_order_no):
        return {"endpoint": "detail", "purchaseOrderNo": str_order_no}


def test_purchasing_executors_dispatch_to_one_endpoint(monkeypatch):
    monkeypatch.setattr(purchasing, "CPurchasingPurchaseOrderService", _FakePurchasingService)

    lst_cases = [
        (purchasing.CPurchasingPurchaseOrderDashboard(), "dashboard", ""),
        (purchasing.CPurchasingPurchaseOrderDeliveryRisk(), "delivery-risk", ""),
        (purchasing.CPurchasingGoodsReceiptDashboard(), "receipts", ""),
        (purchasing.CPurchasingSupplierDashboard(), "suppliers", ""),
        (purchasing.CPurchasingPurchaseOrderDetail(), "detail", "PO-001"),
    ]

    for obj_executor, str_endpoint, str_order_no in lst_cases:
        n_status, n_code, str_message, dict_payload = obj_executor.get("Asia/Taipei", str_order_no)
        assert n_status == 200
        assert n_code == 0
        assert str_message == "success"
        assert dict_payload["endpoint"] == str_endpoint
        if str_order_no:
            assert dict_payload["purchaseOrderNo"] == str_order_no
