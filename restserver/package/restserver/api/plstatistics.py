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


class CManCapacity(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0,'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                n_start = int(request.args.get('start', 0))
                n_count = int(request.args.get('count', 0))
                obj_sort = CTablePLManCapacity.creationTime.asc()

                n_total, lst_obj_result = get_paginated_data(
                    obj_session,
                    CTablePLManCapacity,
                    lst_where,
                    obj_sort,
                    n_start,
                    n_count
                )
                if lst_obj_result:
                    lst_result = []
                    # retrieve warehouse count
                    for obj_row in lst_obj_result:
                        if obj_row:
                            dict_row = object_as_dict(obj_row)
                            dict_row["month"] = obj_row.month.strftime("%Y/%m")
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


    def __fill_query_params(self):
        lst_where = []
        return lst_where


class CItemCapacity(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0, 'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                n_start = int(request.args.get('start', 0))
                n_count = int(request.args.get('count', 0))
                obj_sort = CTablePLItemCapacity.creationTime.asc()

                n_total, lst_obj_result = get_paginated_data(
                    obj_session,
                    CTablePLItemCapacity,
                    lst_where,
                    obj_sort,
                    n_start,
                    n_count
                )
                if lst_obj_result:
                    lst_result = []
                    # retrieve warehouse count
                    for obj_row in lst_obj_result:
                        if obj_row:
                            dict_row = {"month": obj_row.month.strftime("%Y/%m"),
                                        "pl_no": obj_row.pl_no,
                                        "pl_name": obj_row.pl_name,
                                        "productCount": obj_row.productCount,
                                        "item_no": obj_row.item_no,
                                        "item_name": obj_row.item_name,
                                        "assembly_no": obj_row.assembly_no,
                                        "assemblyVer": obj_row.assemblyVer,
                                        "bomWeight": obj_row.bomWeight,
                                        "bomUnit": obj_row.bomUnit,
                                        "unit": obj_row.unit,
                                        "hourlyOutput": obj_row.hourlyOutput}

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

    def __fill_query_params(self):
        lst_where = []
        return lst_where


class CItemLoss(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0, 'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                n_start = int(request.args.get('start', 0))
                n_count = int(request.args.get('count', 0))
                obj_query_base = obj_session.query(CTablePLItemLoss).filter(*lst_where)
                n_total = obj_query_base.count()

                lst_filter = lst_where
                if n_count > 0:
                    ids_query = (obj_session.query(CTablePLItemLoss.no)
                                 .filter(*lst_where)
                                 .group_by(CTablePLItemLoss.no)
                                 .order_by(CTablePLItemLoss.creationTime.asc())
                                 .offset(n_start).limit(n_count).all())
                    lst_filter = [CTablePLItemLoss.no.in_([i[0] for i in ids_query])]
                lst_obj_result = (
                    obj_session.query(CTablePLItemLoss, CTablePLItemCapacity)
                    .outerjoin(CTablePLItemCapacity, CTablePLItemLoss.pl_item_capacity_no == CTablePLItemCapacity.no)
                    .filter(*lst_filter)
                    .group_by(CTablePLItemLoss.no)
                    .order_by(CTablePLItemLoss.creationTime.asc())
                    .all()
                )

                if lst_obj_result:
                    lst_result = []
                    # retrieve warehouse count
                    for obj_loss, obj_output in lst_obj_result:
                        if obj_loss:
                            dict_row = object_as_dict(obj_loss)
                            dict_row["month"] = obj_loss.month.strftime("%Y/%m")
                            dict_row["output"] = {}
                            if obj_output:
                                dict_row["output"]["pl_no"] = obj_output.pl_no
                                dict_row["output"]["pl_name"] = obj_output.pl_name
                                dict_row["output"]["productCount"] = obj_output.productCount
                                dict_row["output"]["item_no"] = obj_output.item_no
                                dict_row["output"]["item_name"] = obj_output.item_name
                                dict_row["output"]["assembly_no"] = obj_output.assembly_no
                                dict_row["output"]["assemblyVer"] = obj_output.assemblyVer
                                dict_row["output"]["bomWeight"] = obj_output.bomWeight
                                dict_row["output"]["bomUnit"] = obj_output.bomUnit
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

    def __fill_query_params(self):
        lst_where = []
        return lst_where



class CItemCost(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0, 'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                n_start = int(request.args.get('start', 0))
                n_count = int(request.args.get('count', 0))
                obj_sort = CTablePLItemCapacity.creationTime.asc()

                n_total, lst_obj_result = get_paginated_data(
                    obj_session,
                    CTablePLItemCapacity,
                    lst_where,
                    obj_sort,
                    n_start,
                    n_count
                )
                if lst_obj_result:
                    lst_result = []
                    # retrieve warehouse count
                    for obj_row in lst_obj_result:
                        if obj_row:
                            dict_row = {"month": obj_row.month.strftime("%Y/%m"),
                                        "pl_no": obj_row.pl_no,
                                        "pl_name": obj_row.pl_name,
                                        "productCount": obj_row.productCount,
                                        "item_no": obj_row.item_no,
                                        "item_name": obj_row.item_name,
                                        "assembly_no": obj_row.assembly_no,
                                        "assemblyVer": obj_row.assemblyVer,
                                        "price": obj_row.price,
                                        "rawMaterialCost": obj_row.rawMaterialCost,
                                        "materialCost": obj_row.materialCost,
                                        "laborCost": obj_row.laborCost}

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

    def __fill_query_params(self):
        lst_where = []
        return lst_where
