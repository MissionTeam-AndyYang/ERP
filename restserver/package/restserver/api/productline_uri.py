# coding=utf8
from flask import Blueprint
from .productline import *
from .common import *
from .apibase import CAPIBase


SUBKEY = 'productline'
productline = Blueprint('productline', __name__)

class CProcessURI(CAPIBase):

    def _get_executor(self):
        return CProcess()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False

class CProductLineURI(CAPIBase):

    def _get_executor(self):
        return CProductLine()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False

class CStationURI(CAPIBase):

    def _get_executor(self):
        return CStation()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False

class CEquipmentURI(CAPIBase):

    def _get_executor(self):
        return CEquipment()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False

class CFactoryURI(CAPIBase):

    def _get_executor(self):
        return CFactory()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False

@productline.route(URL_PATH+'/'+SUBKEY+'/process', methods=['GET', 'POST', 'PUT', 'DELETE'])
def process():
    obj_uri = CProcessURI()
    return obj_uri.run()

@productline.route(URL_PATH+'/'+SUBKEY, methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():
    obj_uri = CProductLineURI()
    return obj_uri.run()


@productline.route(URL_PATH+'/'+SUBKEY+'/station', methods=['GET', 'POST', 'PUT', 'DELETE'])
def station():
    obj_uri = CStationURI()
    return obj_uri.run()

@productline.route(URL_PATH+'/'+SUBKEY+'/equipment', methods=['GET', 'POST', 'PUT', 'DELETE'])
def equipment():
    obj_uri = CEquipmentURI()
    return obj_uri.run()

@productline.route(URL_PATH+'/'+SUBKEY+'/factory', methods=['GET', 'POST', 'PUT', 'DELETE'])
def factory():
    obj_uri = CFactoryURI()
    return obj_uri.run()
