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
from sqlalchemy.orm import aliased

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


class CTransItems(CPrivilegeControl):
    TYPE1 = 1  # 貨品材料產品
    TYPE2 = 2  # 耗品設備工程其他

    CATEGORY1 = 1  # 耗品設備
    CATEGORY2 = 2  # 工程其他
    CATEGORY3 = 3  # 雜項
    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0, 'results': []}

        try:
            n_start = 0
            n_count = 0
            CTablePaidPayment = aliased(CTablePayment)
            CTableReceivedPayment = aliased(CTablePayment)

            if request.args.get('start') and request.args.get('count'):
                n_start = int(request.args.get('start'))
                n_count = int(request.args.get('count'))

            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()

                n_type = int(request.args.get('type', self.TYPE1))
                n_category = int(request.args.get("category", 0))
                obj_table = CTableTransItems2 if n_type == self.TYPE2 else CTableTransItems
                query = self.__fill_query_params(obj_session.query(obj_table))

                if n_type == 2:
                    # 使用字典簡化分類邏輯
                    dict_category_map = {1: [1, 2], 2: [3, 4], 3: [5]}
                    lst_category = dict_category_map.get(n_category, [1, 2])
                    query = query.filter(obj_table.category.in_(lst_category))
                n_total = query.count()
                query = (
                    query.add_entity(CTableCompany)
                    .add_entity(CTablePaidPayment)
                    .add_entity(CTableReceivedPayment)
                    .outerjoin(CTableCompany, obj_table.company_no == CTableCompany.no)
                    .outerjoin(CTablePaidPayment, CTableCompany.paid_id == CTablePaidPayment.id)
                    .outerjoin(CTableReceivedPayment, CTableCompany.received_id == CTableReceivedPayment.id)
                    .order_by(obj_table.category.desc())
                )

                if n_count > 0:
                    query = query.offset(n_start).limit(n_count)
                lst_obj_result = query.all()
                if lst_obj_result:
                    lst_result = []

                    for obj_row in lst_obj_result:
                        dict_row = {"item": {}, "paidPayment":{}, "receivedPayment":{}}
                        if obj_row:
                            dict_row["item"] = object_as_dict(obj_row[0]) if obj_row[0] else {}
                            if dict_row["item"].get("item_no", ""):
                                _, n_category, n_subCategory, n_unitWarehouse, _ = util_new_get_item_info(obj_row[0].item_no if obj_row[0] else "")
                                dict_row["item"]["itemCategory"] = n_category
                                dict_row["item"]["itemSubCategory"] = n_subCategory
                                dict_row["item"]["itemUnit"] = n_unitWarehouse

                            #dict_row['paidPayment'] = object_as_dict(obj_row[2]) if obj_row[2] else {}
                            #dict_row['receivedPayment'] = object_as_dict(obj_row[3]) if obj_row[3] else {}

                            dict_row2 = object_as_dict(obj_row[2]) if obj_row[2] else {}
                            dict_row['paidPayment']["paymentType"] = dict_row2.get("type", 0)
                            dict_row['paidPayment']["paymentDate"] = dict_row2.get("date", 0)
                            dict_row['paidPayment']["paymentPeriod"] = dict_row2.get("period", 0)

                            dict_row3 = object_as_dict(obj_row[3]) if obj_row[3] else {}
                            dict_row['receivedPayment']["paymentType"] = dict_row3.get("type", 0)
                            dict_row['receivedPayment']["paymentDate"] = dict_row3.get("date", 0)
                            dict_row['receivedPayment']["paymentPeriod"] = dict_row3.get("period", 0)
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

        return obj_query


class CTransItems2(CPrivilegeControl):

    CATEGORY1 = 1  # 耗品設備
    CATEGORY2 = 2  # 工程其他
    CATEGORY3 = 3  # 雜項

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0, 'results': []}

        try:
            n_start = 0
            n_count = 0
            CTablePaidPayment = aliased(CTablePayment)
            CTableReceivedPayment = aliased(CTablePayment)
            n_type = int(request.args.get("category", 0))
            obj_TableTransItem = CTableTransItems2 if n_type == self.TYPE2 else CTableTransItems

            if request.args.get('start') and request.args.get('count'):
                n_start = int(request.args.get('start'))
                n_count = int(request.args.get('count'))

            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                n_type =  int(request.args.get('category', 0))
                if n_type == 1:
                    lst_category = [1, 2]
                elif n_type == 2:
                    lst_category = [ 3,4 ]
                elif n_type == 3:
                    lst_category = [5]
                else:
                    lst_category = [1,2]
                obj_query = self.__fill_query_params(obj_session.query(CTableTransItems2))
                n_total = obj_query.count()

                final_query = (
                    obj_query
                    .add_entity(CTableCompany)
                    .add_entity(CTablePaidPayment)
                    .add_entity(CTableReceivedPayment)
                    .filter(CTableTransItems2.category.in_(lst_category))
                    .outerjoin(CTableCompany, CTableTransItems2.company_no == CTableCompany.no)
                    .outerjoin(CTablePaidPayment, CTableCompany.paid_id == CTablePaidPayment.id)
                    .outerjoin(CTableReceivedPayment, CTableCompany.received_id == CTableReceivedPayment.id)
                    .order_by(CTableTransItems2.category.desc())
                )
                if n_count:
                    final_query = final_query.offset(n_start).limit(n_count)

                lst_obj_result = final_query.all()
                if lst_obj_result:
                    lst_result = []

                    for obj_row in lst_obj_result:
                        dict_row = {"item":{}, "company":{}, "paidPayment":{}, "receivedPayment":{}}
                        if obj_row:
                            dict_row["item"] = object_as_dict(obj_row[0]) if obj_row[0] else {}
                            _, n_category, n_subCategory, n_unitWarehouse, _ = util_new_get_item_info(obj_row[0].item_no if obj_row[0] else "")
                            dict_row["item"]["itemCategory"] = n_category
                            dict_row["item"]["itemSubCategory"] = n_subCategory
                            dict_row["item"]["itemUnit"] = n_unitWarehouse
                            dict_row["company"] = object_as_dict(obj_row[1]) if obj_row[1] else {}
                            dict_row['paidPayment'] = object_as_dict(obj_row[2]) if obj_row[2] else {}
                            dict_row['receivedPayment'] = object_as_dict(obj_row[3]) if obj_row[3] else {}
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

        return obj_query
class CTransItemsItem(CPrivilegeControl):
    TYPE1 = 1 # 貨品材料產品
    TYPE2 = 2 # 耗品設備工程其他
    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0, 'results': []}
        if not request.args.get("item_no"):
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'invalid parameter'
        else:
            try:
                CTablePaidPayment = aliased(CTablePayment)
                CTableReceivedPayment = aliased(CTablePayment)
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    lst_obj_result = (
                        obj_session.query(CTableTransItems, CTableCompany, CTablePaidPayment, CTableReceivedPayment)
                        .filter(CTableTransItems.item_no == request.args.get("item_no"))
                        .outerjoin(CTableCompany, CTableTransItems.company_no == CTableCompany.no)
                        .outerjoin(CTablePaidPayment, CTableCompany.paid_id == CTablePaidPayment.id)
                        .outerjoin(CTableReceivedPayment, CTableCompany.received_id == CTableReceivedPayment.id)
                        .all()
                    )

                    if lst_obj_result:
                        lst_result = []

                        for obj_row in lst_obj_result:
                            dict_row = {'transItem': {},
                                        'paidPayment': {},
                                        'receivedPayment': {}}
                            if obj_row:
                                if obj_row[0]:
                                    dict_row['transItem'] = object_as_dict(obj_row[0])
                                    _, n_category, n_subCategory, n_unitWarehouse, _ = util_new_get_item_info(
                                        dict_row['transItem']["item_no"])
                                    dict_row['transItem']["itemCategory"] = n_category
                                    dict_row['transItem']["itemSubCategory"] = n_subCategory
                                    dict_row['transItem']["itemUnit"] = n_unitWarehouse
                                if obj_row[2]:
                                    dict_row['paidPayment'] = object_as_dict(obj_row[2])
                                if obj_row[3]:
                                    dict_row['receivedPayment'] = object_as_dict(obj_row[3])
                            lst_result.append(dict_row)
                        if lst_result:
                            dict_extra_data['total'] = len(lst_obj_result)
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
