# coding=utf8
from flask import Blueprint
from .shipwarehouse import *
from .common import *
from .apibase import CAPIBase

SUBKEY = 'shipwarehouse'
shipwarehouse = Blueprint('shipwarehouse', __name__)


class  CShipWarehouseURI(CAPIBase):

    def _get_executor(self):
        return CShipWarehouse()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False


class CShipWarehouseContractURI(CAPIBase):

    def _get_executor(self):
        return CShipWarehouseContract()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False


class CShippingRecURI(CAPIBase):

    def _get_executor(self):
        return CShippingRec()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False


class CShippingPaymentURI(CAPIBase):

    def _get_executor(self):
        return CShipPayment()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

class CShippingARAPURI(CAPIBase):

    def _get_executor(self):
        return CShipARAP()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

class CWarehouseRecURI(CAPIBase):

    def _get_executor(self):
        return CWarehouseRec()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False


class CWarehousePaymentURI(CAPIBase):

    def _get_executor(self):
        return CWarehousePayment()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

class CWarehouseARAPURI(CAPIBase):

    def _get_executor(self):
        return CWarehouseARAP()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

@shipwarehouse.route(URL_PATH + '/' + SUBKEY, methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():
    obj_uri = CShipWarehouseURI()
    return obj_uri.run()


@shipwarehouse.route(URL_PATH + '/' + SUBKEY + '/contract' , methods=['GET', 'POST', 'PUT', 'DELETE'])
def contract():
    obj_uri = CShipWarehouseContractURI()
    return obj_uri.run()

@shipwarehouse.route(URL_PATH + '/' + SUBKEY + '/shiprec' , methods=['GET', 'POST', 'PUT', 'DELETE'])
def shippingRec():
    obj_uri = CShippingRecURI()
    return obj_uri.run()


@shipwarehouse.route(URL_PATH + '/' + SUBKEY + '/shippayment' , methods=['GET', 'POST', 'PUT', 'DELETE'])
def shippingPayment():
    obj_uri = CShippingPaymentURI()
    return obj_uri.run()


@shipwarehouse.route(URL_PATH + '/' + SUBKEY + '/shiparap' , methods=['GET'])
def shippingARAP():
    obj_uri = CShippingARAPURI()
    return obj_uri.run()

@shipwarehouse.route(URL_PATH + '/' + SUBKEY + '/warehouserec' , methods=['GET', 'POST', 'PUT', 'DELETE'])
def warehouseRec():
    obj_uri = CWarehouseRecURI()
    return obj_uri.run()


@shipwarehouse.route(URL_PATH + '/' + SUBKEY + '/warehousepayment' , methods=['GET', 'POST', 'PUT', 'DELETE'])
def warehousePayment():
    obj_uri = CWarehousePaymentURI()
    return obj_uri.run()


@shipwarehouse.route(URL_PATH + '/' + SUBKEY + '/warehousearap' , methods=['GET'])
def warehouseARAP():
    obj_uri = CWarehouseARAPURI()
    return obj_uri.run()
