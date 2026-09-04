# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.product_wip_360 import CProductWip360Overview


SUBKEY = "product-wip-360"
product_wip_360_v2 = Blueprint("product_wip_360_v2", __name__)


class CProductWip360OverviewURI(CAPIBase):
    def _get_executor(self):
        return CProductWip360Overview()

    def _is_vaildate_param(self):
        return False


@product_wip_360_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/overview", methods=["GET"])
def overview():
    return CProductWip360OverviewURI().run()
