# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.quality_trace_delivery_evidence import CQualityTraceDeliveryEvidenceOverview


quality_trace_delivery_evidence_v2 = Blueprint("quality_trace_delivery_evidence_v2", __name__)


class CQualityTraceDeliveryEvidenceOverviewURI(CAPIBase):
    def _get_executor(self):
        return CQualityTraceDeliveryEvidenceOverview()

    def _is_vaildate_param(self):
        return False


@quality_trace_delivery_evidence_v2.route(URL_PATH_V2 + "/quality-trace-delivery-evidence/overview", methods=["GET"])
def overview():
    return CQualityTraceDeliveryEvidenceOverviewURI().run()
