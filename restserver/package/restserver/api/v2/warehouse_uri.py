# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.warehouse import (
    CWarehouseDashboard,
    CWarehouseInventoryLotDetail,
    CWarehouseInventoryLots,
)


SUBKEY = "warehouse"

warehouse_v2 = Blueprint("warehouse_v2", __name__)


class CWarehouseDashboardURI(CAPIBase):
    def _get_executor(self):
        return CWarehouseDashboard()

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


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/dashboard", methods=["GET"])
def dashboard():
    obj_uri = CWarehouseDashboardURI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/inventory/lots", methods=["GET"])
def inventory_lots():
    obj_uri = CWarehouseInventoryLotsURI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/inventory/lots/<path:str_lot_key>", methods=["GET"])
def inventory_lot_detail(str_lot_key):
    obj_uri = CWarehouseInventoryLotDetailURI()
    return obj_uri.run(str_lot_key)
