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
from package.mes.mes import *
from package.mes.batchnostock import *
from enum import IntEnum
from package.batchno.batchno import *
from package.bom.bom import *

class EProcessOrdeCategory():
    NONE = 0
    RECEIVED = 1            #領料
    RETURN = 2         #退料
    REMAINING = 3    # 餘料
    WASTE = 4            # 廢料
    PRODUCT = 5           # 產出物



class CCProcessOrder(object):
    TYPE_INPUT = 1
    TYPE_OUTPUT = 2
    TYPE_REUSE = 4
    TYPE_ALL = 7

    def __init__(self, str_timezone, str_no):
        self.__m_str_timezone = str_timezone
        self.__m_str_no = str_no
        self.__m_obj_work_order = self.__retrieve_work_order()
    def gen_process_order(self, n_type = TYPE_ALL):
        n_code = EErrorCode.ERROR_SUCCESS
        try:
            if  self.__m_obj_work_order:
                str_product_no = self.__m_obj_work_order.product_no
                #print(self.__m_obj_work_order.product_no, self.__m_obj_work_order.product_name,
                #      self.__m_obj_work_order.output_item_no, self.__m_obj_work_order.output_item_name)
                if n_type & self.TYPE_INPUT:
                    n_version = 1
                    lst_version = self.__get_product_ver(self.__m_obj_work_order.product_no)
                    if lst_version:
                        n_version = lst_version[-1]

                    lst_bom = CCBOMTree().retrieve(str_product_no, n_version, self.__m_obj_work_order.output_item_no)
                    _, lst_input = self.__gen_order_for_rr(lst_bom)
                if n_type & self.TYPE_REUSE:
                    self.__gen_order_for_rw()

                if n_type & self.TYPE_OUTPUT:
                    self.__gen_order_for_p()
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_code

    # 領料單/退料單 回傳投入物, 判斷產出物是否需要多個批號
    def __gen_order_for_rr(self, lst_bom):
        n_code = EErrorCode.ERROR_SUCCESS
        try:
            # 領料 計算投入物
            lst_input = []
            lst_data_r1 = []
            if lst_bom:
                lst_tmp = CMES(lst_bom).calculate(self.__m_obj_work_order.processUnit, self.__m_obj_work_order.processCount)
                if lst_tmp:
                    lst_input = CBatchNoStock(self.__m_str_timezone).retrieve(self.__m_obj_work_order.date, lst_tmp)
            if lst_input:
                # create process order
                lst_data_r1, lst_data_r2 = self.__gen_receive_return_data(lst_input)
                for dict_data in lst_data_r1:
                    # 建立單
                    str_order_no = self.__add_process_order(dict_data["no"], dict_data)
                    # serialno
                    self.__add_serialNo(str_order_no, dict_data)

                for dict_data in lst_data_r2:
                    # 建立單
                    str_order_no = self.__add_process_order(dict_data["no"], dict_data)
                    # serialno
                    self.__add_serialNo(str_order_no, dict_data, False)
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_code, lst_data_r1

    # 餘料單/廢料單
    def __gen_order_for_rw(self):
        n_code = EErrorCode.ERROR_SUCCESS
        try:
            lst_data_r, lst_data_w = self.__gen_remaining_waste_data()
            for dict_data in lst_data_r:
                # 建立單
                str_order_no = self.__add_process_order(dict_data["no"], dict_data)
                # 建立批號
                if str_order_no:
                    str_batchNo = self.__add_batchno(str_order_no, dict_data)
                    print("")

            for dict_data in lst_data_w:
                str_order_no = self.__add_process_order(dict_data["no"], dict_data)
                if str_order_no:
                    str_batchNo = self.__add_batchno(str_order_no, dict_data)
                    print("")

        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_code

    # 產出單
    def __gen_order_for_p(self):
        n_code = EErrorCode.ERROR_SUCCESS
        try:
            lst_data = self.__gen_product_data()
            for dict_data in lst_data:
                # 建立單
                str_order_no = self.__add_process_order(dict_data["no"], dict_data)
                # 建立批號
                if str_order_no:
                    str_batchNo = self.__add_batchno(str_order_no, dict_data)
                    print("")

        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_code

    def __gen_remaining_waste_data(self):
        lst_data_r = []
        lst_data_w = []

        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            lst_obj_result = (
                obj_session.query(CTableRWItems)
                .all()
            )
            str_no_prefix_r = ""
            str_no_prefix_w = ""
            n_index = 1
            for obj_result in lst_obj_result:
                # 餘料
                obj_inproduct = (
                    obj_session.query(CTableInproduct)
                    .filter(CTableInproduct.no == obj_result.item_no)
                    .first()
                )
                str_item_ref_no = None #obj_inproduct.customer_no if obj_inproduct else "",
                str_item_ref_displayName = ""#obj_inproduct.customer_displayName if obj_inproduct else "",
                dict_data ={ "no":"",
                             "creator_id": None,
                             "work_order_no": self.__m_str_no,
                             "date": self.__m_obj_work_order.date if self.__m_obj_work_order else 0,
                             "refProcess":self.__m_obj_work_order.oneProcess if self.__m_obj_work_order else 0,
                             "category": EProcessOrdeCategory.REMAINING,
                             "item_no": obj_result.item_no,
                             "item_name": obj_inproduct.name if obj_inproduct else "",
                             "item_ref_no": str_item_ref_no,
                             "item_ref_displayName": str_item_ref_displayName,
                             "itemCategory": EItemCategory.INPRODUCT,
                             "itemSubCategory": obj_inproduct.category if obj_inproduct else 0,
                             "unit": EUnit.KILOGRAM,
                             "count": 0,
                             "expectedCount": 0,
                             "comment":""
                           }
                if n_index == 1:
                    str_no_prefix_r = self.__gen_no(dict_data["category"], dict_data["work_order_no"])
                dict_data["no"] = f"{str_no_prefix_r}{n_index:02d}_{1}"#品項數_批號數
                lst_data_r.append(dict_data)

                # 廢料
                dict_data_w = deepcopy(dict_data)
                dict_data_w["category"] = EProcessOrdeCategory.WASTE
                if n_index == 1:
                    str_no_prefix_w = self.__gen_no(dict_data_w["category"], dict_data_w["work_order_no"])

                dict_data_w["no"] = f"{str_no_prefix_w}{n_index:02d}_{1}"  # 品項數_批號數
                lst_data_w.append(dict_data_w)
                n_index += 1

        return lst_data_r, lst_data_w

    def __gen_receive_return_data(self, lst_input):
        lst_data_receive = []
        lst_data_return = []

        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()

            str_no_prefix_receive = ""
            str_no_prefix_return = ""
            n_index = 1
            for dict_input in lst_input:
                # 領料 料品品項產商的資訊
                n_category, n_subCategory, str_item_name = self.__get_item_info(dict_input["item_no"])
                str_item_ref_no = None
                str_item_ref_displayName = ""
                dict_data = {"no": "",
                             "creator_id": None,
                             "work_order_no": self.__m_str_no,
                             "date": self.__m_obj_work_order.date if self.__m_obj_work_order else 0,
                             "refProcess": self.__m_obj_work_order.oneProcess if self.__m_obj_work_order else 0,
                             "category": EProcessOrdeCategory.RECEIVED,
                             "item_no": dict_input["item_no"],
                             "item_name": str_item_name,
                             "item_ref_no": str_item_ref_no,
                             "item_ref_displayName": str_item_ref_displayName,
                             "itemCategory": n_category,
                             "itemSubCategory": n_subCategory,
                             "unit": dict_input["unit"],
                             "count": 0,
                             "expectedCount": dict_input["value"],
                             "comment": "",
                             "batchNo": deepcopy(dict_input.get("batchNo", []))

                             }
                if n_index == 1:
                    str_no_prefix_receive = self.__gen_no(dict_data["category"], dict_data["work_order_no"])
                dict_data["no"] = f"{str_no_prefix_receive}{n_index:02d}_{1}"  # 品項數_批號數
                lst_data_receive.append(dict_data)

                # 退料
                dict_data_return = deepcopy(dict_data)
                dict_data_return["category"] = EProcessOrdeCategory.RETURN
                dict_data_return["expectedCount"] = 0
                if n_index == 1:
                    str_no_prefix_return = self.__gen_no(dict_data_return["category"], dict_data_return["work_order_no"])
                dict_data_return["no"] = f"{str_no_prefix_return}{n_index:02d}_{1}"  # 品項數_批號數
                lst_data_return.append(dict_data_return)
                n_index += 1
        return lst_data_receive, lst_data_return

    def __gen_product_data(self):
        lst_data = []

        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            str_no_prefix = ""
            n_index = 1
            # 多個批號?
            # 產品
            str_item_no = self.__m_obj_work_order.output_item_no if self.__m_obj_work_order else ""
            n_unit = self.__m_obj_work_order.processUnit if self.__m_obj_work_order else 0
            n_count = self.__m_obj_work_order.processCount
            n_category, n_subCategory, str_item_name = self.__get_item_info(str_item_no)
            str_item_ref_no = None
            str_item_ref_displayName = ""
            dict_data = {"no": "",
                         "creator_id": None,
                         "work_order_no": self.__m_str_no,
                         "date": self.__m_obj_work_order.date if self.__m_obj_work_order else 0,
                         "refProcess": self.__m_obj_work_order.oneProcess if self.__m_obj_work_order else 0,
                         "category": EProcessOrdeCategory.PRODUCT,
                         "item_no": str_item_no,
                         "item_name": str_item_name,
                         "item_ref_no": str_item_ref_no,
                         "item_ref_displayName": str_item_ref_displayName,
                         "itemCategory": n_category,
                         "itemSubCategory": n_subCategory,
                         "unit": n_unit,
                         "count": 0,
                         "expectedCount": n_count,
                         "comment": ""
                         }
            if n_index == 1:
                str_no_prefix = self.__gen_no(dict_data["category"], dict_data["work_order_no"])
            dict_data["no"] = f"{str_no_prefix}{n_index:02d}_{1}"  # 品項數_批號數
            lst_data.append(dict_data)
        return lst_data

    def __add_serialNo(self, str_order_no, dict_data, f_Received=True):
        try:
            with CDBMgr() as obj_dbmgr:
                for dict_batch in dict_data["batchNo"]:
                    if f_Received:
                        for dict_serial in dict_batch["serialNos"]:
                            new_data = CTableBatchNoSerialNo(
                                batch_number = dict_batch["batchNo"],
                                serialNo = dict_serial["serialNo"],
                                ref_order_no = str_order_no,
                                ref_order_no_category = EInventoryRefCategory.WORK,
                                time = self.__m_obj_work_order.date if self.__m_obj_work_order else 0, #???
                                unit = dict_data["unit"],
                                expectedCount= dict_serial["value"],
                                count = 0,
                                validDate = dict_batch["validDate"],
                                warehouse_no =  dict_batch["warehouse_no"],
                                updatedTime = util_retrieve_now_time()
                            )
                            if obj_dbmgr.insert(new_data) != EErrorCode.ERROR_SUCCESS:
                                str_message = 'failed to create process order'
                                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
                    else:
                        new_data = CTableBatchNoSerialNo(
                            batch_number=dict_batch["batchNo"],
                            serialNo="",
                            ref_order_no=str_order_no,
                            ref_order_no_category=EInventoryRefCategory.WORK,
                            time=self.__m_obj_work_order.date if self.__m_obj_work_order else 0,  # ???
                            unit=dict_data["unit"],
                            count=0,
                            expectedCount=0,
                            validDate=dict_batch["validDate"],
                            warehouse_no=dict_batch["warehouse_no"],
                            updatedTime=util_retrieve_now_time()
                        )
                        if obj_dbmgr.insert(new_data) != EErrorCode.ERROR_SUCCESS:
                            str_message = 'failed to create process order'
                            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))


    def __add_process_order(self, str_no, dict_data):
        try:
            str_id = ''
            with CDBMgr() as obj_dbmgr:
                new_data = CTableProcessOrder(
                    no=str_no,
                    creator_no=dict_data["creator_id"],
                    work_order_no=dict_data["work_order_no"],
                    refProcess=dict_data["refProcess"],
                    date=dict_data["date"],
                    category=dict_data["category"],
                    item_no=dict_data["item_no"],
                    item_name=dict_data["item_name"],
                    item_ref_no=dict_data["item_ref_no"],
                    item_ref_displayName=dict_data["item_ref_displayName"],
                    itemCategory=dict_data["itemCategory"],
                    itemSubCategory = dict_data["itemSubCategory"],

                    unit=dict_data["unit"],
                    count=dict_data["count"],
                    expectedCount=dict_data["expectedCount"],
                    comment=dict_data["comment"],
                    creationTime=util_retrieve_now_time()
                )
                if obj_dbmgr.insert(new_data) == EErrorCode.ERROR_SUCCESS:
                    str_id = str_no
                else:
                    str_message = 'failed to create process order'
                    CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return str_id

    def __add_batchno(self, str_order_no, dict_data):
        n_itemType = EItemType.NONE

        if dict_data["category"] == EProcessOrdeCategory.REMAINING:
            n_itemType = EItemType.REMAINING
        if dict_data["category"] == EProcessOrdeCategory.WASTE:
            n_itemType = EItemType.WASTE
        if dict_data["category"] == EProcessOrdeCategory.PRODUCT:
            n_itemType = EItemType.NEW
        n_refCategory = get_order_type(str_order_no)
        dict_batch_no = {
                            "date": dict_data["date"],
                            "creator_id": dict_data["creator_id"],
                            "ref_no": str_order_no,
                            "refCategory": n_refCategory,
                            "category": EBatchNoCategory.WORK,
                            "item_no": dict_data["item_no"],
                            "item_name": dict_data["item_name"],
                            "item_ref_no": dict_data["item_ref_no"],
                            "item_ref_displayName": dict_data["item_ref_displayName"],
                            "itemCategory": dict_data["itemCategory"],
                            "itemType": n_itemType,
                            "unit": dict_data["unit"],
                            "expectedCount": dict_data["expectedCount"],
                            "checkedCount": 0,
                            "validDate": 0,
                            "validDateNo": "",
                            "comment": ""
                        }
        str_batchNo = CCBatchNumber().add(dict_batch_no)
        return str_batchNo

    def __update_batchno_for_order(self, str_order_no, str_batchNo):
        n_code = EErrorCode.ERROR_SUCCESS
        with CDBMgr() as obj_dbmgr:
            if obj_dbmgr.update(CTableProcessOrder, [CTableProcessOrder.no == str_order_no],
                                         {"batch_numebr": str_batchNo}) != EErrorCode.ERROR_SUCCESS:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'failed to update batchnumber'
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
        return n_code
    def __retrieve_work_order(self):
        obj_result = None
        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                obj_result = (
                    obj_session.query(CTableWorkOrder)
                    .filter(CTableWorkOrder.no == self.__m_str_no)
                    .first()
                )
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return obj_result

    def __gen_no(self, n_category, str_work_no):
        str_temp = ""
        if str_work_no:
            str_temp = str_work_no[-8:] #派工編號後8碼
        str_no = "ZP%d%s" %(n_category, str_temp)
        return str_no

    def __gen_no2(self, n_category, n_date):
        str_date = datetime.fromtimestamp(n_date).strftime('%y%m%d')
        str_no = "ZP%d%s" %(n_category, str_date) + util_random_code(2)
        return str_no



    def __get_product_ver(self, str_product_no):
        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            lst_version = (
                obj_session.query(
                    CTableProductSpec.product_version
                )
                .filter(
                    CTableProductSpec.product_no == str_product_no
                )
                .all()
            )

            if not lst_version:
                str_no = str_product_no + '_1'
                lst_version = (
                    obj_session.query(
                        CTableProductSpec.product_version
                    )
                    .filter(
                        CTableProductSpec.product_no == str_no
                    )
                    .all()
                )
            lst_version = sorted(set(version[0] for version in lst_version), reverse=True)
        return lst_version

    def __get_item_info(self, str_item_no):
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
                n_subCategory = obj_prodcut.category
                str_item_name = obj_prodcut.name
            else:
                obj_inprodcut = (
                    obj_session.query(CTableInproduct)
                    .filter(CTableInproduct.no == str_item_no)
                    .first()
                )
                if obj_inprodcut:
                    n_category = EItemCategory.INPRODUCT
                    n_subCategory = obj_inprodcut.category
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