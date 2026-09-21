# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.manufacturing_definition import CManufacturingDefinitionOverview


manufacturing_definition_v2 = Blueprint("manufacturing_definition_v2", __name__)


class CManufacturingDefinitionOverviewURI(CAPIBase):
    def _get_executor(self):
        return CManufacturingDefinitionOverview()

    def _is_vaildate_param(self):
        return False


@manufacturing_definition_v2.route(URL_PATH_V2 + "/manufacturing-definition/overview", methods=["GET"])
def overview():
    return CManufacturingDefinitionOverviewURI().run()
