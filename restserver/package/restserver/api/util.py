# coding=utf8

from sqlalchemy.orm import class_mapper
from package.dbwrapper.table import *
from .common import *
from package.common.common import *
from package.dbwrapper.dbmgr import CDBMgr
from sqlalchemy import desc, asc


def get_paginated_data(obj_session, model_class, lst_filters=None, order_by=None, n_start=0, n_count=0):
    """
    通用分頁查詢函式
    :param obj_session: SQLAlchemy session
    :param model_class: 資料表類別 (例如 CTableGoods)
    :param filters: 濾鏡列表 (list of criteria)
    :param order_by: 排序欄位物件 (例如 CTableGoods.no.desc())
    :param n_start: 起始索引
    :param n_count: 取得數量 (0 表示不限制)
    :return: (total_count, list_result)
    """
    # 1. 基礎查詢
    obj_query = obj_session.query(model_class)

    # 2. 加入過濾條件
    if lst_filters:
        obj_query = obj_query.filter(*lst_filters)

    # 3. 計算總數 (在排序與分頁前)
    n_total = obj_query.count()

    # 4. 處理排序 (若未提供則預設使用 ID 倒序)
    if order_by is not None:
        obj_query = obj_query.order_by(order_by)
    else:
        obj_query = obj_query.order_by(model_class.no.desc())

    # 5. 處理分頁
    if n_count > 0:
        obj_query = obj_query.offset(n_start).limit(n_count)

    return n_total, obj_query.all()

def object_as_dict(obj):
    return {c.key: (getattr(obj, c.key) if getattr(obj, c.key) is not None else '')
            for c in class_mapper(obj.__class__).columns}


def get_server_id():
    import socket

    str_server_id = socket.gethostname()
    return str_server_id


def get_order_type(str_ref_no):
    n_type = EBatchOrderCategory.NONE
    if str_ref_no:
        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            obj_result = (obj_session.query(CTableGoodsReceiptNote)
                          .filter(CTableGoodsReceiptNote.no == str_ref_no)
                          .first())
            if obj_result:
                n_type = EBatchOrderCategory.PURCHASE
            else:
                obj_result = (obj_session.query(CTableProcessOrder)
                              .filter(CTableProcessOrder.no == str_ref_no)
                              .first())
                if obj_result:
                    n_type = EBatchOrderCategory.PRODUCT
                else:
                    obj_result = (obj_session.query(CTableShippingOrder)
                                  .filter(CTableShippingOrder.no == str_ref_no)
                                  .first())
                    if obj_result:
                        n_type = EBatchOrderCategory.SALE_RETURN

    return n_type


def get_output_item_info(str_item_no):
    n_category = 0
    n_subCategory = 0
    with CDBMgr() as obj_dbmgr:
        obj_session = obj_dbmgr.get_session()
        obj_prodcut = (
            obj_session.query(CTableProduct)
            .filter(CTableProduct.no == str_item_no)
            .first()
        )
        if obj_prodcut:
            n_category = EItemCategory.PRODUCT
            n_subCategory = obj_prodcut.category
        else:
            obj_inprodcut = (
                obj_session.query(CTableInproduct)
                .filter(CTableInproduct.no == str_item_no)
                .first()
            )
            if obj_inprodcut:
                n_category = EItemCategory.INPRODUCT
    return n_category, n_subCategory


def get_item_info( str_item_no):
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


def get_item_unitWarehouse(str_item_no):
    n_unitWarehouse = 0

    with CDBMgr() as obj_dbmgr:
        obj_session = obj_dbmgr.get_session()
        obj_material = (
            obj_session.query(CTableMaterial)
            .filter(CTableMaterial.no == str_item_no)
            .first()
        )

        if obj_material:
            n_unitWarehouse = obj_material.unitWarehouse
        else:

            obj_prodcut = (
                obj_session.query(CTableProduct)
                .filter(CTableProduct.no == str_item_no)
                .first()
            )
            if obj_prodcut:
                n_unitWarehouse = obj_prodcut.unitWarehouse
            else:
                obj_inprodcut = (
                    obj_session.query(CTableInproduct)
                    .filter(CTableInproduct.no == str_item_no)
                    .first()
                )
                if obj_inprodcut:
                    n_unitWarehouse = obj_inprodcut.unitWarehouse
    return  n_unitWarehouse
def convert_to_kg(f_count, n_unit) -> float:
    unit_conversion = {
        EUnit.GRAM: 1000,  # 1 公克 = 0.001 公斤
        EUnit.TAIJIN: 1.6667,  # 1 台斤 = 0.6 公斤
        EUnit.KILOGRAM: 1.0  # 1 公斤 = 1 公斤（不變）
    }

    if n_unit not in unit_conversion:
        raise ValueError(f"無效的單位: {n_unit}, 只能使用 'g', 'jin', 'kg'")

    return round(f_count * unit_conversion[n_unit], 2)




def convert_to_m(f_count, n_unit) -> float:
    unit_conversion = {
        EUnit.CM: 1000,  # 1 公分 = 0.001 公尺
        EUnit.METER: 1.0  # 1 公尺 = 1 公尺（不變）
    }

    if n_unit not in unit_conversion:
        raise ValueError(f"無效的單位: {n_unit}, 只能使用 'cm', 'm'")

    return round(f_count * unit_conversion[n_unit],2)



# convert purchase unit to warehouse unit
def retrieve_warehouse_info(obj_session, n_category, obj_batch, dict_row):
    dict_row["warehouseUnitWeight"] = 0
    dict_row["warehouseCountWeight"] = 0
    dict_row["warehouseUnitLen"] = 0
    dict_row["warehouseCountLen"] = 0
    if n_category not in [EItemCategory.INPRODUCT, EItemCategory.PRODUCT]:
        # retrieve  purchaseUnitWeight / warehouseUnitWeight for material
        # cal count
        dict_row["warehouseUnitWeight"] = dict_row["unit"] #dict_price["warehouseUnitWeight"]
        dict_row["warehouseCountWeight"] = dict_row["checkedCount"]#convert_to_kg(round(dict_row["checkedCount"] * dict_price["purchaseWeightUnit"], 2), dict_row["warehouseUnitWeight"])

    else:
        dict_row["warehouseUnitWeight"] = obj_batch.unit if obj_batch else 0
        dict_row["warehouseCountWeight"] = obj_batch.checkedCount if obj_batch else 0

