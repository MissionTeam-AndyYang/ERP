# coding=utf8
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from sqlalchemy import and_, case, func, or_

from package.common.common import (
    EErrorCode,
    EInventoryDeltaKind,
    EInventoryCategory,
    EItemCategory,
    EShipWarehouseCat,
    EWarehouseRiskLevel,
    EWarehouseRiskType,
    EWorkflowTaskStatus,
    EWorkflowTaskType,
)
from package.dbwrapper.dbmgr import CDBMgr
from package.dbwrapper.table import (
    CTableBatchNumber,
    CTableGoods,
    CTableInventoryDelta,
    CTableInventoryItemMonthStatistic,
    CTableInventoryMonthStatistic,
    CTableInproduct,
    CTableInventoryRec,
    CTableItemSafetyStock,
    CTableMaterial,
    CTableProduct,
    CTableShipWarehouse,
    CTableShipWarehouseAlias,
    CTableShipWarehouseContract,
    CTableWarehouseInventoryReservation,
    CTableWarehousePalletMovement,
    CTableWarehouseQualityHold,
    CTableWarehouseRiskRule,
    CTableWorkflowTaskEvent,
    CTableWorkflowTaskState,
)
from package.log.log import CLogger
from package.util.util import (
    util_round_amount,
    util_round_price,
    util_round_quantity,
    util_safe_float,
    util_safe_int,
)


class CWarehouseInventorySnapshotCalculator(object):
    def query_inventory_rows(
        self,
        obj_session,
        n_query_timestamp,
        str_warehouse_no,
        n_item_category,
        str_timezone,
        fn_query_statistics,
        fn_query_records,
        fn_query_record_stock_tuples,
        fn_stock_tuple,
    ):
        lst_stat_rows, dict_stat_coverage = fn_query_statistics(
            obj_session,
            n_query_timestamp,
            str_warehouse_no,
            n_item_category,
            str_timezone,
        )
        if not lst_stat_rows:
            return fn_query_records(
                obj_session,
                n_query_timestamp,
                str_warehouse_no,
                n_item_category,
            )

        if dict_stat_coverage.get("needsRecordRefresh"):
            return fn_query_records(
                obj_session,
                n_query_timestamp,
                str_warehouse_no,
                n_item_category,
            )

        set_stat_tuples = {
            fn_stock_tuple(
                dict_row.get("itemNo"),
                dict_row.get("batchNo"),
                dict_row.get("warehouseNo"),
            )
            for dict_row in lst_stat_rows
        }
        set_record_tuples = fn_query_record_stock_tuples(
            obj_session,
            n_query_timestamp,
            str_warehouse_no,
            n_item_category,
        )
        set_missing_tuples = set_record_tuples - set_stat_tuples
        if not set_missing_tuples:
            return lst_stat_rows

        lst_stat_rows.extend(fn_query_records(
            obj_session,
            n_query_timestamp,
            str_warehouse_no,
            n_item_category,
            set_missing_tuples,
        ))
        return lst_stat_rows


class CWarehouseDashboardService(object):
    RESERVATION_STATUS_ACTIVE = 1
    QUALITY_HOLD_STATUS_ACTIVE = 1
    PALLET_STATUS_USED = 1
    PALLET_STATUS_RESERVED = 2
    STATUS_ACTIVE = 1

    def get_dashboard(
        self,
        n_date=0,
        str_timezone="",
        str_warehouse_no="",
        n_item_category=0,
        b_include_inventory=False,
        b_risk_only=False,
        n_trend_days=7,
        obj_session=None,
    ):
        if obj_session:
            return self.__get_dashboard_with_session(
                obj_session,
                n_date,
                str_timezone,
                str_warehouse_no,
                n_item_category,
                b_include_inventory,
                b_risk_only,
                n_trend_days,
            )

        with CDBMgr() as obj_dbmgr:
            return self.__get_dashboard_with_session(
                obj_dbmgr.get_session(),
                n_date,
                str_timezone,
                str_warehouse_no,
                n_item_category,
                b_include_inventory,
                b_risk_only,
                n_trend_days,
            )

    def __get_dashboard_with_session(
        self,
        obj_session,
        n_date,
        str_timezone,
        str_warehouse_no,
        n_item_category,
        b_include_inventory,
        b_risk_only,
        n_trend_days,
    ):
        n_query_timestamp = n_date if n_date else int(time.time())
        dict_range = self.__build_range(n_query_timestamp, str_timezone)
        lst_inventory_rows = self.__query_inventory_rows(
            obj_session,
            n_query_timestamp,
            str_warehouse_no,
            n_item_category,
            str_timezone,
        )
        dict_reservations = self.__query_reservations(obj_session, n_query_timestamp)
        dict_quality_holds = self.__query_quality_holds(obj_session, n_query_timestamp)
        dict_pallets = self.__query_pallets(obj_session, n_query_timestamp, str_warehouse_no, n_item_category)
        dict_capacity = self.__query_capacity(obj_session, str_warehouse_no)
        dict_safety_stock = self.__query_safety_stock(obj_session, n_query_timestamp)
        dict_risk_rules = self.__query_risk_rules(obj_session)
        lst_inventory_detail = self.__build_inventory_detail(
            lst_inventory_rows,
            dict_reservations,
            dict_quality_holds,
        )
        lst_risks = self.__build_risk_alerts(
            lst_inventory_detail,
            dict_safety_stock,
            dict_risk_rules,
            n_query_timestamp,
            b_risk_only,
        )
        lst_tasks = self.__query_pending_tasks(obj_session, str_warehouse_no, dict_range["endTimestamp"])
        dict_trend = self.__query_value_trend(
            obj_session,
            n_query_timestamp,
            str_timezone,
            str_warehouse_no,
            n_item_category,
            n_trend_days,
        )
        dict_payload = self.__build_payload(
            n_query_timestamp,
            str_timezone,
            dict_range,
            lst_inventory_rows,
            dict_reservations,
            dict_quality_holds,
            dict_pallets,
            dict_capacity,
            lst_risks,
            lst_tasks,
            lst_inventory_detail,
            b_include_inventory,
            b_risk_only,
            dict_trend,
        )
        return dict_payload

    def __build_range(self, n_timestamp, str_timezone):
        try:
            obj_tz = ZoneInfo(str_timezone or "UTC")
        except Exception:
            obj_tz = timezone.utc
        obj_local = datetime.fromtimestamp(n_timestamp, timezone.utc).astimezone(obj_tz)
        obj_start_local = obj_local.replace(hour=0, minute=0, second=0, microsecond=0)
        n_start = int(obj_start_local.astimezone(timezone.utc).timestamp())
        n_end = n_start + 86399
        return {
            "date": obj_local.strftime("%Y-%m-%d"),
            "startTimestamp": n_start,
            "endTimestamp": n_end,
        }

    def __query_local_date(self, n_timestamp, str_timezone):
        try:
            obj_tz = ZoneInfo(str_timezone or "UTC")
        except Exception:
            obj_tz = timezone.utc
        return datetime.fromtimestamp(n_timestamp, timezone.utc).astimezone(obj_tz).date()

    def __query_inventory_rows(
        self,
        obj_session,
        n_query_timestamp,
        str_warehouse_no,
        n_item_category,
        str_timezone="",
    ):
        return CWarehouseInventorySnapshotCalculator().query_inventory_rows(
            obj_session,
            n_query_timestamp,
            str_warehouse_no,
            n_item_category,
            str_timezone,
            self.__query_inventory_rows_from_statistics,
            self.__query_inventory_rows_from_records,
            self.__query_record_stock_tuples,
            self.__stock_tuple,
        )

    def __query_inventory_rows_from_records(
        self,
        obj_session,
        n_query_timestamp,
        str_warehouse_no,
        n_item_category,
        set_stock_tuples=None,
    ):
        lst_filters = [
            CTableInventoryRec.itemCategory.in_(self.__target_categories()),
            CTableInventoryRec.date <= n_query_timestamp,
        ]
        if str_warehouse_no:
            lst_filters.append(CTableInventoryRec.warehouse_no == str_warehouse_no)
        if n_item_category:
            lst_filters.append(CTableInventoryRec.itemCategory == n_item_category)
        if set_stock_tuples:
            lst_filters.append(self.__stock_tuple_filter(CTableInventoryRec, set_stock_tuples))

        obj_signed_count = func.sum(
            case(
                (CTableInventoryRec.category == EInventoryCategory.IN, CTableInventoryRec.count),
                (CTableInventoryRec.category == EInventoryCategory.OUT, -CTableInventoryRec.count),
                else_=0,
            )
        ).label("currentQuantity")
        obj_signed_amount = func.sum(
            case(
                (CTableInventoryRec.category == EInventoryCategory.IN, CTableInventoryRec.amount),
                (CTableInventoryRec.category == EInventoryCategory.OUT, -CTableInventoryRec.amount),
                else_=0,
            )
        ).label("inventoryValue")
        obj_first_inbound = func.min(
            case(
                (CTableInventoryRec.category == EInventoryCategory.IN, CTableInventoryRec.date),
                else_=None,
            )
        ).label("firstInboundTimestamp")

        lst_rows = (
            obj_session.query(
                CTableInventoryRec.warehouse_no,
                CTableInventoryRec.warehouse_displayName,
                CTableInventoryRec.itemCategory,
                CTableInventoryRec.item_no,
                CTableInventoryRec.item_name,
                CTableInventoryRec.itemType,
                CTableInventoryRec.batchNumber,
                CTableInventoryRec.unit,
                obj_signed_count,
                obj_signed_amount,
                obj_first_inbound,
            )
            .filter(*lst_filters)
            .group_by(
                CTableInventoryRec.warehouse_no,
                CTableInventoryRec.warehouse_displayName,
                CTableInventoryRec.itemCategory,
                CTableInventoryRec.item_no,
                CTableInventoryRec.item_name,
                CTableInventoryRec.itemType,
                CTableInventoryRec.batchNumber,
                CTableInventoryRec.unit,
            )
            .all()
        )

        lst_batch_numbers = [obj_row.batchNumber for obj_row in lst_rows if obj_row.batchNumber]
        dict_batch = {}
        if lst_batch_numbers:
            lst_batch_rows = (
                obj_session.query(
                    CTableBatchNumber.no,
                    CTableBatchNumber.itemSubCategory,
                    CTableBatchNumber.itemType,
                    CTableBatchNumber.validDays,
                    CTableBatchNumber.validDate,
                )
                .filter(CTableBatchNumber.no.in_(lst_batch_numbers))
                .all()
            )
            dict_batch = {
                obj_row.no: {
                    "itemSubCategory": util_safe_int(obj_row.itemSubCategory),
                    "itemType": util_safe_int(obj_row.itemType),
                    "validDays": util_safe_int(obj_row.validDays),
                    "validDate": util_safe_int(obj_row.validDate),
                }
                for obj_row in lst_batch_rows
            }

        dict_item_metadata = self.__query_item_metadata(
            obj_session,
            [(obj_row.item_no, obj_row.itemCategory) for obj_row in lst_rows],
        )
        lst_results = []
        for obj_row in lst_rows:
            f_quantity = util_safe_float(obj_row.currentQuantity)
            if f_quantity == 0:
                continue
            dict_batch_info = dict_batch.get(obj_row.batchNumber, {})
            dict_item_info = dict_item_metadata.get((obj_row.item_no or "", util_safe_int(obj_row.itemCategory)), {})
            lst_results.append({
                "warehouseNo": obj_row.warehouse_no or "",
                "warehouseName": obj_row.warehouse_displayName or "",
                "itemCategory": util_safe_int(obj_row.itemCategory),
                "itemSubCategory": util_safe_int(
                    dict_batch_info.get("itemSubCategory")
                    or dict_item_info.get("itemSubCategory")
                    or 0
                ),
                "itemType": util_safe_int(
                    dict_batch_info.get("itemType")
                    or obj_row.itemType
                    or 0
                ),
                "itemNo": obj_row.item_no or "",
                "itemName": obj_row.item_name or "",
                "batchNo": obj_row.batchNumber or "",
                "unit": util_safe_int(obj_row.unit),
                "currentQuantity": util_round_quantity(f_quantity),
                "inventoryValue": util_round_amount(obj_row.inventoryValue),
                "firstInboundTimestamp": util_safe_int(obj_row.firstInboundTimestamp),
                "validDays": util_safe_int(dict_batch_info.get("validDays", 0)),
                "validDate": util_safe_int(dict_batch_info.get("validDate", 0)),
            })
        return lst_results

    def __query_record_stock_tuples(self, obj_session, n_query_timestamp, str_warehouse_no, n_item_category):
        lst_filters = [
            CTableInventoryRec.itemCategory.in_(self.__target_categories()),
            CTableInventoryRec.date <= n_query_timestamp,
        ]
        if str_warehouse_no:
            lst_filters.append(CTableInventoryRec.warehouse_no == str_warehouse_no)
        if n_item_category:
            lst_filters.append(CTableInventoryRec.itemCategory == n_item_category)

        lst_rows = (
            obj_session.query(
                CTableInventoryRec.item_no,
                CTableInventoryRec.batchNumber,
                CTableInventoryRec.warehouse_no,
            )
            .filter(*lst_filters)
            .group_by(
                CTableInventoryRec.item_no,
                CTableInventoryRec.batchNumber,
                CTableInventoryRec.warehouse_no,
            )
            .all()
        )
        return {
            self.__stock_tuple(obj_row.item_no, obj_row.batchNumber, obj_row.warehouse_no)
            for obj_row in lst_rows
        }

    def __query_inventory_rows_from_statistics(
        self,
        obj_session,
        n_query_timestamp,
        str_warehouse_no,
        n_item_category,
        str_timezone,
    ):
        obj_query_date = self.__query_local_date(n_query_timestamp, str_timezone)
        str_stat_timezone = str_timezone or "UTC"
        lst_filters = [
            CTableInventoryItemMonthStatistic.kind == EInventoryDeltaKind.BATCHNO,
            CTableInventoryItemMonthStatistic.category.in_(self.__target_categories()),
            CTableInventoryItemMonthStatistic.date <= obj_query_date,
            CTableInventoryItemMonthStatistic.timezone == str_stat_timezone,
        ]
        if str_warehouse_no:
            lst_filters.append(CTableInventoryItemMonthStatistic.warehouse_no == str_warehouse_no)
        if n_item_category:
            lst_filters.append(CTableInventoryItemMonthStatistic.category == n_item_category)

        lst_stat_rows = (
            obj_session.query(CTableInventoryItemMonthStatistic)
            .filter(*lst_filters)
            .order_by(CTableInventoryItemMonthStatistic.date.asc(), CTableInventoryItemMonthStatistic.id.asc())
            .all()
        )

        dict_inventory = {}
        dict_latest_stat_date = {}
        for obj_row in lst_stat_rows:
            str_key = self.__stock_key(obj_row.specified_ref_no, obj_row.specified_no, obj_row.warehouse_no)
            dict_inventory[str_key] = {
                "warehouseNo": obj_row.warehouse_no or "",
                "warehouseName": obj_row.warehouse_displayName or "",
                "itemCategory": util_safe_int(obj_row.category),
                "itemNo": obj_row.specified_ref_no or "",
                "itemName": obj_row.specified_ref_name or "",
                "batchNo": obj_row.specified_no or "",
                "unit": util_safe_int(obj_row.unit),
                "currentQuantity": util_safe_float(obj_row.endCount),
                "inventoryValue": util_safe_float(obj_row.endAmount),
            }
            dict_latest_stat_date[str_key] = obj_row.date

        lst_delta_filters = [
            CTableInventoryDelta.kind == EInventoryDeltaKind.BATCHNO,
            CTableInventoryDelta.category.in_(self.__target_categories()),
            CTableInventoryDelta.date <= obj_query_date,
            CTableInventoryDelta.timezone == str_stat_timezone,
        ]
        if str_warehouse_no:
            lst_delta_filters.append(CTableInventoryDelta.warehouse_no == str_warehouse_no)
        if n_item_category:
            lst_delta_filters.append(CTableInventoryDelta.category == n_item_category)

        lst_delta_rows = (
            obj_session.query(CTableInventoryDelta)
            .filter(*lst_delta_filters)
            .all()
        )
        obj_latest_stat_date = max(dict_latest_stat_date.values()) if dict_latest_stat_date else None
        obj_latest_delta_date = max([obj_row.date for obj_row in lst_delta_rows], default=None)
        b_needs_record_refresh = False
        if obj_latest_stat_date and obj_latest_stat_date < obj_query_date:
            b_needs_record_refresh = not obj_latest_delta_date or obj_latest_delta_date < obj_query_date
        elif obj_latest_delta_date and obj_latest_delta_date < obj_query_date and not obj_latest_stat_date:
            b_needs_record_refresh = True

        for obj_row in lst_delta_rows:
            str_key = self.__stock_key(obj_row.specified_ref_no, obj_row.specified_no, obj_row.warehouse_no)
            obj_latest_date = dict_latest_stat_date.get(str_key)
            if obj_latest_date and obj_row.date <= obj_latest_date:
                continue
            if str_key not in dict_inventory:
                dict_inventory[str_key] = {
                    "warehouseNo": obj_row.warehouse_no or "",
                    "warehouseName": obj_row.warehouse_displayName or "",
                    "itemCategory": util_safe_int(obj_row.category),
                    "itemNo": obj_row.specified_ref_no or "",
                    "itemName": obj_row.specified_ref_name or "",
                    "batchNo": obj_row.specified_no or "",
                    "unit": 0,
                    "currentQuantity": 0.0,
                    "inventoryValue": 0.0,
                }
            dict_inventory[str_key]["currentQuantity"] += (
                util_safe_float(obj_row.inCount) - util_safe_float(obj_row.outCount)
            )
            dict_inventory[str_key]["inventoryValue"] += (
                util_safe_float(obj_row.inAmount) - util_safe_float(obj_row.outAmount)
            )

        if not dict_inventory:
            return [], {"needsRecordRefresh": True}

        lst_inventory_rows = list(dict_inventory.values())
        lst_batch_numbers = [dict_row.get("batchNo") for dict_row in lst_inventory_rows if dict_row.get("batchNo")]
        dict_batch = self.__query_batch_metadata(obj_session, lst_batch_numbers)
        dict_item_metadata = self.__query_item_metadata(
            obj_session,
            [(dict_row.get("itemNo"), dict_row.get("itemCategory")) for dict_row in lst_inventory_rows],
        )
        dict_first_inbound = self.__query_first_inbound_timestamps(obj_session, n_query_timestamp)
        dict_record_metadata = self.__query_latest_record_metadata(obj_session, n_query_timestamp)

        lst_results = []
        for dict_row in lst_inventory_rows:
            f_quantity = util_safe_float(dict_row.get("currentQuantity"))
            if f_quantity == 0:
                continue
            str_item_no = dict_row.get("itemNo") or ""
            str_batch_no = dict_row.get("batchNo") or ""
            str_warehouse_no = dict_row.get("warehouseNo") or ""
            n_item_category = util_safe_int(dict_row.get("itemCategory"))
            dict_batch_info = dict_batch.get(str_batch_no, {})
            dict_item_info = dict_item_metadata.get((str_item_no, n_item_category), {})
            dict_record_info = dict_record_metadata.get(self.__stock_key(str_item_no, str_batch_no, str_warehouse_no), {})
            lst_results.append({
                "warehouseNo": str_warehouse_no,
                "warehouseName": dict_row.get("warehouseName") or "",
                "itemCategory": n_item_category,
                "itemSubCategory": util_safe_int(
                    dict_batch_info.get("itemSubCategory")
                    or dict_item_info.get("itemSubCategory")
                    or 0
                ),
                "itemType": util_safe_int(
                    dict_batch_info.get("itemType")
                    or dict_record_info.get("itemType")
                    or 0
                ),
                "itemNo": str_item_no,
                "itemName": dict_row.get("itemName") or "",
                "batchNo": str_batch_no,
                "unit": util_safe_int(dict_row.get("unit") or dict_record_info.get("unit")),
                "currentQuantity": util_round_quantity(f_quantity),
                "inventoryValue": util_round_amount(dict_row.get("inventoryValue")),
                "firstInboundTimestamp": util_safe_int(
                    dict_first_inbound.get(self.__stock_key(str_item_no, str_batch_no, str_warehouse_no))
                ),
                "validDays": util_safe_int(dict_batch_info.get("validDays", 0)),
                "validDate": util_safe_int(dict_batch_info.get("validDate", 0)),
            })
        return lst_results, {
            "latestStatDate": obj_latest_stat_date,
            "latestDeltaDate": obj_latest_delta_date,
            "needsRecordRefresh": b_needs_record_refresh,
        }

    def __query_batch_metadata(self, obj_session, lst_batch_numbers):
        dict_batch = {}
        if not lst_batch_numbers:
            return dict_batch
        lst_batch_rows = (
            obj_session.query(
                CTableBatchNumber.no,
                CTableBatchNumber.itemSubCategory,
                CTableBatchNumber.itemType,
                CTableBatchNumber.validDays,
                CTableBatchNumber.validDate,
            )
            .filter(CTableBatchNumber.no.in_(lst_batch_numbers))
            .all()
        )
        return {
            obj_row.no: {
                "itemSubCategory": util_safe_int(obj_row.itemSubCategory),
                "itemType": util_safe_int(obj_row.itemType),
                "validDays": util_safe_int(obj_row.validDays),
                "validDate": util_safe_int(obj_row.validDate),
            }
            for obj_row in lst_batch_rows
        }

    def __query_first_inbound_timestamps(self, obj_session, n_query_timestamp):
        lst_rows = (
            obj_session.query(
                CTableInventoryRec.item_no,
                CTableInventoryRec.batchNumber,
                CTableInventoryRec.warehouse_no,
                func.min(CTableInventoryRec.date).label("firstInboundTimestamp"),
            )
            .filter(CTableInventoryRec.category == EInventoryCategory.IN)
            .filter(CTableInventoryRec.date <= n_query_timestamp)
            .group_by(
                CTableInventoryRec.item_no,
                CTableInventoryRec.batchNumber,
                CTableInventoryRec.warehouse_no,
            )
            .all()
        )
        return {
            self.__stock_key(obj_row.item_no, obj_row.batchNumber, obj_row.warehouse_no): util_safe_int(obj_row.firstInboundTimestamp)
            for obj_row in lst_rows
        }

    def __query_latest_record_metadata(self, obj_session, n_query_timestamp):
        lst_rows = (
            obj_session.query(CTableInventoryRec)
            .filter(CTableInventoryRec.date <= n_query_timestamp)
            .order_by(CTableInventoryRec.date.desc(), CTableInventoryRec.id.desc())
            .all()
        )
        dict_result = {}
        for obj_row in lst_rows:
            str_key = self.__stock_key(obj_row.item_no, obj_row.batchNumber, obj_row.warehouse_no)
            if str_key not in dict_result:
                dict_result[str_key] = {
                    "itemType": util_safe_int(obj_row.itemType),
                    "unit": util_safe_int(obj_row.unit),
                }
        return dict_result

    def __query_item_metadata(self, obj_session, lst_item_refs):
        dict_result = {}
        dict_items_by_category = defaultdict(set)
        for str_item_no, n_item_category in lst_item_refs:
            if str_item_no:
                dict_items_by_category[util_safe_int(n_item_category)].add(str_item_no)

        self.__append_item_metadata(
            obj_session,
            CTableMaterial,
            [EItemCategory.PM, EItemCategory.MA, EItemCategory.AF],
            dict_items_by_category,
            dict_result,
            "subCategory",
        )
        self.__append_item_metadata(
            obj_session,
            CTableInproduct,
            [EItemCategory.INPRODUCT],
            dict_items_by_category,
            dict_result,
            "category",
        )
        self.__append_item_metadata(
            obj_session,
            CTableProduct,
            [EItemCategory.PRODUCT],
            dict_items_by_category,
            dict_result,
            "category",
        )
        self.__append_item_metadata(
            obj_session,
            CTableGoods,
            [EItemCategory.GOODS],
            dict_items_by_category,
            dict_result,
            "subCategory",
        )
        return dict_result

    def __append_item_metadata(
        self,
        obj_session,
        obj_table,
        lst_categories,
        dict_items_by_category,
        dict_result,
        str_sub_category_field,
    ):
        for n_category in lst_categories:
            lst_item_nos = list(dict_items_by_category.get(n_category, []))
            if not lst_item_nos:
                continue
            obj_sub_category = getattr(obj_table, str_sub_category_field)
            lst_rows = (
                obj_session.query(obj_table.no, obj_sub_category.label("itemSubCategory"))
                .filter(obj_table.no.in_(lst_item_nos))
                .all()
            )
            for obj_row in lst_rows:
                dict_result[(obj_row.no or "", n_category)] = {
                    "itemSubCategory": util_safe_int(obj_row.itemSubCategory),
                }

    def __query_reservations(self, obj_session, n_query_timestamp):
        lst_rows = (
            obj_session.query(
                CTableWarehouseInventoryReservation.item_no,
                CTableWarehouseInventoryReservation.batchNumber,
                CTableWarehouseInventoryReservation.warehouse_no,
                func.sum(CTableWarehouseInventoryReservation.reservedQuantity).label("reservedQuantity"),
                func.sum(CTableWarehouseInventoryReservation.reservedValue).label("reservedValue"),
            )
            .filter(CTableWarehouseInventoryReservation.status == self.RESERVATION_STATUS_ACTIVE)
            .filter(CTableWarehouseInventoryReservation.date <= n_query_timestamp)
            .filter(
                (CTableWarehouseInventoryReservation.releaseTime == None)
                | (CTableWarehouseInventoryReservation.releaseTime > n_query_timestamp)
            )
            .group_by(
                CTableWarehouseInventoryReservation.item_no,
                CTableWarehouseInventoryReservation.batchNumber,
                CTableWarehouseInventoryReservation.warehouse_no,
            )
            .all()
        )
        return {
            self.__stock_key(obj_row.item_no, obj_row.batchNumber, obj_row.warehouse_no): {
                "reservedQuantity": util_round_quantity(obj_row.reservedQuantity),
                "reservedValue": util_round_amount(obj_row.reservedValue),
            }
            for obj_row in lst_rows
        }

    def __query_quality_holds(self, obj_session, n_query_timestamp):
        lst_rows = (
            obj_session.query(
                CTableWarehouseQualityHold.item_no,
                CTableWarehouseQualityHold.batchNumber,
                CTableWarehouseQualityHold.warehouse_no,
                func.sum(CTableWarehouseQualityHold.holdQuantity).label("holdQuantity"),
                func.sum(CTableWarehouseQualityHold.holdValue).label("holdValue"),
            )
            .filter(CTableWarehouseQualityHold.status == self.QUALITY_HOLD_STATUS_ACTIVE)
            .filter(CTableWarehouseQualityHold.date <= n_query_timestamp)
            .group_by(
                CTableWarehouseQualityHold.item_no,
                CTableWarehouseQualityHold.batchNumber,
                CTableWarehouseQualityHold.warehouse_no,
            )
            .all()
        )
        return {
            self.__stock_key(obj_row.item_no, obj_row.batchNumber, obj_row.warehouse_no): {
                "qualityHoldQuantity": util_round_quantity(obj_row.holdQuantity),
                "qualityHoldValue": util_round_amount(obj_row.holdValue),
            }
            for obj_row in lst_rows
        }

    def __query_pallets(self, obj_session, n_query_timestamp, str_warehouse_no, n_item_category):
        lst_filters = [CTableWarehousePalletMovement.date <= n_query_timestamp]
        if str_warehouse_no:
            lst_filters.append(CTableWarehousePalletMovement.warehouse_no == str_warehouse_no)
        if n_item_category:
            lst_filters.append(CTableWarehousePalletMovement.itemCategory == n_item_category)
        lst_rows = (
            obj_session.query(
                CTableWarehousePalletMovement.warehouse_no,
                CTableWarehousePalletMovement.itemCategory,
                CTableWarehousePalletMovement.palletStatus,
                func.sum(CTableWarehousePalletMovement.palletCount).label("palletCount"),
            )
            .filter(*lst_filters)
            .group_by(
                CTableWarehousePalletMovement.warehouse_no,
                CTableWarehousePalletMovement.itemCategory,
                CTableWarehousePalletMovement.palletStatus,
            )
            .all()
        )
        dict_result = {"byWarehouse": defaultdict(lambda: {"usedPallets": 0.0, "reservedPallets": 0.0}),
                       "byCategory": defaultdict(float)}
        for obj_row in lst_rows:
            f_pallet_count = util_safe_float(obj_row.palletCount)
            if obj_row.palletStatus == self.PALLET_STATUS_USED:
                dict_result["byWarehouse"][obj_row.warehouse_no]["usedPallets"] += f_pallet_count
                dict_result["byCategory"][util_safe_int(obj_row.itemCategory)] += f_pallet_count
            elif obj_row.palletStatus == self.PALLET_STATUS_RESERVED:
                dict_result["byWarehouse"][obj_row.warehouse_no]["reservedPallets"] += f_pallet_count
        return dict_result

    def __query_capacity(self, obj_session, str_warehouse_no):
        lst_filters = [CTableShipWarehouseContract.category == EShipWarehouseCat.WAREHOUSE]
        if str_warehouse_no:
            lst_filters.append(CTableShipWarehouseContract.sw_alias_no == str_warehouse_no)
        lst_rows = (
            obj_session.query(
                CTableShipWarehouseContract.sw_alias_no,
                CTableShipWarehouseAlias.name,
                CTableShipWarehouseAlias.type,
                func.sum(CTableShipWarehouse.maxCapacity).label("totalPallets"),
            )
            .join(
                CTableShipWarehouse,
                CTableShipWarehouse.no == CTableShipWarehouseContract.item_no,
            )
            .outerjoin(
                CTableShipWarehouseAlias,
                CTableShipWarehouseAlias.no == CTableShipWarehouseContract.sw_alias_no,
            )
            .filter(*lst_filters)
            .group_by(
                CTableShipWarehouseContract.sw_alias_no,
                CTableShipWarehouseAlias.name,
                CTableShipWarehouseAlias.type,
            )
            .all()
        )
        return {
            obj_row.sw_alias_no: {
                "warehouseNo": obj_row.sw_alias_no or "",
                "warehouseName": obj_row.name or "",
                "warehouseType": util_safe_int(obj_row.type),
                "totalPallets": util_round_quantity(obj_row.totalPallets),
            }
            for obj_row in lst_rows
        }

    def __query_safety_stock(self, obj_session, n_query_timestamp):
        lst_rows = (
            obj_session.query(CTableItemSafetyStock)
            .filter(CTableItemSafetyStock.status == self.STATUS_ACTIVE)
            .all()
        )
        dict_result = {}
        for obj_row in lst_rows:
            n_effective = util_safe_int(obj_row.effectiveDate)
            n_expiry = util_safe_int(obj_row.expiryDate)
            if n_effective and n_effective > n_query_timestamp:
                continue
            if n_expiry and n_expiry < n_query_timestamp:
                continue
            dict_result[(obj_row.item_no or "", obj_row.warehouse_no or "")] = util_round_quantity(obj_row.safetyStock)
        return dict_result

    def __query_risk_rules(self, obj_session):
        lst_rows = (
            obj_session.query(CTableWarehouseRiskRule)
            .filter(CTableWarehouseRiskRule.status == self.STATUS_ACTIVE)
            .all()
        )
        return {
            obj_row.riskType: {
                "riskLevel": util_safe_int(obj_row.riskLevel),
                "messageCode": obj_row.messageCode or "",
                "recommendedActionCode": obj_row.recommendedActionCode or "",
            }
            for obj_row in lst_rows
        }

    def __query_pending_tasks(self, obj_session, str_warehouse_no, n_end_timestamp):
        lst_filters = [
            CTableWorkflowTaskState.taskStatus.in_([
                EWorkflowTaskStatus.PENDING,
                EWorkflowTaskStatus.PARTIAL,
                EWorkflowTaskStatus.BLOCKED,
            ]),
            CTableWorkflowTaskState.dueTimestamp <= n_end_timestamp,
        ]
        if str_warehouse_no:
            lst_filters.append(CTableWorkflowTaskState.warehouse_no == str_warehouse_no)
        lst_rows = (
            obj_session.query(CTableWorkflowTaskState)
            .filter(*lst_filters)
            .order_by(CTableWorkflowTaskState.dueTimestamp.asc())
            .limit(20)
            .all()
        )
        dict_warehouse_names = self.__query_warehouse_names(
            obj_session,
            [obj_row.warehouse_no for obj_row in lst_rows],
        )
        return [self.__task_to_dict(obj_row, dict_warehouse_names) for obj_row in lst_rows]

    def __query_warehouse_names(self, obj_session, lst_warehouse_nos):
        lst_values = [str_no for str_no in set(lst_warehouse_nos) if str_no]
        if not lst_values:
            return {}
        lst_rows = (
            obj_session.query(CTableShipWarehouseAlias.no, CTableShipWarehouseAlias.name)
            .filter(CTableShipWarehouseAlias.no.in_(lst_values))
            .all()
        )
        return {obj_row.no: obj_row.name or "" for obj_row in lst_rows}

    def __query_value_trend(
        self,
        obj_session,
        n_query_timestamp,
        str_timezone,
        str_warehouse_no,
        n_item_category,
        n_trend_days,
    ):
        n_trend_days = 7 if util_safe_int(n_trend_days) != 7 else 7
        obj_query_date = self.__query_local_date(n_query_timestamp, str_timezone)
        obj_start_date = obj_query_date - timedelta(days=n_trend_days - 1)
        obj_base_date = obj_query_date - timedelta(days=n_trend_days)

        dict_stat_trend = self.__query_value_trend_from_statistics(
            obj_session,
            obj_base_date,
            obj_start_date,
            obj_query_date,
            str_timezone,
            str_warehouse_no,
            n_item_category,
        )
        if dict_stat_trend.get("canUse"):
            return dict_stat_trend

        return self.__query_value_trend_from_records(
            obj_session,
            obj_base_date,
            obj_start_date,
            obj_query_date,
            str_timezone,
            str_warehouse_no,
            n_item_category,
        )

    def __query_value_trend_from_statistics(
        self,
        obj_session,
        obj_base_date,
        obj_start_date,
        obj_query_date,
        str_timezone,
        str_warehouse_no,
        n_item_category,
    ):
        str_stat_timezone = str_timezone or "UTC"
        lst_filters = [
            CTableInventoryMonthStatistic.category.in_(self.__target_categories()),
            CTableInventoryMonthStatistic.date <= obj_base_date,
            CTableInventoryMonthStatistic.timezone == str_stat_timezone,
        ]
        if str_warehouse_no:
            lst_filters.append(CTableInventoryMonthStatistic.warehouse_no == str_warehouse_no)
        if n_item_category:
            lst_filters.append(CTableInventoryMonthStatistic.category == n_item_category)

        lst_stat_rows = (
            obj_session.query(CTableInventoryMonthStatistic)
            .filter(*lst_filters)
            .order_by(CTableInventoryMonthStatistic.date.asc(), CTableInventoryMonthStatistic.id.asc())
            .all()
        )
        if not lst_stat_rows:
            return {"canUse": False}

        dict_base_by_key = {}
        for obj_row in lst_stat_rows:
            tuple_key = (obj_row.warehouse_no or "", util_safe_int(obj_row.category))
            dict_base_by_key[tuple_key] = {
                "date": obj_row.date,
                "value": util_safe_float(obj_row.endAmount),
            }

        lst_delta_filters = [
            CTableInventoryDelta.category.in_(self.__target_categories()),
            CTableInventoryDelta.date <= obj_query_date,
            CTableInventoryDelta.timezone == str_stat_timezone,
        ]
        if str_warehouse_no:
            lst_delta_filters.append(CTableInventoryDelta.warehouse_no == str_warehouse_no)
        if n_item_category:
            lst_delta_filters.append(CTableInventoryDelta.category == n_item_category)

        lst_delta_rows = (
            obj_session.query(CTableInventoryDelta)
            .filter(*lst_delta_filters)
            .all()
        )
        obj_latest_delta_date = max([obj_row.date for obj_row in lst_delta_rows], default=None)
        if obj_latest_delta_date and obj_latest_delta_date < obj_query_date:
            return {"canUse": False}
        if not obj_latest_delta_date and obj_base_date < obj_query_date:
            return {"canUse": False}

        dict_values = defaultdict(float)
        dict_base_values = defaultdict(float)
        for tuple_key, dict_base in dict_base_by_key.items():
            n_category = tuple_key[1]
            dict_values[n_category] += util_safe_float(dict_base.get("value"))
            dict_base_values[n_category] += util_safe_float(dict_base.get("value"))

        dict_daily_delta = defaultdict(lambda: defaultdict(float))
        for obj_row in lst_delta_rows:
            tuple_key = (obj_row.warehouse_no or "", util_safe_int(obj_row.category))
            dict_base = dict_base_by_key.get(tuple_key)
            if not dict_base or obj_row.date <= dict_base.get("date"):
                continue
            dict_daily_delta[obj_row.date][tuple_key[1]] += (
                util_safe_float(obj_row.inAmount) - util_safe_float(obj_row.outAmount)
            )

        lst_value_trend = []
        dict_query_values = {}
        for obj_date in self.__date_range(obj_base_date + timedelta(days=1), obj_query_date):
            for n_category, f_delta in dict_daily_delta.get(obj_date, {}).items():
                dict_values[n_category] += f_delta
            if obj_date >= obj_start_date:
                for n_category in self.__target_categories():
                    if n_item_category and n_category != n_item_category:
                        continue
                    lst_value_trend.append({
                        "date": obj_date.strftime("%Y-%m-%d"),
                        "itemCategory": n_category,
                        "inventoryValue": util_round_amount(dict_values.get(n_category, 0.0)),
                    })
            if obj_date == obj_query_date:
                dict_query_values = dict(dict_values)

        return {
            "canUse": True,
            "valueTrend": lst_value_trend,
            "trendByCategory": self.__build_trend_ratio(dict_base_values, dict_query_values),
        }

    def __query_value_trend_from_records(
        self,
        obj_session,
        obj_base_date,
        obj_start_date,
        obj_query_date,
        str_timezone,
        str_warehouse_no,
        n_item_category,
    ):
        dict_values_by_date = {}
        for obj_date in self.__date_range(obj_base_date, obj_query_date):
            n_end_timestamp = self.__business_day_end_timestamp(obj_date, str_timezone)
            dict_values_by_date[obj_date] = self.__query_record_value_by_category(
                obj_session,
                n_end_timestamp,
                str_warehouse_no,
                n_item_category,
            )

        lst_value_trend = []
        for obj_date in self.__date_range(obj_start_date, obj_query_date):
            dict_values = dict_values_by_date.get(obj_date, {})
            for n_category in self.__target_categories():
                if n_item_category and n_category != n_item_category:
                    continue
                lst_value_trend.append({
                    "date": obj_date.strftime("%Y-%m-%d"),
                    "itemCategory": n_category,
                    "inventoryValue": util_round_amount(dict_values.get(n_category, 0.0)),
                })

        return {
            "canUse": True,
            "valueTrend": lst_value_trend,
            "trendByCategory": self.__build_trend_ratio(
                dict_values_by_date.get(obj_base_date, {}),
                dict_values_by_date.get(obj_query_date, {}),
            ),
        }

    def __query_record_value_by_category(self, obj_session, n_end_timestamp, str_warehouse_no, n_item_category):
        lst_filters = [
            CTableInventoryRec.itemCategory.in_(self.__target_categories()),
            CTableInventoryRec.date <= n_end_timestamp,
        ]
        if str_warehouse_no:
            lst_filters.append(CTableInventoryRec.warehouse_no == str_warehouse_no)
        if n_item_category:
            lst_filters.append(CTableInventoryRec.itemCategory == n_item_category)

        obj_signed_amount = func.sum(
            case(
                (CTableInventoryRec.category == EInventoryCategory.IN, CTableInventoryRec.amount),
                (CTableInventoryRec.category == EInventoryCategory.OUT, -CTableInventoryRec.amount),
                else_=0,
            )
        ).label("inventoryValue")
        lst_rows = (
            obj_session.query(CTableInventoryRec.itemCategory, obj_signed_amount)
            .filter(*lst_filters)
            .group_by(CTableInventoryRec.itemCategory)
            .all()
        )
        return {
            util_safe_int(obj_row.itemCategory): util_safe_float(obj_row.inventoryValue)
            for obj_row in lst_rows
        }

    def __build_trend_ratio(self, dict_base_values, dict_query_values):
        dict_result = {}
        for n_category in self.__target_categories():
            f_base_value = util_safe_float(dict_base_values.get(n_category))
            f_query_value = util_safe_float(dict_query_values.get(n_category))
            if not f_base_value:
                dict_result[n_category] = 0.0
            else:
                dict_result[n_category] = util_round_quantity(
                    (f_query_value - f_base_value) / f_base_value * 100
                )
        return dict_result

    def __date_range(self, obj_start_date, obj_end_date):
        obj_current = obj_start_date
        while obj_current <= obj_end_date:
            yield obj_current
            obj_current = obj_current + timedelta(days=1)

    def __business_day_end_timestamp(self, obj_date, str_timezone):
        try:
            obj_tz = ZoneInfo(str_timezone or "UTC")
        except Exception:
            obj_tz = timezone.utc
        obj_local = datetime(
            obj_date.year,
            obj_date.month,
            obj_date.day,
            23,
            59,
            59,
            tzinfo=obj_tz,
        )
        return int(obj_local.astimezone(timezone.utc).timestamp())

    def __build_payload(
        self,
        n_query_timestamp,
        str_timezone,
        dict_range,
        lst_inventory_rows,
        dict_reservations,
        dict_quality_holds,
        dict_pallets,
        dict_capacity,
        lst_risks,
        lst_tasks,
        lst_inventory_detail,
        b_include_inventory,
        b_risk_only,
        dict_trend,
    ):
        dict_category = self.__build_category_summary(
            lst_inventory_rows,
            dict_reservations,
            dict_quality_holds,
            dict_pallets,
            dict_trend.get("trendByCategory", {}),
        )
        lst_capacity = self.__build_capacity_summary(dict_capacity, dict_pallets)
        dict_summary = self.__build_summary(dict_category, lst_capacity, lst_risks, lst_tasks)
        return {
            "serverTimestamp": n_query_timestamp,
            "timezone": str_timezone or "UTC",
            "range": dict_range,
            "summary": dict_summary,
            "inventoryValueByCategory": list(dict_category.values()),
            "capacityByWarehouse": lst_capacity,
            "riskAlerts": lst_risks,
            "pendingTasks": lst_tasks,
            "valueTrend": dict_trend.get("valueTrend", []),
            "inventory": self.__filter_inventory_by_risk(
                lst_inventory_detail,
                lst_risks,
            ) if b_include_inventory and b_risk_only else (lst_inventory_detail if b_include_inventory else []),
        }

    def __build_category_summary(
        self,
        lst_inventory_rows,
        dict_reservations,
        dict_quality_holds,
        dict_pallets,
        dict_trend_by_category=None,
    ):
        dict_trend_by_category = dict_trend_by_category or {}
        dict_category = {}
        for n_category in self.__target_categories():
            dict_category[n_category] = {
                "itemCategory": n_category,
                "inventoryValue": 0.0,
                "reservedValue": 0.0,
                "availableValue": 0.0,
                "qualityHoldValue": 0.0,
                "quantity": 0.0,
                "unit": 0,
                "palletCount": util_round_quantity(dict_pallets["byCategory"].get(n_category, 0.0)),
                "itemCount": 0,
                "valueRatio": 0.0,
                "trend7Days": 0.0,
            }
        dict_items = defaultdict(set)
        for dict_row in lst_inventory_rows:
            n_category = util_safe_int(dict_row.get("itemCategory"))
            dict_summary = dict_category.setdefault(n_category, {
                "itemCategory": n_category,
                "inventoryValue": 0.0,
                "reservedValue": 0.0,
                "availableValue": 0.0,
                "qualityHoldValue": 0.0,
                "quantity": 0.0,
                "unit": 0,
                "palletCount": util_round_quantity(dict_pallets["byCategory"].get(n_category, 0.0)),
                "itemCount": 0,
                "valueRatio": 0.0,
                "trend7Days": 0.0,
            })
            str_key = self.__stock_key(
                dict_row.get("itemNo"),
                dict_row.get("batchNo"),
                dict_row.get("warehouseNo"),
            )
            f_reserved_value = util_safe_float(dict_reservations.get(str_key, {}).get("reservedValue"))
            f_quality_value = util_safe_float(dict_quality_holds.get(str_key, {}).get("qualityHoldValue"))
            dict_summary["inventoryValue"] += util_safe_float(dict_row.get("inventoryValue"))
            dict_summary["reservedValue"] += f_reserved_value
            dict_summary["qualityHoldValue"] += f_quality_value
            dict_summary["quantity"] += util_safe_float(dict_row.get("currentQuantity"))
            dict_items[n_category].add(dict_row.get("itemNo"))
        f_total_value = sum(dict_row["inventoryValue"] for dict_row in dict_category.values())
        for n_category, dict_summary in dict_category.items():
            dict_summary["availableValue"] = max(
                dict_summary["inventoryValue"]
                - dict_summary["reservedValue"]
                - dict_summary["qualityHoldValue"],
                0.0,
            )
            dict_summary["inventoryValue"] = util_round_amount(dict_summary["inventoryValue"])
            dict_summary["reservedValue"] = util_round_amount(dict_summary["reservedValue"])
            dict_summary["availableValue"] = util_round_amount(dict_summary["availableValue"])
            dict_summary["qualityHoldValue"] = util_round_amount(dict_summary["qualityHoldValue"])
            dict_summary["quantity"] = util_round_quantity(dict_summary["quantity"])
            dict_summary["palletCount"] = util_round_quantity(dict_summary["palletCount"])
            dict_summary["itemCount"] = len(dict_items[n_category])
            dict_summary["valueRatio"] = util_round_quantity(dict_summary["inventoryValue"] / f_total_value * 100) if f_total_value else 0.0
            dict_summary["trend7Days"] = util_round_quantity(dict_trend_by_category.get(n_category, 0.0))
        return dict_category

    def __build_capacity_summary(self, dict_capacity, dict_pallets):
        lst_results = []
        set_warehouse_nos = set(dict_capacity.keys()) | set(dict_pallets["byWarehouse"].keys())
        for str_warehouse_no in sorted(set_warehouse_nos):
            dict_base = dict_capacity.get(str_warehouse_no, {
                "warehouseNo": str_warehouse_no or "",
                "warehouseName": "",
                "warehouseType": 0,
                "totalPallets": 0.0,
            })
            dict_pallet = dict_pallets["byWarehouse"].get(str_warehouse_no, {})
            f_used = util_safe_float(dict_pallet.get("usedPallets"))
            f_reserved = util_safe_float(dict_pallet.get("reservedPallets"))
            f_total = util_safe_float(dict_base.get("totalPallets"))
            f_available = max(f_total - f_used - f_reserved, 0.0)
            f_rate = util_round_quantity(f_used / f_total * 100) if f_total else 0.0
            lst_results.append({
                "warehouseNo": dict_base.get("warehouseNo", ""),
                "warehouseName": dict_base.get("warehouseName", ""),
                "warehouseType": util_safe_int(dict_base.get("warehouseType")),
                "totalPallets": util_round_quantity(f_total),
                "usedPallets": util_round_quantity(f_used),
                "reservedPallets": util_round_quantity(f_reserved),
                "availablePallets": util_round_quantity(f_available),
                "utilizationRate": f_rate,
                "riskLevel": self.__capacity_risk_level(f_rate),
            })
        return lst_results

    def __build_summary(self, dict_category, lst_capacity, lst_risks, lst_tasks):
        f_total_value = sum(dict_row["inventoryValue"] for dict_row in dict_category.values())
        f_reserved_value = sum(dict_row["reservedValue"] for dict_row in dict_category.values())
        f_quality_value = sum(dict_row["qualityHoldValue"] for dict_row in dict_category.values())
        f_total_pallets = sum(util_safe_float(dict_row.get("totalPallets")) for dict_row in lst_capacity)
        f_used_pallets = sum(util_safe_float(dict_row.get("usedPallets")) for dict_row in lst_capacity)
        f_reserved_pallets = sum(util_safe_float(dict_row.get("reservedPallets")) for dict_row in lst_capacity)
        return {
            "totalInventoryValue": util_round_amount(f_total_value),
            "reservedInventoryValue": util_round_amount(f_reserved_value),
            "availableInventoryValue": util_round_amount(max(f_total_value - f_reserved_value - f_quality_value, 0.0)),
            "qualityHoldInventoryValue": util_round_amount(f_quality_value),
            "totalPallets": util_round_quantity(f_total_pallets),
            "usedPallets": util_round_quantity(f_used_pallets),
            "reservedPallets": util_round_quantity(f_reserved_pallets),
            "availablePallets": util_round_quantity(max(f_total_pallets - f_used_pallets - f_reserved_pallets, 0.0)),
            "riskAlertCount": len(lst_risks),
            "pendingInboundCount": len([dict_row for dict_row in lst_tasks if dict_row.get("taskType") in [EWorkflowTaskType.GOODS_RECEIPT, EWorkflowTaskType.INBOUND]]),
            "pendingOutboundCount": len([dict_row for dict_row in lst_tasks if dict_row.get("taskType") in [EWorkflowTaskType.OUTBOUND, EWorkflowTaskType.SHIPMENT]]),
        }

    def __build_inventory_detail(self, lst_inventory_rows, dict_reservations, dict_quality_holds):
        lst_results = []
        for dict_row in lst_inventory_rows:
            str_key = self.__stock_key(dict_row.get("itemNo"), dict_row.get("batchNo"), dict_row.get("warehouseNo"))
            f_reserved = util_safe_float(dict_reservations.get(str_key, {}).get("reservedQuantity"))
            f_quality = util_safe_float(dict_quality_holds.get(str_key, {}).get("qualityHoldQuantity"))
            f_quantity = util_safe_float(dict_row.get("currentQuantity"))
            if f_quantity == 0:
                continue
            dict_data = dict(dict_row)
            dict_data.update({
                "currentQuantity": util_round_quantity(dict_row.get("currentQuantity")),
                "inventoryValue": util_round_amount(dict_row.get("inventoryValue")),
                "reservedQuantity": util_round_quantity(f_reserved),
                "availableQuantity": util_round_quantity(max(f_quantity - f_reserved - f_quality, 0.0)),
                "qualityHoldQuantity": util_round_quantity(f_quality),
                "reservedValue": util_round_amount(dict_reservations.get(str_key, {}).get("reservedValue")),
                "availableValue": util_round_amount(max(
                    util_safe_float(dict_row.get("inventoryValue"))
                    - util_safe_float(dict_reservations.get(str_key, {}).get("reservedValue"))
                    - util_safe_float(dict_quality_holds.get(str_key, {}).get("qualityHoldValue")),
                    0.0,
                )),
                "qualityHoldValue": util_round_amount(dict_quality_holds.get(str_key, {}).get("qualityHoldValue")),
            })
            lst_results.append(dict_data)
        return lst_results

    def __build_risk_alerts(
        self,
        lst_inventory_rows,
        dict_safety_stock,
        dict_risk_rules,
        n_query_timestamp,
        b_risk_only,
    ):
        lst_results = []
        for dict_row in lst_inventory_rows:
            if util_safe_float(dict_row.get("currentQuantity")) <= 0:
                continue
            lst_row_risks = []
            n_item_category = util_safe_int(dict_row.get("itemCategory"))
            n_valid_date = util_safe_int(dict_row.get("validDate"))
            n_valid_days = util_safe_int(dict_row.get("validDays"))
            if n_valid_date and n_valid_days and n_item_category not in [EItemCategory.MA, EItemCategory.AF]:
                n_remaining = n_valid_date - n_query_timestamp
                if n_remaining <= (n_valid_days * 86400 / 3):
                    lst_row_risks.append(EWarehouseRiskType.SHELF_LIFE_LT_ONE_THIRD)
            n_first_inbound = util_safe_int(dict_row.get("firstInboundTimestamp"))
            if n_first_inbound and (n_query_timestamp - n_first_inbound) > 30 * 86400:
                lst_row_risks.append(EWarehouseRiskType.TURNOVER_OVER_30_DAYS)
            f_safety_stock = util_safe_float(dict_safety_stock.get((dict_row.get("itemNo"), dict_row.get("warehouseNo"))))
            if not f_safety_stock:
                f_safety_stock = util_safe_float(dict_safety_stock.get((dict_row.get("itemNo"), "")))
            if f_safety_stock and util_safe_float(dict_row.get("availableQuantity")) < f_safety_stock:
                lst_row_risks.append(EWarehouseRiskType.BELOW_SAFETY_STOCK)
            for str_risk_type in lst_row_risks:
                lst_results.append(
                    self.__risk_to_dict(
                        dict_row,
                        str_risk_type,
                        f_safety_stock,
                        n_query_timestamp,
                        dict_risk_rules,
                    )
                )
        return lst_results

    def __risk_to_dict(self, dict_row, str_risk_type, f_safety_stock, n_query_timestamp, dict_risk_rules):
        n_first_inbound = util_safe_int(dict_row.get("firstInboundTimestamp"))
        n_days_in_stock = int((n_query_timestamp - n_first_inbound) / 86400) if n_first_inbound else 0
        dict_rule = dict_risk_rules.get(str_risk_type, {})
        f_remaining_shelf_life_ratio = self.__remaining_shelf_life_ratio(dict_row, n_query_timestamp)
        return {
            "alertId": "%s-%s-%s-%s" % (
                str_risk_type,
                dict_row.get("warehouseNo", ""),
                dict_row.get("itemNo", ""),
                dict_row.get("batchNo", ""),
            ),
            "riskType": str_risk_type,
            "riskLevel": self.__risk_level_value(dict_rule.get("riskLevel"), str_risk_type),
            "itemNo": dict_row.get("itemNo", ""),
            "itemName": dict_row.get("itemName", ""),
            "itemCategory": util_safe_int(dict_row.get("itemCategory")),
            "batchNo": dict_row.get("batchNo", ""),
            "warehouseNo": dict_row.get("warehouseNo", ""),
            "warehouseName": dict_row.get("warehouseName", ""),
            "quantity": util_round_quantity(dict_row.get("currentQuantity")),
            "unit": util_safe_int(dict_row.get("unit")),
            "inventoryValue": util_round_amount(dict_row.get("inventoryValue")),
            "daysInStock": n_days_in_stock,
            "validDate": util_safe_int(dict_row.get("validDate")),
            "remainingShelfLifeRatio": f_remaining_shelf_life_ratio,
            "safetyStock": util_round_quantity(f_safety_stock),
            "messageCode": dict_rule.get("messageCode") or self.__risk_message_code(str_risk_type),
            "messageParams": {
                "currentQuantity": util_round_quantity(dict_row.get("currentQuantity")),
                "daysInStock": n_days_in_stock,
                "validDate": util_safe_int(dict_row.get("validDate")),
                "remainingShelfLifeRatio": f_remaining_shelf_life_ratio,
                "safetyStock": util_round_quantity(f_safety_stock),
            },
            "recommendedActionCode": (
                dict_rule.get("recommendedActionCode")
                or self.__risk_action_code(str_risk_type)
            ),
        }

    def __filter_inventory_by_risk(self, lst_inventory_detail, lst_risks):
        set_risk_keys = {
            self.__stock_key(
                dict_risk.get("itemNo"),
                dict_risk.get("batchNo"),
                dict_risk.get("warehouseNo"),
            )
            for dict_risk in lst_risks
        }
        return [
            dict_row
            for dict_row in lst_inventory_detail
            if self.__stock_key(
                dict_row.get("itemNo"),
                dict_row.get("batchNo"),
                dict_row.get("warehouseNo"),
            ) in set_risk_keys
        ]

    def __task_to_dict(self, obj_row, dict_warehouse_names=None):
        dict_warehouse_names = dict_warehouse_names or {}
        return {
            "taskId": obj_row.taskId or "",
            "taskType": util_safe_int(obj_row.taskType),
            "refCategory": util_safe_int(obj_row.refCategory),
            "sourceNo": obj_row.ref_no or "",
            "sourceSubNo": obj_row.ref_sub_no or "",
            "itemNo": obj_row.item_no or "",
            "itemName": obj_row.item_name or "",
            "itemCategory": util_safe_int(obj_row.itemCategory),
            "batchNo": obj_row.batchNumber or "",
            "expectedQuantity": util_round_quantity(obj_row.expectedQuantity),
            "processedQuantity": util_round_quantity(obj_row.processedQuantity),
            "remainingQuantity": util_round_quantity(max(
                util_safe_float(obj_row.expectedQuantity) - util_safe_float(obj_row.processedQuantity),
                0.0,
            )),
            "unit": util_safe_int(obj_row.unit),
            "palletCount": util_round_quantity(obj_row.palletCount),
            "warehouseNo": obj_row.warehouse_no or "",
            "warehouseName": dict_warehouse_names.get(obj_row.warehouse_no, ""),
            "dueTimestamp": util_safe_int(obj_row.dueTimestamp),
            "taskStatus": util_safe_int(obj_row.taskStatus),
            "ownerDepartment": util_safe_int(obj_row.ownerDepartment),
            "blockReason": obj_row.blockReason or "",
        }

    def __target_categories(self):
        return [
            EItemCategory.PM,
            EItemCategory.MA,
            EItemCategory.AF,
            EItemCategory.INPRODUCT,
            EItemCategory.PRODUCT,
        ]

    def __stock_key(self, str_item_no, str_batch_no, str_warehouse_no):
        return "%s|%s|%s" % (str_item_no or "", str_batch_no or "", str_warehouse_no or "")

    def __stock_tuple(self, str_item_no, str_batch_no, str_warehouse_no):
        return (str_item_no or "", str_batch_no or "", str_warehouse_no or "")

    def __stock_tuple_filter(self, obj_table, set_stock_tuples):
        lst_conditions = []
        for str_item_no, str_batch_no, str_warehouse_no in set_stock_tuples:
            lst_conditions.append(and_(
                self.__text_value_filter(obj_table.item_no, str_item_no),
                self.__text_value_filter(obj_table.batchNumber, str_batch_no),
                self.__text_value_filter(obj_table.warehouse_no, str_warehouse_no),
            ))
        return or_(*lst_conditions)

    def __text_value_filter(self, obj_column, str_value):
        if str_value:
            return obj_column == str_value
        return or_(obj_column == "", obj_column.is_(None))

    def __capacity_risk_level(self, f_rate):
        if f_rate >= 90:
            return EWarehouseRiskLevel.DANGER
        if f_rate >= 75:
            return EWarehouseRiskLevel.WARNING
        return EWarehouseRiskLevel.NORMAL

    def __risk_level_value(self, n_risk_level, str_risk_type):
        if n_risk_level:
            return n_risk_level
        if str_risk_type == EWarehouseRiskType.SHELF_LIFE_LT_ONE_THIRD:
            return EWarehouseRiskLevel.DANGER
        return EWarehouseRiskLevel.WARNING

    def __remaining_shelf_life_ratio(self, dict_row, n_query_timestamp):
        n_valid_days = util_safe_int(dict_row.get("validDays"))
        n_valid_date = util_safe_int(dict_row.get("validDate"))
        if not n_valid_days or not n_valid_date:
            return 0.0
        return round(max(n_valid_date - n_query_timestamp, 0) / float(n_valid_days * 86400), 4)

    def __risk_message_code(self, str_risk_type):
        dict_messages = {
            EWarehouseRiskType.TURNOVER_OVER_30_DAYS: "warehouse.risk.turnoverOver30Days",
            EWarehouseRiskType.SHELF_LIFE_LT_ONE_THIRD: "warehouse.risk.shelfLifeLtOneThird",
            EWarehouseRiskType.BELOW_SAFETY_STOCK: "warehouse.risk.belowSafetyStock",
        }
        return dict_messages.get(str_risk_type, "")

    def __risk_action_code(self, str_risk_type):
        dict_actions = {
            EWarehouseRiskType.TURNOVER_OVER_30_DAYS: "warehouse.action.reviewSlowMovingStock",
            EWarehouseRiskType.SHELF_LIFE_LT_ONE_THIRD: "warehouse.action.prioritizeIssueOrProduction",
            EWarehouseRiskType.BELOW_SAFETY_STOCK: "warehouse.action.createPurchaseRequest",
        }
        return dict_actions.get(str_risk_type, "")


class CWarehouseInventoryContextBuilder(object):
    def build(
        self,
        obj_session,
        n_query_timestamp,
        str_timezone,
        str_warehouse_no,
        n_item_category,
        str_item_no="",
        str_batch_no="",
        b_include_safety_stock=False,
        b_include_open_tasks=False,
        n_task_type=0,
    ):
        dict_dashboard = CWarehouseDashboardService().get_dashboard(
            n_date=n_query_timestamp,
            str_timezone=str_timezone,
            str_warehouse_no=str_warehouse_no,
            n_item_category=n_item_category,
            b_include_inventory=True,
            obj_session=obj_session,
        )
        lst_inventory = self.filter_inventory_rows(
            dict_dashboard.get("inventory", []),
            str_item_no,
            str_batch_no,
        )
        set_stock_keys = self.stock_keys_from_rows(lst_inventory)
        return {
            "dashboard": dict_dashboard,
            "inventoryRows": lst_inventory,
            "risks": self.group_risks(dict_dashboard.get("riskAlerts", [])),
            "pallets": self.query_pallet_counts(obj_session, n_query_timestamp, set_stock_keys),
            "sources": self.query_batch_sources(
                obj_session,
                [dict_row.get("batchNo") for dict_row in lst_inventory],
            ),
            "safetyStock": self.query_safety_stock(
                obj_session,
                n_query_timestamp,
                lst_inventory,
            ) if b_include_safety_stock else {},
            "openTasks": self.query_open_tasks(
                obj_session,
                n_query_timestamp,
                str_timezone,
                n_task_type,
                set_stock_keys,
            ) if b_include_open_tasks else {},
        }

    def filter_inventory_rows(self, lst_inventory, str_item_no="", str_batch_no=""):
        lst_results = []
        for dict_row in lst_inventory:
            if str_item_no and dict_row.get("itemNo") != str_item_no:
                continue
            if str_batch_no and dict_row.get("batchNo") != str_batch_no:
                continue
            lst_results.append(dict_row)
        return lst_results

    def stock_keys_from_rows(self, lst_inventory):
        return {
            self.stock_key(
                dict_row.get("itemNo"),
                dict_row.get("batchNo"),
                dict_row.get("warehouseNo"),
            )
            for dict_row in lst_inventory
        }

    def stock_key(self, str_item_no, str_batch_no, str_warehouse_no):
        return "%s|%s|%s" % (str_item_no or "", str_batch_no or "", str_warehouse_no or "")

    def group_risks(self, lst_risks):
        dict_result = defaultdict(lambda: {"riskTypes": [], "safetyStock": 0.0})
        for dict_risk in lst_risks:
            str_key = self.stock_key(
                dict_risk.get("itemNo"),
                dict_risk.get("batchNo"),
                dict_risk.get("warehouseNo"),
            )
            str_risk_type = dict_risk.get("riskType", "")
            if str_risk_type and str_risk_type not in dict_result[str_key]["riskTypes"]:
                dict_result[str_key]["riskTypes"].append(str_risk_type)
            if util_safe_float(dict_risk.get("safetyStock")):
                dict_result[str_key]["safetyStock"] = util_round_quantity(dict_risk.get("safetyStock"))
        return dict_result

    def query_pallet_counts(self, obj_session, n_query_timestamp, set_stock_keys=None):
        if set_stock_keys is not None and not set_stock_keys:
            return {}
        lst_filters = [
            CTableWarehousePalletMovement.palletStatus == CWarehouseDashboardService.PALLET_STATUS_USED,
            CTableWarehousePalletMovement.date <= n_query_timestamp,
        ]
        self.__append_stock_key_filters(
            lst_filters,
            set_stock_keys,
            CTableWarehousePalletMovement.item_no,
            CTableWarehousePalletMovement.batchNumber,
            CTableWarehousePalletMovement.warehouse_no,
        )
        lst_rows = (
            obj_session.query(
                CTableWarehousePalletMovement.item_no,
                CTableWarehousePalletMovement.batchNumber,
                CTableWarehousePalletMovement.warehouse_no,
                func.sum(CTableWarehousePalletMovement.palletCount).label("palletCount"),
            )
            .filter(*lst_filters)
            .group_by(
                CTableWarehousePalletMovement.item_no,
                CTableWarehousePalletMovement.batchNumber,
                CTableWarehousePalletMovement.warehouse_no,
            )
            .all()
        )
        return {
            self.stock_key(obj_row.item_no, obj_row.batchNumber, obj_row.warehouse_no): util_round_quantity(obj_row.palletCount)
            for obj_row in lst_rows
        }

    def query_batch_sources(self, obj_session, lst_batch_numbers):
        lst_batch_numbers = list({str_batch_no for str_batch_no in lst_batch_numbers if str_batch_no})
        if not lst_batch_numbers:
            return {}
        lst_rows = (
            obj_session.query(CTableBatchNumber)
            .filter(CTableBatchNumber.no.in_(lst_batch_numbers))
            .order_by(
                CTableBatchNumber.date.desc(),
                CTableBatchNumber.creationTime.desc(),
                CTableBatchNumber.id.desc(),
            )
            .all()
        )
        dict_result = {}
        for obj_row in lst_rows:
            str_batch_no = obj_row.no or ""
            if str_batch_no and str_batch_no not in dict_result:
                dict_result[str_batch_no] = {
                    "refNo": obj_row.ref_no or "",
                    "refCategory": util_safe_int(obj_row.refCategory),
                }
        return dict_result

    def query_safety_stock(self, obj_session, n_query_timestamp, lst_inventory):
        set_item_nos = {dict_row.get("itemNo") for dict_row in lst_inventory if dict_row.get("itemNo")}
        if not set_item_nos:
            return {}
        lst_rows = (
            obj_session.query(CTableItemSafetyStock)
            .filter(CTableItemSafetyStock.status == CWarehouseDashboardService.STATUS_ACTIVE)
            .filter(CTableItemSafetyStock.item_no.in_(list(set_item_nos)))
            .all()
        )
        dict_result = {}
        for obj_row in lst_rows:
            n_effective = util_safe_int(obj_row.effectiveDate)
            n_expiry = util_safe_int(obj_row.expiryDate)
            if n_effective and n_effective > n_query_timestamp:
                continue
            if n_expiry and n_expiry < n_query_timestamp:
                continue
            dict_result[(obj_row.item_no or "", obj_row.warehouse_no or "")] = util_round_quantity(obj_row.safetyStock)
        return dict_result

    def query_open_tasks(self, obj_session, n_query_timestamp, str_timezone, n_task_type, set_stock_keys=None):
        if set_stock_keys is not None and not set_stock_keys:
            return {}
        dict_range = self.__build_range(n_query_timestamp, str_timezone)
        lst_filters = [
            CTableWorkflowTaskState.taskStatus.in_([
                EWorkflowTaskStatus.PENDING,
                EWorkflowTaskStatus.PARTIAL,
                EWorkflowTaskStatus.BLOCKED,
            ]),
            CTableWorkflowTaskState.dueTimestamp <= dict_range["endTimestamp"],
        ]
        if n_task_type:
            lst_filters.append(CTableWorkflowTaskState.taskType == n_task_type)
        self.__append_stock_key_filters(
            lst_filters,
            set_stock_keys,
            CTableWorkflowTaskState.item_no,
            CTableWorkflowTaskState.batchNumber,
            CTableWorkflowTaskState.warehouse_no,
        )
        lst_rows = obj_session.query(CTableWorkflowTaskState).filter(*lst_filters).all()
        dict_result = defaultdict(list)
        for obj_row in lst_rows:
            str_key = self.stock_key(obj_row.item_no, obj_row.batchNumber, obj_row.warehouse_no)
            if set_stock_keys and str_key not in set_stock_keys:
                continue
            dict_result[str_key].append(obj_row)
        return dict_result

    def __append_stock_key_filters(self, lst_filters, set_stock_keys, obj_item_column, obj_batch_column, obj_warehouse_column):
        if not set_stock_keys:
            return
        lst_item_nos = []
        lst_batch_numbers = []
        lst_warehouse_nos = []
        for str_key in set_stock_keys:
            str_item_no, str_batch_no, str_warehouse_no = str_key.split("|", 2)
            if str_item_no:
                lst_item_nos.append(str_item_no)
            if str_batch_no:
                lst_batch_numbers.append(str_batch_no)
            if str_warehouse_no:
                lst_warehouse_nos.append(str_warehouse_no)
        if lst_item_nos:
            lst_filters.append(obj_item_column.in_(list(set(lst_item_nos))))
        if lst_batch_numbers:
            lst_filters.append(obj_batch_column.in_(list(set(lst_batch_numbers))))
        if lst_warehouse_nos:
            lst_filters.append(obj_warehouse_column.in_(list(set(lst_warehouse_nos))))

    def __build_range(self, n_timestamp, str_timezone):
        try:
            obj_tz = ZoneInfo(str_timezone or "UTC")
        except Exception:
            obj_tz = timezone.utc
        obj_local = datetime.fromtimestamp(n_timestamp, timezone.utc).astimezone(obj_tz)
        obj_start_local = obj_local.replace(hour=0, minute=0, second=0, microsecond=0)
        n_start = int(obj_start_local.astimezone(timezone.utc).timestamp())
        return {
            "date": obj_local.strftime("%Y-%m-%d"),
            "startTimestamp": n_start,
            "endTimestamp": n_start + 86399,
        }


class CWarehouseInventoryService(object):
    def get_inventory(
        self,
        n_date=0,
        str_timezone="",
        str_warehouse_no="",
        n_item_category=0,
        str_item_no="",
        str_batch_no="",
        str_risk_type="",
        n_start=0,
        n_count=50,
        obj_session=None,
    ):
        if obj_session:
            return self.__get_inventory_with_session(
                obj_session,
                n_date,
                str_timezone,
                str_warehouse_no,
                n_item_category,
                str_item_no,
                str_batch_no,
                str_risk_type,
                n_start,
                n_count,
            )

        with CDBMgr() as obj_dbmgr:
            return self.__get_inventory_with_session(
                obj_dbmgr.get_session(),
                n_date,
                str_timezone,
                str_warehouse_no,
                n_item_category,
                str_item_no,
                str_batch_no,
                str_risk_type,
                n_start,
                n_count,
            )

    def __get_inventory_with_session(
        self,
        obj_session,
        n_date,
        str_timezone,
        str_warehouse_no,
        n_item_category,
        str_item_no,
        str_batch_no,
        str_risk_type,
        n_start,
        n_count,
    ):
        n_query_timestamp = n_date if n_date else int(time.time())
        obj_context_builder = CWarehouseInventoryContextBuilder()
        dict_context = obj_context_builder.build(
            obj_session=obj_session,
            n_query_timestamp=n_query_timestamp,
            str_timezone=str_timezone,
            str_warehouse_no=str_warehouse_no,
            n_item_category=n_item_category,
            str_item_no=str_item_no,
            str_batch_no=str_batch_no,
        )
        n_start = max(util_safe_int(n_start), 0)
        n_count = util_safe_int(n_count) if n_count else 50
        if n_count <= 0:
            n_count = 50
        n_total = 0
        lst_page = []

        for dict_row in dict_context.get("inventoryRows", []):
            if util_safe_float(dict_row.get("currentQuantity")) <= 0:
                continue
            str_key = obj_context_builder.stock_key(
                dict_row.get("itemNo"),
                dict_row.get("batchNo"),
                dict_row.get("warehouseNo"),
            )
            dict_risk = dict_context.get("risks", {}).get(str_key, {"riskTypes": [], "safetyStock": 0.0})
            dict_source = dict_context.get("sources", {}).get(dict_row.get("batchNo") or "", {})
            dict_inventory = self.__inventory_to_dict(
                dict_row,
                dict_risk,
                util_safe_float(dict_context.get("pallets", {}).get(str_key)),
                dict_source,
                n_query_timestamp,
            )
            if self.__is_inventory_matched(dict_inventory, str_risk_type):
                if n_total >= n_start and len(lst_page) < n_count:
                    lst_page.append(dict_inventory)
                n_total += 1
        return {
            "serverTimestamp": n_query_timestamp,
            "timezone": str_timezone or "UTC",
            "total": n_total,
            "count": len(lst_page),
            "start": n_start,
            "results": lst_page,
        }

    def __inventory_to_dict(self, dict_row, dict_risk, f_pallet_count, dict_source, n_query_timestamp):
        f_current_quantity = util_safe_float(dict_row.get("currentQuantity"))
        n_inventory_value = util_round_amount(dict_row.get("inventoryValue"))
        n_first_inbound = util_safe_int(dict_row.get("firstInboundTimestamp"))
        str_warehouse_no = dict_row.get("warehouseNo", "")
        str_item_no = dict_row.get("itemNo", "")
        str_batch_no = dict_row.get("batchNo", "")
        str_serial_no = dict_row.get("serialNo", "")
        return {
            "inventoryId": self.__inventory_id(str_warehouse_no, str_item_no, str_batch_no, str_serial_no),
            "warehouseNo": str_warehouse_no,
            "warehouseName": dict_row.get("warehouseName", ""),
            "itemNo": str_item_no,
            "itemName": dict_row.get("itemName", ""),
            "itemCategory": util_safe_int(dict_row.get("itemCategory")),
            "itemSubCategory": util_safe_int(dict_row.get("itemSubCategory")),
            "itemType": util_safe_int(dict_row.get("itemType")),
            "batchNo": str_batch_no,
            "serialNo": str_serial_no,
            "currentQuantity": util_round_quantity(f_current_quantity),
            "reservedQuantity": util_round_quantity(dict_row.get("reservedQuantity")),
            "availableQuantity": util_round_quantity(dict_row.get("availableQuantity")),
            "qualityHoldQuantity": util_round_quantity(dict_row.get("qualityHoldQuantity")),
            "unit": util_safe_int(dict_row.get("unit")),
            "unitCost": util_round_price(n_inventory_value / f_current_quantity) if f_current_quantity else 0.0,
            "inventoryValue": n_inventory_value,
            "reservedValue": util_round_amount(dict_row.get("reservedValue")),
            "availableValue": util_round_amount(dict_row.get("availableValue")),
            "qualityHoldValue": util_round_amount(dict_row.get("qualityHoldValue")),
            "palletCount": util_round_quantity(f_pallet_count),
            "safetyStock": util_round_quantity(dict_risk.get("safetyStock")),
            "validDays": util_safe_int(dict_row.get("validDays")),
            "validDate": util_safe_int(dict_row.get("validDate")),
            "firstInboundTimestamp": n_first_inbound,
            "daysInStock": int((n_query_timestamp - n_first_inbound) / 86400) if n_first_inbound else 0,
            "sourceNo": dict_source.get("refNo", ""),
            "sourceRefCategory": util_safe_int(dict_source.get("refCategory")),
            "qualityStatus": "hold" if util_safe_float(dict_row.get("qualityHoldQuantity")) else "released",
            "riskTypes": dict_risk.get("riskTypes", []),
        }

    def __is_inventory_matched(self, dict_inventory, str_risk_type):
        if str_risk_type and str_risk_type not in dict_inventory.get("riskTypes", []):
            return False
        return True

    def __inventory_id(self, str_warehouse_no, str_item_no, str_batch_no, str_serial_no):
        return "%s|%s|%s|%s" % (str_warehouse_no or "", str_item_no or "", str_batch_no or "", str_serial_no or "")


class CWarehouseInventoryLotService(object):
    def get_lots(
        self,
        n_date=0,
        str_timezone="",
        str_warehouse_no="",
        n_item_category=0,
        str_item_no="",
        str_batch_no="",
        str_risk_type="",
        n_task_type=0,
        str_availability="",
        str_keyword="",
        str_sort="",
        str_order="",
        n_start=0,
        n_count=50,
        obj_session=None,
    ):
        if obj_session:
            return self.__get_lots_with_session(
                obj_session,
                n_date,
                str_timezone,
                str_warehouse_no,
                n_item_category,
                str_item_no,
                str_batch_no,
                str_risk_type,
                n_task_type,
                str_availability,
                str_keyword,
                str_sort,
                str_order,
                n_start,
                n_count,
            )

        with CDBMgr() as obj_dbmgr:
            return self.__get_lots_with_session(
                obj_dbmgr.get_session(),
                n_date,
                str_timezone,
                str_warehouse_no,
                n_item_category,
                str_item_no,
                str_batch_no,
                str_risk_type,
                n_task_type,
                str_availability,
                str_keyword,
                str_sort,
                str_order,
                n_start,
                n_count,
            )

    def get_lot_detail(
        self,
        n_date=0,
        str_timezone="",
        str_warehouse_no="",
        str_item_no="",
        str_batch_no="",
        obj_session=None,
    ):
        if obj_session:
            return self.__get_lot_detail_with_session(
                obj_session,
                n_date,
                str_timezone,
                str_warehouse_no,
                str_item_no,
                str_batch_no,
            )

        with CDBMgr() as obj_dbmgr:
            return self.__get_lot_detail_with_session(
                obj_dbmgr.get_session(),
                n_date,
                str_timezone,
                str_warehouse_no,
                str_item_no,
                str_batch_no,
            )

    def __get_lots_with_session(
        self,
        obj_session,
        n_date,
        str_timezone,
        str_warehouse_no,
        n_item_category,
        str_item_no,
        str_batch_no,
        str_risk_type,
        n_task_type,
        str_availability,
        str_keyword,
        str_sort,
        str_order,
        n_start,
        n_count,
    ):
        n_query_timestamp = n_date if n_date else int(time.time())
        obj_context_builder = CWarehouseInventoryContextBuilder()
        dict_context = obj_context_builder.build(
            obj_session=obj_session,
            n_query_timestamp=n_query_timestamp,
            str_timezone=str_timezone,
            str_warehouse_no=str_warehouse_no,
            n_item_category=n_item_category,
            str_item_no=str_item_no,
            str_batch_no=str_batch_no,
            b_include_safety_stock=True,
            b_include_open_tasks=True,
            n_task_type=n_task_type,
        )

        n_start = max(util_safe_int(n_start), 0)
        n_count = util_safe_int(n_count) if n_count else 50
        if n_count <= 0:
            n_count = 50
        b_requires_full_result_set = bool(self.__sort_field(str_sort))
        lst_results = []
        lst_page = []
        n_total = 0
        dict_summary = self.__new_summary_accumulator()
        for dict_row in dict_context.get("inventoryRows", []):
            if util_safe_float(dict_row.get("currentQuantity")) == 0:
                continue
            str_key = obj_context_builder.stock_key(
                dict_row.get("itemNo"),
                dict_row.get("batchNo"),
                dict_row.get("warehouseNo"),
            )
            dict_lot = self.__lot_to_dict(
                dict_row,
                dict_context.get("risks", {}).get(str_key, {"riskTypes": []}),
                util_safe_float(dict_context.get("pallets", {}).get(str_key)),
                dict_context.get("sources", {}).get(dict_row.get("batchNo") or "", {}),
                dict_context.get("safetyStock", {}),
                dict_context.get("openTasks", {}).get(str_key, []),
                n_query_timestamp,
            )
            if self.__is_lot_matched(
                dict_lot,
                str_risk_type,
                str_availability,
                str_keyword,
            ):
                self.__accumulate_summary(dict_summary, dict_lot)
                if b_requires_full_result_set:
                    lst_results.append(dict_lot)
                elif n_total >= n_start and len(lst_page) < n_count:
                    lst_page.append(dict_lot)
                n_total += 1

        if b_requires_full_result_set:
            lst_results = self.__sort_lots(lst_results, str_sort, str_order)
            lst_page = lst_results[n_start:n_start + n_count]
        return {
            "serverTimestamp": n_query_timestamp,
            "timezone": str_timezone or "UTC",
            "total": n_total,
            "count": len(lst_page),
            "start": n_start,
            "summary": self.__finalize_summary(dict_summary),
            "results": lst_page,
        }

    def __get_lot_detail_with_session(
        self,
        obj_session,
        n_date,
        str_timezone,
        str_warehouse_no,
        str_item_no,
        str_batch_no,
    ):
        n_query_timestamp = n_date if n_date else int(time.time())
        dict_lots = self.__get_lots_with_session(
            obj_session=obj_session,
            n_date=n_query_timestamp,
            str_timezone=str_timezone,
            str_warehouse_no=str_warehouse_no,
            n_item_category=0,
            str_item_no=str_item_no,
            str_batch_no=str_batch_no,
            str_risk_type="",
            n_task_type=0,
            str_availability="",
            str_keyword="",
            str_sort="",
            str_order="",
            n_start=0,
            n_count=1,
        )
        dict_lot = dict_lots.get("results", [{}])[0] if dict_lots.get("results") else {}
        return {
            "lot": self.__detail_lot_to_dict(dict_lot),
            "inventoryRecords": self.__query_inventory_records(
                obj_session,
                n_query_timestamp,
                str_warehouse_no,
                str_item_no,
                str_batch_no,
            ),
            "reservations": self.__query_reservation_rows(
                obj_session,
                n_query_timestamp,
                str_warehouse_no,
                str_item_no,
                str_batch_no,
            ),
            "qualityHolds": self.__query_quality_hold_rows(
                obj_session,
                n_query_timestamp,
                str_warehouse_no,
                str_item_no,
                str_batch_no,
            ),
            "palletMovements": self.__query_pallet_movement_rows(
                obj_session,
                n_query_timestamp,
                str_warehouse_no,
                str_item_no,
                str_batch_no,
            ),
            "workflowTasks": self.__query_workflow_task_rows(
                obj_session,
                n_query_timestamp,
                str_timezone,
                str_warehouse_no,
                str_item_no,
                str_batch_no,
            ),
        }

    def __lot_to_dict(
        self,
        dict_row,
        dict_risk,
        f_pallet_count,
        dict_source,
        dict_safety_stock,
        lst_tasks,
        n_query_timestamp,
    ):
        f_current_quantity = util_safe_float(dict_row.get("currentQuantity"))
        n_inventory_value = util_round_amount(dict_row.get("inventoryValue"))
        str_warehouse_no = dict_row.get("warehouseNo", "")
        str_item_no = dict_row.get("itemNo", "")
        str_batch_no = dict_row.get("batchNo", "")
        n_first_inbound = util_safe_int(dict_row.get("firstInboundTimestamp"))
        f_safety_stock = util_safe_float(dict_safety_stock.get((str_item_no, str_warehouse_no)))
        if not f_safety_stock:
            f_safety_stock = util_safe_float(dict_safety_stock.get((str_item_no, "")))
        return {
            "lotKey": self.__lot_key(str_warehouse_no, str_item_no, str_batch_no),
            "warehouseNo": str_warehouse_no,
            "warehouseName": dict_row.get("warehouseName", ""),
            "itemCategory": util_safe_int(dict_row.get("itemCategory")),
            "itemNo": str_item_no,
            "itemName": dict_row.get("itemName", ""),
            "batchNo": str_batch_no,
            "unit": util_safe_int(dict_row.get("unit")),
            "currentQuantity": util_round_quantity(f_current_quantity),
            "reservedQuantity": util_round_quantity(dict_row.get("reservedQuantity")),
            "qualityHoldQuantity": util_round_quantity(dict_row.get("qualityHoldQuantity")),
            "availableQuantity": util_round_quantity(dict_row.get("availableQuantity")),
            "unitCost": util_round_price(n_inventory_value / f_current_quantity) if f_current_quantity else 0.0,
            "inventoryValue": n_inventory_value,
            "reservedValue": util_round_amount(dict_row.get("reservedValue")),
            "qualityHoldValue": util_round_amount(dict_row.get("qualityHoldValue")),
            "availableValue": util_round_amount(dict_row.get("availableValue")),
            "palletCount": util_round_quantity(f_pallet_count),
            "firstInboundTimestamp": n_first_inbound,
            "daysInStock": int((n_query_timestamp - n_first_inbound) / 86400) if n_first_inbound else 0,
            "validDays": util_safe_int(dict_row.get("validDays")),
            "validDate": util_safe_int(dict_row.get("validDate")),
            "remainingShelfLifeRatio": self.__remaining_shelf_life_ratio(dict_row, n_query_timestamp),
            "safetyStock": util_round_quantity(f_safety_stock),
            "riskTypes": dict_risk.get("riskTypes", []),
            "openTaskCount": len(lst_tasks),
            "refNo": dict_source.get("refNo", ""),
            "refCategory": util_safe_int(dict_source.get("refCategory")),
        }

    def __detail_lot_to_dict(self, dict_lot):
        if not dict_lot:
            return {}
        return {
            "lotKey": dict_lot.get("lotKey", ""),
            "warehouseNo": dict_lot.get("warehouseNo", ""),
            "warehouseName": dict_lot.get("warehouseName", ""),
            "itemCategory": util_safe_int(dict_lot.get("itemCategory")),
            "itemNo": dict_lot.get("itemNo", ""),
            "itemName": dict_lot.get("itemName", ""),
            "batchNo": dict_lot.get("batchNo", ""),
            "unit": util_safe_int(dict_lot.get("unit")),
            "currentQuantity": util_round_quantity(dict_lot.get("currentQuantity")),
            "reservedQuantity": util_round_quantity(dict_lot.get("reservedQuantity")),
            "qualityHoldQuantity": util_round_quantity(dict_lot.get("qualityHoldQuantity")),
            "availableQuantity": util_round_quantity(dict_lot.get("availableQuantity")),
            "unitCost": util_round_price(dict_lot.get("unitCost")),
            "inventoryValue": util_round_amount(dict_lot.get("inventoryValue")),
            "availableValue": util_round_amount(dict_lot.get("availableValue")),
            "palletCount": util_round_quantity(dict_lot.get("palletCount")),
            "validDate": util_safe_int(dict_lot.get("validDate")),
            "riskTypes": dict_lot.get("riskTypes", []),
        }

    def __query_inventory_records(self, obj_session, n_query_timestamp, str_warehouse_no, str_item_no, str_batch_no):
        lst_rows = (
            obj_session.query(CTableInventoryRec)
            .filter(CTableInventoryRec.warehouse_no == str_warehouse_no)
            .filter(CTableInventoryRec.item_no == str_item_no)
            .filter(CTableInventoryRec.batchNumber == str_batch_no)
            .filter(CTableInventoryRec.date <= n_query_timestamp)
            .order_by(CTableInventoryRec.date.asc(), CTableInventoryRec.id.asc())
            .all()
        )
        return [{
            "refCategory": util_safe_int(obj_row.refCategory),
            "refNo": obj_row.ref_no or "",
            "refSubNo": "",
            "date": util_safe_int(obj_row.date),
            "category": util_safe_int(obj_row.category),
            "quantity": util_round_quantity(obj_row.count),
            "amount": util_round_amount(obj_row.amount),
        } for obj_row in lst_rows]

    def __query_reservation_rows(self, obj_session, n_query_timestamp, str_warehouse_no, str_item_no, str_batch_no):
        lst_rows = (
            obj_session.query(CTableWarehouseInventoryReservation)
            .filter(CTableWarehouseInventoryReservation.warehouse_no == str_warehouse_no)
            .filter(CTableWarehouseInventoryReservation.item_no == str_item_no)
            .filter(CTableWarehouseInventoryReservation.batchNumber == str_batch_no)
            .filter(CTableWarehouseInventoryReservation.date <= n_query_timestamp)
            .filter(CTableWarehouseInventoryReservation.status == CWarehouseDashboardService.RESERVATION_STATUS_ACTIVE)
            .filter(
                (CTableWarehouseInventoryReservation.releaseTime == None)
                | (CTableWarehouseInventoryReservation.releaseTime > n_query_timestamp)
            )
            .order_by(CTableWarehouseInventoryReservation.date.asc(), CTableWarehouseInventoryReservation.id.asc())
            .all()
        )
        return [{
            "reservationNo": obj_row.no or "",
            "refCategory": util_safe_int(obj_row.refCategory),
            "refNo": obj_row.ref_no or "",
            "reservedQuantity": util_round_quantity(obj_row.reservedQuantity),
            "reservedValue": util_round_amount(obj_row.reservedValue),
            "releaseTime": util_safe_int(obj_row.releaseTime),
            "status": util_safe_int(obj_row.status),
        } for obj_row in lst_rows]

    def __query_quality_hold_rows(self, obj_session, n_query_timestamp, str_warehouse_no, str_item_no, str_batch_no):
        lst_rows = (
            obj_session.query(CTableWarehouseQualityHold)
            .filter(CTableWarehouseQualityHold.warehouse_no == str_warehouse_no)
            .filter(CTableWarehouseQualityHold.item_no == str_item_no)
            .filter(CTableWarehouseQualityHold.batchNumber == str_batch_no)
            .filter(CTableWarehouseQualityHold.date <= n_query_timestamp)
            .filter(CTableWarehouseQualityHold.status == CWarehouseDashboardService.QUALITY_HOLD_STATUS_ACTIVE)
            .order_by(CTableWarehouseQualityHold.date.asc(), CTableWarehouseQualityHold.id.asc())
            .all()
        )
        return [{
            "holdNo": obj_row.no or "",
            "inspectionNo": obj_row.inspection_no or "",
            "holdQuantity": util_round_quantity(obj_row.holdQuantity),
            "holdValue": util_round_amount(obj_row.holdValue),
            "reason": obj_row.reason or "",
            "status": util_safe_int(obj_row.status),
        } for obj_row in lst_rows]

    def __query_pallet_movement_rows(self, obj_session, n_query_timestamp, str_warehouse_no, str_item_no, str_batch_no):
        lst_rows = (
            obj_session.query(CTableWarehousePalletMovement)
            .filter(CTableWarehousePalletMovement.warehouse_no == str_warehouse_no)
            .filter(CTableWarehousePalletMovement.item_no == str_item_no)
            .filter(CTableWarehousePalletMovement.batchNumber == str_batch_no)
            .filter(CTableWarehousePalletMovement.date <= n_query_timestamp)
            .order_by(CTableWarehousePalletMovement.date.asc(), CTableWarehousePalletMovement.id.asc())
            .all()
        )
        return [{
            "movementNo": obj_row.no or "",
            "date": util_safe_int(obj_row.date),
            "palletGroupNo": obj_row.pallet_group_no or "",
            "palletStatus": util_safe_int(obj_row.palletStatus),
            "palletCount": util_round_quantity(obj_row.palletCount),
            "refCategory": util_safe_int(obj_row.refCategory),
            "refNo": obj_row.ref_no or "",
        } for obj_row in lst_rows]

    def __query_workflow_task_rows(
        self,
        obj_session,
        n_query_timestamp,
        str_timezone,
        str_warehouse_no,
        str_item_no,
        str_batch_no,
    ):
        dict_range = self.__build_range(n_query_timestamp, str_timezone)
        lst_rows = (
            obj_session.query(CTableWorkflowTaskState)
            .filter(CTableWorkflowTaskState.warehouse_no == str_warehouse_no)
            .filter(CTableWorkflowTaskState.item_no == str_item_no)
            .filter(CTableWorkflowTaskState.batchNumber == str_batch_no)
            .filter(CTableWorkflowTaskState.dueTimestamp <= dict_range["endTimestamp"])
            .filter(CTableWorkflowTaskState.taskStatus.in_([
                EWorkflowTaskStatus.PENDING,
                EWorkflowTaskStatus.PARTIAL,
                EWorkflowTaskStatus.BLOCKED,
            ]))
            .order_by(CTableWorkflowTaskState.dueTimestamp.asc(), CTableWorkflowTaskState.id.asc())
            .all()
        )
        return [self.__task_to_dict(obj_row) for obj_row in lst_rows]

    def __is_lot_matched(self, dict_lot, str_risk_type, str_availability, str_keyword):
        if str_risk_type and str_risk_type not in dict_lot.get("riskTypes", []):
            return False
        if str_availability and not self.__is_availability_matched(dict_lot, str_availability):
            return False
        if str_keyword and not self.__is_keyword_matched(dict_lot, str_keyword):
            return False
        return True

    def __is_availability_matched(self, dict_lot, str_availability):
        str_value = (str_availability or "").lower()
        if str_value == "available":
            return util_safe_float(dict_lot.get("availableQuantity")) > 0
        if str_value == "reserved":
            return util_safe_float(dict_lot.get("reservedQuantity")) > 0
        if str_value == "quality_hold":
            return util_safe_float(dict_lot.get("qualityHoldQuantity")) > 0
        if str_value == "blocked":
            return util_safe_int(dict_lot.get("openTaskCount")) > 0
        return True

    def __is_keyword_matched(self, dict_lot, str_keyword):
        str_keyword = (str_keyword or "").lower()
        lst_values = [
            dict_lot.get("itemNo", ""),
            dict_lot.get("itemName", ""),
            dict_lot.get("batchNo", ""),
            dict_lot.get("refNo", ""),
            dict_lot.get("warehouseName", ""),
        ]
        return any(str_keyword in (str_value or "").lower() for str_value in lst_values)

    def __sort_lots(self, lst_results, str_sort, str_order):
        str_sort = self.__sort_field(str_sort)
        if not str_sort:
            return lst_results
        b_reverse = (str_order or "desc").lower() != "asc"
        return sorted(lst_results, key=lambda dict_row: util_safe_float(dict_row.get(str_sort)), reverse=b_reverse)

    def __sort_field(self, str_sort):
        return str_sort if str_sort in ["inventoryValue", "availableQuantity", "validDate", "daysInStock"] else ""

    def __new_summary_accumulator(self):
        return {
            "lotCount": 0,
            "itemNos": set(),
            "totalQuantity": 0.0,
            "totalInventoryValue": 0.0,
            "totalAvailableQuantity": 0.0,
            "totalAvailableValue": 0.0,
            "riskLotCount": 0,
            "pendingTaskCount": 0,
        }

    def __accumulate_summary(self, dict_summary, dict_lot):
        dict_summary["lotCount"] += 1
        if dict_lot.get("itemNo"):
            dict_summary["itemNos"].add(dict_lot.get("itemNo"))
        dict_summary["totalQuantity"] += util_safe_float(dict_lot.get("currentQuantity"))
        dict_summary["totalInventoryValue"] += util_safe_float(dict_lot.get("inventoryValue"))
        dict_summary["totalAvailableQuantity"] += util_safe_float(dict_lot.get("availableQuantity"))
        dict_summary["totalAvailableValue"] += util_safe_float(dict_lot.get("availableValue"))
        if dict_lot.get("riskTypes"):
            dict_summary["riskLotCount"] += 1
        dict_summary["pendingTaskCount"] += util_safe_int(dict_lot.get("openTaskCount"))

    def __finalize_summary(self, dict_summary):
        return {
            "lotCount": util_safe_int(dict_summary.get("lotCount")),
            "itemCount": len(dict_summary.get("itemNos", set())),
            "totalQuantity": util_round_quantity(dict_summary.get("totalQuantity")),
            "totalInventoryValue": util_round_amount(dict_summary.get("totalInventoryValue")),
            "totalAvailableQuantity": util_round_quantity(dict_summary.get("totalAvailableQuantity")),
            "totalAvailableValue": util_round_amount(dict_summary.get("totalAvailableValue")),
            "riskLotCount": util_safe_int(dict_summary.get("riskLotCount")),
            "pendingTaskCount": util_safe_int(dict_summary.get("pendingTaskCount")),
        }

    def __task_to_dict(self, obj_row):
        return {
            "taskId": obj_row.taskId or "",
            "taskType": util_safe_int(obj_row.taskType),
            "taskStatus": util_safe_int(obj_row.taskStatus),
            "ownerDepartment": util_safe_int(obj_row.ownerDepartment),
            "expectedQuantity": util_round_quantity(obj_row.expectedQuantity),
            "processedQuantity": util_round_quantity(obj_row.processedQuantity),
            "remainingQuantity": util_round_quantity(max(
                util_safe_float(obj_row.expectedQuantity) - util_safe_float(obj_row.processedQuantity),
                0.0,
            )),
            "dueTimestamp": util_safe_int(obj_row.dueTimestamp),
            "blockReason": obj_row.blockReason or "",
        }

    def __remaining_shelf_life_ratio(self, dict_row, n_query_timestamp):
        n_valid_days = util_safe_int(dict_row.get("validDays"))
        n_valid_date = util_safe_int(dict_row.get("validDate"))
        if not n_valid_days or not n_valid_date:
            return 0.0
        return round(max(n_valid_date - n_query_timestamp, 0) / float(n_valid_days * 86400), 4)

    def __build_range(self, n_timestamp, str_timezone):
        try:
            obj_tz = ZoneInfo(str_timezone or "UTC")
        except Exception:
            obj_tz = timezone.utc
        obj_local = datetime.fromtimestamp(n_timestamp, timezone.utc).astimezone(obj_tz)
        obj_start_local = obj_local.replace(hour=0, minute=0, second=0, microsecond=0)
        n_start = int(obj_start_local.astimezone(timezone.utc).timestamp())
        return {
            "date": obj_local.strftime("%Y-%m-%d"),
            "startTimestamp": n_start,
            "endTimestamp": n_start + 86399,
        }

    def __lot_key(self, str_warehouse_no, str_item_no, str_batch_no):
        return "%s|%s|%s" % (str_warehouse_no or "", str_item_no or "", str_batch_no or "")


class CWarehouseTaskWorkbenchService(object):
    TARGET_TASK_TYPES = [
        EWorkflowTaskType.GOODS_RECEIPT,
        EWorkflowTaskType.INBOUND,
        EWorkflowTaskType.OUTBOUND,
        EWorkflowTaskType.TRANSFER,
        EWorkflowTaskType.QUALITY,
        EWorkflowTaskType.SHIPMENT,
    ]
    OPEN_STATUSES = [
        EWorkflowTaskStatus.PENDING,
        EWorkflowTaskStatus.PARTIAL,
        EWorkflowTaskStatus.BLOCKED,
    ]
    RISK_OVERDUE = "OVERDUE"
    RISK_BLOCKED = "BLOCKED"
    RISK_INVENTORY_SHORTAGE = "INVENTORY_SHORTAGE"
    RISK_QUALITY_HOLD = "QUALITY_HOLD"
    RISK_BATCH_NOT_ASSIGNED = "BATCH_NOT_ASSIGNED"

    def get_task_workbench(
        self,
        n_date=0,
        str_timezone="",
        str_date_range="today",
        str_warehouse_no="",
        n_task_type=0,
        str_status="",
        n_owner_department=0,
        b_risk_only=False,
        str_keyword="",
        str_sort="",
        str_order="",
        n_start=0,
        n_count=50,
        obj_session=None,
    ):
        if obj_session:
            return self.__get_task_workbench_with_session(
                obj_session,
                n_date,
                str_timezone,
                str_date_range,
                str_warehouse_no,
                n_task_type,
                str_status,
                n_owner_department,
                b_risk_only,
                str_keyword,
                str_sort,
                str_order,
                n_start,
                n_count,
            )

        with CDBMgr() as obj_dbmgr:
            return self.__get_task_workbench_with_session(
                obj_dbmgr.get_session(),
                n_date,
                str_timezone,
                str_date_range,
                str_warehouse_no,
                n_task_type,
                str_status,
                n_owner_department,
                b_risk_only,
                str_keyword,
                str_sort,
                str_order,
                n_start,
                n_count,
            )

    def get_task_detail(
        self,
        n_date=0,
        str_timezone="",
        str_task_id="",
        obj_session=None,
    ):
        if obj_session:
            return self.__get_task_detail_with_session(
                obj_session,
                n_date,
                str_timezone,
                str_task_id,
            )

        with CDBMgr() as obj_dbmgr:
            return self.__get_task_detail_with_session(
                obj_dbmgr.get_session(),
                n_date,
                str_timezone,
                str_task_id,
            )

    def __get_task_workbench_with_session(
        self,
        obj_session,
        n_date,
        str_timezone,
        str_date_range,
        str_warehouse_no,
        n_task_type,
        str_status,
        n_owner_department,
        b_risk_only,
        str_keyword,
        str_sort,
        str_order,
        n_start,
        n_count,
    ):
        n_query_timestamp = n_date if n_date else int(time.time())
        dict_range = self.__build_range(n_query_timestamp, str_timezone, str_date_range)
        lst_rows = self.__query_task_rows(
            obj_session,
            dict_range,
            str_warehouse_no,
            n_task_type,
            str_status,
            n_owner_department,
            str_keyword,
        )
        dict_context = self.__build_inventory_context(
            obj_session,
            n_query_timestamp,
            str_timezone,
            str_warehouse_no,
            "",
            "",
        )
        dict_warehouse_names = self.__query_warehouse_names(
            obj_session,
            [obj_row.warehouse_no for obj_row in lst_rows],
        )
        lst_results = [
            self.__task_to_workbench_dict(
                obj_row,
                dict_context,
                dict_warehouse_names,
                n_query_timestamp,
            )
            for obj_row in lst_rows
        ]
        if b_risk_only:
            lst_results = [dict_row for dict_row in lst_results if dict_row.get("riskTypes")]

        lst_results = self.__sort_tasks(lst_results, str_sort, str_order)
        n_total = len(lst_results)
        n_start = max(util_safe_int(n_start), 0)
        n_count = util_safe_int(n_count) if n_count else 50
        if n_count <= 0:
            n_count = 50
        lst_page = lst_results[n_start:n_start + n_count]
        return {
            "serverTimestamp": n_query_timestamp,
            "timezone": str_timezone or "UTC",
            "range": {
                "mode": dict_range.get("mode", "today"),
                "startTimestamp": util_safe_int(dict_range.get("startTimestamp")),
                "endTimestamp": util_safe_int(dict_range.get("endTimestamp")),
            },
            "summary": self.__build_summary(lst_results),
            "lanes": self.__build_lanes(lst_results),
            "total": n_total,
            "count": len(lst_page),
            "start": n_start,
            "results": lst_page,
        }

    def __get_task_detail_with_session(
        self,
        obj_session,
        n_date,
        str_timezone,
        str_task_id,
    ):
        n_query_timestamp = n_date if n_date else int(time.time())
        obj_task = (
            obj_session.query(CTableWorkflowTaskState)
            .filter(CTableWorkflowTaskState.taskId == str_task_id)
            .first()
        )
        if not obj_task:
            return {
                "task": {},
                "quantity": {},
                "relatedLots": [],
                "sourceRefs": [],
                "timeline": [],
            }

        dict_context = self.__build_inventory_context(
            obj_session,
            n_query_timestamp,
            str_timezone,
            obj_task.warehouse_no or "",
            obj_task.item_no or "",
            obj_task.batchNumber or "",
        )
        dict_warehouse_names = self.__query_warehouse_names(
            obj_session,
            [obj_task.warehouse_no],
        )
        dict_task = self.__task_to_workbench_dict(
            obj_task,
            dict_context,
            dict_warehouse_names,
            n_query_timestamp,
        )
        return {
            "task": self.__detail_task_to_dict(dict_task),
            "quantity": self.__quantity_to_dict(dict_task),
            "relatedLots": self.__build_related_lots(
                obj_task,
                dict_context,
                n_query_timestamp,
            ),
            "sourceRefs": self.__build_source_refs(obj_task),
            "timeline": self.__query_timeline(obj_session, obj_task.taskId or ""),
        }

    def __query_task_rows(
        self,
        obj_session,
        dict_range,
        str_warehouse_no,
        n_task_type,
        str_status,
        n_owner_department,
        str_keyword,
    ):
        lst_filters = []
        if n_task_type:
            lst_filters.append(CTableWorkflowTaskState.taskType == n_task_type)
        else:
            lst_filters.append(CTableWorkflowTaskState.taskType.in_(self.TARGET_TASK_TYPES))

        lst_statuses = self.__task_status_values(str_status)
        if lst_statuses:
            lst_filters.append(CTableWorkflowTaskState.taskStatus.in_(lst_statuses))
        else:
            lst_filters.append(CTableWorkflowTaskState.taskStatus.in_(self.OPEN_STATUSES))

        if str_warehouse_no:
            lst_filters.append(CTableWorkflowTaskState.warehouse_no == str_warehouse_no)
        if n_owner_department:
            lst_filters.append(CTableWorkflowTaskState.ownerDepartment == n_owner_department)

        if dict_range.get("applyRange"):
            n_start = util_safe_int(dict_range.get("startTimestamp"))
            n_end = util_safe_int(dict_range.get("endTimestamp"))
            if n_start:
                lst_filters.append(CTableWorkflowTaskState.dueTimestamp >= n_start)
            if n_end:
                lst_filters.append(CTableWorkflowTaskState.dueTimestamp <= n_end)
        if str_keyword:
            str_like = "%%%s%%" % str_keyword
            lst_filters.append(or_(
                CTableWorkflowTaskState.taskId.like(str_like),
                CTableWorkflowTaskState.ref_no.like(str_like),
                CTableWorkflowTaskState.ref_sub_no.like(str_like),
                CTableWorkflowTaskState.item_no.like(str_like),
                CTableWorkflowTaskState.item_name.like(str_like),
                CTableWorkflowTaskState.batchNumber.like(str_like),
            ))

        return (
            obj_session.query(CTableWorkflowTaskState)
            .filter(*lst_filters)
            .order_by(
                CTableWorkflowTaskState.dueTimestamp.asc(),
                CTableWorkflowTaskState.taskType.asc(),
                CTableWorkflowTaskState.id.asc(),
            )
            .all()
        )

    def __build_inventory_context(
        self,
        obj_session,
        n_query_timestamp,
        str_timezone,
        str_warehouse_no,
        str_item_no,
        str_batch_no,
    ):
        obj_builder = CWarehouseInventoryContextBuilder()
        dict_context = obj_builder.build(
            obj_session=obj_session,
            n_query_timestamp=n_query_timestamp,
            str_timezone=str_timezone,
            str_warehouse_no=str_warehouse_no,
            n_item_category=0,
            str_item_no=str_item_no,
            str_batch_no=str_batch_no,
        )
        dict_by_key = {}
        dict_by_item_warehouse = defaultdict(lambda: {
            "availableQuantity": 0.0,
            "reservedQuantity": 0.0,
            "qualityHoldQuantity": 0.0,
            "inventoryValue": 0.0,
        })
        for dict_row in dict_context.get("inventoryRows", []):
            str_key = obj_builder.stock_key(
                dict_row.get("itemNo"),
                dict_row.get("batchNo"),
                dict_row.get("warehouseNo"),
            )
            dict_by_key[str_key] = dict_row
            if util_safe_float(dict_row.get("currentQuantity")) <= 0:
                continue
            str_item_warehouse_key = self.__item_warehouse_key(
                dict_row.get("itemNo"),
                dict_row.get("warehouseNo"),
            )
            dict_by_item_warehouse[str_item_warehouse_key]["availableQuantity"] += util_safe_float(dict_row.get("availableQuantity"))
            dict_by_item_warehouse[str_item_warehouse_key]["reservedQuantity"] += util_safe_float(dict_row.get("reservedQuantity"))
            dict_by_item_warehouse[str_item_warehouse_key]["qualityHoldQuantity"] += util_safe_float(dict_row.get("qualityHoldQuantity"))
            dict_by_item_warehouse[str_item_warehouse_key]["inventoryValue"] += util_safe_float(dict_row.get("inventoryValue"))
        dict_context["inventoryByKey"] = dict_by_key
        dict_context["inventoryByItemWarehouse"] = dict_by_item_warehouse
        return dict_context

    def __task_to_workbench_dict(
        self,
        obj_row,
        dict_context,
        dict_warehouse_names,
        n_query_timestamp,
    ):
        dict_inventory = self.__inventory_for_task(obj_row, dict_context)
        f_expected = util_safe_float(obj_row.expectedQuantity)
        f_processed = util_safe_float(obj_row.processedQuantity)
        f_remaining = max(f_expected - f_processed, 0.0)
        f_available = util_safe_float(dict_inventory.get("availableQuantity"))
        f_quality_hold = util_safe_float(dict_inventory.get("qualityHoldQuantity"))
        lst_risk_types = self.__risk_types(obj_row, f_remaining, f_available, f_quality_hold, n_query_timestamp)
        return {
            "taskId": obj_row.taskId or "",
            "taskType": util_safe_int(obj_row.taskType),
            "taskStatus": util_safe_int(obj_row.taskStatus),
            "refCategory": util_safe_int(obj_row.refCategory),
            "refNo": obj_row.ref_no or "",
            "refSubNo": obj_row.ref_sub_no or "",
            "itemCategory": util_safe_int(obj_row.itemCategory),
            "itemNo": obj_row.item_no or "",
            "itemName": obj_row.item_name or "",
            "batchNo": obj_row.batchNumber or "",
            "unit": util_safe_int(obj_row.unit or dict_inventory.get("unit")),
            "expectedQuantity": util_round_quantity(f_expected),
            "processedQuantity": util_round_quantity(f_processed),
            "remainingQuantity": util_round_quantity(f_remaining),
            "warehouseNo": obj_row.warehouse_no or "",
            "warehouseName": dict_warehouse_names.get(obj_row.warehouse_no, "") or dict_inventory.get("warehouseName", ""),
            "dueTimestamp": util_safe_int(obj_row.dueTimestamp),
            "ownerDepartment": util_safe_int(obj_row.ownerDepartment),
            "riskLevel": self.__risk_level(lst_risk_types),
            "riskTypes": lst_risk_types,
            "blockReasonCode": obj_row.blockReasonCode or "",
            "blockReason": obj_row.blockReason or "",
            "availableQuantity": util_round_quantity(f_available),
            "reservedQuantity": util_round_quantity(dict_inventory.get("reservedQuantity")),
            "qualityHoldQuantity": util_round_quantity(f_quality_hold),
            "inventoryValue": util_round_amount(dict_inventory.get("inventoryValue")),
            "nextActionCode": self.__next_action_code(obj_row),
            "laneCode": self.__lane_code(obj_row),
        }

    def __inventory_for_task(self, obj_row, dict_context):
        obj_builder = CWarehouseInventoryContextBuilder()
        str_item_no = obj_row.item_no or ""
        str_batch_no = obj_row.batchNumber or ""
        str_warehouse_no = obj_row.warehouse_no or ""
        if str_batch_no:
            str_key = obj_builder.stock_key(str_item_no, str_batch_no, str_warehouse_no)
            return dict_context.get("inventoryByKey", {}).get(str_key, {})
        return dict_context.get("inventoryByItemWarehouse", {}).get(
            self.__item_warehouse_key(str_item_no, str_warehouse_no),
            {},
        )

    def __risk_types(self, obj_row, f_remaining, f_available, f_quality_hold, n_query_timestamp):
        lst_risks = []
        n_task_status = util_safe_int(obj_row.taskStatus)
        n_task_type = util_safe_int(obj_row.taskType)
        b_open = n_task_status not in [EWorkflowTaskStatus.DONE, EWorkflowTaskStatus.CANCELLED]
        if b_open and util_safe_int(obj_row.dueTimestamp) and util_safe_int(obj_row.dueTimestamp) < n_query_timestamp:
            lst_risks.append(self.RISK_OVERDUE)
        if n_task_status == EWorkflowTaskStatus.BLOCKED:
            lst_risks.append(self.RISK_BLOCKED)
        if n_task_type in [EWorkflowTaskType.OUTBOUND, EWorkflowTaskType.TRANSFER, EWorkflowTaskType.SHIPMENT]:
            if f_remaining > f_available:
                lst_risks.append(self.RISK_INVENTORY_SHORTAGE)
            if f_quality_hold > 0:
                lst_risks.append(self.RISK_QUALITY_HOLD)
            if not (obj_row.batchNumber or ""):
                lst_risks.append(self.RISK_BATCH_NOT_ASSIGNED)
        return lst_risks

    def __risk_level(self, lst_risk_types):
        if self.RISK_BLOCKED in lst_risk_types or self.RISK_OVERDUE in lst_risk_types:
            return EWarehouseRiskLevel.DANGER
        if lst_risk_types:
            return EWarehouseRiskLevel.WARNING
        return EWarehouseRiskLevel.NORMAL

    def __lane_code(self, obj_row):
        if util_safe_int(obj_row.taskStatus) == EWorkflowTaskStatus.BLOCKED:
            return "blocked"
        n_task_type = util_safe_int(obj_row.taskType)
        if n_task_type in [EWorkflowTaskType.GOODS_RECEIPT, EWorkflowTaskType.INBOUND]:
            return "inbound"
        if n_task_type in [EWorkflowTaskType.OUTBOUND, EWorkflowTaskType.TRANSFER]:
            return "outbound"
        if n_task_type == EWorkflowTaskType.QUALITY:
            return "quality"
        if n_task_type == EWorkflowTaskType.SHIPMENT:
            return "shipment"
        return "other"

    def __next_action_code(self, obj_row):
        if util_safe_int(obj_row.taskStatus) == EWorkflowTaskStatus.BLOCKED:
            return "warehouse.task.resolveBlocker"
        dict_actions = {
            EWorkflowTaskType.GOODS_RECEIPT: "warehouse.task.confirmReceipt",
            EWorkflowTaskType.INBOUND: "warehouse.task.arrangeInbound",
            EWorkflowTaskType.OUTBOUND: "warehouse.task.prepareOutbound",
            EWorkflowTaskType.TRANSFER: "warehouse.task.arrangeTransfer",
            EWorkflowTaskType.QUALITY: "warehouse.task.waitQualityDecision",
            EWorkflowTaskType.SHIPMENT: "warehouse.task.prepareShipment",
        }
        return dict_actions.get(util_safe_int(obj_row.taskType), "")

    def __build_summary(self, lst_results):
        return {
            "openTaskCount": len(lst_results),
            "overdueTaskCount": len([dict_row for dict_row in lst_results if self.RISK_OVERDUE in dict_row.get("riskTypes", [])]),
            "blockedTaskCount": len([dict_row for dict_row in lst_results if util_safe_int(dict_row.get("taskStatus")) == EWorkflowTaskStatus.BLOCKED]),
            "inboundTaskCount": len([dict_row for dict_row in lst_results if util_safe_int(dict_row.get("taskType")) in [EWorkflowTaskType.GOODS_RECEIPT, EWorkflowTaskType.INBOUND]]),
            "outboundTaskCount": len([dict_row for dict_row in lst_results if util_safe_int(dict_row.get("taskType")) in [EWorkflowTaskType.OUTBOUND, EWorkflowTaskType.TRANSFER]]),
            "qualityTaskCount": len([dict_row for dict_row in lst_results if util_safe_int(dict_row.get("taskType")) == EWorkflowTaskType.QUALITY]),
            "shipmentTaskCount": len([dict_row for dict_row in lst_results if util_safe_int(dict_row.get("taskType")) == EWorkflowTaskType.SHIPMENT]),
            "inventoryShortageTaskCount": len([dict_row for dict_row in lst_results if self.RISK_INVENTORY_SHORTAGE in dict_row.get("riskTypes", [])]),
        }

    def __build_lanes(self, lst_results):
        dict_lanes = {
            "inbound": {"laneCode": "inbound", "taskCount": 0, "riskCount": 0},
            "outbound": {"laneCode": "outbound", "taskCount": 0, "riskCount": 0},
            "quality": {"laneCode": "quality", "taskCount": 0, "riskCount": 0},
            "shipment": {"laneCode": "shipment", "taskCount": 0, "riskCount": 0},
            "blocked": {"laneCode": "blocked", "taskCount": 0, "riskCount": 0},
        }
        for dict_row in lst_results:
            str_lane = dict_row.get("laneCode", "other")
            if str_lane not in dict_lanes:
                continue
            dict_lanes[str_lane]["taskCount"] += 1
            if dict_row.get("riskTypes"):
                dict_lanes[str_lane]["riskCount"] += 1
        return [dict_lanes[str_key] for str_key in ["inbound", "outbound", "quality", "shipment", "blocked"]]

    def __sort_tasks(self, lst_results, str_sort, str_order):
        str_field = self.__sort_field(str_sort)
        if not str_field:
            return lst_results
        b_reverse = (str_order or "asc").lower() == "desc"
        return sorted(lst_results, key=lambda dict_row: util_safe_float(dict_row.get(str_field)), reverse=b_reverse)

    def __sort_field(self, str_sort):
        dict_fields = {
            "dueTimestamp": "dueTimestamp",
            "taskType": "taskType",
            "remainingQuantity": "remainingQuantity",
            "riskLevel": "riskLevel",
        }
        return dict_fields.get(str_sort or "", "")

    def __detail_task_to_dict(self, dict_task):
        return {
            "taskId": dict_task.get("taskId", ""),
            "taskType": util_safe_int(dict_task.get("taskType")),
            "taskStatus": util_safe_int(dict_task.get("taskStatus")),
            "refCategory": util_safe_int(dict_task.get("refCategory")),
            "refNo": dict_task.get("refNo", ""),
            "refSubNo": dict_task.get("refSubNo", ""),
            "ownerDepartment": util_safe_int(dict_task.get("ownerDepartment")),
            "warehouseNo": dict_task.get("warehouseNo", ""),
            "warehouseName": dict_task.get("warehouseName", ""),
            "dueTimestamp": util_safe_int(dict_task.get("dueTimestamp")),
            "blockReasonCode": dict_task.get("blockReasonCode", ""),
            "blockReason": dict_task.get("blockReason", ""),
            "riskLevel": util_safe_int(dict_task.get("riskLevel")),
            "riskTypes": dict_task.get("riskTypes", []),
            "nextActionCode": dict_task.get("nextActionCode", ""),
        }

    def __quantity_to_dict(self, dict_task):
        return {
            "itemCategory": util_safe_int(dict_task.get("itemCategory")),
            "itemNo": dict_task.get("itemNo", ""),
            "itemName": dict_task.get("itemName", ""),
            "batchNo": dict_task.get("batchNo", ""),
            "unit": util_safe_int(dict_task.get("unit")),
            "expectedQuantity": util_round_quantity(dict_task.get("expectedQuantity")),
            "processedQuantity": util_round_quantity(dict_task.get("processedQuantity")),
            "remainingQuantity": util_round_quantity(dict_task.get("remainingQuantity")),
            "availableQuantity": util_round_quantity(dict_task.get("availableQuantity")),
            "reservedQuantity": util_round_quantity(dict_task.get("reservedQuantity")),
            "qualityHoldQuantity": util_round_quantity(dict_task.get("qualityHoldQuantity")),
        }

    def __build_related_lots(self, obj_task, dict_context, n_query_timestamp):
        obj_builder = CWarehouseInventoryContextBuilder()
        lst_lots = []
        for dict_row in dict_context.get("inventoryRows", []):
            if util_safe_float(dict_row.get("currentQuantity")) <= 0:
                continue
            str_key = obj_builder.stock_key(
                dict_row.get("itemNo"),
                dict_row.get("batchNo"),
                dict_row.get("warehouseNo"),
            )
            dict_risk = dict_context.get("risks", {}).get(str_key, {"riskTypes": []})
            lst_lots.append({
                "lotKey": "%s|%s|%s" % (
                    dict_row.get("warehouseNo", ""),
                    dict_row.get("itemNo", ""),
                    dict_row.get("batchNo", ""),
                ),
                "warehouseNo": dict_row.get("warehouseNo", ""),
                "itemNo": dict_row.get("itemNo", ""),
                "itemName": dict_row.get("itemName", ""),
                "batchNo": dict_row.get("batchNo", ""),
                "currentQuantity": util_round_quantity(dict_row.get("currentQuantity")),
                "availableQuantity": util_round_quantity(dict_row.get("availableQuantity")),
                "qualityHoldQuantity": util_round_quantity(dict_row.get("qualityHoldQuantity")),
                "validDate": util_safe_int(dict_row.get("validDate")),
                "riskTypes": dict_risk.get("riskTypes", []),
            })
        return sorted(
            lst_lots,
            key=lambda dict_row: (
                0 if dict_row.get("riskTypes") else 1,
                util_safe_int(dict_row.get("validDate")) or 9999999999,
                -util_safe_float(dict_row.get("availableQuantity")),
            ),
        )

    def __build_source_refs(self, obj_task):
        if not (obj_task.refCategory or obj_task.ref_no or obj_task.ref_sub_no):
            return []
        return [{
            "refCategory": util_safe_int(obj_task.refCategory),
            "refNo": obj_task.ref_no or "",
            "refSubNo": obj_task.ref_sub_no or "",
            "descriptionCode": self.__source_description_code(obj_task),
        }]

    def __query_timeline(self, obj_session, str_task_id):
        lst_rows = (
            obj_session.query(CTableWorkflowTaskEvent)
            .filter(CTableWorkflowTaskEvent.taskId == str_task_id)
            .order_by(CTableWorkflowTaskEvent.eventTimestamp.asc(), CTableWorkflowTaskEvent.id.asc())
            .all()
        )
        return [{
            "eventCode": obj_row.eventCode or "",
            "eventTimestamp": util_safe_int(obj_row.eventTimestamp),
            "department": util_safe_int(obj_row.toDepartment or obj_row.fromDepartment),
            "status": util_safe_int(obj_row.toStatus or obj_row.fromStatus),
            "comment": obj_row.comment or "",
        } for obj_row in lst_rows]

    def __source_description_code(self, obj_task):
        n_task_type = util_safe_int(obj_task.taskType)
        if n_task_type in [EWorkflowTaskType.GOODS_RECEIPT, EWorkflowTaskType.INBOUND]:
            return "warehouse.source.goodsReceipt"
        if n_task_type in [EWorkflowTaskType.OUTBOUND, EWorkflowTaskType.TRANSFER]:
            return "warehouse.source.inventory"
        if n_task_type == EWorkflowTaskType.PRODUCTION:
            return "warehouse.source.workOrder"
        if n_task_type == EWorkflowTaskType.QUALITY:
            return "warehouse.source.quality"
        if n_task_type == EWorkflowTaskType.SHIPMENT:
            return "warehouse.source.shipment"
        return ""

    def __query_warehouse_names(self, obj_session, lst_warehouse_nos):
        lst_values = [str_no for str_no in set(lst_warehouse_nos) if str_no]
        if not lst_values:
            return {}
        lst_rows = (
            obj_session.query(CTableShipWarehouseAlias.no, CTableShipWarehouseAlias.name)
            .filter(CTableShipWarehouseAlias.no.in_(lst_values))
            .all()
        )
        return {obj_row.no: obj_row.name or "" for obj_row in lst_rows}

    def __build_range(self, n_timestamp, str_timezone, str_date_range):
        try:
            obj_tz = ZoneInfo(str_timezone or "UTC")
        except Exception:
            obj_tz = timezone.utc
        obj_local = datetime.fromtimestamp(n_timestamp, timezone.utc).astimezone(obj_tz)
        obj_start_local = obj_local.replace(hour=0, minute=0, second=0, microsecond=0)
        n_start = int(obj_start_local.astimezone(timezone.utc).timestamp())
        str_mode = str_date_range or "today"
        if str_mode == "next_7_days":
            return {
                "mode": str_mode,
                "startTimestamp": n_start,
                "endTimestamp": n_start + 7 * 86400 - 1,
                "applyRange": True,
            }
        if str_mode == "overdue":
            return {
                "mode": str_mode,
                "startTimestamp": 0,
                "endTimestamp": n_start - 1,
                "applyRange": True,
            }
        if str_mode == "all_open":
            return {
                "mode": str_mode,
                "startTimestamp": 0,
                "endTimestamp": 0,
                "applyRange": False,
            }
        return {
            "mode": "today",
            "startTimestamp": n_start,
            "endTimestamp": n_start + 86399,
            "applyRange": True,
        }

    def __task_status_values(self, str_status):
        if not str_status:
            return []
        dict_status = {
            "pending": EWorkflowTaskStatus.PENDING,
            "partial": EWorkflowTaskStatus.PARTIAL,
            "done": EWorkflowTaskStatus.DONE,
            "blocked": EWorkflowTaskStatus.BLOCKED,
            "cancelled": EWorkflowTaskStatus.CANCELLED,
        }
        if str(str_status).lower() in dict_status:
            return [dict_status.get(str(str_status).lower())]
        n_status = util_safe_int(str_status)
        return [n_status] if n_status else []

    def __item_warehouse_key(self, str_item_no, str_warehouse_no):
        return "%s|%s" % (str_item_no or "", str_warehouse_no or "")


class CWarehouseTaskService(object):
    def get_tasks(
        self,
        n_date=0,
        str_timezone="",
        n_task_type=0,
        str_warehouse_no="",
        str_status="",
        n_start=0,
        n_count=50,
        obj_session=None,
    ):
        if obj_session:
            return self.__get_tasks_with_session(
                obj_session,
                n_date,
                str_timezone,
                n_task_type,
                str_warehouse_no,
                str_status,
                n_start,
                n_count,
            )

        with CDBMgr() as obj_dbmgr:
            return self.__get_tasks_with_session(
                obj_dbmgr.get_session(),
                n_date,
                str_timezone,
                n_task_type,
                str_warehouse_no,
                str_status,
                n_start,
                n_count,
            )

    def __get_tasks_with_session(
        self,
        obj_session,
        n_date,
        str_timezone,
        n_task_type,
        str_warehouse_no,
        str_status,
        n_start,
        n_count,
    ):
        lst_filters = []
        n_status = self.__task_status_value(str_status)
        if n_status:
            lst_filters.append(CTableWorkflowTaskState.taskStatus == n_status)
        else:
            lst_filters.append(CTableWorkflowTaskState.taskStatus.in_([
                EWorkflowTaskStatus.PENDING,
                EWorkflowTaskStatus.PARTIAL,
                EWorkflowTaskStatus.BLOCKED,
            ]))
        if n_task_type:
            lst_filters.append(CTableWorkflowTaskState.taskType == n_task_type)
        if str_warehouse_no:
            lst_filters.append(CTableWorkflowTaskState.warehouse_no == str_warehouse_no)
        if n_date:
            dict_range = self.__build_range(n_date, str_timezone)
            lst_filters.append(CTableWorkflowTaskState.dueTimestamp <= dict_range["endTimestamp"])

        lst_rows = (
            obj_session.query(CTableWorkflowTaskState)
            .filter(*lst_filters)
            .order_by(CTableWorkflowTaskState.dueTimestamp.asc())
            .all()
        )
        n_start = max(util_safe_int(n_start), 0)
        n_count = util_safe_int(n_count) if n_count else 50
        if n_count <= 0:
            n_count = 50
        lst_page = lst_rows[n_start:n_start + n_count]
        dict_warehouse_names = self.__query_warehouse_names(
            obj_session,
            [obj_row.warehouse_no for obj_row in lst_page],
        )
        return {
            "serverTimestamp": n_date if n_date else int(time.time()),
            "timezone": str_timezone or "UTC",
            "total": len(lst_rows),
            "count": len(lst_page),
            "start": n_start,
            "results": [self.__task_to_dict(obj_row, dict_warehouse_names) for obj_row in lst_page],
        }

    def __build_range(self, n_timestamp, str_timezone):
        try:
            obj_tz = ZoneInfo(str_timezone or "UTC")
        except Exception:
            obj_tz = timezone.utc
        obj_local = datetime.fromtimestamp(n_timestamp, timezone.utc).astimezone(obj_tz)
        obj_start_local = obj_local.replace(hour=0, minute=0, second=0, microsecond=0)
        n_start = int(obj_start_local.astimezone(timezone.utc).timestamp())
        return {
            "date": obj_local.strftime("%Y-%m-%d"),
            "startTimestamp": n_start,
            "endTimestamp": n_start + 86399,
        }

    def __query_warehouse_names(self, obj_session, lst_warehouse_nos):
        lst_values = [str_no for str_no in set(lst_warehouse_nos) if str_no]
        if not lst_values:
            return {}
        lst_rows = (
            obj_session.query(CTableShipWarehouseAlias.no, CTableShipWarehouseAlias.name)
            .filter(CTableShipWarehouseAlias.no.in_(lst_values))
            .all()
        )
        return {obj_row.no: obj_row.name or "" for obj_row in lst_rows}

    def __task_to_dict(self, obj_row, dict_warehouse_names=None):
        dict_warehouse_names = dict_warehouse_names or {}
        return {
            "taskId": obj_row.taskId or "",
            "taskType": util_safe_int(obj_row.taskType),
            "refCategory": util_safe_int(obj_row.refCategory),
            "sourceNo": obj_row.ref_no or "",
            "sourceSubNo": obj_row.ref_sub_no or "",
            "itemNo": obj_row.item_no or "",
            "itemName": obj_row.item_name or "",
            "itemCategory": util_safe_int(obj_row.itemCategory),
            "batchNo": obj_row.batchNumber or "",
            "expectedQuantity": util_round_quantity(obj_row.expectedQuantity),
            "processedQuantity": util_round_quantity(obj_row.processedQuantity),
            "remainingQuantity": util_round_quantity(max(
                util_safe_float(obj_row.expectedQuantity) - util_safe_float(obj_row.processedQuantity),
                0.0,
            )),
            "unit": util_safe_int(obj_row.unit),
            "palletCount": util_round_quantity(obj_row.palletCount),
            "warehouseNo": obj_row.warehouse_no or "",
            "warehouseName": dict_warehouse_names.get(obj_row.warehouse_no, ""),
            "dueTimestamp": util_safe_int(obj_row.dueTimestamp),
            "taskStatus": util_safe_int(obj_row.taskStatus),
            "ownerDepartment": util_safe_int(obj_row.ownerDepartment),
            "blockReason": obj_row.blockReason or "",
        }

    def __task_status_value(self, str_status):
        if not str_status:
            return 0
        dict_status = {
            "pending": EWorkflowTaskStatus.PENDING,
            "partial": EWorkflowTaskStatus.PARTIAL,
            "done": EWorkflowTaskStatus.DONE,
            "blocked": EWorkflowTaskStatus.BLOCKED,
            "cancelled": EWorkflowTaskStatus.CANCELLED,
        }
        return dict_status.get(str(str_status).lower(), util_safe_int(str_status))


class CWarehouseDashboard(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            from flask import request

            n_date = request.args.get("date", 0, type=int)
            str_warehouse_no = request.args.get("warehouse_no", "", type=str)
            n_item_category = request.args.get("itemCategory", 0, type=int)
            b_include_inventory = request.args.get("includeInventory", "false").lower() in ["1", "true", "yes"]
            b_risk_only = request.args.get("riskOnly", "false").lower() in ["1", "true", "yes"]
            n_trend_days = request.args.get("trendDays", 7, type=int)
            dict_extra_data = CWarehouseDashboardService().get_dashboard(
                n_date=n_date,
                str_timezone=str_timezone,
                str_warehouse_no=str_warehouse_no,
                n_item_category=n_item_category,
                b_include_inventory=b_include_inventory,
                b_risk_only=b_risk_only,
                n_trend_days=n_trend_days,
            )
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CWarehouseDashboard] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CWarehouseInventory(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            from flask import request

            dict_extra_data = CWarehouseInventoryService().get_inventory(
                n_date=request.args.get("date", 0, type=int),
                str_timezone=str_timezone,
                str_warehouse_no=request.args.get("warehouse_no", "", type=str),
                n_item_category=request.args.get("itemCategory", 0, type=int),
                str_item_no=request.args.get("item_no", "", type=str),
                str_batch_no=request.args.get("batchNo", "", type=str),
                str_risk_type=request.args.get("riskType", "", type=str),
                n_start=request.args.get("start", 0, type=int),
                n_count=request.args.get("count", 50, type=int),
            )
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CWarehouseInventory] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CWarehouseInventoryLots(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            from flask import request

            dict_extra_data = CWarehouseInventoryLotService().get_lots(
                n_date=request.args.get("date", 0, type=int),
                str_timezone=str_timezone,
                str_warehouse_no=request.args.get("warehouse_no", "", type=str),
                n_item_category=request.args.get("itemCategory", 0, type=int),
                str_item_no=request.args.get("item_no", "", type=str),
                str_batch_no=request.args.get("batchNo", "", type=str),
                str_risk_type=request.args.get("riskType", "", type=str),
                n_task_type=request.args.get("taskType", 0, type=int),
                str_availability=request.args.get("availability", "", type=str),
                str_keyword=request.args.get("keyword", "", type=str),
                str_sort=request.args.get("sort", "", type=str),
                str_order=request.args.get("order", "", type=str),
                n_start=request.args.get("start", 0, type=int),
                n_count=request.args.get("count", 50, type=int),
            )
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CWarehouseInventoryLots] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CWarehouseInventoryLotDetail(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            from flask import request

            lst_parts = (str_id or "").split("|")
            str_warehouse_no = lst_parts[0] if len(lst_parts) > 0 else ""
            str_item_no = lst_parts[1] if len(lst_parts) > 1 else ""
            str_batch_no = lst_parts[2] if len(lst_parts) > 2 else ""
            dict_extra_data = CWarehouseInventoryLotService().get_lot_detail(
                n_date=request.args.get("date", 0, type=int),
                str_timezone=str_timezone,
                str_warehouse_no=str_warehouse_no,
                str_item_no=str_item_no,
                str_batch_no=str_batch_no,
            )
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CWarehouseInventoryLotDetail] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CWarehouseTasks(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            from flask import request

            dict_extra_data = CWarehouseTaskService().get_tasks(
                n_date=request.args.get("date", 0, type=int),
                str_timezone=str_timezone,
                n_task_type=request.args.get("taskType", 0, type=int),
                str_warehouse_no=request.args.get("warehouse_no", "", type=str),
                str_status=request.args.get("status", "", type=str),
                n_start=request.args.get("start", 0, type=int),
                n_count=request.args.get("count", 50, type=int),
            )
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CWarehouseTasks] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CWarehouseTaskWorkbench(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            from flask import request

            if str_id:
                dict_extra_data = CWarehouseTaskWorkbenchService().get_task_detail(
                    n_date=request.args.get("date", 0, type=int),
                    str_timezone=str_timezone,
                    str_task_id=str_id,
                )
            else:
                dict_extra_data = CWarehouseTaskWorkbenchService().get_task_workbench(
                    n_date=request.args.get("date", 0, type=int),
                    str_timezone=str_timezone,
                    str_date_range=request.args.get("dateRange", "today", type=str),
                    str_warehouse_no=request.args.get("warehouse_no", "", type=str),
                    n_task_type=request.args.get("taskType", 0, type=int),
                    str_status=request.args.get("status", "", type=str),
                    n_owner_department=request.args.get("ownerDepartment", 0, type=int),
                    b_risk_only=request.args.get("riskOnly", "false").lower() in ["1", "true", "yes"],
                    str_keyword=request.args.get("keyword", "", type=str),
                    str_sort=request.args.get("sort", "", type=str),
                    str_order=request.args.get("order", "", type=str),
                    n_start=request.args.get("start", 0, type=int),
                    n_count=request.args.get("count", 50, type=int),
                )
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CWarehouseTaskWorkbench] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data
