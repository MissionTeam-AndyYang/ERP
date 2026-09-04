# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.packaging_specification import CPackagingSpecificationOverview


SUBKEY = "packaging-specification"
packaging_specification_v2 = Blueprint("packaging_specification_v2", __name__)


class CPackagingSpecificationOverviewURI(CAPIBase):
    def _get_executor(self):
        return CPackagingSpecificationOverview()

    def _is_vaildate_param(self):
        return False


@packaging_specification_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/overview", methods=["GET"])
def overview():
    return CPackagingSpecificationOverviewURI().run()
