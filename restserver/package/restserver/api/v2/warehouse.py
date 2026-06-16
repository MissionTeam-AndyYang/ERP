# coding=utf8
import time
from collections import defaultdict
from sqlalchemy import case, func

from package.common.common import (
    EErrorCode,
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
    CTableInventoryRec,
    CTableItemSafetyStock,
    CTableShipWarehouse,
    CTableShipWarehouseAlias,
    CTableShipWarehouseContract,
    CTableWarehouseInventoryReservation,
    CTableWarehousePalletMovement,
    CTableWarehouseQualityHold,
    CTableWarehouseRiskRule,
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
    ):
        n_query_timestamp = n_date if n_date else int(time.time())
        dict_range = self.__build_range(n_query_timestamp, str_timezone)
        lst_inventory_rows = self.__query_inventory_rows(
            obj_session,
            str_warehouse_no,
            n_item_category,
        )
        dict_reservations = self.__query_reservations(obj_session, n_query_timestamp)
        dict_quality_holds = self.__query_quality_holds(obj_session)
        dict_pallets = self.__query_pallets(obj_session, str_warehouse_no, n_item_category)
        dict_capacity = self.__query_capacity(obj_session, str_warehouse_no)
        dict_safety_stock = self.__query_safety_stock(obj_session, n_query_timestamp)
        dict_risk_rules = self.__query_risk_rules(obj_session)
        lst_risks = self.__build_risk_alerts(
            lst_inventory_rows,
            dict_safety_stock,
            dict_risk_rules,
            n_query_timestamp,
            b_risk_only,
        )
        lst_tasks = self.__query_pending_tasks(obj_session, str_warehouse_no)
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
            b_include_inventory,
        )
        return dict_payload

    def __build_range(self, n_timestamp, str_timezone):
        n_start = n_timestamp - (n_timestamp % 86400)
        n_end = n_start + 86399
        return {
            "date": time.strftime("%Y-%m-%d", time.gmtime(n_timestamp)),
            "startTimestamp": n_start,
            "endTimestamp": n_end,
        }

    def __query_inventory_rows(self, obj_session, str_warehouse_no, n_item_category):
        lst_filters = [CTableInventoryRec.itemCategory.in_(self.__target_categories())]
        if str_warehouse_no:
            lst_filters.append(CTableInventoryRec.warehouse_no == str_warehouse_no)
        if n_item_category:
            lst_filters.append(CTableInventoryRec.itemCategory == n_item_category)

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
                    CTableBatchNumber.validDays,
                    CTableBatchNumber.validDate,
                )
                .filter(CTableBatchNumber.no.in_(lst_batch_numbers))
                .all()
            )
            dict_batch = {
                obj_row.no: {
                    "validDays": util_safe_int(obj_row.validDays),
                    "validDate": util_safe_int(obj_row.validDate),
                }
                for obj_row in lst_batch_rows
            }

        lst_results = []
        for obj_row in lst_rows:
            f_quantity = util_safe_float(obj_row.currentQuantity)
            if f_quantity <= 0:
                continue
            dict_batch_info = dict_batch.get(obj_row.batchNumber, {})
            lst_results.append({
                "warehouseNo": obj_row.warehouse_no or "",
                "warehouseName": obj_row.warehouse_displayName or "",
                "itemCategory": util_safe_int(obj_row.itemCategory),
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

    def __query_quality_holds(self, obj_session):
        lst_rows = (
            obj_session.query(
                CTableWarehouseQualityHold.item_no,
                CTableWarehouseQualityHold.batchNumber,
                CTableWarehouseQualityHold.warehouse_no,
                func.sum(CTableWarehouseQualityHold.holdQuantity).label("holdQuantity"),
                func.sum(CTableWarehouseQualityHold.holdValue).label("holdValue"),
            )
            .filter(CTableWarehouseQualityHold.status == self.QUALITY_HOLD_STATUS_ACTIVE)
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

    def __query_pallets(self, obj_session, str_warehouse_no, n_item_category):
        lst_filters = []
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
                "message": obj_row.messageTemplateZhTw or "",
                "recommendedAction": obj_row.recommendedActionTemplateZhTw or "",
            }
            for obj_row in lst_rows
        }

    def __query_pending_tasks(self, obj_session, str_warehouse_no):
        lst_filters = [
            CTableWorkflowTaskState.taskStatus.in_([
                EWorkflowTaskStatus.PENDING,
                EWorkflowTaskStatus.PARTIAL,
                EWorkflowTaskStatus.BLOCKED,
            ])
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
        return [self.__task_to_dict(obj_row) for obj_row in lst_rows]

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
        b_include_inventory,
    ):
        dict_category = self.__build_category_summary(
            lst_inventory_rows,
            dict_reservations,
            dict_quality_holds,
            dict_pallets,
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
            "valueTrend": [],
            "inventory": self.__build_inventory_detail(
                lst_inventory_rows,
                dict_reservations,
                dict_quality_holds,
            ) if b_include_inventory else [],
        }

    def __build_category_summary(self, lst_inventory_rows, dict_reservations, dict_quality_holds, dict_pallets):
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
            dict_summary["trend7Days"] = util_round_quantity(dict_summary["trend7Days"])
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
            if f_safety_stock and util_safe_float(dict_row.get("currentQuantity")) < f_safety_stock:
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
        str_default_message = self.__risk_message(str_risk_type)
        str_default_action = self.__risk_action(str_risk_type)
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
            "remainingShelfLifeRatio": self.__remaining_shelf_life_ratio(dict_row, n_query_timestamp),
            "safetyStock": util_round_quantity(f_safety_stock),
            "message": self.__safe_risk_text(dict_rule.get("message"), str_default_message),
            "recommendedAction": self.__safe_risk_text(dict_rule.get("recommendedAction"), str_default_action),
        }

    def __task_to_dict(self, obj_row):
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
            "warehouseName": "",
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

    def __risk_message(self, str_risk_type):
        dict_messages = {
            EWarehouseRiskType.TURNOVER_OVER_30_DAYS: "此批庫存迴轉週期超過 30 天。",
            EWarehouseRiskType.SHELF_LIFE_LT_ONE_THIRD: "此批庫存剩餘效期低於三分之一。",
            EWarehouseRiskType.BELOW_SAFETY_STOCK: "目前可用量低於安全水位。",
        }
        return dict_messages.get(str_risk_type, "")

    def __risk_action(self, str_risk_type):
        dict_actions = {
            EWarehouseRiskType.TURNOVER_OVER_30_DAYS: "建議確認是否安排出庫、生產使用或庫存處置。",
            EWarehouseRiskType.SHELF_LIFE_LT_ONE_THIRD: "建議優先安排出庫或轉生產使用。",
            EWarehouseRiskType.BELOW_SAFETY_STOCK: "建議建立請購或確認已下採購單。",
        }
        return dict_actions.get(str_risk_type, "")

    def __safe_risk_text(self, str_value, str_default):
        if not str_value:
            return str_default
        if any(str_marker in str_value for str_marker in ["Ã", "Â", "�"]):
            return str_default
        return str_value


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
        dict_dashboard = CWarehouseDashboardService().get_dashboard(
            n_date=n_query_timestamp,
            str_timezone=str_timezone,
            str_warehouse_no=str_warehouse_no,
            n_item_category=n_item_category,
            b_include_inventory=True,
            obj_session=obj_session,
        )
        dict_risks = self.__group_risks(dict_dashboard.get("riskAlerts", []))
        dict_pallets = self.__query_pallet_counts(obj_session)
        dict_sources = self.__query_latest_sources(obj_session)
        lst_results = []

        for dict_row in dict_dashboard.get("inventory", []):
            str_key = self.__stock_key(
                dict_row.get("itemNo"),
                dict_row.get("batchNo"),
                dict_row.get("warehouseNo"),
            )
            dict_risk = dict_risks.get(str_key, {"riskTypes": [], "safetyStock": 0.0})
            dict_source = dict_sources.get(str_key, {})
            dict_inventory = self.__inventory_to_dict(
                dict_row,
                dict_risk,
                util_safe_float(dict_pallets.get(str_key)),
                dict_source,
                n_query_timestamp,
            )
            if self.__is_inventory_matched(dict_inventory, str_item_no, str_batch_no, str_risk_type):
                lst_results.append(dict_inventory)

        n_start = max(util_safe_int(n_start), 0)
        n_count = util_safe_int(n_count) if n_count else 50
        if n_count <= 0:
            n_count = 50
        lst_page = lst_results[n_start:n_start + n_count]
        return {
            "serverTimestamp": n_query_timestamp,
            "timezone": str_timezone or "UTC",
            "total": len(lst_results),
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
            "sourceType": self.__source_type(util_safe_int(dict_source.get("refCategory"))),
            "sourceNo": dict_source.get("refNo", ""),
            "sourceRefCategory": util_safe_int(dict_source.get("refCategory")),
            "qualityStatus": "hold" if util_safe_float(dict_row.get("qualityHoldQuantity")) else "released",
            "riskTypes": dict_risk.get("riskTypes", []),
        }

    def __is_inventory_matched(self, dict_inventory, str_item_no, str_batch_no, str_risk_type):
        if str_item_no and dict_inventory.get("itemNo") != str_item_no:
            return False
        if str_batch_no and dict_inventory.get("batchNo") != str_batch_no:
            return False
        if str_risk_type and str_risk_type not in dict_inventory.get("riskTypes", []):
            return False
        return True

    def __group_risks(self, lst_risks):
        dict_result = defaultdict(lambda: {"riskTypes": [], "safetyStock": 0.0})
        for dict_risk in lst_risks:
            str_key = self.__stock_key(
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

    def __query_pallet_counts(self, obj_session):
        lst_rows = (
            obj_session.query(
                CTableWarehousePalletMovement.item_no,
                CTableWarehousePalletMovement.batchNumber,
                CTableWarehousePalletMovement.warehouse_no,
                func.sum(CTableWarehousePalletMovement.palletCount).label("palletCount"),
            )
            .filter(CTableWarehousePalletMovement.palletStatus == CWarehouseDashboardService.PALLET_STATUS_USED)
            .group_by(
                CTableWarehousePalletMovement.item_no,
                CTableWarehousePalletMovement.batchNumber,
                CTableWarehousePalletMovement.warehouse_no,
            )
            .all()
        )
        return {
            self.__stock_key(obj_row.item_no, obj_row.batchNumber, obj_row.warehouse_no): util_round_quantity(obj_row.palletCount)
            for obj_row in lst_rows
        }

    def __query_latest_sources(self, obj_session):
        lst_rows = (
            obj_session.query(CTableInventoryRec)
            .filter(CTableInventoryRec.category == EInventoryCategory.IN)
            .order_by(CTableInventoryRec.date.desc(), CTableInventoryRec.id.desc())
            .all()
        )
        dict_result = {}
        for obj_row in lst_rows:
            str_key = self.__stock_key(obj_row.item_no, obj_row.batchNumber, obj_row.warehouse_no)
            if str_key not in dict_result:
                dict_result[str_key] = {
                    "refNo": obj_row.ref_no or "",
                    "refCategory": util_safe_int(obj_row.refCategory),
                }
        return dict_result

    def __stock_key(self, str_item_no, str_batch_no, str_warehouse_no):
        return "%s|%s|%s" % (str_item_no or "", str_batch_no or "", str_warehouse_no or "")

    def __inventory_id(self, str_warehouse_no, str_item_no, str_batch_no, str_serial_no):
        return "%s|%s|%s|%s" % (str_warehouse_no or "", str_item_no or "", str_batch_no or "", str_serial_no or "")

    def __source_type(self, n_ref_category):
        dict_source_type = {
            1: "PURCHASE",
            2: "SALE",
            3: "WORK",
            4: "OTHER",
        }
        return dict_source_type.get(n_ref_category, "OTHER")


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
            n_start_day = n_date - (n_date % 86400)
            n_end_day = n_start_day + 86399
            lst_filters.append(CTableWorkflowTaskState.dueTimestamp <= n_end_day)

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
        return {
            "serverTimestamp": n_date if n_date else int(time.time()),
            "timezone": str_timezone or "UTC",
            "total": len(lst_rows),
            "count": len(lst_page),
            "start": n_start,
            "results": [self.__task_to_dict(obj_row) for obj_row in lst_page],
        }

    def __task_to_dict(self, obj_row):
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
            "warehouseName": "",
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
            dict_extra_data = CWarehouseDashboardService().get_dashboard(
                n_date=n_date,
                str_timezone=str_timezone,
                str_warehouse_no=str_warehouse_no,
                n_item_category=n_item_category,
                b_include_inventory=b_include_inventory,
                b_risk_only=b_risk_only,
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
