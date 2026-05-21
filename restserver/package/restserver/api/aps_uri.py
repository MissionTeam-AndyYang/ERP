# coding=utf8
from flask import Blueprint
from .aps import *
from .common import *
from .apibase import CAPIBase


SUBKEY = 'aps'
aps = Blueprint('aps', __name__)

'''
class CMaterialsURI(CAPIBase):

    def _get_executor(self):
        return CMaterials()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False


class CLaborURI(CAPIBase):

    def _get_executor(self):
        return CLabor()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False


class CQuantityItemURI(CAPIBase):

    def _get_executor(self):
        return CQuantityItem()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

'''

class CQuantityURI(CAPIBase):

    def _get_executor(self):
        return CQuantity()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False


'''
@aps.route(URL_PATH+'/'+SUBKEY+'/quantitydata', methods=['GET'])
def materials():
    obj_uri = CMaterialsURI()
    return obj_uri.run()

@aps.route(URL_PATH+'/'+SUBKEY+'/labor', methods=['PUT'])
def labor():
    obj_uri = CLaborURI()
    return obj_uri.run()

@aps.route(URL_PATH+'/'+SUBKEY+'/quantityitem', methods=['GET', 'PUT'])
def quantityitem():
    obj_uri = CQuantityItemURI()
    return obj_uri.run()
'''

@aps.route(URL_PATH+'/'+SUBKEY+'/quantity', methods=['GET'])
def quantity():
    obj_uri = CQuantityURI()
    return obj_uri.run()


