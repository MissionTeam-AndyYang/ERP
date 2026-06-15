# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH
from package.restserver.api.v2.warehouse import CWarehouseDashboard


URL_PATH_V2 = URL_PATH.replace("/v1", "/v2")
SUBKEY = "warehouse"

warehouse_v2 = Blueprint("warehouse_v2", __name__)


class CWarehouseDashboardURI(CAPIBase):
    def _get_executor(self):
        return CWarehouseDashboard()

    def _is_vaildate_param(self):
        return False


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/dashboard", methods=["GET"])
def dashboard():
    obj_uri = CWarehouseDashboardURI()
    return obj_uri.run()

