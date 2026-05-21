# coding=utf8
from flask import Blueprint
from .batchtrace import *
from .common import *
from .apibase import CAPIBase

SUBKEY = 'batchtrace'
batchtrace = Blueprint('batchtrace', __name__)


class CBatchTraceURI(CAPIBase):

    def _get_executor(self):
        return CBatchTrace()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

class CBatchRecordURI(CAPIBase):

    def _get_executor(self):
        return CBatchRecord()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False




@batchtrace.route(URL_PATH + '/' + SUBKEY, methods=['GET'])
def index():
    obj_uri = CBatchTraceURI()
    return obj_uri.run()

@batchtrace.route(URL_PATH + '/' + SUBKEY + '/record', methods=['GET'])
def record():
    obj_uri = CBatchRecordURI()
    return obj_uri.run()