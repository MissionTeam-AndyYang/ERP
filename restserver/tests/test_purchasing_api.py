# coding=utf8
import sys
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.restserver.api.v2 import purchasing
from package.common.common import EInventoryCategory, EInventoryRefCategory, EWorkflowTaskStatus, EWorkflowTaskType
from package.dbwrapper.table import CTableGoodsReceiptNote, CTableInventoryRec, CTableWorkflowTaskState


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


def test_warehouse_state_uses_workflow_and_inventory_evidence():
    obj_engine = create_engine("sqlite:///:memory:")
    for obj_table in [
        CTableGoodsReceiptNote.__table__,
        CTableWorkflowTaskState.__table__,
        CTableInventoryRec.__table__,
    ]:
        obj_table.create(bind=obj_engine)
    obj_session = sessionmaker(bind=obj_engine)()
    obj_receipt = CTableGoodsReceiptNote(no="GR-001", purchase_order_no="PO-001")
    obj_task = CTableWorkflowTaskState(
        taskId="TASK-001", taskType=EWorkflowTaskType.INBOUND,
        refCategory=EInventoryRefCategory.WORK, ref_no="GR-001",
        taskStatus=EWorkflowTaskStatus.DONE, ownerDepartment=8,
        updateTime=200,
    )
    obj_inventory = CTableInventoryRec(
        refCategory=EInventoryRefCategory.PURCHASE, ref_no="GR-001",
        category=EInventoryCategory.IN, count=10,
    )
    obj_session.add_all([obj_receipt, obj_task, obj_inventory])
    obj_session.commit()

    obj_service = purchasing.CPurchasingPurchaseOrderService("Asia/Taipei")
    dict_states = obj_service._CPurchasingPurchaseOrderService__warehouse_states(
        obj_session, [obj_receipt]
    )

    assert dict_states["GR-001"] == {
        "warehouseStatusCode": "stocked",
        "nextOwnerDepartment": 8,
    }
