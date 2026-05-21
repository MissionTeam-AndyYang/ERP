# coding=utf8
from flask import Blueprint
from .quotation import *
from .common import *
from .apibase import CAPIBase


SUBKEY = 'quotation'
quotation = Blueprint('quotation', __name__)

class CQuotationURI(CAPIBase):

    def _get_executor(self):
        return CAPIQuotation()

    def _is_vaildate_param(self):
        return True if not self._is_get_method() else False



@quotation.route(URL_PATH+'/'+SUBKEY, methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():
    obj_uri = CQuotationURI()
    return obj_uri.run()

