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


class CPrice(object):
    def get(self, str_item_no, n_itemCategory):
        dict_price = {"warehouse":{"price": 0,
                                   "unit": 0}}
        n_unit = 0
        f_price = 0
        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                obj_price = None
                if n_itemCategory in [EItemCategory.PM, EItemCategory.MA, EItemCategory.AF]:
                    obj_price = (
                        obj_session.query(
                            func.greatest(
                                func.ifnull(CTableMaterialPrice.warehouseUnitWeight, 0),
                                func.ifnull(CTableMaterialPrice.warehouseUnitLength, 0),
                                func.ifnull(CTableMaterialPrice.warehouseUnitCount, 0)
                            ).label("warehouseUnit"),  # 取得有數值的庫存單位
                            func.greatest(
                                func.ifnull(CTableMaterialPrice.warehousePriceWeight, 0),
                                func.ifnull(CTableMaterialPrice.warehousePriceLength, 0),
                                func.ifnull(CTableMaterialPrice.warehousePriceCount, 0)
                            ).label("warehousePrice")
                        )
                        .filter(CTableMaterialPrice.item_no == str_item_no)
                        .first()
                    )
                elif n_itemCategory == EItemCategory.INPRODUCT:
                    obj_price = (
                        obj_session.query(CTableInproductPrice)
                        .filter(CTableInproductPrice.item_no == str_item_no)
                        .first()
                    )
                elif n_itemCategory == EItemCategory.PRODUCT:
                    obj_price = (
                        obj_session.query(CTableProductPrice)
                        .filter(CTableProductPrice.item_no == str_item_no)
                        .first()
                    )
                n_unit = obj_price.warehouseUnit if obj_price else 0
                f_price = obj_price.warehousePrice if obj_price else 0

        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_unit, f_price
