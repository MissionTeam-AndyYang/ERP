# coding=utf8
from flask import Blueprint
from .material import *
from .common import *
from .apibase import CAPIBase


SUBKEY = 'material'
material = Blueprint('material', __name__)

class CMaterialURI(CAPIBase):

    def _get_executor(self):
        return CMaterial()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False


class CItemPriceURI(CAPIBase):

    def _get_executor(self):
        return CItemPrice()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False



@material.route(URL_PATH+'/'+SUBKEY, methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():
    obj_uri = CMaterialURI()
    return obj_uri.run()


@material.route(URL_PATH + '/' + SUBKEY + '/itemprice' , methods=['GET'])
def price():
    obj_uri = CItemPriceURI()
    return obj_uri.run()

