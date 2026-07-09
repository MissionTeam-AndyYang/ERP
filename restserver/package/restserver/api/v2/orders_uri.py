# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.orders import (
    COrdersDashboard,
    COrdersFulfillment,
)


SUBKEY = "orders"

orders_v2 = Blueprint("orders_v2", __name__)


class COrdersDashboardURI(CAPIBase):
    def _get_executor(self):
        return COrdersDashboard()

    def _is_vaildate_param(self):
        return False


class COrdersFulfillmentURI(CAPIBase):
    def _get_executor(self):
        return COrdersFulfillment()

    def _is_vaildate_param(self):
        return False


@orders_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/dashboard", methods=["GET"])
def dashboard():
    obj_uri = COrdersDashboardURI()
    return obj_uri.run()


@orders_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/<order_no>/fulfillment", methods=["GET"])
def fulfillment(order_no):
    obj_uri = COrdersFulfillmentURI()
    return obj_uri.run(order_no or "")
