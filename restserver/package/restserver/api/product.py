# coding=utf8
import pytz
import json
import string
import validictory
from copy import deepcopy
from flask import request
from package.util.util import *
from package.common.common import *
from package.log.log import CLogger
from package.dbwrapper.table import *
from package.dbwrapper.dbmgr import CDBMgr
from sqlalchemy import func, cast, Numeric
from .util import *

class CPrivilegeControl(object):

    def is_allowed_for_get(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.PURCHASE and privilege['action'] in (EPrivilegeAction.VIEW, EPrivilegeAction.REPORT)
                   for privilege in lst_privileges)

    def is_allowed_for_post(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.PURCHASE and privilege['action'] == EPrivilegeAction.CREATION
                   for privilege in lst_privileges)

    def is_allowed_for_put(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.PURCHASE and privilege['action'] == EPrivilegeAction.MODIFICATION
                   for privilege in lst_privileges)

    def is_allowed_for_delete(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.PURCHASE and privilege['action'] == EPrivilegeAction.CANCELLATION
                   for privilege in lst_privileges)


class CProduct(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0, 'results': []}

        try:
            n_start = 0
            n_count = 0
            n_total = 0
            if request.args.get('start') and request.args.get('count'):
                n_start = int(request.args.get('start'))
                n_count = int(request.args.get('count'))

            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                obj_query = obj_session.query(
                    CTableProduct
                )
                obj_query = self.__fill_query_params(obj_query)

                n_total = (
                    obj_query
                    .order_by(CTableProduct.no.desc())
                    .count()
                )

                if n_count:
                    lst_obj_result = (
                        obj_query
                        .order_by(CTableProduct.no.desc())
                        .offset(n_start)
                        .limit(n_count)
                        .all()
                    )
                else:
                    lst_obj_result = (
                        obj_query
                        .order_by(CTableProduct.no.desc())
                        .all()
                    )

                if lst_obj_result:
                    lst_result = []

                    for obj_row in lst_obj_result:
                        dict_row = {}
                        if obj_row:
                            dict_row = object_as_dict(obj_row)
                        lst_result.append(dict_row)
                    if lst_result:
                        dict_extra_data['total'] = n_total
                        dict_extra_data['count'] = len(lst_obj_result)
                        dict_extra_data['results'] = lst_result
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def post(self, str_timezone='' , str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}

        return n_status_code, n_code, str_message, dict_extra_data

    def put(self, str_timezone='' , str_id=''):
        dict_param = {}
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        dict_schema = {'type': 'object',
                       'properties': {}}


        return n_status_code, n_code, str_message, dict_extra_data

    def delete(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}

        return n_status_code, n_code, str_message, dict_extra_data

    def __fill_query_params(self, obj_query):
        dict_where = {}

        # setting  find conditions from query parameter
        #if request.args.get('customer_no'):
        #    dict_where['customer_no'] = request.args.get('customer_no')

        if request.args.get('product_no'):
            dict_where['no'] = request.args.get('product_no')

        for key, value in dict_where.items():
            obj_query = obj_query.filter(getattr(CTableProduct, key) == value)

        return obj_query
