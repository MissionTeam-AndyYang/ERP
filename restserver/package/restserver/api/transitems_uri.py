# coding=utf8
from flask import Blueprint
from .transitems import *
from .common import *
from .apibase import CAPIBase


SUBKEY = 'transitems'
transitems = Blueprint('transitems', __name__)

class CTransItemsURI(CAPIBase):

    def _get_executor(self):
        return CTransItems()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False

class CTransItemsItemURI(CAPIBase):

    def _get_executor(self):
        return CTransItemsItem()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False


@transitems.route(URL_PATH+'/'+SUBKEY, methods=['GET'])
def index():
    obj_uri = CTransItemsURI()
    return obj_uri.run()


@transitems.route(URL_PATH+'/'+SUBKEY+'/item', methods=['GET'])
def items():
    obj_uri = CTransItemsItemURI()
    return obj_uri.run()

