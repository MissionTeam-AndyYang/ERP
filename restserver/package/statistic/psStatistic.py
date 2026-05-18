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
from sqlalchemy import func, cast, Numeric
import uuid
from enum import IntEnum
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


class EKind():
    NONE = 0
    PURCHASE = 1
    SALE = 2


class IPSStatistic(ABC):
    def __init__(self, str_timezone):
        self.__m_str_timezone = str_timezone

    @abstractmethod
    def retrieve(self, n_startTime, n_endTime):
        pass
    @abstractmethod
    def calculate(self, n_startTime, n_endTime, f_isCommit=False):
        """必須由繼承類別實作的抽象方法"""
        pass

    def insert_db(self, n_kind, dict_data):
        str_id =""
        str_uuid = str(uuid.uuid4()).replace("-", "")
        new_data = CTablePSMonthStatistic(
            id=str_uuid,
            year=dict_data["year"],
            month=dict_data["month"],
            kind=n_kind,
            category=dict_data["category"],
            specified_no=dict_data["specified_no"],
            specified_name=dict_data["specified_name"],
            amount=dict_data["amount"],
            creationTime=util_retrieve_now_time()
        )
        with CDBMgr() as obj_dbmgr:
            if obj_dbmgr.insert(new_data) != EErrorCode.ERROR_SUCCESS:
                str_id = str_uuid
            else:
                str_message = 'failed to create ps statistic'
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
        return str_id

    def _retrieve_year_month(self, n_startTime: int, n_endTime: int) -> list[dict]:
        lst_result = []
        obj_tz = ZoneInfo(self.__m_str_timezone)
        dict_grouped_by_year = {}
        # 台北時區下的起始時間
        obj_dt = datetime.fromtimestamp(n_startTime, tz=ZoneInfo("UTC")).astimezone(obj_tz)

        while True:
            # 當月 1 號 00:00
            obj_start_local = obj_dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

            # 下個月 1 號
            if obj_dt.month == 12:
                obj_next_month_local = obj_dt.replace(year=obj_dt.year + 1, month=1, day=1)
            else:
                obj_next_month_local = obj_dt.replace(month=obj_dt.month + 1, day=1)

            # UTC 對應的 timestamp 範圍
            n_start_utc = int(obj_start_local.astimezone(ZoneInfo("UTC")).timestamp())
            n_end_utc = int((obj_next_month_local - timedelta(seconds=1)).astimezone(ZoneInfo("UTC")).timestamp())

            if n_start_utc > n_endTime:
                break

            lst_result.append({
                'year': obj_start_local.year,
                'month': obj_start_local.month,
                'start_time': n_start_utc,
                #'end_time': min(n_end_utc, n_endTime)
                'end_time': n_end_utc
            })

            obj_dt = obj_next_month_local

            # 整理成 grouped_by_year：{2025: [1, 2, 3]}
            n_year = obj_start_local.year
            n_month = obj_start_local.month
            dict_grouped_by_year.setdefault(n_year, []).append(n_month)

            # 轉成 {"year": ..., "start_month": ..., "end_month": ...} 格式
            lst_years = []
            for n_year, lst_months in dict_grouped_by_year.items():
                lst_years.append({
                    "year": n_year,
                    "start_month": min(lst_months),
                    "end_month": max(lst_months)
                })
        return lst_result, lst_years

class CPurchaseStatistic(IPSStatistic):

    def __init__(self, str_timezone):
        super().__init__(str_timezone)
        self.__m_n_kind = EKind.PURCHASE

    def retrieve(self, n_startTime, n_endTime):
        lst_data = []

        try:
            lst_obj_result = self.__retrieve_suppliers()
            lst_time, lst_years = self._retrieve_year_month(n_startTime, n_endTime)
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                for dict_time in lst_time:
                    lst_ps = (obj_session.query(
                                CTablePSMonthStatistic)
                                .filter(CTablePSMonthStatistic.kind == self.__m_n_kind,
                                         CTablePSMonthStatistic.year == dict_time["year"],
                                         CTablePSMonthStatistic.month == dict_time["month"])
                                 .all()
                                 )
                    if lst_ps:
                        for obj_ps in lst_ps:
                            dict_tmp = object_as_dict(obj_ps)
                            lst_data.append(dict_tmp)
                    if not lst_ps:
                        for obj_result in lst_obj_result:
                            if obj_result.supplier_no == "":
                                continue
                            dict_data = self.__cal(obj_session, obj_result, dict_time)
                            if dict_data:
                                lst_data.append(dict_data)

        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_data

    def calculate(self, n_startTime, n_endTime, f_isCommit=False):
        lst_data = []
    
        try:
            lst_obj_result = self.__retrieve_suppliers()
            lst_time,_ = self._retrieve_year_month(n_startTime, n_endTime)
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                for dict_time in lst_time:
                    for obj_result in lst_obj_result:
                        if obj_result.supplier_no == "":
                            continue
                        if obj_result.supplier_no == "RCN0000001":
                            pass
                        dict_data = self.__cal(obj_session, obj_result, dict_time)
                        if dict_data:
                            lst_data.append(dict_data)
            if f_isCommit:
                self.__commit(lst_data)
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_data

    def __cal(self, obj_session, obj_result, dict_time):
        dict_data = {}
        n_amount = 0
        obj_amount = (obj_session.query(
                                        func.round(func.sum(CTableGoodsReceiptNote.amount), 0)
                                        )
                                      .filter(CTableGoodsReceiptNote.item_ref_no == obj_result.supplier_no,
                                              CTableGoodsReceiptNote.date.between(dict_time["start_time"], dict_time["end_time"])
                                              )
                                      .all())

        if obj_amount:
            n_amount = int(obj_amount[0][0]) if obj_amount[0][0] is not None else 0
            dict_data = {
                "kind":self.__m_n_kind,
                "category": obj_result.category,
                "specified_no": obj_result.supplier_no,
                "specified_name": obj_result.supplier_displayName,
                "year": dict_time["year"],
                "month": dict_time["month"],
                "start_time": dict_time["start_time"],
                "end_time": dict_time["end_time"],
                "amount": n_amount
            }

        '''
        print(obj_result.supplier_displayName, dict_time["year"], dict_time["month"], dict_time["start_time"],
              dict_time["end_time"], n_amount)
        '''
        return dict_data
    def __commit(self, lst_data):
        for dict_data in lst_data:
            self.insert_db(self.__m_n_kind, dict_data)
            #update?

    def __retrieve_suppliers(self):
        lst_obj_result = []
        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_obj_result = (
                    obj_session.query(CTableMaterial.category,
                                      CTableMaterial.supplier_no,
                                      CTableMaterial.supplier_displayName)
                    .group_by(CTableMaterial.category, CTableMaterial.supplier_no)
                    .all()
                )
                print("")
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_obj_result


class CSaleStatistic(IPSStatistic):

    def __init__(self, str_timezone):
        super().__init__(str_timezone)
        self.__m_n_kind = EKind.SALE

    def retrieve_total(self, n_startTime, n_endTime):
        lst_data = []

        try:
            lst_obj_result = self.__retrieve_customer()
            lst_time, lst_years = self._retrieve_year_month(n_startTime, n_endTime)
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                dict_total = {}
                for dict_time in lst_time:
                    str_key = "%d-%d" % (dict_time["year"], dict_time["month"])
                    lst_ps = (obj_session.query(
                        CTablePSMonthStatistic)
                              .filter(CTablePSMonthStatistic.kind == self.__m_n_kind,
                                      CTablePSMonthStatistic.year == dict_time["year"],
                                      CTablePSMonthStatistic.month == dict_time["month"])
                              .all()
                              )
                    if lst_ps:
                        for obj_ps in lst_ps:
                            if str_key not in dict_total:
                                dict_total[str_key] = 0.0
                            dict_total[str_key] += obj_ps.amount

                    if not lst_ps:
                        for obj_result in lst_obj_result:
                            if obj_result.no == "":
                                continue
                            dict_data = self.__cal(obj_session, obj_result, dict_time)
                            if dict_data:
                                if str_key not in dict_total:
                                    dict_total[str_key] = 0.0
                                dict_total[str_key] += dict_data["amount"]
                if dict_total:
                    lst_data = self.__dict_to_list(dict_total)

        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_data

    def retrieve(self, n_startTime, n_endTime):
        lst_data = []

        try:
            lst_obj_result = self.__retrieve_customer()
            lst_time, lst_years = self._retrieve_year_month(n_startTime, n_endTime)
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                for dict_time in lst_time:
                    lst_ps = (obj_session.query(
                        CTablePSMonthStatistic)
                              .filter(CTablePSMonthStatistic.kind == self.__m_n_kind,
                                      CTablePSMonthStatistic.year == dict_time["year"],
                                      CTablePSMonthStatistic.month == dict_time["month"])
                              .all()
                              )
                    if lst_ps:
                        for obj_ps in lst_ps:
                            dict_tmp = object_as_dict(obj_ps)
                            lst_data.append(dict_tmp)
                    if not lst_ps:
                        for obj_result in lst_obj_result:
                            if obj_result.no == "":
                                continue
                            dict_data = self.__cal(obj_session, obj_result, dict_time)
                            if dict_data:
                                lst_data.append(dict_data)

        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_data

    def calculate(self, n_startTime, n_endTime, f_isCommit=False):
        lst_data = []

        try:
            lst_obj_result = self.__retrieve_customer()
            lst_time, _ = self._retrieve_year_month(n_startTime, n_endTime)
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                for dict_time in lst_time:
                    for obj_result in lst_obj_result:
                        if obj_result.no == "":
                            continue
                        dict_data = self.__cal(obj_session, obj_result, dict_time)
                        if dict_data:
                            lst_data.append(dict_data)
            if f_isCommit:
                self.__commit(lst_data)
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_data

    def __dict_to_list(self, dict_data: dict[str, float]) -> list[dict]:
        result = []
        for str_ym, f_amount in dict_data.items():
            str_year, str_month = str_ym.split("-")
            result.append({
                "year": int(str_year),
                "month": int(str_month),
                "amount": f_amount
            })
        return result
    def __cal(self, obj_session, obj_result, dict_time):
        dict_data = {}
        n_amount = 0
        obj_amount = (obj_session.query(
                        func.round(func.sum(CTableShippingOrder.amount), 0)
                      )
                      .filter(CTableShippingOrder.customer_no == obj_result.no,
                              CTableShippingOrder.date.between(dict_time["start_time"], dict_time["end_time"])
                              )
                      .all())

        if obj_amount:
            n_amount = int(obj_amount[0][0]) if obj_amount[0][0] is not None else 0
            dict_data = {
                "kind": self.__m_n_kind,
                "category":0,     # 需修改取得正確的客戶類別資料
                "specified_no": obj_result.no,
                "specified_name": obj_result.displayName,
                "year": dict_time["year"],
                "month": dict_time["month"],
                "start_time": dict_time["start_time"],
                "end_time": dict_time["end_time"],
                "amount": n_amount
            }
        '''
        if obj_result.displayName == '星巴克':
            print(obj_result.displayName, dict_time["year"], dict_time["month"], n_amount, dict_time["start_time"],
                  dict_time["end_time"])
        '''
        return dict_data

    def __commit(self, lst_data):
        for dict_data in lst_data:
            self.insert_db(self.__m_n_kind, dict_data)

    def __retrieve_customer(self):
        lst_obj_result = []
        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                # 需修改取得正確的客戶類別資料
                '''
                lst_obj_result = (
                    obj_session.query(CTableCustomer.category,
                                      CTableCustomer.no,
                                      CTableCustomer.displayName)
                    .group_by(CTableCustomer.category, CTableCustomer.no)
                    .all()
                )
                '''
                lst_obj_result = (
                    obj_session.query(CTableCompany.no,
                                      CTableCompany.displayName)

                    .all()
                )

                print("")
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_obj_result

