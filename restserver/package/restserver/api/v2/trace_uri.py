# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.trace import CTraceabilityBatchOverview, CTraceabilityDashboard


SUBKEY = "trace"

trace_v2 = Blueprint("trace_v2", __name__)


class CTraceabilityDashboardURI(CAPIBase):
    def _get_executor(self):
        return CTraceabilityDashboard()

    def _is_vaildate_param(self):
        return False


class CTraceabilityBatchOverviewURI(CAPIBase):
    def _get_executor(self):
        return CTraceabilityBatchOverview()

    def _is_vaildate_param(self):
        return False


@trace_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/dashboard", methods=["GET"])
def dashboard():
    obj_uri = CTraceabilityDashboardURI()
    return obj_uri.run()


@trace_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/batches/<batch_no>/overview", methods=["GET"])
def batch_overview(batch_no):
    obj_uri = CTraceabilityBatchOverviewURI()
    return obj_uri.run(batch_no or "")
