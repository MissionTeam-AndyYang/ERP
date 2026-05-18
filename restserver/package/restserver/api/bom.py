# coding=utf8
import pytz
import uuid
import json
import string
import validictory
from copy import deepcopy
import math
from flask import request
from package.util.util import *
from .common import *
from package.common.common import *
from package.log.log import CLogger
from package.dbwrapper.table import *
from package.dbwrapper.dbmgr import CDBMgr
from package.util.util import *
from sqlalchemy import func, cast, Numeric
from .util import *
from sqlalchemy import delete
from sqlalchemy.orm import contains_eager, selectinload
from package.bom.bom import *
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

def gen_no():
    from datetime import datetime
    obj_today = datetime.today()
    n_year = obj_today.year
    n_month = obj_today.month
    str_no = "BOM%02d%02d" % (n_year, n_month) + util_random_code(3)
    return str_no

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


class CBom(CPrivilegeControl):
    LIST=1
    INFO=2
    NAME=3


    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0,'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                if request.args.get('type') and int(request.args.get('type')) == self.LIST:
                    # 取得BOM最新版本
                    lst_where = self.__fill_query_params()
                    subquery = (
                        obj_session.query(
                            CTableBOM.no,
                            func.max(CTableBOM.version).label('max_version')
                        )
                        .filter(*lst_where)
                        .group_by(CTableBOM.no)
                        .subquery()
                    )

                    n_total = obj_session.query(func.count()).select_from(
                        obj_session.query(CTableBOM)
                        .join(
                            subquery,
                            (CTableBOM.no == subquery.c.no) & (CTableBOM.version == subquery.c.max_version)
                        ).subquery()
                    ).scalar()
                    n_start = 0
                    n_count = 0
                    if request.args.get('start') and request.args.get('count'):
                        n_start = int(request.args.get('start'))
                        n_count = int(request.args.get('count'))
                    if n_count:
                        lst_obj_result = (
                            obj_session.query(CTableBOM)
                            .join(
                                subquery,
                                (CTableBOM.no == subquery.c.no) & (CTableBOM.version == subquery.c.max_version)
                            )
                            .offset(n_start)
                            .limit(n_count)
                            .all()
                        )
                    else:
                        lst_obj_result = (
                            obj_session.query(CTableBOM)
                            .join(
                                subquery,
                                (CTableBOM.no == subquery.c.no) & (CTableBOM.version == subquery.c.max_version)
                            )
                            .all()
                        )
                    if lst_obj_result:
                        lst_result = []
                        for obj_row in lst_obj_result:
                            dict_row = {}
                            if obj_row:
                                dict_row = object_as_dict(obj_row)
                                dict_row["items"] = []
                                for obj_item in obj_row.item_data:
                                    dict_row["items"].append(object_as_dict(obj_item))
                            lst_result.append(dict_row)
                        if lst_result:
                            dict_extra_data['total'] = n_total
                            dict_extra_data['count'] = len(lst_obj_result)
                            dict_extra_data['results'] = lst_result
                    print("")

                else:
                    # 資料結構階層 名稱->版本清單->原料清單
                    lst_where = self.__fill_query_params()
                    lst_no = (
                        obj_session.query(CTableBOM)
                        .filter(*lst_where)
                        .group_by(CTableBOM.no)
                        .all()
                    )
                    lst_result = []
                    for obj_no in lst_no:
                        dict_result = {"id": obj_no.id,
                                       "no": obj_no.no,
                                       "displayName": obj_no.displayName,
                                       "unit": obj_no.unit,
                                       "data": []}
                        # retrieve details data
                        if request.args.get('type') and int(request.args.get('type')) == self.INFO:
                            lst_obj_result = (obj_session.query(CTableBOM)
                                              .filter(CTableBOM.no == obj_no.no)
                                              .order_by(CTableBOM.creationTime.desc())
                                              .all())

                            for obj_result in lst_obj_result:
                                dict_result["unit"] = obj_result.unit
                                dict_data = {"version": obj_result.version,
                                             "date": obj_result.date,
                                             "unit": obj_result.unit,
                                             "weight": obj_result.weight,
                                             "creationTime": obj_result.creationTime,
                                             "comment": "",
                                             "items": [],
                                             "cost": []}
                                dict_result["data"].append(dict_data)

                                for obj_row in obj_result.item_data:
                                    dict_row = {}
                                    if obj_row:
                                        dict_row = object_as_dict(obj_row)
                                        #投入物的
                                        _, n_category, n_subCategory, _, n_unitProduct = util_new_get_item_info(dict_row["item_no"])

                                        dict_row["itemCategory"] = n_category
                                        dict_row["itemSubCategory"] = n_subCategory
                                        dict_row["unitProduct"] = n_unitProduct
                                    dict_data["items"].append(dict_row)
                                dict_data["cost"] = self.__get_cost(obj_session, str_timezone, obj_no.no)

                        lst_result.append(dict_result)
                    dict_extra_data['total'] = len(lst_result)
                    dict_extra_data['count'] = len(lst_result)
                    dict_extra_data['results']= lst_result
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
                                       "displayName": {'type': 'string'},
                                       "version": {'type': 'number'},
                                       "comment": {'type': 'string', 'blank': True},
                                       "items": {'type': 'array', 'required': True,
                                                          'items': {'type': 'object',
                                                                    'properties': {
                                                                                   "unit": {
                                                                                       'type': 'integer'},
                                                                                   "weight": {
                                                                                       'type': 'number'},
                                                                                   "material_no": {
                                                                                       'type': 'string'},
                                                                                    "material_name": {
                                                                                        'type': 'string'}
                                                                    }}}
                                      }}
        '''
        01-03 --- BOM
        04-05 --- 建立日期:年
        06-07 --- 建立日期:月
        08-10 --- 隨機
        '''
        try:
            dict_param =  request.get_json()
            validictory.validate(dict_param, dict_schema)
            n_max_retries = 5
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                str_uuid = str(uuid.uuid4()).replace("-", "")
                str_no = self.__gen_no()

                n_nuit = 0
                f_weight = 0.0
                for dict_item in dict_param["items"]:
                    n_nuit = dict_item["unit"]
                    f_weight += dict_item["weight"]
                new_data = CTableBOM(
                    id=str_uuid,
                    no= str_no,
                    displayName=dict_param["displayName"],
                    unit=n_nuit,
                    weight=f_weight,
                    version=dict_param["version"],
                    comment=dict_param["comment"],
                    creationTime=util_retrieve_now_time(),
                )

                for n_index in range(1, n_max_retries + 1):
                    if obj_dbmgr.insert(new_data) == EErrorCode.ERROR_SUCCESS:
                        dict_extra_data = {"id": str_uuid}
                        for dict_item in dict_param["items"]:
                            str_item_uuid = str(uuid.uuid4()).replace("-", "")
                            new_item = CTableBOMItem(
                                id=str_item_uuid,
                                bom_id=str_uuid,
                                item_no=dict_item["material_no"],
                                item_name=dict_item["material_name"],
                                unit=dict_item["unit"],
                                weight=dict_item["weight"],
                                creationTime=util_retrieve_now_time()
                            )
                            if not obj_dbmgr.insert(new_item) == EErrorCode.ERROR_SUCCESS:
                                str_message = 'failed to create BOM obj_session'
                                CLogger().log(CLogger.LOG_LEVELERROR,
                                              '[%s] %s' % (self.__class__.__name__, str_message))

                        break
                    else:
                        n_code = EErrorCode.ERROR_OTHER_ERROR
                        str_message = 'failed to create BOM'
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
        dict_schema = {'type': 'object',
                       'properties': {
                                       "no": {'type': 'string'},
                                       "displayName": {'type': 'string'},
                                       "version": {'type': 'number'},
                                       "comment": {'type': 'string', 'blank': True},
                                       "items": {'type': 'array', 'required': True,
                                                          'items': {'type': 'object',
                                                                    'properties': {
                                                                                   "unit": {
                                                                                       'type': 'integer'},
                                                                                   "weight": {
                                                                                       'type': 'number'},
                                                                                   "material_no": {
                                                                                       'type': 'string'},
                                                                                    "material_name": {
                                                                                        'type': 'string'}
                                                                    }}}
                                      }}
        '''
        01-03 --- BOM
        04-05 --- 建立日期:年
        06-07 --- 建立日期:月
        08-10 --- 隨機
        '''
        try:
            dict_param = request.get_json()
            validictory.validate(dict_param, dict_schema)
            n_max_retries = 5
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                str_uuid = str(uuid.uuid4()).replace("-", "")
                n_nuit = 0
                f_weight = 0.0
                for dict_item in dict_param["items"]:
                    n_nuit = dict_item["unit"]
                    f_weight += dict_item["weight"]
                new_data = CTableBOM(
                    id =str_uuid,
                    no = dict_param["no"],
                    displayName=dict_param["displayName"],
                    unit=n_nuit,
                    weight=f_weight,
                    version=dict_param["version"],
                    comment=dict_param["comment"],
                    creationTime=util_retrieve_now_time(),
                )

                for n_index in range(1, n_max_retries + 1):
                    if obj_dbmgr.insert(new_data) == EErrorCode.ERROR_SUCCESS:
                        dict_extra_data = {"id": str_uuid}
                        for dict_item in dict_param["items"]:
                            str_item_uuid = str(uuid.uuid4()).replace("-", "")
                            new_item = CTableBOMItem(
                                id=str_item_uuid,
                                bom_id=str_uuid,
                                item_no=dict_item["material_no"],
                                item_name=dict_item["material_name"],
                                unit=dict_item["unit"],
                                weight=dict_item["weight"],
                                creationTime=util_retrieve_now_time()
                            )
                            if not obj_dbmgr.insert(new_item) == EErrorCode.ERROR_SUCCESS:
                                str_message = 'failed to create BOM item'
                                CLogger().log(CLogger.LOG_LEVELERROR,
                                              '[%s] %s' % (self.__class__.__name__, str_message))

                        break
                    else:
                        n_code = EErrorCode.ERROR_OTHER_ERROR
                        str_message = 'failed to create BOM'
                        CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s' % (self.__class__.__name__, str_message))
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
                    ids_query = (obj_session.query(
                        CTableBOM.id)
                                 .filter(CTableBOM.no == request.args.get("no"))
                                 )
                    ids = [id[0] for id in ids_query.all()]
                    if ids:
                        #obj_result = obj_session.query(CTableBOMItem).filter(CTableBOMItem.bom_id.in_(ids)).delete()
                        obj_delete = delete(CTableBOMItem).where(CTableBOMItem.bom_id.in_(ids))
                        obj_result = obj_session.execute(obj_delete)
                        deleted_rows = obj_result.rowcount
                        print(f"Deleted {deleted_rows} rows. (BomItem)")
                        obj_session.commit()

                    obj_delete = delete(CTableBOM).where(CTableBOM.no == request.args.get("no"))
                    obj_result = obj_session.execute(obj_delete)
                    deleted_rows = obj_result.rowcount
                    print(f"Deleted {deleted_rows} rows. (Bom)")
                    obj_session.commit()
            except Exception as error:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'throw exception (error: %s)' % str(error)
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                              % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data


    def __fill_query_params(self):
        lst_where = []

        if request.args.get('displayName'):
            lst_where.append(CTableBOM.displayName == request.args.get('displayName'))

        if request.args.get('no'):
            lst_where.append(CTableBOM.no == request.args.get('no'))
        return lst_where

    def __gen_no(self):
        from datetime import datetime
        obj_today = datetime.today()
        n_year = obj_today.year
        n_month = obj_today.month
        str_no = "BOM%02d%02d" %(n_year, n_month) + util_random_code(3)
        return str_no

    def __get_cost(self, obj_session, str_timezone, str_item_no, f_all=True):
        lst_result = []
        obj_start, obj_end = self.__get_date_range(str_timezone)

        if f_all:
            lst_obj_result = (
                obj_session.query(CTableSamplePrice)
                .filter(
                    CTableSamplePrice.item_no == str_item_no
                )
                .order_by(CTableSamplePrice.date.desc())
                .all()
            )
        else:
            lst_obj_result = (
                obj_session.query(CTableSamplePrice)
                .filter(
                    CTableSamplePrice.item_no == str_item_no,
                    CTableSamplePrice.date.between(obj_start, obj_end)
                )
                .order_by(CTableSamplePrice.date.desc())
                .all()
            )

        if lst_obj_result:
            for obj_row in lst_obj_result:
                dict_row = {}
                if obj_row:
                    dict_row = object_as_dict(obj_row)
                    dict_row.pop('date', None)
                    dict_row["date"] = int(datetime.combine(obj_row.date, time.min, tzinfo=ZoneInfo(str_timezone)).timestamp()) #obj_row.date.strftime("%Y/%m")
                lst_result.append(dict_row)
        return lst_result

    def __get_date_range(self, str_timezone):

        from dateutil.relativedelta import relativedelta

        tz = ZoneInfo(str_timezone)

        obj_today = datetime.now(tz).date()
        obj_end = obj_today.replace(day=1)

        obj_start = obj_end - relativedelta(months=12)
        return obj_start, obj_end

class CBomTree(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'results': []}

        try:
            lst_result = []

            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                if request.args.get('product_no'):
                    str_product_no = request.args.get('product_no')
                    lst_tmp = self.__gen_data(obj_session, str_product_no)
                    lst_result.extend(lst_tmp)
                else:
                    lst_prodcut = (
                        obj_session.query(CTableProduct.no)
                        .all()
                    )

                    for obj_row in lst_prodcut:
                        str_product_no = obj_row.no
                        lst_tmp = self.__gen_data(obj_session, str_product_no)
                        lst_result.extend(lst_tmp)

            dict_extra_data["total"] = len(lst_result)
            dict_extra_data["results"] = lst_result
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def __gen_data(self,obj_session, str_product_no):
        n_version = 1
        lst_version = self.__retrieve_product_version(obj_session, str_product_no)
        if lst_version:
            n_version = lst_version[-1]
        lst_tmp = CCBOMTree().retrieve(str_product_no, n_version)
        if lst_tmp:
            self.__walk_tree_for_cost(obj_session, lst_tmp )
        return lst_tmp

    def __walk_tree_for_cost(self, obj_session, lst_data, is_root=True):
        for node in lst_data:
            if is_root and node.get('category') == 5 or not is_root and node.get('category') == 4:
                obj_price = (
                    obj_session.query(
                        CTableItemPrice.estCostPriceWeight
                    )
                    .filter(CTableItemPrice.item_no == node.get('no',"") )
                    .order_by(CTableItemPrice.date.desc())
                    .first()
                )
                node["cost"] = obj_price.estCostPriceWeight if obj_price else 0
            else:
                node["cost"] = 0
            lst_children = node.get('children')
            if isinstance(lst_children, list) and lst_children:
                self.__walk_tree_for_cost(obj_session, lst_children, is_root=False)




    def __retrieve_product_version(self, obj_session, str_product_no):

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


class CProductProcess(CPrivilegeControl):
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
                    obj_session.query(CTableProductProcess)
                    .filter(*lst_where)
                    .order_by(CTableProductProcess.item_no.asc())
                    .count()
                )
                n_start = 0
                n_count = 0
                if request.args.get('start') and request.args.get('count'):
                    n_start = int(request.args.get('start'))
                    n_count = int(request.args.get('count'))

                base_query = (
                    obj_session.query(
                        CTableProductProcess
                    )
                    .options(selectinload(CTableProductProcess.flows))
                    .order_by(CTableProductProcess.no.asc())
                )
                if n_count:
                    ids = [
                        no for (no,) in (
                            obj_session.query(CTableProductProcess.no)
                            .filter(*lst_where)
                            .order_by(CTableProductProcess.item_no.asc())
                            .offset(n_start)
                            .limit(n_count)
                            .all()
                        )
                    ]

                    lst_obj_result = (
                        base_query
                        .filter(CTableProductProcess.no.in_(ids))
                        .all()
                    )
                else:
                    lst_obj_result = (
                        base_query
                        .filter(*lst_where)
                        .all()
                    )

                if lst_obj_result:
                    lst_tmp = []
                    for obj_row1 in lst_obj_result:
                        if obj_row1:
                            dict_row = object_as_dict(obj_row1)
                            str_name, n_category, n_subCategory, _, _ = util_new_get_item_info(dict_row["item_no"])
                            dict_row["name"] = str_name
                            dict_row["itemCategory"] = n_category
                            dict_row["itemSubCategory"] = n_subCategory
                            dict_row["flows"] = []
                            for obj_flow in obj_row1.flows:
                                dict_flow = object_as_dict(obj_flow)
                                dict_row["flows"].append(dict_flow)

                            lst_tmp.append(dict_row)
                    dict_extra_data['total'] = n_total
                    dict_extra_data['count'] = len(lst_tmp)
                    dict_extra_data['results'] = lst_tmp

        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def __fill_query_params(self):
        lst_where = []

        return lst_where

class CBomTree2(CPrivilegeControl):
    CATEGORY_RAW_MATERIAL = 1 #原料
    CATEGORY_MATERIAL = 2 #物料
    CATEGORY_ROLL = 3 #膠捲
    CATEGORY_INPORDUCT = 4 #在製品
    CATEGORY_PORDUCT = 5 #製成品

    PROCESS_BAKING = 1 #烘烤
    PROCESS_STUFFING = 2 #塞灌
    PROCESS_MIXING = 3 #拌料
    PROCESS_PROCESSING = 4 #加工
    PROCESS_PACKAGING =5 #包裝

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total':0, 'results': []}

        try:
            lst_result = []
            if request.args.get('product_no'):
                str_product_no = request.args.get('product_no')
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    n_version = 1
                    lst_version = self.__retrieve_product_version(obj_session, str_product_no)
                    if lst_version:
                        n_version = lst_version[-1]
                    lst_tmp = CCBOMTree().retrieve(str_product_no, n_version)
                    lst_result.extend(lst_tmp)
            dict_extra_data["total"] = len(lst_result)
            dict_extra_data["results"] = lst_result
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def __retrieve_product_version(self, obj_session, str_product_no):

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


    def __retrieve_inproduct_bom_count(self, obj_session, n_version, str_product_no):
        lst_bom = []
        lst_inproduct = []
        str_no = str_product_no + '_1'
        lst_result = (
            obj_session.query(
                CTableProductSpec
            )
            .filter(
                CTableProductSpec.product_no == str_no,
                CTableProductSpec.product_version == n_version
            )
            .all()
        )
        for obj_spec in lst_result:
            # 查詢 組規/箱規 規格
            if obj_spec.item_type == 1: #在製品; 箱規無組規
                lst_inproduct.append({"bom_no": obj_spec.bom_no,
                                      "bom_version": obj_spec.bom_version,
                                      "inproduct_no": obj_spec.item_no,
                                      "inproduct_unit": "",
                                      "inproduct_count": 0,
                                      "inproduct_per_package_unit": obj_spec.unit,
                                      "inproduct_per_package_count": obj_spec.count, #1箱幾個在製品
                                      "product_no": str_product_no,
                                      "product_version": obj_spec.product_version,
                                      "product_per_package_unit": 0,
                                      "product_per_package_count": 0})
            else:
                # 製成品
                lst_tmp = (
                    obj_session.query(
                        CTableProductSpec
                    )
                    .filter(
                        CTableProductSpec.product_no == str_product_no,
                        #CTableProductSpec.product_version == n_version,
                        CTableProductSpec.product_version == obj_spec.product_version
                    )
                    .all()
                )
                for obj_tmp in lst_tmp:
                    if obj_tmp.item_type == 1:  # 在製品; 箱規組規
                        lst_inproduct.append({"bom_no": obj_tmp.bom_no,
                                              "bom_version": obj_tmp.bom_version,
                                              "inproduct_no": obj_tmp.item_no,
                                              "inproduct_unit": "",
                                              "inproduct_count": 0,
                                              "inproduct_per_package_unit": obj_tmp.unit, # 一組幾支
                                              "inproduct_per_package_count": obj_tmp.count,
                                              "product_no": str_product_no,
                                              "product_version": obj_spec.product_version,
                                              "product_per_package_unit": obj_spec.unit, # 一箱幾罐/盒..
                                              "product_per_package_count": obj_spec.count})

        for dict_inproduct in lst_inproduct:
            lst_tmp1 = obj_session.query(
                CTableInproductBOMSpec.bom12_no,
                CTableInproductBOMSpec.count
            ).filter(
                CTableInproductBOMSpec.category == 1,
                CTableInproductBOMSpec.item_no == dict_inproduct["bom_no"],
                CTableInproductBOMSpec.item_version == dict_inproduct["bom_version"],
                CTableInproductBOMSpec.inproduct_no == dict_inproduct["inproduct_no"]
            ).all()
            lst_tmp2 = obj_session.query(
                CTableInproductBOMSpec.bom12_no
            ).filter(
                CTableInproductBOMSpec.category == 2,
                CTableInproductBOMSpec.item_no == str_product_no,
                #CTableInproductBOMSpec.item_version == n_version,
                CTableInproductBOMSpec.item_version == dict_inproduct["product_version"],
                CTableInproductBOMSpec.inproduct_no == dict_inproduct["inproduct_no"]
            ).all()
            lst_bom2 = [row.bom12_no for row in lst_tmp2] if lst_tmp2 else  []
            if lst_tmp1:
                obj_inproduct = (
                    obj_session.query(
                        CTableInproduct
                    )
                    .filter(
                        CTableInproduct.no == dict_inproduct["inproduct_no"]
                    )
                    .first()
                )
                lst_bom.append({"inproduct_no": dict_inproduct["inproduct_no"],
                                 "inproduct_name": obj_inproduct.name,
                                 "inproduct_unit": obj_inproduct.package4Unit,
                                 "inproduct_count": lst_tmp1[0].count,  # ?入/式,不是一包有幾支
                                 "inproduct_per_package_unit": obj_inproduct.package3Unit,
                                 "inproduct_per_package_count": dict_inproduct["inproduct_per_package_count"], # ?個/組
                                 "product_no": dict_inproduct["product_no"],
                                "product_version": dict_inproduct["product_version"],
                                 "product_per_package_unit": dict_inproduct["product_per_package_unit"],
                                 "product_per_package_count": dict_inproduct["product_per_package_count"], # ?組/箱
                                 "bom1_no": lst_tmp1[0].bom12_no,
                                 "bom2_no": lst_bom2})
        return lst_bom
    def __retrieve_product_bom2_count(self, obj_session, n_product_ver, str_no):
        lst_bom = []
        lst_result = (
            obj_session.query(
                CTableProductBOMSpec.bom2_no,
                CTableProductBOMSpec.count
            )
            .filter(
                CTableProductBOMSpec.product_no == str_no,
                CTableProductBOMSpec.product_version == n_product_ver
            )
            .all()
        )
        for obj_spec in lst_result:
            lst_bom.append({"product_no": str_no,
                            "bom2_no": obj_spec.bom2_no,
                            "count": obj_spec.count})
        return lst_bom
    def __retrieve_bom1(self, obj_session, n_version, str_bom1):
        lst_tree = []
        lst_all_nodes = []
        from sqlalchemy import text
        str_query =  text("""
                       WITH RECURSIVE CTE AS (
                           SELECT  parent_no,
                                   parent_name,
                                   child_category,
                                   child_id,
                                   child_name,                                  
                                   childUnit,                                  
                                   weight, 
                                   processWeight,           
                                   CONCAT(parent_name, '>', child_name) AS cte_show, 
                                   weight AS cte_weight,
                                   1 AS level
                           FROM bom1
                             WHERE parent_no = :parent_no
                           UNION ALL
                           SELECT 
                               bom1.parent_no, 
                               bom1.parent_name, 
                               bom1.child_category,
                               bom1.child_id, 
                               bom1.child_name,                               
                               bom1.childUnit,                                                                               
                               bom1.weight, 
                               bom1.processWeight, 
                               CONCAT(CTE.cte_show, '>', bom1.child_name) AS cte_show,
                               bom1.weight * CTE.cte_weight AS cte_weight,
                               CTE.level + 1
                           FROM bom1
                           JOIN CTE ON bom1.parent_no = CTE.child_id                          
                       )
                       SELECT *
                       FROM CTE
                       ORDER BY level ASC;
                   """)

        with CDBMgr().get_engine().connect() as obj_conn:
            lst_result = obj_conn.execute(str_query, {'parent_no': str_bom1, 'version': n_version})
            if lst_result:
                lst_tree, lst_all_nodes = self.__convert1(obj_session, lst_result)
        return lst_tree, lst_all_nodes

    def __retrieve_bom2(self, n_version, str_bom2):
        lst_tree = []
        lst_all_nodes = []

        from sqlalchemy import text
        str_query = text("""
                       WITH RECURSIVE CTE AS (
                           SELECT  parent_no,
                                    parent_name,
                                    child_category,
                                    child_id,
                                    child_name,                                 
                                    childUnit,
                                    weight,                                   
                                    childUnit2,
                                    length,
                                    count,
                                    processCount,
                                    CONCAT(parent_name, '>', child_name) AS cte_show, 
                                    weight AS cte_weight,
                                    1 AS level
                           FROM bom2
                           WHERE parent_no = :parent_no
                                                       
                           UNION ALL
                            SELECT 
                                    bom2.parent_no, 
                                    bom2.parent_name, 
                                    bom2.child_category,
                                    bom2.child_id, 
                                    bom2.child_name, 
                                    bom2.childUnit, 
                                    bom2.count, 
                                    bom2.processCount, 
                                    bom2.childUnit2, 
                                    bom2.length, 
                                    bom2.weight, CONCAT(CTE.cte_show, '>', bom2.child_name) AS cte_show,
                                    bom2.weight * CTE.cte_weight AS cte_weight,
                                    CTE.level + 1
                           FROM bom2
                           JOIN CTE ON bom2.parent_no = CTE.child_id      
                                                     
                       )
                       SELECT *
                       FROM CTE
                       ORDER BY level ASC;
                   """)
        with CDBMgr().get_engine().connect() as obj_conn:
            lst_result = obj_conn.execute(str_query, {'parent_no': str_bom2, 'version': n_version})
            if lst_result:
                lst_tree, lst_all_nodes = self.__convert2(lst_result)
        return lst_tree, lst_all_nodes
    '''
    def __retrieve_bom2(self, n_date, str_bom2):
        lst_tree = []
        lst_all_nodes = []

        from sqlalchemy import text
        str_query = """
                       WITH RECURSIVE CTE AS (
                           SELECT version,
                                  parent_no,
                                    parent_name,
                                    child_category,
                                    child_id,
                                    child_name,
                                    child_version,
                                    childUnit,
                                    weight,                                   
                                    childUnit2,
                                    length,
                                    count,
                                    processCount,
                                    CONCAT(parent_name, '>', child_name) AS cte_show, 
                                    weight AS cte_weight,
                                    1 AS level
                           FROM bom2
                           WHERE parent_no = '{}'                                 
                           UNION ALL
                            SELECT bom2.version, 
                                    bom2.parent_no, 
                                    bom2.parent_name, 
                                    bom2.child_category,
                                    bom2.child_id, 
                                    bom2.child_name, 
                                    bom2.child_version,
                                    bom2.childUnit, 
                                    bom2.count, 
                                    bom2.processCount, 
                                    bom2.childUnit2, 
                                    bom2.length, 
                                    bom2.weight, CONCAT(CTE.cte_show, '>', bom2.child_name) AS cte_show,
                                    bom2.weight * CTE.cte_weight AS cte_weight,
                                    CTE.level + 1
                           FROM bom2
                           JOIN CTE ON bom2.parent_no = CTE.child_id                           
                       )
                       SELECT *
                       FROM CTE
                       ORDER BY version DESC, level ASC;
                   """.format(str_bom2)
        with CDBMgr().get_engine().connect() as obj_conn:
            lst_result = obj_conn.execute(text(str_query))
            if lst_result:
                lst_tree, lst_all_nodes = self.__convert2(lst_result)
        return lst_tree, lst_all_nodes
    '''
    def __build_tree(self, dict_tree, lst_nodes, n_level=1):
        lst_result = []
        for obj_node in lst_nodes:
            lst_children = self.__build_tree(dict_tree, dict_tree[n_level + 1], n_level + 1) if (
                                                                                                     n_level + 1) in dict_tree else []
            obj_node['children'] = [child for child in lst_children if child['parent_no'] == obj_node['child_id']]
            lst_result.append(obj_node)
        return lst_result

    def __convert1(self, obj_session, lst_result):
        from collections import defaultdict
        dict_tree = defaultdict(list)
        # 将结果存储到字典中
        for row in lst_result:
            parent_no, parent_name, child_category, child_id, child_name, childUnit, weight, processWeight, cte_show, cte_weight, level = row
            #print(row)
            dict_inproduct = obj_session.query(
                CTableInproductBOMSpec
            ).filter(
                CTableInproductBOMSpec.category == 1,
                CTableInproductBOMSpec.bom12_no == child_id
            ).first()
            print("")
            # 将数据存储到相应的层级
            dict_node = {
                'parent_no': parent_no,
                'parent_name': parent_name,
                'child_category': child_category,
                'child_id': child_id,
                'child_name': child_name,
                'childUnit': childUnit,
                'weight': weight,
                'processWeight': processWeight,
                'cte_show': cte_show,
                'cte_weight': cte_weight,
                'level': level,
                'process': dict_inproduct.inproduct_data.category if dict_inproduct else 0,
                'children': []
            }
            dict_tree[level].append(dict_node)
        lst_tree = self.__build_tree(dict_tree, dict_tree[1])
        lst_leaf_nodes = []
        lst_all_nodes = []

        for obj_node in lst_tree:
            lst_empty = []
            #self.__cal_parent_node_weight(obj_node)
            #lst_tmp = self.__get_leaf_nodes(obj_node)
            #lst_leaf_nodes.extend(lst_tmp)
            _, lst_tmp2 = self.__cal_node_weight(obj_node, lst_empty)
            lst_all_nodes.extend(lst_tmp2)
        return lst_tree, lst_all_nodes

    def __convert2(self,lst_result):
        from collections import defaultdict
        dict_tree = defaultdict(list)
        # 将结果存储到字典中
        for row in lst_result:
            parent_no, parent_name, child_category, child_id, child_name, childUnit, weight, childUnit2, length, count, processCount, cte_show, cte_weight, level = row
            # 将数据存储到相应的层级
            dict_node = {
                'parent_no': parent_no,
                'parent_name': parent_name,
                'child_category': child_category,
                'child_id': child_id,
                'child_name': child_name,
                'childUnit': childUnit,
                'weight': weight,
                'processCount': processCount,
                'childUnit2': childUnit2,
                'length': length,
                'count': count,
                'cte_show': cte_show,
                'cte_weight': cte_weight,
                'level': level,
                'process':0,
                'children': []
            }
            dict_tree[level].append(dict_node)
        lst_tree = self.__build_tree(dict_tree, dict_tree[1])
        lst_leaf_nodes = []
        lst_all_nodes = []
        for obj_node in lst_tree:
            lst_empty = []
            lst_tmp = self.__get_leaf_nodes(obj_node)
            lst_leaf_nodes.extend(lst_tmp)
            _, lst_tmp2 = self.__cal_node_weight(obj_node, lst_empty)
            lst_all_nodes.extend(lst_tmp2)
        return lst_tree, lst_all_nodes

    def __get_leaf_nodes(self, obj_node, level=0):
        lst_leaf_nodes = []
        if not obj_node['children']:  # 只有在没有子节点时才将其添加到列表中
            lst_leaf_nodes.append(obj_node)

            '''
            lst_leaf_nodes.append({
                    "parent_no": obj_node['parent_no'], "name": obj_node['child_name'], "category": obj_node['child_category'], "unit": obj_node['childUnit'], "weight": obj_node['cte_weight']})
            '''
        else:
            for child in obj_node['children']:
                lst_leaf_nodes.extend(self.__get_leaf_nodes(child, level + 1))
        return lst_leaf_nodes

    def __cal_parent_node_weight(self, obj_node):
        if not obj_node['children']:  # 如果沒有子節點，返回自己的 weight
            obj_node['new_weight'] = obj_node['weight']
            return obj_node['new_weight']
        else:
            f_total_weight = 0.0
            for child in obj_node['children']:
                f_total_weight += self.__cal_parent_node_weight(child)  # 累加子節點的 new_weight
            obj_node['new_weight'] = f_total_weight
            return obj_node['new_weight']



    def __cal_node_weight(self, obj_node, lst_all_nodes, dict_parent_node=None, level=0):
        """
        計算節點權重，子節點需要檢查其母節點的 childUnit 是否為 150，並根據母節點的 weight 進行加權計算
        """
        # 如果沒有子節點，則處理當前節點的 weight
        if not obj_node['children']:
            # 如果母節點存在且母節點的 childUnit 為 150，則進行加權計算
            obj_node['new_weight'] = obj_node['weight']
            '''
            if dict_parent_node and dict_parent_node['child_category'] == 2:
                obj_node['new_weight'] = round(obj_node['weight'] * dict_parent_node['weight'], 2)
            else:
                obj_node['new_weight'] = obj_node['weight']
            '''
            # 將當前節點加入節點列表
            lst_all_nodes.append(obj_node)
            return obj_node['new_weight'], lst_all_nodes

        n_total = 0.0
        lst_child_weights = []

        # 遍歷所有子節點，計算子節點的權重，並檢查母節點的 childUnit 是否為 150
        for obj_child in obj_node['children']:
            f_child_weight, lst_all_nodes = self.__cal_node_weight(
                obj_child, lst_all_nodes, obj_node, level + 1
            )
            n_total += f_child_weight
            lst_child_weights.append(f_child_weight)  # 記錄子節點的權重

        # 處理母節點的權重

        obj_node['new_weight'] = round(n_total, 2)
        obj_node['child_weights'] = lst_child_weights
        # 將母節點加入節點列表
        lst_all_nodes.append(obj_node)
        return obj_node['new_weight'], lst_all_nodes

    def __gen_bom1_dict(self, dict_node):
        if dict_node["child_category"] == 2:
            dict_tmp = {"category": self.CATEGORY_INPORDUCT,
                        "no": dict_node["child_id"],
                        "name": dict_node["child_name"],
                        "count_unit": unit_to_string(dict_node["childUnit"]),
                        "count": int(dict_node["weight"] / dict_node["new_weight"]),  # dict_node["weight"],
                        "unit": unit_to_string(EUnit.GRAM),
                        "weight": dict_node["new_weight"],  # dict_node["new_weight"],
                        "total_weight": dict_node["weight"],  # dict_node["new_weight"],
                        "process": self.__convert_process(dict_node["process"]),
                        "children": []}
            # 遞迴處理每個子節點
            for dict_data in dict_node['children']:
                dict_child = self.__gen_bom1_dict(dict_data)  # 遞迴處理子節點
                dict_tmp["children"].append(dict_child)  # 將結果放到children裡
        else:
            dict_tmp = {"category": self.CATEGORY_RAW_MATERIAL,
                        "no": dict_node["child_id"],
                        "name": dict_node["child_name"],
                        "count_unit": unit_to_string(EUnit.ITEM),
                        "count": 1,
                        "unit": unit_to_string(dict_node["childUnit"]),
                        "weight": dict_node["new_weight"],
                        "total_weight": 1 * dict_node["new_weight"],
                        "process": self.__convert_process(dict_node["process"])}

        return dict_tmp

    def __gen_bom2_dict(self, dict_node):
        dict_tmp = {"category": self.CATEGORY_MATERIAL if dict_node['child_category'] ==1 else self.CATEGORY_ROLL ,
                    "no": dict_node["child_id"],
                    "name": dict_node["child_name"],
                    "count_unit": unit_to_string(EUnit.ITEM),
                    "count": dict_node["count"],
                    "unit": unit_to_string(dict_node["childUnit"]),
                    "weight": dict_node["new_weight"],
                    "total_weight": dict_node["count"]*dict_node["new_weight"],
                    #"total_weight": dict_node["new_weight"],
                    "unit2": unit_to_string(dict_node["childUnit2"]),
                    "length": dict_node["length"],
                    "total_length": dict_node["count"]*dict_node["length"]
                    #"total_length": dict_node["length"]
                    }
        return dict_tmp

    def __convert_process(self, n_data):
        n_processs = 0
        if n_data == 2:
            n_processs = self.PROCESS_MIXING
        elif n_data == 3:
            n_processs = self. PROCESS_STUFFING
        elif n_data == 4:
            n_processs = self.PROCESS_BAKING

        return n_processs



class CBomAPS(CPrivilegeControl):
    CATEGORY_RAW_MATERIAL = 1 #原料
    CATEGORY_MATERIAL = 2 #物料
    CATEGORY_ROLL = 3 #膠捲
    CATEGORY_INPORDUCT = 4 #在製品
    CATEGORY_PORDUCT = 5 #製成品

    PROCESS_BAKING = 1 #烘烤
    PROCESS_STUFFING = 2 #塞灌
    PROCESS_MIXING = 3 #拌料
    PROCESS_PROCESSING = 4 #加工
    PROCESS_PACKAGING =5 #包裝

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'results': []}

        try:
            if request.args.get('product_no'):
                str_product_no = request.args.get('product_no')
                str_order_no = request.args.get('order_no')
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    obj_order = (
                        obj_session.query(
                            CTableProductOrder
                        )
                        .filter(CTableProductOrder.no == str_order_no)
                        .first()
                    )

                    lst_bom = CCBOMTree().retrieve(str_product_no, 1)
                    self.save_bom_recursive(obj_dbmgr, obj_order, lst_bom[0])

                dict_extra_data["results"] = CCBOMTree().retrieve(str_product_no, 1)
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def __convert_proc(self, n_value):
        n_proc = 0
        if n_value in [EBomProc.PROCESS_BAKING, EBomProc.PROCESS_STUFFING, EBomProc.PROCESS_MIXING]:
            n_proc = EProcCategory.PREPROCESS
        elif n_value == EBomProc.PROCESS_PROCESSING:
            n_proc = EProcCategory.PROCESS
        elif n_value == EBomProc.PROCESS_PACKAGING:
            n_proc = EProcCategory.PACKAGE
        return n_proc

    def save_bom_recursive(self, obj_dbmgr, obj_order, node):
        obj_session = obj_dbmgr.get_session()

        # 母節點資訊
        parent_no = node["no"]
        parent_name = node.get("name", "")
        parent_process = self.__convert_proc(node.get("process", 0))

        # 先處理子節點
        children = node.get("children", [])
        if children:# or node["category"] in [EItemCategory.INPRODUCT, EItemCategory.PRODUCT]:
            # 建立 BOM（如果還沒建立）
            bom = obj_session.query(CTableAPSQuantity).filter_by(
                product_order_no=obj_order.no,
                oneProcess=parent_process,
                item_no=parent_no
            ).first()
            if not bom:
                print("父節點", parent_process, parent_no, parent_name)
                str_item_uuid = str(uuid.uuid4()).replace("-", "")
                new_data = CTableAPSQuantity(
                    id = str_item_uuid,
                    product_order_no=obj_order.no,
                    product_order_count = obj_order.count,
                    Product_order_expectedDate = 0,
                    oneProcess = parent_process,
                    item_no = parent_no,
                    item_name = parent_name,
                    itemCategory = node["category"],
                    count = node["total_weight"],
                    unit = node["unit"],
                    minutes = 0,
                    laborCount = 0,
                    creationTime=util_retrieve_now_time()
                )
                obj_dbmgr.insert(new_data)


            # 建立與子項的連結（如果有子項）
            for child in children:
                child_no = child["no"]
                child_name = child.get("name", "")

                child_children = child.get("children", [])
                if child_children:
                    # 子節點自己是母品，不要加到 CTableBOMItem，直接遞迴
                    self.save_bom_recursive(obj_dbmgr, obj_order, child)
                    print(" 節點", child_no, child_name)
                else:
                    # 檢查是否已存在這個 parent-child 關係
                    existing = obj_session.query(CTableAPSQuantityItem).filter_by(
                        product_order_no=obj_order.no,
                        output_item_no=parent_no,
                        oneProcess=parent_process,
                        item_no=child_no
                    ).first()

                    if not existing:
                        str_item_uuid = str(uuid.uuid4()).replace("-", "")
                        obj_item = CTableAPSQuantityItem(
                            id=str_item_uuid,
                            product_order_no=obj_order.no,
                            output_item_no=parent_no,
                            oneProcess=parent_process,
                            item_no =child_no,
                            item_name=child_name,
                            itemCategory=child["category"],
                            count=child["total_weight"],
                            unit=child["unit"]

                        )
                        obj_dbmgr.insert(obj_item)


