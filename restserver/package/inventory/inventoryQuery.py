# coding=utf8
import pytz
import string
from package.util.util import *
from package.common.common import *
from package.log.log import CLogger
from package.dbwrapper.table import *
from package.dbwrapper.dbmgr import CDBMgr
import uuid
from package.restserver.api.util import *

from datetime import datetime
from collections import defaultdict
import random
import time
from sqlalchemy import delete, func, select, case, or_
from package.inventory.stock import *

class CCInventroyRecByBatchNo(object):
    TYPE_PRODUCT_ORDER = 1
    TYPE_PURCHASE_ORDER = 2

    def get(self, n_type, lst_batchNo):
        try:
            lst_records = []
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                dict_batchNo = self.__get_batchNo_validDate(obj_session, lst_batchNo)
                # 產製批號
                if lst_batchNo:
                    n_category = EInventoryCategory.OUT if n_type == self.TYPE_PRODUCT_ORDER else EInventoryCategory.IN
                    n_source = EInventorySrc.RETURN_SALE if n_type == self.TYPE_PRODUCT_ORDER else EInventorySrc.PURCHASE_RECEIVE
                    lst_rec = (
                        obj_session.query(CTableInventoryRec)
                        .filter(CTableInventoryRec.batchNumber.in_(lst_batchNo),
                                CTableInventoryRec.category == n_category,
                                CTableInventoryRec.source == n_source)
                        .order_by(CTableInventoryRec.date.asc())
                        .all()
                    )
                    for obj_rec in lst_rec:
                        dict_rec = object_as_dict(obj_rec)
                        dict_rec["validDate"] = 0
                        if dict_rec["batchNumber"] in dict_batchNo:
                            dict_rec["validDate"] = dict_batchNo[dict_rec["batchNumber"]]
                        lst_records.append(dict_rec)

        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_records

    def __get_batchNo_validDate(self, obj_session, lst_batchNo):
        # 批號. {批號:效期}
        dict_batchNo = {}

        if lst_batchNo:
            batchNos_query = (
                obj_session.query(CTableBatchNumber.no, CTableBatchNumber.validDate)
                .filter(CTableBatchNumber.no.in_(lst_batchNo))
                .order_by(CTableBatchNumber.date.asc())
            )
            dict_batchNo = {no: validDate for no, validDate in batchNos_query.all()}
        return  dict_batchNo


# 採購/訂購單->批號->取回庫存
class CCInventroyRecByOrder(object):
    TYPE_PRODUCT_ORDER = 1
    TYPE_PURCHASE_ORDER = 2
    TYPE_GOODSRECEIPTNOTE = 3
    TYPE_SHIPPING_ORDER = 4

    def get_batch(self, n_type, lst_order_nos, f_stock=True, f_demo=True):
       
        if not lst_order_nos:
            return {}
        lst_where = []
        dict_results = {no: [] for no in lst_order_nos}
        dict_stocks = {no: [] for no in lst_order_nos}
        # 查詢日期區間的資料
        #
        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()

                # --- 1. 取得單據與生產/採購單號對照，並計算日期區間 ---
                dict_mapping = {}
                if n_type == self.TYPE_SHIPPING_ORDER:
                    lst_ships = (obj_session.query(CTableShippingOrder.no, 
                                                   CTableShippingOrder.product_order_no,
                                                   CTableShippingOrder.date)
                             .filter(CTableShippingOrder.no.in_(lst_order_nos))
                             .all())
                    for obj_row in lst_ships:
                        # 若無全域日期參數，採用該單據日期作為當天過濾
                        n_start = obj_row.date
                        n_end = util_convert_timestamp_to_date(n_start, 1) - 1
                        obj_date_range = (n_start, n_end)
                        dict_mapping[obj_row.no] = {"order_no": obj_row.product_order_no, "date_range": obj_date_range}
                elif n_type == self.TYPE_GOODSRECEIPTNOTE:
                    lst_ships = (obj_session.query(
                                    CTableGoodsReceiptNote.no,
                                    CTableGoodsReceiptNote.date)
                                 .filter(CTableGoodsReceiptNote.no.in_(lst_order_nos))
                                 .all())
                    # 若為demo版本進貨單不設定日期
                    if f_demo:
                        dict_mapping = {no: {"order_no": no, "date_range": None} for no in lst_order_nos}
                    else:
                        for obj_row in lst_ships:
                            n_start = obj_row.date
                            n_end = util_convert_timestamp_to_date(n_start, 1) - 1
                            obj_date_range = (n_start, n_end)
                            dict_mapping[obj_row.no] = {"order_no": obj_row.no, "date_range": obj_date_range}
                else:
                    # 採購單或其他類型暫不處理動態日期補丁，或可比照辦理
                    dict_mapping = {no: {"order_no": no, "date_range": None} for no in lst_order_nos}

                # 取得採購/訂購訂單的批號
                lst_sale_purchase_orderNos = list(set([v["order_no"] for v in dict_mapping.values() if v["order_no"]]))
                dict_batch_map = self.__get_batchNos(obj_session, n_type, lst_sale_purchase_orderNos)

                # 產製批號               
                lst_conds = []
                lst_all_batchNo = []
                n_base_cat = EInventoryCategory.OUT if n_type in [self.TYPE_PRODUCT_ORDER,
                                                                  self.TYPE_SHIPPING_ORDER] else EInventoryCategory.IN

                # 進貨/銷貨
                n_category = EInventoryCategory.OUT if n_type in [self.TYPE_PRODUCT_ORDER,
                                                                  self.TYPE_SHIPPING_ORDER] else EInventoryCategory.IN
                n_source = EInventorySrc.RETURN_SALE if n_type in [self.TYPE_PRODUCT_ORDER,
                                                                   self.TYPE_SHIPPING_ORDER] else EInventorySrc.PURCHASE_RECEIVE

                # 進貨/銷貨退回
                n_category2 = EInventoryCategory.IN if n_type in [self.TYPE_PRODUCT_ORDER,
                                                                  self.TYPE_SHIPPING_ORDER] else EInventoryCategory.OUT
                n_source2 = EInventorySrc.SRETURN if n_type in [self.TYPE_PRODUCT_ORDER,
                                                                self.TYPE_SHIPPING_ORDER] else EInventorySrc.RETURN_SALE

                behavior_cond = or_(
                    and_(CTableInventoryRec.category == n_category, CTableInventoryRec.source == n_source),
                    and_(CTableInventoryRec.category == n_category2, CTableInventoryRec.source == n_source2)
                )
                for str_input_no, dict_info in dict_mapping.items():
                    str_order_no = dict_info["order_no"]
                    if str_order_no not in dict_batch_map:
                        continue

                    lst_batchNo = dict_batch_map[str_order_no]["lst"]
                    # 收集所有批號一次查詢
                    #lst_all_batchNo.extend(lst_batchNo)
                    # 查詢該訂購單/採購單的批號+日期區間+category+source
                    obj_cond = CTableInventoryRec.batchNumber.in_(lst_batchNo)
                    if dict_info["date_range"]:
                        obj_cond = and_(obj_cond, CTableInventoryRec.date.between(*dict_info["date_range"]))

                    if lst_where:
                        obj_cond = and_(obj_cond, *lst_where)
                    lst_conds.append(and_(obj_cond, behavior_cond))
                if not lst_conds:
                    return dict_results

                lst_recs = (obj_session.query(CTableInventoryRec)
                            .filter(or_(*lst_conds))
                            .order_by(CTableInventoryRec.date.asc()).all())


                for str_input_no, dict_info in dict_mapping.items():
                    str_order_no = dict_info["order_no"]
                    if str_order_no not in dict_batch_map:
                        continue


                    dict_batchNo = dict_batch_map[str_order_no]["dict"]  # {批號: 效期}
                    obj_date_range = dict_info["date_range"]

                    for obj_row in lst_recs:
                        dict_rec = object_as_dict(obj_row)
                        dict_rec.pop("id", None)
                        dict_rec.pop("creationTime", None)
                        # 比對 批號與日期
                        if obj_row.batchNumber in dict_batchNo:
                            # 檢查日期區間
                            if obj_date_range and not (obj_date_range[0] <= obj_row.date <= obj_date_range[1]):
                                continue
                            dict_rec.update({
                                "validDate": dict_batchNo.get(obj_row.batchNumber, 0),
                                "return": obj_row.category != n_base_cat  # 類別與主類別不同即為退貨
                            })
                            dict_results[str_input_no].append(dict_rec)
                    lst_batchNo = dict_batch_map[str_order_no]["lst"]
                    if f_stock:
                        lst_stock = CCStockByBatchNo().get(lst_batchNo)
                        dict_stocks[str_input_no] = lst_stock
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, f'[CCInventroyRecByOrder] Batch error: {error}')

        return dict_results, dict_stocks

    def __get_batchNos(self, session, n_type, lst_nos):
        """
        批號. {批號:效期}
        """
        dict_result = {no: {"lst": [], "dict": {}} for no in lst_nos}
        dict_mapping = {}
        # 銷貨單/產品品：透過 WorkOrder 找 Batch
        if n_type in [self.TYPE_PRODUCT_ORDER, self.TYPE_SHIPPING_ORDER]:
            lst_works = (session.query(
                                 CTableWorkOrder.no, 
                                 CTableWorkOrder.product_order_no)
                   .filter(CTableWorkOrder.product_order_no.in_(lst_nos),
                           CTableWorkOrder.oneProcess == EProcCategory.PACKAGE)
                   .all())
            # 取得 process_order_no, 未完成 因CTableBatchNumber.ref_no目前參照派工單
            #{派工單:訂購單}
            dict_mapping = {obj_row.no: obj_row.product_order_no for obj_row in lst_works}

        # B. 採購單/進貨單
        elif n_type in [self.TYPE_PURCHASE_ORDER, self.TYPE_GOODSRECEIPTNOTE]:
            
            if n_type == self.TYPE_PURCHASE_ORDER:
                lst_result = (session.query(
                                      CTableGoodsReceiptNote.no, 
                                      CTableGoodsReceiptNote.purchase_order_no)
                        .filter(CTableGoodsReceiptNote.purchase_order_no.in_(lst_nos))
                        .all())
                dict_mapping = {obj_row.no: obj_row.purchase_order_no for obj_row in lst_result}
            else:
                dict_mapping = {no: no for no in lst_nos}
        if dict_mapping:
            batches = (session.query(
                CTableBatchNumber.no,
                CTableBatchNumber.validDate,
                CTableBatchNumber.ref_no)
                       .filter(CTableBatchNumber.ref_no.in_(list(dict_mapping.keys())))
                       .order_by(CTableBatchNumber.date.asc())
                       .all())
            for no, validDate, ref_no in batches:
                str_sale_order_no = dict_mapping.get(ref_no)
                dict_result[str_sale_order_no]["lst"].append(no)
                dict_result[str_sale_order_no]["dict"][no] = validDate
        return dict_result
    
    def __fill_date_params(self):
        lst_where = []

        if self.__dict_date_params.get('start_time', 0) and self.__dict_date_params.get('end_time', 0):
            # get the range of timestamp
            n_start = util_convert_timestamp_to_date(int(self.__dict_date_params.get('start_time', 0)))
            if int(self.__dict_date_params.get('start_time', 0)) == int(self.__dict_date_params.get('end_time', 0)):
                n_end = util_convert_timestamp_to_date(n_start, 1) - 1
            else:
                n_end = util_convert_timestamp_to_date(int(self.__dict_date_params.get('end_time', 0)), 1) - 1
            lst_where.append(CTableInventoryRec.date.between(n_start, n_end))
        return lst_where




class CCInventroyRecByOrder2(object):
    TYPE_PRODUCT_ORDER = 1
    TYPE_PURCHASE_ORDER = 2
    TYPE_GOODSRECEIPTNOTE = 3
    TYPE_SHIPPING_ORDER = 4

    def __init__(self):
        CLogger().log(CLogger.LOG_LEVELERROR, '[%s]'
                      % (self.__class__.__name__))
        self.__dict_date_params = {}

    def setDateParams(self, dict_where):
        self.__dict_date_params = dict_where

    def get(self, n_type, str_order_no, f_stock=True, f_demo=True):
        try:
            lst_stock = []
            lst_records = []
            lst_where = []
            lst_where_r = []
            # 查詢日期區間的資料
            #
            # 以下程式碼為demo使用
            # 正常的程式碼為下列
            if f_demo:
                if n_type != self.TYPE_GOODSRECEIPTNOTE:
                    lst_where =  self.__fill_date_params()
            else:
                lst_where = self.__fill_date_params()

            #
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                str_new_order_no = str_order_no
                if n_type == self.TYPE_SHIPPING_ORDER:
                    obj_result = (
                        obj_session.query(CTableShippingOrder.date,
                                          CTableShippingOrder.product_order_no)
                        .filter(CTableShippingOrder.no == str_order_no)
                        .first()
                    )
                    if obj_result:
                        str_new_order_no = obj_result.product_order_no
                        if not self.__dict_date_params:
                            # imported excel without ref_no data, adopt time for filter
                            n_start = obj_result.date
                            n_end = util_convert_timestamp_to_date(n_start, 1) - 1
                            if n_start and n_end:
                                lst_where.append(CTableInventoryRec.date.between(n_start, n_end))

                # 取得採購/訂購訂單的批號
                lst_batchNo, dict_batchNo = self.__get_batchNos(obj_session, n_type, str_new_order_no)

                # 產製批號
                if lst_batchNo:
                    lst_where.append(CTableInventoryRec.batchNumber.in_(lst_batchNo))
                    lst_where_r = list(lst_where)

                    # 進貨/銷貨
                    n_category = EInventoryCategory.OUT if n_type in [self.TYPE_PRODUCT_ORDER,self.TYPE_SHIPPING_ORDER]  else EInventoryCategory.IN
                    n_source = EInventorySrc.RETURN_SALE if n_type in [self.TYPE_PRODUCT_ORDER,self.TYPE_SHIPPING_ORDER] else EInventorySrc.PURCHASE_RECEIVE
                    lst_where.append(CTableInventoryRec.category == n_category)
                    lst_where.append(CTableInventoryRec.source == n_source)

                    # 進貨/銷貨退回
                    n_category2 = EInventoryCategory.IN if n_type in [self.TYPE_PRODUCT_ORDER,
                                                                      self.TYPE_SHIPPING_ORDER] else EInventoryCategory.OUT
                    n_source2 = EInventorySrc.SRETURN if n_type in [self.TYPE_PRODUCT_ORDER,
                                                                       self.TYPE_SHIPPING_ORDER] else EInventorySrc.RETURN_SALE
                    lst_where_r.append(CTableInventoryRec.category == n_category2)
                    lst_where_r.append(CTableInventoryRec.source == n_source2)

                    # 取得實際出入貨的紀錄
                    lst_tmp = self.__query_and_fill(obj_session, lst_where, dict_batchNo, False)
                    if lst_tmp:
                        lst_records.extend(lst_tmp)
                    lst_tmp2 = self.__query_and_fill(obj_session, lst_where_r, dict_batchNo, True)
                    if lst_tmp2:
                        lst_records.extend(lst_tmp2)
                    
                    if f_stock:
                        lst_stock = CCStockByBatchNo().get(lst_batchNo)

        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_stock, lst_records

    def __query_and_fill(self, obj_session, lst_where, dict_batchNo, f_isReturn):
        lst_records = []
        lst_rec = (
            obj_session.query(CTableInventoryRec)
            .filter(*lst_where)
            .order_by(CTableInventoryRec.date.asc())
            .all()
        )
        for obj_rec in lst_rec:
            dict_rec = object_as_dict(obj_rec)
            dict_rec.pop("id", None)
            dict_rec.pop("creationTime", None)
            dict_rec["validDate"] = 0
            if dict_rec["batchNumber"] in dict_batchNo:
                dict_rec["validDate"] = dict_batchNo[dict_rec["batchNumber"]]
            dict_rec["return"] = f_isReturn
            lst_records.append(dict_rec)
        return lst_records

    def __get_batchNos(self, obj_session, n_type, str_order_no):
        # 批號. {批號:效期}
        lst_batchNo = []
        dict_batchNo = {}

        if n_type in [self.TYPE_PRODUCT_ORDER, self.TYPE_SHIPPING_ORDER]:
            if str_order_no:
                nos_query = (
                    obj_session.query(CTableWorkOrder.no)
                    .filter(CTableWorkOrder.product_order_no == str_order_no,
                            CTableWorkOrder.oneProcess == EProcCategory.PACKAGE)
                    .order_by(CTableWorkOrder.date.desc())
                )
                nos = [no[0] for no in nos_query.all()]

                # 取得 process_order_no
                if nos:
                    batchNos_query = (
                        obj_session.query(CTableBatchNumber.no, CTableBatchNumber.validDate)
                        .filter(CTableBatchNumber.ref_no.in_(nos))
                        .order_by(CTableBatchNumber.date.asc())
                    )
                    lst_batchNo = [no for no, validDate in batchNos_query.all()]
                    dict_batchNo = {no: validDate for no, validDate in batchNos_query.all()}

        if n_type in [self.TYPE_PURCHASE_ORDER, self.TYPE_GOODSRECEIPTNOTE]:
            if n_type == self.TYPE_PURCHASE_ORDER:
                nos_query = (
                    obj_session.query(
                        CTableGoodsReceiptNote.no
                    )
                    .filter(CTableGoodsReceiptNote.purchase_order_no == str_order_no)

                    .order_by(CTableGoodsReceiptNote.date.asc())
                )
                nos = [no[0] for no in nos_query.all()]
            else:
                nos = [str_order_no]
            if nos:
                batchNos_query = (
                    obj_session.query(CTableBatchNumber.no, CTableBatchNumber.validDate)
                    .filter(CTableBatchNumber.ref_no.in_(nos))
                    .order_by(CTableBatchNumber.date.asc())
                )
                lst_batchNo = [no for no, validDate in batchNos_query.all()]
                dict_batchNo = {no: validDate for no, validDate in batchNos_query.all()}
        return lst_batchNo, dict_batchNo

    def __fill_date_params(self):
        lst_where = []

        if self.__dict_date_params.get('start_time', 0) and self.__dict_date_params.get('end_time', 0):
            # get the range of timestamp
            n_start = util_convert_timestamp_to_date(int(self.__dict_date_params.get('start_time', 0)))
            if int(self.__dict_date_params.get('start_time', 0)) == int(self.__dict_date_params.get('end_time', 0)):
                n_end = util_convert_timestamp_to_date(n_start, 1) - 1
            else:
                n_end = util_convert_timestamp_to_date(int(self.__dict_date_params.get('end_time', 0)), 1) - 1
            lst_where.append(CTableInventoryRec.date.between(n_start, n_end))            
        return lst_where
