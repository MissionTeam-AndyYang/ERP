# coding=utf8
from flask import Blueprint
from .bankaccount import *
from .common import *
from .apibase import CAPIBase


SUBKEY = 'bankaccount'
bankaccount = Blueprint('bankaccount', __name__)

class CBankAccountURI(CAPIBase):

    def _get_executor(self):
        return CBankAccount()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False


@bankaccount.route(URL_PATH+'/'+SUBKEY, methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():
    obj_uri = CBankAccountURI()
    return obj_uri.run()

