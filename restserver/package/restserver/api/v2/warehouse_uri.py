# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.warehouse import (
    CWarehouseDashboard,
    CWarehouseInventory,
    CWarehouseTasks,
)


SUBKEY = "warehouse"

warehouse_v2 = Blueprint("warehouse_v2", __name__)


class CWarehouseDashboardURI(CAPIBase):
    def _get_executor(self):
        return CWarehouseDashboard()

    def _is_vaildate_param(self):
        return False


class CWarehouseInventoryURI(CAPIBase):
    def _get_executor(self):
        return CWarehouseInventory()

    def _is_vaildate_param(self):
        return False


class CWarehouseTasksURI(CAPIBase):
    def _get_executor(self):
        return CWarehouseTasks()

    def _is_vaildate_param(self):
        return False


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/dashboard", methods=["GET"])
def dashboard():
    obj_uri = CWarehouseDashboardURI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/inventory", methods=["GET"])
def inventory():
    obj_uri = CWarehouseInventoryURI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/tasks", methods=["GET"])
def tasks():
    obj_uri = CWarehouseTasksURI()
    return obj_uri.run()
