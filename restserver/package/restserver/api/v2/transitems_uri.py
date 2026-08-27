# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.transitems import (
    CTransItemsCompanyDetail,
    CTransItemsDashboard,
    CTransItemsTransItemDetail,
)


SUBKEY = "transitems"
transitems_v2 = Blueprint("transitems_v2", __name__)


class CTransItemsDashboardURI(CAPIBase):
    def _get_executor(self):
        return CTransItemsDashboard()

    def _is_vaildate_param(self):
        return False


class CTransItemsCompanyDetailURI(CAPIBase):
    def _get_executor(self):
        return CTransItemsCompanyDetail()

    def _is_vaildate_param(self):
        return False


class CTransItemsTransItemDetailURI(CAPIBase):
    def _get_executor(self):
        return CTransItemsTransItemDetail()

    def _is_vaildate_param(self):
        return False


@transitems_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/dashboard", methods=["GET"])
def dashboard():
    return CTransItemsDashboardURI().run()


@transitems_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/companies/<company_no>/detail", methods=["GET"])
def company_detail(company_no):
    return CTransItemsCompanyDetailURI().run(company_no or "")


@transitems_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/transitems/<trans_item_no>/detail", methods=["GET"])
def trans_item_detail(trans_item_no):
    return CTransItemsTransItemDetailURI().run(trans_item_no or "")
