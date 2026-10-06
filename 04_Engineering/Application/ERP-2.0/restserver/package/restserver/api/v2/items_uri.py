# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.items import CItemCenterDashboard, CItemCenterDetail


SUBKEY = "items"
items_v2 = Blueprint("items_v2", __name__)


class CItemCenterDashboardURI(CAPIBase):
    def _get_executor(self):
        return CItemCenterDashboard()

    def _is_vaildate_param(self):
        return False


class CItemCenterDetailURI(CAPIBase):
    def _get_executor(self):
        return CItemCenterDetail()

    def _is_vaildate_param(self):
        return False


@items_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/dashboard", methods=["GET"])
def dashboard():
    return CItemCenterDashboardURI().run()


@items_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/<item_no>/detail", methods=["GET"])
def detail(item_no):
    return CItemCenterDetailURI().run(item_no or "")
