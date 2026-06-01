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
from .util import *
from sqlalchemy import func, cast, Numeric, case
from package.contract.contract import CContract


class CPrivilegeControl(object):

    def is_allowed_for_get(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.SALE and privilege['action'] in (EPrivilegeAction.VIEW, EPrivilegeAction.REPORT)
                   for privilege in lst_privileges)

    def is_allowed_for_post(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.SALE and privilege['action'] == EPrivilegeAction.CREATION
                   for privilege in lst_privileges)

    def is_allowed_for_put(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.SALE and privilege['action'] == EPrivilegeAction.MODIFICATION
                   for privilege in lst_privileges)

    def is_allowed_for_delete(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.SALE and privilege['action'] == EPrivilegeAction.CANCELLATION
                   for privilege in lst_privileges)



class CAPIContract(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'results': []}
        try:
            n_total = 0
            lst_result = []
            n_start = int(request.args.get('start', 0))
            n_count = int(request.args.get('count', 0))
            dict_where = self.__fill_query_params()
            str_type = request.args.get('type', '')
            lst_type = []
            if ',' in str_type:
                # 如果有逗號，解析成 list
                lst_type = [int(str_value) for str_value in str_type.split(',') if str_value.strip().isdigit()]
            else:

                lst_type = [int(str_type)] if str_type.isdigit() else []
            for n_type in lst_type:
                n_total1, lst_result1 = CContract(n_type).get(n_start, n_count, dict_where)
                n_total += n_total1
                lst_result.extend(lst_result1)
            dict_extra_data['total'] = n_total
            dict_extra_data['count'] = len(lst_result)
            dict_extra_data['results'] = lst_result
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def __fill_query_params(self):
        dict_where = {}
        if request.args.get('start_time') and request.args.get('end_time'):
            # get the range of timestamp
            n_start = util_convert_timestamp_to_date(int(request.args.get('start_time')))
            if int(request.args.get('start_time')) == int(request.args.get('end_time')):
                n_end = util_convert_timestamp_to_date(n_start, 1) - 1
            else:
                n_end = util_convert_timestamp_to_date(int(request.args.get('end_time')), 1) - 1
            dict_where['start_time'] = n_start
            dict_where['end_time'] = n_end

        if request.args.get('item_no'):
            dict_where['item_no'] = request.args.get('item_no')

        if request.args.get('category'):
            dict_where['category'] = int(request.args.get('category'))

        if request.args.get('itemStyle'):
            dict_where['itemStyle'] = [int(request.args.get('itemStyle'))]
        return dict_where