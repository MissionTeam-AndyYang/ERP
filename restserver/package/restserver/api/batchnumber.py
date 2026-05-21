# coding=utf8
import pytz
import json
import string
import validictory
from copy import deepcopy
from flask import request
from .util import *
from package.common.common import *
from package.log.log import CLogger
from package.dbwrapper.table import *
from package.dbwrapper.dbmgr import CDBMgr
from sqlalchemy import delete
import uuid
from package.util.util import *
from package.batchno.batchno import *

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


class CBatchNumber(CPrivilegeControl):

    INFO_SERIALNO = 1
    TYPE_STOCK = 0
    TYPE_NEAREXPIRY= 1
    TYPE_EXPIRED = 2
    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0,'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                n_total = (
                    obj_session.query(CTableBatchNumber)
                    .filter(*lst_where)
                    .order_by(CTableBatchNumber.date.desc())
                    .count()
                )

                n_start = 0
                n_count = 0
                if request.args.get('start') and request.args.get('count'):
                    n_start = int(request.args.get('start'))
                    n_count = int(request.args.get('count'))

                if n_count:
                    ids_query = (obj_session.query(
                                 CTableBatchNumber.no)
                                 .filter(*lst_where)
                                 .order_by(CTableBatchNumber.date.desc())
                                 .offset(n_start)
                                 .limit(n_count)
                                 )

                    ids = [no[0] for no in ids_query.all()]
                    lst_obj_result = (
                        obj_session.query(CTableBatchNumber)
                        .filter(CTableBatchNumber.no.in_(ids))
                        .order_by(CTableBatchNumber.date.desc())
                        .all()
                    )
                    print("")

                else:
                    lst_obj_result = (
                        obj_session.query(CTableBatchNumber)
                        .filter(*lst_where)
                        .order_by(CTableBatchNumber.date.desc())
                        .all()
                    )

                if lst_obj_result:
                    lst_result = []
                    # retrieve inventory count
                    for obj_row in lst_obj_result:
                        if obj_row:
                            _, n_subCategory, _ = get_item_info(obj_row.item_no)
                            dict_row = object_as_dict(obj_row)
                            dict_row["itemSubCategory"] = n_subCategory
                            # 判斷是否為過期品
                            dict_row["stockType"] = self.__get_stock_type(dict_row["validDays"], dict_row["validDate"])
                            if request.args.get('type') and int( request.args.get('type')) == self.INFO_SERIALNO:
                                dict_row["serialNo"] = []
                                if obj_row.serialNo_data:
                                    for obj_serial in obj_row.serialNo_data:
                                        dict_row["serialNo"].append({"serialNo":  obj_serial.serialNo,
                                                                     "count":  obj_serial.count})
                                else:
                                    dict_row["serialNo"].append({"serialNo": "",
                                                                 "count": obj_row.checkedCount})
                            if request.args.get('info'):
                                retrieve_warehouse_info(obj_session, dict_row["itemCategory"], obj_row, dict_row)
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

    def post(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}

        return n_status_code, n_code, str_message, dict_extra_data


    def put(self, str_timezone='', str_id=''):
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


    def __fill_query_params(self):
        lst_where = []
        if request.args.get('item_ref_no'):
            lst_where.append(CTableBatchNumber.item_ref_no == request.args.get('item_ref_no'))
        if request.args.get('item_no'):
            lst_where.append(CTableBatchNumber.item_no == request.args.get('item_no'))
        if request.args.get('no'):
            lst_where.append(CTableBatchNumber.no == request.args.get('no'))
        if request.args.get('category'):
            str_param = request.args.get('category')
            lst_category = str_param.split(',') if str_param else []
            #lst_where.append(CTableBatchNumber.refCategory == int(request.args.get('category')))
            lst_where.append(CTableBatchNumber.refCategory.in_(lst_category))
        return lst_where

    def __get_stock_type(self, n_validDays, n_validDate):
        n_type = self.TYPE_STOCK
        n_now = util_retrieve_now_time()
        if n_validDate:
            if (n_validDate - n_now) < 0:
                n_type = self.TYPE_EXPIRED #過期
            else:
                if (n_validDate - n_now) <= n_validDays:  # 86400/3 轉換成秒再取三分之一
                    n_type = self.TYPE_NEAREXPIRY #即期
        return n_type

