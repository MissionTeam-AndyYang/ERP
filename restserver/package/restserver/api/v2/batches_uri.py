# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.batches import (
    CBatchCenterDashboard,
    CBatchCenterDetail,
    CBatchCenterDistribution,
)


SUBKEY = "batches"

batches_v2 = Blueprint("batches_v2", __name__)


class CBatchCenterDashboardURI(CAPIBase):
    def _get_executor(self):
        return CBatchCenterDashboard()

    def _is_vaildate_param(self):
        return False


class CBatchCenterDistributionURI(CAPIBase):
    def _get_executor(self):
        return CBatchCenterDistribution()

    def _is_vaildate_param(self):
        return False


class CBatchCenterDetailURI(CAPIBase):
    def _get_executor(self):
        return CBatchCenterDetail()

    def _is_vaildate_param(self):
        return False


@batches_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/dashboard", methods=["GET"])
def dashboard():
    obj_uri = CBatchCenterDashboardURI()
    return obj_uri.run()


@batches_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/items/<item_no>/distribution", methods=["GET"])
def distribution(item_no):
    obj_uri = CBatchCenterDistributionURI()
    return obj_uri.run(item_no or "")


@batches_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/<batch_no>/detail", methods=["GET"])
def detail(batch_no):
    obj_uri = CBatchCenterDetailURI()
    return obj_uri.run(batch_no or "")
