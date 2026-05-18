# coding=utf8
import pytz
import json
import string
import validictory
from copy import deepcopy
from flask import request
from package.util.util import *
from package.common.common import *
from package.log.log import CLogger
from package.dbwrapper.table import *
from package.dbwrapper.dbmgr import CDBMgr
from sqlalchemy import delete
import uuid
from .util import *
from collections import defaultdict

class CPrivilegeControl(object):

    def is_allowed_for_get(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.PURCHASE and privilege['action'] in (EPrivilegeAction.VIEW, EPrivilegeAction.REPORT)
                   for privilege in lst_privileges)

    def is_allowed_for_post(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.PURCHASE and privilege['action'] == EPrivilegeAction.CREATION
                   for privilege in lst_privileges)

    def is_allowed_for_put(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.PURCHASE and privilege['action'] == EPrivilegeAction.MODIFICATION
                   for privilege in lst_privileges)

    def is_allowed_for_delete(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.PURCHASE and privilege['action'] == EPrivilegeAction.CANCELLATION
                   for privilege in lst_privileges)


class CMaterial(CPrivilegeControl):
    GET_NAME = 1

    MODIFY_BASIC = 1
    MODIFY_PRICE = 2

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                n_total = (
                    obj_session.query(CTableMaterial)
                    .filter(*lst_where)
                    .order_by(CTableMaterial.no.asc())
                    .count()
                )
                n_start = 0
                n_count = 0
                if request.args.get('start') and request.args.get('count'):
                    n_start = int(request.args.get('start'))
                    n_count = int(request.args.get('count'))

                if n_count:
                    ids_query = (obj_session.query(
                                 CTableMaterial.no)
                                 .filter(*lst_where)
                                 .order_by(CTableMaterial.no.asc())
                                 .offset(n_start)
                                 .limit(n_count)
                                 )

                    ids = [no[0] for no in ids_query.all()]
                    lst_obj_result = (
                        obj_session.query(CTableMaterial)

                        .filter(CTableMaterial.no.in_(ids))
                        .order_by(CTableMaterial.no.asc())
                        .all()
                    )
                else:
                    lst_obj_result = (
                        obj_session.query(CTableMaterial)
                        .filter(*lst_where)
                        .order_by(CTableMaterial.no.asc())
                        .all()
                    )
                    
                if lst_obj_result:
                    lst_result = []



                    for obj_row in lst_obj_result:
                        dict_row = {}
                        if obj_row:
                            dict_row = object_as_dict(obj_row)
                            obj_price = (
                                obj_session.query(CTableMaterialPrice)
                                .filter(CTableMaterialPrice.item_no == dict_row["no"])
                                .first()
                            )
                            # 取得採購資訊
                            dict_row['purchase'] = {"date": obj_price.date if obj_price else 0,
                                                    "unit": obj_price.purchaseUnit if obj_price else 0,
                                                    "count":obj_price.purchaseCount if obj_price else 0,
                                                    "price":obj_price.purchasePrice if obj_price else 0,
                                                    "weightUnit": obj_price.purchaseWeightUnit if obj_price else 0,
                                                    "lenUnit": obj_price.purchaseLengthUnit if obj_price else 0,
                                                    "countUnit": obj_price.purchaseCountUnit if obj_price else 0,
                                                    }
                            dict_row['prices'] = []
                            # 取得盤點價位資訊
                            dict_row['prices'].append({"type":1, "weightUnit":obj_price.warehouseUnitWeight if obj_price else 0,
                                                       "weightPrice":obj_price.warehousePriceWeight if obj_price else 0,
                                                       "lenUnit":obj_price.warehouseUnitLength if obj_price else 0,
                                                       "lenPrice":obj_price.warehousePriceLength if obj_price else 0,
                                                       "countUnit": obj_price.warehouseUnitCount if obj_price else 0,
                                                       "countPrice": obj_price.warehousePriceCount if obj_price else 0
                                                       })
                            # 取得配方成本資訊
                            dict_row['prices'].append({"type": 2, "weightUnit":obj_price.costUnitWeight if obj_price else 0,
                                                       "weightPrice":obj_price.costPriceWeight if obj_price else 0,
                                                       "lenUnit": obj_price.costUnitLength if obj_price else 0,
                                                       "lenPrice": obj_price.costPriceLength if obj_price else 0,
                                                       "countUnit": obj_price.costUnitCount if obj_price else 0,
                                                       "countPrice": obj_price.costPriceCount if obj_price else 0
                                                       })
                        lst_result.append(dict_row)
                    if lst_result:
                        lst_tmp = []

                        if request.args.get('type') == 1:
                            for dict_data in lst_result:
                                lst_tmp.append({"id": dict_data["id"],
                                                "no": dict_data["no"],
                                                "name": dict_data["name"]})
                        else:
                            lst_tmp = lst_result
                        dict_extra_data['total'] = n_total
                        dict_extra_data['count'] = len(lst_tmp)
                        dict_extra_data['results'] = lst_tmp

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
                       'properties': {"material": {'type': 'object',
                                                   'properties': {
                                                       "category": {'type': 'integer'},
                                                       "subCategory": {'type': 'integer'},
                                                       "name": {'type': 'string'},
                                                       "supplier_no": {'type': 'string'},
                                                       "comment": {'type': 'string', 'blank': True}
                                                   }},
                                      "price": {'type': 'object',
                                                  'properties': {
                                                      "date": {'type': 'integer'},
                                                      "purchaseCount": {'type': 'integer'},
                                                      "purchaseUnit": {'type': 'integer'},
                                                      "purchasePrice": {'type': 'number'},
                                                      "purchaseWeightUnit": {'type': 'number'},
                                                      "purchaseLengthUnit": {'type': 'number'},
                                                      "purchaseCountUnit": {'type': 'number'},
                                                      "warehouseUnitWeight": {'type': 'integer'},
                                                      "warehousePriceWeight": {'type': 'number'},
                                                      "costUnitWeight": {'type': 'integer'},
                                                      "costPriceWeight": {'type': 'number'},
                                                      "warehouseUnitLength": {'type': 'integer'},
                                                      "warehousePriceLength": {'type': 'number'},
                                                      "costUnitLength": {'type': 'integer'},
                                                      "costPriceLength": {'type': 'number'},
                                                      "warehouseUnitCount": {'type': 'integer'},
                                                      "warehousePriceCount": {'type': 'number'},
                                                      "costUnitCount": {'type': 'integer'},
                                                      "costPriceCount": {'type': 'number'}

                                                  }}
                                      }}
        try:
            dict_param = request.get_json()
            validictory.validate(dict_param, dict_schema)
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()

                str_uuid = str(uuid.uuid4()).replace("-", "")
                dict_material = dict_param["material"]
                dict_price = dict_param["price"]
                str_no = self.__gen_no(dict_material["category"], dict_material["subCategory"])
                str_displayName = self.__retrieve_supplier_displayName(obj_session,
                                                                       dict_material["supplier_no"])
                new_data = CTableMaterial(
                    id=str_uuid,
                    no = str_no,
                    category=dict_material["category"],
                    subCategory=dict_material["subCategory"],
                    name=dict_material["name"],
                    supplier_no=dict_material["supplier_no"],
                    supplier_displayName=str_displayName,
                    unitShipping=0,
                    unitWarehouse=0,
                    package1Unit=0,
                    package12Count=0,
                    package2Unit=0,
                    package23Count=0,
                    package3Unit=0,
                    package34Count=0,
                    package4Unit=0,
                    specUnitType=0,
                    specUnit=0,
                    specValue=0,
                    comment=dict_material["comment"],
                    creationTime=util_retrieve_now_time(),
                )
                if obj_dbmgr.insert(new_data) == EErrorCode.ERROR_SUCCESS:
                    dict_extra_data = {"id": str_uuid}
                    # insert price
                    new_price = CTableMaterialPrice(
                        id=str(uuid.uuid4()).replace("-", ""),
                        item_no=str_no,
                        date = dict_price["date"],
                        purchaseCount = dict_price["purchaseCount"],
                        purchaseUnit = dict_price["purchaseUnit"],
                        purchasePrice = dict_price["purchasePrice"],
                        purchaseWeightUnit = dict_price["purchaseWeightUnit"],
                        purchaseLengthUnit = dict_price["purchaseLengthUnit"],
                        purchaseCountUnit=dict_price["purchaseCountUnit"],
                        warehouseUnitWeight = dict_price["warehouseUnitWeight"],
                        warehousePriceWeight = dict_price["warehousePriceWeight"],
                        warehouseUnitLength = dict_price["warehouseUnitLength"],
                        warehousePriceLength = dict_price["warehousePriceLength"],
                        warehouseUnitCount=dict_price["warehouseUnitCount"],
                        warehousePriceCount=dict_price["warehousePriceCount"],
                        costUnitWeight = dict_price["costUnitWeight"],
                        costPriceWeight = dict_price["costPriceWeight"],
                        costUnitLength = dict_price["costUnitLength"],
                        costPriceLength = dict_price["costPriceLength"],
                        costUnitCount=dict_price["costUnitCount"],
                        costPriceCount=dict_price["costPriceCount"],
                        creationTime=util_retrieve_now_time(),
                    )
                    if obj_dbmgr.insert(new_price) != EErrorCode.ERROR_SUCCESS:
                        n_code = EErrorCode.ERROR_OTHER_ERROR
                        str_message = 'failed to create material price'
                        CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
                else:
                    n_code = EErrorCode.ERROR_OTHER_ERROR
                    str_message = 'failed to create material'
                    CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def put(self, str_timezone='' , str_id=''):
        dict_param = {}
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
            try:
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    obj_material = (
                        obj_session.query(CTableMaterial)
                        .filter(CTableMaterial.no == request.args.get("no"))
                        .first()
                    )
                    dict_material = object_as_dict(obj_material)
                    dict_old = deepcopy(dict_material)

                    obj_price = (
                        obj_session.query(CTableMaterialPrice)
                        .filter(CTableMaterialPrice.item_no == request.args.get("no"))
                        .first()
                    )

                    if obj_price:
                        dict_price = object_as_dict(obj_price)
                    else:
                        dict_price = {
                            "item_no": request.args.get("no"),
                            "date": 0,
                            "purchaseCount": 0,
                            "purchaseUnit": 0,
                            "purchasePrice": 0,
                            "purchaseWeightUnit": 0,
                            "purchaseLengthUnit": 0,
                            "purchaseCountUnit": 0,
                            "warehouseUnitWeight": 0,
                            "warehousePriceWeight": 0,
                            "warehouseUnitLength": 0,
                            "warehousePriceLength": 0,
                            "warehouseUnitCount": 0,
                            "warehousePriceCount": 0,
                            "costUnitWeight": 0,
                            "costPriceWeight": 0,
                            "costUnitLength": 0,
                            "costPriceLength": 0,
                            "costUnitCount": 0,
                            "costPriceCount": 0,
                            "creationTime": util_retrieve_now_time(),
                        }
                    dict_old_price = deepcopy(dict_price)

                    if "material" in dict_param:
                        if "subCategory" in dict_param["material"]:
                            dict_material["subCategory"] = dict_param["material"]["subCategory"]
                        '''
                        if "supplier_no" in dict_param["material"]:
                            str_displayName = self.__retrieve_supplier_displayName(obj_session, dict_param["material"]["supplier_no"])
                            dict_material["supplier_no"] = dict_param["material"]["supplier_no"]
                            dict_material["supplier_displayName"] = str_displayName

                        if "category" in dict_param["material"]:
                            dict_material["category"] = dict_param["material"]["category"]
                        
                        if "name" in dict_param["material"]:
                            dict_material["name"] = dict_param["material"]["name"]
                        '''
                        if obj_dbmgr.update(CTableMaterial, [CTableMaterial.no == request.args.get("no")], dict_material) != EErrorCode.ERROR_SUCCESS:
                            n_code = EErrorCode.ERROR_OTHER_ERROR
                            str_message = 'failed to create material'
                            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
                        else:
                            #update history
                            self.__update_material_history(obj_session, request.args.get("no"),  dict_old,"999999999")

                    if "price" in dict_param:
                        if "date" in dict_param["price"]:
                            dict_price["date"] = dict_param["price"]["date"]

                        if "purchaseCount" in dict_param["price"]:
                            dict_price["purchaseCount"] = dict_param["price"]["purchaseCount"]

                        if "purchaseUnit" in dict_param["price"]:
                            dict_price["purchaseUnit"] = dict_param["price"]["purchaseUnit"]

                        if "purchasePrice" in dict_param["price"]:
                            dict_price["purchasePrice"] = dict_param["price"]["purchasePrice"]

                        if "purchaseWeightUnit" in dict_param["price"]:
                            dict_price["purchaseWeightUnit"] = dict_param["price"]["purchaseWeightUnit"]

                        if "purchaseLengthUnit" in dict_param["price"]:
                            dict_price["purchaseLengthUnit"] = dict_param["price"]["purchaseLengthUnit"]

                        if "purchaseCountUnit" in dict_param["price"]:
                            dict_price["purchaseCountUnit"] = dict_param["price"]["purchaseCountUnit"]


                        if "warehouseUnitWeight" in dict_param["price"]:
                            dict_price["warehouseUnitWeight"] = dict_param["price"]["warehouseUnitWeight"]

                        if "warehousePriceWeight" in dict_param["price"]:
                            dict_price["warehousePriceWeight"] = dict_param["price"]["warehousePriceWeight"]

                        if "warehouseUnitLength" in dict_param["price"]:
                            dict_price["warehouseUnitLength"] = dict_param["price"]["warehouseUnitLength"]

                        if "warehousePriceLength" in dict_param["price"]:
                            dict_price["warehousePriceLength"] = dict_param["price"]["warehousePriceLength"]

                        if "warehouseUnitCount" in dict_param["price"]:
                            dict_price["warehouseUnitCount"] = dict_param["price"]["warehouseUnitCount"]

                        if "warehousePriceCount" in dict_param["price"]:
                            dict_price["warehousePriceCount"] = dict_param["price"]["warehousePriceCount"]

                        if "costUnitWeight" in dict_param["price"]:
                            dict_price["costUnitWeight"] = dict_param["price"]["costUnitWeight"]

                        if "costPriceWeight" in dict_param["price"]:
                            dict_price["costPriceWeight"] = dict_param["price"]["costPriceWeight"]

                        if "costUnitLength" in dict_param["price"]:
                            dict_price["costUnitLength"] = dict_param["price"]["costUnitLength"]

                        if "costPriceLength" in dict_param["price"]:
                            dict_price["costPriceLength"] = dict_param["price"]["costPriceLength"]

                        if "costUnitCount" in dict_param["price"]:
                            dict_price["costUnitCount"] = dict_param["price"]["costUnitCount"]

                        if "costPriceCount" in dict_param["price"]:
                            dict_price["costPriceCount"] = dict_param["price"]["costPriceCount"]

                        if obj_price:
                            if obj_dbmgr.update(CTableMaterialPrice, [CTableMaterialPrice.item_no == request.args.get("no")],
                                                dict_price) != EErrorCode.ERROR_SUCCESS:
                                n_code = EErrorCode.ERROR_OTHER_ERROR
                                str_message = 'failed to create material'
                                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
                        else:
                            new_price = CTableMaterialPrice(
                                id=str(uuid.uuid4()).replace("-", ""),
                                item_no=dict_price["item_no"],
                                date=dict_price["date"],
                                purchaseCount=dict_price["purchaseCount"],
                                purchaseUnit=dict_price["purchaseUnit"],
                                purchasePrice=dict_price["purchasePrice"],
                                purchaseWeightUnit=dict_price["purchaseWeightUnit"],
                                purchaseLengthUnit=dict_price["purchaseLengthUnit"],
                                purchaseCountUnit=dict_price["purchaseCountUnit"],
                                warehouseUnitWeight=dict_price["warehouseUnitWeight"],
                                warehousePriceWeight=dict_price["warehousePriceWeight"],
                                warehouseUnitLength=dict_price["warehouseUnitLength"],
                                warehousePriceLength=dict_price["warehousePriceLength"],
                                warehouseUnitCount=dict_price["warehouseUnitCount"],
                                warehousePriceCount=dict_price["warehousePriceCount"],
                                costUnitWeight=dict_price["costUnitWeight"],
                                costPriceWeight=dict_price["costPriceWeight"],
                                costUnitLength=dict_price["costUnitLength"],
                                costPriceLength=dict_price["costPriceLength"],
                                costUnitCount=dict_price["costUnitCount"],
                                costPriceCount=dict_price["costPriceCount"],
                                creationTime=util_retrieve_now_time(),
                            )
                            if obj_dbmgr.insert(new_price) != EErrorCode.ERROR_SUCCESS:
                                n_code = EErrorCode.ERROR_OTHER_ERROR
                                str_message = 'failed to create material price'
                                CLogger().log(CLogger.LOG_LEVELERROR,
                                              '[%s] %s' % (self.__class__.__name__, str_message))
                        if  n_code == EErrorCode.ERROR_SUCCESS:
                            # update history
                            self.__update_price_history(obj_session, request.args.get("no"), dict_old_price, "999999999")
            except Exception as error:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'throw exception (error: %s)' % str(error)
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                              % (self.__class__.__name__, str(error)))
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
                    # delete material price
                    obj_delete1 = delete(CTableMaterialPrice).where(CTableMaterialPrice.item_no == request.args.get("no"))
                    obj_result1 = obj_session.execute(obj_delete1)
                    deleted_rows1 = obj_result1.rowcount
                    print(f"Deleted {deleted_rows1} rows.")

                    # delete material
                    obj_delete2 = delete(CTableMaterial).where(CTableMaterial.no == request.args.get("no"))
                    obj_result2 = obj_session.execute(obj_delete2)
                    deleted_rows2 = obj_result2.rowcount
                    print(f"Deleted {deleted_rows2} rows.")

                    # delete ItemHistory
                    obj_delete3 = delete(CTableItemHistory).where(
                        CTableItemHistory.ref_no == request.args.get("no"))
                    obj_result3 = obj_session.execute(obj_delete3)
                    deleted_rows3 = obj_result3.rowcount
                    print(f"Deleted {deleted_rows3} rows.")

                    # delete ItemPriceHistory
                    obj_delete4 = delete(CTableItemPriceHistory).where(
                        CTableItemPriceHistory.ref_no == request.args.get("no"))
                    obj_result4 = obj_session.execute(obj_delete4)
                    deleted_rows4 = obj_result4.rowcount
                    print(f"Deleted {deleted_rows4} rows.")
                    obj_session.commit()
            except Exception as error:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'throw exception (error: %s)' % str(error)
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                              % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def __fill_query_params(self):
        lst_where = []

        # setting  find conditions from query parameter
        if request.args.get('material_id'):
            lst_where.append(CTableMaterial.id == request.args.get('material_id'))

        if request.args.get('material_no'):
            lst_where.append(CTableMaterial.no == request.args.get('material_no'))

        if request.args.get('supplier_no'):
            lst_where.append(CTableMaterial.supplier_no == request.args.get('supplier_no'))

        if request.args.get('category'):
            lst_where.append(CTableMaterial.category == request.args.get('category'))

        return lst_where

    def __retrieve_supplier_displayName(self, obj_session, str_supplier_no):

        lst_result = (
            obj_session.query(CTableCompany.displayName)
            .filter(CTableCompany.no == str_supplier_no)
            .all()
        )
        return lst_result[0][0] if lst_result else ""


    def __gen_no(self, n_category, n_subCategory):
        str_type = ''
        if n_category == EMaterialType.PM:
            str_type = 'PM'
        elif n_category == EMaterialType.MA:
            str_type = 'MA'
        elif n_category == EMaterialType.AF:
            str_type = 'AF'
        str_no = "%s%02d" %(str_type, n_subCategory) + util_random_code(5)
        return str_no

    def __update_material_history(self, obj_session, str_material_no, old_data, user_id):
            new_obj_material = obj_session.query(CTableMaterial).filter_by(no=str_material_no).first()
            if not new_obj_material:
                raise ValueError("material not found")

            changes = []
            n_now = util_retrieve_now_time()
            for field, old_value in old_data.items():
                new_value = getattr(new_obj_material, field)  # 更新後的值
                if old_value != new_value:  # 檢查是否有變更
                    changes.append(
                        CTableItemHistory(
                            ref_no=str_material_no,
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

    def __update_price_history(self, obj_session, str_material_no, old_data, user_id):
            new_obj_price = obj_session.query(CTableMaterialPrice).filter_by(item_no=str_material_no).first()
            if not new_obj_price:
                raise ValueError("material not found")

            changes = []
            n_now = util_retrieve_now_time()
            for field, old_value in old_data.items():
                new_value = getattr(new_obj_price, field)  # 更新後的值
                if old_value != new_value:  # 檢查是否有變更
                    changes.append(
                        CTableItemPriceHistory(
                            ref_no=str_material_no,
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

class CItemPrice(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'count': 0, 'results': []}

        if not request.args.get("item_no"):
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'invalid parameter'
        else:
            try:
                with CDBMgr() as obj_dbmgr:
                    str_item_no = request.args.get("item_no")
                    obj_session = obj_dbmgr.get_session()
                    obj_date = self.__retrieve_one_year_ago(str_timezone)
                    lst_obj_price = (
                        obj_session.query(CTableItemPrice)
                        .filter(
                            CTableItemPrice.item_no == str_item_no,
                            CTableItemPrice.date >= obj_date
                        )
                        .order_by(CTableItemPrice.date.desc())
                        .all()
                    )

                    lst_result = []
                    for obj_price in lst_obj_price:
                        obj_loss = (
                            obj_session.query(CTableItemLoss)
                            .filter(
                                CTableItemLoss.item_no == str_item_no,
                                CTableItemLoss.date == obj_price.date
                            )
                            .first()
                        )
                        lst_result.append({
                            "month": obj_price.date.strftime("%Y/%m"),
                            "estUnit": obj_price.costUnitLength if obj_price.costUnitLength else obj_price.costUnitWeight,
                            "estPrice": obj_price.estCostPriceLength if obj_price.costUnitLength else obj_price.estCostPriceWeight,
                            "unit": obj_price.costUnitLength if obj_price.costUnitLength else obj_price.costUnitWeight,
                            "price": obj_price.costPriceLength if obj_price.costUnitLength else obj_price.costPriceWeight,
                            "lossUnit": obj_loss.unit if obj_loss else 0,
                            "loss": obj_loss.value if obj_loss else 0,
                            "estLoss": obj_loss.estValue if obj_loss else 0,
                        })
                    dict_extra_data["count"] = len(lst_result)
                    dict_extra_data["results"] = lst_result
            except Exception as error:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'throw exception (error: %s)' % str(error)
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                              % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def __retrieve_one_year_ago(self, str_timezone):
        from datetime import datetime
        from dateutil.relativedelta import relativedelta

        # 算出 11 個月前（含本月共12個月）的 1 號
        obj_date = (datetime.now() - relativedelta(months=11)).replace(day=1).date()
        return obj_date







class CMaterialHistory(CPrivilegeControl):
    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0,'results': []}

        if not request.args.get("no"):
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'invalid parameter'
        else:
            try:
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    lst_result = self.__get_history(obj_session, request.args.get("no"))
                    dict_extra_data['total'] = len(lst_result)
                    dict_extra_data['count'] = len(lst_result)
                    dict_extra_data['results'] = lst_result
            except Exception as error:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'throw exception (error: %s)' % str(error)
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                              % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data
    def __get_history(self, obj_session, str_material_no):
        import ast
        from collections import defaultdict

        lst_result = []
        obj_material = obj_session.query(CTableMaterial).filter(
            CTableMaterial.no == str_material_no
        ).first()

        obj_price = obj_session.query(CTableMaterialPrice).filter(
            CTableMaterialPrice.item_no == str_material_no
        ).first()

        if obj_material:
            dict_data = {"date":0,
                         "material": {},
                         "price":   {"date": 0,
                                     "purchaseCount": 0,
                                     "purchaseUnit": 0,
                                     "purchasePrice": 0,
                                     "purchaseWeightUnit": 0,
                                     "purchaseLengthUnit": 0,
                                     "purchaseCountUnit": 0,
                                     "warehouseUnitWeight": 0,
                                     "warehousePriceWeight": 0,
                                     "warehouseUnitLength": 0,
                                     "warehousePriceLength": 0,
                                     "warehouseUnitCount": 0,
                                     "warehousePriceCount": 0,
                                     "costUnitWeight": 0,
                                     "costPriceWeight": 0,
                                     "costUnitLength": 0,
                                     "costPriceLength": 0,
                                     "costUnitCount": 0,
                                     "costPriceCount": 0,
                                     }}
            dict_material = object_as_dict(obj_material)
            if obj_price:
                dict_price = object_as_dict(obj_price)
                dict_data["price"] = deepcopy(dict_price)
            dict_data["material"] = deepcopy(dict_material)
            dict_cur_data = deepcopy(dict_data)
            dict_cur_data['date'] = dict_cur_data["material"]["creationTime"]
            lst_result.append(dict_cur_data)

            # 查詢歷史記錄，按 modified_at 排序
            '''
            lst_records = obj_session.query(CTableItemHistory).filter(
                CTableItemHistory.ref_no == str_material_no
            ).order_by(
                CTableItemHistory.modifiedAt.desc()
            ).all()
            '''
            lst_records = self.__get_combined_history(obj_session, str_material_no)
            # 分組歷史記錄
            dict_group = defaultdict(list)
            for obj_record in lst_records:
                # 使用 modified_at 作為分組的 key
                n_key = obj_record.modifiedAt
                dict_group[n_key].append({
                    "changeType": obj_record.changeType,
                    "fieldName": obj_record.fieldName,
                    "oldValue": obj_record.oldValue,
                    "newValue": obj_record.newValue,
                    "modifiedBy": obj_record.modifiedBy
                })

            for n_time, lst_record in dict_group.items():
                dict_data['date'] = n_time
                for dict_record in lst_record:
                    if dict_record["changeType"] == "info":
                        dict_data["material"][dict_record["fieldName"]] = dict_record["oldValue"]
                    else:
                        dict_data["price"][dict_record["fieldName"]] = dict_record["oldValue"]
                dict_tmp = deepcopy(dict_data)
                lst_result.append(dict_tmp)
            self.__rotate_dates(lst_result)
        return lst_result

    # 假設已經有 `session` 物件
    def __get_combined_history(self, obj_session, ref_no):
        from sqlalchemy.orm import aliased
        from sqlalchemy import literal, union_all

        # 定義兩個表的別名
        item_history = aliased(CTableItemHistory)
        price_history = aliased(CTableItemPriceHistory)

        # 物料資訊修改紀錄
        query_item = obj_session.query(
            item_history.id.label("id"),
            item_history.ref_no.label("ref_no"),
            item_history.fieldName.label("fieldName"),
            item_history.oldValue.label("oldValue"),
            item_history.newValue.label("newValue"),
            item_history.modifiedBy.label("modifiedBy"),
            item_history.modifiedAt.label("modifiedAt"),
            literal("info").label("changeType")  # 加入識別欄位
        )

        # 價格修改紀錄
        query_price = obj_session.query(
            price_history.id.label("id"),
            price_history.ref_no.label("ref_no"),
            price_history.fieldName.label("fieldName"),
            price_history.oldValue.label("oldValue"),
            price_history.newValue.label("newValue"),
            price_history.modifiedBy.label("modifiedBy"),
            price_history.modifiedAt.label("modifiedAt"),
            literal("price").label("changeType")  # 加入識別欄位
        )

        # 使用 UNION ALL 合併兩個查詢
        combined_query = union_all(query_item, query_price).alias("history")

        # 建立最終查詢
        final_query = obj_session.query(
            combined_query.c.id,
            combined_query.c.ref_no,
            combined_query.c.fieldName,
            combined_query.c.oldValue,
            combined_query.c.newValue,
            combined_query.c.modifiedBy,
            combined_query.c.modifiedAt,
            combined_query.c.changeType
        )

        # 過濾條件：只查詢特定 ref_no
        if ref_no:
            final_query = final_query.filter(combined_query.c.ref_no == ref_no)

        # 排序（時間降序）
        final_query = final_query.order_by(combined_query.c.modifiedAt.desc())

        # 執行查詢
        return final_query.all()

    def __rotate_dates(self, lst_result):
        # 提取所有的日期，按順序移位
        lst_dates = [dict_item["date"] for dict_item in lst_result]
        lst_rotated_dates = lst_dates[1:] + lst_dates[:1]  # 右移：從第二個到最後一個，再補上第一個

        # 更新日期到對應的字典中
        for i, dict_item in enumerate(lst_result):
            dict_item["date"] = lst_rotated_dates[i]

