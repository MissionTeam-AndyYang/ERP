# coding=utf8
import time
from collections import defaultdict

from sqlalchemy import Column, Float, Integer, String, Text, UniqueConstraint
from sqlalchemy import case, distinct, func

from package.common.common import (
    EDepartment,
    EErrorCode,
    EInventoryCategory,
    EItemCategory,
)
from package.dbwrapper.dbmgr import CDBMgr, obj_base
from package.dbwrapper.table import (
    CTableBatchNumber,
    CTableInventoryRec,
    CTableShipWarehouse,
    CTableShipWarehouseAlias,
    CTableShipWarehouseContract,
)
from package.log.log import CLogger


class EWarehouseRiskType(object):
    TURNOVER_OVER_30_DAYS = "TURNOVER_OVER_30_DAYS"
    SHELF_LIFE_LT_ONE_THIRD = "SHELF_LIFE_LT_ONE_THIRD"
    BELOW_SAFETY_STOCK = "BELOW_SAFETY_STOCK"


class EWarehouseRiskLevel(object):
    NORMAL = 1
    NOTICE = 2
    WARNING = 3
    DANGER = 4


class EWorkflowTaskStatus(object):
    PENDING = 1
    PARTIAL = 2
    DONE = 3
    BLOCKED = 4
    CANCELLED = 5


class EWorkflowTaskType(object):
    PURCHASE_REQUEST = 1
    PURCHASE = 2
    GOODS_RECEIPT = 3
    INBOUND = 4
    OUTBOUND = 5
    TRANSFER = 6
    PRODUCTION = 7
    QUALITY = 8
    SHIPMENT = 9


class CTableWarehouseInventoryReservation(obj_base):
    __tablename__ = "warehouse_inventory_reservation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    date = Column(Integer)
    refCategory = Column(Integer)
    ref_no = Column(String(length=60))
    ref_sub_no = Column(String(length=60))
    warehouse_no = Column(String(length=60))
    warehouse_displayName = Column(String(length=60))
    itemCategory = Column(Integer)
    item_no = Column(String(length=60))
    item_name = Column(String(length=255))
    batchNumber = Column(String(length=60))
    unit = Column(Integer)
    reservedQuantity = Column(Float)
    unitCost = Column(Float)
    reservedValue = Column(Float)
    status = Column(Integer)
    releaseTime = Column(Integer)
    comment = Column(Text)
    creationTime = Column(Integer)

    __table_args__ = (
        UniqueConstraint("no", name="uq_warehouse_inventory_reservation_composite"),
    )


class CTableWarehouseQualityHold(obj_base):
    __tablename__ = "warehouse_quality_hold"

    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    date = Column(Integer)
    refCategory = Column(Integer)
    ref_no = Column(String(length=60))
    ref_sub_no = Column(String(length=60))
    inspection_no = Column(String(length=60))
    warehouse_no = Column(String(length=60))
    warehouse_displayName = Column(String(length=60))
    itemCategory = Column(Integer)
    item_no = Column(String(length=60))
    item_name = Column(String(length=255))
    batchNumber = Column(String(length=60))
    unit = Column(Integer)
    holdQuantity = Column(Float)
    unitCost = Column(Float)
    holdValue = Column(Float)
    status = Column(Integer)
    releaseTime = Column(Integer)
    reason = Column(String(length=255))
    comment = Column(Text)
    creationTime = Column(Integer)

    __table_args__ = (
        UniqueConstraint("no", name="uq_warehouse_quality_hold_composite"),
    )


class CTableWarehousePalletMovement(obj_base):
    __tablename__ = "warehouse_pallet_movement"

    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    date = Column(Integer)
    inventory_record_id = Column(Integer)
    refCategory = Column(Integer)
    ref_no = Column(String(length=60))
    warehouse_no = Column(String(length=60))
    pallet_group_no = Column(String(length=60))
    batchNumber = Column(String(length=60))
    serialNo = Column(String(length=60))
    itemCategory = Column(Integer)
    item_no = Column(String(length=60))
    palletStatus = Column(Integer)
    palletCount = Column(Float)
    creationTime = Column(Integer)

    __table_args__ = (
        UniqueConstraint("no", name="uq_warehouse_pallet_movement_composite"),
    )


class CTableItemSafetyStock(obj_base):
    __tablename__ = "item_safety_stock"

    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    itemCategory = Column(Integer)
    item_no = Column(String(length=60))
    item_name = Column(String(length=255))
    warehouse_no = Column(String(length=60))
    unit = Column(Integer)
    safetyStock = Column(Float)
    effectiveDate = Column(Integer)
    expiryDate = Column(Integer)
    status = Column(Integer)
    comment = Column(Text)
    creationTime = Column(Integer)

    __table_args__ = (
        UniqueConstraint("no", name="uq_item_safety_stock_composite"),
    )


class CTableWarehouseRiskRule(obj_base):
    __tablename__ = "warehouse_risk_rule"

    id = Column(Integer, primary_key=True, autoincrement=True)
    riskType = Column(String(length=60))
    riskLevel = Column(Integer)
    messageCode = Column(String(length=80))
    messageTemplateZhTw = Column(String(length=255))
    recommendedActionCode = Column(String(length=80))
    recommendedActionTemplateZhTw = Column(String(length=255))
    thresholdValue = Column(Float)
    excludedItemCategories = Column(Text)
    status = Column(Integer)
    creationTime = Column(Integer)

    __table_args__ = (
        UniqueConstraint("riskType", name="uq_warehouse_risk_rule_composite"),
    )


class CTableWorkflowTaskState(obj_base):
    __tablename__ = "workflow_task_state"

    id = Column(Integer, primary_key=True, autoincrement=True)
    taskId = Column(String(length=80))
    module = Column(Integer)
    taskType = Column(Integer)
    refCategory = Column(Integer)
    ref_no = Column(String(length=60))
    ref_sub_no = Column(String(length=60))
    itemCategory = Column(Integer)
    item_no = Column(String(length=60))
    item_name = Column(String(length=255))
    batchNumber = Column(String(length=60))
    warehouse_no = Column(String(length=60))
    expectedQuantity = Column(Float)
    processedQuantity = Column(Float)
    acceptedQuantity = Column(Float)
    rejectedQuantity = Column(Float)
    cancelledQuantity = Column(Float)
    unit = Column(Integer)
    palletCount = Column(Float)
    dueTimestamp = Column(Integer)
    taskStatus = Column(Integer)
    ownerDepartment = Column(Integer)
    blockReasonCode = Column(String(length=80))
    blockReason = Column(String(length=255))
    updateTime = Column(Integer)
    creationTime = Column(Integer)

    __table_args__ = (
        UniqueConstraint("taskId", name="uq_workflow_task_state_composite"),
    )


class CTableWorkflowNextOwnerRule(obj_base):
    __tablename__ = "workflow_next_owner_rule"

    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    module = Column(Integer)
    taskType = Column(Integer)
    refCategory = Column(Integer)
    taskStatus = Column(Integer)
    blockReasonCode = Column(String(length=80))
    fromDepartment = Column(Integer)
    ownerDepartment = Column(Integer)
    rulePriority = Column(Integer)
    status = Column(Integer)
    comment = Column(Text)
    creationTime = Column(Integer)

    __table_args__ = (
        UniqueConstraint("no", name="uq_workflow_next_owner_rule_composite"),
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
        f_include_inventory=False,
        f_risk_only=False,
        obj_session=None,
    ):
        if obj_session:
            return self.__get_dashboard_with_session(
                obj_session,
                n_date,
                str_timezone,
                str_warehouse_no,
                n_item_category,
                f_include_inventory,
                f_risk_only,
            )

        with CDBMgr() as obj_dbmgr:
            return self.__get_dashboard_with_session(
                obj_dbmgr.get_session(),
                n_date,
                str_timezone,
                str_warehouse_no,
                n_item_category,
                f_include_inventory,
                f_risk_only,
            )

    def __get_dashboard_with_session(
        self,
        obj_session,
        n_date,
        str_timezone,
        str_warehouse_no,
        n_item_category,
        f_include_inventory,
        f_risk_only,
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
            f_risk_only,
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
            f_include_inventory,
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
                    "validDays": self.__safe_int(obj_row.validDays),
                    "validDate": self.__safe_int(obj_row.validDate),
                }
                for obj_row in lst_batch_rows
            }

        lst_results = []
        for obj_row in lst_rows:
            f_quantity = self.__safe_float(obj_row.currentQuantity)
            if f_quantity <= 0:
                continue
            dict_batch_info = dict_batch.get(obj_row.batchNumber, {})
            lst_results.append({
                "warehouseNo": obj_row.warehouse_no or "",
                "warehouseName": obj_row.warehouse_displayName or "",
                "itemCategory": self.__safe_int(obj_row.itemCategory),
                "itemNo": obj_row.item_no or "",
                "itemName": obj_row.item_name or "",
                "batchNo": obj_row.batchNumber or "",
                "unit": self.__safe_int(obj_row.unit),
                "currentQuantity": f_quantity,
                "inventoryValue": self.__safe_float(obj_row.inventoryValue),
                "firstInboundTimestamp": self.__safe_int(obj_row.firstInboundTimestamp),
                "validDays": self.__safe_int(dict_batch_info.get("validDays", 0)),
                "validDate": self.__safe_int(dict_batch_info.get("validDate", 0)),
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
                "reservedQuantity": self.__safe_float(obj_row.reservedQuantity),
                "reservedValue": self.__safe_float(obj_row.reservedValue),
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
                "qualityHoldQuantity": self.__safe_float(obj_row.holdQuantity),
                "qualityHoldValue": self.__safe_float(obj_row.holdValue),
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
            f_pallet_count = self.__safe_float(obj_row.palletCount)
            if obj_row.palletStatus == self.PALLET_STATUS_USED:
                dict_result["byWarehouse"][obj_row.warehouse_no]["usedPallets"] += f_pallet_count
                dict_result["byCategory"][self.__safe_int(obj_row.itemCategory)] += f_pallet_count
            elif obj_row.palletStatus == self.PALLET_STATUS_RESERVED:
                dict_result["byWarehouse"][obj_row.warehouse_no]["reservedPallets"] += f_pallet_count
        return dict_result

    def __query_capacity(self, obj_session, str_warehouse_no):
        lst_filters = []
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
                "warehouseType": self.__safe_int(obj_row.type),
                "totalPallets": self.__safe_float(obj_row.totalPallets),
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
            n_effective = self.__safe_int(obj_row.effectiveDate)
            n_expiry = self.__safe_int(obj_row.expiryDate)
            if n_effective and n_effective > n_query_timestamp:
                continue
            if n_expiry and n_expiry < n_query_timestamp:
                continue
            dict_result[(obj_row.item_no or "", obj_row.warehouse_no or "")] = self.__safe_float(obj_row.safetyStock)
        return dict_result

    def __query_risk_rules(self, obj_session):
        lst_rows = (
            obj_session.query(CTableWarehouseRiskRule)
            .filter(CTableWarehouseRiskRule.status == self.STATUS_ACTIVE)
            .all()
        )
        return {
            obj_row.riskType: {
                "riskLevel": self.__safe_int(obj_row.riskLevel),
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
        f_include_inventory,
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
            ) if f_include_inventory else [],
        }

    def __build_category_summary(self, lst_inventory_rows, dict_reservations, dict_quality_holds, dict_pallets):
        dict_category = {}
        for n_category in self.__target_categories():
            dict_category[n_category] = {
                "itemCategory": n_category,
                "categoryName": self.__category_name(n_category),
                "inventoryValue": 0.0,
                "reservedValue": 0.0,
                "availableValue": 0.0,
                "qualityHoldValue": 0.0,
                "quantity": 0.0,
                "unit": 0,
                "palletCount": self.__safe_float(dict_pallets["byCategory"].get(n_category, 0.0)),
                "itemCount": 0,
                "valueRatio": 0.0,
                "trend7Days": 0.0,
            }
        dict_items = defaultdict(set)
        for dict_row in lst_inventory_rows:
            n_category = self.__safe_int(dict_row.get("itemCategory"))
            dict_summary = dict_category.setdefault(n_category, {
                "itemCategory": n_category,
                "categoryName": self.__category_name(n_category),
                "inventoryValue": 0.0,
                "reservedValue": 0.0,
                "availableValue": 0.0,
                "qualityHoldValue": 0.0,
                "quantity": 0.0,
                "unit": 0,
                "palletCount": self.__safe_float(dict_pallets["byCategory"].get(n_category, 0.0)),
                "itemCount": 0,
                "valueRatio": 0.0,
                "trend7Days": 0.0,
            })
            str_key = self.__stock_key(
                dict_row.get("itemNo"),
                dict_row.get("batchNo"),
                dict_row.get("warehouseNo"),
            )
            f_reserved_value = self.__safe_float(dict_reservations.get(str_key, {}).get("reservedValue"))
            f_quality_value = self.__safe_float(dict_quality_holds.get(str_key, {}).get("qualityHoldValue"))
            dict_summary["inventoryValue"] += self.__safe_float(dict_row.get("inventoryValue"))
            dict_summary["reservedValue"] += f_reserved_value
            dict_summary["qualityHoldValue"] += f_quality_value
            dict_summary["quantity"] += self.__safe_float(dict_row.get("currentQuantity"))
            dict_items[n_category].add(dict_row.get("itemNo"))
        f_total_value = sum(dict_row["inventoryValue"] for dict_row in dict_category.values())
        for n_category, dict_summary in dict_category.items():
            dict_summary["availableValue"] = max(
                dict_summary["inventoryValue"]
                - dict_summary["reservedValue"]
                - dict_summary["qualityHoldValue"],
                0.0,
            )
            dict_summary["itemCount"] = len(dict_items[n_category])
            dict_summary["valueRatio"] = round(dict_summary["inventoryValue"] / f_total_value * 100, 2) if f_total_value else 0.0
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
            f_used = self.__safe_float(dict_pallet.get("usedPallets"))
            f_reserved = self.__safe_float(dict_pallet.get("reservedPallets"))
            f_total = self.__safe_float(dict_base.get("totalPallets"))
            f_available = max(f_total - f_used - f_reserved, 0.0)
            f_rate = round(f_used / f_total * 100, 2) if f_total else 0.0
            lst_results.append({
                "warehouseNo": dict_base.get("warehouseNo", ""),
                "warehouseName": dict_base.get("warehouseName", ""),
                "warehouseType": self.__safe_int(dict_base.get("warehouseType")),
                "totalPallets": f_total,
                "usedPallets": f_used,
                "reservedPallets": f_reserved,
                "availablePallets": f_available,
                "utilizationRate": f_rate,
                "riskLevel": self.__capacity_risk_level(f_rate),
            })
        return lst_results

    def __build_summary(self, dict_category, lst_capacity, lst_risks, lst_tasks):
        f_total_value = sum(dict_row["inventoryValue"] for dict_row in dict_category.values())
        f_reserved_value = sum(dict_row["reservedValue"] for dict_row in dict_category.values())
        f_quality_value = sum(dict_row["qualityHoldValue"] for dict_row in dict_category.values())
        f_total_pallets = sum(self.__safe_float(dict_row.get("totalPallets")) for dict_row in lst_capacity)
        f_used_pallets = sum(self.__safe_float(dict_row.get("usedPallets")) for dict_row in lst_capacity)
        f_reserved_pallets = sum(self.__safe_float(dict_row.get("reservedPallets")) for dict_row in lst_capacity)
        return {
            "totalInventoryValue": f_total_value,
            "reservedInventoryValue": f_reserved_value,
            "availableInventoryValue": max(f_total_value - f_reserved_value - f_quality_value, 0.0),
            "qualityHoldInventoryValue": f_quality_value,
            "totalPallets": f_total_pallets,
            "usedPallets": f_used_pallets,
            "reservedPallets": f_reserved_pallets,
            "availablePallets": max(f_total_pallets - f_used_pallets - f_reserved_pallets, 0.0),
            "riskAlertCount": len(lst_risks),
            "pendingInboundCount": len([dict_row for dict_row in lst_tasks if dict_row.get("taskType") in [EWorkflowTaskType.GOODS_RECEIPT, EWorkflowTaskType.INBOUND]]),
            "pendingOutboundCount": len([dict_row for dict_row in lst_tasks if dict_row.get("taskType") in [EWorkflowTaskType.OUTBOUND, EWorkflowTaskType.SHIPMENT]]),
        }

    def __build_inventory_detail(self, lst_inventory_rows, dict_reservations, dict_quality_holds):
        lst_results = []
        for dict_row in lst_inventory_rows:
            str_key = self.__stock_key(dict_row.get("itemNo"), dict_row.get("batchNo"), dict_row.get("warehouseNo"))
            f_reserved = self.__safe_float(dict_reservations.get(str_key, {}).get("reservedQuantity"))
            f_quality = self.__safe_float(dict_quality_holds.get(str_key, {}).get("qualityHoldQuantity"))
            f_quantity = self.__safe_float(dict_row.get("currentQuantity"))
            dict_data = dict(dict_row)
            dict_data.update({
                "reservedQuantity": f_reserved,
                "availableQuantity": max(f_quantity - f_reserved - f_quality, 0.0),
                "qualityHoldQuantity": f_quality,
                "reservedValue": self.__safe_float(dict_reservations.get(str_key, {}).get("reservedValue")),
                "availableValue": max(
                    self.__safe_float(dict_row.get("inventoryValue"))
                    - self.__safe_float(dict_reservations.get(str_key, {}).get("reservedValue"))
                    - self.__safe_float(dict_quality_holds.get(str_key, {}).get("qualityHoldValue")),
                    0.0,
                ),
                "qualityHoldValue": self.__safe_float(dict_quality_holds.get(str_key, {}).get("qualityHoldValue")),
            })
            lst_results.append(dict_data)
        return lst_results

    def __build_risk_alerts(
        self,
        lst_inventory_rows,
        dict_safety_stock,
        dict_risk_rules,
        n_query_timestamp,
        f_risk_only,
    ):
        lst_results = []
        for dict_row in lst_inventory_rows:
            lst_row_risks = []
            n_item_category = self.__safe_int(dict_row.get("itemCategory"))
            n_valid_date = self.__safe_int(dict_row.get("validDate"))
            n_valid_days = self.__safe_int(dict_row.get("validDays"))
            if n_valid_date and n_valid_days and n_item_category not in [EItemCategory.MA, EItemCategory.AF]:
                n_remaining = n_valid_date - n_query_timestamp
                if n_remaining <= (n_valid_days * 86400 / 3):
                    lst_row_risks.append(EWarehouseRiskType.SHELF_LIFE_LT_ONE_THIRD)
            n_first_inbound = self.__safe_int(dict_row.get("firstInboundTimestamp"))
            if n_first_inbound and (n_query_timestamp - n_first_inbound) > 30 * 86400:
                lst_row_risks.append(EWarehouseRiskType.TURNOVER_OVER_30_DAYS)
            f_safety_stock = self.__safe_float(dict_safety_stock.get((dict_row.get("itemNo"), dict_row.get("warehouseNo"))))
            if not f_safety_stock:
                f_safety_stock = self.__safe_float(dict_safety_stock.get((dict_row.get("itemNo"), "")))
            if f_safety_stock and self.__safe_float(dict_row.get("currentQuantity")) < f_safety_stock:
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
        n_first_inbound = self.__safe_int(dict_row.get("firstInboundTimestamp"))
        n_days_in_stock = int((n_query_timestamp - n_first_inbound) / 86400) if n_first_inbound else 0
        dict_rule = dict_risk_rules.get(str_risk_type, {})
        return {
            "alertId": "%s-%s-%s-%s" % (
                str_risk_type,
                dict_row.get("warehouseNo", ""),
                dict_row.get("itemNo", ""),
                dict_row.get("batchNo", ""),
            ),
            "riskType": str_risk_type,
            "riskLevel": self.__risk_level_name(dict_rule.get("riskLevel"), str_risk_type),
            "itemNo": dict_row.get("itemNo", ""),
            "itemName": dict_row.get("itemName", ""),
            "itemCategory": self.__safe_int(dict_row.get("itemCategory")),
            "batchNo": dict_row.get("batchNo", ""),
            "warehouseNo": dict_row.get("warehouseNo", ""),
            "warehouseName": dict_row.get("warehouseName", ""),
            "quantity": self.__safe_float(dict_row.get("currentQuantity")),
            "unit": self.__safe_int(dict_row.get("unit")),
            "inventoryValue": self.__safe_float(dict_row.get("inventoryValue")),
            "daysInStock": n_days_in_stock,
            "validDate": self.__safe_int(dict_row.get("validDate")),
            "remainingShelfLifeRatio": self.__remaining_shelf_life_ratio(dict_row, n_query_timestamp),
            "safetyStock": f_safety_stock,
            "message": dict_rule.get("message") or self.__risk_message(str_risk_type),
            "recommendedAction": dict_rule.get("recommendedAction") or self.__risk_action(str_risk_type),
        }

    def __task_to_dict(self, obj_row):
        return {
            "taskId": obj_row.taskId or "",
            "taskType": self.__safe_int(obj_row.taskType),
            "refCategory": self.__safe_int(obj_row.refCategory),
            "sourceNo": obj_row.ref_no or "",
            "sourceSubNo": obj_row.ref_sub_no or "",
            "itemNo": obj_row.item_no or "",
            "itemName": obj_row.item_name or "",
            "itemCategory": self.__safe_int(obj_row.itemCategory),
            "batchNo": obj_row.batchNumber or "",
            "expectedQuantity": self.__safe_float(obj_row.expectedQuantity),
            "processedQuantity": self.__safe_float(obj_row.processedQuantity),
            "remainingQuantity": max(
                self.__safe_float(obj_row.expectedQuantity) - self.__safe_float(obj_row.processedQuantity),
                0.0,
            ),
            "unit": self.__safe_int(obj_row.unit),
            "palletCount": self.__safe_float(obj_row.palletCount),
            "warehouseNo": obj_row.warehouse_no or "",
            "warehouseName": "",
            "dueTimestamp": self.__safe_int(obj_row.dueTimestamp),
            "status": self.__task_status_name(self.__safe_int(obj_row.taskStatus)),
            "ownerDepartment": self.__department_name(self.__safe_int(obj_row.ownerDepartment)),
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

    def __category_name(self, n_category):
        dict_names = {
            EItemCategory.PM: "原料",
            EItemCategory.MA: "物料",
            EItemCategory.AF: "膠捲",
            EItemCategory.INPRODUCT: "在製品",
            EItemCategory.PRODUCT: "製成品",
            EItemCategory.GOODS: "貨品",
            EItemCategory.NONE: "其他",
        }
        return dict_names.get(n_category, "其他")

    def __department_name(self, n_department):
        dict_names = {
            EDepartment.SALES: "業務部",
            EDepartment.PRODUCTION: "製造部",
            EDepartment.QA: "品保部",
            EDepartment.PLANNING: "生管部",
            EDepartment.WAREHOUSE: "倉庫部",
            EDepartment.PURCHASING: "採購部",
            EDepartment.RD: "研發部",
            EDepartment.FINANCE: "財務部",
        }
        return dict_names.get(n_department, "")

    def __task_status_name(self, n_status):
        dict_names = {
            EWorkflowTaskStatus.PENDING: "pending",
            EWorkflowTaskStatus.PARTIAL: "partial",
            EWorkflowTaskStatus.DONE: "done",
            EWorkflowTaskStatus.BLOCKED: "blocked",
            EWorkflowTaskStatus.CANCELLED: "cancelled",
        }
        return dict_names.get(n_status, "pending")

    def __capacity_risk_level(self, f_rate):
        if f_rate >= 90:
            return "danger"
        if f_rate >= 75:
            return "warning"
        return "normal"

    def __risk_level_name(self, n_risk_level, str_risk_type):
        dict_names = {
            EWarehouseRiskLevel.NORMAL: "normal",
            EWarehouseRiskLevel.NOTICE: "notice",
            EWarehouseRiskLevel.WARNING: "warning",
            EWarehouseRiskLevel.DANGER: "danger",
        }
        if n_risk_level:
            return dict_names.get(n_risk_level, "warning")
        if str_risk_type == EWarehouseRiskType.SHELF_LIFE_LT_ONE_THIRD:
            return "danger"
        return "warning"

    def __remaining_shelf_life_ratio(self, dict_row, n_query_timestamp):
        n_valid_days = self.__safe_int(dict_row.get("validDays"))
        n_valid_date = self.__safe_int(dict_row.get("validDate"))
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

    def __safe_float(self, obj_value):
        try:
            return float(obj_value) if obj_value is not None else 0.0
        except (TypeError, ValueError):
            return 0.0

    def __safe_int(self, obj_value):
        try:
            return int(obj_value) if obj_value is not None else 0
        except (TypeError, ValueError):
            return 0


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
            f_include_inventory = request.args.get("includeInventory", "false").lower() in ["1", "true", "yes"]
            f_risk_only = request.args.get("riskOnly", "false").lower() in ["1", "true", "yes"]
            dict_extra_data = CWarehouseDashboardService().get_dashboard(
                n_date=n_date,
                str_timezone=str_timezone,
                str_warehouse_no=str_warehouse_no,
                n_item_category=n_item_category,
                f_include_inventory=f_include_inventory,
                f_risk_only=f_risk_only,
            )
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CWarehouseDashboard] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data
