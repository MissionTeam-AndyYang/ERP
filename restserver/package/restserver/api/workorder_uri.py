# coding=utf8
from flask import Blueprint
from .workorder import *
from .common import *
from .apibase import CAPIBase


SUBKEY = 'workorder'
workorder = Blueprint('workorder', __name__)

class CWorkOrderURI(CAPIBase):

    def _get_executor(self):
        return CWorkOrder()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False

class CProductDataURI(CAPIBase):

    def _get_executor(self):
        return CProductData()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

class CExpectedDataURI(CAPIBase):

    def _get_executor(self):
        return CExpectedData()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False


class CStatisticURI(CAPIBase):

    def _get_executor(self):
        return CStatistic()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False


@workorder.route(URL_PATH+'/'+SUBKEY, methods=['GET'])
def index():
    obj_uri = CWorkOrderURI()
    return obj_uri.run()


@workorder.route(URL_PATH+'/'+SUBKEY+'/productdata', methods=['GET'])
def product_data():
    obj_uri = CProductDataURI()
    return obj_uri.run()

@workorder.route(URL_PATH+'/'+SUBKEY+'/expecteddata', methods=['GET'])
def expected_data():
    obj_uri = CExpectedDataURI()
    return obj_uri.run()

@workorder.route(URL_PATH+'/'+SUBKEY+'/statistics', methods=['GET'])
def statistic():
    obj_uri = CStatisticURI()
    return obj_uri.run()
