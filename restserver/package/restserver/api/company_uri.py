# coding=utf8
from flask import Blueprint
from .company import *
from .common import *
from .apibase import CAPIBase

SUBKEY = 'company'
company = Blueprint('company', __name__)


class CCompanyURI(CAPIBase):

    def _get_executor(self):
        return CCompany()

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False


@company.route(URL_PATH + '/' + SUBKEY, methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():
    obj_uri = CCompanyURI()
    return obj_uri.run()
