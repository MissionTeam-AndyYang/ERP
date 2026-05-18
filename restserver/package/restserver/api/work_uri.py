# coding=utf8
from flask import Blueprint
from .work import *
from .common import *
from .apibase import CAPIBase


SUBKEY = 'work'
work = Blueprint('work', __name__)


class CAssignmentURI(CAPIBase):

    def _get_executor(self):
        return CAssignment()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False

class CProcessOrderURI(CAPIBase):

    def _get_executor(self):
        return CProcessOrder()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False


class CProgressURI(CAPIBase):

    def _get_executor(self):
        return CProgress()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False

class CProductDataURI(CAPIBase):

    def _get_executor(self):
        return CProductData()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False

@work.route(URL_PATH+'/'+SUBKEY+'/assignment', methods=['GET'])
def assignment():
    obj_uri = CAssignmentURI()
    return obj_uri.run()


@work.route(URL_PATH+'/'+SUBKEY+'/process', methods=['GET', 'POST', 'PUT', 'DELETE'])
def process_order():
    obj_uri = CProcessOrderURI()
    return obj_uri.run()



@work.route(URL_PATH+'/'+SUBKEY+'/productdata', methods=['GET'])
def product_data():
    obj_uri = CProductDataURI()
    return obj_uri.run()

@work.route(URL_PATH+'/'+SUBKEY+'/progress', methods=['GET'])
def progress():
    obj_uri = CProgressURI()
    return obj_uri.run()
