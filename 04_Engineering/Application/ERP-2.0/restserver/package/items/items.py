# coding=utf8
import pytz
import string
from copy import deepcopy
from package.util.util import *
from package.log.log import CLogger
from package.dbwrapper.dbmgr import CDBMgr
import uuid
from package.restserver.api.util import *
from itertools import groupby
from operator import attrgetter


class EPageType(object):
    WEIGHT = 1   #秤重
    COUNT = 2    #數量
    SCAN = 3     #掃條碼


class CItems(object):
    PURCHASE = 1
    MANUFACTURE = 2
    SALES = 3
    OTHER = 4

    def __init__(self, str_register_no, str_timezone):
        self.__m_str_timezone = str_timezone
        self.__m_str_register_no = str_register_no
        self.__m_str_hardwareId, self.__m_n_role = self.__retrieve_role()

        CLogger().log(CLogger.LOG_LEVELINFO, '[%s] (deviceId: %s, deviceRole: %d)'
                  % (self.__class__.__name__,  self.__m_str_hardwareId, self.__m_n_role))

    def get(self, n_type, n_date, n_shift, n_refProcess=0):
        lst_data = []

        try:
            if self.__m_n_role:
                if self.__m_n_role == ELocationType.STORAGE:
                    # 物料不秤重. 最大最小重量
                    if n_type == self.PURCHASE:
                        # 取得進貨單
                        # EDevAction.IN
                        lst_data = self.__gen_data_purchase(n_date, n_shift)
                        # 取得進貨退回單
                        # EDevAction.OUT
                        lst_tmp = self.__gen_data_purchase(n_date, n_shift, True)
                        lst_data.extend(lst_tmp)
                    if n_type == self.MANUFACTURE:
                        # 取得領料單 1張派工單對應到多張領退餘料產單
                        # EDevAction.OUT
                        # 取得餘廢料產單 同一品項產品單, 因多個批號而有多張產品酖
                        # EDevAction.IN
                        lst_data = self.__gen_data_work(n_date, n_shift, n_refProcess)
                    if n_type == self.SALES:
                        # 取得銷貨單
                        # EDevAction.OUT
                        lst_data = self.__gen_data_sale(n_date, n_shift)
                        # 取得銷貨退回單
                        # EDevAction.IN
                        lst_tmp = self.__gen_data_sale(n_date, n_shift, True)
                        lst_data.extend(lst_tmp)
                    if n_type == self.OTHER:
                        # 取得庫存單
                        # EDevAction.IN
                        lst_data = self.__gen_data_other(n_date, n_shift)
                else:
                    if n_type == self.MANUFACTURE:
                        # 取得領料單
                        # EDevAction.IN
                        # 取得餘廢料產單
                        # EDevAction.OUT
                        lst_data = self.__gen_data_work(n_date, n_shift, n_refProcess)
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_data

    def __retrieve_role(self):
        n_role = 0
        str_hardwareId = ""
        if self.__m_str_register_no:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                obj_result = (
                    obj_session.query(CTableDevice)
                    .filter(CTableDevice.no == self.__m_str_register_no)
                    .first()
                )
                if obj_result:
                    n_role = obj_result.role
                    str_hardwareId = obj_result.hardwareId
        return str_hardwareId, n_role

    def __gen_data_purchase(self, n_date, n_shift, f_isReturn=False):
        lst_data = []
        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            n_start, n_end = self.__retrieve_time(n_date, n_shift)
            n_condition = EGoodsReceiptNoteCategory.NORMAL if not f_isReturn else EGoodsReceiptNoteCategory.RETURN
            # 進貨
            lst_obj_result = (
                obj_session.query(CTableGoodsReceiptNote)
                .filter(CTableGoodsReceiptNote.date.between(n_start, n_end),
                        CTableGoodsReceiptNote.category == n_condition)
                .all()
            )

            for obj_result in lst_obj_result:
                if f_isReturn:
                    lst_batchno, n_itemType, n_itemCategory = self.__retrieve_serialno(obj_session, obj_result.no)
                else:
                    obj_batch = (
                        obj_session.query(CTableBatchNumber)
                        .filter(CTableBatchNumber.ref_no == obj_result.no)
                        .first()
                    )

                    lst_batchno = [
                        {
                            "batchNo": obj_batch.no if obj_batch else "",
                            "validDateTimestamp": obj_batch.validDate if obj_batch else 0,
                            "serialNos": []
                        }
                    ] if obj_batch else []
                    n_itemType = obj_batch.itemType if obj_batch else 0
                    n_itemCategory = obj_batch.itemCategory if obj_batch else 0
                n_pageType = EPageType.SCAN if f_isReturn else EPageType.COUNT if n_itemCategory == EItemCategory.MA else EPageType.WEIGHT
                dict_data = {
                    "action": EDevAction.OUT if f_isReturn else EDevAction.IN,
                    "refNo": obj_result.no,
                    "refNoSec": "",
                    "refDateTimestamp": obj_result.date,
                    "itemNo": obj_result.item_no,
                    "itemName": obj_result.item_name,
                    "itemVendor": obj_result.item_ref_displayName,
                    "itemType": n_itemCategory,
                    "itemCategory": n_itemType,
                    "itemAmount": obj_result.expectedCount,
                    "itemAmountUnit": obj_result.unit,
                    "itemComment": obj_result.comment,
                    "itemPageType": n_pageType,
                    "itemMaxWeight": 0,
                    "itemMinWeight": 0,
                    "itemBatchNo": lst_batchno
                }
                lst_data.append(dict_data)

        return lst_data

    def __gen_data_work(self, n_date, n_shift, n_refProcess):
        #在製品/製成品 有最大最小
        lst_tmp = []
        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            n_start, n_end = self.__retrieve_time(n_date, n_shift)

            # 領退餘廢產
            if n_refProcess:
                lst_obj_result = (
                    obj_session.query(CTableProcessOrder)
                    .filter(CTableProcessOrder.date.between(n_start, n_end),
                            CTableProcessOrder.refProcess == n_refProcess)
                    .all()
                )
            else:
                lst_obj_result = (
                    obj_session.query(CTableProcessOrder)
                    .filter(CTableProcessOrder.date.between(n_start, n_end))
                    .all()
                )

            for obj_result in lst_obj_result:
                lst_batchno = []
                n_action = 0
                n_itemType = 0
                lst_batchno = []
                n_pageType = EPageType.SCAN
                if obj_result.category == EProcessOrderCategory.RECEIVE:
                    n_action = EDevAction.OUT if self.__m_n_role == ELocationType.STORAGE else EDevAction.IN
                    n_pageType = EPageType.SCAN
                if obj_result.category in [EProcessOrderCategory.RETURN, EProcessOrderCategory.REMAIN, EProcessOrderCategory.WASTE, EProcessOrderCategory.PRODUCT]:
                    n_action = EDevAction.IN if self.__m_n_role == ELocationType.STORAGE else EDevAction.OUT
                    n_pageType = EPageType.SCAN if self.__m_n_role == ELocationType.STORAGE else EPageType.WEIGHT
                if obj_result.category in [EProcessOrderCategory.RECEIVE, EProcessOrderCategory.RETURN]:
                    # 領/退料
                    lst_batchno, n_itemType, _ = self.__retrieve_serialno(obj_session, obj_result.no)
                else:
                    # 餘/廢/產料
                    lst_obj_batch = (
                        obj_session.query(CTableBatchNumber)
                        .filter(CTableBatchNumber.ref_no == obj_result.no)
                        .all()
                    )

                    for obj_batch in lst_obj_batch:
                        n_itemType = obj_batch.itemType
                        lst_batchno.append({"batchNo": obj_batch.no,
                                            "validDateTimestamp": obj_batch.validDate,
                                            "serialNos": []})

                dict_data = {
                    "action": n_action,
                    "refNo": obj_result.work_order_no,
                    "refNoSec": obj_result.no,
                    "refDateTimestamp": obj_result.date,
                    "refProcess": obj_result.refProcess,
                    "itemNo": obj_result.item_no,
                    "itemName": obj_result.item_name,
                    "itemVendor": obj_result.item_ref_displayName,
                    "itemType": obj_result.itemCategory,
                    "itemCategory": n_itemType,
                    "itemAmount": obj_result.expectedCount, #總數
                    "itemAmountUnit": obj_result.unit,
                    "itemComment": obj_result.comment,
                    "itemPageType": n_pageType,
                    "itemMaxWeight": 0,
                    "itemMinWeight": 0,
                    "itemBatchNo": lst_batchno
                }
                lst_tmp.append(dict_data)
            lst_data = self.__merge_items(lst_tmp)
            lst_data = sorted(lst_data, key=lambda x: x['action'])
        return lst_data


    def __gen_data_sale(self, n_date, n_shift, f_isReturn=False):
        lst_data = []
        n_pageType = EPageType.SCAN
        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            n_start, n_end = self.__retrieve_time(n_date, n_shift)
            n_condition = EShippingOrderCategory.NORMAL if not f_isReturn else EShippingOrderCategory.RETURN
            # 銷貨/銷貨退回
            lst_obj_result = (
                obj_session.query(CTableShippingOrder)
                .filter(CTableShippingOrder.date.between(n_start, n_end),
                        CTableShippingOrder.category == n_condition)
                .all()
            )
            for obj_result in lst_obj_result:
                if not f_isReturn:
                    lst_batchno, n_itemType, n_itemCategory = self.__retrieve_serialno(obj_session, obj_result.no)
                else:
                    obj_batch = (
                        obj_session.query(CTableBatchNumber)
                        .filter(CTableBatchNumber.ref_no == obj_result.no)
                        .first()
                    )

                    lst_batchno = [
                        {
                            "batchNo": obj_batch.no if obj_batch else "",
                            "validDateTimestamp": obj_batch.validDate if obj_batch else 0,
                            "serialNos": []
                        }
                    ] if obj_batch else []
                    n_itemType = obj_batch.itemType if obj_batch else 0
                    n_itemCategory = obj_batch.itemCategory if obj_batch else 0
                dict_data = {
                    "action": EDevAction.IN if f_isReturn else EDevAction.OUT,
                    "refNo": obj_result.no,
                    "refNoSec": "",
                    "refDateTimestamp": obj_result.date,
                    "itemNo": obj_result.item_no,
                    "itemName": obj_result.item_name,
                    "itemVendor": obj_result.item_ref_displayName,
                    "itemType": n_itemCategory,
                    "itemCategory": n_itemType,
                    "itemAmount": obj_result.expectedCount,
                    "itemAmountUnit": obj_result.unit,
                    "itemComment": obj_result.comment,
                    "itemPageType": n_pageType,
                    "itemMaxWeight": 0,
                    "itemMinWeight": 0,
                    "itemBatchNo": lst_batchno
                }
                lst_data.append(dict_data)
        return lst_data


    def __gen_data_other(self, n_date, n_shift):
        lst_data = []
        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            n_start, n_end = self.__retrieve_time(n_date, n_shift)
            n_pageType = EPageType.SCAN
            # 銷貨/銷貨退回
            lst_obj_result = (
                obj_session.query(CTableInventoryOrder)
                .filter(CTableInventoryOrder.date.between(n_start, n_end))
                .all()
            )
            for obj_result in lst_obj_result:
                # 出庫 入庫?
                if obj_result.category == EInventoryCategory.OUT:
                    lst_batchno, n_itemType, n_itemCategory = self.__retrieve_serialno(obj_session, obj_result.no)
                    dict_data = {
                        "action": EDevAction.IN if obj_result.category == EInventoryCategory.IN else EDevAction.OUT,
                        "refNo": obj_result.no,
                        "refNoSec": "",
                        "refDateTimestamp": obj_result.date,
                        "itemNo": obj_result.item_no,
                        "itemName": obj_result.item_name,
                        "itemVendor": obj_result.item_ref_displayName,
                        "itemType": n_itemCategory,
                        "itemCategory": n_itemType,
                        "itemAmount": obj_result.expectedCount,
                        "itemAmountUnit": obj_result.unit,
                        "itemComment": self.__gen_other_comment(obj_result.category, obj_result.subCategory, obj_result.comment),
                        "itemPageType": n_pageType,
                        "itemMaxWeight": 0,
                        "itemMinWeight": 0,
                        "itemBatchNo": lst_batchno
                    }
                    lst_data.append(dict_data)
        return lst_data

    def __retrieve_time(self, n_date, n_shift):

        if n_shift == 0:
            n_start = util_convert_timestamp_to_date(n_date)
            n_end = util_convert_timestamp_to_date(n_start, 1) - 1
        else:
            n_start = util_convert_timestamp_to_date(n_date)
            n_end = util_convert_timestamp_to_date(n_start, 1) - 1
        CLogger().log(CLogger.LOG_LEVELINFO, '[%s] (start_time: %d, end_time: %d)'
                      % (self.__class__.__name__, n_start, n_end))
        return n_start, n_end

    def  __retrieve_serialno(self, obj_session, str_ref_no):
        lst_batchno = []
        n_itemType = 0
        n_itemCategory = 0
        str_batchno = ""
        lst_obj_batchno = (
            obj_session.query(CTableBatchNoSerialNo)
            .filter(CTableBatchNoSerialNo.ref_order_no == str_ref_no)
            .order_by(CTableBatchNoSerialNo.batch_number)
            .all()
        )

        dict_batchno = {
            batch_number: list(group)
            for batch_number, group in groupby(lst_obj_batchno, key=attrgetter('batch_number'))
        }
        for str_key, lst_temp in dict_batchno.items():
            lst_serial = []
            n_validDate = 0
            for obj_temp in lst_temp:
                n_validDate = obj_temp.validDate
                if obj_temp.serialNo:
                    lst_serial.append({"serialNo": obj_temp.serialNo, "value": obj_temp.expectedCount})
            lst_batchno.append({"batchNo": str_key,
                                "validDateTimestamp": n_validDate,
                                "serialNos": lst_serial})
            str_batchno = str_key
        if str_batchno:
            obj_result = (
                obj_session.query(CTableBatchNumber)
                .filter(CTableBatchNumber.no==str_batchno)
                .first()
            )
            n_itemType = obj_result.itemType
            n_itemCategory = obj_result.itemCategory
        return lst_batchno, n_itemType, n_itemCategory

    def __gen_other_comment(self, n_category, n_subCategory, str_comment):
        str_data = str_comment
        if n_category == EInventoryCategory.OUT:
            if n_subCategory == EInventorySubCategory.SCRAPPED:
                str_data = "廢品料報廢"
            if n_subCategory == EInventorySubCategory.GIVEAWAY:
                str_data = "公關贈品"
            if n_subCategory == EInventorySubCategory.RD:
                str_data = "研發打樣"

        return str_data
    def __merge_items(self, data):
        import re
        from collections import defaultdict
        import copy

        merged = {}
        grouped = defaultdict(list)

        for item in data:
            match = re.match(r"(.+?)_(\d+)$", item["refNoSec"])
            if match:
                base_key, suffix = match.groups()
                grouped[base_key].append((int(suffix), item))
            else:
                if item["itemPageType"] == EPageType.WEIGHT:
                    # 誤差正負3%
                    item["itemMaxWeight"] = round(item["itemAmount"] * (1 + 0.03), 2)
                    item["itemMinWeight"] = round(item["itemAmount"] * (1 - 0.03), 2)
                merged[item["refNoSec"]] = item  # 無須合併的直接加入

        for base_key, items in grouped.items():
            # 依照 suffix 排序
            items.sort()
            base_item = copy.deepcopy(items[0][1])  # 取第一筆作為 base
            suffixes = [str(suffix) for suffix, _ in items]

            # 合併 refNoSec
            base_item["refNoSec"] = base_key + "@" + "@".join(suffixes)

            # 合併 itemBatchNo
            merged_batches = []
            f_total = 0
            for _, it in items:
                merged_batches.extend(it.get("itemBatchNo", []))
                f_total += it.get("itemAmount", 0)
            base_item["itemBatchNo"] = merged_batches
            base_item["itemAmount"] = f_total
            if base_item["itemPageType"] == EPageType.WEIGHT:
                # 誤差正負3%
                base_item["itemMaxWeight"] = round(base_item["itemAmount"] * (1 + 0.03), 2)
                base_item["itemMinWeight"] = round(base_item["itemAmount"] * (1 - 0.03), 2)
            merged[base_key] = base_item

        return list(merged.values())