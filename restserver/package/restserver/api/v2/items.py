# coding=utf8
import time
from collections import defaultdict

from flask import request
from sqlalchemy import or_

from package.common.common import (
    EBatchRiskLevelCode,
    EErrorCode,
    EItemCategory,
    EItemMaintenanceRiskCode,
    EItemMaintenanceSuggestionTypeCode,
    EItemMasterStatusCode,
)
from package.dbwrapper.dbmgr import CDBMgr
from package.dbwrapper.table import (
    CTableBOM,
    CTableBOMItem,
    CTableBatchNumber,
    CTableGoods,
    CTableInproduct,
    CTableInproductBOMSpec,
    CTableMaterial,
    CTableProduct,
    CTableProductBOMSpec,
    CTableProductSpec,
)
from package.log.log import CLogger
from package.restserver.api.v2.warehouse import CWarehouseInventoryContextBuilder
from package.util.util import util_round_quantity, util_safe_float, util_safe_int


class CItemCenterService(object):
    MAX_RECENT_BATCHES = 20

    def get_dashboard(
        self,
        n_date=0,
        str_timezone="",
        str_keyword="",
        n_item_category=0,
        n_item_sub_category=0,
        str_master_status_code="",
        b_has_stock=False,
        b_has_bom=False,
        n_start=0,
        n_count=50,
    ):
        with CDBMgr() as obj_dbmgr:
            return self.__get_dashboard_with_session(
                obj_dbmgr.get_session(),
                n_date,
                str_timezone,
                str_keyword,
                n_item_category,
                n_item_sub_category,
                str_master_status_code,
                b_has_stock,
                b_has_bom,
                n_start,
                n_count,
            )

    def get_detail(self, str_item_no, n_date=0, str_timezone=""):
        with CDBMgr() as obj_dbmgr:
            return self.__get_detail_with_session(obj_dbmgr.get_session(), str_item_no, n_date, str_timezone)

    def __get_dashboard_with_session(
        self,
        obj_session,
        n_date,
        str_timezone,
        str_keyword,
        n_item_category,
        n_item_sub_category,
        str_master_status_code,
        b_has_stock,
        b_has_bom,
        n_start,
        n_count,
    ):
        n_query_timestamp = util_safe_int(n_date) or util_safe_int(time.time())
        n_start, n_count = self.__normalize_page(n_start, n_count)
        lst_items = self.__build_item_rows(obj_session)
        dict_inventory = self.__build_inventory_summary_by_item(obj_session, n_query_timestamp, str_timezone)
        dict_bom = self.__build_bom_summary_by_item(obj_session)
        dict_recent_batch_counts = self.__query_recent_batch_counts(obj_session)
        lst_rows = [
            self.__build_dashboard_row(dict_item, dict_inventory, dict_bom, dict_recent_batch_counts)
            for dict_item in lst_items
        ]
        lst_rows = self.__filter_rows(
            lst_rows,
            str_keyword,
            n_item_category,
            n_item_sub_category,
            str_master_status_code,
            b_has_stock,
            b_has_bom,
        )
        lst_rows = self.__sort_rows(lst_rows)
        n_total = len(lst_rows)
        lst_page = lst_rows[n_start:n_start + n_count]
        return {
            "serverTimestamp": n_query_timestamp,
            "summary": self.__build_summary(lst_rows),
            "categorySummary": self.__build_category_summary(lst_rows),
            "items": lst_page,
            "maintenanceSuggestions": self.__build_maintenance_suggestions(lst_rows),
            "total": n_total,
            "start": n_start,
            "count": len(lst_page),
        }

    def __get_detail_with_session(self, obj_session, str_item_no, n_date, str_timezone):
        str_item_no = (str_item_no or "").strip()
        if not str_item_no:
            return None
        n_query_timestamp = util_safe_int(n_date) or util_safe_int(time.time())
        lst_items = [dict_item for dict_item in self.__build_item_rows(obj_session) if dict_item.get("itemNo") == str_item_no]
        if not lst_items:
            return None
        dict_item = lst_items[0]
        dict_inventory = self.__build_inventory_summary_by_item(obj_session, n_query_timestamp, str_timezone, str_item_no)
        dict_bom = self.__build_bom_summary_by_item(obj_session, str_item_no)
        dict_recent_batch_counts = self.__query_recent_batch_counts(obj_session, str_item_no)
        dict_row = self.__build_dashboard_row(dict_item, dict_inventory, dict_bom, dict_recent_batch_counts)
        return {
            "serverTimestamp": n_query_timestamp,
            "item": self.__build_item_detail(dict_row),
            "inventorySummary": self.__build_inventory_detail_summary(dict_inventory.get(str_item_no, {})),
            "bomUsage": self.__query_bom_usage(obj_session, str_item_no),
            "recentBatches": self.__query_recent_batches(obj_session, str_item_no, n_query_timestamp, dict_inventory),
            "maintenanceSuggestions": [
                self.__build_maintenance_suggestion(dict_row)
            ] if dict_row.get("masterStatusCode") == EItemMasterStatusCode.MAINTENANCE_NEEDED else [],
        }

    def __build_item_rows(self, obj_session):
        lst_rows = []
        for obj_row in obj_session.query(CTableMaterial).all():
            lst_rows.append(self.__item_row(
                obj_row,
                util_safe_int(obj_row.category),
                util_safe_int(obj_row.subCategory),
            ))
        for obj_row in obj_session.query(CTableInproduct).all():
            lst_rows.append(self.__item_row(
                obj_row,
                EItemCategory.INPRODUCT,
                util_safe_int(obj_row.category),
            ))
        for obj_row in obj_session.query(CTableProduct).all():
            lst_rows.append(self.__item_row(
                obj_row,
                EItemCategory.PRODUCT,
                util_safe_int(obj_row.category),
            ))
        for obj_row in obj_session.query(CTableGoods).all():
            lst_rows.append(self.__item_row(
                obj_row,
                EItemCategory.GOODS,
                util_safe_int(obj_row.subCategory),
            ))
        return lst_rows

    def __item_row(self, obj_row, n_item_category, n_item_sub_category):
        return {
            "itemNo": obj_row.no or "",
            "itemName": obj_row.name or "",
            "itemCategory": util_safe_int(n_item_category),
            "itemSubCategory": util_safe_int(n_item_sub_category),
            "unitWarehouse": util_safe_int(getattr(obj_row, "unitWarehouse", 0)),
            "unitProduct": util_safe_int(getattr(obj_row, "unitProduct", 0)),
            "creationTime": util_safe_int(getattr(obj_row, "creationTime", 0)),
        }

    def __build_inventory_summary_by_item(self, obj_session, n_query_timestamp, str_timezone, str_item_no=""):
        obj_context_builder = CWarehouseInventoryContextBuilder()
        return obj_context_builder.query_item_inventory_summary(
            obj_session=obj_session,
            n_query_timestamp=n_query_timestamp,
            n_item_category=0,
            str_item_no=str_item_no,
        )

    def __build_bom_summary_by_item(self, obj_session, str_item_no=""):
        lst_item_nos = [str_item_no] if str_item_no else None
        dict_result = defaultdict(lambda: {"bomCount": 0, "_keys": set()})
        self.__append_bom_item_counts(obj_session, dict_result, lst_item_nos)
        self.__append_product_spec_counts(obj_session, dict_result, lst_item_nos)
        self.__append_product_bom_spec_counts(obj_session, dict_result, lst_item_nos)
        self.__append_inproduct_bom_spec_counts(obj_session, dict_result, lst_item_nos)
        for dict_row in dict_result.values():
            dict_row["bomCount"] = len(dict_row.pop("_keys"))
        return dict_result

    def __append_bom_item_counts(self, obj_session, dict_result, lst_item_nos):
        obj_query = obj_session.query(CTableBOMItem)
        if lst_item_nos:
            obj_query = obj_query.filter(CTableBOMItem.item_no.in_(lst_item_nos))
        for obj_row in obj_query.all():
            dict_result[obj_row.item_no or ""]["_keys"].add("bom_item:%s" % (obj_row.bom_no or ""))

    def __append_product_spec_counts(self, obj_session, dict_result, lst_item_nos):
        obj_query = obj_session.query(CTableProductSpec)
        if lst_item_nos:
            obj_query = obj_query.filter(or_(
                CTableProductSpec.product_no.in_(lst_item_nos),
                CTableProductSpec.item_no.in_(lst_item_nos),
                CTableProductSpec.bom_no.in_(lst_item_nos),
            ))
        for obj_row in obj_query.all():
            if obj_row.product_no:
                dict_result[obj_row.product_no]["_keys"].add("product_spec_owner:%s:%s" % (obj_row.bom_no or "", util_safe_int(obj_row.bom_version)))
            str_item_no = obj_row.item_no or ""
            if str_item_no:
                dict_result[str_item_no]["_keys"].add("product_spec:%s:%s" % (obj_row.product_no or "", util_safe_int(obj_row.product_version)))

    def __append_product_bom_spec_counts(self, obj_session, dict_result, lst_item_nos):
        obj_query = obj_session.query(CTableProductBOMSpec)
        if lst_item_nos:
            obj_query = obj_query.filter(or_(
                CTableProductBOMSpec.product_no.in_(lst_item_nos),
                CTableProductBOMSpec.bom2_no.in_(lst_item_nos),
            ))
        for obj_row in obj_query.all():
            if obj_row.product_no:
                dict_result[obj_row.product_no]["_keys"].add("product_bom_spec_owner:%s:%s" % (obj_row.bom2_no or "", util_safe_int(obj_row.product_version)))
            dict_result[obj_row.bom2_no or ""]["_keys"].add("product_bom_spec:%s:%s" % (obj_row.product_no or "", util_safe_int(obj_row.product_version)))

    def __append_inproduct_bom_spec_counts(self, obj_session, dict_result, lst_item_nos):
        obj_query = obj_session.query(CTableInproductBOMSpec)
        if lst_item_nos:
            obj_query = obj_query.filter(or_(CTableInproductBOMSpec.inproduct_no.in_(lst_item_nos), CTableInproductBOMSpec.item_no.in_(lst_item_nos), CTableInproductBOMSpec.bom12_no.in_(lst_item_nos)))
        for obj_row in obj_query.all():
            if obj_row.inproduct_no:
                dict_result[obj_row.inproduct_no]["_keys"].add("inproduct_bom_spec:%s" % util_safe_int(obj_row.id))
            if obj_row.item_no:
                dict_result[obj_row.item_no]["_keys"].add("inproduct_bom_spec:%s" % util_safe_int(obj_row.id))
            if obj_row.bom12_no:
                dict_result[obj_row.bom12_no]["_keys"].add("inproduct_bom_spec:%s" % util_safe_int(obj_row.id))

    def __query_recent_batch_counts(self, obj_session, str_item_no=""):
        obj_query = obj_session.query(CTableBatchNumber)
        if str_item_no:
            obj_query = obj_query.filter(CTableBatchNumber.item_no == str_item_no)
        dict_result = defaultdict(set)
        for obj_row in obj_query.all():
            if obj_row.item_no and obj_row.no:
                dict_result[obj_row.item_no].add(obj_row.no)
        return {
            str_item_no: len(set_batch_nos)
            for str_item_no, set_batch_nos in dict_result.items()
        }

    def __build_dashboard_row(self, dict_item, dict_inventory, dict_bom, dict_recent_batch_counts):
        str_item_no = dict_item.get("itemNo", "")
        dict_stock = dict_inventory.get(str_item_no, {})
        dict_bom_summary = dict_bom.get(str_item_no, {})
        n_batch_count = max(
            util_safe_int(dict_stock.get("batchCount")),
            util_safe_int(dict_recent_batch_counts.get(str_item_no)),
        )
        dict_status = self.__evaluate_master_status(dict_item, dict_stock, dict_bom_summary, n_batch_count)
        return {
            "itemNo": str_item_no,
            "itemName": dict_item.get("itemName", ""),
            "itemCategory": util_safe_int(dict_item.get("itemCategory")),
            "itemSubCategory": util_safe_int(dict_item.get("itemSubCategory")),
            "unitWarehouse": util_safe_int(dict_item.get("unitWarehouse")),
            "unitProduct": util_safe_int(dict_item.get("unitProduct")),
            "masterStatusCode": dict_status.get("masterStatusCode"),
            "maintenanceRiskCode": dict_status.get("maintenanceRiskCode"),
            "hasStock": util_safe_float(dict_stock.get("currentQuantity")) > 0,
            "currentQuantity": util_round_quantity(dict_stock.get("currentQuantity")),
            "batchCount": n_batch_count,
            "bomCount": util_safe_int(dict_bom_summary.get("bomCount")),
            "creationTime": util_safe_int(dict_item.get("creationTime")),
        }

    def __evaluate_master_status(self, dict_item, dict_stock, dict_bom, n_batch_count):
        str_risk = EItemMaintenanceRiskCode.NORMAL
        n_item_category = util_safe_int(dict_item.get("itemCategory"))
        if not util_safe_int(dict_item.get("unitWarehouse")):
            str_risk = EItemMaintenanceRiskCode.MISSING_UNIT
        elif n_item_category in [EItemCategory.INPRODUCT, EItemCategory.PRODUCT] and not util_safe_int(dict_bom.get("bomCount")):
            str_risk = EItemMaintenanceRiskCode.MISSING_BOM
        elif n_item_category in [EItemCategory.PM, EItemCategory.MA, EItemCategory.AF] and not util_safe_float(dict_stock.get("currentQuantity")) and not util_safe_int(n_batch_count):
            str_risk = EItemMaintenanceRiskCode.MISSING_STOCK_SIGNAL
        return {
            "masterStatusCode": EItemMasterStatusCode.READY if str_risk == EItemMaintenanceRiskCode.NORMAL else EItemMasterStatusCode.MAINTENANCE_NEEDED,
            "maintenanceRiskCode": str_risk,
        }

    def __filter_rows(
        self,
        lst_rows,
        str_keyword,
        n_item_category,
        n_item_sub_category,
        str_master_status_code,
        b_has_stock,
        b_has_bom,
    ):
        str_keyword = (str_keyword or "").strip().lower()
        lst_results = []
        for dict_row in lst_rows:
            if n_item_category and util_safe_int(dict_row.get("itemCategory")) != n_item_category:
                continue
            if n_item_sub_category and util_safe_int(dict_row.get("itemSubCategory")) != n_item_sub_category:
                continue
            if str_master_status_code and dict_row.get("masterStatusCode") != str_master_status_code:
                continue
            if b_has_stock and not dict_row.get("hasStock"):
                continue
            if b_has_bom and util_safe_int(dict_row.get("bomCount")) <= 0:
                continue
            if str_keyword and not self.__matches_keyword(dict_row, str_keyword):
                continue
            lst_results.append(dict_row)
        return lst_results

    def __matches_keyword(self, dict_row, str_keyword):
        return any(str_keyword in (str(dict_row.get(str_key, ""))).lower() for str_key in [
            "itemNo",
            "itemName",
        ])

    def __sort_rows(self, lst_rows):
        return sorted(
            lst_rows,
            key=lambda dict_row: (
                0 if dict_row.get("masterStatusCode") == EItemMasterStatusCode.MAINTENANCE_NEEDED else 1,
                self.__item_category_sort(util_safe_int(dict_row.get("itemCategory"))),
                dict_row.get("itemNo", ""),
            ),
        )

    def __build_summary(self, lst_rows):
        return {
            "totalItemCount": len(lst_rows),
            "activeItemCount": len(lst_rows),
            "finishedGoodsCount": len([dict_row for dict_row in lst_rows if util_safe_int(dict_row.get("itemCategory")) == EItemCategory.PRODUCT]),
            "maintenanceItemCount": len([dict_row for dict_row in lst_rows if dict_row.get("masterStatusCode") == EItemMasterStatusCode.MAINTENANCE_NEEDED]),
        }

    def __build_category_summary(self, lst_rows):
        dict_categories = defaultdict(lambda: {
            "itemCategory": 0,
            "itemCount": 0,
            "stockItemCount": 0,
            "bomLinkedItemCount": 0,
            "maintenanceItemCount": 0,
        })
        for dict_row in lst_rows:
            n_item_category = util_safe_int(dict_row.get("itemCategory"))
            dict_summary = dict_categories[n_item_category]
            dict_summary["itemCategory"] = n_item_category
            dict_summary["itemCount"] += 1
            if dict_row.get("hasStock"):
                dict_summary["stockItemCount"] += 1
            if util_safe_int(dict_row.get("bomCount")) > 0:
                dict_summary["bomLinkedItemCount"] += 1
            if dict_row.get("masterStatusCode") == EItemMasterStatusCode.MAINTENANCE_NEEDED:
                dict_summary["maintenanceItemCount"] += 1
        return [
            dict_categories[n_item_category]
            for n_item_category in sorted(dict_categories.keys(), key=self.__item_category_sort)
        ]

    def __build_maintenance_suggestions(self, lst_rows):
        return [
            self.__build_maintenance_suggestion(dict_row)
            for dict_row in lst_rows
            if dict_row.get("masterStatusCode") == EItemMasterStatusCode.MAINTENANCE_NEEDED
        ]

    def __build_maintenance_suggestion(self, dict_row):
        str_risk_code = dict_row.get("maintenanceRiskCode") or EItemMaintenanceRiskCode.UNKNOWN
        return {
            "suggestionId": "ITEM-%s-%s" % (dict_row.get("itemNo", ""), str_risk_code),
            "itemNo": dict_row.get("itemNo", ""),
            "suggestionTypeCode": self.__suggestion_type_code(str_risk_code),
            "riskLevelCode": self.__suggestion_risk_level_code(str_risk_code),
        }

    def __suggestion_type_code(self, str_risk_code):
        if str_risk_code == EItemMaintenanceRiskCode.MISSING_UNIT:
            return EItemMaintenanceSuggestionTypeCode.MISSING_UNIT
        if str_risk_code == EItemMaintenanceRiskCode.MISSING_BOM:
            return EItemMaintenanceSuggestionTypeCode.MISSING_BOM
        if str_risk_code == EItemMaintenanceRiskCode.MISSING_STOCK_SIGNAL:
            return EItemMaintenanceSuggestionTypeCode.MISSING_STOCK_SIGNAL
        return EItemMaintenanceRiskCode.UNKNOWN

    def __suggestion_risk_level_code(self, str_risk_code):
        if str_risk_code in [EItemMaintenanceRiskCode.MISSING_UNIT, EItemMaintenanceRiskCode.MISSING_BOM]:
            return EBatchRiskLevelCode.ATTENTION
        if str_risk_code == EItemMaintenanceRiskCode.MISSING_STOCK_SIGNAL:
            return EBatchRiskLevelCode.NORMAL
        return EBatchRiskLevelCode.NORMAL

    def __build_item_detail(self, dict_row):
        return {
            "itemNo": dict_row.get("itemNo", ""),
            "itemName": dict_row.get("itemName", ""),
            "itemCategory": util_safe_int(dict_row.get("itemCategory")),
            "itemSubCategory": util_safe_int(dict_row.get("itemSubCategory")),
            "unitWarehouse": util_safe_int(dict_row.get("unitWarehouse")),
            "unitProduct": util_safe_int(dict_row.get("unitProduct")),
            "masterStatusCode": dict_row.get("masterStatusCode", EItemMasterStatusCode.UNKNOWN),
            "maintenanceRiskCode": dict_row.get("maintenanceRiskCode", EItemMaintenanceRiskCode.UNKNOWN),
            "creationTime": util_safe_int(dict_row.get("creationTime")),
        }

    def __build_inventory_detail_summary(self, dict_stock):
        return {
            "hasStock": util_safe_float(dict_stock.get("currentQuantity")) > 0,
            "currentQuantity": util_round_quantity(dict_stock.get("currentQuantity")),
            "availableQuantity": util_round_quantity(dict_stock.get("availableQuantity")),
            "reservedQuantity": util_round_quantity(dict_stock.get("reservedQuantity")),
            "qualityHoldQuantity": util_round_quantity(dict_stock.get("qualityHoldQuantity")),
            "warehouseCount": util_safe_int(dict_stock.get("warehouseCount")),
            "batchCount": util_safe_int(dict_stock.get("batchCount")),
        }

    def __query_bom_usage(self, obj_session, str_item_no):
        lst_usage = []
        for obj_row in obj_session.query(CTableBOMItem).filter(CTableBOMItem.item_no == str_item_no).all():
            obj_bom = self.__query_bom(obj_session, obj_row.bom_no)
            lst_usage.append({
                "bomNo": obj_row.bom_no or "",
                "bomVersion": util_safe_int(getattr(obj_bom, "version", 0)),
                "quantity": util_round_quantity(obj_row.weight),
                "unit": util_safe_int(obj_row.unit),
                "effectiveTimestamp": util_safe_int(getattr(obj_bom, "date", 0)),
            })
        for obj_row in obj_session.query(CTableProductSpec).filter(CTableProductSpec.item_no == str_item_no).all():
            lst_usage.append({
                "bomNo": obj_row.bom_no or "",
                "bomVersion": util_safe_int(obj_row.bom_version),
                "quantity": util_round_quantity(obj_row.weight or obj_row.count),
                "unit": util_safe_int(obj_row.unit),
                "effectiveTimestamp": util_safe_int(getattr(self.__query_bom(obj_session, obj_row.bom_no), "date", 0)),
            })
        return self.__unique_bom_usage(lst_usage)

    def __query_bom(self, obj_session, str_bom_no):
        if not str_bom_no:
            return None
        return (
            obj_session.query(CTableBOM)
            .filter(CTableBOM.no == str_bom_no)
            .order_by(CTableBOM.version.desc(), CTableBOM.date.desc())
            .first()
        )

    def __unique_bom_usage(self, lst_usage):
        dict_rows = {}
        for dict_row in lst_usage:
            str_key = "%s|%s|%s|%s" % (
                dict_row.get("bomNo", ""),
                util_safe_int(dict_row.get("bomVersion")),
                util_safe_int(dict_row.get("unit")),
                util_round_quantity(dict_row.get("quantity")),
            )
            dict_rows[str_key] = dict_row
        return [
            dict_rows[str_key]
            for str_key in sorted(dict_rows.keys())
            if dict_rows[str_key].get("bomNo")
        ]

    def __query_recent_batches(self, obj_session, str_item_no, n_query_timestamp, dict_inventory):
        dict_stock = dict_inventory.get(str_item_no, {})
        dict_batch_quantities = dict_stock.get("_batchQuantities", {})
        lst_rows = (
            obj_session.query(CTableBatchNumber)
            .filter(CTableBatchNumber.item_no == str_item_no)
            .order_by(CTableBatchNumber.date.desc(), CTableBatchNumber.creationTime.desc(), CTableBatchNumber.id.desc())
            .limit(self.MAX_RECENT_BATCHES)
            .all()
        )
        return [
            {
                "batchNo": obj_row.no or "",
                "refCategory": util_safe_int(obj_row.refCategory),
                "refNo": obj_row.ref_no or "",
                "currentQuantity": util_round_quantity(dict_batch_quantities.get(obj_row.no or "", 0.0)),
                "unit": util_safe_int(obj_row.unit),
                "validDate": util_safe_int(obj_row.validDate),
                "riskLevelCode": self.__batch_risk_level_code(obj_row, dict_batch_quantities.get(obj_row.no or "", 0.0), n_query_timestamp),
            }
            for obj_row in lst_rows
        ]

    def __batch_risk_level_code(self, obj_batch, f_current_quantity, n_query_timestamp):
        if util_safe_int(obj_batch.validDate) and util_safe_int(obj_batch.validDate) < n_query_timestamp and util_safe_float(f_current_quantity) > 0:
            return EBatchRiskLevelCode.HIGH_RISK
        return EBatchRiskLevelCode.NORMAL

    def __item_category_sort(self, n_item_category):
        return {
            EItemCategory.PM: 1,
            EItemCategory.MA: 2,
            EItemCategory.AF: 3,
            EItemCategory.INPRODUCT: 4,
            EItemCategory.PRODUCT: 5,
            EItemCategory.GOODS: 6,
            EItemCategory.NONE: 7,
        }.get(util_safe_int(n_item_category), 99)

    def __normalize_page(self, n_start, n_count):
        n_start = max(util_safe_int(n_start), 0)
        n_count = min(max(util_safe_int(n_count), 1), 100)
        return n_start, n_count


class CItemCenterDashboard(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CItemCenterService().get_dashboard(
                n_date=request.args.get("date", 0, type=int),
                str_timezone=str_timezone,
                str_keyword=request.args.get("keyword", "", type=str),
                n_item_category=request.args.get("itemCategory", 0, type=int),
                n_item_sub_category=request.args.get("itemSubCategory", 0, type=int),
                str_master_status_code=request.args.get("masterStatusCode", "", type=str),
                b_has_stock=request.args.get("hasStock", "false", type=str).lower() == "true",
                b_has_bom=request.args.get("hasBom", "false", type=str).lower() == "true",
                n_start=request.args.get("start", 0, type=int),
                n_count=request.args.get("count", 50, type=int),
            )
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CItemCenterDashboard] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CItemCenterDetail(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CItemCenterService().get_detail(
                str_item_no=str_id,
                n_date=request.args.get("date", 0, type=int),
                str_timezone=str_timezone,
            )
            if dict_extra_data is None:
                n_status_code = 400
                n_code = EErrorCode.ERROR_NO_MORE_ITEMS
                str_message = "record not found"
                dict_extra_data = {}
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CItemCenterDetail] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data
