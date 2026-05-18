# coding=utf8
from flask import Blueprint
from .heartbeat import *
from .common import *
from .apibase import CAPIBase

SUBKEY = 'heartbeat'
heartbeat = Blueprint('heartbeat', __name__)


class CHeartbeatURI(CAPIBase):

    def _get_executor(self):
        return CHeartbeat()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

    def _is_vaildate_token(self):
        return False

    def _is_reset_alive_time(self):
        return False


@heartbeat.route(URL_PATH_DEVICE + '/' + SUBKEY, methods=['GET'])
def index():
    obj_uri = CHeartbeatURI()
    return obj_uri.run()
