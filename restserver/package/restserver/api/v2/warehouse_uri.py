# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.warehouse import (
    CWarehouseDashboard,
    CWarehouseInventory,
    CWarehouseInventoryLotDetail,
    CWarehouseInventoryLots,
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


class CWarehouseInventoryLotsURI(CAPIBase):
    def _get_executor(self):
        return CWarehouseInventoryLots()

    def _is_vaildate_param(self):
        return False


class CWarehouseInventoryLotDetailURI(CAPIBase):
    def _get_executor(self):
        return CWarehouseInventoryLotDetail()

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


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/inventory/lots", methods=["GET"])
def inventory_lots():
    obj_uri = CWarehouseInventoryLotsURI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/inventory/lots/wh/<warehouse_no>/item/<item_no>/batch/<batch_no>", methods=["GET"])
def inventory_lot_detail(warehouse_no, item_no, batch_no):
    obj_uri = CWarehouseInventoryLotDetailURI()
    return obj_uri.run("%s|%s|%s" % (warehouse_no or "", item_no or "", batch_no or ""))


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/tasks", methods=["GET"])
def tasks():
    obj_uri = CWarehouseTasksURI()
    return obj_uri.run()
