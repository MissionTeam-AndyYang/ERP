# coding=utf8
from flask import Blueprint
from .goods import *
from .common import *
from .apibase import CAPIBase


SUBKEY = 'goods'
goods = Blueprint('goods', __name__)

class CGoodsURI(CAPIBase):

    def _get_executor(self):
        return CGoods()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False


@goods.route(URL_PATH+'/'+SUBKEY, methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():
    obj_uri = CGoodsURI()
    return obj_uri.run()

