# coding=utf8
import time

from flask import request
from sqlalchemy import or_

from package.common.common import (
    EErrorCode,
    EInventoryCategory,
    EInventoryReadPermissionCode,
)
from package.dbwrapper.dbmgr import CDBMgr
from package.dbwrapper.table import CTableInventoryRec
from package.log.log import CLogger
from package.restserver.api.v2.trace import CTraceabilityService
from package.restserver.api.v2.warehouse import CWarehouseInventoryLotService, CWarehouseInventoryService
from package.util.util import (
    util_build_local_date_range,
    util_round_amount,
    util_round_price,
    util_round_quantity,
    util_safe_float,
    util_safe_int,
)


class CInventoryReadService(object):
    MAX_PAGE_COUNT = 100

    def get_balances(
        self,
        n_date=0,
        str_timezone="",
        str_warehouse_no="",
        n_item_category=0,
        str_item_no="",
        str_lot_code="",
        n_start=0,
        n_count=50,
    ):
        with CDBMgr() as obj_dbmgr:
            return self._get_balances_with_session(
                obj_dbmgr.get_session(),
                n_date,
                str_timezone,
                str_warehouse_no,
                n_item_category,
                str_item_no,
                str_lot_code,
                n_start,
                n_count,
            )

    def _get_balances_with_session(
        self,
        obj_session,
        n_date=0,
        str_timezone="",
        str_warehouse_no="",
        n_item_category=0,
        str_item_no="",
        str_lot_code="",
        n_start=0,
        n_count=50,
    ):
        dict_payload = CWarehouseInventoryService()._get_inventory_with_session(
            obj_session=obj_session,
            n_date=n_date,
            str_timezone=str_timezone,
            str_warehouse_no=str_warehouse_no,
            n_item_category=n_item_category,
            str_item_no=str_item_no,
            str_batch_no=str_lot_code,
            str_risk_type="",
            n_start=n_start,
            n_count=self.__normalize_count(n_count),
        )
        return self.__balance_payload(dict_payload)

    def get_lots(
        self,
        n_date=0,
        str_timezone="",
        str_warehouse_no="",
        n_item_category=0,
        str_item_no="",
        str_lot_code="",
        str_keyword="",
        n_start=0,
        n_count=50,
    ):
        with CDBMgr() as obj_dbmgr:
            return self._get_lots_with_session(
                obj_dbmgr.get_session(),
                n_date,
                str_timezone,
                str_warehouse_no,
                n_item_category,
                str_item_no,
                str_lot_code,
                str_keyword,
                n_start,
                n_count,
            )

    def _get_lots_with_session(
        self,
        obj_session,
        n_date=0,
        str_timezone="",
        str_warehouse_no="",
        n_item_category=0,
        str_item_no="",
        str_lot_code="",
        str_keyword="",
        n_start=0,
        n_count=50,
    ):
        dict_payload = CWarehouseInventoryLotService()._get_lots_with_session(
            obj_session=obj_session,
            n_date=n_date,
            str_timezone=str_timezone,
            str_warehouse_no=str_warehouse_no,
            n_item_category=n_item_category,
            str_item_no=str_item_no,
            str_batch_no=str_lot_code,
            str_risk_type="",
            n_task_type=0,
            str_availability="",
            str_keyword=str_keyword,
            str_sort="",
            str_order="",
            n_start=n_start,
            n_count=self.__normalize_count(n_count),
        )
        return self.__lot_payload(dict_payload)

    def get_movements(
        self,
        n_date=0,
        str_timezone="",
        str_warehouse_no="",
        n_item_category=0,
        str_item_no="",
        str_lot_code="",
        str_keyword="",
        str_start_date="",
        str_end_date="",
        n_start=0,
        n_count=50,
    ):
        with CDBMgr() as obj_dbmgr:
            return self.__get_movements_with_session(
                obj_dbmgr.get_session(),
                n_date,
                str_timezone,
                str_warehouse_no,
                n_item_category,
                str_item_no,
                str_lot_code,
                str_keyword,
                str_start_date,
                str_end_date,
                n_start,
                n_count,
            )

    def _get_movements_with_session(
        self,
        obj_session,
        n_date=0,
        str_timezone="",
        str_warehouse_no="",
        n_item_category=0,
        str_item_no="",
        str_lot_code="",
        str_keyword="",
        str_start_date="",
        str_end_date="",
        n_start=0,
        n_count=50,
    ):
        return self.__get_movements_with_session(
            obj_session,
            n_date,
            str_timezone,
            str_warehouse_no,
            n_item_category,
            str_item_no,
            str_lot_code,
            str_keyword,
            str_start_date,
            str_end_date,
            n_start,
            n_count,
        )

    def get_lot_trace(self, str_lot_code, str_timezone=""):
        return CTraceabilityService().get_batch_overview(
            str_batch_no=str_lot_code,
            str_timezone=str_timezone,
        )

    def permission_code(self):
        return EInventoryReadPermissionCode.WH_INV_READ

    def __get_movements_with_session(
        self,
        obj_session,
        n_date,
        str_timezone,
        str_warehouse_no,
        n_item_category,
        str_item_no,
        str_lot_code,
        str_keyword,
        str_start_date,
        str_end_date,
        n_start,
        n_count,
    ):
        n_query_timestamp = util_safe_int(n_date) or util_safe_int(time.time())
        n_start = max(util_safe_int(n_start), 0)
        n_count = self.__normalize_count(n_count)
        lst_filters = []
        dict_range = util_build_local_date_range(str_start_date, str_end_date, str_timezone) if str_start_date and str_end_date else None
        if dict_range:
            lst_filters.append(CTableInventoryRec.date >= dict_range.get("startTimestamp", 0))
            lst_filters.append(CTableInventoryRec.date <= dict_range.get("endTimestamp", 0))
        else:
            lst_filters.append(CTableInventoryRec.date <= n_query_timestamp)
        if str_warehouse_no:
            lst_filters.append(CTableInventoryRec.warehouse_no == str_warehouse_no)
        if n_item_category:
            lst_filters.append(CTableInventoryRec.itemCategory == n_item_category)
        if str_item_no:
            lst_filters.append(CTableInventoryRec.item_no == str_item_no)
        if str_lot_code:
            lst_filters.append(CTableInventoryRec.batchNumber == str_lot_code)
        str_keyword = (str_keyword or "").strip()
        if str_keyword:
            str_like = "%%%s%%" % str_keyword
            lst_filters.append(or_(
                CTableInventoryRec.ref_no.ilike(str_like),
                CTableInventoryRec.item_no.ilike(str_like),
                CTableInventoryRec.item_name.ilike(str_like),
                CTableInventoryRec.batchNumber.ilike(str_like),
                CTableInventoryRec.warehouse_no.ilike(str_like),
                CTableInventoryRec.warehouse_displayName.ilike(str_like),
            ))

        obj_query = obj_session.query(CTableInventoryRec).filter(*lst_filters)
        n_total = obj_query.count()
        lst_rows = (
            obj_query
            .order_by(CTableInventoryRec.date.desc(), CTableInventoryRec.id.desc())
            .offset(n_start)
            .limit(n_count)
            .all()
        )
        return {
            "serverTimestamp": n_query_timestamp,
            "timezone": str_timezone or "UTC",
            "total": n_total,
            "start": n_start,
            "count": len(lst_rows),
            "permissionCode": self.permission_code(),
            "range": self.__range_payload(dict_range),
            "movements": [self.__movement_to_dict(obj_row) for obj_row in lst_rows],
        }

    def __balance_payload(self, dict_payload):
        return {
            "serverTimestamp": util_safe_int(dict_payload.get("serverTimestamp")),
            "timezone": dict_payload.get("timezone", "UTC"),
            "total": util_safe_int(dict_payload.get("total")),
            "start": util_safe_int(dict_payload.get("start")),
            "count": util_safe_int(dict_payload.get("count")),
            "permissionCode": self.permission_code(),
            "balances": [self.__balance_to_dict(dict_row) for dict_row in dict_payload.get("results", [])],
        }

    def __lot_payload(self, dict_payload):
        return {
            "serverTimestamp": util_safe_int(dict_payload.get("serverTimestamp")),
            "timezone": dict_payload.get("timezone", "UTC"),
            "total": util_safe_int(dict_payload.get("total")),
            "start": util_safe_int(dict_payload.get("start")),
            "count": util_safe_int(dict_payload.get("count")),
            "permissionCode": self.permission_code(),
            "summary": dict_payload.get("summary", {}),
            "lots": [self.__lot_to_dict(dict_row) for dict_row in dict_payload.get("results", [])],
        }

    def __balance_to_dict(self, dict_row):
        return {
            "balanceId": dict_row.get("inventoryId", ""),
            "warehouseNo": dict_row.get("warehouseNo", ""),
            "warehouseName": dict_row.get("warehouseName", ""),
            "itemNo": dict_row.get("itemNo", ""),
            "itemName": dict_row.get("itemName", ""),
            "itemCategory": util_safe_int(dict_row.get("itemCategory")),
            "itemSubCategory": util_safe_int(dict_row.get("itemSubCategory")),
            "lotCode": dict_row.get("batchNo", ""),
            "serialNo": dict_row.get("serialNo", ""),
            "currentQuantity": util_round_quantity(dict_row.get("currentQuantity")),
            "reservedQuantity": util_round_quantity(dict_row.get("reservedQuantity")),
            "qualityHoldQuantity": util_round_quantity(dict_row.get("qualityHoldQuantity")),
            "availableQuantity": util_round_quantity(dict_row.get("availableQuantity")),
            "unit": util_safe_int(dict_row.get("unit")),
            "unitCost": util_round_price(dict_row.get("unitCost")),
            "inventoryValue": util_round_amount(dict_row.get("inventoryValue")),
            "availableValue": util_round_amount(dict_row.get("availableValue")),
            "sourceRefCategory": util_safe_int(dict_row.get("sourceRefCategory")),
            "sourceNo": dict_row.get("sourceNo", ""),
            "qualityStatus": dict_row.get("qualityStatus", ""),
            "riskTypes": dict_row.get("riskTypes", []),
        }

    def __lot_to_dict(self, dict_row):
        return {
            "lotKey": dict_row.get("lotKey", ""),
            "lotCode": dict_row.get("batchNo", ""),
            "warehouseNo": dict_row.get("warehouseNo", ""),
            "warehouseName": dict_row.get("warehouseName", ""),
            "itemCategory": util_safe_int(dict_row.get("itemCategory")),
            "itemNo": dict_row.get("itemNo", ""),
            "itemName": dict_row.get("itemName", ""),
            "currentQuantity": util_round_quantity(dict_row.get("currentQuantity")),
            "reservedQuantity": util_round_quantity(dict_row.get("reservedQuantity")),
            "qualityHoldQuantity": util_round_quantity(dict_row.get("qualityHoldQuantity")),
            "availableQuantity": util_round_quantity(dict_row.get("availableQuantity")),
            "unit": util_safe_int(dict_row.get("unit")),
            "unitCost": util_round_price(dict_row.get("unitCost")),
            "inventoryValue": util_round_amount(dict_row.get("inventoryValue")),
            "palletCount": util_round_quantity(dict_row.get("palletCount")),
            "firstInboundTimestamp": util_safe_int(dict_row.get("firstInboundTimestamp")),
            "daysInStock": util_safe_int(dict_row.get("daysInStock")),
            "validDate": util_safe_int(dict_row.get("validDate")),
            "validDays": util_safe_int(dict_row.get("validDays")),
            "safetyStock": util_round_quantity(dict_row.get("safetyStock")),
            "riskTypes": dict_row.get("riskTypes", []),
            "openTaskCount": util_safe_int(dict_row.get("openTaskCount")),
            "refCategory": util_safe_int(dict_row.get("refCategory")),
            "refNo": dict_row.get("refNo", ""),
        }

    def __movement_to_dict(self, obj_row):
        f_quantity = util_round_quantity(obj_row.count)
        n_amount = util_round_amount(obj_row.amount)
        return {
            "movementId": util_safe_int(obj_row.id),
            "groupNo": obj_row.group or "",
            "warehouseNo": obj_row.warehouse_no or "",
            "warehouseName": obj_row.warehouse_displayName or "",
            "itemNo": obj_row.item_no or "",
            "itemName": obj_row.item_name or "",
            "itemCategory": util_safe_int(obj_row.itemCategory),
            "lotCode": obj_row.batchNumber or "",
            "serialNo": obj_row.serialNo or "",
            "movementTimestamp": util_safe_int(obj_row.date),
            "category": util_safe_int(obj_row.category),
            "source": util_safe_int(obj_row.source),
            "quantity": f_quantity,
            "unit": util_safe_int(obj_row.unit),
            "unitCost": util_round_price(float(n_amount) / f_quantity) if f_quantity else 0.0,
            "amount": n_amount,
            "refCategory": util_safe_int(obj_row.refCategory),
            "refNo": obj_row.ref_no or "",
            "comment": obj_row.comment or "",
            "creationTime": util_safe_int(obj_row.creationTime),
        }

    def __range_payload(self, dict_range):
        if not dict_range:
            return {}
        return {
            "period": dict_range.get("period", ""),
            "startDate": dict_range.get("startDate", ""),
            "endDate": dict_range.get("endDate", ""),
            "startTimestamp": util_safe_int(dict_range.get("startTimestamp")),
            "endTimestamp": util_safe_int(dict_range.get("endTimestamp")),
        }

    def __normalize_count(self, n_count):
        n_count = util_safe_int(n_count) if n_count else 50
        return min(max(n_count, 1), self.MAX_PAGE_COUNT)


class CInventoryReadBase(object):
    def is_allowed_for_get(self, lst_privileges):
        return True

    def permission_code(self):
        return EInventoryReadPermissionCode.WH_INV_READ


class CInventoryBalances(CInventoryReadBase):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CInventoryReadService().get_balances(
                n_date=request.args.get("date", 0, type=int),
                str_timezone=str_timezone,
                str_warehouse_no=request.args.get("warehouse_no", "", type=str),
                n_item_category=request.args.get("itemCategory", 0, type=int),
                str_item_no=request.args.get("item_no", "", type=str),
                str_lot_code=request.args.get("lotCode", "", type=str),
                n_start=request.args.get("start", 0, type=int),
                n_count=request.args.get("count", 50, type=int),
            )
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CInventoryBalances] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CInventoryMovements(CInventoryReadBase):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CInventoryReadService().get_movements(
                n_date=request.args.get("date", 0, type=int),
                str_timezone=str_timezone,
                str_warehouse_no=request.args.get("warehouse_no", "", type=str),
                n_item_category=request.args.get("itemCategory", 0, type=int),
                str_item_no=request.args.get("item_no", "", type=str),
                str_lot_code=request.args.get("lotCode", "", type=str),
                str_keyword=request.args.get("keyword", "", type=str),
                str_start_date=request.args.get("startDate", "", type=str),
                str_end_date=request.args.get("endDate", "", type=str),
                n_start=request.args.get("start", 0, type=int),
                n_count=request.args.get("count", 50, type=int),
            )
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CInventoryMovements] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CInventoryLots(CInventoryReadBase):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CInventoryReadService().get_lots(
                n_date=request.args.get("date", 0, type=int),
                str_timezone=str_timezone,
                str_warehouse_no=request.args.get("warehouse_no", "", type=str),
                n_item_category=request.args.get("itemCategory", 0, type=int),
                str_item_no=request.args.get("item_no", "", type=str),
                str_lot_code=request.args.get("lotCode", "", type=str),
                str_keyword=request.args.get("keyword", "", type=str),
                n_start=request.args.get("start", 0, type=int),
                n_count=request.args.get("count", 50, type=int),
            )
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CInventoryLots] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CInventoryLotTrace(CInventoryReadBase):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CInventoryReadService().get_lot_trace(
                str_lot_code=str_id,
                str_timezone=str_timezone,
            )
            if dict_extra_data is None:
                n_status_code = 400
                n_code = EErrorCode.ERROR_NO_MORE_ITEMS
                str_message = "record not found"
                dict_extra_data = {}
            else:
                dict_extra_data["permissionCode"] = EInventoryReadPermissionCode.WH_INV_READ
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CInventoryLotTrace] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data
