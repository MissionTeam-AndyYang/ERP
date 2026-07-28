# coding=utf8
from flask import Blueprint
from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.purchasing import CPurchasingPurchaseOrder

SUBKEY = "purchasing"
purchasing_v2 = Blueprint("purchasing_v2", __name__)


class CPurchasingPurchaseOrderURI(CAPIBase):
    def _get_executor(self):
        return CPurchasingPurchaseOrder()

    def _is_vaildate_param(self):
        return False


@purchasing_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/purchase-orders/dashboard", methods=["GET"])
def purchase_order_dashboard():
    return CPurchasingPurchaseOrderURI().run()


@purchasing_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/purchase-orders/delivery-risk", methods=["GET"])
def purchase_order_delivery_risk():
    return CPurchasingPurchaseOrderURI().run()


@purchasing_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/goods-receipts/dashboard", methods=["GET"])
def goods_receipts_dashboard():
    return CPurchasingPurchaseOrderURI().run()


@purchasing_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/suppliers/dashboard", methods=["GET"])
def suppliers_dashboard():
    return CPurchasingPurchaseOrderURI().run()


@purchasing_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/purchase-orders/<purchase_order_no>/detail", methods=["GET"])
def purchase_order_detail(purchase_order_no):
    return CPurchasingPurchaseOrderURI().run(purchase_order_no or "")
