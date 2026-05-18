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

from sqlalchemy.orm import selectinload
class CAPSBase(object):
    def __init__(self, str_order_no):
        self.__m_str_order_no = str_order_no
        self.__m_dict_data = self.__get_aps_quantity_data()

    def __get_aps_quantity_data(self):
        dict_data = {"creationTime": 0, "material":[], "labor":[]}
        n_create_time = 0
        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            lst_obj_result = (obj_session.query(
                    CTableAPSQuantity
                )
                .options(selectinload(CTableAPSQuantity.item_data))
                .filter(CTableAPSQuantity.product_order_no == self.__m_str_order_no)
                .all())
            dict_process = {}
            for obj_result in lst_obj_result:
                n_create_time = obj_result.creationTime
                if obj_result.oneProcess not in dict_process:
                    dict_process[obj_result.oneProcess] = {"material":[], "labor":[]}
                dict_tmp_m = {"item_no": obj_result.item_no,
                              "item_name": obj_result.item_name,
                              "unit": obj_result.unit,
                              "count": obj_result.count,
                              "items": []}
                for obj_item in obj_result.item_data:
                    dict_tmp_m["items"].append({
                                    "item_no": obj_item.item_no,
                                    "item_name": obj_item.item_name,
                                    "itemCategory": obj_item.itemCategory,
                                    "unit": obj_item.unit,
                                    "count": obj_item.count
                                    })

                dict_tmp_l = {"APSQuantity_id": obj_result.no,
                              "item_no": obj_result.item_no,
                              "item_name": obj_result.item_name,
                              "minutes": obj_result.minutes,
                              "laborCount": obj_result.laborCount
                             }
                dict_process[obj_result.oneProcess]["material"].append(deepcopy(dict_tmp_m))
                dict_process[obj_result.oneProcess]["labor"].append(deepcopy(dict_tmp_l))
        dict_data["creationTime"] = n_create_time
        for n_process, dict_tmp in dict_process.items():
            dict_data["material"].append({"oneProcess": n_process, "inproduct":dict_tmp["material"]})
            dict_data["labor"].append({"oneProcess": n_process, "inproduct": dict_tmp["labor"]})
        return dict_data

    def get_aps_quantity_item(self):
        return self.__m_dict_data["material"] if self.__m_dict_data else {}

    def get_aps_time_labor(self):
        return self.__m_dict_data["labor"] if self.__m_dict_data else {}

    def get_creationTime(self):
        return self.__m_dict_data["creationTime"] if self.__m_dict_data else {}

class CAPSMaterial():
    def __init__(self, str_order_no):
        self.__m_obj_base = CAPSBase(str_order_no)

    def get(self):
        lst_data = self.__m_obj_base.get_aps_quantity_item()
        return lst_data

    def getTime(self):
        return self.__m_obj_base.get_creationTime()

class CAPSLabor():
    def __init__(self, str_order_no):
        self.__m_obj_base = CAPSBase(str_order_no)

    def get(self):
        lst_data = self.__m_obj_base.get_aps_time_labor()
        return lst_data

    def getTime(self):
        return self.__m_obj_base.get_creationTime()