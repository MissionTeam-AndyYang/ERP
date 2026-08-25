# coding=utf8
import time
from collections import defaultdict, deque

from flask import request
from sqlalchemy import case, func, or_

from package.common.common import (
    EErrorCode,
    EInventoryCategory,
    EItemCategory,
    ETraceDirectionCode,
    ETracePartnerTypeCode,
    ETraceRiskCode,
    ETraceRiskLevelCode,
    ETraceStepTypeCode,
    ETraceStatusCode,
)
from package.dbwrapper.dbmgr import CDBMgr
from package.dbwrapper.table import (
    CTableBatchNumber,
    CTableGoodsReceiptNote,
    CTableInventoryRec,
    CTableProductionData,
    CTableProductionDataInput,
    CTableProductionDataOutput,
    CTableWarehouseQualityHold,
    CTableWorkflowTaskEvent,
)
from package.log.log import CLogger
from package.restserver.api.v2.warehouse import CWarehouseInventoryContextBuilder
from package.util.util import (
    util_build_local_date_range,
    util_round_quantity,
    util_safe_float,
    util_safe_int,
)


class CTraceabilityService(object):
    MAX_TRACE_DEPTH = 5
    MAX_TRACE_BATCH_COUNT = 100
    MAX_TRACE_STEP_COUNT = 150

    def get_dashboard(
        self,
        str_timezone="",
        str_keyword="",
        n_item_category=0,
        str_item_no="",
        str_batch_no="",
        str_start_date="",
        str_end_date="",
        n_start=0,
        n_count=50,
    ):
        with CDBMgr() as obj_dbmgr:
            return self.__get_dashboard_with_session(
                obj_dbmgr.get_session(),
                str_timezone,
                str_keyword,
                n_item_category,
                str_item_no,
                str_batch_no,
                str_start_date,
                str_end_date,
                n_start,
                n_count,
            )

    def get_batch_overview(self, str_batch_no, str_timezone=""):
        with CDBMgr() as obj_dbmgr:
            return self.__get_batch_overview_with_session(
                obj_dbmgr.get_session(),
                str_batch_no,
                str_timezone,
            )

    def __get_dashboard_with_session(
        self,
        obj_session,
        str_timezone,
        str_keyword,
        n_item_category,
        str_item_no,
        str_batch_no,
        str_start_date,
        str_end_date,
        n_start,
        n_count,
    ):
        n_query_timestamp = util_safe_int(time.time())
        n_start, n_count = self.__normalize_page(n_start, n_count)
        dict_range = util_build_local_date_range(str_start_date, str_end_date, str_timezone) if str_start_date and str_end_date else None
        lst_all_batches = self.__query_batch_headers(
            obj_session,
            str_keyword,
            n_item_category,
            str_item_no,
            str_batch_no,
            dict_range,
        )
        n_total = len(lst_all_batches)
        lst_batches = lst_all_batches[n_start:n_start + n_count]
        lst_all_batch_nos = [obj_batch.no for obj_batch in lst_all_batches if obj_batch.no]
        lst_page_batch_nos = [obj_batch.no for obj_batch in lst_batches if obj_batch.no]
        dict_inventory = self.__build_inventory_by_batch(
            obj_session,
            n_query_timestamp,
            str_timezone,
            n_item_category,
            str_item_no,
            str_batch_no,
            lst_all_batch_nos,
        )
        dict_prod_inputs = self.__query_production_inputs_by_batch(obj_session, lst_all_batch_nos)
        dict_prod_outputs = self.__query_production_outputs_by_batch(obj_session, lst_all_batch_nos)
        dict_quality = self.__query_quality_holds_by_batch(obj_session, lst_all_batch_nos)
        dict_latest = self.__query_latest_event_timestamp_by_batch(obj_session, lst_all_batch_nos)

        lst_all_records = [
            self.__build_dashboard_record(
                obj_batch,
                dict_inventory,
                dict_prod_inputs,
                dict_prod_outputs,
                dict_quality,
                dict_latest,
                n_query_timestamp,
            )
            for obj_batch in lst_all_batches
        ]
        dict_records_by_batch = {dict_record.get("batchNo", ""): dict_record for dict_record in lst_all_records}
        lst_page = [
            dict_records_by_batch.get(str_batch_no)
            for str_batch_no in lst_page_batch_nos
            if dict_records_by_batch.get(str_batch_no)
        ]

        return {
            "serverTimestamp": n_query_timestamp,
            "summary": self.__build_summary(lst_all_records),
            "records": lst_page,
            "total": n_total,
            "start": n_start,
            "count": len(lst_page),
        }

    def __get_batch_overview_with_session(self, obj_session, str_batch_no, str_timezone):
        str_batch_no = (str_batch_no or "").strip()
        if not str_batch_no:
            return None
        n_query_timestamp = util_safe_int(time.time())
        obj_batch = self.__query_batch_header(obj_session, str_batch_no)
        if not obj_batch:
            return None
        dict_inventory = self.__build_inventory_by_batch(
            obj_session,
            n_query_timestamp,
            str_timezone,
            0,
            "",
            str_batch_no,
        ).get(str_batch_no, {})
        b_core_category = self.__is_trace_core_item_category(util_safe_int(obj_batch.itemCategory))
        lst_trace_steps = []
        if b_core_category:
            lst_trace_steps = self.__build_trace_steps(obj_session, obj_batch)
            dict_trace = self.__build_trace_state(
                obj_batch,
                dict_inventory,
                self.__query_production_inputs_by_batch(obj_session, [str_batch_no]).get(str_batch_no, []),
                self.__query_production_outputs_by_batch(obj_session, [str_batch_no]).get(str_batch_no, []),
                self.__query_quality_holds_by_batch(obj_session, [str_batch_no]).get(str_batch_no, []),
                n_query_timestamp,
            )
        else:
            dict_trace = {
                "traceStatusCode": ETraceStatusCode.UNKNOWN,
                "riskLevelCode": ETraceRiskLevelCode.NORMAL,
                "riskCode": ETraceRiskCode.UNKNOWN,
            }
        return {
            "serverTimestamp": n_query_timestamp,
            "batch": {
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
                "traceDirectionCode": self.__trace_direction_code(obj_batch),
                "traceStatusCode": dict_trace.get("traceStatusCode"),
                "riskLevelCode": dict_trace.get("riskLevelCode"),
                "riskCode": dict_trace.get("riskCode"),
            },
            "traceSteps": lst_trace_steps,
        }

    def __query_batch_headers(self, obj_session, str_keyword, n_item_category, str_item_no, str_batch_no, dict_range):
        obj_query = obj_session.query(CTableBatchNumber)
        if n_item_category:
            obj_query = obj_query.filter(CTableBatchNumber.itemCategory == n_item_category)
        if str_item_no:
            obj_query = obj_query.filter(CTableBatchNumber.item_no == str_item_no)
        if str_batch_no:
            obj_query = obj_query.filter(CTableBatchNumber.no == str_batch_no)
        if dict_range:
            obj_query = obj_query.filter(CTableBatchNumber.date >= dict_range.get("startTimestamp", 0))
            obj_query = obj_query.filter(CTableBatchNumber.date <= dict_range.get("endTimestamp", 0))
        str_keyword = (str_keyword or "").strip()
        if str_keyword:
            str_like = "%%%s%%" % str_keyword
            obj_query = obj_query.filter(or_(
                CTableBatchNumber.no.ilike(str_like),
                CTableBatchNumber.item_no.ilike(str_like),
                CTableBatchNumber.item_name.ilike(str_like),
                CTableBatchNumber.ref_no.ilike(str_like),
            ))
        lst_rows = obj_query.order_by(
            CTableBatchNumber.date.desc(),
            CTableBatchNumber.creationTime.desc(),
            CTableBatchNumber.id.desc(),
        ).all()
        dict_rows = {}
        for obj_row in lst_rows:
            if obj_row.no and obj_row.no not in dict_rows:
                dict_rows[obj_row.no] = obj_row
        return list(dict_rows.values())

    def __query_batch_header(self, obj_session, str_batch_no):
        return (
            obj_session.query(CTableBatchNumber)
            .filter(CTableBatchNumber.no == str_batch_no)
            .order_by(CTableBatchNumber.date.desc(), CTableBatchNumber.creationTime.desc(), CTableBatchNumber.id.desc())
            .first()
        )

    def __build_dashboard_record(
        self,
        obj_batch,
        dict_inventory,
        dict_prod_inputs,
        dict_prod_outputs,
        dict_quality,
        dict_latest,
        n_query_timestamp,
    ):
        str_no = obj_batch.no or ""
        dict_stock = dict_inventory.get(str_no, {})
        lst_inputs = dict_prod_inputs.get(str_no, [])
        lst_outputs = dict_prod_outputs.get(str_no, [])
        lst_holds = dict_quality.get(str_no, [])
        dict_trace = self.__build_trace_state(obj_batch, dict_stock, lst_inputs, lst_outputs, lst_holds, n_query_timestamp)
        return {
            "traceId": "TRACE-%s" % str_no,
            "traceDirectionCode": self.__trace_direction_code(obj_batch),
            "itemNo": obj_batch.item_no or dict_stock.get("itemNo", ""),
            "itemName": obj_batch.item_name or dict_stock.get("itemName", ""),
            "itemCategory": util_safe_int(obj_batch.itemCategory or dict_stock.get("itemCategory")),
            "itemSubCategory": util_safe_int(obj_batch.itemSubCategory or dict_stock.get("itemSubCategory")),
            "itemType": util_safe_int(obj_batch.itemType or dict_stock.get("itemType")),
            "batchNo": str_no,
            "refCategory": util_safe_int(obj_batch.refCategory),
            "refNo": obj_batch.ref_no or "",
            "partnerTypeCode": self.__partner_type_code(obj_batch),
            "partnerNo": "",
            "partnerName": "",
            "workOrderNo": self.__first_work_order_no(lst_inputs, lst_outputs),
            "warehouseNo": dict_stock.get("warehouseNo", ""),
            "warehouseName": dict_stock.get("warehouseName", ""),
            "currentQuantity": util_round_quantity(dict_stock.get("currentQuantity")),
            "unit": util_safe_int(obj_batch.unit or dict_stock.get("unit")),
            "traceStatusCode": dict_trace.get("traceStatusCode"),
            "riskLevelCode": dict_trace.get("riskLevelCode"),
            "riskCode": dict_trace.get("riskCode"),
            "latestEventTimestamp": max(
                util_safe_int(dict_latest.get(str_no)),
                util_safe_int(obj_batch.creationTime),
                util_safe_int(obj_batch.date),
                util_safe_int(dict_stock.get("latestInventoryTimestamp")),
            ),
        }

    def __build_inventory_by_batch(
        self,
        obj_session,
        n_query_timestamp,
        str_timezone,
        n_item_category,
        str_item_no,
        str_batch_no,
        lst_batch_nos=None,
    ):
        if lst_batch_nos is not None:
            return self.__query_inventory_summary_by_batch(
                obj_session,
                n_query_timestamp,
                n_item_category,
                str_item_no,
                str_batch_no,
                lst_batch_nos,
            )
        obj_builder = CWarehouseInventoryContextBuilder()
        dict_context = obj_builder.build(
            obj_session=obj_session,
            n_query_timestamp=n_query_timestamp,
            str_timezone=str_timezone,
            str_warehouse_no="",
            n_item_category=n_item_category,
            str_item_no=str_item_no,
            str_batch_no=str_batch_no,
            b_include_open_tasks=True,
        )
        dict_result = {}
        for dict_row in dict_context.get("inventoryRows", []):
            if util_safe_float(dict_row.get("currentQuantity")) <= 0:
                continue
            str_batch = dict_row.get("batchNo") or ""
            if not str_batch:
                continue
            dict_stock = dict_result.setdefault(str_batch, {
                "itemNo": dict_row.get("itemNo", ""),
                "itemName": dict_row.get("itemName", ""),
                "itemCategory": util_safe_int(dict_row.get("itemCategory")),
                "itemSubCategory": util_safe_int(dict_row.get("itemSubCategory")),
                "itemType": util_safe_int(dict_row.get("itemType")),
                "unit": util_safe_int(dict_row.get("unit")),
                "warehouseNo": dict_row.get("warehouseNo", ""),
                "warehouseName": dict_row.get("warehouseName", ""),
                "currentQuantity": 0.0,
                "qualityHoldQuantity": 0.0,
                "latestInventoryTimestamp": util_safe_int(dict_row.get("firstInboundTimestamp")),
                "_warehouses": [],
            })
            dict_stock["currentQuantity"] += util_safe_float(dict_row.get("currentQuantity"))
            dict_stock["qualityHoldQuantity"] += util_safe_float(dict_row.get("qualityHoldQuantity"))
            dict_stock["_warehouses"].append(dict_row)
        for dict_stock in dict_result.values():
            dict_stock["currentQuantity"] = util_round_quantity(dict_stock.get("currentQuantity"))
            dict_stock["qualityHoldQuantity"] = util_round_quantity(dict_stock.get("qualityHoldQuantity"))
        return dict_result

    def __query_inventory_summary_by_batch(
        self,
        obj_session,
        n_query_timestamp,
        n_item_category,
        str_item_no,
        str_batch_no,
        lst_batch_nos,
    ):
        lst_batch_nos = self.__clean_list(lst_batch_nos)
        if not lst_batch_nos:
            return {}
        lst_filters = [
            CTableInventoryRec.date <= n_query_timestamp,
            CTableInventoryRec.batchNumber.in_(lst_batch_nos),
        ]
        if n_item_category:
            lst_filters.append(CTableInventoryRec.itemCategory == n_item_category)
        if str_item_no:
            lst_filters.append(CTableInventoryRec.item_no == str_item_no)
        if str_batch_no:
            lst_filters.append(CTableInventoryRec.batchNumber == str_batch_no)
        obj_signed_count = func.sum(
            case(
                (CTableInventoryRec.category == EInventoryCategory.IN, CTableInventoryRec.count),
                (CTableInventoryRec.category == EInventoryCategory.OUT, -CTableInventoryRec.count),
                else_=0,
            )
        ).label("currentQuantity")
        obj_latest_inventory = func.max(CTableInventoryRec.date).label("latestInventoryTimestamp")
        lst_rows = (
            obj_session.query(
                CTableInventoryRec.batchNumber,
                CTableInventoryRec.item_no,
                CTableInventoryRec.item_name,
                CTableInventoryRec.itemCategory,
                CTableInventoryRec.itemType,
                CTableInventoryRec.warehouse_no,
                CTableInventoryRec.warehouse_displayName,
                CTableInventoryRec.unit,
                obj_signed_count,
                obj_latest_inventory,
            )
            .filter(*lst_filters)
            .group_by(
                CTableInventoryRec.batchNumber,
                CTableInventoryRec.item_no,
                CTableInventoryRec.item_name,
                CTableInventoryRec.itemCategory,
                CTableInventoryRec.itemType,
                CTableInventoryRec.warehouse_no,
                CTableInventoryRec.warehouse_displayName,
                CTableInventoryRec.unit,
            )
            .all()
        )
        dict_quality = self.__query_quality_quantity_by_batch(obj_session, lst_batch_nos)
        dict_result = {}
        for obj_row in lst_rows:
            if util_safe_float(obj_row.currentQuantity) <= 0:
                continue
            str_batch = obj_row.batchNumber or ""
            dict_stock = dict_result.setdefault(str_batch, {
                "itemNo": obj_row.item_no or "",
                "itemName": obj_row.item_name or "",
                "itemCategory": util_safe_int(obj_row.itemCategory),
                "itemSubCategory": 0,
                "itemType": util_safe_int(obj_row.itemType),
                "unit": util_safe_int(obj_row.unit),
                "warehouseNo": obj_row.warehouse_no or "",
                "warehouseName": obj_row.warehouse_displayName or "",
                "currentQuantity": 0.0,
                "qualityHoldQuantity": 0.0,
                "latestInventoryTimestamp": 0,
            })
            dict_stock["currentQuantity"] += util_safe_float(obj_row.currentQuantity)
            dict_stock["latestInventoryTimestamp"] = max(
                util_safe_int(dict_stock.get("latestInventoryTimestamp")),
                util_safe_int(obj_row.latestInventoryTimestamp),
            )
        dict_batch_metadata = self.__query_batch_metadata(obj_session, lst_batch_nos)
        for str_batch, dict_stock in dict_result.items():
            dict_metadata = dict_batch_metadata.get(str_batch, {})
            dict_stock["itemSubCategory"] = util_safe_int(dict_metadata.get("itemSubCategory"))
            dict_stock["itemType"] = util_safe_int(dict_metadata.get("itemType") or dict_stock.get("itemType"))
            dict_stock["currentQuantity"] = util_round_quantity(dict_stock.get("currentQuantity"))
            dict_stock["qualityHoldQuantity"] = util_round_quantity(dict_quality.get(str_batch))
        return dict_result

    def __query_batch_metadata(self, obj_session, lst_batch_nos):
        lst_batch_nos = self.__clean_list(lst_batch_nos)
        if not lst_batch_nos:
            return {}
        lst_rows = (
            obj_session.query(CTableBatchNumber)
            .filter(CTableBatchNumber.no.in_(lst_batch_nos))
            .order_by(CTableBatchNumber.date.desc(), CTableBatchNumber.creationTime.desc(), CTableBatchNumber.id.desc())
            .all()
        )
        dict_result = {}
        for obj_row in lst_rows:
            str_batch_no = obj_row.no or ""
            if str_batch_no and str_batch_no not in dict_result:
                dict_result[str_batch_no] = {
                    "itemSubCategory": util_safe_int(obj_row.itemSubCategory),
                    "itemType": util_safe_int(obj_row.itemType),
                }
        return dict_result

    def __query_quality_quantity_by_batch(self, obj_session, lst_batch_nos):
        lst_batch_nos = self.__clean_list(lst_batch_nos)
        if not lst_batch_nos:
            return {}
        lst_rows = (
            obj_session.query(
                CTableWarehouseQualityHold.batchNumber,
                func.sum(CTableWarehouseQualityHold.holdQuantity).label("holdQuantity"),
            )
            .filter(CTableWarehouseQualityHold.batchNumber.in_(lst_batch_nos))
            .group_by(CTableWarehouseQualityHold.batchNumber)
            .all()
        )
        return {obj_row.batchNumber or "": util_round_quantity(obj_row.holdQuantity) for obj_row in lst_rows}

    def __query_production_inputs_by_batch(self, obj_session, lst_batch_nos):
        return self.__group_by_batch(
            obj_session.query(CTableProductionDataInput)
            .filter(CTableProductionDataInput.batch_number.in_(self.__clean_list(lst_batch_nos)))
            .all(),
            "batch_number",
        ) if self.__clean_list(lst_batch_nos) else {}

    def __query_production_outputs_by_batch(self, obj_session, lst_batch_nos):
        return self.__group_by_batch(
            obj_session.query(CTableProductionDataOutput)
            .filter(CTableProductionDataOutput.batch_number.in_(self.__clean_list(lst_batch_nos)))
            .all(),
            "batch_number",
        ) if self.__clean_list(lst_batch_nos) else {}

    def __query_quality_holds_by_batch(self, obj_session, lst_batch_nos):
        return self.__group_by_batch(
            obj_session.query(CTableWarehouseQualityHold)
            .filter(CTableWarehouseQualityHold.batchNumber.in_(self.__clean_list(lst_batch_nos)))
            .all(),
            "batchNumber",
        ) if self.__clean_list(lst_batch_nos) else {}

    def __query_latest_event_timestamp_by_batch(self, obj_session, lst_batch_nos):
        lst_batch_nos = self.__clean_list(lst_batch_nos)
        if not lst_batch_nos:
            return {}
        dict_result = defaultdict(int)
        for obj_row in obj_session.query(CTableInventoryRec).filter(CTableInventoryRec.batchNumber.in_(lst_batch_nos)).all():
            dict_result[obj_row.batchNumber or ""] = max(dict_result[obj_row.batchNumber or ""], util_safe_int(obj_row.date))
        for obj_row in obj_session.query(CTableWorkflowTaskEvent).filter(CTableWorkflowTaskEvent.batchNumber.in_(lst_batch_nos)).all():
            dict_result[obj_row.batchNumber or ""] = max(dict_result[obj_row.batchNumber or ""], util_safe_int(obj_row.eventTimestamp))
        return dict_result

    def __build_trace_steps(self, obj_session, obj_root_batch):
        dict_context = {
            "batchHeaders": {obj_root_batch.no or "": obj_root_batch},
            "inputsByBatch": {},
            "outputsByBatch": {},
            "inputsByScope": {},
            "outputsByScope": {},
            "productionData": {},
        }
        dict_steps = {}
        obj_queue = deque([(obj_root_batch.no or "", 0)])
        set_visited = set()
        while obj_queue and len(set_visited) < self.MAX_TRACE_BATCH_COUNT and len(dict_steps) < self.MAX_TRACE_STEP_COUNT:
            str_batch_no, n_depth = obj_queue.popleft()
            if not str_batch_no or str_batch_no in set_visited or n_depth > self.MAX_TRACE_DEPTH:
                continue
            set_visited.add(str_batch_no)
            obj_batch = self.__query_batch_header_cached(obj_session, dict_context, str_batch_no)
            if not obj_batch or not self.__is_trace_core_item_category(util_safe_int(obj_batch.itemCategory)):
                continue
            self.__append_receipt_step(obj_session, obj_batch, dict_steps)
            for obj_input in self.__query_inputs_by_batch_no_cached(obj_session, dict_context, str_batch_no):
                self.__append_production_step_by_work_order(
                    obj_session,
                    dict_context,
                    obj_input.work_order_no,
                    obj_input.process_order_no,
                    obj_input.group,
                    dict_steps,
                    obj_queue,
                    n_depth,
                )
            for obj_output in self.__query_outputs_by_batch_no_cached(obj_session, dict_context, str_batch_no):
                self.__append_production_step_by_work_order(
                    obj_session,
                    dict_context,
                    obj_output.work_order_no,
                    obj_output.process_order_no,
                    obj_output.group,
                    dict_steps,
                    obj_queue,
                    n_depth,
                )
        return sorted(dict_steps.values(), key=lambda dict_row: (dict_row.get("eventTimestamp", 0), dict_row.get("stepId", "")))

    def __append_receipt_step(self, obj_session, obj_batch, dict_steps):
        if not obj_batch or not obj_batch.no or not obj_batch.ref_no:
            return
        obj_receipt = (
            obj_session.query(CTableGoodsReceiptNote)
            .filter(CTableGoodsReceiptNote.no == obj_batch.ref_no)
            .first()
        )
        if not obj_receipt and util_safe_int(obj_batch.refCategory) != 1:
            return
        n_timestamp = util_safe_int(getattr(obj_receipt, "date", 0) or obj_batch.date or obj_batch.creationTime)
        str_step_id = self.__trace_step_id(ETraceStepTypeCode.RECEIPT, obj_batch.ref_no, obj_batch.no)
        if str_step_id in dict_steps:
            return
        dict_steps[str_step_id] = {
            "stepId": str_step_id,
            "stepTypeCode": ETraceStepTypeCode.RECEIPT,
            "eventTimestamp": n_timestamp,
            "refCategory": util_safe_int(obj_batch.refCategory),
            "refNo": obj_batch.ref_no or "",
            "statusCode": ETraceStatusCode.COMPLETE,
            "riskLevelCode": ETraceRiskLevelCode.NORMAL,
            "inputItems": [],
            "outputItems": [
                {
                    "itemNo": getattr(obj_receipt, "item_no", "") or obj_batch.item_no or "",
                    "itemName": getattr(obj_receipt, "item_name", "") or obj_batch.item_name or "",
                    "itemCategory": util_safe_int(getattr(obj_receipt, "itemCategory", 0) or obj_batch.itemCategory),
                    "batchNo": obj_batch.no or "",
                    "quantity": util_round_quantity(getattr(obj_receipt, "checkedCount", 0) or obj_batch.checkedCount or obj_batch.expectedCount),
                    "unit": util_safe_int(getattr(obj_receipt, "unit", 0) or obj_batch.unit),
                }
            ],
        }

    def __append_production_step_by_work_order(
        self,
        obj_session,
        dict_context,
        str_work_order_no,
        str_process_order_no,
        str_group,
        dict_steps,
        obj_queue,
        n_depth,
    ):
        str_work_order_no = str_work_order_no or ""
        if not str_work_order_no:
            return
        str_step_id = self.__trace_production_step_id(str_work_order_no, str_process_order_no, str_group)
        if str_step_id in dict_steps:
            return
        lst_inputs = self.__query_inputs_by_work_scope(
            obj_session,
            dict_context,
            str_work_order_no,
            str_process_order_no,
            str_group,
        )
        lst_outputs = self.__query_outputs_by_work_scope(
            obj_session,
            dict_context,
            str_work_order_no,
            str_process_order_no,
            str_group,
        )
        lst_input_items = self.__aggregate_trace_step_items(lst_inputs)
        lst_output_items = self.__aggregate_trace_step_items(lst_outputs)
        if not lst_input_items and not lst_output_items:
            return
        obj_data = self.__query_production_data_cached(obj_session, dict_context, str_work_order_no)
        n_timestamp = self.__production_step_timestamp(obj_data, lst_inputs, lst_outputs)
        dict_steps[str_step_id] = {
            "stepId": str_step_id,
            "stepTypeCode": ETraceStepTypeCode.PRODUCTION,
            "eventTimestamp": n_timestamp,
            "refCategory": 0,
            "refNo": str_work_order_no,
            "statusCode": ETraceStatusCode.COMPLETE,
            "riskLevelCode": ETraceRiskLevelCode.NORMAL,
            "inputItems": lst_input_items,
            "outputItems": lst_output_items,
        }
        for obj_row in list(lst_inputs) + list(lst_outputs):
            str_batch_no = obj_row.batch_number or ""
            if str_batch_no and len(dict_steps) < self.MAX_TRACE_STEP_COUNT:
                obj_queue.append((str_batch_no, n_depth + 1))

    def __query_batch_header_cached(self, obj_session, dict_context, str_batch_no):
        str_batch_no = str_batch_no or ""
        if str_batch_no not in dict_context["batchHeaders"]:
            dict_context["batchHeaders"][str_batch_no] = self.__query_batch_header(obj_session, str_batch_no)
        return dict_context["batchHeaders"].get(str_batch_no)

    def __query_inputs_by_batch_no_cached(self, obj_session, dict_context, str_batch_no):
        str_batch_no = str_batch_no or ""
        if str_batch_no not in dict_context["inputsByBatch"]:
            dict_context["inputsByBatch"][str_batch_no] = self.__query_inputs_by_batch_no(obj_session, str_batch_no)
        return dict_context["inputsByBatch"].get(str_batch_no, [])

    def __query_outputs_by_batch_no_cached(self, obj_session, dict_context, str_batch_no):
        str_batch_no = str_batch_no or ""
        if str_batch_no not in dict_context["outputsByBatch"]:
            dict_context["outputsByBatch"][str_batch_no] = self.__query_outputs_by_batch_no(obj_session, str_batch_no)
        return dict_context["outputsByBatch"].get(str_batch_no, [])

    def __query_production_data_cached(self, obj_session, dict_context, str_work_order_no):
        str_work_order_no = str_work_order_no or ""
        if str_work_order_no not in dict_context["productionData"]:
            dict_context["productionData"][str_work_order_no] = (
                obj_session.query(CTableProductionData)
                .filter(CTableProductionData.work_order_no == str_work_order_no)
                .first()
            )
        return dict_context["productionData"].get(str_work_order_no)

    def __query_inputs_by_batch_no(self, obj_session, str_batch_no):
        return (
            obj_session.query(CTableProductionDataInput)
            .filter(CTableProductionDataInput.batch_number == str_batch_no)
            .all()
        )

    def __query_outputs_by_batch_no(self, obj_session, str_batch_no):
        return (
            obj_session.query(CTableProductionDataOutput)
            .filter(CTableProductionDataOutput.batch_number == str_batch_no)
            .all()
        )

    def __query_inputs_by_work_scope(self, obj_session, dict_context, str_work_order_no, str_process_order_no, str_group):
        tpl_scope = self.__work_scope_key(str_work_order_no, str_process_order_no, str_group)
        if tpl_scope not in dict_context["inputsByScope"]:
            obj_query = (
                obj_session.query(CTableProductionDataInput)
                .filter(CTableProductionDataInput.work_order_no == str_work_order_no)
            )
            if str_process_order_no:
                obj_query = obj_query.filter(CTableProductionDataInput.process_order_no == str_process_order_no)
            if str_group:
                obj_query = obj_query.filter(CTableProductionDataInput.group == str_group)
            dict_context["inputsByScope"][tpl_scope] = obj_query.order_by(
                CTableProductionDataInput.time.asc(),
                CTableProductionDataInput.id.asc(),
            ).all()
        return dict_context["inputsByScope"].get(tpl_scope, [])

    def __query_outputs_by_work_scope(self, obj_session, dict_context, str_work_order_no, str_process_order_no, str_group):
        tpl_scope = self.__work_scope_key(str_work_order_no, str_process_order_no, str_group)
        if tpl_scope not in dict_context["outputsByScope"]:
            obj_query = (
                obj_session.query(CTableProductionDataOutput)
                .filter(CTableProductionDataOutput.work_order_no == str_work_order_no)
            )
            if str_process_order_no:
                obj_query = obj_query.filter(CTableProductionDataOutput.process_order_no == str_process_order_no)
            if str_group:
                obj_query = obj_query.filter(CTableProductionDataOutput.group == str_group)
            dict_context["outputsByScope"][tpl_scope] = obj_query.order_by(
                CTableProductionDataOutput.time.asc(),
                CTableProductionDataOutput.id.asc(),
            ).all()
        return dict_context["outputsByScope"].get(tpl_scope, [])

    def __build_trace_step_item(self, obj_row):
        return {
            "itemNo": obj_row.item_no or "",
            "itemName": obj_row.item_name or "",
            "itemCategory": util_safe_int(obj_row.category),
            "batchNo": obj_row.batch_number or "",
            "quantity": util_round_quantity(obj_row.count),
            "unit": util_safe_int(obj_row.unit),
        }

    def __aggregate_trace_step_items(self, lst_rows):
        dict_items = {}
        for obj_row in lst_rows:
            if not self.__is_trace_core_item_category(util_safe_int(obj_row.category)):
                continue
            dict_item = self.__build_trace_step_item(obj_row)
            str_key = "%s|%s|%s|%s" % (
                dict_item.get("itemNo", ""),
                dict_item.get("batchNo", ""),
                util_safe_int(dict_item.get("itemCategory")),
                util_safe_int(dict_item.get("unit")),
            )
            dict_summary = dict_items.setdefault(str_key, {
                "itemNo": dict_item.get("itemNo", ""),
                "itemName": dict_item.get("itemName", ""),
                "itemCategory": util_safe_int(dict_item.get("itemCategory")),
                "batchNo": dict_item.get("batchNo", ""),
                "quantity": 0.0,
                "unit": util_safe_int(dict_item.get("unit")),
            })
            dict_summary["quantity"] += util_safe_float(dict_item.get("quantity"))
        return [
            {
                "itemNo": dict_row.get("itemNo", ""),
                "itemName": dict_row.get("itemName", ""),
                "itemCategory": util_safe_int(dict_row.get("itemCategory")),
                "batchNo": dict_row.get("batchNo", ""),
                "quantity": util_round_quantity(dict_row.get("quantity")),
                "unit": util_safe_int(dict_row.get("unit")),
            }
            for dict_row in sorted(dict_items.values(), key=lambda dict_row: (
                dict_row.get("itemNo", ""),
                dict_row.get("batchNo", ""),
                util_safe_int(dict_row.get("unit")),
            ))
        ]

    def __production_step_timestamp(self, obj_data, lst_inputs, lst_outputs):
        lst_timestamps = [util_safe_int(getattr(obj_data, "date", 0))]
        lst_timestamps.extend([util_safe_int(obj_row.time) for obj_row in list(lst_inputs) + list(lst_outputs)])
        lst_timestamps = [n_timestamp for n_timestamp in lst_timestamps if n_timestamp > 0]
        return min(lst_timestamps) if lst_timestamps else 0

    def __is_trace_core_item_category(self, n_item_category):
        return util_safe_int(n_item_category) in [
            EItemCategory.PM,
            EItemCategory.INPRODUCT,
            EItemCategory.PRODUCT,
        ]

    def __trace_step_id(self, str_step_type_code, str_ref_no, str_batch_no):
        return "%s:%s:%s" % (str_step_type_code or "", str_ref_no or "", str_batch_no or "")

    def __trace_production_step_id(self, str_work_order_no, str_process_order_no, str_group):
        return "%s:%s:%s:%s" % (
            ETraceStepTypeCode.PRODUCTION,
            str_work_order_no or "",
            str_process_order_no or "",
            str_group or "",
        )

    def __work_scope_key(self, str_work_order_no, str_process_order_no, str_group):
        return (str_work_order_no or "", str_process_order_no or "", str_group or "")

    def __build_trace_state(self, obj_batch, dict_stock, lst_inputs, lst_outputs, lst_holds, n_query_timestamp):
        b_has_connection = bool(obj_batch.ref_no or lst_inputs or lst_outputs or dict_stock.get("currentQuantity"))
        str_status = ETraceStatusCode.COMPLETE if b_has_connection else ETraceStatusCode.BROKEN
        str_risk_code = ETraceRiskCode.NORMAL
        str_risk_level = ETraceRiskLevelCode.NORMAL
        if str_status == ETraceStatusCode.BROKEN:
            str_risk_code = ETraceRiskCode.BROKEN_CHAIN
            str_risk_level = ETraceRiskLevelCode.HIGH_RISK
        elif util_safe_int(obj_batch.validDate) and util_safe_int(obj_batch.validDate) < n_query_timestamp and util_safe_float(dict_stock.get("currentQuantity")) > 0:
            str_risk_code = ETraceRiskCode.EXPIRED
            str_risk_level = ETraceRiskLevelCode.HIGH_RISK
        elif lst_holds or util_safe_float(dict_stock.get("qualityHoldQuantity")) > 0:
            str_risk_code = ETraceRiskCode.QUALITY_HOLD
            str_risk_level = ETraceRiskLevelCode.ATTENTION
        return {
            "traceStatusCode": str_status,
            "riskLevelCode": str_risk_level,
            "riskCode": str_risk_code,
        }

    def __batch_risk_level(self, obj_batch, dict_stock, lst_holds, n_query_timestamp):
        return self.__build_trace_state(obj_batch, dict_stock, [], [], lst_holds, n_query_timestamp).get("riskLevelCode")

    def __build_summary(self, lst_records):
        n_total = len(lst_records)
        n_complete = len([dict_row for dict_row in lst_records if dict_row.get("traceStatusCode") == ETraceStatusCode.COMPLETE])
        return {
            "traceableBatchCount": n_complete,
            "completeTraceRate": round((float(n_complete) / float(n_total)) * 100, 2) if n_total else 0.0,
            "brokenTraceCount": len([dict_row for dict_row in lst_records if dict_row.get("traceStatusCode") == ETraceStatusCode.BROKEN]),
            "highRiskTraceCount": len([dict_row for dict_row in lst_records if dict_row.get("riskLevelCode") == ETraceRiskLevelCode.HIGH_RISK]),
        }

    def __trace_direction_code(self, obj_batch):
        n_category = util_safe_int(obj_batch.itemCategory)
        if n_category in [EItemCategory.PM, EItemCategory.MA, EItemCategory.AF]:
            return ETraceDirectionCode.DOWNSTREAM
        if n_category == EItemCategory.PRODUCT:
            return ETraceDirectionCode.UPSTREAM
        return ETraceDirectionCode.BOTH

    def __partner_type_code(self, obj_batch):
        if not obj_batch or not obj_batch.ref_no:
            return ETracePartnerTypeCode.UNKNOWN
        if util_safe_int(obj_batch.refCategory) == 1:
            return ETracePartnerTypeCode.SUPPLIER
        if util_safe_int(obj_batch.refCategory) == 2:
            return ETracePartnerTypeCode.INTERNAL
        return ETracePartnerTypeCode.UNKNOWN

    def __first_work_order_no(self, lst_inputs, lst_outputs):
        for obj_row in list(lst_inputs) + list(lst_outputs):
            if obj_row.work_order_no:
                return obj_row.work_order_no
        return ""

    def __matches_keyword(self, dict_record, str_keyword):
        str_keyword = (str_keyword or "").strip().lower()
        if not str_keyword:
            return True
        return any(str_keyword in (str(dict_record.get(str_key, ""))).lower() for str_key in [
            "traceId", "itemNo", "itemName", "batchNo", "refNo", "workOrderNo", "warehouseNo", "warehouseName"
        ])

    def __group_by_batch(self, lst_rows, str_attr):
        dict_result = defaultdict(list)
        for obj_row in lst_rows:
            str_batch_no = getattr(obj_row, str_attr, "") or ""
            if str_batch_no:
                dict_result[str_batch_no].append(obj_row)
        return dict_result

    def __clean_list(self, lst_values):
        return list({str_value for str_value in lst_values if str_value})

    def __normalize_page(self, n_start, n_count):
        n_start = max(util_safe_int(n_start), 0)
        n_count = min(max(util_safe_int(n_count), 1), 100)
        return n_start, n_count

    def __risk_sort(self, str_risk_level_code):
        return {
            ETraceRiskLevelCode.HIGH_RISK: 0,
            ETraceRiskLevelCode.ATTENTION: 1,
            ETraceRiskLevelCode.NORMAL: 2,
        }.get(str_risk_level_code, 3)

    def __trace_status_sort(self, str_trace_status_code):
        return {
            ETraceStatusCode.BROKEN: 0,
            ETraceStatusCode.UNKNOWN: 1,
            ETraceStatusCode.COMPLETE: 2,
        }.get(str_trace_status_code, 3)

class CTraceabilityDashboard(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CTraceabilityService().get_dashboard(
                str_timezone=str_timezone,
                str_keyword=request.args.get("keyword", "", type=str),
                n_item_category=request.args.get("itemCategory", 0, type=int),
                str_item_no=request.args.get("itemNo", "", type=str),
                str_batch_no=request.args.get("batchNo", "", type=str),
                str_start_date=request.args.get("startDate", "", type=str),
                str_end_date=request.args.get("endDate", "", type=str),
                n_start=request.args.get("start", 0, type=int),
                n_count=request.args.get("count", 50, type=int),
            )
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CTraceabilityDashboard] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CTraceabilityBatchOverview(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CTraceabilityService().get_batch_overview(
                str_batch_no=str_id,
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
            CLogger().log(CLogger.LOG_LEVELERROR, "[CTraceabilityBatchOverview] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data
