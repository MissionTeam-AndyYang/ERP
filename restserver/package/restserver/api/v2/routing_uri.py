# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.routing import (
    CRoutingCurrent,
    CRoutingDashboard,
    CRoutingSteps,
    CRoutingVersions,
)


SUBKEY = "routing"
routing_v2 = Blueprint("routing_v2", __name__)


class CRoutingDashboardURI(CAPIBase):
    def _get_executor(self):
        return CRoutingDashboard()

    def _is_vaildate_param(self):
        return False


class CRoutingVersionsURI(CAPIBase):
    def _get_executor(self):
        return CRoutingVersions()

    def _is_vaildate_param(self):
        return False


class CRoutingStepsURI(CAPIBase):
    def _get_executor(self):
        return CRoutingSteps()

    def _is_vaildate_param(self):
        return False


class CRoutingCurrentURI(CAPIBase):
    def _get_executor(self):
        return CRoutingCurrent()

    def _is_vaildate_param(self):
        return False


@routing_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/dashboard", methods=["GET"])
def dashboard():
    return CRoutingDashboardURI().run()


@routing_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/products/<item_no>/versions", methods=["GET"])
def versions(item_no):
    return CRoutingVersionsURI().run(item_no or "")


@routing_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/versions/<routing_version_id>/steps", methods=["GET"])
def steps(routing_version_id):
    return CRoutingStepsURI().run(routing_version_id or "")


@routing_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/products/<item_no>/current", methods=["GET"])
def current(item_no):
    return CRoutingCurrentURI().run(item_no or "")

