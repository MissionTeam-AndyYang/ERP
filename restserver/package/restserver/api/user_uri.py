# coding=utf8
from flask import Blueprint
from .user import *
from .common import *
from .apibase import CAPIBase

SUBKEY = 'user'
user = Blueprint('user', __name__)

class CLoginURI(CAPIBase):

    def _get_executor(self):
        return CLogin()

    def _is_vaildate_token(self):
        return False if self._is_post_method() else True

    def _is_reset_alive_time(self):
        return False


class CDeviceLoginURI(CAPIBase):

    def _get_executor(self):
        return CDeviceLogin()

    def _is_vaildate_token(self):
        return False if self._is_post_method() else True

    def _is_reset_alive_time(self):
        return False


class CDeviceLogoutURI(CAPIBase):

    def _get_executor(self):
        return CDeviceLogout()

    def _is_vaildate_token(self):
        return False if self._is_post_method() else True

    def _is_reset_alive_time(self):
        return False


@user.route(URL_PATH+'/'+SUBKEY+'/login', methods=['POST', 'DELETE'])
def login():
    obj_uri = CLoginURI()
    return obj_uri.run()


@user.route(URL_PATH_DEVICE+ '/' +SUBKEY+'/device/login', methods=['POST'])
def device_login():
    obj_uri = CDeviceLoginURI()
    return obj_uri.run()


@user.route(URL_PATH_DEVICE+ '/' +SUBKEY+'/device/logout', methods=['DELETE'])
def device_logout():
    obj_uri = CDeviceLogoutURI()
    return obj_uri.run()
