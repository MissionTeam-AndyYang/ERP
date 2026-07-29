# coding=utf8
from flask import Blueprint
from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.purchasing import (
    CPurchasingGoodsReceiptDashboard,
    CPurchasingPurchaseOrderDashboard,
    CPurchasingPurchaseOrderDeliveryRisk,
    CPurchasingPurchaseOrderDetail,
    CPurchasingSupplierDashboard,
)

SUBKEY = "purchasing"
purchasing_v2 = Blueprint("purchasing_v2", __name__)


class CPurchasingPurchaseOrderDashboardURI(CAPIBase):
    def _get_executor(self):
        return CPurchasingPurchaseOrderDashboard()

    def _is_vaildate_param(self):
        return False


class CPurchasingPurchaseOrderDeliveryRiskURI(CAPIBase):
    def _get_executor(self):
        return CPurchasingPurchaseOrderDeliveryRisk()

    def _is_vaildate_param(self):
        return False


class CPurchasingGoodsReceiptDashboardURI(CAPIBase):
    def _get_executor(self):
        return CPurchasingGoodsReceiptDashboard()

    def _is_vaildate_param(self):
        return False


class CPurchasingSupplierDashboardURI(CAPIBase):
    def _get_executor(self):
        return CPurchasingSupplierDashboard()

    def _is_vaildate_param(self):
        return False


class CPurchasingPurchaseOrderDetailURI(CAPIBase):
    def _get_executor(self):
        return CPurchasingPurchaseOrderDetail()

    def _is_vaildate_param(self):
        return False


@purchasing_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/purchase-orders/dashboard", methods=["GET"])
def purchase_order_dashboard():
    return CPurchasingPurchaseOrderDashboardURI().run()


@purchasing_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/purchase-orders/delivery-risk", methods=["GET"])
def purchase_order_delivery_risk():
    return CPurchasingPurchaseOrderDeliveryRiskURI().run()


@purchasing_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/goods-receipts/dashboard", methods=["GET"])
def goods_receipts_dashboard():
    return CPurchasingGoodsReceiptDashboardURI().run()


@purchasing_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/suppliers/dashboard", methods=["GET"])
def suppliers_dashboard():
    return CPurchasingSupplierDashboardURI().run()


@purchasing_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/purchase-orders/<purchase_order_no>/detail", methods=["GET"])
def purchase_order_detail(purchase_order_no):
    return CPurchasingPurchaseOrderDetailURI().run(purchase_order_no or "")
