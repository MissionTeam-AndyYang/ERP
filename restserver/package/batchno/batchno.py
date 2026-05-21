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


class CCBatchNumber(object):

    def add(self, dict_param):
        try:
            str_id = ''
            with CDBMgr() as obj_dbmgr:
                str_uuid = str(uuid.uuid4()).replace("-", "")
                str_no = self.__gen_no(dict_param)
                new_data = CTableBatchNumber(
                    #id=str_uuid,
                    no=str_no,
                    date=dict_param["date"],
                    creator_no=dict_param["creator_id"] if dict_param["creator_id"]  else None ,
                    ref_no=dict_param["ref_no"],
                    refCategory=dict_param["refCategory"],
                    item_no=dict_param["item_no"],
                    item_name=dict_param["item_name"],
                    item_ref_no=dict_param["item_ref_no"],
                    item_ref_displayName=dict_param["item_ref_displayName"],
                    itemCategory=dict_param["itemCategory"],
                    itemType=dict_param["itemType"],
                    unit=dict_param["unit"],
                    expectedCount=dict_param["expectedCount"],
                    checkedCount=dict_param["checkedCount"],
                    validDate=dict_param["validDate"],
                    validDateNo=dict_param["validDateNo"],
                    validDays = 0,
                    comment=dict_param["comment"],
                    creationTime=util_retrieve_now_time()
                )
                if obj_dbmgr.insert(new_data) == EErrorCode.ERROR_SUCCESS:
                    str_id = str_no
                else:
                    str_message = 'failed to create batch number'
                    CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return str_id


    def update(self, str_no, dict_param, str_user_id):
        n_code = EErrorCode.ERROR_SUCCESS

        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            obj_batchnumber = (
                obj_session.query(CTableBatchNumber)
                .filter(CTableBatchNumber.no == str_no)
                .first()
            )
            dict_batchnumber = object_as_dict(obj_batchnumber)
            dict_old = deepcopy(dict_batchnumber)

            if "creator_id" in dict_param:
                dict_batchnumber["creator_id"] = dict_param["creator_id"]
            if "category" in dict_param:
                dict_batchnumber["category"] = dict_param["category"]
            if "itemType" in dict_param:
                dict_batchnumber["itemType"] = dict_param["itemType"]
            if "unit" in dict_param:
                dict_batchnumber["unit"] = dict_param["unit"]
            if "checkedCount" in dict_param:
                dict_batchnumber["checkedCount"] = dict_param["checkedCount"]
            if "validDate" in dict_param:
                dict_batchnumber["validDate"] = dict_param["validDate"]
            if "comment" in dict_param:
                dict_batchnumber["comment"] = dict_param["comment"]
            #print(str_no)
            if obj_dbmgr.update(CTableBatchNumber, [CTableBatchNumber.no == str_no],
                                dict_batchnumber) != EErrorCode.ERROR_SUCCESS:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'failed to update batchnumber'
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))

        return n_code

    def delete(self, str_no):
        n_code = EErrorCode.ERROR_SUCCESS
        if str_no:
            try:
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()

                    obj_delete = delete(CTableBatchNumber).where(CTableBatchNumber.no == str_no)
                    obj_result = obj_session.execute(obj_delete)
                    deleted_rows = obj_result.rowcount
                    print(f"Deleted batchNumber {deleted_rows} rows.")
                    obj_session.commit()
            except Exception as error:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                              % (self.__class__.__name__, str(error)))
        return n_code


    def __gen_no(self, dict_param):
        from datetime import datetime
        str_date = datetime.fromtimestamp(dict_param["date"]).strftime('%y%m%d')
        str_no = "BN%d%d%s" %(dict_param["itemCategory"],  dict_param["itemType"], str_date) + util_random_code(2)
        return str_no

