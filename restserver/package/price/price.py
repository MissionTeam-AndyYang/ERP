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
        n_unit = 0
        f_price = 0
        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                obj_price = (
                    obj_session.query(
                        CTableItemPrice.whUnitWeight,
                        CTableItemPrice.whPriceWeight
                    )
                    .filter(CTableItemPrice.item_no == str_item_no)
                    .order_by(CTableItemPrice.date.desc())
                    .first()
                )
                n_unit = obj_price.whUnitWeight if obj_price else 0
                f_price = obj_price.whPriceWeight if obj_price else 0

        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_unit, f_price
