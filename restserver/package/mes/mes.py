# coding=utf8
import pytz
import string
from copy import deepcopy
from package.util.util import *
from package.common.common import *
from package.log.log import CLogger
from package.dbwrapper.table import *
from package.dbwrapper.dbmgr import CDBMgr
from sqlalchemy import delete
from sqlalchemy import func, cast, Numeric
import uuid
import math


class CMES():
    ELossType_EXPECTED = 1
    ELossType_ACTUAL = 2

    def __init__(self, lst_bom):
       self.__m_lst_bom = lst_bom

    def calculate(self, n_unit, n_value, n_loss_type = ELossType_EXPECTED):
        lst_data = []
        n_code =  EErrorCode.ERROR_SUCCESS
        try:
            if self.__m_lst_bom:
                dict_bom = self.__m_lst_bom[0]
                #print(n_unit, n_value)
                if n_unit == EUnit.KILOGRAM: #公斤
                    for dict_item in dict_bom.get("children", []):
                        f_loss = self.__get_loss(n_loss_type, dict_item)
                        #print(dict_item["count"], dict_item["weight"], f_loss)
                        n_unit = EUnit.KILOGRAM
                        f_value = round((((n_value / dict_bom["weight"]) * dict_item["weight"])*( 1.0 + f_loss)), 2) if dict_bom["weight"]  else 0
                        lst_data.append(self.__create_data(dict_item, n_unit, f_value))
                elif n_unit == EUnit.CASE: #箱
                    for dict_item in dict_bom.get("children", []):
                        #print("item1", dict_item["count"], dict_item["weight"], dict_item["unit"])
                        if dict_item.get("category", 0) == EItemCategory.PRODUCT:
                            for dict_item2 in dict_item.get("children", []):
                                f_loss = self.__get_loss(n_loss_type, dict_item2)
                                n_unit, f_value = self.__cal_value(dict_item2.get("category", 0),
                                                                   n_value * dict_item["count"]* dict_item2["count"], dict_item2["weight"],
                                                                   dict_item2.get("length", 0),  f_loss)
                                #print("item2", dict_item2["count"], dict_item2["weight"], dict_item2["unit"], f_loss)
                                lst_data.append(self.__create_data(dict_item2, n_unit, f_value))

                        else:
                            f_loss = self.__get_loss(n_loss_type, dict_item)
                            n_unit, f_value = self.__cal_value(dict_item.get("category", 0), n_value * dict_item["count"],
                                                               dict_item["weight"], dict_item.get("length",0), f_loss)

                            lst_data.append(self.__create_data(dict_item, n_unit, f_value))
                            #print("item1 loss", f_loss)
                else: # 盒/桶/包
                    if dict_bom.get("count_unit", 0) == EUnit.CASE:
                        for dict_item in dict_bom.get("children", []):
                            if dict_item.get("category", 0) == EItemCategory.PRODUCT:
                                dict_bom = dict_item
                                break
                    for dict_item in dict_bom.get("children", []):
                        f_loss = self.__get_loss(n_loss_type, dict_item)
                        #print(dict_item["count"], dict_item["weight"], dict_item["unit"], f_loss)
                        n_unit, f_value = self.__cal_value(dict_item.get("category",0), n_value * dict_item["count"], dict_item["weight"], dict_item.get("length",0), f_loss)
                        lst_data.append(self.__create_data(dict_item, n_unit, f_value))
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_data

    def __get_loss(self, n_loss_type, dict_item):
        if n_loss_type == self.ELossType_EXPECTED:
            f_loss = round(dict_item.get("expectedLoss", 0) / 100.0, 2) if dict_item.get("expectedLoss",
                                                                                         0) else 0
        else:
            f_loss = round(dict_item.get("actualLoss", 0) / 100.0, 2) if dict_item.get("actualLoss",
                                                                                       0) else 0
        return f_loss

    def __create_data(self, dict_item, n_unit, f_value):
        dict_data = {
            "item_no": dict_item["no"],
            "item_name": dict_item["name"],
            "unit": n_unit,
            "value": f_value
        }

        #print(dict_data)
        return dict_data

    def __cal_value(self, n_category, n_count, f_weight, f_length, f_loss ):
        if n_category == EItemCategory.MA and not f_length:

            f_value = math.ceil(n_count * (1.0 + f_loss))
            n_unit = EUnit.ITEM
        else:
            f_value = round((n_count * f_weight * (1.0 + f_loss)) / 1000.0, 2)  # g to kg
            n_unit = EUnit.KILOGRAM
        return n_unit, f_value