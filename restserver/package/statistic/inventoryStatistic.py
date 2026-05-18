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
from enum import IntEnum
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo


class IInventoryStatistic(ABC):

    def __init__(self, str_timezone):
        self.m_str_timezone = str_timezone

    @abstractmethod
    def calculate(self, n_startTime, n_endTime, f_isCommit=False):
        """必須由繼承類別實作的抽象方法"""
        pass

    @abstractmethod
    def update(self, n_date): #當庫存異動更新資料
        """必須由繼承類別實作的抽象方法"""
        pass

    def retrieve_day(self, n_startTime: int, n_endTime: int) -> list[dict]:
        lst_result = []
        obj_tz = ZoneInfo(self.m_str_timezone)  # 例如 Asia/Taipei

        # 把 UTC timestamp 轉換成當地時間
        dt_local = datetime.fromtimestamp(n_startTime, tz=ZoneInfo("UTC")).astimezone(obj_tz)
        dt_end_local = datetime.fromtimestamp(n_endTime, tz=ZoneInfo("UTC")).astimezone(obj_tz)

        while True:
            day_start_local = dt_local.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end_local = day_start_local + timedelta(days=1) - timedelta(seconds=1)

            start_utc = int(day_start_local.astimezone(ZoneInfo("UTC")).timestamp())
            end_utc = int(day_end_local.astimezone(ZoneInfo("UTC")).timestamp())

            if start_utc > n_endTime:
                break

            lst_result.append({
                "date": day_start_local.strftime("%Y-%m-%d"),
                "start_time": start_utc,
                # "end_time": min(end_utc, n_endTime)  # 防止最後一天超過區間
                "end_time": end_utc
            })
            dt_local = day_start_local + timedelta(days=1)

        return lst_result


class CInventoryDelta(IInventoryStatistic):
    TYPE_ITEMS = 1
    TYPE_BATCHNO = 2
    def __init__(self, str_timezone, n_type):
        super().__init__(str_timezone)
        self.__m_n_type = n_type

    def retrieve(self, n_startTime, n_endTime, f_refresh = False):
        lst_data = []

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_day = self.retrieve_day(n_startTime, n_endTime)
                for dict_day in lst_day:
                    lst_data = self.__cal(obj_session, dict_day, f_refresh)
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_data

    def retrieve_items_total(self, n_startTime, n_endTime, f_refresh=False):
        lst_data = []

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                #print("CInventoryDelta retrieve_items_total", n_startTime, n_endTime)
                lst_data = self.__cal_items_total(obj_session, n_startTime, n_endTime)
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_data

    def calculate(self, n_startTime, n_endTime, f_isCommit=False, f_refresh = False):
        lst_data = []
    
        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_day = self.retrieve_day(n_startTime, n_endTime)
                for dict_day in lst_day:
                    lst_tmp = self.__cal(obj_session, dict_day, f_refresh)
                    if f_isCommit:
                        self.__commit(lst_tmp)
                    lst_data.extend(lst_tmp)

        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_data

    def update(self, n_date):
        pass

    @abstractmethod
    def _get_data(self, obj_session, n_start, n_end):
        """必須由繼承類別實作的抽象方法"""
        pass

    @abstractmethod
    def _fill_data(self, obj_data, obj_date, n_kind, lst_in_ids, lst_out_ids):
        """必須由繼承類別實作的抽象方法"""
        pass

    @abstractmethod
    def _get_data_for_without(self, obj_session, n_start, n_end):
        """必須由繼承類別實作的抽象方法"""
        pass

    @abstractmethod
    def _fill_data_for_without(self, obj_data, obj_date, n_kind):
        """必須由繼承類別實作的抽象方法"""
        pass

    def __get_data_range(self, obj_session, lst_where, n_start, n_end):
        # 建立台灣時區
        tz = ZoneInfo(self.m_str_timezone)

        # 1. 將 UTC timestamp 轉為台灣時區的 date
        obj_start = datetime.fromtimestamp(n_start, tz=timezone.utc).astimezone(tz).date()
        obj_end = datetime.fromtimestamp(n_end, tz=timezone.utc).astimezone(tz).date()

        # 2. 查詢資料庫中最大日期
        obj_latest_date = (obj_session
                           .query(func.max(getattr(CTableInventoryDelta, "date")))
                            .filter(*lst_where)
                           .scalar())
        if obj_latest_date is None:
            return {
                "with_data": (None, None, 0, 0),
                "without_data": (obj_start, obj_end, n_start, n_end)
            }
        if obj_latest_date < obj_start:
            return {
                "with_data": (None, None, 0, 0),
                "without_data": (obj_start, obj_end, n_start, n_end)
            }
        elif obj_start <= obj_latest_date < obj_end:
            obj_next_day = obj_latest_date + timedelta(days=1)
            obj_latest_tw = datetime.combine(obj_latest_date, time.min, tzinfo=tz)
            n_latest = int(obj_latest_tw.astimezone(timezone.utc).timestamp())
            obj_next_tw = datetime.combine(obj_next_day, time.min, tzinfo=tz)
            n_next = int(obj_next_tw.astimezone(timezone.utc).timestamp())
            return {
                "with_data": (obj_start, obj_latest_date, n_start, n_latest),
                "without_data": (obj_next_day, obj_end, n_next, n_end)
            }
        else:
            return {
                "with_data": (obj_start, obj_end, n_start, n_end),
                "without_data": (None, None, 0, 0),
            }

    def __cal_items_total(self, obj_session, n_startTime, n_endTime):
        lst_data1 = []
        lst_data2 = []
        lst_where = self._fill_query_params()
        dict_range = self.__get_data_range(obj_session, lst_where, n_startTime, n_endTime)
        dict_with = dict_range["with_data"]
        dict_without = dict_range["without_data"]
        if dict_with[0]:
            lst_tmp = (
                obj_session.query(
                    CTableInventoryDelta.warehouse_no,
                    CTableInventoryDelta.warehouse_displayName,
                    CTableInventoryDelta.kind,
                    CTableInventoryDelta.category,
                    CTableInventoryDelta.specified_no,
                    CTableInventoryDelta.specified_name,
                    CTableInventoryDelta.specified_ref_no,
                    CTableInventoryDelta.specified_ref_name,
                    func.sum(
                        CTableInventoryDelta.inAmount
                    ).label("inAmount_total"),
                    func.sum(
                        CTableInventoryDelta.inPurchaseAmount
                    ).label("inPurchaseAmount_total"),
                    func.sum(CTableInventoryDelta.inCount
                    ).label("inCount_total"),
                    func.sum(CTableInventoryDelta.outAmount
                    ).label("outAmount_total"),
                    func.sum(CTableInventoryDelta.outCount
                    ).label("outCount_total"),
                )
                .filter(*lst_where)
                .filter(
                    CTableInventoryDelta.date.between(dict_with[0], dict_with[1]),
                    CTableInventoryDelta.timezone == self.m_str_timezone
                ).group_by(
                    CTableInventoryDelta.warehouse_no,
                    CTableInventoryDelta.warehouse_displayName,
                    CTableInventoryDelta.kind,
                    CTableInventoryDelta.category,
                    CTableInventoryDelta.specified_no
                )
                .all()
            )

            if lst_tmp:
                for obj_row in lst_tmp:
                    dict_data = {
                        "warehouse_no": obj_row.warehouse_no,
                        "warehouse_displayName": obj_row.warehouse_displayName,
                        "timezone": self.m_str_timezone,
                        "kind": obj_row.kind,
                        "category": obj_row.category,
                        "specified_no": obj_row.specified_no,
                        "specified_name": obj_row.specified_name,
                        "specified_ref_no": obj_row.specified_ref_no,
                        "specified_ref_name": obj_row.specified_ref_name,
                        "inCount": round(obj_row.inCount_total, 2),
                        "inAmount": round(obj_row.inAmount_total, 2),
                        "inPurchaseAmount": round(obj_row.inPurchaseAmount_total, 2),
                        "outCount": round(obj_row.outCount_total, 2),
                        "outAmount": round(obj_row.outAmount_total, 2)
                    }
                    lst_data1.append(dict_data)


        if dict_without[2]:
            n_start = dict_without[2]
            n_end = dict_without[3]

            lst_obj_data = self._get_data_for_without(obj_session, n_start, n_end)
            for obj_data in lst_obj_data:
                n_kind = self.__get_kind(obj_data)
                dict_data = self._fill_data_for_without(obj_data, n_kind)
                lst_data2.append(dict_data)
        lst_data = self.__merge_lists(lst_data1, lst_data2)

        return lst_data

    def __cal(self, obj_session, dict_day, f_refresh=False):
        lst_data = []
        lst_tmp = []

        if not f_refresh:
            #obj_start = datetime.utcfromtimestamp(dict_day["start_time"]).date()
            obj_date = datetime.strptime(dict_day["date"], "%Y-%m-%d").date()
            lst_where = self._fill_query_params()
            lst_tmp = (
                obj_session.query(
                    CTableInventoryDelta
                )
                .filter(*lst_where)
                .filter(
                    CTableInventoryDelta.date == obj_date,
                    CTableInventoryDelta.timezone == self.m_str_timezone
                )
                .all()
            )
            if lst_tmp:
                for obj_tmp in lst_tmp:
                    dict_tmp = object_as_dict(obj_tmp)
                    lst_data.append(dict_tmp)

        if f_refresh or not lst_tmp:
            lst_result = self._get_data(obj_session, dict_day["start_time"], dict_day["end_time"])
            str_date = dict_day["date"]
            lst_tmp = self.__gen_data(str_date, lst_result)
            lst_data.extend(lst_tmp)

        return lst_data

    def __get_kind(self, obj_data):
        n_kind = EInventoryDeltaKind.NONE
        if self.__m_n_type == self.TYPE_ITEMS:
            if obj_data.itemCategory in [EItemCategory.PM, EItemCategory.MA, EItemCategory.AF]:
                n_kind = EInventoryDeltaKind.MATERIAL
            elif obj_data.itemCategory == EItemCategory.INPRODUCT:
                n_kind = EInventoryDeltaKind.INPRODUCT
            elif obj_data.itemCategory == EItemCategory.PRODUCT:
                n_kind = EInventoryDeltaKind.PRODUCT
        else:
            n_kind = EInventoryDeltaKind.BATCHNO
        return n_kind

    def __gen_data(self, str_date, lst_result):
        from datetime import datetime

        lst_data = []
        for obj_data in lst_result:
            #print(str_date, obj_data.item_name, obj_data.inPurchaseAmount)
            lst_in_ids = obj_data.in_ids.split(',') if obj_data.in_ids else []
            lst_out_ids = obj_data.out_ids.split(',') if obj_data.out_ids else []
            n_kind = EInventoryDeltaKind.NONE
            if obj_data.itemCategory in [EItemCategory.PM, EItemCategory.MA, EItemCategory.AF]:
                n_kind = EInventoryDeltaKind.MATERIAL
            elif obj_data.itemCategory == EItemCategory.INPRODUCT:
                n_kind = EInventoryDeltaKind.INPRODUCT
            elif obj_data.itemCategory == EItemCategory.PRODUCT:
                n_kind = EInventoryDeltaKind.PRODUCT

            obj_date = datetime.strptime(str_date, '%Y-%m-%d').date()
            dict_data = self._fill_data(obj_data, obj_date, n_kind, lst_in_ids, lst_out_ids)
            lst_data.append(dict_data)
        return lst_data

    def __merge_lists(self, list_a, list_b):
        merged_dict = {}
        for item in list_a + list_b:
            key = (item["warehouse_no"], item["specified_no"], item["timezone"])
            if key not in merged_dict:
                # 建立新項目（注意要 copy，不然可能會影響原 list）
                merged_dict[key] = item.copy()
            else:
                # 累加數值欄位
                for field in ["inCount", "inAmount", "outCount", "outAmount"]:
                    merged_dict[key][field] += round(item.get(field, 0),)

        return list(merged_dict.values())

    def __commit(self, lst_data):
        for dict_data in lst_data:
            self.__insert_update_db(dict_data)

    def __insert_update_db(self, dict_data):
        str_id =""
        with CDBMgr() as obj_dbmgr:
            str_uuid = str(uuid.uuid4()).replace("-", "")
            new_data = CTableInventoryDelta(
                id=str_uuid,
                warehouse_no=dict_data["warehouse_no"],
                warehouse_displayName=dict_data["warehouse_displayName"],
                date=dict_data["date"],
                timezone=dict_data["timezone"],
                kind=dict_data["kind"],
                category=dict_data["category"],
                specified_no=dict_data["specified_no"],
                specified_name=dict_data["specified_name"],
                specified_ref_no=dict_data["specified_ref_no"],
                specified_ref_name=dict_data["specified_ref_name"],
                in_ref_id=dict_data["in_ref_id"],
                out_ref_id=dict_data["out_ref_id"],
                inPurchaseCount=dict_data["inPurchaseCount"],
                inPurchaseAmount=dict_data["inPurchaseAmount"],
                inCount=dict_data["inCount"],
                inAmount=dict_data["inAmount"],
                outCount=dict_data["outCount"],
                outAmount=dict_data["outAmount"],
                creationTime=util_retrieve_now_time()
            )
            if obj_dbmgr.insert(new_data) == EErrorCode.ERROR_SUCCESS:
                str_id = str_uuid
            else:
                str_message = 'failed to create inventory delta'
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
                dict_tmp = { "in_ref_id":dict_data["in_ref_id"],
                             "out_ref_id":dict_data["out_ref_id"],
                             "inPurchaseCount": dict_data["inPurchaseCount"],
                             "inPurchaseAmount": dict_data["inPurchaseAmount"],
                             "inCount": dict_data["inCount"],
                             "inAmount": dict_data["inAmount"],
                             "outAmount": dict_data["outAmount"],
                             "outCount": dict_data["outCount"]}
                if obj_dbmgr.update(CTableInventoryDelta,
                                           [CTableInventoryDelta.warehouse_no == dict_data["warehouse_no"],
                                            CTableInventoryDelta.date == dict_data["date"],
                                            CTableInventoryDelta.timezone == dict_data["timezone"],
                                            CTableInventoryDelta.specified_no == dict_data["specified_no"]],
                                           dict_tmp) != EErrorCode.ERROR_SUCCESS:
                    str_message = 'failed to update inventory delta'
                    CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
            return str_id


class CInventoryDeltaItem(CInventoryDelta):

    def __init__(self, str_timezone):
        super().__init__(str_timezone, CInventoryDelta.TYPE_ITEMS)
        self.__m_str_item_no = ""
        self.__m_n_itemCategory = 0
    def setParam(self, str_item_no, n_itemCategory):
        if str_item_no:
            self.__m_str_item_no = str_item_no
        if n_itemCategory:
            self.__m_n_itemCategory = n_itemCategory

    def _get_data(self, obj_session, n_start, n_end):
        lst_where = self.__fill_query_params_rec()

        lst_result = (
            obj_session.query(
                CTableInventoryRec.warehouse_no,
                CTableInventoryRec.warehouse_displayName,
                CTableInventoryRec.source,
                CTableInventoryRec.item_no,
                CTableInventoryRec.item_name,
                CTableInventoryRec.item_ref_no,
                CTableInventoryRec.item_ref_displayName,
                CTableInventoryRec.itemCategory,

                func.sum(
                    case((and_(
                        CTableInventoryRec.category == EInventoryCategory.IN,
                        or_(
                            and_(
                                CTableInventoryRec.itemCategory.in_([1, 2, 3]),
                                CTableInventoryRec.source == 1
                            ),
                            and_(
                                CTableInventoryRec.itemCategory.in_([4, 5]),
                                CTableInventoryRec.source == 5
                            )
                        )
                    ),
                          CTableInventoryRec.count * CTableInventoryRec.price), else_=0)
                ).label("inPurchaseAmount"),
                func.sum(
                    case((and_(
                        CTableInventoryRec.category == EInventoryCategory.IN,
                        or_(
                            and_(
                                CTableInventoryRec.itemCategory.in_([1, 2, 3]),
                                CTableInventoryRec.source == 1
                            ),
                            and_(
                                CTableInventoryRec.itemCategory.in_([4, 5]),
                                CTableInventoryRec.source == 5
                            )
                        )
                    ),
                          CTableInventoryRec.count), else_=0)
                ).label("inPurchaseCount"),

                func.sum(
                    case((CTableInventoryRec.category == EInventoryCategory.IN,
                          CTableInventoryRec.count * CTableInventoryRec.price), else_=0)
                ).label("inAmount"),
                func.sum(
                    case((CTableInventoryRec.category == EInventoryCategory.IN,
                          CTableInventoryRec.count), else_=0)
                ).label("inCount"),

                func.group_concat(
                    case((CTableInventoryRec.category == EInventoryCategory.IN, CTableInventoryRec.id), else_=None)
                ).label("in_ids"),

                func.sum(
                    case((CTableInventoryRec.category == EInventoryCategory.OUT,
                          CTableInventoryRec.count * CTableInventoryRec.price), else_=0)
                ).label("outAmount"),
                func.sum(
                    case((CTableInventoryRec.category == EInventoryCategory.OUT,
                          CTableInventoryRec.count), else_=0)
                ).label("outCount"),

                func.group_concat(
                    case((CTableInventoryRec.category == EInventoryCategory.OUT, CTableInventoryRec.id),
                         else_=None)
                ).label("out_ids"),
            )
            #.filter(*lst_where)
            .filter(CTableInventoryRec.itemType == EItemType.NEW,
                    CTableInventoryRec.date.between(n_start, n_end))
            .group_by(
                CTableInventoryRec.warehouse_no,
                CTableInventoryRec.warehouse_displayName,
                CTableInventoryRec.item_no,
                CTableInventoryRec.item_name,
                CTableInventoryRec.item_ref_no,
                CTableInventoryRec.item_ref_displayName,
                CTableInventoryRec.itemCategory
            )
            .all()
        )
        return lst_result

    def _get_data_for_without(self, obj_session, n_start, n_end):
        lst_where = self.__fill_query_params_rec()
        lst_result = (
            obj_session.query(
                CTableInventoryRec.warehouse_no,
                CTableInventoryRec.warehouse_displayName,
                CTableInventoryRec.source,
                CTableInventoryRec.item_no,
                CTableInventoryRec.item_name,
                CTableInventoryRec.item_ref_no,
                CTableInventoryRec.item_ref_displayName,
                CTableInventoryRec.itemCategory,
                func.sum(
                    case((and_(
                        CTableInventoryRec.category == EInventoryCategory.IN,
                        or_(
                            and_(
                                CTableInventoryRec.itemCategory.in_([1, 2, 3]),
                                CTableInventoryRec.source == 1
                            ),
                            and_(
                                CTableInventoryRec.itemCategory.in_([4, 5]),
                                CTableInventoryRec.source == 5
                            )
                        )
                    ),
                    CTableInventoryRec.count * CTableInventoryRec.price), else_=0)
                ).label("inPurchaseAmount"),
                func.sum(
                    case((and_(
                        CTableInventoryRec.category == EInventoryCategory.IN,
                        or_(
                            and_(
                                CTableInventoryRec.itemCategory.in_([1, 2, 3]),
                                CTableInventoryRec.source == 1
                            ),
                            and_(
                                CTableInventoryRec.itemCategory.in_([4, 5]),
                                CTableInventoryRec.source == 5
                            )
                        )
                    ),
                    CTableInventoryRec.count), else_=0)
                ).label("inPurchaseCount"),

                func.sum(
                    case((CTableInventoryRec.category == EInventoryCategory.IN,
                          CTableInventoryRec.count * CTableInventoryRec.price), else_=0)
                ).label("inAmount"),
                func.sum(
                    case((CTableInventoryRec.category == EInventoryCategory.IN,
                          CTableInventoryRec.count), else_=0)
                ).label("inCount"),
                func.sum(
                    case((CTableInventoryRec.category == EInventoryCategory.OUT,
                          CTableInventoryRec.count * CTableInventoryRec.price), else_=0)
                ).label("outAmount"),
                func.sum(
                    case((CTableInventoryRec.category == EInventoryCategory.OUT,
                          CTableInventoryRec.count), else_=0)
                ).label("outCount")
            )
            .filter(*lst_where)
            .filter(CTableInventoryRec.itemType == EItemType.NEW,
                    CTableInventoryRec.date.between(n_start, n_end))
            .group_by(
                CTableInventoryRec.warehouse_no,
                CTableInventoryRec.warehouse_displayName,
                CTableInventoryRec.item_no,
                CTableInventoryRec.item_name,
                CTableInventoryRec.item_ref_no,
                CTableInventoryRec.item_ref_displayName,
                CTableInventoryRec.itemCategory
            )
            .all()
        )

        return lst_result

    def _fill_data(self, obj_data, obj_date, n_kind, lst_in_ids, lst_out_ids):
        dict_data = {
            "warehouse_no": obj_data.warehouse_no,
            "warehouse_displayName": obj_data.warehouse_displayName,
            "date": obj_date,
            "timezone": self.m_str_timezone,
            "kind": n_kind,
            "category": obj_data.itemCategory if n_kind == EInventoryDeltaKind.MATERIAL else 0,
            "specified_no": obj_data.item_no,
            "specified_name": obj_data.item_name,
            "specified_ref_no": obj_data.item_ref_no,
            "specified_ref_name": obj_data.item_ref_displayName,
            "in_ref_id": lst_in_ids,
            "out_ref_id": lst_out_ids,
            "inPurchaseCount": round(obj_data.inPurchaseCount, 2),
            "inPurchaseAmount": round(obj_data.inPurchaseAmount, 2),
            "inCount": round(obj_data.inCount, 2),
            "inAmount": round(obj_data.inAmount, 2),
            "outCount": round(obj_data.outCount, 2),
            "outAmount": round(obj_data.outAmount, 2)
        }
        return dict_data

    def _fill_data_for_without(self, obj_data, n_kind):
        dict_data = {
            "warehouse_no": obj_data.warehouse_no,
            "warehouse_displayName": obj_data.warehouse_displayName,
            "timezone": self.m_str_timezone,
            "kind": n_kind,
            "category": obj_data.itemCategory if n_kind == EInventoryDeltaKind.MATERIAL else 0, #來自於inventrory_record 在製品/製成品填0
            "specified_no": obj_data.item_no,
            "specified_name": obj_data.item_name,
            "specified_ref_no": obj_data.item_ref_no,
            "specified_ref_name": obj_data.item_ref_displayName,
            "inPurchaseCount": round(obj_data.inPurchaseCount, 2),
            "inPurchaseAmount": round(obj_data.inPurchaseAmount, 2),
            "inCount": round(obj_data.inCount, 2),
            "inAmount": round(obj_data.inAmount, 2),
            "outCount": round(obj_data.outCount, 2),
            "outAmount": round(obj_data.outAmount, 2)
        }
        return dict_data

    def _fill_query_params(self):
        lst_where = [CTableInventoryDelta.kind != EInventoryDeltaKind.BATCHNO]
        if self.__m_str_item_no:
            lst_where.append(CTableInventoryDelta.specified_no == self.__m_str_item_no)

        if self.__m_n_itemCategory:
            if self.__m_n_itemCategory == EItemCategory.PRODUCT:
                lst_where.append(CTableInventoryDelta.kind == EInventoryDeltaKind.PRODUCT)
            if self.__m_n_itemCategory == EItemCategory.INPRODUCT:
                lst_where.append(CTableInventoryDelta.kind == EInventoryDeltaKind.INPRODUCT)
            if self.__m_n_itemCategory == EItemCategory.PM:
                lst_where.append(CTableInventoryDelta.kind == EInventoryDeltaKind.MATERIAL)
                lst_where.append(CTableInventoryDelta.category == EMaterialType.PM)
            if self.__m_n_itemCategory == EItemCategory.AF:
                lst_where.append(CTableInventoryDelta.kind == EInventoryDeltaKind.MATERIAL)
                lst_where.append(CTableInventoryDelta.category == EMaterialType.AF)
            if self.__m_n_itemCategory == EItemCategory.MA:
                lst_where.append(CTableInventoryDelta.kind == EInventoryDeltaKind.MATERIAL)
                lst_where.append(CTableInventoryDelta.category == EMaterialType.MA)
        return lst_where

    def __fill_query_params_rec(self):
        lst_where = []
        if self.__m_str_item_no:
            lst_where.append(CTableInventoryRec.item_no == self.__m_str_item_no)
        if self.__m_n_itemCategory:
            lst_where.append(CTableInventoryRec.itemCategory == self.__m_n_itemCategory)
        return lst_where


class CInventoryDeltaBatchNo(CInventoryDelta):

    def __init__(self, str_timezone):
        super().__init__(str_timezone, CInventoryDelta.TYPE_BATCHNO)
        self.__m_str_item_no = ""
        self.__m_n_itemCategory = 0

    def setParam(self, str_item_no, n_itemCategory):
        if str_item_no:
            self.__m_str_item_no = str_item_no
        if n_itemCategory:
            self.__m_n_itemCategory = n_itemCategory


    def _fill_data(self, obj_data, obj_date, n_kind, lst_in_ids, lst_out_ids):
        dict_data = {
            "warehouse_no": obj_data.warehouse_no,
            "warehouse_displayName": obj_data.warehouse_displayName,
            "date": obj_date,
            "timezone": self.m_str_timezone,
            "kind": EInventoryDeltaKind.BATCHNO,
            "category": obj_data.itemCategory,

            "specified_no": obj_data.batchNumber,
            "specified_name": "",

            "specified_ref_no": obj_data.item_no,
            "specified_ref_name": obj_data.item_name,

            "in_ref_id": lst_in_ids,
            "out_ref_id": lst_out_ids,
            "inPurchaseCount": round(obj_data.inPurchaseCount, 2),
            "inPurchaseAmount": round(obj_data.inPurchaseAmount, 2),
            "inCount": round(obj_data.inCount, 2),
            "inAmount": round(obj_data.inAmount, 2),
            "outCount": round(obj_data.outCount, 2),
            "outAmount": round(obj_data.outAmount, 2)
        }
        return dict_data

    def _get_data(self, obj_session, n_start, n_end):
        pass

    def _get_data_for_without(self, obj_session, n_start, n_end):
        lst_where = self.__fill_query_params_rec()
        lst_result = (
                obj_session.query(
                    CTableInventoryRec.warehouse_no,
                    CTableInventoryRec.warehouse_displayName,
                    CTableInventoryRec.source,
                    CTableInventoryRec.item_no,
                    CTableInventoryRec.item_name,
                    CTableInventoryRec.item_ref_no,
                    CTableInventoryRec.item_ref_displayName,
                    CTableInventoryRec.itemCategory,
                    CTableInventoryRec.batchNumber,
                    func.sum(
                        case((CTableInventoryRec.category == EInventoryCategory.IN,
                              CTableInventoryRec.count * CTableInventoryRec.price), else_=0)
                    ).label("inAmount"),
                    func.sum(
                        case((CTableInventoryRec.category == EInventoryCategory.IN,
                              CTableInventoryRec.count), else_=0)
                    ).label("inCount"),
                    func.sum(
                        case((CTableInventoryRec.category == EInventoryCategory.OUT,
                              CTableInventoryRec.count * CTableInventoryRec.price), else_=0)
                    ).label("outAmount"),
                    func.sum(
                        case((CTableInventoryRec.category == EInventoryCategory.OUT,
                              CTableInventoryRec.count), else_=0)
                    ).label("outCount")
                )
                .filter(*lst_where)
                .filter(CTableInventoryRec.itemType == EItemType.NEW,
                        CTableInventoryRec.date.between(n_start, n_end))
                .group_by(
                    CTableInventoryRec.warehouse_no,
                    CTableInventoryRec.warehouse_displayName,
                    CTableInventoryRec.item_no,
                    CTableInventoryRec.item_name,
                    CTableInventoryRec.item_ref_no,
                    CTableInventoryRec.item_ref_displayName,
                    CTableInventoryRec.itemCategory,
                    CTableInventoryRec.batchNumber
                )
                .all()
            )

        return lst_result

    def _fill_data_for_without(self, obj_data, n_kind):
        dict_data = {
            "warehouse_no": obj_data.warehouse_no,
            "warehouse_displayName": obj_data.warehouse_displayName,
            "timezone": self.m_str_timezone,
            "kind": n_kind,
            #"category": obj_data.itemCategory if n_kind == EInventoryDeltaKind.MATERIAL else 0,
            "category": obj_data.itemCategory,
            "specified_no": obj_data.batchNumber,
            "specified_name": "",

            "specified_ref_no": obj_data.item_no,
            "specified_ref_name": obj_data.item_name,

            "inCount": round(obj_data.inCount, 2),
            "inAmount": round(obj_data.inAmount, 2),
            "outCount": round(obj_data.outCount, 2),
            "outAmount": round(obj_data.outAmount, 2)
        }
        return dict_data

    def _fill_query_params(self):
        lst_where = [CTableInventoryDelta.kind == EInventoryDeltaKind.BATCHNO]
        if self.__m_str_item_no:
            lst_where.append(CTableInventoryDelta.specified_ref_no == self.__m_str_item_no)
        if self.__m_n_itemCategory:
            lst_where.append(CTableInventoryDelta.category == self.__m_n_itemCategory)
        return lst_where

    def __fill_query_params_rec(self):
        lst_where = []
        if self.__m_str_item_no:
            lst_where.append(CTableInventoryRec.item_no == self.__m_str_item_no)
        if self.__m_n_itemCategory:
            lst_where.append(CTableInventoryRec.itemCategory == self.__m_n_itemCategory)
        return lst_where

class CInventoryItemMonth():
    TYPE_ITEMS = 1
    TYPE_BATCHNO = 2
    def __init__(self, str_timezone):
        self.__m_str_timezone = str_timezone

    def retrieve_realTime(self, n_date, n_itemCategory, str_item_no="", f_refresh=False):
        lst_data = []

        try:
            with CDBMgr() as obj_dbmgr:

                obj_session = obj_dbmgr.get_session()
                str_month = self.__get_month(n_date)
                lst_tmp = self.__cal(obj_session, self.TYPE_ITEMS, str_month, n_date, n_itemCategory, str_item_no, f_refresh)
                # 移除 endCount 和 endAmount 同時為 0 的項目
                lst_data = [
                    item for item in lst_tmp
                    if not (item.get("endCount", 0) == 0 and -1 < item.get("endAmount", 0) < 1)
                ]

                lst_tmp_batchno = self.__cal(obj_session, self.TYPE_BATCHNO, str_month, n_date, n_itemCategory, "", f_refresh)
                # retrieve price 計算即期 未稅價錢? 含稅價錢?
                dict_map = self.__get_price(obj_session, lst_data)
                for dict_data in lst_data:
                    dict_data['itemCategory'] = 0
                    dict_data['itemSubCategory'] = 0
                    if dict_data['kind'] != EInventoryDeltaKind.BATCHNO:
                        n_category, n_subCategory, _,  _,  _ = util_get_item_info(dict_data['specified_no'])
                        dict_data['itemCategory'] = n_category
                        dict_data['itemSubCategory'] = n_subCategory
                    dict_data['unit'] = 0
                    dict_data['price'] = 0
                    dict_data['nearExpiryCount'] = 0
                    dict_data['nearExpiryAmount'] = 0
                    dict_data['expiredCount'] = 0
                    dict_data['expiredAmount'] = 0
                    if dict_map and dict_data['specified_no'] in dict_map:
                        dict_data['unit'] = dict_map[dict_data['specified_no']]["unit"]
                        dict_data['price'] = dict_map[dict_data['specified_no']]["price"] * 1

                    #lst_batchno = self.__cal(obj_session, self.TYPE_BATCHNO, str_month, n_date, n_itemCategory, dict_data['specified_no'], f_refresh)
                    lst_batchno = [rec for rec in lst_tmp_batchno if rec['specified_ref_no'] == dict_data['specified_no']]
                    n_nearExpiryCount, n_nearExpiryAmount, n_expiredCount, n_expiredAmount, lst_newBatchNo = self.__gen_batchno_and_cal(obj_session, lst_batchno)
                    if str_item_no:
                        lst_newBatchNo = self.__get_first_in_date(obj_session, lst_newBatchNo)
                    dict_data['batchNo'] = lst_newBatchNo
                    dict_data['nearExpiryCount'] += n_nearExpiryCount
                    dict_data['nearExpiryAmount'] += n_nearExpiryAmount
                    dict_data['expiredCount'] += n_expiredCount
                    dict_data['expiredAmount'] += n_expiredAmount

                    dict_data.pop("id", None)
                    dict_data.pop("date", None)
                    dict_data.pop("timezone", None)
                    dict_data.pop("creationTime", None)


            # check data
            '''
            n_total = 0
            f_value = 0
            n_storage = 0
            for dict_data in lst_data:
                n_count = 0
                n_batch_amount = 0
                for dict_batch in dict_data["batchNo"]:
                    n_count += dict_batch["endCount"]
                    n_total += dict_batch["endAmount"]
                    n_batch_amount += dict_batch["endAmount"]
                if dict_data["endCount"] != n_count:
                    for dict_batch in dict_data["batchNo"]:
                        str_on = dict_batch["specified_no"]
                        f_count = round(dict_batch["endCount"], 2)
                        #print(f"{str_on}   {f_count}")
                    #print("{} {} {} {}".format(dict_data["specified_no"], round(dict_data["endCount"],2),
                    #      round(n_count,2), dict_data["specified_name"]))

                #f_tax = round(n_batch_amount * 1, 0)

                f_tax = round(n_batch_amount, 0)
                f_value += (dict_data["endAmount"] - f_tax)
               
                if round(dict_data["endAmount"] - f_tax, 2) != 0:
                    for dict_batch in dict_data["batchNo"]:
                        str_on = dict_batch["specified_no"]
                        f_count = round(dict_batch["endCount"], 2)
                        #print(f"{str_on}   {f_count}")
                    print("金額不相等 {} {} {} {} {} {} {} {}".format(
                                                           round(dict_data["endAmount"] - f_tax, 2),
                                                            dict_data["specified_no"], dict_data["specified_name"],
                                                           round(dict_data["endCount"], 2),
                                                           round(n_count, 2),
                                                           round(dict_data["endCount"] - n_count, 2),
                                                           round(dict_data["endAmount"], 2),
                                                           f_tax))

              
                if round(dict_data["endCount"] - n_count, 2) != 0:
                    for dict_batch in dict_data["batchNo"]:
                        str_on = dict_batch["specified_no"]
                        f_count = round(dict_batch["endCount"], 2)
                        #print(f"{str_on}   {f_count}")
                    print("{} {} {} {} {} {} {} {}".format(round(dict_data["endCount"] - n_count, 2),
                                                  dict_data["specified_no"], dict_data["specified_name"],
                                                  round(dict_data["endCount"], 2),
                                                  round(n_count, 2),
                                                  round(dict_data["endAmount"], 2),
                                                    f_tax,
                                                    round(dict_data["endAmount"]-f_tax, 2)))
                
                n_storage += round(dict_data["endAmount"], 2)
            print("batch total:{} {} {}".format(round(n_storage, 0), round(n_total, 0), round(n_storage- n_total, 0)))
            '''
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_data

    def update(self, n_date):
        pass

    def calculate(self, n_type, n_itemCategory, n_startTime, n_endTime, f_isCommit=False, f_refresh=False):
        lst_data = []

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_month = self.__retrieve_month(n_startTime, n_endTime)
                for str_month in lst_month:
                    lst_tmp = self.__cal(obj_session, n_type, str_month, 0, n_itemCategory, "", f_refresh)
                    if f_isCommit:
                        self.__commit(lst_tmp)
                    lst_data.extend(lst_tmp)


        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_data

    def __gen_batchno_and_cal(self, obj_session, lst_batchno):
        n_nearExpiryCount = 0
        n_nearExpiryAmount = 0
        n_expiredCount = 0
        n_expiredAmount = 0
        lst_data = []
        if len(lst_batchno) > 0:
            # 移除 endCount 和 endAmount 同時為 0 的項目
            lst_data = [
                item for item in lst_batchno
                if not (item.get("endCount", 0) == 0 and -1 < item.get("endAmount", 0) < 1)
            ]

            lst_nos = [dict_data["specified_no"] for dict_data in lst_data]
            if lst_nos:
                n_now = util_retrieve_now_time()
                lst_tmp = (
                    obj_session.query(CTableBatchNumber)
                    .filter(
                        CTableBatchNumber.no.in_(lst_nos)
                    )
                    .all()
                )


                for dict_data in lst_data:
                    dict_data['itemType'] = 0
                    dict_data['validDate'] = 0
                    dict_data['itemSubCategory'] = 0
                    dict_data['nearExpiryCount'] = 0
                    dict_data['nearExpiryAmount'] = 0
                    dict_data['expiredCount'] = 0
                    dict_data['expiredAmount'] = 0
                    #資料庫尋找即期商品/過期商品
                    for obj_data in lst_tmp:
                        if obj_data.no == dict_data["specified_no"]:
                            dict_data['itemType'] = obj_data.itemType
                            dict_data['validDate'] = obj_data.validDate
                            dict_data['itemSubCategory'] = obj_data.itemSubCategory
                            n_validDays = 0
                            if obj_data.validDays:
                                n_validDays = obj_data.validDays * 28800
                            if obj_data.validDate:
                                if  (obj_data.validDate - n_now) < 0:
                                    n_expiredCount += dict_data['endCount']
                                    n_expiredAmount += dict_data['endAmount']
                                    dict_data['expiredCount'] = dict_data['endCount']
                                    dict_data['expiredAmount'] = dict_data['endAmount']
                                else:
                                    if (obj_data.validDate - n_now) <= n_validDays:  # 86400/3 轉換成秒再取三分之一
                                        n_nearExpiryCount += dict_data['endCount']
                                        n_nearExpiryAmount += dict_data['endAmount']
                                        dict_data['nearExpiryCount'] = dict_data['endCount']
                                        dict_data['nearExpiryAmount'] = dict_data['endAmount']
                            break
                    dict_data.pop("date", None)
                    dict_data.pop("timezone", None)

        return n_nearExpiryCount, n_nearExpiryAmount, n_expiredCount, n_expiredAmount, lst_data

    def __get_first_in_date(self, obj_session, lst_data):

        for dict_data in lst_data:
            obj_rec = (
                obj_session.query(
                    CTableInventoryRec.group,
                    func.min(CTableInventoryRec.date).label('firstInDate')
                )
                .filter(
                    CTableInventoryRec.batchNumber == dict_data["specified_no"],
                    CTableInventoryRec.warehouse_no == dict_data["warehouse_no"],
                    CTableInventoryRec.category == EInventoryCategory.IN
                )
                .group_by(CTableInventoryRec.group)
                .order_by(CTableInventoryRec.date.asc())
                .first()
            )
            dict_data["firstInDate"] = obj_rec.firstInDate if obj_rec else 0


        return lst_data

    def __get_month(self, n_Time: int) -> str:
        obj_tz = ZoneInfo(self.__m_str_timezone)  # 例如 Asia/Taipei
        # 把 UTC timestamp 轉換成當地時間
        dt_local = datetime.fromtimestamp(n_Time, tz=ZoneInfo("UTC")).astimezone(obj_tz)
        str_month = dt_local.strftime("%Y-%m")
        return str_month

    def __get_price(self, obj_session, lst_data):
        from collections import defaultdict
        dict_map = {}
        lst_results = []

        # 建立以 kind 為 key 的 dict，值為指定的 specified_no 列表
        dict_no = defaultdict(list)

        for item in lst_data:
            kind = item.get("kind")
            specified_no = item.get("specified_no")
            dict_no[kind].append(specified_no)
        lst_price = []
        for n_kind, lst_no in dict_no.items():
            if n_kind == 1:
                lst_tmp = (
                    obj_session.query(CTableMaterialPrice)
                    .with_entities(CTableMaterialPrice.item_no,
                                    CTableMaterialPrice.warehouseUnitWeight,
                                   CTableMaterialPrice.warehousePriceWeight,
                                   CTableMaterialPrice.warehouseUnitLength,
                                   CTableMaterialPrice.warehousePriceLength,
                                   CTableMaterialPrice.warehouseUnitCount,
                                   CTableMaterialPrice.warehousePriceCount
                                   )
                    .filter(CTableMaterialPrice.item_no.in_(lst_no))
                    .all()
                )

                for row in lst_tmp:
                    n_unit = 0
                    f_price = 0
                    n_w_unit = row[1]
                    n_l_unit = row[3]
                    n_c_unit = row[5]
                    if n_w_unit:
                        n_unit = n_w_unit
                        f_price = row[2]
                    elif n_l_unit:
                        n_unit = n_l_unit
                        f_price = row[4]
                    elif n_c_unit:
                        n_unit = n_c_unit
                        f_price = row[6]
                    lst_price.append((row[0], n_unit, f_price))
            else:
                obj_table = CTableInproductPrice if n_kind == 2 else CTableProductPrice
                lst_tmp = (
                    obj_session.query(obj_table)
                    .with_entities(obj_table.item_no,
                                    obj_table.warehouseUnit,
                                   obj_table.warehousePrice)
                    .filter(obj_table.item_no.in_(lst_no))
                    .all()
                )
                lst_price.extend(lst_tmp)

        if lst_price:
            dict_map = {
                row[0]: {"unit": row[1], "price": row[2]}
                for row in lst_price
            }
        return dict_map


    def __cal(self, obj_session, n_type, str_month, n_specified_end, n_itemCategory, str_item_no, f_refresh):
        from datetime import datetime, date
        from dateutil.relativedelta import relativedelta

        lst_data = []
        obj_date = datetime.strptime(str_month, '%Y-%m').date()
        lst_where = self.__fill_query_params(n_type, n_itemCategory, str_item_no)

        # 前一個月
        #obj_prev_month = obj_date - relativedelta(months=1)
        obj_latest_month = (obj_session
                            .query(func.max(getattr(CTableInventoryItemMonthStatistic, "date")))
                            .filter(*lst_where)
                            .scalar())

        if not obj_latest_month:
            #obj_latest_month = date(2024,1,1)
            obj_prev_month = None
        else:
            # 查看前一個月有沒有資料
            if obj_date < obj_latest_month:
                obj_prev_month = obj_date
            if obj_date == obj_latest_month:
                obj_prev_month = obj_latest_month
            if obj_latest_month < obj_date:
                obj_prev_month = obj_latest_month

        lst_obj_pre = []
        if obj_prev_month:
            # 取得有紀錄的endCount/endAmount
            lst_obj_pre = (
                obj_session.query(
                    CTableInventoryItemMonthStatistic
                )
                .filter(*lst_where)
                .filter(
                    CTableInventoryItemMonthStatistic.date == obj_prev_month, #str_prev_month,
                    CTableInventoryItemMonthStatistic.timezone == self.__m_str_timezone
                )
                .all()
            )

        lst_cal = []  # 未稅的價錢
        f_cal = False
        if obj_prev_month:
            n_month_diff = (obj_date.year - obj_prev_month.year) * 12 + (obj_date.month - obj_prev_month.month)
            #print("n_month_diff", n_type, n_month_diff)
            if n_month_diff != 0:
                f_cal = True
                if n_month_diff == 1:
                    n_start, n_end = self.__get_month_utc_range(obj_date, obj_date)
                else:
                    obj_start_month = obj_prev_month + relativedelta(months=1)
                    n_start, n_end = self.__get_month_utc_range(obj_start_month, obj_date)
                n_end = n_specified_end if n_specified_end else n_end
        else:
            f_cal = True
            n_start, n_end = self.__get_month_utc_range(obj_date, obj_date)
            n_end = n_specified_end if n_specified_end else n_end


        if f_cal:
            if n_type == self.TYPE_ITEMS:
                obj_inv = CInventoryDeltaItem(self.__m_str_timezone)
                obj_inv.setParam(str_item_no, n_itemCategory)
                lst_cal = obj_inv.retrieve_items_total(n_start, n_end)
            else:
                obj_inv = CInventoryDeltaBatchNo(self.__m_str_timezone)
                obj_inv.setParam(str_item_no, n_itemCategory)
                lst_cal = obj_inv.retrieve_items_total(n_start, n_end)

        lst_pre = [] # lst_pre 含稅的價錢, lst_cal 不含稅價錢
        for obj_pre in lst_obj_pre:
            dict_pre = object_as_dict(obj_pre)
            lst_pre.append(dict_pre)
        lst_data = self.__merge_lists(str_month, lst_pre, lst_cal)

        '''
        n_inAmount = 0
        n_outAmount = 0
        n_inPurchaseAmount = 0
        for obj_tmp in lst_cal:
            print(obj_tmp["specified_no"], round(1*(obj_tmp["inAmount"] - obj_tmp["outAmount"]),2))
            n_inAmount += obj_tmp["inAmount"]
            if "inPurchaseAmount" in obj_tmp:
                n_inPurchaseAmount += obj_tmp["inPurchaseAmount"]
            n_outAmount += obj_tmp["outAmount"]
        print("result", n_inAmount, n_outAmount,  round(1*n_inPurchaseAmount,2), round(1*(n_inAmount - n_outAmount),2))
       
        print("====")
        for obj_tmp in lst_pre:
           print(obj_tmp["specified_no"], obj_tmp["endAmount"])

        print("====")
        '''
        return lst_data


    def __get_month_utc_range(self, obj_start, obj_end):
        import calendar
        # 台灣時區
        tz = ZoneInfo(self.__m_str_timezone)

        year = obj_start.year
        month = obj_start.month
        start_local = datetime(year, month, 1, 0, 0, 0, tzinfo=tz)
        if obj_start == obj_end:
            _, days_in_month = calendar.monthrange(year, month)
            end_local = datetime(year, month, days_in_month, 23, 59, 59, tzinfo=tz)
        else:
            n_endYear = obj_end.year
            n_endMonth = obj_end.month
            _, days_in_month = calendar.monthrange(n_endYear, n_endMonth)
            end_local = datetime(n_endYear, n_endMonth, days_in_month, 23, 59, 59, tzinfo=tz)

        # 轉成 UTC timestamp
        return int(start_local.timestamp()), int(end_local.timestamp())

    def __merge_lists(self, str_date, lst_a, lst_b):
        lst_result = []
        obj_date = datetime.strptime(str_date, '%Y-%m').date()
        # lst_a含稅價 lst_b未稅價
        # 建立 lst_b 的索引表方便比對
        b_dict = {
            (item["warehouse_no"], item["specified_no"]): item
            for item in lst_b
        }

        matched_keys = set()

        for a_item in lst_a:
            key = (a_item["warehouse_no"], a_item["specified_no"])
            b_item = b_dict.get(key)

            if b_item:
                # 有符合的，依照 lst_a 為主，並做計算
                merged = a_item.copy()
                merged["date"] = obj_date
                merged["endCount"] = round((
                        a_item.get("endCount", 0.0)
                        + b_item.get("inCount", 0.0)
                        - b_item.get("outCount", 0.0)
                ),2)
                f_amount = ((b_item.get("inAmount", 0.0) - b_item.get("outAmount", 0.0)) * 1)
                merged["endAmount"] = round(a_item.get("endAmount", 0.0) + f_amount, 2)

                lst_result .append(merged)
                matched_keys.add(key)
            else:
                # 只出現在 A 裡，直接加入
                dict_atmp = a_item.copy()
                dict_atmp["date"] = obj_date
                lst_result .append(dict_atmp)

        # 處理只出現在 B 裡的項目
        for b_item in lst_b:
            key = (b_item["warehouse_no"], b_item["specified_no"])
            if key not in matched_keys:
                new_item = {
                    "warehouse_no": b_item["warehouse_no"],
                    "warehouse_displayName": b_item.get("warehouse_displayName"),
                    "date": obj_date,
                    "timezone": b_item.get("timezone"),
                    "kind": b_item.get("kind"),
                    "category": b_item.get("category"),
                    "specified_no": b_item["specified_no"],
                    "specified_name": b_item.get("specified_name"),
                    "specified_ref_no": b_item.get("specified_ref_no"),
                    "specified_ref_name": b_item.get("specified_ref_name"),
                    "startCount": 0.0,
                    "startAmount": 0.0,
                    "inCount": 0.0,
                    "inAmount": 0.0,
                    "endCount": round(b_item.get("inCount", 0.0) - b_item.get("outCount", 0.0),2),
                    "endAmount": round((b_item.get("inAmount", 0.0) - b_item.get("outAmount", 0.0)) * 1 ,2)
                }
                lst_result .append(new_item)
        return lst_result


    def __commit(self, lst_data):
        for dict_data in lst_data:
            self.__insert_update_db(dict_data)

    def __insert_update_db(self, dict_data):
        str_id = ""

        with CDBMgr() as obj_dbmgr:
            str_uuid = str(uuid.uuid4()).replace("-", "")
            new_data = CTableInventoryItemMonthStatistic(
                id=str_uuid,
                warehouse_no=dict_data["warehouse_no"],
                warehouse_displayName=dict_data["warehouse_displayName"],
                date=dict_data["date"],
                timezone=dict_data["timezone"],
                kind=dict_data["kind"],
                category=dict_data["category"],
                specified_no=dict_data["specified_no"],
                specified_name = dict_data["specified_name"],
                specified_ref_no = dict_data["specified_ref_no"],
                specified_ref_name = dict_data["specified_ref_name"],
                unit=EUnit.KILOGRAM,
                startAmount=0,
                startCount=0,
                inAmount=0,
                inCount=0,
                endCount=dict_data["endCount"],
                endAmount=dict_data["endAmount"],
                creationTime=util_retrieve_now_time()
            )

            if obj_dbmgr.insert(new_data) == EErrorCode.ERROR_SUCCESS:
                str_id = str_uuid
            else:
                str_message = 'failed to create inventory item month'
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
                dict_tmp = {"startCount": 0,
                            "startAmount": 0,
                            "inCount": 0,
                            "inAmount": 0,
                            "endCount": dict_data["endCount"],
                            "endAmount": dict_data["endAmount"]}
                if obj_dbmgr.update(CTableInventoryItemMonthStatistic,
                                    [CTableInventoryItemMonthStatistic.warehouse_no == dict_data["warehouse_no"],
                                             CTableInventoryItemMonthStatistic.date == dict_data["date"],
                                             CTableInventoryItemMonthStatistic.timezone == dict_data["timezone"],
                                             CTableInventoryItemMonthStatistic.category == dict_data["category"],
                                             CTableInventoryItemMonthStatistic.specified_no == dict_data["specified_no"]],
                                    dict_tmp) != EErrorCode.ERROR_SUCCESS:
                    str_message = 'failed to update inventory month'
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

    def __fill_query_params(self, n_type, n_itemCategory, str_item_no):
        if n_type == self.TYPE_BATCHNO:
            lst_where = [CTableInventoryItemMonthStatistic.kind == EInventoryDeltaKind.BATCHNO]
            if str_item_no:
                lst_where.append(CTableInventoryItemMonthStatistic.specified_ref_no == str_item_no)
            if n_itemCategory:
                lst_where.append(CTableInventoryItemMonthStatistic.category == n_itemCategory)
        if n_type == self.TYPE_ITEMS:
            lst_where = [CTableInventoryItemMonthStatistic.kind != EInventoryDeltaKind.BATCHNO]
            if str_item_no:
                lst_where.append(CTableInventoryItemMonthStatistic.specified_no == str_item_no)
            if n_itemCategory:
                if n_itemCategory == EItemCategory.PRODUCT:
                    lst_where.append(CTableInventoryItemMonthStatistic.kind == EInventoryDeltaKind.PRODUCT)
                if n_itemCategory == EItemCategory.INPRODUCT:
                    lst_where.append(CTableInventoryItemMonthStatistic.kind == EInventoryDeltaKind.INPRODUCT)
                if n_itemCategory == EItemCategory.PM:
                    lst_where.append(CTableInventoryItemMonthStatistic.kind == EInventoryDeltaKind.MATERIAL)
                    lst_where.append(CTableInventoryItemMonthStatistic.category == EMaterialType.PM)
                if n_itemCategory == EItemCategory.AF:
                    lst_where.append(CTableInventoryItemMonthStatistic.kind == EInventoryDeltaKind.MATERIAL)
                    lst_where.append(CTableInventoryItemMonthStatistic.category == EMaterialType.AF)
                if n_itemCategory == EItemCategory.MA:
                    lst_where.append(CTableInventoryItemMonthStatistic.kind == EInventoryDeltaKind.MATERIAL)
                    lst_where.append(CTableInventoryItemMonthStatistic.category == EMaterialType.MA)
        return lst_where


class CInventoryMonth(IInventoryStatistic):
    # 原料/物料/膠捲/在製品/製成品 總和
    def __init__(self, str_timezone):
        super().__init__(str_timezone)

    def retrieve(self, n_startTime, n_endTime):
        lst_data = []

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_month = self.__retrieve_month(n_startTime, n_endTime)
                for str_month in lst_month:
                    lst_tmp = (
                        obj_session.query(
                            CTableInventoryMonthStatistic
                        )
                        .filter(
                            func.date_format(CTableInventoryMonthStatistic.date, '%Y-%m') == str_month,
                            CTableInventoryMonthStatistic.timezone == self.m_str_timezone
                        )
                        .all()
                    )
                    if lst_tmp:
                        for obj_tmp in lst_tmp:
                            dict_tmp = object_as_dict(obj_tmp)
                            lst_data.append(dict_tmp)
                    else:
                        lst_temp = self.__cal(obj_session, str_month)
                        if lst_temp:
                            lst_data.extend(lst_temp)

                for dict_tmp in lst_data:
                    dict_tmp["year"] = dict_tmp["date"].year
                    dict_tmp["month"] = dict_tmp["date"].month
                    dict_tmp.pop("id", None)
                    dict_tmp.pop("date", None)
                    dict_tmp.pop("timezone", None)
                    dict_tmp.pop("creationTime", None)
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_data

    def update(self, n_date):
        pass

    def calculate(self, n_startTime, n_endTime, f_isCommit=False):
        lst_data = []

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                # 只能計算單月
                lst_month = self.__retrieve_month(n_startTime, n_endTime)
                for str_month in lst_month:
                    lst_tmp = self.__cal(obj_session, str_month)
                    if f_isCommit:
                        self.__commit(lst_tmp)
                    lst_data.extend(lst_tmp)
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_data
    def __cal(self, obj_session, str_month):
        from datetime import datetime, date
        from dateutil.relativedelta import relativedelta

        lst_data = []
        obj_date = datetime.strptime(str_month, '%Y-%m').date()
        # 取得 原料/物料/膠捲/在製品/製成品的 總和

        lst_all = []  # 全部的類別
        for n_idx in range(EItemCategory.PM, EItemCategory.PRODUCT + 1):
            obj_latest_month = (obj_session
                                .query(func.max(getattr(CTableInventoryMonthStatistic, "date")))
                                .filter(CTableInventoryMonthStatistic.category == n_idx)
                                .scalar())

            if not obj_latest_month:
                # obj_latest_month = date(2024,1,1)
                obj_prev_month = None
            else:
                # 查看前一個月有沒有資料
                if obj_date < obj_latest_month:
                    obj_prev_month = obj_date
                if obj_date == obj_latest_month:
                    obj_prev_month = obj_latest_month
                if obj_latest_month < obj_date:
                    obj_prev_month = obj_latest_month

            lst_cal = []  # 含稅的價錢
            if obj_prev_month:
                n_month_diff = (obj_date.year - obj_prev_month.year) * 12 + (obj_date.month - obj_prev_month.month)
                # print("n_month_diff", n_type, n_month_diff)
                if n_month_diff != 0:
                    f_cal = True
                    if n_month_diff == 1:
                        n_start, n_end = self.__get_month_utc_range(obj_date, obj_date)
                    else:
                        obj_start_month = obj_prev_month + relativedelta(months=1)
                        n_start, n_end = self.__get_month_utc_range(obj_start_month, obj_date)
            else:
                f_cal = True
                n_start, n_end = self.__get_month_utc_range(obj_date, obj_date)

            if f_cal:
                #  由CInventoryDeltaItem判斷哪些月份有Delta, 那些月份沒有
                obj_inv = CInventoryDeltaItem(self.m_str_timezone)
                obj_inv.setParam("", n_idx)
                lst_cal = obj_inv.retrieve_items_total(n_start, n_end)
            if lst_cal:
                # 分群/計算總合
                lst_tmp = self.__cal_total_amount(lst_cal)
                lst_all.extend(lst_tmp)
        if lst_all:
            lst_data = self.__gen_data(obj_session, str_month, lst_all)

        '''

        # 取得 原料/物料/膠捲/在製品/製成品的 總和
        lst_result = (
            obj_session.query(
                CTableInventoryDelta.warehouse_no,
                CTableInventoryDelta.warehouse_displayName,
                CTableInventoryDelta.kind,
                CTableInventoryDelta.category,
                func.round(func.sum(CTableInventoryDelta.inPurchaseAmount), 2).label("total_inPurchaseAmount"),
                func.round(func.sum(CTableInventoryDelta.inAmount), 2).label("total_inAmount"),
                func.round(func.sum(CTableInventoryDelta.outAmount), 2).label("total_outAmount"),
            )
            .filter(func.date_format(CTableInventoryDelta.date, '%Y-%m') == str_month,
                    CTableInventoryDelta.timezone == self.m_str_timezone)
            .group_by(
                CTableInventoryDelta.warehouse_no,
                CTableInventoryDelta.warehouse_displayName,
                CTableInventoryDelta.kind,
                CTableInventoryDelta.category
            )
            .all()
        )

        if lst_result:
            lst_tmp = []
            for obj_result in lst_result:
                if obj_result.kind != EInventoryDeltaKind.BATCHNO:
                    dict_result = {"warehouse_no": obj_result.warehouse_no,
                                   "warehouse_displayName": obj_result.warehouse_displayName,
                                   "kind": obj_result.kind,
                                   "category": obj_result.category,
                                   "inPurchaseAmount": obj_result.total_inPurchaseAmount,
                                   "inAmount": obj_result.total_inAmount,
                                   "outAmount": obj_result.total_outAmount}
                    lst_tmp.append(dict_result)
            lst_data = self.__gen_data(obj_session, str_month, lst_tmp)
        else:
            # 沒有delta
            # 取得最後一個月的資料
            lst_all = [] # 全部的類別
            for n_idx in range(EItemCategory.PM, EItemCategory.PRODUCT + 1):
                obj_latest_month = (obj_session
                                    .query(func.max(getattr(CTableInventoryMonthStatistic, "date")))
                                    .filter(CTableInventoryMonthStatistic.category == n_idx)
                                    .scalar())

                if not obj_latest_month:
                    # obj_latest_month = date(2024,1,1)
                    obj_prev_month = None
                else:
                    # 查看前一個月有沒有資料
                    if obj_date < obj_latest_month:
                        obj_prev_month = obj_date
                    if obj_date == obj_latest_month:
                        obj_prev_month = obj_latest_month
                    if obj_latest_month < obj_date:
                        obj_prev_month = obj_latest_month


                lst_cal = []  # 含稅的價錢
                if obj_prev_month:
                    n_month_diff = (obj_date.year - obj_prev_month.year) * 12 + (obj_date.month - obj_prev_month.month)
                    # print("n_month_diff", n_type, n_month_diff)
                    if n_month_diff != 0:
                        f_cal = True
                        if n_month_diff == 1:
                            n_start, n_end = self.__get_month_utc_range(obj_date, obj_date)
                        else:
                            obj_start_month = obj_prev_month + relativedelta(months=1)
                            n_start, n_end = self.__get_month_utc_range(obj_start_month, obj_date)
                else:
                    f_cal = True
                    n_start, n_end = self.__get_month_utc_range(obj_date, obj_date)

                if f_cal:
                    obj_inv = CInventoryDeltaItem(self.m_str_timezone)
                    obj_inv.setParam("", n_idx)
                    lst_cal = obj_inv.retrieve_items_total(n_start, n_end)
                if lst_cal:
                    # 分群/計算總合
                    lst_tmp = self.__cal_total_amount(lst_cal)
                    lst_all.extend(lst_tmp)
            if lst_all:
                lst_data = self.__gen_data(obj_session, str_month, lst_all)
            '''
        return lst_data

    def __gen_data(self, obj_session, str_month, lst_result):
        lst_data = []
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        obj_date = datetime.strptime(str_month, '%Y-%m').date()

        obj_prev_month = None
        for n_idx1 in range(EInventoryDeltaKind.MATERIAL, EInventoryDeltaKind.PRODUCT + 1):
            obj_latest_month = (obj_session
                                .query(func.max(getattr(CTableInventoryMonthStatistic, "date")))
                                .filter(CTableInventoryMonthStatistic.category == n_idx1)
                                .scalar())
            # 查看前一個月有沒有資料
            if obj_date < obj_latest_month:
                obj_prev_month = obj_date
            if obj_date == obj_latest_month:
                obj_prev_month = obj_latest_month
            if obj_latest_month < obj_date:
                obj_prev_month = obj_latest_month
            if obj_prev_month:
                str_prev_month = obj_prev_month.strftime('%Y-%m-%d')

            # 原物料/在製品/製成品/批號
            for n_idx2 in range(0, 4):
                # 原料/物料/膠捲
                n_category = EItemCategory.NONE
                if n_idx1 == EInventoryDeltaKind.MATERIAL:
                    if n_idx2 == 0:
                        continue
                    else:
                        n_category = n_idx2
                else:
                    if n_idx2 != 0:
                        continue
                    else:
                        if n_idx1 == EInventoryDeltaKind.INPRODUCT:
                            n_category = EItemCategory.INPRODUCT
                        elif n_idx1 == EInventoryDeltaKind.PRODUCT:
                            n_category = EItemCategory.PRODUCT
                # 倉庫要分群
                lst_filter = self.__group_warehouse(n_idx1, n_idx2, lst_result)
                dict_data = {
                    "warehouse_no": "",
                    "warehouse_displayName": "",
                    "date": obj_date,
                    "timezone": self.m_str_timezone,
                    "category": n_category,
                    "startAmount": 0,
                    "inPurchaseAmount": 0,
                    "inAmount": 0,
                    "outAmount": 0,
                    "endAmount": 0
                }
                if lst_filter:
                    for dict_warehouse in lst_filter:
                        for dict_filter in dict_warehouse["items"]:
                            dict_data1 = deepcopy(dict_data)
                            # 取得上個月的endCount/endAmount
                            obj_pre = (
                                obj_session.query(
                                    CTableInventoryMonthStatistic
                                )
                                .filter(
                                    CTableInventoryMonthStatistic.date == str_prev_month,
                                    CTableInventoryMonthStatistic.timezone == self.m_str_timezone,
                                    CTableInventoryMonthStatistic.warehouse_no == dict_filter["warehouse_no"],
                                    CTableInventoryMonthStatistic.category == n_category
                                )
                                .first()
                            )
                            f_startAmount = round(obj_pre.endAmount if obj_pre else 0)
                            f_amount = round((dict_filter["inAmount"]  - dict_filter["outAmount"] ) * 1, 2)
                            dict_data1["warehouse_no"] = dict_filter["warehouse_no"]
                            dict_data1["warehouse_displayName"] = dict_filter["warehouse_displayName"]
                            dict_data1["startAmount"] = f_startAmount
                            dict_data1["inPurchaseAmount"] = round(dict_filter["inPurchaseAmount"]  * 1)
                            dict_data1["inAmount"] = round(dict_filter["inAmount"]  * 1, 2)
                            dict_data1["outAmount"] = round(dict_filter["outAmount"] * 1, 2)
                            dict_data1["endAmount"] = round(f_startAmount + f_amount)
                            lst_data.append(dict_data1)
                else:
                    lst_data.append(dict_data)

        return lst_data

    def __group_warehouse(self, n_kind, n_category, lst_result):
        from collections import defaultdict
        lst_filter = [r for r in lst_result if r["kind"] == n_kind and r["category"] == n_category]

        grouped = defaultdict(lambda: {'warehouse_displayName': '', 'items': []})
        for item in lst_filter:
            wh_no = item['warehouse_no']
            grouped[wh_no]['warehouse_displayName'] = item['warehouse_displayName']
            grouped[wh_no]['items'].append(item)

        # 轉換成 list 結構
        lst_group = [
            {'warehouse_no': wh_no, 'warehouse_displayName': v['warehouse_displayName'], 'items': v['items']}
            for wh_no, v in grouped.items()
        ]

        return lst_group


    def __cal_total_amount(self, lst_cal):
        from collections import defaultdict
        # 建立分群字典
        grouped = defaultdict(lambda: {'inPurchaseAmount': 0.0, 'inAmount': 0.0, 'outAmount': 0.0})

        for item in lst_cal:
            key = (item['warehouse_no'], item['warehouse_displayName'], item['kind'], item['category'])
            grouped[key]['inPurchaseAmount'] += item.get('inPurchaseAmount', 0.0)
            grouped[key]['inAmount'] += item.get('inAmount', 0.0)
            grouped[key]['outAmount'] += item.get('outAmount', 0.0)

        # 轉成 list 輸出
        lst_result = []
        for (wh_no, wh_name, kind, category), sums in grouped.items():
            lst_result.append({
                'warehouse_no': wh_no,
                'warehouse_displayName': wh_name,
                'kind': kind,
                'category': category,
                **sums
            })

        return lst_result


    def __commit(self, lst_data):
        for dict_data in lst_data:
            self.__insert_update_db(dict_data)

    def __insert_update_db(self, dict_data):
        str_id = ""
        with CDBMgr() as obj_dbmgr:
            str_uuid = str(uuid.uuid4()).replace("-", "")
            new_data = CTableInventoryMonthStatistic(
                id=str_uuid,
                warehouse_no=dict_data["warehouse_no"],
                warehouse_displayName=dict_data["warehouse_displayName"],
                date=dict_data["date"],
                timezone=dict_data["timezone"],
                category=dict_data["category"],
                startAmount=int(dict_data["startAmount"]),
                inPurchaseAmount=int(dict_data["inPurchaseAmount"]),
                inAmount=int(dict_data["inAmount"]),
                outAmount=int(dict_data["outAmount"]),
                endAmount=int(dict_data["endAmount"]),
                creationTime=util_retrieve_now_time()
            )
            if obj_dbmgr.insert(new_data) == EErrorCode.ERROR_SUCCESS:
                str_id = str_uuid
            else:
                str_message = 'failed to create inventory month'
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
                dict_tmp = {"startAmount": int(dict_data["startAmount"]),
                            "inPurchaseAmount": int(dict_data["inPurchaseAmount"]),
                            "inAmount": int(dict_data["inAmount"]),
                            "outAmount": int(dict_data["outAmount"]),
                            "endAmount": int(dict_data["endAmount"])}
                if obj_dbmgr.update(CTableInventoryMonthStatistic,
                                    [CTableInventoryMonthStatistic.warehouse_no == dict_data["warehouse_no"],
                                             CTableInventoryMonthStatistic.date == dict_data["date"],
                                             CTableInventoryMonthStatistic.timezone == dict_data["timezone"],
                                             CTableInventoryMonthStatistic.category == dict_data["category"]],
                                    dict_tmp) != EErrorCode.ERROR_SUCCESS:
                    str_message = 'failed to update inventory month'
                    CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
        return str_id
    def __retrieve_month(self, n_startTime: int, n_endTime: int) -> list[dict]:
        lst_result = []
        obj_tz = ZoneInfo(self.m_str_timezone)

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

    def __get_month_utc_range(self, obj_start, obj_end):
        import calendar
        # 台灣時區
        tz = ZoneInfo(self.m_str_timezone)

        year = obj_start.year
        month = obj_start.month
        start_local = datetime(year, month, 1, 0, 0, 0, tzinfo=tz)
        if obj_start == obj_end:
            _, days_in_month = calendar.monthrange(year, month)
            end_local = datetime(year, month, days_in_month, 23, 59, 59, tzinfo=tz)
        else:
            n_endYear = obj_end.year
            n_endMonth = obj_end.month
            _, days_in_month = calendar.monthrange(n_endYear, n_endMonth)
            end_local = datetime(n_endYear, n_endMonth, days_in_month, 23, 59, 59, tzinfo=tz)

        # 轉成 UTC timestamp
        return int(start_local.timestamp()), int(end_local.timestamp())

    '''
    def __gen_data(self, obj_session, str_month, lst_result):
        lst_data = []
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        obj_date = datetime.strptime(str_month, '%Y-%m').date()

        # 前一個月
        obj_prev_month = obj_date - relativedelta(months=1)

        # 格式化為字串
        str_prev_month = obj_prev_month.strftime('%Y-%m-%d')

        for n_idx1 in range(EInventoryDeltaKind.MATERIAL, EInventoryDeltaKind.PRODUCT+1):
            # 原物料/在製品/製成品/批號
            for n_idx2 in range(0, 4):
                # 原料/物料/膠捲
                n_category = EItemCategory.NONE
                if n_idx1 == EInventoryDeltaKind.MATERIAL:
                    if n_idx2 == 0:
                        continue
                    else:
                        n_category = n_idx2
                else:
                    if n_idx2 != 0:
                        continue
                    else:
                        if n_idx1 == EInventoryDeltaKind.INPRODUCT:
                            n_category = EItemCategory.INPRODUCT
                        elif n_idx1 == EInventoryDeltaKind.PRODUCT:
                            n_category = EItemCategory.PRODUCT

                lst_filter = [r for r in lst_result if r.kind == n_idx1 and r.category == n_idx2]

                dict_data = {
                    "warehouse_no": "",
                    "warehouse_displayName": "",
                    "date": obj_date,
                    "timezone": self.m_str_timezone,
                    "category": n_category,
                    "startAmount": 0,
                    "inPurchaseAmount":0,
                    "inAmount": 0,
                    "outAmount": 0,
                    "endAmount": 0
                }

                if lst_filter:
                    # 第一筆的倉庫? 倉庫要分群
                    obj_data = lst_filter[0]
                    #print(obj_data.warehouse_no, obj_data.kind, obj_data.category)

                    # 取得上個月的endCount/endAmount
                    obj_pre = (
                        obj_session.query(
                            CTableInventoryMonthStatistic
                        )
                        .filter(
                            CTableInventoryMonthStatistic.date == str_prev_month,
                            CTableInventoryMonthStatistic.timezone == self.m_str_timezone,
                            CTableInventoryMonthStatistic.warehouse_no == obj_data.warehouse_no,
                            CTableInventoryMonthStatistic.category == n_category
                        )
                        .first()
                    )
                    f_startAmount = round(obj_pre.endAmount if obj_pre else 0)
                    f_amount = round((obj_data.total_inAmount - obj_data.total_outAmount) * 1, 2)
                    #print(n_category)
                    dict_data["warehouse_no"] = obj_data.warehouse_no
                    dict_data["warehouse_displayName"] = obj_data.warehouse_displayName
                    dict_data["startAmount"] = f_startAmount
                    dict_data["inPurchaseAmount"] = round(obj_data.total_inPurchaseAmount * 1)
                    dict_data["inAmount"] = round(obj_data.total_inAmount* 1)
                    dict_data["outAmount"] = round(obj_data.total_outAmount * 1)
                    dict_data["endAmount"] = round(f_startAmount + f_amount)
                lst_data.append(dict_data)

        return lst_data
    '''