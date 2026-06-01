# coding=utf8
from flask import Blueprint
from .product import *
from .common import *
from .apibase import CAPIBase


SUBKEY = 'product'
product = Blueprint('product', __name__)

class CProductURI(CAPIBase):

    def _get_executor(self):
        return CProduct()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False


@product.route(URL_PATH+'/'+SUBKEY, methods=['GET'])
def index():
    obj_uri = CProductURI()
    return obj_uri.run()

