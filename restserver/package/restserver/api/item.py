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
from sqlalchemy import delete
import uuid
from package.util.util import *
from jsonschema import validate, ValidationError
from package.serialno.serialno import *
from package.serialno.observer import *
from package.items.items import *
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


class CPurchase(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'serverId': get_server_id(),
                           'serverTimestamp': util_retrieve_now_time(),
                           'count': 0,'results': []}

        try:
            n_date = 0
            n_shift = 0
            str_registerNo = ""

            if request.args.get("registerNo"):
                str_registerNo = request.args.get("registerNo")

            if request.args.get("dateTimestampUTC"):
                n_date = int(request.args.get("dateTimestampUTC"))

            if request.args.get("shift"):
                n_shift = int(request.args.get("shift"))

            lst_result = CItems(str_registerNo, str_timezone).get(CItems.PURCHASE, n_date, n_shift)
            if lst_result:
                dict_extra_data['count'] = len(lst_result)
                dict_extra_data['results'] = lst_result

        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data


class CManufacture(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'serverId':get_server_id(),
                           'serverTimestamp': util_retrieve_now_time(),
                           'count': 0,'results': []}

        try:
            n_date = 0
            n_shift = 0
            n_process = 0
            str_registerNo = ""

            if request.args.get("registerNo"):
                str_registerNo = request.args.get("registerNo")

            if request.args.get("dateTimestampUTC"):
                n_date = int(request.args.get("dateTimestampUTC"))

            if request.args.get("shift"):
                n_shift = int(request.args.get("shift"))

            if request.args.get("refProcess"):
                n_process = int(request.args.get("refProcess"))

            lst_result = CItems(str_registerNo, str_timezone).get(CItems.MANUFACTURE, n_date, n_shift, n_process)
            if lst_result:
                dict_extra_data['count'] = len(lst_result)
                dict_extra_data['results'] = lst_result

        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data


class CSales(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'serverId':get_server_id(), 'serverTimestamp': util_retrieve_now_time(), 'count': 0,'results': []}

        try:

            n_date = 0
            n_shift = 0
            str_registerNo = ""

            if request.args.get("registerNo"):
                str_registerNo = request.args.get("registerNo")

            if request.args.get("dateTimestampUTC"):
                n_date = int(request.args.get("dateTimestampUTC"))

            if request.args.get("shift"):
                n_shift = int(request.args.get("shift"))

            lst_result = CItems(str_registerNo, str_timezone).get(CItems.SALES, n_date, n_shift)
            if lst_result:
                dict_extra_data['count'] = len(lst_result)
                dict_extra_data['results'] = lst_result

        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data


class COther(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'serverId':get_server_id(), 'serverTimestamp': util_retrieve_now_time(), 'count': 0,'results': []}

        try:

            n_date = 0
            n_shift = 0
            str_registerNo = ""

            if request.args.get("registerNo"):
                str_registerNo = request.args.get("registerNo")

            if request.args.get("dateTimestampUTC"):
                n_date = int(request.args.get("dateTimestampUTC"))

            if request.args.get("shift"):
                n_shift = int(request.args.get("shift"))

            lst_result = CItems(str_registerNo, str_timezone).get(CItems.OTHER, n_date, n_shift)
            if lst_result:
                dict_extra_data['count'] = len(lst_result)
                dict_extra_data['results'] = lst_result

        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data



class CItemData(CPrivilegeControl):

    def post(self, str_timezone='' , str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {"serverTimestamp": util_retrieve_now_time(),
                           "serverId": get_server_id()}
        dict_schema = {
            'type': 'object',
            'properties': {
                "registerNo": {'type': 'string', "minLength": 1},
                # "checksum": {'type': 'string', "minLength": 1},
                'results': {
                    'type': 'array',
                    'minItems': 1,  # results 不可為空
                    'items': {
                        'type': 'object',
                        'properties': {
                            'devAction': {
                                'type': 'integer',
                                'enum': [EDevAction.IN, EDevAction.OUT]
                            },

                            'refNo': {'type': 'string', "minLength": 1},
                            'refNoSec': {'type': 'string'},
                            'itemBatchNo': {
                                'type': 'array',
                                'minItems': 1,  # itemBatchNo 不可為空
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'batchNo': {'type': 'string', "minLength": 1},
                                        'serialNos': {
                                            'type': 'array',
                                            'minItems': 1,  # serialNos 不可為空 value需大於0
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'devDateTimestamp': {'type': 'integer'},
                                                    'serialNo': {'type': 'string', "minLength": 1},
                                                    'value': {'type': 'number', 'exclusiveMinimum': 0},
                                                    'isValid': {'type': 'boolean'}
                                                },
                                                'required': ['devDateTimestamp', 'serialNo', 'value', 'isValid']
                                            }
                                        }
                                    },
                                    'required': ['batchNo', 'serialNos']
                                }
                            }
                        },
                        'required': ['devAction', 'refNo', 'itemBatchNo']
                    }
                }
            },
            'required': ['registerNo', 'results']
        }

        try:
            dict_body = request.get_json()
            str_body = request.get_data(as_text=True)
            validate(instance=dict_body, schema=dict_schema)

            obj_BSNo = CBSNoSubject()
            self.__register(obj_BSNo)
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                n_BSType = EBSType.NONE
                str_hardwareId, n_role = self.__retrieve_role(obj_session, dict_body["registerNo"])
                if str_hardwareId and n_role:
                    for dict_result in dict_body["results"]:
                        n_refno_category, n_refno_subCategory = self.__retrieve_refno_category_subCategory(obj_session, dict_result)
                        n_BSType = self.__retrieve_type(n_role, dict_result["devAction"], n_refno_category,
                                                        n_refno_subCategory)

                        lst_batchNo = []
                        for dict_batch in dict_result["itemBatchNo"]:
                            dict_data = {
                                "bsType": n_BSType,
                                #"date": dict_result["devDateTimestamp"],
                                "ref_no": dict_result["refNo"],
                                "ref_no_category": n_refno_category,
                                "ref_no_sub": dict_result["refNoSec"],
                                "ref_no_subCategory": n_refno_subCategory,
                                "batchno": dict_batch["batchNo"],
                                "serialNos": dict_batch["serialNos"], # 時間&有效
                                "comment": dict_result["devComment"]
                            }
                            # 倉庫
                            # 1.新增出入庫紀錄.
                            # 2.紀錄批號與序號關聯(庫存/批號/更新批號檢定數量)
                            # 3. 寫log
                            # 產間 1.紀錄批號與序號關聯(餘廢產單/批號 更新批號檢定數量/製造數據/餘廢產單)
                            # 2. 寫log
                            lst_batchNo.append(dict_data)
                        if lst_batchNo:
                            obj_BSNo.add(lst_batchNo, str_hardwareId)
                self.__write_log(obj_dbmgr, str_body, str_hardwareId, n_role, n_BSType)
        except ValidationError as e:
            n_code = EErrorCode.ERROR_INVAILD_BODY
            str_message = 'validated error: {0} {1}'.format(e.message, list(e.path))
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s, body: %s)'
                          % (self.__class__.__name__, str(e.message), str_body))

        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s, body: %s)'
                          % (self.__class__.__name__, str(error), str_body))

        return n_status_code, n_code, str_message, dict_extra_data


    def __register(self, obj_subject):
        # 批號檢定數量
        obj_subject.register_observer(CBatchNumberObserver.update)

        # 進貨計價數量
        obj_subject.register_observer(CGRNoteObserver.update)

        # 銷貨計價數量
        obj_subject.register_observer(CShippingOrderObserver.update)


    def __retrieve_role(self, obj_session, str_registerNo):
        obj_result = (
            obj_session.query(CTableDevice)
            .filter(CTableDevice.no == str_registerNo)
            .first()
        )
        return obj_result.hardwareId if obj_result else "", obj_result.role if obj_result else 0

    def __retrieve_type(self, n_role, n_action, n_refno_category, n_refno_subCategory):
        n_type = EBSType.NONE

        if n_role == ELocationType.STORAGE:
            if n_action == EDevAction.IN:
                if n_refno_category == EDevRefCategory.WORK:
                    # 1.餘/廢/產入庫 2. 退料入庫
                    # 確認批號是否為投入物; 退料入庫
                    if n_refno_subCategory == EProcessOrderCategory.RETURN:
                        n_type = EBSType.PRODUCT_RETURN_IN_S
                    elif n_refno_subCategory in [EProcessOrderCategory.REMAIN, EProcessOrderCategory.WASTE, EProcessOrderCategory.PRODUCT]:
                        n_type = EBSType.PRODUCT_IN_S

                elif n_refno_category == EDevRefCategory.PURCHASE:
                    n_type = EBSType.PURCHASE_IN_S
                elif n_refno_category == EDevRefCategory.SALE:
                    n_type = EBSType.SALE_IN_S
                elif n_refno_category == EDevRefCategory.OTHER:
                    n_type = EBSType.OTHER_IN_S
            elif n_action == EDevAction.OUT:
                if n_refno_category == EDevRefCategory.WORK and n_refno_subCategory == EProcessOrderCategory.RECEIVE:
                    n_type = EBSType.PRODUCT_OUT_S
                elif n_refno_category == EDevRefCategory.PURCHASE:
                    n_type = EBSType.PURCHASE_OUT_S
                elif n_refno_category == EDevRefCategory.SALE:
                    n_type = EBSType.SALE_OUT_S
                elif n_refno_category == EDevRefCategory.OTHER:
                    n_type = EBSType.OTHER_OUT_S
        else:
            if n_action == EDevAction.IN:
                if n_refno_category == EDevRefCategory.WORK:
                   n_type = EBSType.PRODUCT_IN_P
            elif n_action == EDevAction.OUT:
                if n_refno_category == EDevRefCategory.WORK:
                    n_type = EBSType.PRODUCT_OUT_P
        return n_type


    def __retrieve_refno_category_subCategory(self, obj_session, dict_body):
        n_category = EDevRefCategory.NONE
        n_subCategory = EProcessOrderCategory.NONE
        str_ref_no = dict_body["refNo"]
        str_ref_no_sec = dict_body["refNoSec"]
        obj_result = (
            obj_session.query(CTableGoodsReceiptNote)
            .filter(CTableGoodsReceiptNote.no == str_ref_no)
            .first()
        )
        if obj_result:
            n_category = EDevRefCategory.PURCHASE
        else:
            obj_result = (
                obj_session.query(CTableWorkOrder)
                .filter(CTableWorkOrder.no == str_ref_no)
                .first()
            )
            if obj_result:
                # 產製入庫-->多個 子訂單
                lst_temp = str_ref_no_sec.split('@')
                if 1 < len(lst_temp):
                    str_ref_no_sec = lst_temp[0] + '_' + lst_temp[1]

                n_category = EDevRefCategory.WORK
                obj_process_order = (
                    obj_session.query(CTableProcessOrder)
                    .filter(CTableProcessOrder.no == str_ref_no_sec)
                    .first()
                )
                if obj_process_order:
                    n_subCategory = obj_process_order.category
            else:
                obj_result = (
                    obj_session.query(CTableShippingOrder)
                    .filter(CTableShippingOrder.no == str_ref_no)
                    .first()
                )
                if obj_result:
                    n_category = EDevRefCategory.SALE
                else:
                    # inventory_order
                    obj_result = (
                        obj_session.query(CTableInventoryOrder)
                        .filter(CTableInventoryOrder.no == str_ref_no)
                        .first()
                    )
                    if obj_result:
                        n_category = EDevRefCategory.OTHER
        return n_category, n_subCategory

    def __write_log(self, obj_dbmgr, str_body, str_hardwareId, n_role, n_BSType):
        str_uuid = str(uuid.uuid4()).replace("-", "")
        new_log = CTableDeviceLog(

            hardwareId= str_hardwareId,
            role = n_role,
            action = n_BSType,
            data = str_body,
            creationTime = util_retrieve_now_time()
        )
        if obj_dbmgr.insert(new_log) != EErrorCode.ERROR_SUCCESS:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'failed to create log'
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))


class CItemDataGroup(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'serverId':get_server_id(),
                           'serverTimestamp': util_retrieve_now_time(),
                           'count': 0,'results': []}

        try:
            from sqlalchemy import text
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                sql = text("""
                    SELECT `group`, batch_number, GROUP_CONCAT(serialNo) AS serials
                    FROM batchno_serialno_group
                    GROUP BY `group`, batch_number;
                """)
                lst_tmp = obj_session.execute(sql)
                for row in lst_tmp:
                    str_group = row[0]
                    str_batchNo = row[1]
                    lst_serials = row[2].split(',')  # GROUP_CONCAT 結果需分割
                #if lst_result:
                #    dict_extra_data['count'] = len(lst_result)
                #    dict_extra_data['results'] = lst_result

        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def post(self, str_timezone='' , str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {"serverTimestamp": util_retrieve_now_time(),
                           "serverId": get_server_id()}
        dict_schema = {
            'type': 'object',
            'properties': {
                "registerNo": {'type': 'string', "minLength": 1},
                "total": {'type': 'integer'},
                'results': {
                    'type': 'array',
                    'minItems': 1,  # results 不可為空
                    'items': {
                        'type': 'object',
                        'properties': {
                            'devDateTimestamp': {'type': 'integer'},
                            'devGroupNo': {'type': 'string', "minLength": 1},
                            'devComment': {'type': 'string'},
                            'itemBatchNo': {
                                'type': 'array',
                                'minItems': 1,  # itemBatchNo 不可為空
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'batchNo': {'type': 'string', "minLength": 1},
                                        'serialNos': {
                                            'type': 'array',
                                            'minItems': 1,  # serialNos 不可為空
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'serialNo': {'type': 'string', "minLength": 1},
                                                    'value': {'type': 'number'}
                                                },
                                                'required': ['serialNo', 'value']
                                            }
                                        },

                                    },
                                    'required': ['batchNo', 'serialNos']
                                }
                            }
                        },
                        'required': ['devDateTimestamp', 'devGroupNo', 'itemBatchNo']
                    }
                }
            },
            'required': ['registerNo', 'results']
        }

        try:
            str_body = request.get_data(as_text=True)
            dict_body = request.get_json()
            validate(instance=dict_body, schema=dict_schema)
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                for dict_result in dict_body["results"]:
                    str_group_no = dict_result["devGroupNo"]
                    lst_result = (
                        obj_session.query(CTableBatchNoSerialNoGroup)
                        .filter(CTableBatchNoSerialNoGroup.group == str_group_no)
                        .all()
                    )
                    if lst_result:
                        obj_session.query(CTableBatchNoSerialNoGroup) \
                            .filter(CTableBatchNoSerialNoGroup.group == str_group_no) \
                            .delete(synchronize_session=False)

                        obj_session.commit()

                    for dict_batch in dict_result["itemBatchNo"]:
                        for dict_serialNo in dict_batch["serialNos"]:
                            new_data = CTableBatchNoSerialNoGroup(
                                time=dict_result["devDateTimestamp"],
                                group=dict_result["devGroupNo"],
                                batch_number=dict_batch["batchNo"],
                                serialNo=dict_serialNo["serialNo"],
                                count=dict_serialNo["value"],
                                warehouse_no = "WH4250218PDL",
                                comment=dict_result["devComment"]
                            )
                            if obj_dbmgr.insert(new_data) != EErrorCode.ERROR_SUCCESS:
                                n_code = EErrorCode.ERROR_OTHER_ERROR
                                str_message = 'failed to create group item data'
                                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))

        except ValidationError as e:
            n_code = EErrorCode.ERROR_INVAILD_BODY
            str_message = 'validated error: {0} {1}'.format(e.message, list(e.path))
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s, body: %s)'
                          % (self.__class__.__name__, str(e.message), str_body))
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s, body: %s)'
                          % (self.__class__.__name__, str(error), str_body))

        return n_status_code, n_code, str_message, dict_extra_data

class CInfo(CPrivilegeControl):
    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'serverId': get_server_id(), 'serverTimestamp': util_retrieve_now_time(), 'count': 0,
                           'results': []}

        try:
            str_registerNo = ""
            str_batchNo = ""
            if request.args.get("registerNo"):
                str_registerNo = request.args.get("registerNo")
            if request.args.get("batchNo"):
                str_batchNo = request.args.get("batchNo")

            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_result = []
                if str_batchNo:
                    lst_obj_result = (
                        obj_session.query(CTableBatchNumber)
                        .filter(CTableBatchNumber.no == str_batchNo)
                        .all()
                    )
                    for obj_result in lst_obj_result:
                        lst_result.append({ "itemNo": obj_result.item_no,
                                            "itemName": obj_result.item_name,
                                            "itemVendor": obj_result.item_ref_displayName,
                                            "itemType": obj_result.itemCategory,
                                            "itemCategory": obj_result.itemType,
                                            "itemBatchNo": obj_result.no,
                                            "itemValidDateTimestamp": obj_result.validDate,
                                            "itemComment": obj_result.comment})
                if lst_result:
                    dict_extra_data['count'] = len(lst_result)
                    dict_extra_data['results'] = lst_result

        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

class CGroupInfo(CPrivilegeControl):
    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'serverId': get_server_id(), 'serverTimestamp': util_retrieve_now_time(), 'count': 0,
                           'results': []}

        try:
            str_registerNo = ""
            str_groupNo = ""
            if request.args.get("registerNo"):
                str_registerNo = request.args.get("registerNo")
            if request.args.get("groupNo"):
                str_groupNo = request.args.get("groupNo")

            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_result = []
                if str_groupNo:
                    lst_obj_result = (
                        obj_session.query(CTableBatchNoSerialNoGroup)
                        .filter(CTableBatchNoSerialNoGroup.group == str_groupNo)
                        .all()
                    )
                    if lst_obj_result:

                        lst_batchno = []
                        dict_batchno = {
                            batch_number: list(group)
                            for batch_number, group in groupby(lst_obj_result, key=attrgetter('batch_number'))
                        }
                        str_itemNo = ""
                        str_itemName = ""
                        str_itemVendor =  ""
                        n_itemType = 0
                        n_itemCategory = 0
                        str_comment = ""
                        for str_key, lst_temp in dict_batchno.items():
                            lst_serial = []

                            obj_result = (
                                obj_session.query(CTableBatchNumber)
                                .filter(CTableBatchNumber.no == str_key)
                                .first()
                            )
                            str_itemNo = obj_result.item_no if obj_result else ""
                            str_itemName = obj_result.item_name if obj_result else ""
                            str_itemVendor = obj_result.item_ref_displayName if obj_result else ""
                            n_itemType = obj_result.itemType if obj_result else 0
                            n_itemCategory = obj_result.itemCategory if obj_result else 0
                            str_comment = ""
                            n_validDate =  obj_result.validDate if obj_result else 0
                            for obj_temp in lst_temp:
                                str_comment = obj_temp.comment
                                if obj_temp.serialNo:
                                    lst_serial.append({"serialNo": obj_temp.serialNo, "value": obj_temp.count})
                            lst_batchno.append({"batchNo": str_key,
                                                "validDateTimestamp": n_validDate,
                                                "serialNos": lst_serial})

                        dict_data = {"groupNo": str_groupNo,
                                     "itemNo": str_itemNo,
                                     "itemName": str_itemName,
                                     "itemVendor": str_itemVendor,
                                     "itemType": n_itemCategory,
                                     "itemCategory": n_itemType,
                                     "itemComment": str_comment,
                                     "itemBatchNo": lst_batchno
                                     }
                        lst_result.append(dict_data)
                if lst_result:
                    dict_extra_data['count'] = len(lst_result)
                    dict_extra_data['results'] = lst_result

        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data
