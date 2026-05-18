# coding=utf8
import pytz
import string
from copy import deepcopy
from package.util.util import *
from package.log.log import CLogger
from package.dbwrapper.dbmgr import CDBMgr
import uuid
from package.restserver.api.util import *
from .common import *
from package.price.price import *
from package.inventory.inventory import *

class CBSNoSubject(object):

    lst_observers = []

    def add(self, dict_data):
        n_code =  EErrorCode.ERROR_SUCCESS
        try:
            if dict_data.get("batchno", ""):
                f_total = 0
                dict_tmp = deepcopy(dict_data)
                n_BSType = dict_tmp["bsType"]
                n_refno_subCategory = dict_tmp["ref_no_subCategory"]
                lst_data = dict_tmp["serialNos"]

                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    str_batch_item_no = ""
                    obj_batch = self.__get_batch_no(obj_session, dict_tmp["batchno"])
                    if obj_batch:
                        str_batch_item_no = obj_batch.item_no
                        dict_tmp["ref_no_sub"] = self.__convent_ref_no_sub(obj_batch,  dict_tmp["ref_no_sub"])

                    str_item_no = self.__get_order_item_no(obj_session, dict_tmp["ref_no"], dict_tmp["ref_no_category"], dict_tmp["ref_no_sub"])
                    if str_batch_item_no and str_item_no and str_batch_item_no == str_item_no:
                        for dict_serialNo in lst_data:
                            if dict_serialNo["isValid"]:
                                f_total += dict_serialNo["value"]
                                # 進貨.銷貨退回.其他?, 新增 批號序號表
                                # 領.退.餘.廢.產, 新增製造數據
                                if n_BSType in [EBSType.PURCHASE_IN_S, EBSType.PRODUCT_RETURN_IN_S, EBSType.PRODUCT_IN_S, EBSType.SALE_IN_S, EBSType.OTHER_IN_S]:
                                    # 入庫
                                    # 1.新增入庫紀錄
                                    self.__gen_inventory(obj_batch, EInventoryCategory.IN, dict_tmp, dict_serialNo)
                                    if n_BSType in [EBSType.PURCHASE_IN_S, EBSType.SALE_IN_S]:
                                        #2. 新增 批號+序號 進貨單
                                        self.__add_batchNo_serialNo(obj_dbmgr, obj_batch, dict_tmp, dict_serialNo)
                                elif n_BSType in [EBSType.PURCHASE_OUT_S, EBSType.PRODUCT_OUT_S, EBSType.SALE_OUT_S, EBSType.OTHER_OUT_S]:
                                    #出庫
                                    # 1.新增出庫紀錄
                                    self.__gen_inventory(obj_batch, EInventoryCategory.OUT, dict_tmp, dict_serialNo)
                                else:
                                    #產間
                                    # 1.新增製造數據
                                    str_data_id = self.__add_productiondata(obj_dbmgr,  dict_tmp, dict_serialNo)
                                    if n_BSType == EBSType.PRODUCT_OUT_P:
                                        #餘廢產
                                        # 新增 批號+序號 ,
                                        self.__add_batchNo_serialNo(obj_dbmgr, obj_batch, dict_tmp, dict_serialNo)
                                        if n_refno_subCategory == EProcessOrderCategory.REMAIN:
                                            self.__add_productiondata_reuse(obj_dbmgr, str_data_id, dict_tmp, dict_serialNo)
                                        if n_refno_subCategory == EProcessOrderCategory.WASTE:
                                            self.__add_productiondata_reuse(obj_dbmgr, str_data_id, dict_tmp, dict_serialNo)
                                        if n_refno_subCategory == EProcessOrderCategory.PRODUCT:
                                            self.__add_productiondata_output(obj_dbmgr, str_data_id, dict_tmp, dict_serialNo)
                                    elif n_BSType in [EBSType.PRODUCT_IN_P, EBSType.PRODUCT_RETURN_OUT_P]:
                                        # 領/退料
                                        self.__add_productiondata_input(obj_dbmgr, str_data_id, dict_tmp, dict_serialNo)
                            else:
                                pass #不相符的資料
                        # 通知註冊函式 , 更新批號/訂單檢定數量
                        dict_param = {
                            "bsType": n_BSType,
                            "ref_no": dict_tmp["ref_no"],
                            "ref_no_category": dict_tmp["ref_no_category"],
                            "ref_no_sub": dict_tmp["ref_no_sub"],
                            "refno_subCategory": n_refno_subCategory,
                            "batchno": dict_tmp["batchno"],
                            "total": round(f_total, 2)
                        }
                        self.__notify_observers(dict_param)
                    else:
                        CLogger().log(CLogger.LOG_LEVELWARNING, '[%s] item_no is not matched. (refNo: %s, batchNo: %s)'
                                      % (self.__class__.__name__, str_batch_item_no, str_item_no))
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_code

    @classmethod
    def register_observer(cls, func):
        """註冊外部 observer 函式"""
        if callable(func) and func not in cls.lst_observers:
            cls.lst_observers.append(func)

    @classmethod
    def unregister_observer(cls, func):
        """取消註冊 observer"""
        if func in cls.lst_observers:
            cls.lst_observers.remove(func)

    def __notify_observers(self, dict_param):
        """呼叫所有註冊的 observer 函式"""
        for observerFun in self.lst_observers:
            observerFun(dict_param)  # 傳入自己作為參數.


    def __gen_inventory(self, obj_batch, n_category, dict_data, dict_serialNo):
        n_BSType = dict_data["bsType"]
        #n_date = dict_data["date"]
        n_date = dict_serialNo["devDateTimestamp"]
        str_ref_no = dict_data["ref_no"]
        n_refno_category = dict_data["ref_no_category"]

        str_ref_no_sub = dict_data["ref_no_sub"]
        n_refno_subCategory = dict_data["ref_no_subCategory"]
        str_batchno = dict_data["batchno"]
        str_comment = dict_data["comment"]

        # 產製入庫-->多個 子訂單
        str_group = str(uuid.uuid4()).replace("-", "")
        f_count = dict_serialNo["value"]

        if obj_batch:
            n_unit, f_price = CPrice().get(obj_batch.item_no, obj_batch.itemCategory)
            dict_inventory = {
                "creator_id": "",
                "group": str_group,
                "ref_no": str_ref_no_sub if(n_refno_category == EDevRefCategory.WORK) else str_ref_no,
                "ref_category": n_refno_category,
                "warehouse_no": "WH4250218PDL",
                "warehouse_displayName": "恆旺_台中",
                "date": n_date,
                "category": n_category,  # 出入庫
                "source": self.__get_inventory_src(n_BSType),  # 緣由
                "batchNumber": str_batchno,
                "serialNo": dict_serialNo["serialNo"],
                "item_no": obj_batch.item_no if obj_batch else "",
                "item_name": obj_batch.item_name if obj_batch else "",
                "item_ref_no": obj_batch.item_ref_no if obj_batch else "",
                "item_ref_displayName": obj_batch.item_ref_displayName if obj_batch else "",
                "itemCategory": obj_batch.itemCategory if obj_batch else 0,
                "itemType": obj_batch.itemType if obj_batch else 0,
                "unit": obj_batch.unit, # 待確認
                "price": f_price,
                "count": f_count,
                "amount": round(f_count * f_price, 0),
                "comment": str_comment
            }
            CCInventroyRec().add(str_group, dict_inventory)

    def __get_inventory_src(self, n_BSType):
        n_src = 0
        if n_BSType == EBSType.PURCHASE_IN_S:
            n_src = EInventorySrc.PURCHASE_RECEIVE

        if n_BSType == EBSType.PRODUCT_IN_S:
            n_src = EInventorySrc.PRODUCT

        if n_BSType == EBSType.PRODUCT_RETURN_IN_S:
            n_src = EInventorySrc.RETURN_SALE

        if n_BSType == EBSType.SALE_IN_S:
            n_src = EInventorySrc.SRETURN

        if n_BSType == EBSType.OTHER_IN_S:# 其他入庫 ?
            n_src = EInventorySrc.PURCHASE_RECEIVE

        if n_BSType == EBSType.PURCHASE_OUT_S:
            n_src = EInventorySrc.REMAINING_PRETURN

        if n_BSType == EBSType.PRODUCT_OUT_S:
            n_src = EInventorySrc.PURCHASE_RECEIVE

        if n_BSType == EBSType.SALE_OUT_S:
            n_src = EInventorySrc.RETURN_SALE
        if n_BSType == EBSType.OTHER_OUT_S: # 其他出庫 ?
            n_src = EInventorySrc.PURCHASE_RECEIVE
        return n_src

    def __add_batchNo_serialNo(self, obj_dbmgr, obj_batch, dict_data, dict_serialNo):
        #n_date = dict_data["date"]
        n_date = dict_serialNo["devDateTimestamp"]
        str_ref_no = dict_data["ref_no"]
        n_refno_category = dict_data["ref_no_category"]
        str_ref_no_sub = dict_data["ref_no_sub"]
        n_refno_subCategory = dict_data["ref_no_subCategory"]
        str_batchno = dict_data["batchno"]

        new_data = CTableBatchNoSerialNo(
            serialNo=dict_serialNo["serialNo"],
            batch_number=str_batchno,
            ref_order_no=str_ref_no,
            ref_order_no_category = n_refno_category,
            time= n_date,
            unit = obj_batch.unit if obj_batch else 0,
            count=dict_serialNo["value"],
            validDate=obj_batch.validDate,
            warehouse_no = "",
            updatedTime=util_retrieve_now_time()
        )
        if obj_dbmgr.insert(new_data) != EErrorCode.ERROR_SUCCESS:
            str_message = 'failed to create batchno_serialno'
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))


    def __add_productiondata(self, obj_dbmgr,  dict_data, dict_serialNo):
        str_data_id = ""
        # 領退料
        obj_session = obj_dbmgr.get_session()
        #n_date = dict_data["date"]
        n_date = util_convert_timestamp_to_date(dict_serialNo["devDateTimestamp"])

        str_ref_no = dict_data["ref_no"]
        n_refno_category = dict_data["ref_no_category"]
        str_ref_no_sub = dict_data["ref_no_sub"]
        n_refno_subCategory = dict_data["ref_no_subCategory"]
        str_batchno = dict_data["batchno"]

        obj_data = (
            obj_session.query(CTableProductionData)
            .filter(CTableProductionData.work_order_no == str_ref_no)
            .first()
        )
        if obj_data:
            str_data_id = obj_data.no
        else:
            obj_work = (
                obj_session.query(CTableWorkOrder)
                .filter(CTableWorkOrder.no == str_ref_no)
                .first()
            )
            if obj_work:
                str_uuid = str(uuid.uuid4()).replace("-", "")
                new_data = CTableProductionData(
                    id=str_uuid,
                    creator_id='',
                    work_order_no=str_ref_no,
                    product_order_no=obj_work.product_order_no,
                    customer_no=obj_work.customer_no,
                    customer_displayName=obj_work.customer_displayName,
                    product_no=obj_work.product_no,
                    product_name=obj_work.product_name,
                    date=n_date,
                    product_line_no=obj_work.production_line_no,
                    oneProcess=obj_work.oneProcess,
                    secProcess=obj_work.secProcess,
                    preStartTime=0,
                    preEndTime=0,
                    postStartTime=0,
                    postEndTime=0,
                    preTotalTime=0,
                    postTotalTime=0,
                    laborCount=0,
                    laborList=[""],
                    item_no=obj_work.output_item_no,
                    item_name=obj_work.output_item_name,
                    unit=0,
                    count=0,
                    materialLoss=0,
                    grossWeight=0,
                    comment='',
                    creationTime=util_retrieve_now_time()
                )
                if obj_dbmgr.insert(new_data) != EErrorCode.ERROR_SUCCESS:
                    n_code = EErrorCode.ERROR_OTHER_ERROR
                    str_message = 'failed to create production data'
                    CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
                else:
                    str_data_id = str_uuid
        return str_data_id
    
    def __add_productiondata_input(self, obj_dbmgr, str_data_id,  dict_data, dict_serialNo):
        # 領退料
        obj_session = obj_dbmgr.get_session()
        #n_date = dict_data["date"]
        n_date = dict_serialNo["devDateTimestamp"]
        str_ref_no = dict_data["ref_no"]
        n_refno_category = dict_data["ref_no_category"]
        str_ref_no_sub = dict_data["ref_no_sub"]
        n_refno_subCategory = dict_data["ref_no_subCategory"]
        str_batchno = dict_data["batchno"]
        str_uuid = str(uuid.uuid4()).replace("-", "")
        str_comment = dict_data["comment"]

        obj_item = (
            obj_session.query(CTableProcessOrder)
            .filter(CTableProcessOrder.no == str_ref_no_sub)
            .first()
        )

        if obj_item:
            new_input = CTableProductionDataInput(
                id=str_uuid,
                work_order_no=str_ref_no,
                process_order_no=str_ref_no_sub,
                group="",
                production_data_id=str_data_id,
                time=n_date,
                action=EInputAction.RECEIVE if n_refno_subCategory == EProcessOrderCategory.RECEIVE else EInputAction.RETURN if n_refno_subCategory == EProcessOrderCategory.RETURN else 0,
                item_no=obj_item.item_no,
                item_name=obj_item.item_name,
                category=obj_item.itemCategory,
                itemSubCategory=obj_item.itemSubCategory,
                batch_number=str_batchno ,
                serial_no=dict_serialNo["serialNo"],
                unit=obj_item.unit,
                count=dict_serialNo["value"],
                avgLoss=0,
                comment = str_comment
            )
            if obj_dbmgr.insert(new_input) != EErrorCode.ERROR_SUCCESS:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'failed to create production data input'
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))

    def __add_productiondata_output(self, obj_dbmgr, str_data_id, dict_data, dict_serialNo):
        # 產品單
        obj_session = obj_dbmgr.get_session()
        #n_date = dict_data["date"]
        n_date = dict_serialNo["devDateTimestamp"]
        str_ref_no = dict_data["ref_no"]
        n_refno_category = dict_data["ref_no_category"]
        str_ref_no_sub = dict_data["ref_no_sub"]
        n_refno_subCategory = dict_data["ref_no_subCategory"]
        str_batchno = dict_data["batchno"]
        str_uuid = str(uuid.uuid4()).replace("-", "")
        str_comment = dict_data["comment"]

        obj_item = (
            obj_session.query(CTableProcessOrder)
            .filter(CTableProcessOrder.no == str_ref_no_sub)
            .first()
        )
        if obj_item:
            new_output = CTableProductionDataOutput(
                id=str_uuid,
                work_order_no=str_ref_no,
                process_order_no=str_ref_no_sub,
                production_data_id=str_data_id,
                time=n_date,
                action=EOutputAction.WORK,
                item_no=obj_item.item_no,
                item_name=obj_item.item_name,
                category=obj_item.itemCategory,
                batch_number=str_batchno,
                serial_no=dict_serialNo["serialNo"],
                unit=obj_item.unit,
                count=dict_serialNo["value"],
                comment=str_comment
            )
            if obj_dbmgr.insert(new_output) != EErrorCode.ERROR_SUCCESS:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'failed to create production data output'
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))

    def __add_productiondata_reuse(self, obj_dbmgr, str_data_id,  dict_data, dict_serialNo):
        # 餘/廢料單
        obj_session = obj_dbmgr.get_session()
        #n_date = dict_data["date"]
        n_date = dict_serialNo["devDateTimestamp"]
        str_ref_no = dict_data["ref_no"]
        n_refno_category = dict_data["ref_no_category"] #採購/產製/訂購
        str_ref_no_sub = dict_data["ref_no_sub"]
        n_refno_subCategory = dict_data["ref_no_subCategory"] #領/退/廢/餘/產
        str_batchno = dict_data["batchno"]
        str_uuid = str(uuid.uuid4()).replace("-", "")
        str_comment = dict_data["comment"]

        obj_item = (
            obj_session.query(CTableProcessOrder)
            .filter(CTableProcessOrder.no == str_ref_no_sub)
            .first()
        )
        if obj_item:
            new_reuse = CTableProductionDataReuse(
                id=str_uuid,
                work_order_no=str_ref_no,
                process_order_no=str_ref_no_sub,
                production_data_id=str_data_id,
                time=n_date,
                action=EOutputAction.WORK,
                item_no=obj_item.item_no,
                item_name=obj_item.item_name,
                category= EReuseCategory.REMAINING if n_refno_subCategory == EProcessOrderCategory.REMAIN else  EReuseCategory.WASTE if n_refno_subCategory == EProcessOrderCategory.WASTE else 0, # 餘/廢料
                itemSubCategory=obj_item.itemSubCategory,
                batch_number=str_batchno,
                serial_no=dict_serialNo["serialNo"],
                unit=obj_item.unit,
                count=dict_serialNo["value"],
                comment=str_comment
            )
            if obj_dbmgr.insert(new_reuse) != EErrorCode.ERROR_SUCCESS:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'failed to create production data output'
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))


    def __get_order_item_no(self, obj_session, str_ref_no, n_refno_category, str_ref_no_sub):
        str_item_no = ""
        if n_refno_category == EDevRefCategory.PURCHASE:
            obj_item = (
                obj_session.query(CTableGoodsReceiptNote)
                .filter(CTableGoodsReceiptNote.no == str_ref_no)
                .first()
            )
            if obj_item:
                str_item_no = obj_item.item_no
        if n_refno_category == EDevRefCategory.SALE:
            obj_item = (
                obj_session.query(CTableShippingOrder)
                .filter(CTableShippingOrder.no == str_ref_no)
                .first()
            )
            if obj_item:
                str_item_no = obj_item.item_no

        if n_refno_category == EDevRefCategory.WORK:
            obj_item = (
                obj_session.query(CTableProcessOrder)
                .filter(CTableProcessOrder.no == str_ref_no_sub)
                .first()
            )
            if obj_item:
                str_item_no = obj_item.item_no
        if n_refno_category == EDevRefCategory.OTHER:
            obj_item = (
                obj_session.query(CTableInventoryOrder)
                .filter(CTableInventoryOrder.no == str_ref_no)
                .first()
            )
            if obj_item:
                str_item_no = obj_item.item_no
        return str_item_no

    def __get_batch_no(self, obj_session, str_batchno):
        obj_batch = (
                obj_session.query(CTableBatchNumber)
                .filter(CTableBatchNumber.no == str_batchno)
                .first()
            )
        return obj_batch

    def __convent_ref_no_sub(self, obj_batch, str_ref_no_sub):
        lst_temp = str_ref_no_sub.split('@')
        if 1 < len(lst_temp) and obj_batch:
            str_ref_no_sub = obj_batch.ref_no
        return str_ref_no_sub