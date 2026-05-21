# coding=utf8
from flask import Blueprint
from .device import *
from .common import *
from .apibase import CAPIBase

SUBKEY = 'device'
device = Blueprint('device', __name__)


class CDeviceURI(CAPIBase):

    def _get_executor(self):
        return CDevice()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

    def _is_vaildate_token(self):
        return False

    def _is_reset_alive_time(self):
        return False



@device.route(URL_PATH_DEVICE + '/' + SUBKEY + '/register', methods=['POST'])
def index():
    obj_uri = CDeviceURI()
    return obj_uri.run()
