# coding=utf8
from flask import Blueprint
from .mix import *
from .common import *
from .apibase import CAPIBase

SUBKEY = 'mix'
mix = Blueprint('mix', __name__)


class CMixItemURI(CAPIBase):

    def _get_executor(self):
        return CMixItem()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

class CItemPriceURI(CAPIBase):

    def _get_executor(self):
        return CItemPrice()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False


@mix.route(URL_PATH + '/' + SUBKEY + '/item', methods=['GET'])
def mixitem():
    obj_uri = CMixItemURI()
    return obj_uri.run()

@mix.route(URL_PATH + '/' + SUBKEY + '/itemprice' , methods=['GET'])
def price():
    obj_uri = CItemPriceURI()
    return obj_uri.run()