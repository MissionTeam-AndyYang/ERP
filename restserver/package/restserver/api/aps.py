# coding=utf8
import pytz
import uuid
import json
import string
import validictory
from copy import deepcopy
import math
from flask import request
from package.util.util import *
from .common import *
from package.common.common import *
from package.log.log import CLogger
from package.dbwrapper.table import *
from package.dbwrapper.dbmgr import CDBMgr
from package.util.util import *
from sqlalchemy import func, cast, Numeric,desc
from .util import *
from package.aps.aps import *

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


class CQuantity(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'results': {}}

        try:
            lst_result = []
            with (CDBMgr() as obj_dbmgr):
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                n_start = int(request.args.get('start', 0))
                n_count = int(request.args.get('count', 0))

                # 選取不重複的訂單編號
                obj_order_query = (
                    obj_session.query(CTableAPSQuantity.product_order_no)
                    .filter(*lst_where)
                    .distinct()
                    .order_by(CTableAPSQuantity.product_order_no.asc())
                )
                #算出「總訂單數」
                n_total = obj_order_query.count()
                if n_count > 0:
                    lst_order_nos = [
                        row[0] for row in obj_order_query.offset(n_start).limit(n_count).all()
                    ]
                else:
                    lst_order_nos = [
                        row[0] for row in obj_order_query.all()
                    ]
                dict_grouped = defaultdict(list)
                dict_order_grouped = defaultdict(set)
                if lst_order_nos:
                    # 抓取這幾筆訂單的所有 APS 資料與關聯的訂單資訊
                    lst_obj_result = (
                        obj_session.query(CTableAPSQuantity, CTableProductOrder, CTableContract)
                        .outerjoin(CTableProductOrder, CTableAPSQuantity.product_order_no == CTableProductOrder.no)
                        .outerjoin(CTableContract,
                                   CTableContract.no == CTableProductOrder.ref_no)
                        .filter(CTableAPSQuantity.product_order_no.in_(lst_order_nos))
                        .order_by(CTableAPSQuantity.product_order_no.asc(), CTableAPSQuantity.creationTime.asc())
                        .all()
                    )

                    for obj_aps, obj_order, obj_contract in lst_obj_result:
                        str_order_no = obj_aps.product_order_no
                        dict_grouped[str_order_no].append(obj_aps)
                        dict_order_grouped[str_order_no] = (obj_order, obj_contract)

                    for str_order_no, lst_aps in dict_grouped.items():
                        obj_order = dict_order_grouped[str_order_no][0]
                        obj_contract = dict_order_grouped[str_order_no][1]
                        dict_data = {
                            "product_order": {"no": obj_order.no if obj_order else "",
                                              "unit": obj_order.unit if obj_order else 0,
                                              "item_name": obj_order.item_name if obj_order else "",
                                              "item_ref_displayName": obj_order.item_ref_displayName if obj_order else "",
                                              "price": obj_order.price if obj_order else 0,
                                              "count": obj_order.count if obj_order else 0,
                                              "amount": obj_order.amount if obj_order else 0,
                                              "preparedCount": obj_order.preparedCount if obj_order else 0,
                                              "paymentType": obj_order.payment_type if obj_order else 0,

                                              "contractCategory": obj_contract.category if obj_contract else 0,
                                              "contractType": obj_contract.type if obj_contract else 0,
                                              "contractItemStyle": obj_contract.itemStyle if obj_contract else 0,
                                              "contractComment": obj_contract.comment if obj_contract else "",

                                              },
                            "process": []
                        }
                        for obj_data in lst_aps:
                            dict_process = {
                                "no": obj_data.no if obj_data else "",
                                "item_name": obj_data.item_name if obj_data else "",
                                "oneProcess": obj_data.oneProcess if obj_data else 0,
                                "secProcess": obj_data.secProcess if obj_data else 0,
                                "unit": obj_data.unit if obj_order else 0,
                                "amount": obj_data.amount if obj_data else 0,
                                "hours": round(obj_data.minutes/60.0, 2) if obj_data else 0 # 換算成小時
                            }
                            dict_data["process"].append(dict_process)
                        dict_data["process"] = sorted(dict_data["process"], key=lambda x: x['oneProcess'])
                        lst_result.append(dict_data)
                dict_extra_data['total'] = n_total
                dict_extra_data['count'] = len(lst_order_nos) # 回傳訂購訂單筆數
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
