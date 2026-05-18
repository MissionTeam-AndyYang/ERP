# coding=utf8
import pytz
import string
from copy import deepcopy
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
from sqlalchemy import delete, func, select, case


class CCStockByBatchNo(object):
    def get(self, lst_batchNo):
        try:
            lst_stock = []

            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                n_now = util_retrieve_now_time()
                # 預先取得批號有效期限
                dict_batchNo = self.__get_batchNo_validDate(obj_session, lst_batchNo)

                # 先找各批號各倉庫的最早入庫日
                obj_sub_query = (
                    obj_session.query(
                        CTableInventoryRec.batchNumber,
                        CTableInventoryRec.warehouse_no,
                        func.min(CTableInventoryRec.date).label("firstInDate")
                    )
                    .filter(CTableInventoryRec.batchNumber.in_(lst_batchNo),
                            CTableInventoryRec.category == EInventoryCategory.IN)
                    .group_by(CTableInventoryRec.batchNumber, CTableInventoryRec.warehouse_no)
                    .subquery()
                )
                # 計算剩餘數量與金額
                lst_rec = (
                    obj_session.query(
                        CTableInventoryRec,
                        # 入庫 - 出庫
                        func.sum(case((CTableInventoryRec.category == EInventoryCategory.IN, CTableInventoryRec.count),
                                      else_=-CTableInventoryRec.count)).label("remaining_count"),
                        func.sum(case((CTableInventoryRec.category == EInventoryCategory.IN, CTableInventoryRec.amount),
                                      else_=-CTableInventoryRec.amount)).label("remaining_amount"),
                        obj_sub_query.c.firstInDate
                    )
                    .outerjoin(obj_sub_query, (CTableInventoryRec.batchNumber == obj_sub_query.c.batchNumber) &
                               (CTableInventoryRec.warehouse_no == obj_sub_query.c.warehouse_no))
                    .filter(CTableInventoryRec.batchNumber.in_(lst_batchNo))
                    .group_by(CTableInventoryRec.batchNumber, CTableInventoryRec.warehouse_no)
                    .all()
                )

                lst_stock = []
                for obj_rec, remain_count, remain_amount, firstInDate in lst_rec:
                    if not remain_count: continue

                    str_batchNo = obj_rec.batchNumber
                    dict_batchInfo = dict_batchNo.get(str_batchNo, {"validDate": 0, "validDays": 0})
                    n_valid_date, n_valid_days = dict_batchInfo["validDate"], dict_batchInfo["validDays"]

                    # 判斷過期/即期
                    f_expired = (n_valid_date > 0 and (n_valid_date - n_now) < 0)
                    f_nearExpired = (n_valid_date > 0 and not f_expired and (n_valid_date - n_now) <= n_valid_days)

                    lst_stock.append({
                        "warehouse_no": obj_rec.warehouse_no,
                        "warehouse_displayName": obj_rec.warehouse_displayName,
                        "itemCategory": obj_rec.itemCategory,
                        "itemType": obj_rec.itemType,
                        "item_no": obj_rec.item_no,
                        "item_name": obj_rec.item_name,
                        "batchNumber": str_batchNo,
                        "validDate": n_valid_date,
                        "amount": round(remain_amount, 2),
                        "count": round(remain_count, 2),
                        "nearExpiryAmount": round(remain_amount, 2) if f_nearExpired else 0,
                        "nearExpiryCount": round(remain_count, 2) if f_nearExpired else 0,
                        "expiredAmount": round(remain_amount, 2) if f_expired else 0,
                        "expiredCount": round(remain_count, 2) if f_expired else 0,
                        "unit": obj_rec.unit,
                        "firstInDate": firstInDate or 0
                    })

                # 產製批號
                for str_batchNo in lst_batchNo:
                    n_validDate = 0
                    n_validDays = 0
                    if str_batchNo in dict_batchNo:
                        n_validDate = dict_batchNo[str_batchNo]["validDate"]
                        n_validDays = dict_batchNo[str_batchNo]["validDays"] * 28800
                    lst_rec = (
                        obj_session.query(
                            CTableInventoryRec,
                            func.sum(
                                case(
                                    (
                                        CTableInventoryRec.category == EInventoryCategory.IN,
                                        CTableInventoryRec.count),
                                    # 入庫
                                    (CTableInventoryRec.category == EInventoryCategory.OUT,
                                     -CTableInventoryRec.count)  # 出庫
                                )
                            ).label("remaining_count"),
                            func.sum(
                                case(
                                    (
                                        CTableInventoryRec.category == EInventoryCategory.IN,
                                        CTableInventoryRec.amount),
                                    # 入庫
                                    (CTableInventoryRec.category == EInventoryCategory.OUT,
                                     -CTableInventoryRec.amount)  # 出庫
                                )
                            ).label("remaining_amount")
                        )
                        .filter(CTableInventoryRec.batchNumber == str_batchNo)
                        .group_by(CTableInventoryRec.warehouse_no)
                        .all()
                    )
                    for obj_rec in lst_rec:
                        n_expiredCount = 0
                        n_expiredAmount = 0
                        n_nearExpiryCount = 0
                        n_nearExpiryAmount = 0
                        if n_validDate:
                            if (n_validDate - n_now) < 0:
                                n_expiredCount = round(obj_rec.remaining_count, 2)
                                n_expiredAmount = round(obj_rec.remaining_amount, 2),
                            else:
                                if (n_validDate - n_now) <= n_validDays:  # 86400/3 轉換成秒再取三分之一
                                    n_nearExpiryCount = round(obj_rec.remaining_count, 2)
                                    n_nearExpiryAmount = round(obj_rec.remaining_amount, 2)
                        if obj_rec.remaining_count:
                            n_firstInDate = self.__get_first_in_date(obj_session, str_batchNo, obj_rec[0].warehouse_no)
                            lst_stock.append({"warehouse_no": obj_rec[0].warehouse_no,
                                              "warehouse_displayName": obj_rec[0].warehouse_displayName,
                                              "itemCategory": obj_rec[0].itemCategory,
                                              "itemType": obj_rec[0].itemType,
                                              "item_no": obj_rec[0].item_no,
                                              "item_name": obj_rec[0].item_name,
                                              "batchNumber": str_batchNo,
                                              "validDate": n_validDate,
                                              "amount": round(obj_rec.remaining_amount, 2),
                                              "count": round(obj_rec.remaining_count, 2),
                                              "nearExpiryAmount": n_nearExpiryAmount,
                                              "nearExpiryCount": n_nearExpiryCount,
                                              "expiredAmount": n_expiredAmount,
                                              "expiredCount": n_expiredCount,
                                              "unit": obj_rec[0].unit,
                                              "firstInDate": n_firstInDate})

        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_stock

    def __get_batchNo_validDate(self, obj_session, lst_batchNo):
        # 批號. {批號:效期} * 28800
        dict_batchNo = {}
        if lst_batchNo:
            batchNos_query = (
                obj_session.query(
                    CTableBatchNumber.no,
                    CTableBatchNumber.validDate,
                    CTableBatchNumber.validDays)
                .filter(CTableBatchNumber.no.in_(lst_batchNo))
                .order_by(CTableBatchNumber.date.asc())
            )
            #validDays * 28800 = 86400/3 轉換成秒再取有效天數三分之一
            dict_batchNo = {no: {'validDate': validDate, 'validDays': (validDays * 86400 / 3)} for no, validDate, validDays in batchNos_query.all()}
        return dict_batchNo


