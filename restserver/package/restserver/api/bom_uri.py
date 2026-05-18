# coding=utf8
from flask import Blueprint
from .bom import *
from .common import *
from .apibase import CAPIBase


SUBKEY = 'bom'
bom = Blueprint('bom', __name__)

class CBomAPSURI(CAPIBase):

    def _get_executor(self):
        return CBomAPS()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False

class CBomTreeURI(CAPIBase):

    def _get_executor(self):
        return CBomTree()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False

class CBomURI(CAPIBase):

    def _get_executor(self):
        return CBom()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False


class CProductProcessURI(CAPIBase):

    def _get_executor(self):
        return CProductProcess()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

@bom.route(URL_PATH+'/'+SUBKEY, methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():
    obj_uri = CBomURI()
    return obj_uri.run()



@bom.route(URL_PATH+'/'+SUBKEY+'/tree', methods=['GET'])
def tree():
    obj_uri = CBomTreeURI()
    return obj_uri.run()


@bom.route(URL_PATH+'/'+SUBKEY+'/process', methods=['GET'])
def process():
    obj_uri = CProductProcessURI()
    return obj_uri.run()

@bom.route(URL_PATH+'/'+SUBKEY+'/aps', methods=['GET'])
def APS():
    obj_uri = CBomAPSURI()
    return obj_uri.run()