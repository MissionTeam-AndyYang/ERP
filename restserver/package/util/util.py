# coding=utf8
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")
import time
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from sqlalchemy.orm import class_mapper
from package.common.common import *
from package.dbwrapper.table import *
from package.dbwrapper.dbmgr import CDBMgr

def object_as_dict(obj):
    return {c.key: (getattr(obj, c.key) if getattr(obj, c.key) is not None else '')
            for c in class_mapper(obj.__class__).columns}

def util_convert_time(obj_date):
    """將 datetime 物件轉換為 UTC 時間的 Unix Timestamp"""
    obj_date = obj_date.replace(tzinfo=timezone.utc)  # 明確指定為 UTC 時間
    return int(obj_date.timestamp())  # 直接取得 UTC timestamp（秒）

def util_retrieve_now_time():
    """ 取得當前 UTC 時間的 Unix Timestamp """
    return int(datetime.now(timezone.utc).timestamp())


def util_convert_timestamp_to_date2(n_timestamp, n_added_days=0):
    """
    轉換 Unix Timestamp 並增加天數，回傳 UTC 時間的 Unix Timestamp（取到日期為基準）
    """
    if not n_timestamp:
        return 0

    # 轉換 timestamp 為 UTC datetime，並將時間歸零（00:00:00）
    dt = datetime.fromtimestamp(int(n_timestamp), tz=timezone.utc) + timedelta(days=n_added_days)
    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)  # 設定為 UTC 的 00:00:00

    # 轉換為 UTC timestamp（秒級整數）
    return int(dt.timestamp())

def util_convert_timestamp_to_date(n_timestamp, n_added_days=0):
    n_date = 0
    if n_timestamp:
        if os.name == 'nt':
            n_date = int(time.mktime((datetime.strptime(datetime.fromtimestamp(n_timestamp).strftime('%Y%m%d'), '%Y%m%d')
                                      + timedelta(days=n_added_days)).timetuple()))
        else:
            n_date = int((datetime.strptime(datetime.fromtimestamp(n_timestamp).strftime('%Y%m%d'), '%Y%m%d')
                          + timedelta(days=n_added_days)).strftime('%s'))
    return n_date

def util_convert_timestamp_to_str(n_timestamp):
    str_time = ''
    if n_timestamp:
        str_time = datetime.utcfromtimestamp(n_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return str_time

def util_convert_to_g(n_unit, f_count) -> float:
    unit_conversion = {
        EUnit.KILOGRAM: 1000.0  # 1 公斤 = 1 公斤（不變）
    }

    if n_unit not in unit_conversion:
        raise ValueError(f"無效的單位: {n_unit}, 只能使用 'kg'")

    return round(f_count * unit_conversion[n_unit], 2)

def util_convert_to_kg(f_count, n_unit) -> float:
    unit_conversion = {
        EUnit.GRAM: 0.001,  # 1 公克 = 0.001 公斤
        EUnit.TAIJIN: 0.6,  # 1 台斤 = 0.6 公斤
        EUnit.KILOGRAM: 1.0  # 1 公斤 = 1 公斤（不變）
    }

    if n_unit not in unit_conversion:
        raise ValueError(f"無效的單位: {n_unit}, 只能使用 'g', 'jin', 'kg'")

    return round(f_count * unit_conversion[n_unit], 2)



def util_get_item_info( str_item_no):
    n_category = 0
    n_subCategory = 0
    str_item_name = ""

    with CDBMgr() as obj_dbmgr:
        obj_session = obj_dbmgr.get_session()
        obj_prodcut = (
            obj_session.query(CTableProduct)
            .filter(CTableProduct.no == str_item_no)
            .first()
        )
        if obj_prodcut:
            n_category = EItemCategory.PRODUCT
            str_item_name = obj_prodcut.name
            n_subCategory = obj_prodcut.category
        else:
            obj_inprodcut = (
                obj_session.query(CTableInproduct)
                .filter(CTableInproduct.no == str_item_no)
                .first()
            )
            if obj_inprodcut:
                n_category = EItemCategory.INPRODUCT
                str_item_name = obj_inprodcut.name
            else:
                obj_material = (
                    obj_session.query(CTableMaterial)
                    .filter(CTableMaterial.no == str_item_no)
                    .first()
                )
                if obj_material:
                    n_category = obj_material.category
                    n_subCategory= obj_material.subCategory
                    str_item_name = obj_material.name
    return  n_category, n_subCategory, str_item_name

def util_new_get_item_info( str_item_no):
    str_name = ''
    n_category = 0
    n_subCategory = 0
    n_unitWarehouse = 0
    n_unitProduct = 0

    with CDBMgr() as obj_dbmgr:
        obj_session = obj_dbmgr.get_session()
        obj_prodcut = (
            obj_session.query(CTableProduct)
            .filter(CTableProduct.no == str_item_no)
            .first()
        )
        if obj_prodcut:
            n_category = EItemCategory.PRODUCT
            str_name = obj_prodcut.name
            n_subCategory = obj_prodcut.category
            n_unitWarehouse = obj_prodcut.unitWarehouse
            n_unitProduct = obj_prodcut.unitProduct
        else:
            obj_inprodcut = (
                obj_session.query(CTableInproduct)
                .filter(CTableInproduct.no == str_item_no)
                .first()
            )
            if obj_inprodcut:
                str_name = obj_inprodcut.name
                n_category = EItemCategory.INPRODUCT
                n_unitWarehouse = obj_inprodcut.unitWarehouse
                n_unitProduct = obj_inprodcut.unitProduct
            else:
                obj_material = (
                    obj_session.query(CTableMaterial)
                    .filter(CTableMaterial.no == str_item_no)
                    .first()
                )
                if obj_material:
                    str_name = obj_material.name
                    n_category = obj_material.category
                    n_subCategory= obj_material.subCategory
                    n_unitWarehouse = obj_material.unitWarehouse
                    n_unitProduct = obj_material.unitProduct
                else:
                    obj_goods = (
                        obj_session.query(CTableGoods)
                        .filter(CTableGoods.no == str_item_no)
                        .first()
                    )
                    if obj_goods:
                        str_name = obj_goods.name
                        n_category = EItemCategory.GOODS
                        n_unitWarehouse = obj_goods.unitWarehouse
                        n_unitProduct = obj_goods.unitProduct
    return  str_name, n_category, n_subCategory, n_unitWarehouse, n_unitProduct


# ------------------------------------------------------------
# Common value conversion and numeric output helpers
# ------------------------------------------------------------

def util_safe_float(obj_value):
    try:
        return float(obj_value) if obj_value is not None else 0.0
    except (TypeError, ValueError):
        return 0.0


def util_safe_int(obj_value):
    try:
        return int(obj_value) if obj_value is not None else 0
    except (TypeError, ValueError):
        return 0


def util_round_price(obj_value):
    return float(
        Decimal(str(util_safe_float(obj_value))).quantize(
            Decimal("0.0001"),
            rounding=ROUND_HALF_UP,
        )
    )


def util_round_quantity(obj_value):
    return float(
        Decimal(str(util_safe_float(obj_value))).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
    )


def util_round_amount(obj_value):
    return int(
        Decimal(str(util_safe_float(obj_value))).quantize(
            Decimal("1"),
            rounding=ROUND_HALF_UP,
        )
    )


def util_build_day_range(n_timestamp, str_timezone):
    try:
        obj_tz = ZoneInfo(str_timezone or "UTC")
    except Exception:
        obj_tz = timezone.utc
    obj_local = datetime.fromtimestamp(util_safe_int(n_timestamp), timezone.utc).astimezone(obj_tz)
    obj_start_local = obj_local.replace(hour=0, minute=0, second=0, microsecond=0)
    n_start = util_safe_int(obj_start_local.astimezone(timezone.utc).timestamp())
    return {
        "date": obj_local.strftime("%Y-%m-%d"),
        "startTimestamp": n_start,
        "endTimestamp": n_start + 86399,
    }


def util_build_task_date_range(n_timestamp, str_timezone, str_date_range):
    dict_day_range = util_build_day_range(n_timestamp, str_timezone)
    str_mode = str_date_range or "today"
    n_start = util_safe_int(dict_day_range.get("startTimestamp"))
    if str_mode == "next_7_days":
        return {
            "mode": str_mode,
            "startTimestamp": n_start,
            "endTimestamp": n_start + 7 * 86400 - 1,
            "applyRange": True,
        }
    if str_mode == "overdue":
        return {
            "mode": str_mode,
            "startTimestamp": 0,
            "endTimestamp": n_start - 1,
            "applyRange": True,
        }
    if str_mode == "all_open":
        return {
            "mode": str_mode,
            "startTimestamp": 0,
            "endTimestamp": 0,
            "applyRange": False,
        }
    return {
        "mode": "today",
        "startTimestamp": n_start,
        "endTimestamp": n_start + 86399,
        "applyRange": True,
    }


def util_build_period_range(n_query_timestamp, str_period, dict_period_days, str_default_period):
    str_period = str_period if str_period in dict_period_days else str_default_period
    n_days = util_safe_int(dict_period_days.get(str_period))
    n_end_timestamp = util_safe_int(n_query_timestamp)
    n_start_timestamp = max(n_end_timestamp - n_days * 86400, 0)
    return {
        "period": str_period,
        "startTimestamp": n_start_timestamp,
        "endTimestamp": n_end_timestamp,
    }



'''
def util_convert_time(obj_date):
    if os.name == 'nt':
        n_date = int(time.mktime(obj_date.timetuple()))
    else:
        n_date = int(obj_date.strftime('%s'))
    return n_date


def util_retrieve_now_time():
    if os.name == 'nt':
        n_date = int(time.mktime(datetime.now().timetuple()))
    else:
        n_date = int(datetime.now().strftime('%s'))
    return n_date


def util_convert_timestamp_to_date(n_timestamp, n_added_days=0):
    n_date = 0
    if n_timestamp:
        if os.name == 'nt':
            n_date = int(time.mktime((datetime.strptime(datetime.fromtimestamp(n_timestamp).strftime('%Y%m%d'), '%Y%m%d')
                                      + timedelta(days=n_added_days)).timetuple()))
        else:
            n_date = int((datetime.strptime(datetime.fromtimestamp(n_timestamp).strftime('%Y%m%d'), '%Y%m%d')
                          + timedelta(days=n_added_days)).strftime('%s'))
    return n_date

def util_convert_timestamp_to_str(n_timestamp):
    str_time = ''
    if n_timestamp:
        str_time = datetime.utcfromtimestamp(n_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return str_time

def util_convert_timestamp_to_local_str(n_timestamp):
    from datetime import datetime
    import pytz
    # 转换时间戳为 UTC 时间
    utc_time = datetime.utcfromtimestamp(n_timestamp)
    local_timezone = pytz.timezone('Asia/Taipei')
    # 将 UTC 时间转换为本地时间
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    str_time = local_time.strftime('%Y-%m-%d')

    return str_time
'''
def util_retrieve_config_path():
    str_path = ''
    if getattr(sys, 'frozen', False):
        str_path = os.path.dirname(sys.executable)
    elif __file__:
        str_path = os.path.join(os.path.dirname(__file__), os.pardir)
        if str_path:
            str_path = os.path.join(str_path, 'config')
    return str_path


def util_random_code(n_k):
    import random
    import string
    str_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=n_k))
    return str_code



