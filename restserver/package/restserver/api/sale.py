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
from package.inventory.inventoryQuery import CCInventroyRecByOrder, CCInventroyRecByOrder2
from package.statistic.orderStatistic import COrdersItemMonth, COrdersSum,COrdersItemCategory
from package.contract.contract import CContract
from package.arap.arap import COrderPayment

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


class CProductOrder(CPrivilegeControl):
    STATUS_NONE = 0
    STATUS_PREACTION = 1
    STATUS_PROCESS = 2
    STATUS_COMPLETE = 4
    STATUS_CANCEL = 8


    TYPE_RAW = 0
    TYPE_STOCK = 1 #新增API

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'sum':{"amount": 0,
                                  "realAmount": 0,
                                  "returnAmount": 0,
                                  "itemCategoryAmount": []},

                           'total': 0,
                           'count': 0,
                           'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()

                if request.args.get('type') and int(request.args.get('type')) == self.TYPE_STOCK:
                   dict_extra_data = self.__get_stock(obj_session)
                else:
                    lst_where, dict_time = self.__fill_query_params()
                    n_total = (
                        obj_session.query(CTableProductOrder)
                        .filter(*lst_where)
                        .order_by(CTableProductOrder.date.desc())
                        .count()
                    )
                    lst_amount = COrdersItemCategory(str_timezone).getAmount(EOrderStatisticKind.PRODUCT, dict_time)
                    dict_extra_data['sum']["itemCategoryAmount"] = lst_amount
                    dict_sum = COrdersSum(str_timezone).get(EOrderStatisticKind.PRODUCT, dict_time )
                    dict_extra_data['sum']["amount"] = dict_sum["ordersAmount"]
                    dict_extra_data['sum']["realAmount"] =  dict_sum["realAmount"]
                    dict_extra_data['sum']["returnAmount"] =  dict_sum["returnAmount"]

                    n_start = 0
                    n_count = 0
                    if request.args.get('start') and request.args.get('count'):
                        n_start = int(request.args.get('start'))
                        n_count = int(request.args.get('count'))

                    if n_count:
                        ids_query = (obj_session.query(
                            CTableProductOrder.id)
                                     .filter(*lst_where)
                                     .order_by(CTableProductOrder.date.desc())
                                     .offset(n_start)
                                     .limit(n_count)
                                     )

                        ids = [id[0] for id in ids_query.all()]
                        lst_obj_result = (
                            obj_session.query(
                                CTableProductOrder,
                                func.round(func.sum(CTableShippingOrder.checkedCount), 2),
                                func.round(func.sum(CTableShippingOrder.amount), 0),
                                CTableContract
                            )
                            .filter(CTableProductOrder.id.in_(ids))
                            .outerjoin(CTableShippingOrder, CTableShippingOrder.product_order_no == CTableProductOrder.no)
                            .outerjoin(CTableContract,
                                       CTableContract.no == CTableProductOrder.ref_no)
                            .order_by(CTableProductOrder.date.desc())
                            .group_by(CTableProductOrder.no)
                            .all()
                        )
                    else:
                        lst_obj_result = (
                            obj_session.query( CTableProductOrder,
                                func.round(func.sum(CTableShippingOrder.checkedCount), 2),
                                func.round(func.sum(CTableShippingOrder.amount), 0),
                                CTableContract
                                )
                            .filter(*lst_where)
                            .outerjoin(CTableShippingOrder, CTableShippingOrder.product_order_no == CTableProductOrder.no)
                            .outerjoin(CTableContract,
                                       CTableContract.no == CTableProductOrder.ref_no)
                            .order_by(CTableProductOrder.date.desc())
                            .group_by(CTableProductOrder.no)
                            .all()
                        )

                    lst_result = []
                    for obj_row in lst_obj_result:
                       dict_row = object_as_dict(obj_row[0])
                       dict_row['contract'] = {
                           'price': obj_row[3].price if obj_row[3] is not None else 0,
                           'name': obj_row[3].displayName if obj_row[3] is not None else "",
                           'type': obj_row[3].type if obj_row[3] is not None else 0,
                           'date': obj_row[3].date if obj_row[3] is not None else 0,
                           'comment': obj_row[3].comment if obj_row[3] is not None else ""
                       }
                       n_category, n_subCategory, _, _, _ = get_item_info(dict_row['item_no'])
                       dict_row['itemCategory'] = n_category
                       dict_row['itemSubCategory'] = n_subCategory

                       dict_row['realCount'] = obj_row[1] if obj_row[1] is not None else 0
                       dict_row['realAmount'] = int(obj_row[2]) if obj_row[2] is not None else 0
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

    def __get_stock(self, obj_session):
        from collections import defaultdict
        from itertools import groupby
        from operator import attrgetter
        dict_data = {'inventory': [], # 庫存量
                     'refRecords':[], # 出入庫紀錄
                     'orders':[]} # 銷貨單
        if request.args.get('order_no'):
            str_order_no = request.args.get('order_no')
            dict_records, dict_stocks = CCInventroyRecByOrder().get_batch(CCInventroyRecByOrder.TYPE_PRODUCT_ORDER, [str_order_no])


            # 取得庫存
            dict_data['inventory'] = dict_stocks.get(str_order_no, [])
            # 取得出入庫
            dict_data['refRecords'] = dict_records.get(str_order_no, [])

            # 取得銷貨單
            lst_orders = (
                obj_session.query(CTableShippingOrder)
                .filter(CTableShippingOrder.product_order_no == str_order_no)
                .order_by(CTableShippingOrder.date.asc())
                .all()
            )

            for n_date, items in groupby(lst_orders, key=attrgetter('date')):
                lst_items = list(items)
                f_count = round(sum(obj.expectedCount for obj in lst_items), 2)
                lst_dict = [object_as_dict(obj) for obj in lst_items]
                dict_temp = {
                    "date": n_date,
                    "count": f_count,
                    "data": lst_dict
                }
                dict_data['orders'].append(dict_temp)  # 銷貨單
        return dict_data

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

    def __fill_query_params(self):
        lst_where = []
        dict_time = {'start_time': 0, 'end_time': 0}
        if request.args.get('start_time') and request.args.get('end_time'):
            # get the range of timestamp
            n_start = util_convert_timestamp_to_date(int(request.args.get('start_time')))
            if int(request.args.get('start_time')) == int(request.args.get('end_time')):
                n_end = util_convert_timestamp_to_date(n_start, 1) - 1
            else:
                n_end = util_convert_timestamp_to_date(int(request.args.get('end_time')), 1) - 1
            dict_time['start_time'] = n_start
            dict_time['end_time'] = n_end
            lst_where.append(CTableProductOrder.date.between(n_start, n_end))

        if request.args.get('item_no'):
            lst_where.append(CTableProductOrder.item_no == request.args.get('item_no'))

        if request.args.get('item_name'):
            lst_where.append(CTableProductOrder.item_name == request.args.get('item_name'))

        if request.args.get('item_ref_name'):
            lst_where.append(CTableProductOrder.item_ref_name == request.args.get('item_ref_name'))

        if request.args.get('item_ref_no'):
            lst_where.append(CTableProductOrder.item_ref_no == request.args.get('item_ref_no'))

        if request.args.get('no'):
            lst_where.append(CTableProductOrder.no == request.args.get('no'))

        if request.args.get('status'):
            pass

        return lst_where, dict_time

class CShippingOrder(CPrivilegeControl):
    STATUS_NONE = 0
    STATUS_PREACTION = 1
    STATUS_PROCESS = 2
    STATUS_COMPLETE = 4
    STATUS_CANCEL = 8
    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = { 'sum': {"amount": 0,
                                    "returnAmount": 0},
                           'total': 0,
                           'count': 0,
                           'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                n_total = (
                    obj_session.query(CTableShippingOrder)
                    .filter(*lst_where)
                    .order_by(CTableShippingOrder.date.desc())
                    .count()
                )

                obj_sum = (
                    obj_session.query(
                        func.round(
                            func.sum(
                                case(
                                    (CTableShippingOrder.category == 0, CTableShippingOrder.amount),
                                    else_=0)
                            ), 0
                        ).label("amount"),
                        func.round(
                            func.sum(
                                case(
                                    (CTableShippingOrder.category == 1, CTableShippingOrder.amount),
                                    else_=0)
                            ), 0
                        ).label("return_amount")

                    )
                    .filter(*lst_where)
                    .one()
                )
                if obj_sum:
                    dict_extra_data['sum']["amount"] = int(obj_sum.amount) if obj_sum.amount else 0
                    dict_extra_data['sum']["returnAmount"] = int(obj_sum.return_amount) if obj_sum.return_amount else 0

                n_start = 0
                n_count = 0
                if request.args.get('start') and request.args.get('count'):
                    n_start = int(request.args.get('start'))
                    n_count = int(request.args.get('count'))

                if n_count:
                    ids_query = (obj_session.query(
                                CTableShippingOrder.id)
                                 .filter(*lst_where)
                                 .order_by(CTableShippingOrder.date.desc())
                                 .offset(n_start)
                                 .limit(n_count)
                                 )

                    ids = [id[0] for id in ids_query.all()]
                    lst_obj_result = (
                        obj_session.query(
                            CTableShippingOrder,
                            CTableProductOrder.payment_type
                        )
                        .filter(CTableShippingOrder.id.in_(ids))
                        .outerjoin(CTableProductOrder, CTableShippingOrder.product_order_no == CTableProductOrder.no)
                        .order_by(CTableShippingOrder.date.desc())
                        .all()
                    )
                else:
                    lst_obj_result = (
                        obj_session.query(CTableShippingOrder,
                                          CTableProductOrder.payment_type)
                        .filter(*lst_where)
                        .outerjoin(CTableProductOrder, CTableShippingOrder.product_order_no == CTableProductOrder.no)
                        .order_by(CTableShippingOrder.date.desc())
                        .all()
                    )

                lst_result = []
                for obj_row in lst_obj_result:
                    dict_row = object_as_dict(obj_row[0])
                    dict_row['payment_type'] = obj_row[1]
                    n_category, n_subCategory, _, _, _ = get_item_info(dict_row['item_no'])
                    dict_row['itemCategory'] = n_category
                    dict_row['itemSubCategory'] = n_subCategory
                    dict_row['inventory'] = []
                    dict_row['refRecords'] = []
                    self.__get_inventory(obj_session, dict_row)
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

    def __get_inventory(self, obj_session, dict_row):
        # 同銷貨單, 同批號不同倉儲
        lst_obj_records = (
            obj_session.query(
                CTableInventoryRec,
                CTableBatchNumber.validDate
            )
            .filter(CTableInventoryRec.ref_no == dict_row["no"])
            .outerjoin(CTableBatchNumber,
                       CTableBatchNumber.no == CTableInventoryRec.batchNumber)
            .all()
        )

        # 取得計算 批號_倉儲的庫存量
        for obj_rec in lst_obj_records:
            dict_rec = object_as_dict(obj_rec[0])
            dict_rec["validDate"] = obj_rec[1] if obj_rec[1] is not None else 0
            dict_row['refRecords'].append(dict_rec)

            lst_obj_rec2 = (
                obj_session.query(
                    CTableInventoryRec.warehouse_no,
                    CTableInventoryRec.warehouse_displayName,
                    func.sum(
                        case(
                            (CTableInventoryRec.category == EInventoryCategory.IN, CTableInventoryRec.count),  # 入庫
                            (CTableInventoryRec.category == EInventoryCategory.OUT, -CTableInventoryRec.count)  # 出庫
                        )
                    ).label("remaining_count")
                )
                .filter(CTableInventoryRec.batchNumber == dict_rec["batchNumber"],
                        CTableInventoryRec.warehouse_no == dict_rec["warehouse_no"])
                .all()
            )
            for obj_rec in lst_obj_rec2:
                dict_row['inventory'].append({"warehouse_no": obj_rec.warehouse_no,
                                              "warehouse_displayName": obj_rec.warehouse_displayName,
                                              "batchNumber": dict_rec["batchNumber"],
                                              "validDate": dict_rec["validDate"],
                                              "count": round(obj_rec.remaining_count, 2)})


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

    def __fill_query_params(self):
        lst_where = []

        if request.args.get('start_time') and request.args.get('end_time'):
            # get the range of timestamp
            n_start = util_convert_timestamp_to_date(int(request.args.get('start_time')))
            if int(request.args.get('start_time')) == int(request.args.get('end_time')):
                n_end = util_convert_timestamp_to_date(n_start, 1) - 1
            else:
                n_end = util_convert_timestamp_to_date(int(request.args.get('end_time')), 1) - 1
            lst_where.append(CTableShippingOrder.date.between(n_start, n_end))

        if request.args.get('product_order_no'):
            lst_where.append(CTableShippingOrder.product_order_no == request.args.get('product_order_no'))

        if request.args.get('item_ref_name'):
            lst_where.append(CTableShippingOrder.item_ref_name == request.args.get('item_ref_name'))

        if request.args.get('status'):
            pass

        return lst_where

class CStatistic(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'contract': [],
                           'amount': [],
                           'company': []}

        try:
            f_isCommit = False
            n_orderCategory = EOrderStatisticKind.PRODUCT
            if request.args.get('start_time') and request.args.get('end_time'):
                # get the range of timestamp
                n_start = int(request.args.get('start_time'))
                n_end = int(request.args.get('end_time'))
                # 庫存
                if request.args.get('commit'):
                    f_isCommit = True
                # 取得銷貨金額/訂單帳款金額
                lst_amount = COrdersItemMonth(str_timezone).calculate(n_start, n_end, n_orderCategory, f_isCommit)

                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    # 計算訂購合約/廠商數量
                    lst_contract = self.__get_contract_statistic(obj_session, n_start, n_end)
                    # 計算廠商每月的銷貨總和
                    lst_company = self.__get_company_statistic(obj_session, n_start, n_end)
                dict_extra_data['contract'] = lst_contract
                dict_extra_data['amount'] = lst_amount
                dict_extra_data['company'] = lst_company
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def __get_contract_statistic(self, obj_session, n_start, n_end):
        from sqlalchemy import func, distinct

        lst_result = []
        obj_contract = (
            obj_session.query(
                CTableContract.no,
                CTableContract.itemCategory,
                CTableContract.itemStyle
            )
            .group_by(CTableContract.no)  # 確保每個 no 只有一組分類
            .subquery()
        )

        lst_obj_result = (
            obj_session.query(
                # 如果 itemStyle/itemCategory 是 None，在 SQL 層級可以給它一個預設顯示名稱
                func.coalesce(obj_contract.c.itemCategory, -1).label("itemCategory"),
                func.coalesce(obj_contract.c.itemStyle, -1).label("itemStyle"),
                # 強制轉型為 Integer 避免 Decimal 問題
                func.cast(func.sum(CTableProductOrder.amount), Integer).label("totalAmount"),
                # 不重複個數計算
                func.count(distinct(CTableProductOrder.item_ref_no)).label("companyCount")
            )
            # 使用 outerjoin 確保沒有合約的訂單也會被算進去
            .outerjoin(obj_contract, CTableProductOrder.ref_no == obj_contract.c.no)
            .filter(
                CTableProductOrder.date >= n_start,
                CTableProductOrder.date < n_end
            )

            .group_by(
                func.coalesce(obj_contract.c.itemCategory, -1),
                func.coalesce(obj_contract.c.itemStyle, -1)
            )
            .all()
        )
        for itemCategory, itemStyle, totalAmount, companyCount in lst_obj_result:
            dict_data = {
                "itemCategory": itemCategory if itemCategory else 0,# 合約
                "itemStyle": itemStyle if itemStyle else 0, # 合約
                "companyCount": companyCount if companyCount else 0,
                "totalAmount": totalAmount if totalAmount else 0,
            }
            lst_result.append(dict_data)
        return lst_result

    def __get_company_statistic(self, obj_session, n_start, n_end):
        from sqlalchemy import func
        str_month = func.from_unixtime(CTableShippingOrder.date, '%Y-%m')
        lst_result = []
        # 取得公司列表
        lst_obj_tmp = (
            obj_session.query(
                CTableShippingOrder.item_ref_no
            )
            .filter(
                CTableShippingOrder.date >= n_start,
                CTableShippingOrder.date < n_end
            )
            .group_by(
                CTableShippingOrder.item_ref_no
            )
            .all()
        )
        lst_nos = [obj_row.item_ref_no for obj_row in lst_obj_tmp if obj_row]

        lst_obj_result = (
            obj_session.query(
                str_month.label("month"),  # 選出月份字串
                CTableShippingOrder.item_ref_no,
                CTableShippingOrder.item_ref_displayName,
                func.cast(func.sum(CTableShippingOrder.amount), Integer).label("totalAmount")
            )
            .filter(
                CTableShippingOrder.date >= n_start,
                CTableShippingOrder.date < n_end,
                CTableShippingOrder.item_ref_no.in_(lst_nos)
            )
            .group_by(str_month, CTableShippingOrder.item_ref_no)  # 按月份分群
            .order_by(str_month.asc(),                              # 先按月份排序
                      CTableShippingOrder.item_ref_no.asc())        # 同月份內再按項目編號排序
            .all()
        )
        for month, item_ref_no, item_ref_displayName, totalAmount in lst_obj_result:
            dict_data = {
                "month": month if month else "",
                "item_ref_no": item_ref_no if item_ref_no else "",
                "item_ref_displayName": item_ref_displayName if item_ref_displayName else "",

                "totalAmount": totalAmount if totalAmount else 0,
            }
            lst_result.append(dict_data)
        return lst_result

class CPayment(CPrivilegeControl):
    # 帳款費用
    def get(self, str_timezone='', str_id=''):
        str_message, n_status_code, n_code = 'success', 200, EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()

                obj_query_base = obj_session.query(CTableOrderPayment).filter(*lst_where)
                n_total = obj_query_base.count()

                n_start = int(request.args.get('start', 0))
                n_count = int(request.args.get('count', 0))

                lst_filter = lst_where
                if n_count > 0:
                    ids_query = (obj_session.query(CTableOrderPayment.no)
                                 .filter(*lst_where)
                                 .group_by(CTableOrderPayment.no)
                                 .order_by(CTableOrderPayment.date.desc())
                                 .offset(n_start).limit(n_count).all())
                    lst_filter = [CTableOrderPayment.no.in_([i[0] for i in ids_query])]

                # 1. 先建立一個包含總額的 Subquery
                subq = (
                    obj_session.query(
                        CTableOrderPayment.no.label('payment_no'),
                        func.round(func.sum(CTableOrderPayment.count), 0).label("count"),
                        func.round(func.sum(CTableOrderPayment.addDeleteAmount), 0).label("addDeleteAmount"),
                        func.round(func.sum(CTableOrderPayment.amount), 0).label("amount"),
                    )
                    .filter(*lst_filter)
                    .group_by(CTableOrderPayment.no)
                    .subquery()
                )

                # 2. 用這個 Subquery 去關聯其他 Table
                lst_obj_result = (
                    obj_session.query(CTableOrderPayment, CTableShippingOrder, CTableContract, subq)
                    .join(subq, CTableOrderPayment.no == subq.c.payment_no)
                    .outerjoin(CTableShippingOrder, CTableOrderPayment.ref_sub_no == CTableShippingOrder.no)
                    .outerjoin(CTableProductOrder, CTableProductOrder.no == CTableShippingOrder.product_order_no)
                    .outerjoin(CTableContract, CTableProductOrder.ref_no == CTableContract.no)
                    .order_by(CTableOrderPayment.ref_no.desc())
                    .all()
                )

                lst_result = []
                for row in lst_obj_result:
                    payment = row.CTableOrderPayment
                    shipping = row.CTableShippingOrder
                    contract = row.CTableContract

                    lst_result.append({
                        "payment": {
                            "no": payment.no,
                            "date": payment.date,
                            "month": payment.month.strftime("%Y/%m"),
                            "count": row.count,
                            "amount": int(row.amount or 0),
                            "addDeleteAmount": int(row.addDeleteAmount or 0)
                        },
                        "order": {
                            "no": shipping.no if shipping else "",
                            "count": shipping.checkedCount if shipping else 0,
                            "expectedCount": shipping.expectedCount if shipping else 0,
                            "parentNo": shipping.product_order_no if shipping else "",
                            "item_name": shipping.item_name if shipping else "",
                            "item_ref_displayName": shipping.item_ref_displayName if shipping else "",
                            "unit": shipping.unit if shipping else 0,
                            "price": shipping.price if shipping else 0,
                            "contractCategory": contract.category if contract else 0,
                            "contractType": contract.type if contract else 0,
                            "contractItemStyle": contract.itemStyle if contract else 0,
                            "paymentType": payment.paymentType if payment else 0,
                        },

                    })
                    print("")

                if lst_result:
                    dict_extra_data.update({'total': n_total, 'count': len(lst_result), 'results': lst_result})

        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = f'throw exception (error: {error})'
            CLogger().log(CLogger.LOG_LEVELERROR, f'[{self.__class__.__name__}] {str_message}')

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

    def __fill_query_params(self):
        lst_where = [CTableOrderPayment.refCategory == EBatchTraceRefCategory.SALE]

        return lst_where

class CSaleARAP(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'results': []}
        if not request.args.get("order_no"):
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'invalid parameter'
        else:
            try:
                str_order_no = request.args.get("order_no")
                lst_result = COrderPayment(str_timezone).get(EARAPType.AR, str_order_no)
                dict_records, _ = CCInventroyRecByOrder().get_batch(CCInventroyRecByOrder.TYPE_PRODUCT_ORDER,
                                                                              [str_order_no], False)
                lst_records = dict_records.get(str_order_no, [])
                for dict_result in lst_result:
                    dict_result["records"] = []
                    with CDBMgr() as obj_dbmgr:
                        obj_session = obj_dbmgr.get_session()
                        obj_result = (
                            obj_session.query(
                                func.min(CTableShippingOrder.date),  # 取得最早日期
                                func.max(CTableShippingOrder.date)  # 取得最晚日期
                            )
                            .filter(CTableShippingOrder.no.in_(dict_result["subOrderNos"]))
                            .first()
                        )

                        if obj_result:
                            n_start_date, n_end_date = obj_result
                            lst_inventory = [
                                dict_record for dict_record in lst_records
                                if n_start_date <= dict_record['date'] <= n_end_date
                            ]
                            dict_result["records"].extend(lst_inventory)
                dict_extra_data['total'] = len(lst_result)
                dict_extra_data['results'] = lst_result
            except Exception as error:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'throw exception (error: %s)' % str(error)
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                              % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data


class CSaleContract(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'results': []}
        try:
            n_start = 0
            n_count = 0
            if request.args.get('start') and request.args.get('count'):
                n_start = int(request.args.get('start'))
                n_count = int(request.args.get('count'))

            n_total, lst_result = CContract().get(n_start, n_count, {'category': CContract.SALES, 'itemStyle': [EItemStyle.GOODS, EItemStyle.MATERIAL]})
            dict_extra_data['total'] = n_total
            dict_extra_data['count'] = len(lst_result)
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
