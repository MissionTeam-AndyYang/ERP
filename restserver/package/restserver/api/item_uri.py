# coding=utf8
from flask import Blueprint
from .item import *
from .common import *
from .apibase import CAPIBase

SUBKEY = 'item'
item = Blueprint('item', __name__)


class CItemURI(CAPIBase):

    def _get_executor(self):
        return CItemData()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

    def _is_reset_alive_time(self):
        return True
class CGroupURI(CAPIBase):

    def _get_executor(self):
        return CItemDataGroup()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

    def _is_reset_alive_time(self):
        return True
class CPurchaseURI(CAPIBase):

    def _get_executor(self):
        return CPurchase()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

    def _is_reset_alive_time(self):
        return True
class CManufactureURI(CAPIBase):

    def _get_executor(self):
        return CManufacture()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

    def _is_reset_alive_time(self):
        return True
class CSalesURI(CAPIBase):

    def _get_executor(self):
        return CSales()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

    def _is_reset_alive_time(self):
        return True



class COtherURI(CAPIBase):

    def _get_executor(self):
        return COther()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

    def _is_reset_alive_time(self):
        return True

class CInfoURI(CAPIBase):

    def _get_executor(self):
        return CInfo()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

    def _is_reset_alive_time(self):
        return True


class CGroupInfoURI(CAPIBase):

    def _get_executor(self):
        return CGroupInfo()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

    def _is_reset_alive_time(self):
        return True


@item.route(URL_PATH_DEVICE + '/' + SUBKEY + '/data', methods=['POST'])
def data():
    obj_uri = CItemURI()
    return obj_uri.run()

@item.route(URL_PATH_DEVICE + '/' + SUBKEY + '/data/group', methods=['GET','POST'])
def group():
    obj_uri = CGroupURI()
    return obj_uri.run()

@item.route(URL_PATH_DEVICE + '/' + SUBKEY + '/purchase', methods=['GET'])
def purchase():
    obj_uri = CPurchaseURI()
    return obj_uri.run()


@item.route(URL_PATH_DEVICE + '/' + SUBKEY + '/manufacture', methods=['GET'])
def manufacture():
    obj_uri = CManufactureURI()
    return obj_uri.run()


@item.route(URL_PATH_DEVICE + '/' + SUBKEY + '/sales', methods=['GET'])
def sales():
    obj_uri = CSalesURI()
    return obj_uri.run()


@item.route(URL_PATH_DEVICE + '/' + SUBKEY + '/other', methods=['GET'])
def other():
    obj_uri = COtherURI()
    return obj_uri.run()


@item.route(URL_PATH_DEVICE + '/' + SUBKEY + '/info', methods=['GET'])
def info():
    obj_uri = CInfoURI()
    return obj_uri.run()


@item.route(URL_PATH_DEVICE + '/' + SUBKEY + '/groupInfo', methods=['GET'])
def groupInfo():
    obj_uri = CGroupInfoURI()
    return obj_uri.run()
