# coding=utf8
from flask import Blueprint
from .enterprise import *
from .common import *
from .apibase import CAPIBase

SUBKEY = 'enterprise'
enterprise = Blueprint('enterprise', __name__)


class CEnterpriseURI(CAPIBase):

    def _get_executor(self):
        return CEnterprise()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False


@enterprise.route(URL_PATH + '/' + SUBKEY, methods=['GET'])
def index():
    obj_uri = CEnterpriseURI()
    return obj_uri.run()
