# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.production import CProductionDashboard, CProductionWorkOrderDetail


SUBKEY = "production"
production_v2 = Blueprint("production_v2", __name__)


class CProductionDashboardURI(CAPIBase):
    def _get_executor(self):
        return CProductionDashboard()

    def _is_vaildate_param(self):
        return False


class CProductionWorkOrderDetailURI(CAPIBase):
    def _get_executor(self):
        return CProductionWorkOrderDetail()

    def _is_vaildate_param(self):
        return False


@production_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/dashboard", methods=["GET"])
def dashboard():
    return CProductionDashboardURI().run()


@production_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/work-orders/<work_order_no>/detail", methods=["GET"])
def work_order_detail(work_order_no):
    return CProductionWorkOrderDetailURI().run(work_order_no or "")
