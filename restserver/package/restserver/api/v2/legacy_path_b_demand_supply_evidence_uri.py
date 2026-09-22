# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.legacy_path_b_demand_supply_evidence import CLegacyPathBDemandSupplyEvidenceOverview


legacy_path_b_demand_supply_evidence_v2 = Blueprint("legacy_path_b_demand_supply_evidence_v2", __name__)


class CLegacyPathBDemandSupplyEvidenceOverviewURI(CAPIBase):
    def _get_executor(self):
        return CLegacyPathBDemandSupplyEvidenceOverview()

    def _is_vaildate_param(self):
        return False


@legacy_path_b_demand_supply_evidence_v2.route(URL_PATH_V2 + "/legacy-path-b/demand-supply-evidence/overview", methods=["GET"])
def overview():
    return CLegacyPathBDemandSupplyEvidenceOverviewURI().run()
