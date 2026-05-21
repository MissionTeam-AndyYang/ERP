# coding=utf8
import pytz
import json
import string
import validictory
from copy import deepcopy
from flask import request
from .util import *
from package.common.common import *
from package.log.log import CLogger
from package.dbwrapper.table import *
from package.dbwrapper.dbmgr import CDBMgr
from sqlalchemy import delete, func, select, case
import uuid
from package.util.util import *
from package.inventory.stock import *
from package.inventory.inventoryQuery import *

from collections import defaultdict
from sqlalchemy import and_, or_

def g_get_material_subCategory(obj_session, str_item_no):
    n_subCategory = 0
    if str_item_no:
        obj_tmp = (
            obj_session.query(CTableMaterial.subCategory)
            .filter(CTableMaterial.no == str_item_no)
            .first()
        )
        if obj_tmp:
            n_subCategory = obj_tmp.subCategory
    return n_subCategory



class CPrivilegeControl(object):

    def is_allowed_for_get(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.SALE and privilege['action'] in (EPrivilegeAction.VIEW, EPrivilegeAction.REPORT)
                   for privilege in lst_privileges)

    def is_allowed_for_post(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.SALE and privilege['action'] == EPrivilegeAction.CREATION
                   for privilege in lst_privileges)

    def is_allowed_for_put(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.SALE and privilege['action'] == EPrivilegeAction.MODIFICATION
                   for privilege in lst_privileges)

    def is_allowed_for_delete(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.SALE and privilege['action'] == EPrivilegeAction.CANCELLATION
                   for privilege in lst_privileges)


class CBatchTrace(CPrivilegeControl):
    TYPE_DATE = 1
    TYPE_ORDER = 2

    ORDER_PURCHASE = 1
    ORDER_PRODUCT = 2
    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0, 'results': []}
        if not request.args.get("type"):
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'invalid parameter'
        else:
            try:
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    n_total = 0
                    lst_result = []
                    if int(request.args.get("type")) == self.TYPE_DATE:
                        if request.args.get('inventoryType'):
                            # 進貨/出貨
                            n_total, lst_result = self.__retrieveByDate2(obj_session)
                        else:
                            n_total, lst_result = self.__retrieveByDate1(obj_session)
                    elif int(request.args.get("type")) == self.TYPE_ORDER:
                        if request.args.get('orderCategory'):
                            if int(request.args.get('orderCategory')) == self.ORDER_PURCHASE:
                                n_total, lst_result = self.__retrieveByOrder1(obj_session)
                            elif int(request.args.get('orderCategory')) == self.ORDER_PRODUCT:
                                n_total, lst_result = self.__retrieveByOrder2(obj_session)
                    if lst_result:
                        dict_extra_data['total'] = n_total
                        dict_extra_data['count'] = len(lst_result)
                        dict_extra_data['results'] = lst_result

            except Exception as error:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'throw exception (error: %s)' % str(error)
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                              % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def  __retrieveByDate1(self, obj_session):
        lst_result = []
        lst_where = self.__fill_query_params1()

        n_start = 0
        n_count = 0
        if request.args.get('start') and request.args.get('count'):
            n_start = int(request.args.get('start'))
            n_count = int(request.args.get('count'))

        n_total = (obj_session.query(CTableBatchNumber.no)
                   .filter(*lst_where)
                   .count())
        if n_count:
            ids_query = (obj_session.query(
                            CTableBatchNumber.no)
                         .filter(*lst_where)
                         .order_by(CTableBatchNumber.date.desc())
                         .offset(n_start)
                         .limit(n_count)
                         )

            ids = [id[0] for id in ids_query.all()]
            print("")
        else:
            ids_query = (obj_session.query(
                CTableBatchNumber.no)
                         .filter(*lst_where)
                         .order_by(CTableBatchNumber.date.desc())
                         )

            ids = [id[0] for id in ids_query.all()]

        if ids:
            lst_result = self.__fill_data(obj_session, ids)
        return n_total, lst_result

    def __retrieveByDate2(self, obj_session):
        lst_result = []
        lst_obj_result = []
        lst_where = self.__fill_query_params2()
        n_start = 0
        n_count = 0
        if request.args.get('start') and request.args.get('count'):
            n_start = int(request.args.get('start'))
            n_count = int(request.args.get('count'))

        n_total = (obj_session.query(CTableInventoryRec.batchNumber)
                   .filter(*lst_where)
                   .group_by(CTableInventoryRec.batchNumber)
                   .count())
        if n_count:
            ids_query = (obj_session.query(
                CTableInventoryRec.batchNumber)
                         .filter(*lst_where)
                         .group_by(CTableInventoryRec.batchNumber)
                         .order_by(CTableInventoryRec.date.desc())
                         .offset(n_start)
                         .limit(n_count)
                         )

            ids = [id[0] for id in ids_query.all()]
            print("")
        else:
            ids_query = (obj_session.query(
                CTableInventoryRec.batchNumber)
                         .filter(*lst_where)
                         .group_by(CTableInventoryRec.batchNumber)
                         .order_by(CTableInventoryRec.date.desc())
                         )

            ids = [id[0] for id in ids_query.all()]
        if ids:
            lst_obj_result = (
                obj_session.query(
                    CTableInventoryRec.unit, CTableBatchNumber,
                    func.sum(
                        case(
                            (
                                CTableInventoryRec.category == EInventoryCategory.IN,
                                CTableInventoryRec.count),
                            # 入庫
                            (CTableInventoryRec.category == EInventoryCategory.OUT,
                             -CTableInventoryRec.count)  # 出庫
                        )
                    ).label("remaining"),
                    CTableInventoryRec.batchNumber
                )
                .filter(CTableInventoryRec.batchNumber.in_(ids))
                .outerjoin(CTableBatchNumber, CTableInventoryRec.batchNumber == CTableBatchNumber.no)
                .group_by(CTableInventoryRec.batchNumber, CTableBatchNumber)  # 依 batchNumber 分組計算
                .all()
            )

        if lst_obj_result:
            # retrieve inventory count
            for obj_row in lst_obj_result:
                if obj_row:
                    dict_row = object_as_dict(obj_row[1]) if obj_row[1] else {"no": obj_row[3] if obj_row[3] else ""}
                    dict_row["itemSubCategory"] = 0
                    dict_row["product_order_no"] = ""
                    if dict_row.get("itemCategory", None):
                        if dict_row["itemCategory"] == EItemCategory.PM:
                            dict_row["itemSubCategory"] = g_get_material_subCategory(obj_session, dict_row["item_no"])
                        if dict_row["itemCategory"] == EItemCategory.PRODUCT:
                            dict_row["product_order_no"] = self.__get_product_order_no(obj_session, dict_row["ref_no"])

                    dict_row["remaining"] = obj_row[2]
                    dict_row["inventory_unit"] = obj_row[0]  # dict_tmp["unit"]
                    lst_result.append(dict_row)
        return n_total, lst_result

    def __fill_data(self, obj_session, ids):
        lst_result = []
        if ids:
            lst_obj_result = (
                obj_session.query(
                    CTableBatchNumber
                )
                .filter(CTableBatchNumber.no.in_(ids))
                .all()
            )

            lst_obj_inventory = (
                obj_session.query(
                    CTableInventoryRec.batchNumber,
                    func.sum(
                        case(
                            (
                                CTableInventoryRec.category == EInventoryCategory.IN,
                                CTableInventoryRec.count),
                            # 入庫
                            (CTableInventoryRec.category == EInventoryCategory.OUT,
                             -CTableInventoryRec.count)  # 出庫
                        )
                    ).label("remaining"),

                )
                .filter(CTableInventoryRec.batchNumber.in_(ids))
                .group_by(CTableInventoryRec.batchNumber)  # 依 batchNumber 分組計算
                .all()
            )

            lst_obj_price = (
                obj_session.query(
                    CTableInventoryRec.batchNumber,
                    func.round(func.avg(CTableInventoryRec.price), 2).label("avg_price")
                )
                .filter(CTableInventoryRec.batchNumber.in_(ids),
                        CTableInventoryRec.category == EInventoryCategory.IN,
                        CTableInventoryRec.source.in_([EInventorySrc.PURCHASE_RECEIVE, EInventorySrc.PRODUCT]))
                .group_by(CTableInventoryRec.batchNumber)  # 依 batchNumber 分組計算
                .all()
            )

            # batch_number 取得資料
            if lst_obj_result:
                # retrieve inventory count
                for obj_row in lst_obj_result:
                    if obj_row:
                        f_reamining = self.__find_inventory_rec(lst_obj_inventory, obj_row.no)
                        f_costPrice = self.__find_inventory_price(lst_obj_price, obj_row.no)

                        # 單位批號數量
                        dict_row = object_as_dict(obj_row) if obj_row else {"no": obj_row.no}

                        dict_row["price"] = 0 # 銷售/採購單價
                        dict_row["costPrice"] = f_costPrice  # 成本單價=盤點單價 ??
                        dict_row["itemSubCategory"] = 0
                        dict_row["itemSubCategory"] = 0
                        dict_row["ref_order_no"] = ""
                        dict_row["ref_order_category"] = EBatchTraceRefCategory.NONE
                        if dict_row.get("itemCategory", None):
                            if dict_row["itemCategory"] == EItemCategory.PM:
                                dict_row["ref_order_category"] = EBatchTraceRefCategory.PURCHASE
                                dict_row["ref_order_no"] = dict_row["ref_no"]
                                dict_row["itemSubCategory"] = g_get_material_subCategory(obj_session, dict_row["item_no"])
                                dict_row["price"] = self.__get_price(obj_session, EBatchTraceRefCategory.PURCHASE, dict_row["ref_no"])
                            if dict_row["itemCategory"] == EItemCategory.PRODUCT:
                                dict_row["ref_order_category"] = EBatchTraceRefCategory.SALE
                                dict_row["ref_order_no"] = self.__get_product_order_no(obj_session, dict_row["ref_no"])
                                dict_row["price"] = self.__get_price(obj_session, EBatchTraceRefCategory.SALE,
                                                           dict_row["ref_no"])

                        dict_row["remaining"] = f_reamining
                        dict_row["inventory_unit"] = dict_row["unit"]
                        lst_result.append(dict_row)
        return lst_result

    def __find_inventory_rec(self, lst_obj_result, str_batchNo):
        f_remainig = 0

        for obj_row in lst_obj_result:
            if obj_row:
                # 單位批號數量
                if obj_row[0] == str_batchNo:
                    f_remainig = obj_row[1]
                    break
        return f_remainig

    def __find_inventory_price(self, lst_obj_result, str_batchNo):
        f_cost_price = 0

        for obj_row in lst_obj_result:
            if obj_row:
                # 單位批號數量
                if obj_row[0] == str_batchNo:
                    f_cost_price = obj_row[1]
                    break
        return f_cost_price

    def __get_price(self, obj_session, n_ref_category, str_ref_no):
        f_price = 0

        if n_ref_category == EBatchTraceRefCategory.PURCHASE:
            obj_order = (
                obj_session.query(
                    CTableGoodsReceiptNote.price
                )
                .filter(CTableGoodsReceiptNote.no == str_ref_no)
                .first()
            )
            if obj_order:
                f_price = obj_order.price
        else:
            str_order_no = self.__get_product_order_no(obj_session, str_ref_no)
            if str_order_no:
                obj_order = (
                    obj_session.query(
                        CTableProductOrder.price
                    )
                    .filter(CTableProductOrder.no == str_order_no)
                    .first()
                )
                if obj_order:
                    f_price = obj_order.price
        return f_price

    def  __retrieveByOrder1(self, obj_session):
        n_total = 0
        lst_result = []
        lst_obj_result = []
        lst_where = [CTableGoodsReceiptNote.purchase_order_no == request.args.get('order')]

        note_ids_query = (obj_session.query(
            CTableGoodsReceiptNote.no)
                     .filter(*lst_where)
                     .group_by(CTableGoodsReceiptNote.no)
                     )
        note_ids = [id[0] for id in note_ids_query.all()]
        if note_ids:
            n_total = (obj_session.query(CTableBatchNumber.no)
                       .filter(CTableBatchNumber.ref_no.in_(note_ids))
                       .group_by(CTableBatchNumber.ref_no)
                       .count())

            n_start = 0
            n_count = 0
            if request.args.get('start') and request.args.get('count'):
                n_start = int(request.args.get('start'))
                n_count = int(request.args.get('count'))

            if n_count:
                ids_query = (obj_session.query(CTableBatchNumber.no)
                             .filter(CTableBatchNumber.ref_no.in_(note_ids))
                             .group_by(CTableBatchNumber.ref_no)
                             .order_by(CTableBatchNumber.validDate.desc())
                             .offset(n_start)
                             .limit(n_count))
                ids = [id[0] for id in ids_query.all()]
            else:
                ids_query = (obj_session.query(CTableBatchNumber.no)
                             .filter(CTableBatchNumber.ref_no.in_(note_ids))
                             .group_by(CTableBatchNumber.ref_no)
                             .order_by(CTableBatchNumber.validDate.desc())
                             )
                ids = [id[0] for id in ids_query.all()]
            if ids:
                lst_obj_result = (
                    obj_session.query(
                        CTableInventoryRec.unit, CTableBatchNumber,
                        func.sum(
                            case(
                                (
                                    CTableInventoryRec.category == EInventoryCategory.IN,
                                    CTableInventoryRec.count),
                                # 入庫
                                (CTableInventoryRec.category == EInventoryCategory.OUT,
                                 -CTableInventoryRec.count)  # 出庫
                            )
                        ).label("remaining")
                    )
                    .filter(CTableInventoryRec.batchNumber.in_(ids))
                    .outerjoin(CTableBatchNumber, CTableInventoryRec.batchNumber == CTableBatchNumber.no)
                    .group_by(CTableInventoryRec.batchNumber, CTableBatchNumber)  # 依 batchNumber 分組計算
                    .all()
                )

            if lst_obj_result:
                # retrieve inventory count
                for obj_row in lst_obj_result:
                    if obj_row:
                        # dict_tmp = object_as_dict(obj_row[0])
                        dict_row = object_as_dict(obj_row[1]) if obj_row[1] else {}
                        dict_row["remaining"] = obj_row[2]
                        dict_row["inventory_unit"] = obj_row[0]  # dict_tmp["unit"]
                        lst_result.append(dict_row)
        return n_total, lst_result

    def  __retrieveByOrder2(self, obj_session):
        n_total = 0
        lst_result = []
        lst_obj_result = []

        note_ids_query = (obj_session.query(
            CTableProductionData.work_order_no)
                     .filter(CTableProductionData.product_order_no == request.args.get('order'),
                             CTableProductionData.oneProcess == 3)
                     .group_by(CTableProductionData.work_order_no)
                     .order_by(CTableProductionData.date.asc())
                     )
        note_ids = [id[0] for id in note_ids_query.all()]
        if note_ids:
            n_total = (obj_session.query(CTableProductionDataOutput.batch_number)
                       .filter(CTableProductionDataOutput.work_order_no.in_(note_ids))
                       .group_by(CTableProductionDataOutput.work_order_no)
                       .count())

            n_start = 0
            n_count = 0
            if request.args.get('start') and request.args.get('count'):
                n_start = int(request.args.get('start'))
                n_count = int(request.args.get('count'))

            if n_count:
                ids_query = (obj_session.query(CTableProductionDataOutput.batch_number)
                             .filter(CTableProductionDataOutput.work_order_no.in_(note_ids))
                             .group_by(CTableProductionDataOutput.work_order_no)
                             .offset(n_start)
                             .limit(n_count))
                ids = [id[0] for id in ids_query.all()]
            else:
                ids_query = (obj_session.query(CTableProductionDataOutput.batch_number)
                             .filter(CTableProductionDataOutput.work_order_no.in_(note_ids))
                             .group_by(CTableProductionDataOutput.work_order_no)
                             .order_by(CTableBatchNumber.validDate.desc())
                             )
                ids = [id[0] for id in ids_query.all()]
            if ids:
                lst_obj_result = (
                    obj_session.query(
                        CTableInventoryRec.unit, CTableBatchNumber,
                        func.sum(
                            case(
                                (
                                    CTableInventoryRec.category == EInventoryCategory.IN,
                                    CTableInventoryRec.count),
                                # 入庫
                                (CTableInventoryRec.category == EInventoryCategory.OUT,
                                 -CTableInventoryRec.count)  # 出庫
                            )
                        ).label("remaining")
                    )
                    .filter(CTableInventoryRec.batchNumber.in_(ids))
                    .outerjoin(CTableBatchNumber, CTableInventoryRec.batchNumber == CTableBatchNumber.no)
                    .group_by(CTableInventoryRec.batchNumber, CTableBatchNumber)  # 依 batchNumber 分組計算
                    .all()
                )

            if lst_obj_result:
                # retrieve inventory count
                for obj_row in lst_obj_result:
                    if obj_row:
                        # dict_tmp = object_as_dict(obj_row[0])
                        dict_row = object_as_dict(obj_row[1]) if obj_row[1] else {}
                        dict_row["remaining"] = obj_row[2]
                        dict_row["inventory_unit"] = obj_row[0]  # dict_tmp["unit"]
                        lst_result.append(dict_row)
        return n_total, lst_result

    def __fill_query_params1(self):
        lst_where = []
        if request.args.get('start_date') and request.args.get('end_date'):
            # get the range of timestamp
            n_start = util_convert_timestamp_to_date(int(request.args.get('start_date')))
            if int(request.args.get('start_date')) == int(request.args.get('end_date')):
                n_end = util_convert_timestamp_to_date(n_start, 1) - 1
            else:
                n_end = util_convert_timestamp_to_date(int(request.args.get('end_date')), 1) - 1
            lst_where.append(CTableBatchNumber.date.between(n_start, n_end))

        if request.args.get('itemNo'):
            lst_where.append(CTableBatchNumber.item_no == request.args.get('itemNo'))

        if request.args.get('itemCategory'):
            lst_where.append(CTableBatchNumber.itemCategory == int(request.args.get('itemCategory')))
        else:
            lst_where.append(CTableBatchNumber.itemCategory.in_([1, 5]))
        return lst_where


    def __fill_query_params2(self):
        lst_where = []
        if request.args.get('start_date') and request.args.get('end_date'):
            # get the range of timestamp
            n_start = util_convert_timestamp_to_date(int(request.args.get('start_date')))
            if int(request.args.get('start_date')) == int(request.args.get('end_date')):
                n_end = util_convert_timestamp_to_date(n_start, 1) - 1
            else:
                n_end = util_convert_timestamp_to_date(int(request.args.get('end_date')), 1) - 1
            lst_where.append(CTableInventoryRec.date.between(n_start, n_end))
            
        if request.args.get('itemNo'):
            lst_where.append(CTableInventoryRec.item_no == request.args.get('itemNo'))

        if request.args.get('inventoryType'):
            lst_where.append(CTableInventoryRec.category == int(request.args.get('inventoryType')))

        if not request.args.get('itemCategory'):
            if request.args.get('inventoryType'):
                if int(request.args.get('inventoryType')) == EInventoryCategory.IN:
                    lst_where.append(
                        or_(
                            and_(
                                CTableInventoryRec.itemCategory == 1,
                                CTableInventoryRec.source == 1
                            ),
                            and_(
                                CTableInventoryRec.itemCategory == 5,
                                CTableInventoryRec.source == 5
                            )
                        )
                    )
                else:
                    lst_where.append(
                        and_(
                            CTableInventoryRec.itemCategory == 5,
                            CTableInventoryRec.source == 2
                        )

                    )
            else:
                lst_where.append(
                    or_(
                        and_(
                            CTableInventoryRec.itemCategory == 1,
                            CTableInventoryRec.source == 1
                        ),
                        and_(
                            CTableInventoryRec.itemCategory == 5,
                            CTableInventoryRec.source == 5
                        ),
                        and_(
                            CTableInventoryRec.itemCategory == 5,
                            CTableInventoryRec.source == 2
                        )
                    )
                )

        else:
            if int(request.args.get('itemCategory')) == 1:
                # 原料只有進貨
                lst_where.append(CTableInventoryRec.itemCategory == 1)
                lst_where.append(CTableInventoryRec.source == 1)

            if int(request.args.get('itemCategory')) == 5:
                lst_where.append(CTableInventoryRec.itemCategory == 5)
                if request.args.get('inventoryType'):
                    if int(request.args.get('inventoryType')) == EInventoryCategory.IN:
                        lst_where.append(CTableInventoryRec.source == 5)
                    else:
                        lst_where.append(CTableInventoryRec.source == 2)
                else:
                    lst_where.append(
                        or_(
                            and_(
                                CTableInventoryRec.category == EInventoryCategory.IN,
                                CTableInventoryRec.source == 5
                            ),
                            and_(
                                CTableInventoryRec.category == EInventoryCategory.OUT,
                                CTableInventoryRec.source == 2
                            )
                        )
                    )
        return lst_where


    def __get_product_order_no(self, obj_session, str_ref_no):
        str_order_no = ""
        if str_ref_no:
            obj_tmp = (
                obj_session.query(CTableWorkOrder.product_order_no)
                .filter(CTableWorkOrder.no == str_ref_no)
                .first()
            )

            if obj_tmp:
                str_order_no = obj_tmp.product_order_no
            else:
                obj_process_order = (
                    obj_session.query(
                        CTableProcessOrder.work_order_no
                    )
                    .filter(CTableProcessOrder.no == str_ref_no)
                    .first()
                )
                if obj_process_order:
                    obj_work_order = (
                        obj_session.query(
                            CTableWorkOrder.product_order_no
                        )
                        .filter(CTableWorkOrder.no == obj_process_order.work_order_no)
                        .first()
                    )
                    if obj_work_order:
                        str_order_no = obj_work_order.product_order_no
        return str_order_no



class CBatchRecord(CPrivilegeControl):
    TYPE_DATE = 1
    TYPE_ORDER = 2

    TYPE_PURCHASE = 1
    TYPE_SALE = 2
    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'stock': {}, 'nonWork': [], 'work': []}

        if not request.args.get("no") or not request.args.get("itemCategory"):
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'invalid parameter'
        else:
            try:
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    lst_result = []
                    dict_data = {}

                    # 取得庫存
                    dict_extra_data["stock"] = CCStockByBatchNo().get([request.args.get("no")])
                    if int(request.args.get("itemCategory")) == 1:
                        # 取得原物料入庫紀錄
                        lst_purchase = self.__retrieve_purchase_sale(self.TYPE_PURCHASE, request.args.get("no"))
                        dict_extra_data["nonWork"] = lst_purchase

                        lst_obj_result = (
                            obj_session.query(CTableProductionDataInput)
                            .join(CTableProductionData,
                                  CTableProductionDataInput.work_order_no == CTableProductionData.work_order_no)
                            .filter(CTableProductionDataInput.batch_number == request.args.get("no"),
                                    CTableProductionDataInput.action == 1)
                            .order_by(CTableProductionData.date.asc())
                            .all()
                        )

                        for n_index, obj_row in enumerate(lst_obj_result):
                            if obj_row.production_data.product_name not in dict_data:
                                dict_data[obj_row.production_data.product_name] = []
                            if obj_row.work_order_no:
                                lst_tmp = (
                                    obj_session.query(CTableProductionDataOutput)
                                    .filter(CTableProductionDataOutput.work_order_no == obj_row.work_order_no)
                                    .all()
                                )

                                for obj_tmp in lst_tmp:
                                    dict_tmp = self.__fill_data(obj_session, obj_row.batch_number, obj_row, obj_tmp)
                                    if dict_tmp:
                                        dict_data[obj_row.production_data.product_name].append(dict_tmp)

                                    if obj_tmp.category != EOutputCategory.PRODUCT:
                                        self.__recursive_query(obj_session, obj_tmp.batch_number,
                                                               dict_data[obj_row.production_data.product_name])
                    # 製成品, 取得製造產品
                    else:
                        # 取得產製品出庫紀錄
                        lst_sale = self.__retrieve_purchase_sale(self.TYPE_SALE, request.args.get("no"))
                        dict_extra_data["nonWork"] = lst_sale

                        lst_obj_result = (
                            obj_session.query(CTableProductionDataOutput)
                            .join(CTableProductionData,
                                  CTableProductionDataOutput.work_order_no == CTableProductionData.work_order_no)
                            .filter(CTableProductionDataOutput.batch_number == request.args.get("no"))
                            .order_by(CTableProductionData.date.asc())
                            .all()
                        )
                        for n_index, obj_row in enumerate(lst_obj_result):
                            if obj_row.item_name not in dict_data:
                                dict_data[obj_row.item_name] = []
                            self.__recursive_trace2(obj_session, obj_row.work_order_no, obj_row,
                                                    dict_data[obj_row.item_name])

                    if dict_data:
                        for str_name, lst_data in dict_data.items():
                            lst_tmp = sorted(lst_data, key=lambda x: x['date'])
                            dict_newItems = self.group_data_by_source_and_order(lst_tmp)
                            lst_new = []
                            for str_key, lst_data in dict_newItems.items():
                                for dict_new in lst_data:
                                    if str_key == "work":
                                        lst_input, lst_output, n_oneProcess, n_secProcess = self.__refill(
                                            dict_new["data"])
                                        dict_new["data"] = {"oneProcess": n_oneProcess, "secProcess": n_secProcess,  "input": lst_input, "output": lst_output}
                                        lst_new.append(dict_new)
                                    else:
                                        # 原料進貨
                                        pass
                            lst_result.append({"name": str_name, "records": lst_new})
                        dict_extra_data['work'] = lst_result
            except Exception as error:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'throw exception (error: %s)' % str(error)
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                              % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data



    def group_data_by_source_and_order(sef, lst_data):
        from collections import defaultdict

        grouped = {
            "work": defaultdict(list),
            "nonWork": defaultdict(list)
        }

        # 依 order + date 分群
        '''
        for item in lst_data:
            key = (item['order'], item['date'])  # 用 tuple 當 key
            if item['source'] == EActionType.WORK:
                grouped['work'][key].append(item)
            else:
                grouped['nonWork'][key].append(item)
        '''

        # 依 order + date + group 分群

        for item in lst_data:
            key = (item['order'], item['date'], item['group'])  # 用 tuple 當 key
            if item['source'] == EActionType.WORK:
                grouped['work'][key].append(item)
            else:
                grouped['nonWork'][key].append(item)

        dict_result = {
            "work": [],
            "nonWork": []
        }

        for key, items in grouped['work'].items():
            order, date, group = key
            dict_result['work'].append({
                "date": date,
                "order": order,
                "data": items
            })

        for key, items in grouped['nonWork'].items():
            order, date, group = key
            dict_result['nonWork'].append({
                "date": date,
                "order": order,
                "data": items
            })

        return dict_result

    def __retrieve_reuse_data(sef, obj_session, dict_wrok, n_subCategory=0):
        if dict_wrok:
            str_work_order_no = dict_wrok["order"]
            lst_obj_remain = (
                obj_session.query(CTableProductionDataReuse)
                .filter(CTableProductionDataReuse.work_order_no == str_work_order_no,
                        CTableProductionDataReuse.category == EItemType.REMAINING,
                        CTableProductionDataReuse.count != 0)
                .all()
            )
            for obj_data in lst_obj_remain:
                if n_subCategory and n_subCategory != obj_data.itemSubCategory:
                    continue
                dict_wrok["data"]["remain"].append({
                    "batch_no": obj_data.batch_number,
                    "item_no": obj_data.item_no,
                    "item_name": obj_data.item_name,
                    "unit": obj_data.unit,
                    "count": obj_data.count
                })

            lst_obj_waste = (
                obj_session.query(CTableProductionDataReuse)
                .filter(CTableProductionDataReuse.work_order_no == str_work_order_no,
                        CTableProductionDataReuse.category == EItemType.WASTE,
                        CTableProductionDataReuse.count != 0)
                .all()
            )
            for obj_data in lst_obj_waste:
                dict_wrok["data"]["waste"].append({
                    "batch_no": obj_data.batch_number,
                    "item_no": obj_data.item_no,
                    "item_name": obj_data.item_name,
                    "unit": obj_data.unit,
                    "count": obj_data.count
                })

        return dict_wrok

    def __retrieve_purchase_sale(self, n_type, str_batchNo):
        lst_data = []
        # 從庫存進出取得原物料進貨/製成品出貨
        n_type2 = CCInventroyRecByBatchNo.TYPE_PRODUCT_ORDER if n_type == self.TYPE_SALE else CCInventroyRecByBatchNo.TYPE_PURCHASE_ORDER
        lst_temp = CCInventroyRecByBatchNo().get(n_type2, [str_batchNo])
        for obj_data in lst_temp:
            dict_tmp = {
                "date": obj_data["date"],
                "source": EActionType.PURCHASE if n_type == self.TYPE_PURCHASE  else EActionType.SALE,
                "warehouse_no": obj_data["warehouse_no"],
                "warehouse_displayName": obj_data["warehouse_displayName"],
                "itemCategory": obj_data["itemCategory"],
                "itemType": obj_data["itemType"],
                "item_no": obj_data["item_no"],
                "item_name": obj_data["item_name"],
                "batchNumber": str_batchNo,
                "serialNo": obj_data["serialNo"],
                "validDate": obj_data["validDate"],
                "count": obj_data["count"],
                "amount": obj_data["amount"],
                "unit": obj_data["unit"],
                "order": obj_data["ref_no"]
            }
            lst_data.append(dict_tmp)
        return lst_data

    def group_data_by_source_and_order2(sef, lst_data):
        from collections import defaultdict

        grouped = {
            "work": defaultdict(list),
            "nonWork": defaultdict(list)
        }

        #依 order + date 分群
        for item in lst_data:
            key = (item['order'], item['date'])  # 用 tuple 當 key
            if item['source'] ==  EActionType.WORK:
                grouped['work'][key].append(item)
            else:
                grouped['nonWork'][key].append(item)


        dict_result = {
            "work": [],
            "nonWork": []
        }

        for key, items in grouped['work'].items():
            order, date = key
            dict_result['work'].append({
                "date": date,
                "order": order,
                "data": items
            })

        for key, items in grouped['nonWork'].items():
            order, date = key
            dict_result['nonWork'].append({
                "date": date,
                "order": order,
                "data": items
            })

        return dict_result

    def __retrieve_sale2(self, obj_session, lst_output):
        lst_data = []
        # 取得在製品/製成品出貨訂單
        for dict_output in lst_output:
            print(dict_output["output_batch_no"])
            lst_sale = (
                obj_session.query(CTableInventoryRec)
                .filter(CTableInventoryRec.batchNumber == dict_output["output_batch_no"],
                        CTableInventoryRec.refCategory == EInventoryOrderCategory.SALE)
                .all()
            )

            for obj_sale in lst_sale:
                dict_temp = {
                    "date": obj_sale.date,
                    "order": obj_sale.ref_no,
                    "data": {"oneProcess": 0, "secProcess" : 0,  "input": [], "output": [], "remain":[], "waste":[]}
                }
                dict_tmp = {
                    "date": obj_sale.date,
                    "source": EActionType.SALE,
                    "category": obj_sale.itemCategory,
                    "item_no": obj_sale.item_no,
                    "item_name": obj_sale.item_name,
                    "batch_number": obj_sale.batchNumber,
                    "validDate": "",
                    "count": obj_sale.count,
                    "unit": obj_sale.unit,
                    "output_batch_no": "",
                    "output_item_no": "",
                    "output_item_name": "",
                    "output_itemType": 0,
                    "output_validDate": 0,
                    "output_unit": 0,
                    "output_count": 0,
                    "order": obj_sale.ref_no,
                    "oneProcess": 0,
                    "secProcess": 0
                }
                dict_temp["data"]["input"].append(dict_tmp)
                lst_data.append(dict_temp)
        return lst_data


    def __recursive_query(self, obj_session, str_batch_no, lst_data, visited=None):
        if visited is None:
            visited = set()

        if str_batch_no in visited:  # 避免循環遞迴
            return
        visited.add(str_batch_no)
        # 查詢對應 batch_number 的 CTableProductionDataInput
        if str_batch_no:
            lst_tmp1 = (
                obj_session.query(CTableProductionDataInput)
                .filter(CTableProductionDataInput.batch_number == str_batch_no,
                        CTableProductionDataInput.action == 1)
                .all()
            )

            for obj_tmp1 in lst_tmp1:
                lst_tmp2 = (
                    obj_session.query(CTableProductionDataOutput)
                    .filter(CTableProductionDataOutput.work_order_no == obj_tmp1.work_order_no,
                            CTableProductionDataOutput.group == obj_tmp1.group)
                    .all()
                )
                # 產出多個批號
                for obj_tmp2 in lst_tmp2:
                    print(obj_tmp1.work_order_no, obj_tmp1.group, obj_tmp2.group)
                    dict_data = self.__fill_data(obj_session, str_batch_no, obj_tmp1, obj_tmp2)
                    if dict_data:
                        lst_data.append(dict_data)
                    if obj_tmp2.category != EOutputCategory.PRODUCT:
                        self.__recursive_query(obj_session, obj_tmp2.batch_number, lst_data, visited)


    def __recursive_trace2(self, obj_session, str_work_order_no, output_item, lst_data, visited=None):
        if visited is None:
            visited = set()

        if str_work_order_no in visited:  # 避免無限循環
            return
        visited.add(str_work_order_no)

        # 查詢此工單的所有投入 (`CTableProductionDataInput`)
        str_group = output_item.group
        lst_input = (
            obj_session.query(CTableProductionDataInput)
            .filter(CTableProductionDataInput.work_order_no == str_work_order_no,
                    CTableProductionDataInput.group == str_group,
                    CTableProductionDataInput.action == 1)
            .all()
        )

        for obj_input in lst_input:
            # 取得原料進貨訂單
            if obj_input.category == EItemCategory.PM:
                obj_data = self.__get_batchNum(obj_session, obj_input.batch_number)
                if obj_data:
                    dict_tmp = {
                        "date": obj_data.date,
                        "source": EActionType.PURCHASE,
                        "group": obj_input.group,
                        "itemCategory": obj_data.itemCategory,
                        "itemType": obj_data.itemType,

                        "item_no": obj_data.item_no,
                        "item_name": obj_data.item_name,
                        "batch_number": obj_data.no,
                        "validDate": obj_data.validDate,
                        "count": obj_data.checkedCount,
                        "unit": obj_data.unit,
                        "output_batch_no": "",
                        "output_item_no": "",
                        "output_item_name": "",
                        "output_itemType": 0,
                        "output_validDate": 0,
                        "output_unit": 0,
                        "output_count": 0,
                        "order": obj_data.ref_no,
                        "oneProcess": 0,
                        "secProcess": 0
                    }
                    lst_data.append(dict_tmp)


            # 過濾物料/膠捲
            if obj_input.category not in [EItemCategory.MA, EItemCategory.AF]:
                dict_tmp = self.__fill_data(obj_session, obj_input.batch_number, obj_input, output_item)
                if dict_tmp:
                    lst_data.append(dict_tmp)

            # 若 `category == INPRODUCT`，則繼續追蹤這個投入批號的輸出 (`CTableProductionDataOutput`)
            if obj_input.category == EItemCategory.INPRODUCT:
                if obj_input.batch_number:
                    lst_output = (
                        obj_session.query(CTableProductionDataOutput)
                        .filter(CTableProductionDataOutput.batch_number == obj_input.batch_number)
                        .all()
                    )

                    for obj_output in lst_output:
                        # 根據 `obj_output.work_order_no`，繼續遞迴查詢下一層 `work_order_no`
                        self.__recursive_trace2(obj_session, obj_output.work_order_no, obj_output, lst_data, visited)
                        #self.__recursive_trace2(obj_session, obj_output.work_order_no, obj_input, lst_data, visited)
    def __get_validDate(self, obj_session, str_batch_no):
        n_validDate = 0
        n_itemType = 0
        obj_tmp = (
            obj_session.query(CTableBatchNumber)
            .filter(CTableBatchNumber.no == str_batch_no)
            .first()
        )
        if obj_tmp:
            n_validDate = obj_tmp.validDate
            n_itemType = obj_tmp.itemType
        return n_validDate,  n_itemType

    def __get_batchNum(self, obj_session, str_batch_no):
        if str_batch_no:
            obj_tmp = (
                obj_session.query(CTableBatchNumber)
                .filter(CTableBatchNumber.no == str_batch_no)
                .first()
            )
        else:
            obj_tmp = None
        return obj_tmp if obj_tmp else None


    def __fill_data(self, obj_session, str_batch_no, obj_data1, obj_data2):
        n_count = 0
        dict_data = {}
        # obj_data1為投入物
        # 扣除退料的數量
        obj_return = (
            obj_session.query(CTableProductionDataInput)
            .filter(
                CTableProductionDataInput.work_order_no == obj_data1.work_order_no,
                CTableProductionDataInput.batch_number == str_batch_no,
                CTableProductionDataInput.action == 2)
            .first()
        )
        if obj_return:
            n_count = obj_data1.count - obj_return.count
            #obj_data1.count  = obj_data1.count - obj_return.count
        if n_count:
            n_validDate, n_itemType = self.__get_validDate(obj_session, str_batch_no)
            n_validDate2, n_itemType2 = self.__get_validDate(obj_session, obj_data2.batch_number)
            dict_data = {
                "group": obj_data1.group,
                "date": obj_data1.production_data.date,
                "source": EActionType.WORK,
                "itemCategory": obj_data1.category,
                "itemType": n_itemType,
                "item_no": obj_data1.item_no,
                "item_name": obj_data1.item_name,
                "batch_number": obj_data1.batch_number,
                "validDate": n_validDate,
                "count": n_count,
                "unit": obj_data1.unit,
                "output_batch_no":  obj_data2.batch_number if obj_data2 else "",
                "output_item_no": obj_data2.item_no if obj_data2 else "",
                "output_item_name": obj_data2.item_name if obj_data2 else "",
                "output_itemType": n_itemType2,
                "output_validDate": n_validDate2,
                "output_unit": obj_data2.unit if obj_data2 else "",
                "output_count": obj_data2.count if obj_data2 else "",
                "order": obj_data1.work_order_no,
                "oneProcess": obj_data1.production_data.oneProcess,
                "secProcess": obj_data1.production_data.secProcess
            }
        return dict_data

    def __refill(self, lst_data):
        n_oneProcess = 0
        n_secProcess = 0
        # 存放分類結果
        output_set = set()
        output_list = []
        input_set = set()
        input_list = []

        for item in lst_data:
            n_oneProcess = item["oneProcess"]
            n_secProcess = item["secProcess"]
            # 處理 output (去重)
            output_key = (item["output_batch_no"], item["output_item_no"], item["output_item_name"])
            if output_key not in output_set:
                output_set.add(output_key)
                output_list.append({
                    "output_batch_no": item["output_batch_no"],
                    "output_item_no": item["output_item_no"],
                    "output_item_name": item["output_item_name"],
                    "output_itemType": item["output_itemType"],
                    "output_validDate": item["output_validDate"],
                    "output_unit": item["output_unit"],
                    "output_count": item["output_count"],
                })

            # 處理 input (去重 batch_number + count)
            input_key = (item["batch_number"], item["count"])
            if input_key not in input_set:
                input_set.add(input_key)
                input_list.append({
                    "source": item["source"],
                    "itemCategory": item["itemCategory"],
                    "itemType": item["itemType"],
                    "item_no": item["item_no"],
                    "item_name": item["item_name"],
                    "batch_number": item["batch_number"],
                    "validDate": item["validDate"],
                    "count": item["count"],
                    "unit": item["unit"]
                })
        return input_list, output_list, n_oneProcess, n_secProcess