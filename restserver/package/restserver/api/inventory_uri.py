# coding=utf8
from flask import Blueprint
from .inventory import *
from .common import *
from .apibase import CAPIBase

SUBKEY = 'inventory'
inventory = Blueprint('inventory', __name__)

class CPriceURI(CAPIBase):

    def _get_executor(self):
        return CPrice()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

class CInventoryURI(CAPIBase):

    def _get_executor(self):
        return CInventory()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

class CStatisticsURI(CAPIBase):

    def _get_executor(self):
        return CStatistics()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

class CItemsURI(CAPIBase):

    def _get_executor(self):
        return CItems()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False


class CMonthsURI(CAPIBase):

    def _get_executor(self):
        return CMonthAmount()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False


@inventory.route(URL_PATH + '/' + SUBKEY, methods=['GET'])
def index():
    obj_uri = CInventoryURI()
    return obj_uri.run()


@inventory.route(URL_PATH + '/' + SUBKEY+ '/price', methods=['GET'])
def price():
    obj_uri = CPriceURI()
    return obj_uri.run()


@inventory.route(URL_PATH + '/' + SUBKEY+ '/statistics', methods=['GET'])
def statistics():
    obj_uri = CStatisticsURI()
    return obj_uri.run()


@inventory.route(URL_PATH + '/' + SUBKEY+ '/items', methods=['GET'])
def items():
    obj_uri = CItemsURI()
    return obj_uri.run()



@inventory.route(URL_PATH + '/' + SUBKEY+ '/months', methods=['GET'])
def months():
    obj_uri = CMonthsURI()
    return obj_uri.run()

