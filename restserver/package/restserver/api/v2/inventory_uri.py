# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.inventory import (
    CInventoryBalances,
    CInventoryLotTrace,
    CInventoryLots,
    CInventoryMovements,
)


SUBKEY_INVENTORY = "inventory"
SUBKEY_LOTS = "lots"

inventory_v2 = Blueprint("inventory_v2", __name__)


class CInventoryReadURI(CAPIBase):
    def _is_vaildate_param(self):
        return False

    def _is_support_post(self):
        return False

    def _is_support_put(self):
        return False

    def _is_support_delete(self):
        return False


class CInventoryBalancesURI(CInventoryReadURI):
    def _get_executor(self):
        return CInventoryBalances()


class CInventoryMovementsURI(CInventoryReadURI):
    def _get_executor(self):
        return CInventoryMovements()


class CInventoryLotsURI(CInventoryReadURI):
    def _get_executor(self):
        return CInventoryLots()


class CInventoryLotTraceURI(CInventoryReadURI):
    def _get_executor(self):
        return CInventoryLotTrace()


@inventory_v2.route(URL_PATH_V2 + "/" + SUBKEY_INVENTORY + "/balances", methods=["GET"])
def balances():
    return CInventoryBalancesURI().run()


@inventory_v2.route(URL_PATH_V2 + "/" + SUBKEY_INVENTORY + "/movements", methods=["GET"])
def movements():
    return CInventoryMovementsURI().run()


@inventory_v2.route(URL_PATH_V2 + "/" + SUBKEY_LOTS, methods=["GET"])
def lots():
    return CInventoryLotsURI().run()


@inventory_v2.route(URL_PATH_V2 + "/" + SUBKEY_LOTS + "/<lot_code>/trace", methods=["GET"])
def lot_trace(lot_code):
    return CInventoryLotTraceURI().run(lot_code or "")
