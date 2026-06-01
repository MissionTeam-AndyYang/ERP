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
from sqlalchemy import delete
import uuid
from .util import *
from collections import defaultdict

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


class CMaterial(CPrivilegeControl):
    GET_NAME = 1

    MODIFY_BASIC = 1
    MODIFY_PRICE = 2

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                n_total = (
                    obj_session.query(CTableMaterial)
                    .filter(*lst_where)
                    .order_by(CTableMaterial.no.asc())
                    .count()
                )
                n_start = 0
                n_count = 0
                if request.args.get('start') and request.args.get('count'):
                    n_start = int(request.args.get('start'))
                    n_count = int(request.args.get('count'))

                if n_count:
                    ids_query = (obj_session.query(
                                 CTableMaterial.no)
                                 .filter(*lst_where)
                                 .order_by(CTableMaterial.no.asc())
                                 .offset(n_start)
                                 .limit(n_count)
                                 )

                    ids = [no[0] for no in ids_query.all()]
                    lst_obj_result = (
                        obj_session.query(CTableMaterial)

                        .filter(CTableMaterial.no.in_(ids))
                        .order_by(CTableMaterial.no.asc())
                        .all()
                    )
                else:
                    lst_obj_result = (
                        obj_session.query(CTableMaterial)
                        .filter(*lst_where)
                        .order_by(CTableMaterial.no.asc())
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
                        lst_tmp = []
                        if request.args.get('type') == 1:
                            for dict_data in lst_result:
                                lst_tmp.append({"id": dict_data["id"],
                                                "no": dict_data["no"],
                                                "name": dict_data["name"]})
                        else:
                            lst_tmp = lst_result
                        dict_extra_data['total'] = n_total
                        dict_extra_data['count'] = len(lst_tmp)
                        dict_extra_data['results'] = lst_tmp

        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def __fill_query_params(self):
        lst_where = []

        # setting  find conditions from query parameter
        if request.args.get('material_id'):
            lst_where.append(CTableMaterial.id == request.args.get('material_id'))

        if request.args.get('material_no'):
            lst_where.append(CTableMaterial.no == request.args.get('material_no'))

        if request.args.get('supplier_no'):
            lst_where.append(CTableMaterial.supplier_no == request.args.get('supplier_no'))

        if request.args.get('category'):
            lst_where.append(CTableMaterial.category == request.args.get('category'))

        return lst_where


class CItemPrice(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'count': 0, 'results': []}

        if not request.args.get("item_no"):
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'invalid parameter'
        else:
            try:
                with CDBMgr() as obj_dbmgr:
                    str_item_no = request.args.get("item_no")
                    obj_session = obj_dbmgr.get_session()
                    obj_date = self.__retrieve_one_year_ago(str_timezone)
                    lst_obj_price = (
                        obj_session.query(CTableItemPrice)
                        .filter(
                            CTableItemPrice.item_no == str_item_no,
                            CTableItemPrice.date >= obj_date
                        )
                        .order_by(CTableItemPrice.date.desc())
                        .all()
                    )

                    lst_result = []
                    for obj_price in lst_obj_price:
                        obj_loss = (
                            obj_session.query(CTableItemLoss)
                            .filter(
                                CTableItemLoss.item_no == str_item_no,
                                CTableItemLoss.date == obj_price.date
                            )
                            .first()
                        )
                        lst_result.append({
                            "month": obj_price.date.strftime("%Y/%m"),
                            "estUnit": obj_price.costUnitLength if obj_price.costUnitLength else obj_price.costUnitWeight,
                            "estPrice": obj_price.estCostPriceLength if obj_price.costUnitLength else obj_price.estCostPriceWeight,
                            "unit": obj_price.costUnitLength if obj_price.costUnitLength else obj_price.costUnitWeight,
                            "price": obj_price.costPriceLength if obj_price.costUnitLength else obj_price.costPriceWeight,
                            "lossUnit": obj_loss.unit if obj_loss else 0,
                            "loss": obj_loss.value if obj_loss else 0,
                            "estLoss": obj_loss.estValue if obj_loss else 0,
                        })
                    dict_extra_data["count"] = len(lst_result)
                    dict_extra_data["results"] = lst_result
            except Exception as error:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'throw exception (error: %s)' % str(error)
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                              % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def __retrieve_one_year_ago(self, str_timezone):
        from datetime import datetime
        from dateutil.relativedelta import relativedelta

        # 算出 11 個月前（含本月共12個月）的 1 號
        obj_date = (datetime.now() - relativedelta(months=11)).replace(day=1).date()
        return obj_date


