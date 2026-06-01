# coding=utf8
from flask import Blueprint
from .contract import *
from .common import *
from .apibase import CAPIBase


SUBKEY = 'contract'
contract = Blueprint('contract', __name__)

class CContractURI(CAPIBase):

    def _get_executor(self):
        return CAPIContract()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False



@contract.route(URL_PATH+'/'+SUBKEY, methods=['GET'])
def index():
    obj_uri = CContractURI()
    return obj_uri.run()

