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
from package.restserver.api.util import *

from datetime import datetime
from collections import defaultdict
import random
import time

from .common import *
from sqlalchemy import delete, func, select, case
from abc import ABC, abstractmethod
from package.batchno.batchno import *

class IObserver(ABC):
    @abstractmethod
    def update(self, data):
        pass


# 更新batch_number checkedOut
class CBatchNumberObserver(IObserver):

    @staticmethod
    def update(dict_param):
        n_code = EErrorCode.ERROR_SUCCESS

        try:
            str_batchno = dict_param["batchno"]
            if str_batchno and dict_param["bsType"] in [EBSType.PURCHASE_IN_S, EBSType.PRODUCT_IN_S, EBSType.OTHER_IN_S, EBSType.SALE_IN_S]:
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    #f_total = dict_param.get("total", 0)

                    f_total = 0
                    str_ref_no = dict_param["ref_no_sub"] if dict_param["ref_no_category"] == EDevRefCategory.WORK else dict_param["ref_no"]

                    lst_obj = obj_session.query(
                        func.round(func.sum(CTableInventoryRec.count), 2)
                    ).filter(CTableInventoryRec.ref_no == str_ref_no,
                             CTableInventoryRec.category == EInventoryCategory.IN).all()

                    if lst_obj:
                        f_total = float(lst_obj[0][0]) if lst_obj[0][0]  is not None else 0

                    if f_total:
                        # batch number
                        dict_update = {"checkedCount": f_total}
                        n_code = CCBatchNumber().update(str_batchno, dict_update, SYSTEM_ID)
                        if n_code != EErrorCode.ERROR_SUCCESS:
                            str_message = 'failed to update batch number [checkedCount] value '
                            CLogger().log(CLogger.LOG_LEVELERROR,
                                          '[CBatchNumberObserver] %s' % (str_message))


        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[CBatchNumberObserver] throw exception (error: %s)'
                          % (str(error)))
        return n_code

class CGRNoteObserver(IObserver):

    @staticmethod
    def update(dict_param):
        n_code = EErrorCode.ERROR_SUCCESS

        try:
            str_ref_no = dict_param["ref_no"]
            if str_ref_no and dict_param["bsType"] in [EBSType.PURCHASE_IN_S, EBSType.PURCHASE_OUT_S]:
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    #f_total = dict_param.get("total", 0)
                    f_total = 0
                    n_condition = EInventoryCategory.IN if dict_param["bsType"] == EBSType.PURCHASE_IN_S else EInventoryCategory.OUT
                    lst_obj = obj_session.query(
                        func.round(func.sum(CTableInventoryRec.count), 0)
                    ).filter(CTableInventoryRec.ref_no == str_ref_no,
                             CTableInventoryRec.category == n_condition).all()
                    if lst_obj:
                        f_total = float(lst_obj[0][0]) if lst_obj[0][0] is not None else 0

                    if f_total:
                        obj_order = obj_session.query(
                            CTableGoodsReceiptNote
                        ).filter(CTableGoodsReceiptNote.no == str_ref_no).first()
                        dict_update = object_as_dict(obj_order)
                        dict_update["checkedCount"] = f_total
                        dict_update["amount"] = round(f_total * dict_update["price"],2)
                        if obj_dbmgr.update(CTableGoodsReceiptNote, [CTableGoodsReceiptNote.no == str_ref_no],
                                            dict_update) != EErrorCode.ERROR_SUCCESS:
                            n_code = EErrorCode.ERROR_OTHER_ERROR
                            str_message = 'failed to update goods_receipt_note [count] value'
                            CLogger().log(CLogger.LOG_LEVELERROR, '[CGRNoteObserver] %s' % (str_message))

        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[CGRNoteObserver] throw exception (error: %s)'
                          % (str(error)))
        return n_code


class CShippingOrderObserver(IObserver):

    @staticmethod
    def update(dict_param):
        n_code = EErrorCode.ERROR_SUCCESS

        try:
            str_ref_no = dict_param["ref_no"]
            if str_ref_no and dict_param["bsType"] in [EBSType.SALE_OUT_S, EBSType.SALE_IN_S]:
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    #f_total = dict_param.get("total", 0)
                    f_total = 0
                    n_condition = EInventoryCategory.IN if dict_param["bsType"] == EBSType.SALE_IN_S else EInventoryCategory.OUT
                    lst_obj = obj_session.query(
                        func.round(func.sum(CTableInventoryRec.count), 0)
                    ).filter(CTableInventoryRec.ref_no == str_ref_no,
                             CTableInventoryRec.category == n_condition).all()
                    if lst_obj:
                        f_total = float(lst_obj[0][0]) if lst_obj[0][0] is not None else 0

                    if f_total:
                        obj_order = obj_session.query(
                            CTableShippingOrder
                        ).filter(CTableShippingOrder.no == str_ref_no).first()
                        dict_update = object_as_dict(obj_order)
                        dict_update["checkedCount"] = f_total
                        dict_update["amount"] = round(f_total * dict_update["price"], 2)
                        if obj_dbmgr.update(CTableShippingOrder, [CTableShippingOrder.no == str_ref_no],
                                            dict_update) != EErrorCode.ERROR_SUCCESS:
                            n_code = EErrorCode.ERROR_OTHER_ERROR
                            str_message = 'failed to update shipping_order [count] value'
                            CLogger().log(CLogger.LOG_LEVELERROR, '[CShippingOrderObserver] %s' % (str_message))
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[CShippingOrderObserver] throw exception (error: %s)'
                          % (str(error)))
        return n_code

class CInventoryOrderObserver(IObserver):

    @staticmethod
    def update(dict_param):
        n_code = EErrorCode.ERROR_SUCCESS

        try:
            str_ref_no = dict_param["ref_no"]
            if str_ref_no and dict_param["bsType"] == EBSType.OTHER_OUT_S:
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    #f_total = dict_param.get("total", 0)
                    f_total = 0
                    n_condition = EInventoryCategory.OUT
                    lst_obj = obj_session.query(
                        func.round(func.sum(CTableInventoryRec.count), 0)
                    ).filter(CTableInventoryRec.ref_no == str_ref_no,
                             CTableInventoryRec.category == n_condition).all()
                    if lst_obj:
                        f_total = float(lst_obj[0][0]) if lst_obj[0][0] is not None else 0

                    if f_total:
                        obj_order = obj_session.query(
                            CTableInventoryOrder
                        ).filter(CTableInventoryOrder.no == str_ref_no).first()
                        dict_update = object_as_dict(obj_order)
                        dict_update["checkedCount"] = f_total
                        dict_update["amount"] = round(f_total * dict_update["price"], 2)
                        if obj_dbmgr.update(CTableInventoryOrder, [CTableInventoryOrder.no == str_ref_no],
                                            dict_update) != EErrorCode.ERROR_SUCCESS:
                            n_code = EErrorCode.ERROR_OTHER_ERROR
                            str_message = 'failed to update invnetory_order [count] value'
                            CLogger().log(CLogger.LOG_LEVELERROR, '[CInventoryOrderObserver] %s' % (str_message))
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[CInventoryOrderObserver] throw exception (error: %s)'
                          % (str(error)))
        return n_code

