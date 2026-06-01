# coding=utf8
from flask import Blueprint
from .aps import *
from .common import *
from .apibase import CAPIBase


SUBKEY = 'aps'
aps = Blueprint('aps', __name__)

class CQuantityURI(CAPIBase):

    def _get_executor(self):
        return CQuantity()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False


@aps.route(URL_PATH+'/'+SUBKEY+'/quantity', methods=['GET'])
def quantity():
    obj_uri = CQuantityURI()
    return obj_uri.run()


