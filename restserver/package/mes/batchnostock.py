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
from package.statistic.inventoryStatistic import *


class CBatchNoStock():
    def __init__(self, str_timezone):
      self.__m_str_timezone = str_timezone

    def retrieve(self, n_date, lst_items):
        lst_data = []
        n_code =  EErrorCode.ERROR_SUCCESS
        try:
            # 取得實際庫存 & 批號序號
            # 扣除預先分配
            for dict_item in lst_items:
                print("CBatchNoStock", dict_item.get("item_no", 0))
                dict_item["batchNo"] = []
                str_item_no = dict_item.get("item_no", 0)#"PMA0001004""PMB0019002"
                n_category = self.__get_item_category(str_item_no)
                n_stock_date = util_retrieve_now_time()
                print("CBatchNoStock", str_item_no, n_category)
                lst_stock = CInventoryItemMonth(self.__m_str_timezone).retrieve_realTime(n_stock_date, n_category, str_item_no)
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    if lst_stock:
                        lst_serialNos = self.__get_batchno_from_order(obj_session, n_date, str_item_no)
                        for dict_stock in lst_stock:
                            for dict_batchno in dict_stock.get("batchNo", []):
                                str_batchNo = dict_batchno.get("specified_no", "")
                                str_warehouse_no = dict_batchno.get("warehouse_no", "")
                                n_validDate = self.__get_validDate(obj_session, str_batchNo)
                                dict_batchno["validDate"] = n_validDate
                                dict_batchno["serialNos"] = self.__get_serialNos(obj_session, str_batchNo, str_warehouse_no)

                        if lst_serialNos:
                            self.__deduct_values_from_stock(lst_stock, lst_serialNos)
                        n_code, lst_result = self.__allocate_from_stock(dict_item, lst_stock, str_warehouse_no="WH4250218PDL")
                        dict_item["batchNo"] = deepcopy(lst_result)
                    lst_data.append(deepcopy(dict_item))
                    print("")
                print("")
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_data


    def __allocate_from_stock(self, dict_required, lst_stock, str_warehouse_no):
        from collections import defaultdict
        lst_result = []
        n_code = EErrorCode.ERROR_SUCCESS
        n_value = dict_required["value"]

        # 過濾指定倉庫的庫存
        dict_inventory = next(
            (inv for inv in lst_stock if inv["warehouse_no"] == str_warehouse_no), None
        )

        if not dict_inventory:
            n_code = EErrorCode.ERROR_WAREHOUSE_NOT_FOUND
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] Not found (warehouse_no: %s)'
                          % (self.__class__.__name__, str_warehouse_no))
        else:
            # 排序批號（依效期升冪）
            sorted_batches = sorted(
                dict_inventory.get("batchNo", []),
                key=lambda x: datetime.fromtimestamp(x.get("validDate", 9999999999))
            )
            for batch in sorted_batches:
                str_batch_no = batch["specified_no"]
                str_warehouse_no = batch["warehouse_no"]
                n_valid_date = batch.get("validDate", 0)

                serial_nos = []

                for serial in batch.get("serialNos", []):
                    str_serial_no = serial["serialNo"]
                    available_value = serial["value"]

                    if available_value <= 0 or n_value <= 0:
                        continue

                    used_value = min(n_value, available_value)
                    serial_nos.append({
                        "serialNo": str_serial_no,
                        "value": round(used_value, 2)
                    })
                    n_value -= used_value

                if serial_nos:
                    lst_result.append({
                        "batchNo": str_batch_no,
                        "validDate": n_valid_date,
                        "warehouse_no":str_warehouse_no,
                        "serialNos": serial_nos
                    })

                if n_value <= 0:
                    break

            if n_value > 0:
                n_code = EErrorCode.ERROR_STOCK_NOT_ENOUGH
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] Insufficient inventory: %s still need (%f)'
                              % (self.__class__.__name__, dict_required["item_name"], n_value))
        return n_code, lst_result

    def __get_validDate(self, obj_session, str_batchNo):
        n_validDate = 0
        if str_batchNo:
            obj_reuslt = (
                obj_session.query(CTableBatchNumber.validDate)
                .filter(CTableBatchNumber.no == str_batchNo)
                .first()
            )
            n_validDate = obj_reuslt.validDate if obj_reuslt else 0
        return n_validDate

    def __get_serialNos(self, obj_session, str_batchNo, str_warehouse_no):
        lst_data = []
        lst_reuslt = (
            obj_session.query(
                CTableInventoryRec.serialNo,
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
            .filter(CTableInventoryRec.warehouse_no == str_warehouse_no,
                    CTableInventoryRec.batchNumber == str_batchNo)
            .group_by(
                CTableInventoryRec.serialNo
            )
            .all()
        )
        for obj_result in lst_reuslt:
            lst_data.append({"serialNo": obj_result.serialNo,
                             "value": obj_result.remaining})
        return lst_data


    def __get_batchno_from_order(self, obj_session, n_date, str_item_no):
        lst_data = []
        nos_query = (
            obj_session.query(
                CTableProcessOrder.no
            )
            .filter( CTableProcessOrder.date >= n_date,
                    CTableProcessOrder.item_no == str_item_no,
                    CTableProcessOrder.category == EProcessOrderCategory.RECEIVE,
                    CTableProcessOrder.count == 0)
        )

        lst_no = [no[0] for no in nos_query.all()]
        lst_result = (
            obj_session.query(
                CTableBatchNoSerialNo
            )
            .filter(CTableBatchNoSerialNo.ref_order_no.in_(lst_no))
            .all()

        )
        for obj_result in lst_result:
            lst_data.append({"batchNo": obj_result.batch_number,
                             "warehouse_no": obj_result.warehouse_no,
                             "serialNo": obj_result.serialNo,
                             "value": obj_result.count
                             })
        return lst_data

    def __deduct_values_from_stock(self, inventory_a, deduction_b):
        # 建立扣除查找表：依 batchNo, serialNo, warehouse_no 建索引
        deduction_map = {}
        for item in deduction_b:
            key = (item["batchNo"], item["serialNo"], item["warehouse_no"])
            deduction_map[key] = item["value"]

        # 處理 A：逐一批號與序號做扣減
        for item in inventory_a:
            for batch in item.get("batchNo", []):
                batch_no = batch.get("specified_no")
                warehouse_no = batch.get("warehouse_no")

                for serial in batch.get("serialNos", []):
                    serialNo = serial["serialNo"]
                    key = (batch_no, serialNo, warehouse_no)

                    if key in deduction_map:
                        deduct_value = deduction_map[key]
                        original_value = serial["value"]
                        serial["value"] = max(0, original_value - deduct_value)  # 防止負數
        return inventory_a

    def __get_item_category(self, str_item_no):
        n_category = 0
        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            obj_prodcut = (
                obj_session.query(CTableProduct)
                .filter(CTableProduct.no == str_item_no)
                .first()
            )
            if obj_prodcut:
                n_category = EItemCategory.PRODUCT
            else:
                obj_inprodcut = (
                    obj_session.query(CTableInproduct)
                    .filter(CTableInproduct.no == str_item_no)
                    .first()
                )
                if obj_inprodcut:
                    n_category = EItemCategory.INPRODUCT
                else:
                    obj_material = (
                        obj_session.query(CTableMaterial)
                        .filter(CTableMaterial.no == str_item_no)
                        .first()
                    )
                    if obj_material:
                        n_category = obj_material.category
        return n_category