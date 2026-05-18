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
from package.restserver.api.util import *

from datetime import datetime
from collections import defaultdict
import random
import time


class CCInventroyRec(object):
    lst_observers = []
    def add(self, str_group, dict_data):
        try:
            str_id = ""
            with CDBMgr() as obj_dbmgr:
                str_uuid = str(uuid.uuid4()).replace("-", "")
                new_data = CTableInventoryRec(
                    id=str_uuid,
                    creator_id=dict_data.get("creator_id",""),
                    group=str_group,
                    ref_no = dict_data.get("ref_no",""),
                    refCategory= dict_data.get("ref_category",0),
                    warehouse_no=dict_data.get("warehouse_no",""),
                    warehouse_displayName=dict_data.get("warehouse_displayName",""),
                    date=dict_data.get("date",0),
                    category=dict_data.get("category",0), # 出入庫
                    source=dict_data.get("source",0), # 緣由
                    batchNumber=dict_data.get("batchNumber",""),
                    serialNo=dict_data.get("serialNo", ""),
                    item_no=dict_data.get("item_no",""),
                    item_name=dict_data.get("item_name",""),
                    item_ref_no=dict_data.get("item_ref_no",""),
                    item_ref_displayName=dict_data.get("item_ref_displayName",""),
                    itemCategory=dict_data.get("itemCategory",0),
                    itemType=dict_data.get("itemType",0),
                    unit=dict_data.get("unit", 0),
                    count=dict_data.get("count", 0),
                    price=dict_data.get("price", 0),
                    amount=dict_data.get("amount", 0),
                    comment=dict_data.get("comment",""),
                    registerDevId=dict_data.get("registerDevId", ""),
                    creationTime=util_retrieve_now_time()
                )
                if obj_dbmgr.insert(new_data) == EErrorCode.ERROR_SUCCESS:
                    str_id = str_uuid
                    self.__notify_observers(dict_data)
                else:
                    str_message = 'failed to create inventory record'
                    CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s (%s)' % (
                        self.__class__.__name__, str_message, dict_data["warehouse_displayName"]))
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return str_id

    def update(self, dict_where, dict_data):
        n_code = EErrorCode.ERROR_SUCCESS
        '''
        with CDBMgr() as obj_dbmgr:
            lst_where = self.__fill_update_params(dict_where)
            if lst_where:
                if obj_dbmgr.update(CTableInventoryRec,
                                    lst_where,
                                    dict_data) != EErrorCode.ERROR_SUCCESS:
                    str_message = 'failed to update inventory record'
                    n_code = EErrorCode.ERROR_DB
        '''
        return n_code

    def delete(self, lst_where):

        n_code = EErrorCode.ERROR_SUCCESS
        '''
        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            obj_delete = delete(CTableInventoryRec).where(and_(*lst_where))
            obj_result = obj_session.execute(obj_delete)
            deleted_rows = obj_result.rowcount
            print(f"Deleted {deleted_rows} rows.")
            obj_session.commit()
        '''
        return n_code

    @classmethod
    def register_observer(cls, func):
        """註冊外部 observer 函式"""
        if callable(func) and func not in cls.lst_observers:
            cls.lst_observers.append(func)

    @classmethod
    def unregister_observer(cls, func):
        """取消註冊 observer"""
        if func in cls.lst_observers:
            cls.lst_observers.remove(func)

    def __notify_observers(self, dict_param):
        """呼叫所有註冊的 observer 函式"""
        for observer in self.lst_observers:
            observer.update(dict_param)  # 傳入自己作為參數.

    def __fill_update_params(self, dict_where):
        lst_where = []
        if dict_where.get('ref_no', ''):
            lst_where.append(CTableInventoryRec.ref_no == dict_where.get('ref_no', ''))
        if dict_where.get('category', ''):
            lst_where.append(CTableInventoryRec.category == dict_where.get('category', 0))
        if dict_where.get('batchNumber', ''):
            lst_where.append(CTableInventoryRec.batchNumber == dict_where.get('batchNumber', ''))
        if dict_where.get('serialNo', ''):
            lst_where.append(CTableInventoryRec.serialNo == dict_where.get('serialNo', ''))
        if dict_where.get('registerDevId', ''):
            lst_where.append(CTableInventoryRec.registerDevId == dict_where.get('registerDevId', ''))
        return lst_where