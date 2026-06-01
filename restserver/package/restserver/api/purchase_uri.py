# coding=utf8
from flask import Blueprint
from .purchase import *
from .common import *
from .apibase import CAPIBase


SUBKEY = 'purchase'
purchase = Blueprint('purchase', __name__)

class CPurchaseOrderURI(CAPIBase):

    def _get_executor(self):
        return CPurchaseOrder()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False

class CGoodsReceiptNoteURI(CAPIBase):

    def _get_executor(self):
        return CGoodsReceiptNote()

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
        return CPurchaseARAP()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False

class CContractURI(CAPIBase):

    def _get_executor(self):
        return CPurchaseContract()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False

@purchase.route(URL_PATH+'/'+SUBKEY+'/purchaseorder', methods=['GET'])
def order():
    obj_uri = CPurchaseOrderURI()
    return obj_uri.run()


@purchase.route(URL_PATH+'/'+SUBKEY+'/goodsreceiptnote', methods=['GET'])
def goodsreceiptnote():
    obj_uri = CGoodsReceiptNoteURI()
    return obj_uri.run()

@purchase.route(URL_PATH+'/'+SUBKEY+'/statistics', methods=['GET'])
def statistic():
    obj_uri = CStatisticURI()
    return obj_uri.run()

@purchase.route(URL_PATH+'/'+SUBKEY+'/payment', methods=['GET'])
def payment():
    obj_uri = CPaymentURI()
    return obj_uri.run()

@purchase.route(URL_PATH+'/'+SUBKEY+'/contract', methods=['GET'])
def contract():
    obj_uri = CContractURI()
    return obj_uri.run()

@purchase.route(URL_PATH+'/'+SUBKEY+'/arap', methods=['GET'])
def arap():
    obj_uri = CARAPURI()
    return obj_uri.run()