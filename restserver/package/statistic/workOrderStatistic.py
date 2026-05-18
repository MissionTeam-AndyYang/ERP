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

class COrdersProcessMonth():

    def __init__(self, str_timezone):
        self.__m_str_timezone = str_timezone

    def calculate(self, n_startTime, n_endTime, f_isCommit=False, f_refresh=False):
        lst_data = []

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_month = self.__retrieve_month(n_startTime, n_endTime)
                for str_month in lst_month:
                    lst_tmp = self.__cal(obj_session, str_month, f_refresh)
                    if f_isCommit:
                        pass

                    for dict_data in lst_tmp:
                        dict_data["date"] = dict_data["date"].strftime('%Y-%m')
                    lst_data.extend(lst_tmp)
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_data

    def __cal(self, obj_session, str_month, f_refresh):
        obj_month = datetime.strptime(str_month, '%Y-%m').date()
        if obj_month:
            lst_data = self.__cal_value(obj_session, obj_month)
        return lst_data


    def __cal_value(self, obj_session, obj_month):
        lst_data = []

        try:
            n_start1, n_end1 = self.__get_month_utc_range(obj_month)
            from sqlalchemy import func

            lst_total = (
                obj_session.query(
                    CTableWorkOrder.oneProcess,
                    CTableWorkOrder.secProcess,
                    func.count().label("total")
                )
                .filter(CTableWorkOrder.date.between(n_start1, n_end1))
                .group_by(
                    CTableWorkOrder.oneProcess,
                    CTableWorkOrder.secProcess
                )
                .all()
            )

            for obj_total in lst_total:
                if obj_total:
                    dict_tmp = {
                        "date": obj_month,
                        "oneProcess": obj_total[0],
                        "secProcess": obj_total[1],
                        "total": obj_total[2]
                    }
                    lst_data.append(dict_tmp)

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

