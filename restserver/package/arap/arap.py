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
from sqlalchemy import delete
from sqlalchemy import func, cast, Numeric, case
from package.restserver.api.util import *
from package.inventory.inventoryQuery import CCInventroyRecByOrder

# 取得預計收付款日
def g_cal_due_date(str_timezone, n_year, n_month, n_day, n_payment_period):
    from datetime import datetime, time
    from zoneinfo import ZoneInfo
    from dateutil.relativedelta import relativedelta

    n_base_date = datetime(n_year, n_month, 1) + relativedelta(days=n_day - 1)
    n_months_add = n_payment_period // 30
    n_days_add = n_payment_period % 30

    obj_target = n_base_date + relativedelta(months=n_months_add)
    obj_last_day_of_month = obj_target + relativedelta(day=31)

    final_dt = datetime.combine(obj_last_day_of_month.date(), time.min)
    final_dt += relativedelta(days=n_days_add + (n_payment_period == 0))

    taipei_tz = ZoneInfo(str_timezone)
    obj_timezone_date = final_dt.replace(tzinfo=taipei_tz)

    n_date = int(obj_timezone_date.timestamp())
    return n_date

class COrderPayment(object):
    def __init__(self, str_timezone):
        self.__m_str_timezone = str_timezone

    def get(self, n_arap, str_ref_no):
        try:
            lst_result = []
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()

                lst_obj_result = (
                    obj_session.query(
                        CTableOrderPayment.group_no,
                        CTableOrderPayment.month,
                        CTableOrderPayment.paymentType,
                        CTableOrderPayment.item_ref_displayName,
                        func.group_concat(func.distinct(CTableOrderPayment.date)).label("dates"),
                        func.group_concat(func.distinct(CTableOrderPayment.ref_sub_no)).label("subNos"),
                        func.round(func.sum(CTableOrderPayment.totalAmount), 0).label("totalAmount"),
                        CTablePayment
                    )
                    .filter(
                        CTableOrderPayment.ref_no == str_ref_no,
                        CTableOrderPayment.arapType == n_arap
                    )
                    .outerjoin(CTableCompany, CTableOrderPayment.item_ref_no == CTableCompany.no)
                    .outerjoin(CTablePayment, CTablePayment.id == case(
                        (CTableOrderPayment.arapType == EARAPType.AP, CTableCompany.received_id),
                        else_=CTableCompany.paid_id
                    ))
                    .group_by(
                        CTableOrderPayment.month,
                        CTableOrderPayment.group_no,
                        CTablePayment.id
                    )
                    .all()
                )

                for obj_row in lst_obj_result:
                    lst_sub_no = obj_row.subNos.split(",") if obj_row.subNos else []
                    lst_dates = obj_row.dates.split(",") if obj_row.dates else []
                    obj_month = obj_row.month
                    n_paymentType = obj_row.paymentType
                    str_company = obj_row.item_ref_displayName
                    obj_payment = obj_row.CTablePayment
                    n_due_date = lst_dates[0] if lst_dates else 0
                    # 月結
                    if n_paymentType == 1 and obj_month and obj_payment:
                        n_due_date = g_cal_due_date(self.__m_str_timezone, obj_month.year, obj_month.month, obj_payment.date, obj_payment.period)
                    dict_data = {
                        "no": obj_row.group_no if obj_row.group_no else '',
                        "month": obj_row.month.strftime("%Y/%m") if obj_row.month else  '',
                        "companyName": str_company,
                        "subOrderNos": lst_sub_no,
                        "totalAmount": obj_row.totalAmount if obj_row.totalAmount else 0,
                        "dueDate":n_due_date
                    }
                    if dict_data["totalAmount"]:
                        lst_result.append(dict_data)
        except Exception as error:
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
            raise ValueError(str_message)
        return lst_result


class CCShipPayment(object):
    def __init__(self, str_timezone):
        self.__m_str_timezone = str_timezone

    def get(self, n_arap, str_ref_no):
        try:
            lst_result = []
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_obj_result = (
                    obj_session.query(
                        CTableShippingPayment.group_no,
                        CTableShippingPayment.month,
                        CTableShippingPayment.item_ref_displayName,
                        CTableShippingPayment.paymentType,
                        func.group_concat(func.distinct(CTableShippingPayment.date)).label("dates"),
                        # 將單號與金額串接，並用逗號分隔
                        # 產出格式範例: "REC001:1500,REC002:2300"
                        func.group_concat(
                            func.distinct(
                                func.concat(
                                    CTableShippingPayment.record_no,
                                    ':',
                                    func.cast(CTableShippingPayment.totalAmount, String)
                                )
                            )
                        ).label("recDetails"),

                        # 整體群組的加總金額
                        func.round(func.sum(CTableShippingPayment.totalAmount), 0).label("totalAmount"),
                        CTablePayment
                    )
                    .outerjoin(CTableCompany, CTableShippingPayment.item_ref_no == CTableCompany.no)
                    .outerjoin(CTablePayment, CTablePayment.id == case(
                        (CTableShippingPayment.arapType == EARAPType.AP, CTableCompany.received_id),
                        else_=CTableCompany.paid_id
                    ))
                    .filter(
                        CTableShippingPayment.ref_no == str_ref_no,
                        CTableShippingPayment.arapType == n_arap
                    )
                    .group_by(
                        CTableShippingPayment.month,
                        CTableShippingPayment.group_no,
                        CTablePayment.id
                    )
                    .all()
                )

                for obj_row in lst_obj_result:
                    lst_rec = []
                    lst_dates = obj_row.dates.split(",") if obj_row.dates else []
                    lst_item = obj_row.recDetails.split(",")
                    for str_item in lst_item:
                        str_rec_no, str_amount = str_item.split(':')
                        lst_rec.append({"rec_no": str_rec_no,
                                        "amount": float(str_amount)})
                    obj_month = obj_row.month
                    n_paymentType = obj_row.paymentType
                    str_company = obj_row.item_ref_displayName
                    obj_payment = obj_row.CTablePayment
                    n_due_date = lst_dates[0] if lst_dates else 0
                    # 月結
                    if n_paymentType == 1 and obj_month and obj_payment:
                        n_due_date = g_cal_due_date(self.__m_str_timezone, obj_month.year, obj_month.month,
                                                    obj_payment.date, obj_payment.period)
                    dict_data = {
                        "no": obj_row.group_no if obj_row.group_no else '',
                        "month": obj_row.month.strftime("%Y/%m") if obj_row.month else '',
                        "companyName": str_company,
                        "recDetails": lst_rec,
                        "totalAmount": obj_row.totalAmount if obj_row.totalAmount else 0,
                        "dueDate": n_due_date
                    }
                    if dict_data["totalAmount"]:
                        lst_result.append(dict_data)
        except Exception as error:
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
            raise ValueError(str_message)
        return lst_result

class CCWarehousePayment(object):
    TYPE_PRODUCT_ORDER = 1
    TYPE_PURCHASE_ORDER = 2
    TYPE_GOODSRECEIPTNOTE = 3
    TYPE_SHIPPING_ORDER = 4

    def __init__(self, str_timezone):
        self.__m_str_timezone = str_timezone

    def get(self, n_order_category, str_order_no):
        try:
            lst_result = []

            dict_records, _ = CCInventroyRecByOrder().get_batch(n_order_category,
                                                                [str_order_no], False)
            lst_tmp = dict_records.get(str_order_no, [])
            lst_batchNos = [dict_item.get("batchNumber", "") for dict_item in lst_tmp] if lst_tmp else []

            if lst_batchNos:
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    lst_obj_result = (
                        obj_session.query(
                            CTableWarehousePayment.group_no,
                            CTableWarehousePayment.month,
                            CTableWarehousePayment.item_ref_displayName,
                            CTableWarehousePayment.paymentType,
                            func.group_concat(func.distinct(CTableWarehousePayment.date)).label("dates"),
                            # 將單號與金額串接，並用逗號分隔
                            # 產出格式範例: "REC001:1500,REC002:2300"
                            func.group_concat(
                                func.distinct(
                                    func.concat(
                                        CTableWarehousePayment.record_no,
                                        ':',
                                        func.cast(CTableWarehousePayment.totalAmount, String)
                                    )
                                )
                            ).label("recDetails"),

                            # 整體群組的加總金額
                            func.round(func.sum(CTableWarehousePayment.totalAmount), 0).label("totalAmount"),
                            CTablePayment
                        )
                        .outerjoin(CTableCompany, CTableWarehousePayment.item_ref_no == CTableCompany.no)
                        .outerjoin(CTablePayment, CTablePayment.id == case(
                            (CTableWarehousePayment.arapType == EARAPType.AP, CTableCompany.received_id),
                            else_=CTableCompany.paid_id
                        ))
                        .filter(
                            CTableWarehousePayment.batch_no.in_(lst_batchNos)
                        )
                        .group_by(
                            CTableWarehousePayment.month,
                            CTableWarehousePayment.group_no,
                            CTablePayment.id
                        )
                        .all()
                    )

                    for obj_row in lst_obj_result:
                        lst_rec = []
                        lst_dates = obj_row.dates.split(",") if obj_row.dates else []
                        lst_item = obj_row.recDetails.split(",")
                        for str_item in lst_item:
                            str_rec_no, str_amount = str_item.split(':')
                            lst_rec.append({"rec_no": str_rec_no,
                                            "amount": float(str_amount)})
                        obj_month = obj_row.month
                        n_paymentType = obj_row.paymentType
                        str_company = obj_row.item_ref_displayName
                        obj_payment = obj_row.CTablePayment
                        n_due_date = lst_dates[0] if lst_dates else 0
                        # 月結
                        if n_paymentType == 1 and obj_month and obj_payment:
                            n_due_date = g_cal_due_date(self.__m_str_timezone, obj_month.year, obj_month.month,
                                                        obj_payment.date, obj_payment.period)
                        dict_data = {
                            "no": obj_row.group_no if obj_row.group_no else '',
                            "month": obj_row.month.strftime("%Y/%m") if obj_row.month else '',
                            "companyName": str_company,
                            "recDetails": lst_rec,
                            "totalAmount": obj_row.totalAmount if obj_row.totalAmount else 0,
                            "dueDate": n_due_date
                        }
                        if dict_data["totalAmount"]:
                            lst_result.append(dict_data)

        except Exception as error:
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
            raise ValueError(str_message)
        return lst_result