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
from sqlalchemy.orm import aliased
import uuid
from package.util.util import *

def recursive_sort(obj):
    if isinstance(obj, dict):
        return {k: recursive_sort(obj[k]) for k in sorted(obj)}
    elif isinstance(obj, list):
        return [recursive_sort(i) for i in obj]
    else:
        return obj

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


class CCompany(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0,'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                CTablePaidPayment = aliased(CTablePayment)
                CTableReceivedPayment = aliased(CTablePayment)
                n_total = (
                    obj_session.query(CTableCompany)
                    .filter(*lst_where)
                    .order_by(CTableCompany.no.asc())
                    .count()
                )
                n_start = 0
                n_count = 0
                if request.args.get('start') and request.args.get('count'):
                    n_start = int(request.args.get('start'))
                    n_count = int(request.args.get('count'))

                if n_count:
                    ids_query = (obj_session.query(
                                 CTableCompany.no)
                                 .filter(*lst_where)
                                 .order_by(CTableCompany.no.asc())
                                 .offset(n_start)
                                 .limit(n_count)
                                 )

                    ids = [id[0] for id in ids_query.all()]
                    lst_obj_result = (
                        obj_session.query(CTableCompany, CTablePaidPayment, CTableReceivedPayment)
                        .outerjoin(CTablePaidPayment, CTableCompany.paid_id == CTablePaidPayment.id)
                        .outerjoin(CTableReceivedPayment, CTableCompany.received_id == CTableReceivedPayment.id)
                        .filter(CTableCompany.no.in_(ids))
                        .order_by(CTableCompany.no.asc())
                        .all()
                    )
                else:
                    lst_obj_result = (
                        obj_session.query(CTableCompany, CTablePaidPayment, CTableReceivedPayment)
                        .filter(*lst_where)
                        .outerjoin(CTablePaidPayment, CTableCompany.paid_id == CTablePaidPayment.id)
                        .outerjoin(CTableReceivedPayment, CTableCompany.received_id == CTableReceivedPayment.id)
                        .order_by(CTableCompany.no.asc())
                        .all()
                    )
                if lst_obj_result:
                    lst_result = []

                    for obj_row in lst_obj_result:
                        dict_row = {'company': {},
                                    'paidPayment': {},
                                    'receivedPayment': {}}
                        if obj_row[0]:
                            dict_row['company'] = object_as_dict(obj_row[0])
                        if obj_row[1]:
                            dict_row['paidPayment'] = object_as_dict(obj_row[1])
                        if obj_row[2]:
                            dict_row['receivedPayment'] = object_as_dict(obj_row[2])
                        lst_result.append(dict_row)
                    if lst_result:
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
        lst_where = []
        return lst_where

