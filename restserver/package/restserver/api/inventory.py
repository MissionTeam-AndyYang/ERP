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
from sqlalchemy.orm import selectinload
import uuid
from package.util.util import *
from package.price.price import *
from package.inventory.inventory import *
from package.statistic.inventoryStatistic import *

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


class CPrice(CPrivilegeControl):

    TYPE_LIST_PRICE = 1 # 定價
    TYPE_CURRENT_PRICE = 1  # 時價

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'results': []}
        if not request.args.get("type"):
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'invalid parameter'
        else:
            try:
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    n_type = request.args.get('type', 0, type=int)
                    # 1. 統一基礎查詢
                    obj_query = (
                        obj_session.query(CTableItemPrice)
                        # .filter(*lst_where)  # 加入你的篩選條件
                        .options(
                            selectinload(CTableItemPrice.trans_items).selectinload(CTableTransItems.contracts),
                            selectinload(CTableItemPrice.material),
                            selectinload(CTableItemPrice.inproduct),
                            selectinload(CTableItemPrice.product),
                            selectinload(CTableItemPrice.goods)
                        )
                        .order_by(CTableItemPrice.itemCategory.asc(), CTableItemPrice.creationTime.desc())
                    )

                    # 2. 計算總數
                    dict_extra_data['total'] = obj_session.query(CTableItemPrice).count()

                    # 3. 處理分頁參數與執行查詢
                    n_start = request.args.get('start', 0, type=int)
                    n_count = request.args.get('count', 0, type=int)

                    if n_count > 0:
                        obj_query = obj_query.offset(n_start).limit(n_count)

                    lst_obj_result = obj_query.all()

                    lst_result = []
                    for obj_price in lst_obj_result:
                        n_subCategory = None

                        # 根據類別決定取哪個屬性
                        if obj_price.itemCategory in [EItemCategory.PM, EItemCategory.MA, EItemCategory.AF]:
                            n_subCategory = obj_price.material.subCategory if obj_price.material else 0
                        elif obj_price.itemCategory == EItemCategory.INPRODUCT:
                            n_subCategory = obj_price.inproduct.category if obj_price.inproduct else 0
                        elif obj_price.itemCategory == EItemCategory.PRODUCT:
                            n_subCategory = obj_price.product.category if obj_price.product else 0
                        elif obj_price.itemCategory == EItemCategory.GOODS:
                            n_subCategory = obj_price.goods.category if obj_price.goods else 0
                        if n_type == self.TYPE_LIST_PRICE: # 定價
                            dict_data = {
                                "no": obj_price.no,
                                "month": obj_price.date.strftime("%Y/%m"),
                                "unit": obj_price.whUnitWeight,
                                "price": obj_price.estWHPriceWeight,
                                "item_no": obj_price.item_no,
                                "item_name": obj_price.item_name,
                                "itemCategory": obj_price.itemCategory,
                                "itemSubCategory": n_subCategory,
                            }
                            lst_result.append(dict_data)
                        else:
                            dict_data = {
                                "no": obj_price.no,
                                "month": obj_price.date.strftime("%Y/%m"),
                                "unit": obj_price.whUnitWeight,
                                "price": obj_price.whPriceWeight,
                                "item_no": obj_price.item_no,
                                "item_name": obj_price.item_name,
                                "itemCategory": obj_price.itemCategory,
                                "itemSubCategory": n_subCategory,
                                "contract": {}
                            }
                            if not obj_price.trans_items:
                                lst_result.append(dict_data)
                                continue  # 如果沒有，就跳到下一筆 Price

                            for obj_trans in obj_price.trans_items:
                                # 判斷有沒有 Contracts
                                if not obj_trans.contracts:
                                    lst_result.append(dict_data)
                                    continue

                                for obj_contract in obj_trans.contracts:
                                    # 都要建立一個全新的 dict (使用 copy)
                                    new_dict_data = dict_data.copy()
                                    new_dict_data["contract"] = {
                                        "contract": {
                                            "displayName": obj_contract.displayName if obj_contract else"",
                                            "category": obj_contract.category if obj_contract else 0,
                                            "type": obj_contract.type if obj_contract else 0,
                                            "itemStyle": obj_contract.itemStyle if obj_contract else 0,
                                            "unit": obj_contract.unit if obj_contract else 0,
                                            "price": obj_contract.price if obj_contract else 0,
                                            "comment": obj_contract.type if obj_contract else "",
                                        }
                                    }
                                    lst_result.append(new_dict_data)
                    dict_extra_data['results'] = lst_result
                    dict_extra_data['count'] = len(lst_result)
            except Exception as error:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'throw exception (error: %s)' % str(error)
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                              % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data


class CItems(CPrivilegeControl):
    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total':0, 'results': {}}

        try:
            n_itemCategoty = 0
            if request.args.get('type'):
                # type = 1 品項; type = 2 批號
                n_type = int(request.args.get('type'))
            if request.args.get('itemCategory'):
                n_itemCategoty = int(request.args.get('itemCategory'))

            if request.args.get('start_time') and request.args.get('end_time'):
                # get the range of timestamp
                n_start = int(request.args.get('start_time'))
                n_end = int(request.args.get('end_time'))
                # 庫存
                if request.args.get('commit'):
                    if n_type == 2:
                        CInventoryDeltaBatchNo(str_timezone).calculate(n_start, n_end, True)
                    else:
                        CInventoryDeltaItem(str_timezone).calculate(n_start, n_end, True)
                    #obj_delta  = CInventoryDeltaItem(str_timezone)
                    #obj_delta.setParam("",1)
                    #obj_delta.calculate(n_start, n_end, True)


                    #CInventoryDeltaItem(str_timezone).calculate(n_start, n_end, True, True)
                    #CInventoryItemMonth(str_timezone).calculate(n_type, n_itemCategoty, n_start, n_end, True)
                    # n_itemCategoty 原/物/膠/在製品/製成品
                    CInventoryItemMonth(str_timezone).calculate(n_type, 1, n_start, n_end, True)
                    CInventoryItemMonth(str_timezone).calculate(n_type, 2, n_start, n_end, True)
                    CInventoryItemMonth(str_timezone).calculate(n_type, 3, n_start, n_end, True)
                    CInventoryItemMonth(str_timezone).calculate(n_type, 4, n_start, n_end, True)
                    CInventoryItemMonth(str_timezone).calculate(n_type, 5, n_start, n_end, True)

            if request.args.get('date') and n_type:
                # UI取得至當日的庫存
                n_date = int(request.args.get('date'))
                str_item_no = request.args.get('item_no', '')

                lst_result = CInventoryItemMonth(str_timezone).retrieve_realTime(n_date, n_itemCategoty, str_item_no)
                dict_extra_data['total'] = len(lst_result)
                dict_extra_data['results'] = lst_result
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data


class CInventory(CPrivilegeControl):
    TYPE_BATCHNO = 1 # 批號為視角
    TYPE_RAW = 2     # RAW Data
    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0,'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                n_total = (obj_session.query(CTableInventoryRec)
                           .filter(*lst_where)
                           .group_by(CTableInventoryRec.group)
                           .count())
                n_start = 0
                n_count = 0
                if request.args.get('start') and request.args.get('count'):
                    n_start = int(request.args.get('start'))
                    n_count = int(request.args.get('count'))

                if n_count:
                    obj_subquery = (
                        obj_session.query(CTableInventoryRec.group)
                        .filter(*lst_where)
                        .group_by(CTableInventoryRec.group)
                        .order_by(CTableInventoryRec.date.desc())
                        .offset(n_start)
                        .limit(n_count)
                        .subquery()
                    )
                else:
                    obj_subquery = (
                        obj_session.query(CTableInventoryRec.group)
                        .filter(*lst_where)
                        .group_by(CTableInventoryRec.group)
                        .order_by(CTableInventoryRec.date.desc())
                        .subquery()
                    )
                lst_tmp = (
                    obj_session.query(CTableInventoryRec)
                    .filter(*lst_where)
                    .filter(CTableInventoryRec.group.in_(select(obj_subquery)))
                    .order_by(CTableInventoryRec.date.desc())
                    .all()
                )

                if lst_tmp:
                    lst_result = self.__gen_data(obj_session, lst_tmp)
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

    def __gen_data(self, obj_session, lst_tmp):
        lst_result = []
        if request.args.get('type') and int(request.args.get('type')) == self.TYPE_BATCHNO:
            from collections import defaultdict
            dict_group_data = defaultdict(lambda: {
                "group":"",
                "date": 0,
                "creator_no":"",
                "ref_no":"",
                "refCategory":0,
                "category": 0,
                "source": 0,
                "batchNumber": "",
                "serialNo":"",
                "unit": 0,
                "validDate": 0,
                "checkedCount": 0,
                "item_no": "",
                "item_name": "",
                "item_ref_no": "",
                "item_ref_displayName": "",
                "itemCategory": 0,
                "itemType": 0,
                "comment": "",
                "warehouse": []
            })

            for obj_row in lst_tmp:
                str_group_key = obj_row.group
                if not dict_group_data[str_group_key]["date"]:
                    n_category, n_subCategory, str_item_name= get_item_info(obj_row.item_no)
                    obj_batch = (
                        obj_session.query(CTableBatchNumber)
                        .filter(CTableBatchNumber.no == obj_row.batchNumber )
                        .first()
                    )
                    str_ref_no = obj_row.ref_no
                    if obj_row.refCategory == EInventoryRefCategory.WORK:
                        obj_process = (
                            obj_session.query(CTableProcessOrder)
                            .filter(CTableProcessOrder.no == obj_row.ref_no)
                            .first()
                        )
                        if obj_process:
                            str_ref_no = obj_process.work_order_no
                    dict_group_data[str_group_key].update({
                        "group": obj_row.group,
                        "date": obj_row.date,
                        "creator_no": obj_row.creator_no,
                        "ref_no": str_ref_no,
                        "refCategory": obj_row.refCategory,
                        "category": obj_row.category,
                        "source": obj_row.source,
                        "batchNumber": obj_row.batchNumber,
                        "serialNo": obj_row.serialNo,
                        "unit": obj_batch.unit if obj_batch else 0,
                        "validDate": obj_batch.validDate if obj_batch else 0,
                        "checkedCount": obj_batch.checkedCount if obj_batch else 0,
                        "item_no": obj_row.item_no,
                        "item_name": obj_row.item_name,
                        "item_ref_no": obj_row.item_ref_no,
                        "item_ref_displayName": obj_row.item_ref_displayName,
                        "itemType": obj_row.itemType,
                        "itemCategory": obj_row.itemCategory,
                        "itemSubCategory": n_subCategory
                    })
                    retrieve_warehouse_info(obj_session, dict_group_data[str_group_key]["itemCategory"], obj_batch, dict_group_data[str_group_key])

                obj_result = (
                            obj_session.query(
                                func.sum(
                                    case(
                                        (CTableInventoryRec.category == EInventoryCategory.IN, CTableInventoryRec.count),  # 入庫
                                        (CTableInventoryRec.category == EInventoryCategory.OUT, -CTableInventoryRec.count)  # 出庫
                                    )
                                ).label("remaining_count")
                            )
                            .filter(CTableInventoryRec.batchNumber == obj_row.batchNumber,
                                    CTableInventoryRec.warehouse_no == obj_row.warehouse_no)
                            .first()
                        )
                dict_group_data[str_group_key]["warehouse"].append({
                    "recId": obj_row.id,
                    "warehouse_no": obj_row.warehouse_no,
                    "warehouse_displayName": obj_row.warehouse_displayName,
                    "unit": obj_row.unit,
                    "count": obj_row.count,
                    "inventory_count": obj_result.remaining_count if obj_result else 0
                })
                dict_group_data[str_group_key]["warehouse"] = sorted(dict_group_data[str_group_key]["warehouse"], key=lambda x: x['warehouse_no'])
                lst_result = list(dict_group_data.values())
        else:
            for obj_row in lst_tmp:
                dict_row = object_as_dict(obj_row)
                lst_result.append(dict_row)

        return lst_result


    def __fill_query_params(self):
        lst_where = []
        if request.args.get('item_ref_no'):
            lst_where.append(CTableInventoryRec.item_ref_no == request.args.get('item_ref_no'))
        if request.args.get('item_no'):
            lst_where.append(CTableInventoryRec.item_no == request.args.get('item_no'))

        if request.args.get('batchNumber'):
            lst_where.append(CTableInventoryRec.batchNumber == request.args.get('batchNumber'))
        if request.args.get('category'):
            lst_where.append(CTableInventoryRec.category == int(request.args.get('category')))
        return lst_where


class CMonthAmount(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total':0, 'results': {}}

        try:
            if request.args.get('start_time') and request.args.get('end_time'):
                # get the range of timestamp
                n_start = int(request.args.get('start_time'))
                n_end = int(request.args.get('end_time'))
                #CInventoryMonth(str_timezone).calculate(1756656000, 1759161600, True)

                lst_result = CInventoryMonth(str_timezone).retrieve(n_start, n_end)
                dict_extra_data['total'] = len(lst_result)
                dict_extra_data['results'] = lst_result
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data


class CStatistics(CPrivilegeControl):
    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'results': {}}
        if not request.args.get("batchNumber"):
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'invalid parameter'
        else:
            try:
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    lst_obj_result = (
                        obj_session.query(
                            CTableInventoryRec.item_no,
                            CTableInventoryRec.item_name,
                            CTableInventoryRec.item_ref_no,
                            CTableInventoryRec.item_ref_displayName,
                            CTableInventoryRec.itemType,
                            CTableInventoryRec.itemCategory,
                            CTableInventoryRec.warehouse_no,
                            CTableInventoryRec.warehouse_displayName,
                            CTableInventoryRec.unit,
                            func.sum(
                                case(
                                    (CTableInventoryRec.category == EInventoryCategory.IN, CTableInventoryRec.count),  # 入庫
                                    (CTableInventoryRec.category == EInventoryCategory.OUT, -CTableInventoryRec.count)  # 出庫
                                )
                            ).label("remaining_count")
                        )
                        .filter(CTableInventoryRec.batchNumber == request.args.get("batchNumber"))
                        .group_by(CTableInventoryRec.warehouse_no)
                        .all()
                    )

                    dict_extra_data['results'] = {"warehouse":[]}
                    for item_no,item_name, item_ref_no, item_ref_displayName, itemType, itemCategory, warehouse_no, warehouse_displayName, unit, remaining_count in lst_obj_result:
                        dict_extra_data['results']["item_no"] = item_no
                        dict_extra_data['results']["item_name"] = item_name
                        dict_extra_data['results']["item_ref_no"] = item_ref_no
                        dict_extra_data['results']["item_ref_displayName"] = item_ref_displayName
                        dict_extra_data['results']["itemType"] = itemType
                        dict_extra_data['results']["itemCategory"] = itemCategory
                        dict_extra_data['results']["warehouse"].append({"warehouse_no": warehouse_no,
                                                                       "warehouse_displayName": warehouse_displayName,
                                                                       "unit": unit,
                                                                       "count": remaining_count})

            except Exception as error:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'throw exception (error: %s)' % str(error)
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                              % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data


