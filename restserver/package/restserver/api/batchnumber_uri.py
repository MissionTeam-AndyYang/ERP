# coding=utf8
from flask import Blueprint
from .batchnumber import *
from .common import *
from .apibase import CAPIBase

SUBKEY = 'batchnumber'
batchnumber = Blueprint('batchnumber', __name__)


class CBatchNumberURI(CAPIBase):

    def _get_executor(self):
        return CBatchNumber()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False




@batchnumber.route(URL_PATH + '/' + SUBKEY, methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():
    obj_uri = CBatchNumberURI()
    return obj_uri.run()

