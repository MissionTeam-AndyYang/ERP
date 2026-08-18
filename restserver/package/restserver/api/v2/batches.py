# coding=utf8
import time
from collections import defaultdict

from flask import request

from package.common.common import (
    EBatchExpiryStatusCode,
    EBatchQaStatusCode,
    EBatchRiskCode,
    EBatchRiskLevelCode,
    EBatchStageCode,
    EErrorCode,
    EWarehouseRiskType,
    EWorkflowTaskStatus,
)
from package.dbwrapper.dbmgr import CDBMgr
from package.dbwrapper.table import (
    CTableBatchNumber,
    CTableInventoryRec,
    CTableWarehouseInventoryReservation,
    CTableWarehousePalletMovement,
    CTableWarehouseQualityHold,
    CTableWorkflowTaskState,
)
from package.log.log import CLogger
from package.restserver.api.v2.warehouse import CWarehouseInventoryContextBuilder
from package.util.util import util_round_amount, util_round_quantity, util_safe_float, util_safe_int


class CBatchCenterService(object):
    ITEM_CATEGORY_ORDER = {
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        5: 5,
        6: 6,
        0: 7,
    }

    ACTIVE_STATUS = 1
    MAX_DETAIL_RECORDS = 100

    def get_dashboard(
        self,
        n_date=0,
        str_timezone="",
        str_keyword="",
        n_item_category=0,
        n_item_sub_category=0,
        n_item_type=0,
        str_warehouse_no="",
        str_batch_no="",
        str_risk_level_code="",
        str_qa_status_code="",
        str_batch_stage_code="",
        str_availability_code="",
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
                n_item_type,
                str_warehouse_no,
                str_batch_no,
                str_risk_level_code,
                str_qa_status_code,
                str_batch_stage_code,
                str_availability_code,
                n_start,
                n_count,
            )

    def get_distribution(
        self,
        str_item_no,
        n_date=0,
        str_timezone="",
        str_keyword="",
        n_item_category=0,
        n_item_sub_category=0,
        n_item_type=0,
        str_warehouse_no="",
        str_batch_no="",
        str_risk_level_code="",
        str_qa_status_code="",
        str_batch_stage_code="",
        str_availability_code="",
        n_start=0,
        n_count=50,
    ):
        with CDBMgr() as obj_dbmgr:
            return self.__get_distribution_with_session(
                obj_dbmgr.get_session(),
                str_item_no,
                n_date,
                str_timezone,
                str_keyword,
                n_item_category,
                n_item_sub_category,
                n_item_type,
                str_warehouse_no,
                str_batch_no,
                str_risk_level_code,
                str_qa_status_code,
                str_batch_stage_code,
                str_availability_code,
                n_start,
                n_count,
            )

    def get_detail(self, str_batch_no, n_date=0, str_timezone=""):
        with CDBMgr() as obj_dbmgr:
            return self.__get_detail_with_session(
                obj_dbmgr.get_session(),
                str_batch_no,
                n_date,
                str_timezone,
            )

    def __get_dashboard_with_session(
        self,
        obj_session,
        n_date,
        str_timezone,
        str_keyword,
        n_item_category,
        n_item_sub_category,
        n_item_type,
        str_warehouse_no,
        str_batch_no,
        str_risk_level_code,
        str_qa_status_code,
        str_batch_stage_code,
        str_availability_code,
        n_start,
        n_count,
    ):
        n_query_timestamp = util_safe_int(n_date) or util_safe_int(time.time())
        n_start, n_count = self.__normalize_page(n_start, n_count)
        obj_context_builder = CWarehouseInventoryContextBuilder()
        dict_context = obj_context_builder.build(
            obj_session=obj_session,
            n_query_timestamp=n_query_timestamp,
            str_timezone=str_timezone,
            str_warehouse_no=str_warehouse_no,
            n_item_category=n_item_category,
            str_item_no="",
            str_batch_no=str_batch_no,
            b_include_open_tasks=True,
        )
        lst_rows = self.__build_stock_rows(
            obj_session,
            obj_context_builder,
            dict_context,
            n_query_timestamp,
        )
        lst_rows = self.__filter_rows(
            lst_rows,
            str_keyword,
            n_item_category,
            n_item_sub_category,
            n_item_type,
            str_warehouse_no,
            str_batch_no,
            str_risk_level_code,
            str_qa_status_code,
            str_batch_stage_code,
            str_availability_code,
        )
        lst_items = self.__build_dashboard_items(lst_rows)
        n_total = len(lst_items)
        lst_page = lst_items[n_start:n_start + n_count]
        return {
            "serverTimestamp": n_query_timestamp,
            "summary": self.__build_dashboard_summary(lst_items),
            "items": lst_page,
            "total": n_total,
            "start": n_start,
            "count": len(lst_page),
        }

    def __get_distribution_with_session(
        self,
        obj_session,
        str_item_no,
        n_date,
        str_timezone,
        str_keyword,
        n_item_category,
        n_item_sub_category,
        n_item_type,
        str_warehouse_no,
        str_batch_no,
        str_risk_level_code,
        str_qa_status_code,
        str_batch_stage_code,
        str_availability_code,
        n_start,
        n_count,
    ):
        str_item_no = (str_item_no or "").strip()
        if not str_item_no:
            return None
        n_query_timestamp = util_safe_int(n_date) or util_safe_int(time.time())
        n_start, n_count = self.__normalize_page(n_start, n_count)
        obj_context_builder = CWarehouseInventoryContextBuilder()
        dict_context = obj_context_builder.build(
            obj_session=obj_session,
            n_query_timestamp=n_query_timestamp,
            str_timezone=str_timezone,
            str_warehouse_no=str_warehouse_no,
            n_item_category=n_item_category,
            str_item_no=str_item_no,
            str_batch_no=str_batch_no,
            b_include_open_tasks=True,
        )
        lst_rows = self.__build_stock_rows(
            obj_session,
            obj_context_builder,
            dict_context,
            n_query_timestamp,
        )
        lst_rows = self.__filter_rows(
            lst_rows,
            str_keyword,
            n_item_category,
            n_item_sub_category,
            n_item_type,
            str_warehouse_no,
            str_batch_no,
            str_risk_level_code,
            str_qa_status_code,
            str_batch_stage_code,
            str_availability_code,
        )
        lst_rows = sorted(
            lst_rows,
            key=lambda dict_row: (
                self.__risk_sort(dict_row.get("riskLevelCode")),
                util_safe_int(dict_row.get("validDate")) if util_safe_int(dict_row.get("validDate")) else 9999999999,
                dict_row.get("batchNo", ""),
                dict_row.get("warehouseNo", ""),
                dict_row.get("batchStageCode", ""),
            ),
        )
        n_total = len(lst_rows)
        lst_page = lst_rows[n_start:n_start + n_count]
        dict_item = self.__build_item_header(str_item_no, lst_rows)
        return {
            "item": dict_item,
            "batches": [self.__distribution_row(dict_row) for dict_row in lst_page],
            "total": n_total,
            "start": n_start,
            "count": len(lst_page),
        }

    def __get_detail_with_session(self, obj_session, str_batch_no, n_date, str_timezone):
        str_batch_no = (str_batch_no or "").strip()
        if not str_batch_no:
            return None
        n_query_timestamp = util_safe_int(n_date) or util_safe_int(time.time())
        obj_batch = self.__query_batch_header(obj_session, str_batch_no)
        if not obj_batch:
            return None
        obj_context_builder = CWarehouseInventoryContextBuilder()
        dict_context = obj_context_builder.build(
            obj_session=obj_session,
            n_query_timestamp=n_query_timestamp,
            str_timezone=str_timezone,
            str_warehouse_no="",
            n_item_category=0,
            str_item_no="",
            str_batch_no=str_batch_no,
            b_include_open_tasks=True,
        )
        lst_rows = self.__build_stock_rows(
            obj_session,
            obj_context_builder,
            dict_context,
            n_query_timestamp,
        )
        return {
            "batch": self.__batch_header_to_dict(obj_batch),
            "stockByWarehouse": [self.__stock_by_warehouse_row(dict_row) for dict_row in lst_rows],
            "inventoryRecords": self.__query_inventory_records(obj_session, str_batch_no),
            "reservations": self.__query_reservations(obj_session, str_batch_no),
            "qualityHolds": self.__query_quality_holds(obj_session, str_batch_no),
            "palletMovements": self.__query_pallet_movements(obj_session, str_batch_no),
            "tasks": self.__query_tasks(obj_session, str_batch_no),
        }

    def __build_stock_rows(self, obj_session, obj_context_builder, dict_context, n_query_timestamp):
        dict_sources = dict_context.get("sources", {})
        dict_related_documents = self.__query_related_documents(
            obj_session,
            dict_context.get("inventoryRows", []),
        )
        lst_rows = []
        for dict_inventory in dict_context.get("inventoryRows", []):
            if util_safe_float(dict_inventory.get("currentQuantity")) <= 0:
                continue
            str_key = obj_context_builder.stock_key(
                dict_inventory.get("itemNo"),
                dict_inventory.get("batchNo"),
                dict_inventory.get("warehouseNo"),
            )
            dict_source = dict_sources.get(dict_inventory.get("batchNo") or "", {})
            lst_tasks = dict_context.get("openTasks", {}).get(str_key, [])
            dict_risk = dict_context.get("risks", {}).get(str_key, {"riskTypes": []})
            lst_risk_codes = self.__risk_codes(dict_inventory, dict_risk, lst_tasks, n_query_timestamp)
            str_risk_level_code = self.__risk_level_code(lst_risk_codes, dict_inventory)
            str_risk_code = self.__primary_risk_code(lst_risk_codes)
            dict_row = {
                "batchNo": dict_inventory.get("batchNo", ""),
                "warehouseNo": dict_inventory.get("warehouseNo", ""),
                "warehouseName": dict_inventory.get("warehouseName", ""),
                "locationCode": "",
                "palletCount": util_round_quantity(dict_context.get("pallets", {}).get(str_key, 0.0)),
                "currentQuantity": util_round_quantity(dict_inventory.get("currentQuantity")),
                "availableQuantity": util_round_quantity(dict_inventory.get("availableQuantity")),
                "reservedQuantity": util_round_quantity(dict_inventory.get("reservedQuantity")),
                "qualityHoldQuantity": util_round_quantity(dict_inventory.get("qualityHoldQuantity")),
                "unit": util_safe_int(dict_inventory.get("unit")),
                "validDate": util_safe_int(dict_inventory.get("validDate")),
                "validDays": util_safe_int(dict_inventory.get("validDays")),
                "daysInStock": self.__days_in_stock(dict_inventory, n_query_timestamp),
                "expiryStatusCode": self.__expiry_status_code(dict_inventory, n_query_timestamp),
                "qaStatusCode": self.__qa_status_code(dict_inventory, lst_tasks),
                "batchStageCode": self.__batch_stage_code(dict_inventory, lst_tasks),
                "riskLevelCode": str_risk_level_code,
                "riskCode": str_risk_code,
                "riskCodes": lst_risk_codes,
                "refCategory": util_safe_int(dict_source.get("refCategory")),
                "refNo": dict_source.get("refNo", ""),
                "relatedDocuments": dict_related_documents.get(str_key, []),
                "itemNo": dict_inventory.get("itemNo", ""),
                "itemName": dict_inventory.get("itemName", ""),
                "itemCategory": util_safe_int(dict_inventory.get("itemCategory")),
                "itemSubCategory": util_safe_int(dict_inventory.get("itemSubCategory")),
                "itemType": util_safe_int(dict_inventory.get("itemType")),
                "ownerDepartment": self.__owner_department(lst_tasks),
            }
            lst_rows.append(dict_row)
        return lst_rows

    def __build_dashboard_items(self, lst_rows):
        dict_items = {}
        for dict_row in lst_rows:
            str_item_no = dict_row.get("itemNo", "")
            if not str_item_no:
                continue
            dict_item = dict_items.setdefault(str_item_no, {
                "itemNo": str_item_no,
                "itemName": dict_row.get("itemName", ""),
                "itemCategory": util_safe_int(dict_row.get("itemCategory")),
                "itemSubCategory": util_safe_int(dict_row.get("itemSubCategory")),
                "itemType": util_safe_int(dict_row.get("itemType")),
                "unit": util_safe_int(dict_row.get("unit")),
                "totalBatchCount": 0,
                "warehouseCount": 0,
                "currentQuantity": 0.0,
                "availableQuantity": 0.0,
                "reservedQuantity": 0.0,
                "qualityHoldQuantity": 0.0,
                "earliestValidDate": 0,
                "qaHoldBatchCount": 0,
                "nearExpiryBatchCount": 0,
                "riskLevelCode": EBatchRiskLevelCode.NORMAL,
                "riskCode": EBatchRiskCode.NORMAL,
                "ownerDepartment": 0,
                "_batches": set(),
                "_warehouses": set(),
                "_qaHoldBatches": set(),
                "_nearExpiryBatches": set(),
                "_riskCodes": [],
            })
            str_batch_no = dict_row.get("batchNo", "")
            str_warehouse_no = dict_row.get("warehouseNo", "")
            if str_batch_no:
                dict_item["_batches"].add(str_batch_no)
            if str_warehouse_no:
                dict_item["_warehouses"].add(str_warehouse_no)
            if util_safe_float(dict_row.get("qualityHoldQuantity")) > 0 and str_batch_no:
                dict_item["_qaHoldBatches"].add(str_batch_no)
            if dict_row.get("riskCode") in [EBatchRiskCode.EXPIRED, EBatchRiskCode.NEAR_EXPIRY] and str_batch_no:
                dict_item["_nearExpiryBatches"].add(str_batch_no)
            dict_item["currentQuantity"] += util_safe_float(dict_row.get("currentQuantity"))
            dict_item["availableQuantity"] += util_safe_float(dict_row.get("availableQuantity"))
            dict_item["reservedQuantity"] += util_safe_float(dict_row.get("reservedQuantity"))
            dict_item["qualityHoldQuantity"] += util_safe_float(dict_row.get("qualityHoldQuantity"))
            n_valid_date = util_safe_int(dict_row.get("validDate"))
            if n_valid_date and (not dict_item["earliestValidDate"] or n_valid_date < dict_item["earliestValidDate"]):
                dict_item["earliestValidDate"] = n_valid_date
            dict_item["riskLevelCode"] = self.__max_risk_level_code(dict_item["riskLevelCode"], dict_row.get("riskLevelCode"))
            for str_risk_code in dict_row.get("riskCodes", []):
                if str_risk_code not in dict_item["_riskCodes"]:
                    dict_item["_riskCodes"].append(str_risk_code)
            if not dict_item["ownerDepartment"]:
                dict_item["ownerDepartment"] = util_safe_int(dict_row.get("ownerDepartment"))

        lst_results = []
        for dict_item in dict_items.values():
            dict_item["totalBatchCount"] = len(dict_item.pop("_batches"))
            dict_item["warehouseCount"] = len(dict_item.pop("_warehouses"))
            dict_item["qaHoldBatchCount"] = len(dict_item.pop("_qaHoldBatches"))
            dict_item["nearExpiryBatchCount"] = len(dict_item.pop("_nearExpiryBatches"))
            dict_item["currentQuantity"] = util_round_quantity(dict_item["currentQuantity"])
            dict_item["availableQuantity"] = util_round_quantity(dict_item["availableQuantity"])
            dict_item["reservedQuantity"] = util_round_quantity(dict_item["reservedQuantity"])
            dict_item["qualityHoldQuantity"] = util_round_quantity(dict_item["qualityHoldQuantity"])
            dict_item["riskCode"] = self.__primary_risk_code(dict_item.pop("_riskCodes"))
            lst_results.append(dict_item)
        return sorted(
            lst_results,
            key=lambda dict_item: (
                self.ITEM_CATEGORY_ORDER.get(util_safe_int(dict_item.get("itemCategory")), 99),
                self.__risk_sort(dict_item.get("riskLevelCode")),
                util_safe_int(dict_item.get("earliestValidDate")) if util_safe_int(dict_item.get("earliestValidDate")) else 9999999999,
                dict_item.get("itemNo", ""),
            ),
        )

    def __build_dashboard_summary(self, lst_items):
        return {
            "stockItemCount": len(lst_items),
            "highRiskItemCount": len([
                dict_item for dict_item in lst_items
                if dict_item.get("riskLevelCode") == EBatchRiskLevelCode.HIGH_RISK
            ]),
            "stockBatchCount": sum(util_safe_int(dict_item.get("totalBatchCount")) for dict_item in lst_items),
            "qualityHoldQuantity": util_round_quantity(sum(util_safe_float(dict_item.get("qualityHoldQuantity")) for dict_item in lst_items)),
            "nearExpiryBatchCount": sum(util_safe_int(dict_item.get("nearExpiryBatchCount")) for dict_item in lst_items),
        }

    def __distribution_row(self, dict_row):
        return {
            "batchNo": dict_row.get("batchNo", ""),
            "warehouseNo": dict_row.get("warehouseNo", ""),
            "warehouseName": dict_row.get("warehouseName", ""),
            "locationCode": dict_row.get("locationCode", ""),
            "palletCount": util_round_quantity(dict_row.get("palletCount")),
            "currentQuantity": util_round_quantity(dict_row.get("currentQuantity")),
            "availableQuantity": util_round_quantity(dict_row.get("availableQuantity")),
            "reservedQuantity": util_round_quantity(dict_row.get("reservedQuantity")),
            "qualityHoldQuantity": util_round_quantity(dict_row.get("qualityHoldQuantity")),
            "unit": util_safe_int(dict_row.get("unit")),
            "validDate": util_safe_int(dict_row.get("validDate")),
            "validDays": util_safe_int(dict_row.get("validDays")),
            "daysInStock": util_safe_int(dict_row.get("daysInStock")),
            "expiryStatusCode": dict_row.get("expiryStatusCode", EBatchExpiryStatusCode.UNKNOWN),
            "qaStatusCode": dict_row.get("qaStatusCode", EBatchQaStatusCode.UNKNOWN),
            "batchStageCode": dict_row.get("batchStageCode", EBatchStageCode.UNKNOWN),
            "riskLevelCode": dict_row.get("riskLevelCode", EBatchRiskLevelCode.NORMAL),
            "riskCodes": dict_row.get("riskCodes", []),
            "refCategory": util_safe_int(dict_row.get("refCategory")),
            "refNo": dict_row.get("refNo", ""),
            "relatedDocuments": dict_row.get("relatedDocuments", []),
        }

    def __stock_by_warehouse_row(self, dict_row):
        return {
            "warehouseNo": dict_row.get("warehouseNo", ""),
            "warehouseName": dict_row.get("warehouseName", ""),
            "locationCode": dict_row.get("locationCode", ""),
            "palletCount": util_round_quantity(dict_row.get("palletCount")),
            "currentQuantity": util_round_quantity(dict_row.get("currentQuantity")),
            "availableQuantity": util_round_quantity(dict_row.get("availableQuantity")),
            "reservedQuantity": util_round_quantity(dict_row.get("reservedQuantity")),
            "qualityHoldQuantity": util_round_quantity(dict_row.get("qualityHoldQuantity")),
            "unit": util_safe_int(dict_row.get("unit")),
            "riskLevelCode": dict_row.get("riskLevelCode", EBatchRiskLevelCode.NORMAL),
            "riskCodes": dict_row.get("riskCodes", []),
        }

    def __query_batch_header(self, obj_session, str_batch_no):
        return (
            obj_session.query(CTableBatchNumber)
            .filter(CTableBatchNumber.no == str_batch_no)
            .order_by(
                CTableBatchNumber.date.desc(),
                CTableBatchNumber.creationTime.desc(),
                CTableBatchNumber.id.desc(),
            )
            .first()
        )

    def __batch_header_to_dict(self, obj_batch):
        return {
            "batchNo": obj_batch.no or "",
            "itemNo": obj_batch.item_no or "",
            "itemName": obj_batch.item_name or "",
            "itemCategory": util_safe_int(obj_batch.itemCategory),
            "itemSubCategory": util_safe_int(obj_batch.itemSubCategory),
            "itemType": util_safe_int(obj_batch.itemType),
            "unit": util_safe_int(obj_batch.unit),
            "validDate": util_safe_int(obj_batch.validDate),
            "validDays": util_safe_int(obj_batch.validDays),
            "refCategory": util_safe_int(obj_batch.refCategory),
            "refNo": obj_batch.ref_no or "",
            "creatorNo": obj_batch.creator_no or "",
            "creationTime": util_safe_int(obj_batch.creationTime),
        }

    def __query_inventory_records(self, obj_session, str_batch_no):
        lst_rows = (
            obj_session.query(CTableInventoryRec)
            .filter(CTableInventoryRec.batchNumber == str_batch_no)
            .order_by(CTableInventoryRec.date.desc(), CTableInventoryRec.id.desc())
            .limit(self.MAX_DETAIL_RECORDS)
            .all()
        )
        return [
            {
                "recordTime": util_safe_int(obj_row.date),
                "refCategory": util_safe_int(obj_row.refCategory),
                "refNo": obj_row.ref_no or "",
                "warehouseNo": obj_row.warehouse_no or "",
                "category": util_safe_int(obj_row.category),
                "source": util_safe_int(obj_row.source),
                "quantity": util_round_quantity(obj_row.count),
                "unit": util_safe_int(obj_row.unit),
                "amount": util_round_amount(obj_row.amount),
            }
            for obj_row in lst_rows
        ]

    def __query_reservations(self, obj_session, str_batch_no):
        lst_rows = (
            obj_session.query(CTableWarehouseInventoryReservation)
            .filter(CTableWarehouseInventoryReservation.batchNumber == str_batch_no)
            .order_by(CTableWarehouseInventoryReservation.date.desc(), CTableWarehouseInventoryReservation.id.desc())
            .all()
        )
        return [
            {
                "reservationNo": obj_row.no or str(util_safe_int(obj_row.id)),
                "refCategory": util_safe_int(obj_row.refCategory),
                "refNo": obj_row.ref_no or "",
                "warehouseNo": obj_row.warehouse_no or "",
                "reservedQuantity": util_round_quantity(obj_row.reservedQuantity),
                "status": util_safe_int(obj_row.status),
                "expiryTimestamp": util_safe_int(obj_row.releaseTime),
            }
            for obj_row in lst_rows
        ]

    def __query_quality_holds(self, obj_session, str_batch_no):
        lst_rows = (
            obj_session.query(CTableWarehouseQualityHold)
            .filter(CTableWarehouseQualityHold.batchNumber == str_batch_no)
            .order_by(CTableWarehouseQualityHold.date.desc(), CTableWarehouseQualityHold.id.desc())
            .all()
        )
        return [
            {
                "holdNo": obj_row.no or str(util_safe_int(obj_row.id)),
                "warehouseNo": obj_row.warehouse_no or "",
                "holdQuantity": util_round_quantity(obj_row.holdQuantity),
                "status": util_safe_int(obj_row.status),
                "reasonCode": obj_row.reason or "",
                "createdTimestamp": util_safe_int(obj_row.creationTime),
            }
            for obj_row in lst_rows
        ]

    def __query_pallet_movements(self, obj_session, str_batch_no):
        lst_rows = (
            obj_session.query(CTableWarehousePalletMovement)
            .filter(CTableWarehousePalletMovement.batchNumber == str_batch_no)
            .order_by(CTableWarehousePalletMovement.date.desc(), CTableWarehousePalletMovement.id.desc())
            .limit(self.MAX_DETAIL_RECORDS)
            .all()
        )
        return [
            {
                "movementNo": obj_row.no or str(util_safe_int(obj_row.id)),
                "warehouseNo": obj_row.warehouse_no or "",
                "palletNo": obj_row.pallet_group_no or "",
                "palletCount": util_round_quantity(obj_row.palletCount),
                "palletStatus": util_safe_int(obj_row.palletStatus),
                "movementTimestamp": util_safe_int(obj_row.date),
            }
            for obj_row in lst_rows
        ]

    def __query_tasks(self, obj_session, str_batch_no):
        lst_rows = (
            obj_session.query(CTableWorkflowTaskState)
            .filter(CTableWorkflowTaskState.batchNumber == str_batch_no)
            .filter(CTableWorkflowTaskState.taskStatus.in_([
                EWorkflowTaskStatus.PENDING,
                EWorkflowTaskStatus.PARTIAL,
                EWorkflowTaskStatus.BLOCKED,
            ]))
            .order_by(CTableWorkflowTaskState.dueTimestamp.asc(), CTableWorkflowTaskState.id.asc())
            .all()
        )
        return [
            {
                "taskId": obj_row.taskId or str(util_safe_int(obj_row.id)),
                "taskType": util_safe_int(obj_row.taskType),
                "taskStatus": util_safe_int(obj_row.taskStatus),
                "nextOwnerDepartment": util_safe_int(obj_row.ownerDepartment),
                "dueTimestamp": util_safe_int(obj_row.dueTimestamp),
                "refCategory": util_safe_int(obj_row.refCategory),
                "refNo": obj_row.ref_no or "",
            }
            for obj_row in lst_rows
        ]

    def __query_related_documents(self, obj_session, lst_inventory_rows):
        set_stock_keys = {
            self.__stock_key(dict_row.get("itemNo"), dict_row.get("batchNo"), dict_row.get("warehouseNo"))
            for dict_row in lst_inventory_rows
            if dict_row.get("batchNo")
        }
        if not set_stock_keys:
            return {}
        dict_docs = defaultdict(list)
        self.__append_related_task_docs(obj_session, set_stock_keys, dict_docs)
        self.__append_related_reservation_docs(obj_session, set_stock_keys, dict_docs)
        self.__append_related_quality_docs(obj_session, set_stock_keys, dict_docs)
        self.__append_related_inventory_docs(obj_session, set_stock_keys, dict_docs)
        return dict_docs

    def __append_related_task_docs(self, obj_session, set_stock_keys, dict_docs):
        lst_batch_numbers = self.__stock_key_parts(set_stock_keys, 1)
        if not lst_batch_numbers:
            return
        lst_rows = obj_session.query(CTableWorkflowTaskState).filter(CTableWorkflowTaskState.batchNumber.in_(lst_batch_numbers)).all()
        for obj_row in lst_rows:
            str_key = self.__stock_key(obj_row.item_no, obj_row.batchNumber, obj_row.warehouse_no)
            self.__add_related_doc(dict_docs, str_key, obj_row.refCategory, obj_row.ref_no)

    def __append_related_reservation_docs(self, obj_session, set_stock_keys, dict_docs):
        lst_batch_numbers = self.__stock_key_parts(set_stock_keys, 1)
        if not lst_batch_numbers:
            return
        lst_rows = obj_session.query(CTableWarehouseInventoryReservation).filter(CTableWarehouseInventoryReservation.batchNumber.in_(lst_batch_numbers)).all()
        for obj_row in lst_rows:
            str_key = self.__stock_key(obj_row.item_no, obj_row.batchNumber, obj_row.warehouse_no)
            self.__add_related_doc(dict_docs, str_key, obj_row.refCategory, obj_row.ref_no)

    def __append_related_quality_docs(self, obj_session, set_stock_keys, dict_docs):
        lst_batch_numbers = self.__stock_key_parts(set_stock_keys, 1)
        if not lst_batch_numbers:
            return
        lst_rows = obj_session.query(CTableWarehouseQualityHold).filter(CTableWarehouseQualityHold.batchNumber.in_(lst_batch_numbers)).all()
        for obj_row in lst_rows:
            str_key = self.__stock_key(obj_row.item_no, obj_row.batchNumber, obj_row.warehouse_no)
            self.__add_related_doc(dict_docs, str_key, obj_row.refCategory, obj_row.ref_no)

    def __append_related_inventory_docs(self, obj_session, set_stock_keys, dict_docs):
        lst_batch_numbers = self.__stock_key_parts(set_stock_keys, 1)
        if not lst_batch_numbers:
            return
        lst_rows = obj_session.query(CTableInventoryRec).filter(CTableInventoryRec.batchNumber.in_(lst_batch_numbers)).all()
        for obj_row in lst_rows:
            str_key = self.__stock_key(obj_row.item_no, obj_row.batchNumber, obj_row.warehouse_no)
            self.__add_related_doc(dict_docs, str_key, obj_row.refCategory, obj_row.ref_no)

    def __add_related_doc(self, dict_docs, str_key, n_ref_category, str_ref_no):
        str_ref_no = str_ref_no or ""
        n_ref_category = util_safe_int(n_ref_category)
        if not str_ref_no and not n_ref_category:
            return
        dict_doc = {"refCategory": n_ref_category, "refNo": str_ref_no}
        if dict_doc not in dict_docs[str_key]:
            dict_docs[str_key].append(dict_doc)

    def __build_item_header(self, str_item_no, lst_rows):
        for dict_row in lst_rows:
            if dict_row.get("itemNo") == str_item_no:
                return {
                    "itemNo": str_item_no,
                    "itemName": dict_row.get("itemName", ""),
                    "itemCategory": util_safe_int(dict_row.get("itemCategory")),
                    "itemSubCategory": util_safe_int(dict_row.get("itemSubCategory")),
                    "itemType": util_safe_int(dict_row.get("itemType")),
                    "unit": util_safe_int(dict_row.get("unit")),
                }
        return {
            "itemNo": str_item_no,
            "itemName": "",
            "itemCategory": 0,
            "itemSubCategory": 0,
            "itemType": 0,
            "unit": 0,
        }

    def __filter_rows(
        self,
        lst_rows,
        str_keyword,
        n_item_category,
        n_item_sub_category,
        n_item_type,
        str_warehouse_no,
        str_batch_no,
        str_risk_level_code,
        str_qa_status_code,
        str_batch_stage_code,
        str_availability_code,
    ):
        lst_results = []
        str_keyword = (str_keyword or "").strip().lower()
        for dict_row in lst_rows:
            if n_item_category and util_safe_int(dict_row.get("itemCategory")) != n_item_category:
                continue
            if n_item_sub_category and util_safe_int(dict_row.get("itemSubCategory")) != n_item_sub_category:
                continue
            if n_item_type and util_safe_int(dict_row.get("itemType")) != n_item_type:
                continue
            if str_warehouse_no and dict_row.get("warehouseNo") != str_warehouse_no:
                continue
            if str_batch_no and dict_row.get("batchNo") != str_batch_no:
                continue
            if str_risk_level_code and dict_row.get("riskLevelCode") != str_risk_level_code:
                continue
            if str_qa_status_code and dict_row.get("qaStatusCode") != str_qa_status_code:
                continue
            if str_batch_stage_code and dict_row.get("batchStageCode") != str_batch_stage_code:
                continue
            if str_availability_code and not self.__matches_availability(dict_row, str_availability_code):
                continue
            if str_keyword and not self.__matches_keyword(dict_row, str_keyword):
                continue
            lst_results.append(dict_row)
        return lst_results

    def __matches_keyword(self, dict_row, str_keyword):
        lst_values = [
            dict_row.get("itemNo", ""),
            dict_row.get("itemName", ""),
            dict_row.get("batchNo", ""),
            dict_row.get("refNo", ""),
            dict_row.get("warehouseNo", ""),
        ]
        return any(str_keyword in (str_value or "").lower() for str_value in lst_values)

    def __matches_availability(self, dict_row, str_availability_code):
        if str_availability_code == EBatchStageCode.AVAILABLE:
            return util_safe_float(dict_row.get("availableQuantity")) > 0
        if str_availability_code == EBatchStageCode.RESERVED:
            return util_safe_float(dict_row.get("reservedQuantity")) > 0
        if str_availability_code == EBatchStageCode.QUALITY_HOLD:
            return util_safe_float(dict_row.get("qualityHoldQuantity")) > 0
        if str_availability_code == "empty":
            return util_safe_float(dict_row.get("currentQuantity")) <= 0
        return True

    def __risk_codes(self, dict_inventory, dict_risk, lst_tasks, n_query_timestamp):
        lst_codes = []
        n_valid_date = util_safe_int(dict_inventory.get("validDate"))
        n_valid_days = util_safe_int(dict_inventory.get("validDays"))
        if n_valid_date and n_valid_date < n_query_timestamp:
            lst_codes.append(EBatchRiskCode.EXPIRED)
        elif self.__is_near_expiry(dict_inventory, n_query_timestamp):
            lst_codes.append(EBatchRiskCode.NEAR_EXPIRY)
        for str_risk_type in dict_risk.get("riskTypes", []):
            if str_risk_type == EWarehouseRiskType.SHELF_LIFE_LT_ONE_THIRD and EBatchRiskCode.NEAR_EXPIRY not in lst_codes:
                lst_codes.append(EBatchRiskCode.NEAR_EXPIRY)
            elif str_risk_type == EWarehouseRiskType.BELOW_SAFETY_STOCK and EBatchRiskCode.STOCK_SHORTAGE not in lst_codes:
                lst_codes.append(EBatchRiskCode.STOCK_SHORTAGE)
        if util_safe_float(dict_inventory.get("qualityHoldQuantity")) > 0:
            lst_codes.append(EBatchRiskCode.QUALITY_HOLD)
        if util_safe_float(dict_inventory.get("reservedQuantity")) > 0:
            lst_codes.append(EBatchRiskCode.RESERVED)
        if any(util_safe_int(obj_task.taskStatus) == EWorkflowTaskStatus.BLOCKED for obj_task in lst_tasks):
            lst_codes.append(EBatchRiskCode.WORKFLOW_BLOCKED)
        return self.__unique_codes(lst_codes) or [EBatchRiskCode.NORMAL]

    def __is_near_expiry(self, dict_inventory, n_query_timestamp):
        n_item_category = util_safe_int(dict_inventory.get("itemCategory"))
        if n_item_category in [2, 3]:
            return False
        n_valid_date = util_safe_int(dict_inventory.get("validDate"))
        n_valid_days = util_safe_int(dict_inventory.get("validDays"))
        if not n_valid_date or not n_valid_days:
            return False
        n_remaining_seconds = n_valid_date - n_query_timestamp
        if n_remaining_seconds < 0:
            return False
        return (float(n_remaining_seconds) / float(n_valid_days * 86400)) <= (1.0 / 3.0)

    def __expiry_status_code(self, dict_inventory, n_query_timestamp):
        n_valid_date = util_safe_int(dict_inventory.get("validDate"))
        if not n_valid_date:
            return EBatchExpiryStatusCode.UNKNOWN
        if n_valid_date < n_query_timestamp:
            return EBatchExpiryStatusCode.EXPIRED
        if self.__is_near_expiry(dict_inventory, n_query_timestamp):
            return EBatchExpiryStatusCode.NEAR_EXPIRY
        return EBatchExpiryStatusCode.VALID

    def __days_in_stock(self, dict_inventory, n_query_timestamp):
        n_first_inbound_timestamp = util_safe_int(dict_inventory.get("firstInboundTimestamp"))
        if not n_first_inbound_timestamp or n_first_inbound_timestamp > n_query_timestamp:
            return 0
        return int((n_query_timestamp - n_first_inbound_timestamp) / 86400)

    def __risk_level_code(self, lst_risk_codes, dict_inventory):
        if EBatchRiskCode.EXPIRED in lst_risk_codes:
            return EBatchRiskLevelCode.HIGH_RISK
        if EBatchRiskCode.QUALITY_HOLD in lst_risk_codes and util_safe_float(dict_inventory.get("reservedQuantity")) > 0:
            return EBatchRiskLevelCode.HIGH_RISK
        if any(str_code in lst_risk_codes for str_code in [
            EBatchRiskCode.NEAR_EXPIRY,
            EBatchRiskCode.QUALITY_HOLD,
            EBatchRiskCode.RESERVED,
            EBatchRiskCode.STOCK_SHORTAGE,
            EBatchRiskCode.WORKFLOW_BLOCKED,
        ]):
            return EBatchRiskLevelCode.ATTENTION
        return EBatchRiskLevelCode.NORMAL

    def __primary_risk_code(self, lst_risk_codes):
        lst_priority = [
            EBatchRiskCode.EXPIRED,
            EBatchRiskCode.QUALITY_HOLD,
            EBatchRiskCode.STOCK_SHORTAGE,
            EBatchRiskCode.WORKFLOW_BLOCKED,
            EBatchRiskCode.NEAR_EXPIRY,
            EBatchRiskCode.RESERVED,
            EBatchRiskCode.NORMAL,
        ]
        for str_code in lst_priority:
            if str_code in lst_risk_codes:
                return str_code
        return EBatchRiskCode.UNKNOWN

    def __qa_status_code(self, dict_inventory, lst_tasks):
        if util_safe_float(dict_inventory.get("qualityHoldQuantity")) > 0:
            if any(util_safe_int(obj_task.taskStatus) == EWorkflowTaskStatus.BLOCKED for obj_task in lst_tasks):
                return EBatchQaStatusCode.BLOCKED
            return EBatchQaStatusCode.QUALITY_HOLD
        if lst_tasks:
            return EBatchQaStatusCode.INSPECTION
        return EBatchQaStatusCode.RELEASED

    def __batch_stage_code(self, dict_inventory, lst_tasks):
        f_quality = util_safe_float(dict_inventory.get("qualityHoldQuantity"))
        f_reserved = util_safe_float(dict_inventory.get("reservedQuantity"))
        f_available = util_safe_float(dict_inventory.get("availableQuantity"))
        f_current = util_safe_float(dict_inventory.get("currentQuantity"))
        if f_quality > 0:
            return EBatchStageCode.QUALITY_HOLD
        if f_reserved > 0 and f_available <= 0:
            return EBatchStageCode.RESERVED
        if f_available > 0:
            return EBatchStageCode.AVAILABLE
        if f_current > 0:
            return EBatchStageCode.STOCKED
        if lst_tasks:
            return EBatchStageCode.INBOUND_PENDING
        return EBatchStageCode.UNKNOWN

    def __owner_department(self, lst_tasks):
        if not lst_tasks:
            return 0
        lst_sorted = sorted(
            lst_tasks,
            key=lambda obj_task: (
                util_safe_int(obj_task.dueTimestamp) if util_safe_int(obj_task.dueTimestamp) else 9999999999,
                util_safe_int(obj_task.id),
            ),
        )
        return util_safe_int(lst_sorted[0].ownerDepartment)

    def __max_risk_level_code(self, str_left, str_right):
        return str_left if self.__risk_sort(str_left) <= self.__risk_sort(str_right) else str_right

    def __risk_sort(self, str_risk_level_code):
        return {
            EBatchRiskLevelCode.HIGH_RISK: 0,
            EBatchRiskLevelCode.ATTENTION: 1,
            EBatchRiskLevelCode.NORMAL: 2,
        }.get(str_risk_level_code, 3)

    def __unique_codes(self, lst_codes):
        lst_results = []
        for str_code in lst_codes:
            if str_code and str_code not in lst_results:
                lst_results.append(str_code)
        return lst_results

    def __normalize_page(self, n_start, n_count):
        n_start = max(util_safe_int(n_start), 0)
        n_count = util_safe_int(n_count) if n_count else 50
        n_count = min(max(n_count, 1), 100)
        return n_start, n_count

    def __stock_key(self, str_item_no, str_batch_no, str_warehouse_no):
        return "%s|%s|%s" % (str_item_no or "", str_batch_no or "", str_warehouse_no or "")

    def __stock_key_parts(self, set_stock_keys, n_index):
        return list({
            str_key.split("|", 2)[n_index]
            for str_key in set_stock_keys
            if len(str_key.split("|", 2)) > n_index and str_key.split("|", 2)[n_index]
        })


class CBatchCenterDashboard(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CBatchCenterService().get_dashboard(
                n_date=request.args.get("date", 0, type=int),
                str_timezone=str_timezone,
                str_keyword=request.args.get("keyword", "", type=str),
                n_item_category=request.args.get("itemCategory", 0, type=int),
                n_item_sub_category=request.args.get("itemSubCategory", 0, type=int),
                n_item_type=request.args.get("itemType", 0, type=int),
                str_warehouse_no=request.args.get("warehouseNo", "", type=str),
                str_batch_no=request.args.get("batchNo", "", type=str),
                str_risk_level_code=request.args.get("riskLevelCode", "", type=str),
                str_qa_status_code=request.args.get("qaStatusCode", "", type=str),
                str_batch_stage_code=request.args.get("batchStageCode", "", type=str),
                str_availability_code=request.args.get("availabilityCode", "", type=str),
                n_start=request.args.get("start", 0, type=int),
                n_count=request.args.get("count", 50, type=int),
            )
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CBatchCenterDashboard] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CBatchCenterDistribution(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CBatchCenterService().get_distribution(
                str_item_no=str_id,
                n_date=request.args.get("date", 0, type=int),
                str_timezone=str_timezone,
                str_keyword=request.args.get("keyword", "", type=str),
                n_item_category=request.args.get("itemCategory", 0, type=int),
                n_item_sub_category=request.args.get("itemSubCategory", 0, type=int),
                n_item_type=request.args.get("itemType", 0, type=int),
                str_warehouse_no=request.args.get("warehouseNo", "", type=str),
                str_batch_no=request.args.get("batchNo", "", type=str),
                str_risk_level_code=request.args.get("riskLevelCode", "", type=str),
                str_qa_status_code=request.args.get("qaStatusCode", "", type=str),
                str_batch_stage_code=request.args.get("batchStageCode", "", type=str),
                str_availability_code=request.args.get("availabilityCode", "", type=str),
                n_start=request.args.get("start", 0, type=int),
                n_count=request.args.get("count", 50, type=int),
            )
            if dict_extra_data is None:
                n_status_code = 400
                n_code = EErrorCode.ERROR_INVAILD_PARAM
                str_message = "invalid item_no"
                dict_extra_data = {}
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CBatchCenterDistribution] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CBatchCenterDetail(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CBatchCenterService().get_detail(
                str_batch_no=str_id,
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
            CLogger().log(CLogger.LOG_LEVELERROR, "[CBatchCenterDetail] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data
