# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.bom import CBomCenterDashboard, CBomCenterDetail


SUBKEY = "bom"
bom_v2 = Blueprint("bom_v2", __name__)


class CBomCenterDashboardURI(CAPIBase):
    def _get_executor(self):
        return CBomCenterDashboard()

    def _is_vaildate_param(self):
        return False


class CBomCenterDetailURI(CAPIBase):
    def _get_executor(self):
        return CBomCenterDetail()

    def _is_vaildate_param(self):
        return False


@bom_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/dashboard", methods=["GET"])
def dashboard():
    return CBomCenterDashboardURI().run()


@bom_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/<bom_no>/detail", methods=["GET"])
def detail(bom_no):
    return CBomCenterDetailURI().run(bom_no or "")
