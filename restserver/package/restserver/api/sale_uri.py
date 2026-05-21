# coding=utf8
from flask import Blueprint
from .sale import *
from .common import *
from .apibase import CAPIBase


SUBKEY = 'sale'
sale = Blueprint('sale', __name__)

class CProductOrderURI(CAPIBase):

    def _get_executor(self):
        return CProductOrder()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False

class CShippingOrderURI(CAPIBase):

    def _get_executor(self):
        return CShippingOrder()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False

class CStatisticURI(CAPIBase):

    def _get_executor(self):
        return CStatistic()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False

class CPaymentURI(CAPIBase):

    def _get_executor(self):
        return CPayment()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False

class CARAPURI(CAPIBase):

    def _get_executor(self):
        return CSaleARAP()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False

class CContractURI(CAPIBase):

    def _get_executor(self):
        return CSaleContract()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False


@sale.route(URL_PATH+'/'+SUBKEY+'/productorder', methods=['GET', 'POST', 'PUT', 'DELETE'])
def order():
    obj_uri = CProductOrderURI()
    return obj_uri.run()


@sale.route(URL_PATH+'/'+SUBKEY+'/shippingorder', methods=['GET', 'POST', 'PUT', 'DELETE'])
def shippingOrder():
    obj_uri = CShippingOrderURI()
    return obj_uri.run()

@sale.route(URL_PATH+'/'+SUBKEY+'/statistics', methods=['GET'])
def statistic():
    obj_uri = CStatisticURI()
    return obj_uri.run()

@sale.route(URL_PATH+'/'+SUBKEY+'/payment', methods=['GET', 'POST', 'PUT', 'DELETE'])
def payment():
    obj_uri = CPaymentURI()
    return obj_uri.run()

@sale.route(URL_PATH+'/'+SUBKEY+'/contract', methods=['GET', 'POST', 'PUT', 'DELETE'])
def contract():
    obj_uri = CContractURI()
    return obj_uri.run()

@sale.route(URL_PATH+'/'+SUBKEY+'/arap', methods=['GET'])
def arap():
    obj_uri = CARAPURI()
    return obj_uri.run()
