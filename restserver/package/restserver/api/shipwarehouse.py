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
from sqlalchemy.orm import aliased
import uuid
from package.util.util import *
from package.arap.arap import CCShipPayment, CCWarehousePayment


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

# alias
class CShipWarehouse(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0,'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                n_start = int(request.args.get('start', 0))
                n_count = int(request.args.get('count', 0))
                obj_sort = CTableShipWarehouseAlias.creationTime.asc()

                n_total, lst_obj_result = get_paginated_data(
                    obj_session,
                    CTableShipWarehouseAlias,
                    lst_where,
                    obj_sort,
                    n_start,
                    n_count
                )
                if lst_obj_result:
                    lst_result = []
                    for obj_row in lst_obj_result:
                        if obj_row:
                            dict_row = object_as_dict(obj_row)
                            lst_result.append(dict_row)
                    if lst_result:
                        dict_extra_data['total'] = n_total
                        dict_extra_data['count'] = len(lst_obj_result)
                        dict_extra_data['results'] = lst_result
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
        dict_extra_data = {}
        dict_schema = {'type': 'object',
                       'properties': {
                                        "company_no": {'type': 'string'},
                                        "company_displayName": {'type': 'string'},
                                        "displayName": {'type': 'string'},
                                        "region": {'type': 'integer'},
                                        "category": {'type': 'integer'},
                                        "subCategory": {'type': 'integer'},
                                        "unit": {'type': 'integer'},
                                        "validDate": {'type': 'integer'},
                                        "maxCapacity": {'type': 'number'},
                                        "price": {'type': 'number'},
                                        "comment": {'type': 'string', 'blank': True}
                                    }
                        }
        try:
            pass
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))

        return n_status_code, n_code, str_message, dict_extra_data

    def put(self, str_timezone='' , str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        dict_param = request.get_json()

        return n_status_code, n_code, str_message, dict_extra_data

    def delete(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}

        return n_status_code, n_code, str_message, dict_extra_data


    def __fill_query_params(self):
        lst_where = []
        if request.args.get('category'):
            lst_where.append(CTableShipWarehouseAlias.category == int(request.args.get('category')))

        return lst_where


class CShipWarehouseContract(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message, n_status_code, n_code = 'success', 200, EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0, 'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()

                # 1. 統一基礎查詢
                obj_query = (
                    obj_session.query(
                        CTableShipWarehouseContract,
                        CTableShipWarehouse,
                        CTableCompany,
                        CTablePayment
                    )
                    .filter(*lst_where)
                    .outerjoin(CTableShipWarehouse, CTableShipWarehouseContract.item_no == CTableShipWarehouse.no)
                    .outerjoin(CTableCompany, CTableShipWarehouse.company_no == CTableCompany.no)
                    .outerjoin(CTablePayment, CTableCompany.received_id == CTablePayment.id)
                    .order_by(CTableShipWarehouseContract.date.desc())
                )

                # 2. 計算總數
                dict_extra_data['total'] = obj_session.query(CTableShipWarehouseContract).filter(*lst_where).count()

                # 3. 處理分頁參數與執行查詢
                n_start = request.args.get('start', 0, type=int)
                n_count = request.args.get('count', 0, type=int)

                if n_count > 0:
                    obj_query = obj_query.offset(n_start).limit(n_count)

                lst_obj_result = obj_query.all()


                lst_result = []
                for obj_contract, wh, com, pay in lst_obj_result:
                    # con: Contract, wh: Warehouse, com: Company, pay: Payment
                    # 查詢議價編碼與日期
                    dict_data = object_as_dict(obj_contract)
                    dict_data.update(
                    {
                        "shipwh": {
                            "no": obj_contract.item_no,
                            "displayName": wh.displayName if wh else "",
                            "attribute": wh.attribute if wh else 0,
                        },
                        "vendor": {
                            "no": com.no if com else "",
                            "displayName": com.displayName if com else "",
                            "paymentType": pay.type if pay else 0,
                            "paymentDate": pay.date if pay else 0,
                            "paymentPeriod": pay.period if pay else 0
                        }
                    })
                    lst_result.append(dict_data)

                dict_extra_data['results'] = lst_result
                dict_extra_data['count'] = len(lst_result)

        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = f'throw exception (error: {error})'
            CLogger().log(CLogger.LOG_LEVELERROR, f'[{self.__class__.__name__}] {str_message}')

        return n_status_code, n_code, str_message, dict_extra_data

    def post(self, str_timezone='' , str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        dict_schema = {'type': 'object',
                       'properties': {
                                        "company_no": {'type': 'string'},
                                        "company_displayName": {'type': 'string'},
                                        "displayName": {'type': 'string'},
                                        "region": {'type': 'integer'},
                                        "category": {'type': 'integer'},
                                        "subCategory": {'type': 'integer'},
                                        "unit": {'type': 'integer'},
                                        "validDate": {'type': 'integer'},
                                        "maxCapacity": {'type': 'number'},
                                        "price": {'type': 'number'},
                                        "comment": {'type': 'string', 'blank': True}
                                    }
                        }
        try:
            dict_param = request.get_json()
            validictory.validate(dict_param, dict_schema)
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                str_uuid = str(uuid.uuid4()).replace("-", "")
                str_no = self.__gen_no(dict_param)
                new_data = CTableShipWarehouseContract(
                    id=str_uuid,
                    no=str_no,
                    company_no=dict_param["company_no"],
                    company_displayName=dict_param["company_displayName"],
                    displayName=dict_param["displayName"],
                    region=dict_param["region"],
                    category=dict_param["category"],
                    subCategory=dict_param["subCategory"],
                    validDate=dict_param["validDate"],
                    maxCapacity=dict_param["maxCapacity"],
                    unit=dict_param["unit"],
                    price=dict_param["price"],
                    comment=dict_param["comment"],
                    creationTime=util_retrieve_now_time()
                )
                if obj_dbmgr.insert(new_data) == EErrorCode.ERROR_SUCCESS:
                    dict_extra_data = {"id": str_uuid}
                else:
                    n_code = EErrorCode.ERROR_OTHER_ERROR
                    str_message = 'failed to create warehouse price'
                    CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))

        return n_status_code, n_code, str_message, dict_extra_data

    def put(self, str_timezone='' , str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        dict_param = request.get_json()
        if not request.args.get("no"):
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'invalid parameter'
        else:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                obj_warehouse = (
                    obj_session.query(CTableShipWarehouseContract)
                    .filter(CTableShipWarehouseContract.no == request.args.get("no"))
                    .first()
                )
                dict_warehouse = object_as_dict(obj_warehouse)
                dict_old = deepcopy(dict_warehouse)
                if "displayName" in dict_param:
                    dict_warehouse["displayName"] = dict_param["displayName"]
                if "category" in dict_param:
                    dict_warehouse["category"] = dict_param["category"]
                if "subCategory" in dict_param:
                    dict_warehouse["subCategory"] = dict_param["subCategory"]
                if "validDate" in dict_param:
                    dict_warehouse["validDate"] = dict_param["validDate"]
                if "maxCapacity" in dict_param:
                    dict_warehouse["maxCapacity"] = dict_param["maxCapacity"]
                if "unit" in dict_param:
                    dict_warehouse["unit"] = dict_param["unit"]
                if "price" in dict_param:
                    dict_warehouse["price"] = dict_param["price"]
                if "comment" in dict_param:
                    dict_warehouse["comment"] = dict_param["comment"]
                print(request.args.get("no"))
                if obj_dbmgr.update(CTableShipWarehouseContract, [CTableShipWarehouseContract.no == request.args.get("no")], dict_warehouse) != EErrorCode.ERROR_SUCCESS:
                    n_code = EErrorCode.ERROR_OTHER_ERROR
                    str_message = 'failed to update warehouse'
                    CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
                else:
                    # update history
                    self.__update_history(obj_session, request.args.get("no"), dict_old, "999999999")

        return n_status_code, n_code, str_message, dict_extra_data

    def delete(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}

        if not request.args.get("no"):
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'invalid parameter'
        else:
            try:
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    obj_delete = delete(CTableShipWarehouseContract).where(CTableShipWarehouseContract.no == request.args.get("no"))
                    obj_result = obj_session.execute(obj_delete)
                    deleted_rows = obj_result.rowcount
                    print(f"Deleted {deleted_rows} rows.")

                    # delete ItemHistory
                    obj_delete2 = delete(CTableWarehouseHistory).where(
                        CTableWarehouseHistory.ref_no == request.args.get("no"))
                    obj_result2 = obj_session.execute(obj_delete2)
                    deleted_rows2 = obj_result2.rowcount
                    print(f"Deleted {deleted_rows2} rows.")

                    obj_session.commit()
            except Exception as error:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'throw exception (error: %s)' % str(error)
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                              % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data


    def __fill_query_params(self):
        lst_where = []
        if request.args.get('category'):
            lst_where.append(CTableShipWarehouseContract.category == request.args.get('category'))

        if request.args.get('item_no'):
            lst_where.append(CTableShipWarehouseContract.item_no == request.args.get('item_no'))

        if request.args.get('no'):
            lst_where.append(CTableShipWarehouseContract.no == request.args.get('no'))

        if request.args.get('displayName'):
            lst_where.append(CTableShipWarehouseContract.displayName == request.args.get('displayName'))

        return lst_where

    def __gen_no(self, dict_param):
        from datetime import datetime
        str_date = datetime.fromtimestamp(dict_param["validDate"]).strftime('%y%m%d')
        str_no = "WH%d%s" %(dict_param["region"], str_date) + util_random_code(3)
        return str_no

    def __update_history(self, obj_session, str_no, old_data, user_id):
            new_obj_data = obj_session.query(CTableShipWarehouseContract).filter_by(no=str_no).first()
            if not new_obj_data:
                raise ValueError("warehouse not found")

            changes = []
            n_now = util_retrieve_now_time()
            for field, old_value in old_data.items():
                new_value = getattr(new_obj_data, field)  # 更新後的值
                if old_value != new_value:  # 檢查是否有變更
                    changes.append(
                        CTableWarehouseHistory(
                            ref_no=str_no,
                            fieldName=field,
                            oldValue=str(old_value) if old_value is not None else None,
                            newValue=str(new_value) if new_value is not None else None,
                            modifiedBy=user_id,
                            modifiedAt=n_now
                        )
                    )
            if changes:
                obj_session.add_all(changes)
            obj_session.commit()

class CShippingRec(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0,'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                n_start = int(request.args.get('start', 0))
                n_count = int(request.args.get('count', 0))
                CTablePaidPayment = aliased(CTablePayment)
                CTableReceivedPayment = aliased(CTablePayment)

                obj_query = obj_session.query(CTableShippingRec)
                if lst_where:
                    obj_query = obj_query.filter(*lst_where)
                n_total = obj_query.count()

                obj_query = (
                    obj_query.add_entity(CTableShipWarehouseAlias)
                    .add_entity(CTableShipWarehouseContract)
                    .add_entity(CTableShippingOrder)
                    .add_entity(CTableGoodsReceiptNote)
                    .outerjoin(CTableShipWarehouseAlias, CTableShippingRec.sw_alias_no == CTableShipWarehouseAlias.no)
                    .outerjoin(CTableShipWarehouseContract,
                               CTableShippingRec.contract_no == CTableShipWarehouseContract.no)
                    .outerjoin(CTableShippingOrder, CTableShippingRec.ref_no == CTableShippingOrder.no)
                    .outerjoin(CTableGoodsReceiptNote, CTableShippingRec.ref_no == CTableGoodsReceiptNote.no)
                    .add_entity(CTableProductOrder)
                    .add_entity(CTablePurchaseOrder)
                    .outerjoin(CTableProductOrder, CTableShippingOrder.product_order_no == CTableProductOrder.no)
                    .outerjoin(CTablePurchaseOrder, CTableGoodsReceiptNote.purchase_order_no == CTablePurchaseOrder.no)
                    # .outerjoin(CTablePaidPayment, CTableCompany.paid_id == CTablePaidPayment.id)
                    # .outerjoin(CTableReceivedPayment, CTableCompany.received_id == CTableReceivedPayment.id)

                    #.add_entity(CTableCompany)
                    #.add_entity(CTablePaidPayment)
                    #.add_entity(CTableReceivedPayment)
                    #.outerjoin(
                    #     CTableCompany,
                        # func.coalesce 動態決定要拿哪張表的 item_ref_no
                    #    CTableCompany.no == func.coalesce(
                    #         CTableShippingOrder.item_ref_no,
                    #        CTableGoodsReceiptNote.item_ref_no
                    #     )
                    #)
                    # .outerjoin(CTablePaidPayment, CTableCompany.paid_id == CTablePaidPayment.id)
                    #.outerjoin(CTableReceivedPayment, CTableCompany.received_id == CTableReceivedPayment.id)

                    .order_by(CTableShippingRec.date.asc())
                )

                if n_count > 0:
                    obj_query = obj_query.offset(n_start).limit(n_count)

                lst_obj_result = obj_query.all()
                if lst_obj_result:
                    lst_result = []
                    for obj_row in lst_obj_result:
                        if obj_row:
                            obj_rec = obj_row.CTableShippingRec
                            obj_alias = obj_row.CTableShipWarehouseAlias
                            obj_contract = obj_row.CTableShipWarehouseContract
                            obj_shipping_order = obj_row.CTableShippingOrder
                            obj_grn = obj_row.CTableGoodsReceiptNote
                            obj_product = obj_row.CTableProductOrder
                            obj_purchase = obj_row.CTablePurchaseOrder
                            #obj_paid_payment = obj_row[6]
                            #obj_received_payment = obj_row[7]
                            obj_order = obj_shipping_order if obj_shipping_order else obj_grn if obj_grn else None
                            obj_parent_order = obj_product if obj_product else obj_purchase if obj_purchase else None
                            #obj_payment = obj_paid_payment if obj_paid_payment else obj_received_payment if obj_received_payment else None
                            dict_row = {
                                "no":obj_rec.no if obj_rec else "",
                                "date": obj_rec.date if obj_rec else 0,
                                "count": obj_rec.count if obj_rec else 0,
                                "alias": {"name": obj_alias.name if obj_alias else "",
                                          "type": obj_alias.type if obj_alias else 0},
                                "contract": {"category": obj_contract.category if obj_contract else 0,
                                             "type": obj_contract.type if obj_contract else 0,
                                             "region": obj_contract.region if obj_contract else 0,
                                             "unit": obj_contract.unit if obj_contract else 0,
                                             "price": obj_contract.price  if obj_contract else 0},
                                "order": {"date": obj_order.date if obj_order else 0,

                                          "item_name": obj_order.item_name if obj_order else "",
                                          "item_ref_displayName": obj_order.item_ref_displayName if obj_order else "",
                                          #"paymentType": obj_payment.type if obj_payment else 0,
                                          "unit": obj_order.unit if obj_order else 0,
                                          "price": obj_order.price if obj_order else 0,
                                          "contractPrice": obj_parent_order.price if obj_parent_order else 0,
                                          },
                            }

                            lst_result.append(dict_row)
                    if lst_result:
                        dict_extra_data['total'] = n_total
                        dict_extra_data['count'] = len(lst_obj_result)
                        dict_extra_data['results'] = lst_result
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
        dict_extra_data = {}
        dict_schema = {'type': 'object',
                       'properties': {
                                        "company_no": {'type': 'string'},
                                        "company_displayName": {'type': 'string'},
                                        "displayName": {'type': 'string'},
                                        "region": {'type': 'integer'},
                                        "category": {'type': 'integer'},
                                        "subCategory": {'type': 'integer'},
                                        "unit": {'type': 'integer'},
                                        "validDate": {'type': 'integer'},
                                        "maxCapacity": {'type': 'number'},
                                        "price": {'type': 'number'},
                                        "comment": {'type': 'string', 'blank': True}
                                    }
                        }
        try:
            pass
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))

        return n_status_code, n_code, str_message, dict_extra_data

    def put(self, str_timezone='' , str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        dict_param = request.get_json()

        return n_status_code, n_code, str_message, dict_extra_data

    def delete(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}

        return n_status_code, n_code, str_message, dict_extra_data


    def __fill_query_params(self):
        lst_where = []
        if request.args.get('category'):
            lst_where.append(CTableShippingRec.refCategory == int(request.args.get('category')))

        return lst_where


class CShipPayment(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message, n_status_code, n_code = 'success', 200, EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0, 'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()

                obj_query_base = obj_session.query(CTableShippingPayment).filter(*lst_where)
                n_total = obj_query_base.count()

                n_start = int(request.args.get('start', 0))
                n_count = int(request.args.get('count', 0))

                lst_filter = lst_where
                if n_count > 0:
                    ids_query = (obj_session.query(CTableShippingPayment.no)
                                 .filter(*lst_where)
                                 .group_by(CTableShippingPayment.no)
                                 .order_by(CTableShippingPayment.date.desc())
                                 .offset(n_start).limit(n_count).all())
                    lst_filter = [CTableShippingPayment.no.in_([i[0] for i in ids_query])]

                # 1. 先建立一個包含總額的 Subquery
                subq = (
                    obj_session.query(
                        CTableShippingPayment.no.label('payment_no'),
                        func.round(func.sum(CTableShippingPayment.count), 0).label("count"),
                        func.round(func.sum(CTableShippingPayment.addDeleteAmount), 0).label("addDeleteAmount"),
                        func.round(func.sum(CTableShippingPayment.amount), 0).label("amount"),
                    )
                    .filter(*lst_filter)
                    .group_by(CTableShippingPayment.no)
                    .subquery()
                )

                # 2. 用這個 Subquery 去關聯其他 Table
                lst_obj_result = (
                    obj_session.query(CTableShippingPayment, CTableShippingRec, CTableShipWarehouseContract, subq)
                    .join(subq, CTableShippingPayment.no == subq.c.payment_no)
                    .outerjoin(CTableShippingRec, CTableShippingPayment.record_no == CTableShippingRec.no)
                    .outerjoin(CTableShipWarehouseContract,
                               CTableShippingRec.contract_no == CTableShipWarehouseContract.no)
                    .order_by(CTableShippingPayment.date.desc())
                    .all()
                )

                lst_result = []

                for row in lst_obj_result:
                    payment = row.CTableShippingPayment
                    shipping = row.CTableShippingRec
                    contract = row.CTableShipWarehouseContract

                    lst_result.append({
                        "payment": {
                            "no": payment.no,
                            "date": payment.date,
                            "month": payment.month.strftime("%Y/%m"),
                            "count": row.count,
                            "amount": int(row.amount or 0),
                            "addDeleteAmount": int(row.addDeleteAmount or 0)
                        },
                        "order": {
                            "checkedCount": shipping.checkedCount if shipping else 0,
                            "expectedCount": shipping.expectedCount if shipping else 0,
                            "item_name": shipping.item_name if shipping else "",
                            "item_ref_displayName": shipping.item_ref_displayName if shipping else "",
                            "unit": shipping.unit if shipping else 0,
                            "price": shipping.price if shipping else 0,
                            "contractNo": contract.no if contract else "",
                            "contractCategory": contract.category if contract else 0,
                            "contractType": contract.type if contract else 0,
                            "contractItemStyle": contract.itemStyle if contract else 0,
                            "paymentType": payment.paymentType if payment else 0,
                        },

                    })

                if lst_result:
                    dict_extra_data.update({'total': n_total, 'count': len(lst_result), 'results': lst_result})

        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = f'throw exception (error: {error})'
            CLogger().log(CLogger.LOG_LEVELERROR, f'[{self.__class__.__name__}] {str_message}')

        return n_status_code, n_code, str_message, dict_extra_data

    def post(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        return n_status_code, n_code, str_message, dict_extra_data

    def put(self, str_timezone='', str_id=''):
        dict_param = {}
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        dict_schema = {'type': 'object',
                       'properties': {}}

        return n_status_code, n_code, str_message, dict_extra_data

    def delete(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}

        return n_status_code, n_code, str_message, dict_extra_data

    def __fill_query_params(self):
        lst_where = []
        if request.args.get('category'):
            lst_where.append(CTableShippingPayment.refCategory == int(request.args.get('category')))

        return lst_where

class CShipARAP(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'results': []}
        if not request.args.get("order_no"):
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'invalid parameter'
        else:
            try:
                str_order_no = request.args.get("order_no")
                lst_result = CCShipPayment(str_timezone).get(EARAPType.AP, str_order_no)
                for dict_result in lst_result:
                    lst_recNos = [dict_rec["rec_no"] for dict_rec in dict_result["recDetails"]]
                    dict_result["records"] = []
                    with CDBMgr() as obj_dbmgr:
                        obj_session = obj_dbmgr.get_session()
                        lst_obj_result = (
                            obj_session.query(
                                CTableShippingRec,
                                CTableShipWarehouseContract
                            )
                            .outerjoin(CTableShipWarehouseContract,
                                       CTableShippingRec.contract_no == CTableShipWarehouseContract.no)
                            .filter(
                                CTableShippingRec.no.in_(lst_recNos)
                            )
                            .all()
                        )
                        for obj_row in lst_obj_result:
                            shipping = obj_row.CTableShippingRec
                            contract = obj_row.CTableShipWarehouseContract
                            f_amount = 0
                            for dict_rec in dict_result["recDetails"]:
                                if shipping and dict_rec["rec_no"] == shipping.no:
                                    f_amount = dict_rec["amount"]
                                    break

                            dict_record = {
                                "shipRec": {
                                    "date": shipping.date if shipping else 0,
                                    "unit": shipping.unit if shipping else 0,
                                    "price": shipping.price if shipping else 0,
                                    "amount": f_amount,
                                    "comment": shipping.comment if shipping else ""
                                },
                                "contract":{
                                    "category": contract.category if contract else 0,
                                    "type": contract.type if contract else 0,
                                    "region": contract.region if contract else 0
                                }
                            }
                            dict_result["records"].append(dict_record)
                    dict_result.pop('recDetails', None)
                dict_extra_data['total'] = len(lst_result)
                dict_extra_data['results'] = lst_result
            except Exception as error:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'throw exception (error: %s)' % str(error)
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                              % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data


class CWarehouseRec(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0,'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                n_start = int(request.args.get('start', 0))
                n_count = int(request.args.get('count', 0))


                obj_query = obj_session.query(CTableWarehouseRec)
                if lst_where:
                    obj_query = obj_query.filter(*lst_where)
                n_total = obj_query.count()

                obj_query = (
                    obj_query.add_entity(CTableShipWarehouseAlias)
                    .add_entity(CTableShipWarehouseContract)
                    .add_entity(CTableBatchNumber)
                    .outerjoin(CTableShipWarehouseAlias, CTableWarehouseRec.sw_alias_no == CTableShipWarehouseAlias.no)
                    .outerjoin(CTableShipWarehouseContract,
                               CTableWarehouseRec.contract_no == CTableShipWarehouseContract.no)
                    .outerjoin(CTableBatchNumber,
                               CTableWarehouseRec.batch_no == CTableBatchNumber.no)
                    .order_by(CTableWarehouseRec.date.asc())
                )

                if n_count > 0:
                    obj_query = obj_query.offset(n_start).limit(n_count)

                lst_obj_result = obj_query.all()
                if lst_obj_result:
                    lst_result = []
                    for obj_row in lst_obj_result:
                        if obj_row:
                            obj_rec = obj_row.CTableWarehouseRec
                            obj_alias = obj_row.CTableShipWarehouseAlias
                            obj_batch = obj_row.CTableBatchNumber
                            obj_contract = obj_row.CTableShipWarehouseContract

                            dict_row = {
                                "no":obj_rec.no if obj_rec else "",
                                "date": obj_rec.date if obj_rec else 0,
                                "count": obj_rec.count if obj_rec else 0,
                                "days": obj_rec.days if obj_rec else 0,
                                "alias": {"name": obj_alias.name if obj_alias else "",
                                          "type": obj_alias.type if obj_alias else 0},
                                "contract": {"category": obj_contract.category if obj_contract else 0,
                                             "type": obj_contract.type if obj_contract else 0,
                                             "unit": obj_contract.unit if obj_contract else 0,
                                             "price": obj_contract.price  if obj_contract else 0},
                                "batch": {
                                          "no": obj_batch.no if obj_batch else "",
                                          "item_name": obj_batch.item_name if obj_batch else "",
                                          "itemCategory": obj_batch.itemCategory if obj_batch else 0,
                                          "itemSubCategory": obj_batch.itemSubCategory if obj_batch else 0,
                                          "validDate": obj_batch.validDate if obj_batch else 0,
                                          },
                            }

                            lst_result.append(dict_row)
                    if lst_result:
                        dict_extra_data['total'] = n_total
                        dict_extra_data['count'] = len(lst_obj_result)
                        dict_extra_data['results'] = lst_result
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
        dict_extra_data = {}
        dict_schema = {'type': 'object',
                       'properties': {
                                        "company_no": {'type': 'string'},
                                        "company_displayName": {'type': 'string'},
                                        "displayName": {'type': 'string'},
                                        "region": {'type': 'integer'},
                                        "category": {'type': 'integer'},
                                        "subCategory": {'type': 'integer'},
                                        "unit": {'type': 'integer'},
                                        "validDate": {'type': 'integer'},
                                        "maxCapacity": {'type': 'number'},
                                        "price": {'type': 'number'},
                                        "comment": {'type': 'string', 'blank': True}
                                    }
                        }
        try:
            pass
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))

        return n_status_code, n_code, str_message, dict_extra_data

    def put(self, str_timezone='' , str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        dict_param = request.get_json()

        return n_status_code, n_code, str_message, dict_extra_data

    def delete(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}

        return n_status_code, n_code, str_message, dict_extra_data


    def __fill_query_params(self):
        lst_where = []


        return lst_where



class CWarehousePayment(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message, n_status_code, n_code = 'success', 200, EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0, 'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()

                obj_query_base = obj_session.query(CTableWarehousePayment).filter(*lst_where)
                n_total = obj_query_base.count()

                n_start = int(request.args.get('start', 0))
                n_count = int(request.args.get('count', 0))

                lst_filter = lst_where
                if n_count > 0:
                    ids_query = (obj_session.query(CTableWarehousePayment.no)
                                 .filter(*lst_where)
                                 .group_by(CTableWarehousePayment.no)
                                 .order_by(CTableWarehousePayment.date.desc())
                                 .offset(n_start).limit(n_count).all())
                    lst_filter = [CTableWarehousePayment.no.in_([i[0] for i in ids_query])]

                # 1. 先建立一個包含總額的 Subquery
                subq = (
                    obj_session.query(
                        CTableWarehousePayment.no.label('payment_no'),
                        func.round(func.sum(CTableWarehousePayment.count), 0).label("count"),
                        func.round(func.sum(CTableWarehousePayment.addDeleteAmount), 0).label("addDeleteAmount"),
                        func.round(func.sum(CTableWarehousePayment.amount), 0).label("amount"),
                    )
                    .filter(*lst_filter)
                    .group_by(CTableWarehousePayment.no)
                    .subquery()
                )

                # 2. 用這個 Subquery 去關聯其他 Table
                lst_obj_result = (
                    obj_session.query(CTableWarehousePayment, CTableWarehouseRec, CTableShipWarehouseContract, subq)
                    .join(subq, CTableWarehousePayment.no == subq.c.payment_no)
                    .outerjoin(CTableWarehouseRec, CTableWarehousePayment.record_no == CTableWarehouseRec.no)
                    .outerjoin(CTableShipWarehouseContract,
                               CTableWarehouseRec.contract_no == CTableShipWarehouseContract.no)
                    .order_by(CTableWarehousePayment.date.desc())
                    .all()
                )

                lst_result = []

                for row in lst_obj_result:
                    payment = row.CTableWarehousePayment
                    warehouse = row.CTableWarehouseRec
                    contract = row.CTableShipWarehouseContract

                    lst_result.append({
                        "payment": {
                            "no": payment.no,
                            "date": payment.date,
                            "month": payment.month.strftime("%Y/%m"),
                            "count": row.count,
                            "amount": int(row.amount or 0),
                            "addDeleteAmount": int(row.addDeleteAmount or 0)
                        },
                        "order": {
                            "count": warehouse.count if warehouse else 0,
                            "item_name": warehouse.item_name if warehouse else "",
                            "item_ref_displayName": warehouse.item_ref_displayName if warehouse else "",
                            "unit": warehouse.unit if warehouse else 0,
                            "price": warehouse.price if warehouse else 0,
                            "contractNo": contract.no if contract else "",
                            "contractCategory": contract.category if contract else 0,
                            "contractType": contract.type if contract else 0,
                            "contractItemStyle": contract.itemStyle if contract else 0,
                            "paymentType": payment.paymentType if payment else 0,
                        },

                    })

                if lst_result:
                    dict_extra_data.update({'total': n_total, 'count': len(lst_result), 'results': lst_result})

        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = f'throw exception (error: {error})'
            CLogger().log(CLogger.LOG_LEVELERROR, f'[{self.__class__.__name__}] {str_message}')

        return n_status_code, n_code, str_message, dict_extra_data

    def post(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        return n_status_code, n_code, str_message, dict_extra_data

    def put(self, str_timezone='', str_id=''):
        dict_param = {}
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        dict_schema = {'type': 'object',
                       'properties': {}}

        return n_status_code, n_code, str_message, dict_extra_data

    def delete(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}

        return n_status_code, n_code, str_message, dict_extra_data

    def __fill_query_params(self):
        lst_where = []

        return lst_where

class CWarehouseARAP(CPrivilegeControl):
    TYPE_PRODUCT_ORDER = 1
    TYPE_PURCHASE_ORDER = 2
    TYPE_GOODSRECEIPTNOTE = 3
    TYPE_SHIPPING_ORDER = 4

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'results': []}
        if not request.args.get("order_no"):
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'invalid parameter'
        else:
            try:
                str_order_no = request.args.get("order_no")
                n_category = int(request.args.get("order_category"))
                lst_result = CCWarehousePayment(str_timezone).get(n_category, str_order_no)

                for dict_result in lst_result:
                    lst_recNos = [dict_rec["rec_no"] for dict_rec in dict_result["recDetails"]]
                    dict_result["records"] = []
                    with CDBMgr() as obj_dbmgr:
                        obj_session = obj_dbmgr.get_session()
                        lst_obj_result = (
                            obj_session.query(
                                CTableWarehouseRec,
                                CTableShipWarehouseContract
                            )
                            .outerjoin(CTableShipWarehouseContract,
                                       CTableWarehouseRec.contract_no == CTableShipWarehouseContract.no)
                            .filter(
                                CTableWarehouseRec.no.in_(lst_recNos)
                            )
                            .all()
                        )
                        for obj_row in lst_obj_result:
                            warehouse = obj_row.CTableWarehouseRec
                            contract = obj_row.CTableShipWarehouseContract
                            f_amount = 0
                            for dict_rec in dict_result["recDetails"]:
                                if warehouse and dict_rec["rec_no"] == warehouse.no:
                                    f_amount = dict_rec["amount"]
                                    break

                            dict_record = {
                                "warehouseRec": {
                                    "date": warehouse.date if warehouse else 0,
                                    "unit": warehouse.unit if warehouse else 0,
                                    "price": warehouse.price if warehouse else 0,
                                    "countDays": warehouse.count * warehouse.days if warehouse else 0,
                                    "amount": f_amount,
                                    "comment": warehouse.comment if warehouse else ""
                                },
                                "contract": {
                                    "category": contract.category if contract else 0,
                                    "type": contract.type if contract else 0,
                                    "region": contract.region if contract else 0
                                }
                            }
                            dict_result["records"].append(dict_record)
                    dict_result.pop('recDetails', None)
                dict_extra_data['total'] = len(lst_result)
                dict_extra_data['results'] = lst_result

            except Exception as error:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'throw exception (error: %s)' % str(error)
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                              % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data