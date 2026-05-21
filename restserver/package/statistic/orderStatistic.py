# coding=utf8
import pytz
import string
from copy import deepcopy
from flask import request
from package.util.util import *
from package.common.common import *
from package.log.log import CLogger
from package.dbwrapper.table import *
from package.dbwrapper.dbmgr import CDBMgr
from sqlalchemy import func, cast, Numeric, case, and_, not_,or_
import uuid
from datetime import datetime, timedelta, time, date
from zoneinfo import ZoneInfo
import calendar
from collections import defaultdict


class COrdersSum():

    def __init__(self, str_timezone):
        self.__m_str_timezone = str_timezone

    def get(self, n_order_category, dict_where ):
        dict_data = {
            "ordersAmount": 0, #期間內訂單金額
            "returnAmount": 0, #期間內退回金額
            "realAmount":0     #期間內進銷貨金額
        }
        OrderTable1 = None
        OrderTable2 = None
        if n_order_category == EOrderStatisticKind.PURCHASE:
            OrderTable1 = CTablePurchaseOrder
            OrderTable2 = CTableGoodsReceiptNote
            Key = "purchase_order_no"

        elif n_order_category == EOrderStatisticKind.PRODUCT:
            OrderTable1 = CTableProductOrder
            OrderTable2 = CTableShippingOrder
            Key = "product_order_no"

        lst_where1 = self.__fill_query_params(dict_where, OrderTable1)
        lst_where2 = self.__fill_query_params(dict_where, OrderTable2)

        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()

            # 單純計算 OrderTable1 總金額
            n_amount = (
                obj_session.query(func.round(func.sum(OrderTable1.amount), 0))
                .filter(*lst_where1)
                .scalar()
            )

            # 計算 realAmount 與 returnAmount
            obj_sum = (
                obj_session.query(
                    func.round(
                        func.sum(
                            case(
                                (OrderTable2.category == 0, OrderTable2.amount),
                                else_=0,
                            )
                        ), 0
                    ).label("realAmount"),
                    func.round(
                        func.sum(
                            case(
                                (OrderTable2.category == 1, OrderTable2.amount),
                                else_=0,
                            )
                        ), 0
                    ).label("returnAmount"),
                )
                .filter(*lst_where2)
                .one()
            )
            '''
            計算關聯此訂購/採購訂單的銷貨/進貨金額
            obj_sum = (
                obj_session.query(
                    func.round(
                        func.sum(
                            case(
                                (OrderTable2.category == 0, OrderTable2.amount),
                                else_=0,
                            )
                        ), 0
                    ).label("realAmount"),
                    func.round(
                        func.sum(
                            case(
                                (OrderTable2.category == 1, OrderTable2.amount),
                                else_=0,
                            )
                        ), 0
                    ).label("returnAmount"),
                )
                .select_from(OrderTable1)  # 明確指定主表
                .outerjoin(OrderTable2, getattr(OrderTable2, Key) == OrderTable1.no)
                .filter(*lst_where2)
                .one()
            )
            '''
            # 組合結果
            dict_data["ordersAmount"] = int(n_amount) if n_amount else 0
            dict_data["realAmount"] = int(obj_sum.realAmount)  if obj_sum.realAmount else 0
            dict_data["returnAmount"] = int(obj_sum.returnAmount)  if obj_sum.returnAmount else 0
        return dict_data

    def __fill_query_params(self, dict_where, OrderTable):
        lst_where = []
        if dict_where.get('start_time', 0) and dict_where.get('end_time', 0):
            # get the range of timestamp
            n_start = util_convert_timestamp_to_date(dict_where['start_time'])
            if dict_where['start_time'] == dict_where['end_time']:
                n_end = util_convert_timestamp_to_date(n_start, 1) - 1
            else:
                n_end = util_convert_timestamp_to_date(dict_where['end_time'], 1) - 1
            lst_where.append(OrderTable.date.between(n_start, n_end))
        return lst_where


# 計算原料/物料/膠捲 廠商數與總金額
class COrdersItemCategory():

    def __init__(self, str_timezone):
        self.__m_str_timezone = str_timezone

    def getCount(self, n_order_category, dict_where ):
        from collections import defaultdict

        OrderTable = None
        if n_order_category == EOrderStatisticKind.PURCHASE:
            OrderTable = CTableGoodsReceiptNote
        elif n_order_category == EOrderStatisticKind.PRODUCT:
            OrderTable = CTableShippingOrder
        lst_where = self.__fill_query_params(dict_where, OrderTable)

        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            lst_data = []
            if n_order_category == EOrderStatisticKind.PURCHASE:

                # 計算分群筆數
                lst_count = (
                    obj_session.query(
                        CTableMaterial.category.label("category"),
                        OrderTable.item_ref_no.label("item_ref_no"),
                        OrderTable.item_ref_displayName.label("item_ref_name"),
                        func.count().label("count")
                    )
                    .select_from(OrderTable)
                    .outerjoin(CTableMaterial, OrderTable.item_no == CTableMaterial.no)
                    .filter(*lst_where)
                    .group_by(CTableMaterial.category, OrderTable.item_ref_no)
                    .all()
                )
                # 這是你系統中「預期會出現的所有分類」
                lst_category = [EItemCategory.PM, EItemCategory.MA, EItemCategory.AF]

                # 統計開始
                dict_group = defaultdict(set)
                for category, item_ref_no, item_ref_name, count in lst_count:
                    dict_group[category].add(item_ref_no)

                # 最終統計結果 — 強制包含 lst_category
                for category in lst_category:
                    item_refs = dict_group.get(category, set())
                    lst_data.append({
                        "category": category,
                        "count": len(item_refs)
                    })

            elif n_order_category == EOrderStatisticKind.PRODUCT:
                lst_count = (
                    obj_session.query(
                        OrderTable.item_ref_no.label("item_ref_no"),
                        OrderTable.item_ref_displayName.label("item_ref_name"),
                        func.count().label("count")
                    )
                    .filter(*lst_where)
                    .group_by(OrderTable.item_ref_no)
                    .all()
                )
                lst_data = [
                    {"category": 1, "count": len(lst_count)},
                    {"category": 2, "count": 0}
                ]
                print("")
        return lst_data

    def getAmount(self, n_order_category, dict_where ):
        from collections import defaultdict

        OrderTable = None
        if n_order_category == EOrderStatisticKind.PURCHASE:
            OrderTable = CTableGoodsReceiptNote
        elif n_order_category == EOrderStatisticKind.PRODUCT:
            OrderTable = CTableShippingOrder
        lst_where = self.__fill_query_params(dict_where, OrderTable)

        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            lst_data = []
            if n_order_category == EOrderStatisticKind.PURCHASE:

                # 計算分群筆數
                lst_amount = (
                    obj_session.query(
                        CTableMaterial.category.label("category"),
                        cast(func.round(func.sum(OrderTable.amount), 0), Float).label("totalAmount")
                    )
                    .select_from(OrderTable)
                    .outerjoin(CTableMaterial, OrderTable.item_no == CTableMaterial.no)
                    .filter(*lst_where)
                    .group_by(CTableMaterial.category)
                    .all()
                )
                # 這是你系統中「預期會出現的所有分類」
                lst_category = [EItemCategory.PM, EItemCategory.MA, EItemCategory.AF]

                # 統計開始
                dict_group = defaultdict(set)
                for category, totalAmount in lst_amount:
                    dict_group[category] = totalAmount

                # 最終統計結果 — 強制包含 lst_category
                for category in lst_category:
                    n_total = dict_group.get(category, 0)
                    lst_data.append({
                        "category": category,
                        "amount": n_total
                    })

            elif n_order_category == EOrderStatisticKind.PRODUCT:
                obj_amount = (
                    obj_session.query(
                        cast(func.round(func.sum(OrderTable.amount), 0), Float).label("totalAmount")
                    )
                    .filter(*lst_where)
                    .first()
                )
                lst_data = [
                    {"category": 1, "amount":obj_amount.totalAmount if obj_amount else 0}, # 產製品
                    {"category": 2, "amount": 0} # 貨品
                ]
                print("")
        return lst_data

    def __fill_query_params(self, dict_where, OrderTable):
        lst_where = []
        if dict_where.get('start_time', 0) and dict_where.get('end_time', 0):
            # get the range of timestamp
            n_start = util_convert_timestamp_to_date(dict_where['start_time'])
            if dict_where['start_time'] == dict_where['end_time']:
                n_end = util_convert_timestamp_to_date(n_start, 1) - 1
            else:
                n_end = util_convert_timestamp_to_date(dict_where['end_time'], 1) - 1
            lst_where.append(OrderTable.date.between(n_start, n_end))
        return lst_where


class COrdersItemMonth():

    def __init__(self, str_timezone):
        self.__m_str_timezone = str_timezone

    def calculate(self, n_startTime, n_endTime, n_order_category, f_isCommit=False, f_refresh=False):
        lst_data = []

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_month = self.__retrieve_month(n_startTime, n_endTime)
                for str_month in lst_month:
                    lst_tmp = self.__cal(obj_session, str_month, n_order_category, f_refresh)
                    if f_isCommit:
                        self.__commit(lst_tmp)

                    for dict_data in lst_tmp:
                        dict_data["date"] = dict_data["date"].strftime('%Y-%m')
                    lst_data.extend(lst_tmp)
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_data

    def __cal(self, obj_session, str_month, n_order_category, f_refresh):
        obj_month = datetime.strptime(str_month, '%Y-%m').date()
        lst_where = self.__fill_query_params(n_order_category)

        if obj_month:
            lst_obj_result = (
                obj_session.query(
                    CTableOrderItemMonthStatistic
                )
                .filter(*lst_where)
                .filter(
                    CTableOrderItemMonthStatistic.date == obj_month,
                    CTableOrderItemMonthStatistic.timezone == self.__m_str_timezone
                )
                .all()
            )

        lst_cal = []  # 含稅的價錢
        if not lst_obj_result:
            lst_cal = self.__cal_value(obj_session, n_order_category, obj_month)

        lst_pre = []  # lst_pre 含稅的價錢, lst_cal 含稅價錢
        for obj_pre in lst_obj_result:
            dict_pre = object_as_dict(obj_pre)
            dict_pre.pop("id", None)
            dict_pre.pop("timezone", None)
            dict_pre.pop("creationTime", None)
            lst_pre.append(dict_pre)
        lst_data = lst_pre + lst_cal
        return lst_data


    def __cal_value(self, obj_session, n_order_category, obj_month):
        lst_data = []

        try:
            OrderTable = None
            VendorTable = None

            if n_order_category == EOrderStatisticKind.PURCHASE:
                OrderTable = CTableGoodsReceiptNote
                VendorTable = CTableCompany
            elif n_order_category == EOrderStatisticKind.PRODUCT:
                OrderTable = CTableShippingOrder
                VendorTable = CTableCompany

            # 取得全部廠商清單+帳款區間
            lst_vendor = []
            if VendorTable:
                lst_obj_tmp = (
                    obj_session.query(
                        VendorTable.paid_id,
                        VendorTable.no,
                        VendorTable.displayName,
                        CTablePayment.type.label("payment_type")
                    )
                    .outerjoin(CTablePayment, VendorTable.paid_id == CTablePayment.id)
                    .all()
                )

                # vendor_nos 會是逗號字串，要轉成 list
                dict_grouped = defaultdict(list)
                for row in lst_obj_tmp:
                    payment_type = 0 if row.payment_type is None else row.payment_type
                    dict_grouped[payment_type].append(row.no)

                lst_vendor = [
                    {
                        "payment_type": key,
                        "vendor_nos": nos
                    }
                    for key, nos in dict_grouped.items()
                ]
            # 現結/月結廠商
            for dict_vendor in lst_vendor:
                n_start1, n_end1 = self.__get_month_utc_range(obj_month)

                # 計算客戶/廠商進銷貨金額
                lst_total = (obj_session.query(
                    OrderTable.itemCategory,
                    OrderTable.itemSubCategory,
                    OrderTable.item_ref_no,
                    OrderTable.item_ref_displayName,
                    func.round(func.sum(OrderTable.amount), 0).label("total"),
                ).filter(OrderTable.date.between(n_start1, n_end1),
                         OrderTable.item_ref_no.in_(dict_vendor["vendor_nos"]))
                .group_by(OrderTable.item_ref_no, OrderTable.itemCategory, OrderTable.itemSubCategory)
                .all())

                dict_tmp = {}
                for obj_row in lst_total:
                    if obj_row.item_ref_no == None:
                        continue
                    if obj_row.item_ref_no not in dict_tmp:
                        dict_tmp[obj_row.item_ref_no] = {
                            "date": obj_month,
                            "kind": n_order_category,
                            "category": obj_row.itemCategory, #itemCategory
                            "subCategory": obj_row.itemSubCategory, #itemSubCategory
                            "type": dict_vendor["payment_type"],
                            "specified_no": obj_row.item_ref_no,
                            "specified_name": obj_row.item_ref_displayName,
                            "payment": 0.0, # 帳款
                            "amount": int(obj_row.total) #進銷貨金額
                        }

                # 計算客戶/廠商月結帳款額
                lst_payment = (obj_session.query(
                    CTableOrderPayment.item_ref_no,
                    CTableOrderPayment.item_ref_displayName,
                    func.round(func.sum(CTableOrderPayment.totalAmount), 0).label("totalAmount")
                     ).filter(CTableOrderPayment.refCategory == n_order_category,
                              CTableOrderPayment.month == obj_month,
                              CTableOrderPayment.item_ref_no.in_(dict_vendor["vendor_nos"]))
                    .group_by(CTableOrderPayment.item_ref_no, CTableOrderPayment.paymentType)
                    .all())

                for obj_row in lst_payment:
                    n_payment = int(obj_row.totalAmount)
                    if obj_row.item_ref_no == None:
                        continue
                    if obj_row.item_ref_no not in dict_tmp:
                        dict_tmp[obj_row.item_ref_no] = {
                            "date": obj_month,
                            "kind": n_order_category,
                            "category": dict_vendor["payment_type"],
                            "specified_no": obj_row.item_ref_no,
                            "specified_name": obj_row.item_ref_displayName,
                            "payment": n_payment,
                            "amount": 0.0
                        }
                    else:
                        dict_tmp[obj_row.item_ref_no]["payment"] = n_payment
                for str_key, dict_item in dict_tmp.items():
                    lst_data.append(dict_item)

                print("")
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_data


    def __get_month_utc_range(self, obj_month):
        # 1轉成當地時區的起始日期
        obj_tz = pytz.timezone(self.__m_str_timezone)

        # 該月的第一天 (本地時間)
        local_start = obj_tz.localize(datetime(obj_month.year, obj_month.month, 1, 0, 0, 0))

        # 該月的天數
        days_in_month = calendar.monthrange(obj_month.year, obj_month.month)[1]

        # 該月的最後一天 +1天 = 下一月的0點
        local_end = obj_tz.localize(datetime(obj_month.year, obj_month.month, days_in_month, 0, 0, 0)) + timedelta(
            days=1)

        # 轉換成 UTC timestamp
        n_start = int(local_start.timestamp())
        n_end = int(local_end.timestamp()) - 1

        return n_start, n_end


    def __get_payment_utc_range(self, n_year, n_month, n_day):
        """
        根據輸入的年月日（結帳日），回傳「上期結帳日 + 1」到「本期結帳日」的 timestamp 區間
        """
        # 結帳日（本期結束日）
        if n_day in [0, 30]:
            start_date = date(n_year, n_month, 1)

            # 1. 取得下個月的第一天
            if n_month + 1 > 12:
                day_of_month = date(n_year+1, 1, 1)
            else:
                day_of_month = date(n_year, n_month + 1, 1)
            # 2. 從第一天減去一天，就得到上個月的最後一天
            end_date = day_of_month - timedelta(days=1)
        else:
            end_date = date(n_year, n_month, n_day)

            # 計算上期月份
            if n_month == 1:
                prev_year = n_year - 1
                prev_month = 12
            else:
                prev_year = n_year
                prev_month = n_month - 1

            # 取得上期月底（可能比結帳日短）
            last_day_prev_month = calendar.monthrange(prev_year, prev_month)[1]
            prev_close_day = min(n_day, last_day_prev_month)  # 若前月沒有該日（如2月），取月底

            # 起始日為上期結帳日 + 1
            start_date = date(prev_year, prev_month, prev_close_day) + timedelta(days=1)

        # 轉成 timestamp
        n_start = self.__convert_to_utc_time(self.__m_str_timezone, start_date)
        n_end = self.__convert_to_utc_time(self.__m_str_timezone, end_date, True)
        return start_date, end_date, n_start, n_end

    def __commit(self, lst_data):
        for dict_data in lst_data:
            self.__insert_update_db(dict_data)

    def __insert_update_db(self, dict_data):
        str_id = ""

        with CDBMgr() as obj_dbmgr:
            str_uuid = str(uuid.uuid4()).replace("-", "")
            new_data = CTableOrderItemMonthStatistic(

                date=dict_data["date"],
                timezone=self.__m_str_timezone,
                kind=dict_data["kind"],
                category=dict_data["category"],
                subCategory=dict_data["subCategory"],
                type = dict_data["type"],
                specified_no=dict_data["specified_no"],
                specified_name = dict_data["specified_name"],
                amount=dict_data["amount"],
                payment=dict_data["payment"],
                creationTime=util_retrieve_now_time()
            )


            if obj_dbmgr.insert(new_data) == EErrorCode.ERROR_SUCCESS:
                str_id = new_data.id
            else:
                str_message = 'failed to create order item month'
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
                dict_tmp = {"amount": dict_data["amount"],
                            "payment": dict_data["payment"],
                            "creationTime":util_retrieve_now_time()}
                if obj_dbmgr.update(CTableOrderItemMonthStatistic,
                                    [
                                        CTableOrderItemMonthStatistic.date == dict_data["date"],
                                        CTableOrderItemMonthStatistic.kind == dict_data["kind"],
                                        CTableOrderItemMonthStatistic.timezone == self.__m_str_timezone,
                                        CTableOrderItemMonthStatistic.category == dict_data["category"],
                                        CTableOrderItemMonthStatistic.specified_no == dict_data["specified_no"]],
                                    dict_tmp) != EErrorCode.ERROR_SUCCESS:
                    str_message = 'failed to update order month'
                    CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
        return str_id
    def __retrieve_month(self, n_startTime: int, n_endTime: int) -> list[dict]:
        lst_result = []
        obj_tz = ZoneInfo(self.__m_str_timezone)

        obj_dt = datetime.fromtimestamp(n_startTime, tz=ZoneInfo("UTC")).astimezone(obj_tz)

        while True:
            # 當月 1 號 00:00
            obj_start_local = obj_dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

            # UTC 對應的 timestamp 範圍
            n_start_utc = int(obj_start_local.astimezone(ZoneInfo("UTC")).timestamp())

            # 下個月 1 號
            if obj_dt.month == 12:
                obj_next_month_local = obj_dt.replace(year=obj_dt.year + 1, month=1, day=1)
            else:
                obj_next_month_local = obj_dt.replace(month=obj_dt.month + 1, day=1)

            if n_start_utc > n_endTime:
                break

            lst_result.append( obj_start_local.strftime("%Y-%m") )
            obj_dt = obj_next_month_local
        return lst_result

    def __fill_query_params(self, n_order_category):
        lst_where = []

        if n_order_category:
            lst_where.append(CTableOrderItemMonthStatistic.kind == n_order_category)
        return lst_where

    def __convert_to_utc_time(self, str_timezone, dt, f_second=False):
        try:
            tz_local = pytz.timezone(str_timezone)

            # 若是 date 而非 datetime，補上時間（00:00）
            if isinstance(dt, datetime):
                pass
            else:
                if f_second:
                    dt = datetime(dt.year, dt.month, dt.day, 23, 59, 59)
                else:
                    dt = datetime(dt.year, dt.month, dt.day)

            # 若沒有時區資訊，設為本地時區
            if dt.tzinfo is None:
                dt = tz_local.localize(dt)

            # 轉換為 UTC
            dt_utc = dt.astimezone(pytz.utc)

            # 回傳 timestamp（秒）
            return int(dt_utc.timestamp())

        except Exception as e:
            print("Error:", e)
            return 0

