# coding=utf8
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")
import time
from datetime import datetime, timedelta, timezone
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
    str_item_ref_no = ""
    str_item_ref_displayName = ""

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
            str_item_ref_no = obj_prodcut.customer_no
            str_item_ref_displayName = obj_prodcut.customer_displayName
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
                str_item_ref_no = obj_inprodcut.customer_no
                str_item_ref_displayName = obj_inprodcut.customer_displayName
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
                    str_item_ref_no = obj_material.supplier_no
                    str_item_ref_displayName = obj_material.supplier_displayName
    return  n_category, n_subCategory, str_item_name,  str_item_ref_no,  str_item_ref_displayName

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



