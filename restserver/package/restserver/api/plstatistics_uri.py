# coding=utf8
from flask import Blueprint
from .plstatistics import *
from .common import *
from .apibase import CAPIBase

SUBKEY = 'plstatistics'
plstatistics = Blueprint('plstatistics', __name__)


class CManCapacityURI(CAPIBase):

    def _get_executor(self):
        return CManCapacity()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False


class CItemCapacityURI(CAPIBase):

    def _get_executor(self):
        return CItemCapacity()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

class CItemLossURI(CAPIBase):

    def _get_executor(self):
        return CItemLoss()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

class CItemCostURI(CAPIBase):

    def _get_executor(self):
        return CItemCost()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

@plstatistics.route(URL_PATH + '/' + SUBKEY + '/mancapacity' , methods=['GET'])
def mancapacity():
    obj_uri = CManCapacityURI()
    return obj_uri.run()

@plstatistics.route(URL_PATH + '/' + SUBKEY + '/itemcapacity' , methods=['GET'])
def itemcapacity():
    obj_uri = CItemCapacityURI()
    return obj_uri.run()

@plstatistics.route(URL_PATH + '/' + SUBKEY + '/itemloss' , methods=['GET'])
def itemloss():
    obj_uri = CItemLossURI()
    #產線料品消耗
    return obj_uri.run()

@plstatistics.route(URL_PATH + '/' + SUBKEY + '/itemcost' , methods=['GET'])
def itemcost():
    obj_uri = CItemCostURI()
    return obj_uri.run()


