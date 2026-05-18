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
import uuid
from package.util.util import *
from sqlalchemy import literal, union_all
from collections import defaultdict


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


class CMixItem(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0,'results': []}

        try:
            n_start = 0
            n_count = 0
            n_total = 0
            if request.args.get('start') and request.args.get('count'):
                n_start = int(request.args.get("start", 0))
                n_count = int(request.args.get("count", 20))

            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                q_inproduct = obj_session.query(
                    CTableInproduct.no.label("no"),
                    CTableInproduct.name.label("name"),
                    literal(EItemCategory.INPRODUCT).label("category"),
                    literal(0).label("subCategory"),
                    CTableInproduct.unitWarehouse.label("unitWarehouse"),
                    CTableInproduct.unitProduct.label("unitProduct")
                )

                q_product = obj_session.query(
                    CTableProduct.no.label("no"),
                    CTableProduct.name.label("name"),
                    literal(EItemCategory.PRODUCT).label("category"),
                    CTableProduct.category.label("subCategory"),
                    CTableProduct.unitWarehouse.label("unitWarehouse"),
                    CTableProduct.unitProduct.label("unitProduct")
                )
                union_subq = union_all(q_inproduct, q_product).subquery()
                lst_obj_rows = (
                    obj_session.query(union_subq)
                    .order_by(union_subq.c.no.asc())
                    .limit(n_count)
                    .offset(n_start)
                    .all()
                )
                n_total = obj_session.query(func.count()).select_from(union_subq).scalar()

                lst_result = []
                for obj_row in lst_obj_rows:
                    dict_bom = {}
                    if obj_row.category == EItemCategory.PRODUCT:
                        dict_bom = self.__get_product_bom(obj_session, obj_row.no)
                    else:
                        dict_bom = self.__get_inproduct_bom(obj_session, obj_row.no)
                    dict_data = {
                        "no": obj_row.no,
                        "name": obj_row.name,
                        "category": obj_row.category,
                        "subCategory": obj_row.subCategory,
                        "unitWarehouse": obj_row.unitWarehouse,
                        "unitProduct": obj_row.unitProduct,
                        "bom": dict_bom
                    }

                    lst_result.append(dict_data)

                dict_extra_data["total"] = n_total
                dict_extra_data["count"] = len(lst_result)
                dict_extra_data["results"] = lst_result
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def __get_product_bom(self, obj_session, str_item_no):
        try:
            obj_ver = (
                obj_session.query(CTableProductVer)
                .filter( CTableProductVer.item_no == str_item_no)
                .order_by(CTableProductVer.date.desc())
                .first()
            )
            # 取得內容物淨重+單位
            str_item_no_box = str_item_no+ '_1'
            obj_result = (
                obj_session.query(
                    func.sum(CTableProductSpec.weight).label('total_weight'),
                    CTableProductSpec.unit
                )
                .filter(
                    CTableProductSpec.product_no == str_item_no_box,
                    CTableProductSpec.product_version == obj_ver.version
                )
                .group_by(CTableProductSpec.unit)  # 依照單位分組，確保能抓到 unit
                .first()
            )

            # 取得物料
            n_bom2Weight = (
                obj_session.query(
                    func.sum(CTableProductBOMSpec.weight).label('total_weight')
                )
                .filter(
                    CTableProductBOMSpec.product_no == str_item_no_box,
                    CTableProductBOMSpec.product_version == obj_ver.version
                )
                .scalar() or 0
            )
            n_netWeight = obj_result.total_weight if obj_result else 0

            n_grossWeight = n_netWeight + n_bom2Weight
            dict_bom = {
                "assemblyNo": obj_ver.no if obj_ver else "",
                "version": obj_ver.version if obj_ver else 0,
                "date": obj_ver.date if obj_ver else 0,
                "unit": obj_result.unit if obj_result else 0,
                "netWeight": n_netWeight,
                "grossWeight": n_grossWeight,
            }
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return dict_bom

    def __get_inproduct_bom(self, obj_session, str_item_no):
        try:

            # 取得內容物淨重+單位
            n_version = 1
            lst_result = (
                obj_session.query(
                    CTableInproductBOMSpec.item_no,
                    CTableInproductBOMSpec.weight,
                    CTableInproductBOMSpec.unit
                )
                .filter(
                    CTableInproductBOMSpec.inproduct_no == str_item_no,
                    CTableInproductBOMSpec.category == EBomCategory.PM,
                    CTableInproductBOMSpec.item_version == n_version  # 關鍵：指定版本
                )
                .group_by(CTableInproductBOMSpec.unit)  # 必須加上 group_by
                .all()
            )
            n_netWeight = 0
            n_unit = 0
            for obj_result in lst_result:
                n_netWeight = obj_result.weight
                n_unit = obj_result.unit
                if obj_result.item_no == "":
                    break

            # 取得物料
            n_bom2Weight = (
                obj_session.query(
                    func.sum(CTableProductBOMSpec.weight).label('total_weight')
                )
                .filter(
                    CTableInproductBOMSpec.inproduct_no == str_item_no,
                    CTableInproductBOMSpec.category == EBomCategory.MA_AP
                )
                .scalar() or 0
            )

            n_grossWeight = n_netWeight + n_bom2Weight
            dict_bom = {
                "assemblyNo": "",
                "version": 0,
                "date": 0,
                "unit": n_unit,
                "netWeight": n_netWeight,
                "grossWeight": n_grossWeight,
            }
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return dict_bom
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
                            "estPrice1": obj_price.estCostPriceLength1 if obj_price.costUnitLength else obj_price.estCostPriceWeight1,
                            "estPrice2": obj_price.estCostPriceLength2 if obj_price.costUnitLength else obj_price.estCostPriceWeight2,
                            "estLaborCost": obj_price.estLaborCost,
                            "unit": obj_price.costUnitLength if obj_price.costUnitLength else obj_price.costUnitWeight,
                            "price": obj_price.costPriceLength if obj_price.costUnitLength else obj_price.costPriceWeight,
                            "price1": obj_price.costPriceLength1 if obj_price.costUnitLength else obj_price.costPriceWeight1,
                            "price2": obj_price.costPriceLength2 if obj_price.costUnitLength else obj_price.costPriceWeight2,
                            "laborCost": obj_price.laborCost,
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

