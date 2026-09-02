# coding=utf8
import os
import time
from datetime import datetime, timezone

from flask import request
from sqlalchemy import create_engine, or_, text

from package.common.common import (
    EErrorCode,
    EInventoryCategory,
    EInventoryReadPermissionCode,
)
from package.dbwrapper.dbmgr import CDBMgr
from package.dbwrapper.maria import CMaria
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


class CInventoryStagingReadService(object):
    MAX_PAGE_COUNT = 100
    READY_STATE = "READY_FOR_READ_ONLY_API"

    def __init__(self, obj_engine=None):
        self.m_obj_engine = obj_engine

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
        with self.__connect() as obj_connection:
            return self._get_balances_with_connection(
                obj_connection=obj_connection,
                n_date=n_date,
                str_timezone=str_timezone,
                str_warehouse_no=str_warehouse_no,
                n_item_category=n_item_category,
                str_item_no=str_item_no,
                str_lot_code=str_lot_code,
                n_start=n_start,
                n_count=n_count,
            )

    def _get_balances_with_connection(
        self,
        obj_connection,
        n_date=0,
        str_timezone="",
        str_warehouse_no="",
        n_item_category=0,
        str_item_no="",
        str_lot_code="",
        n_start=0,
        n_count=50,
    ):
        n_query_timestamp = util_safe_int(n_date) or util_safe_int(time.time())
        n_start, n_count = self.__page(n_start, n_count)
        dict_params = {
            "readyState": self.READY_STATE,
            "warehouseNo": str_warehouse_no,
            "itemNo": str_item_no,
            "lotCode": str_lot_code,
        }
        str_where = self.__balance_where(str_warehouse_no, n_item_category, str_item_no, str_lot_code)
        n_total = self.__scalar(
            obj_connection,
            """
            SELECT COUNT(*)
            FROM np_stg_inventory_balance_snapshot bal
            JOIN np_xwalk_item_identity item ON item.xwalk_item_identity_id = bal.item_xwalk_id
            LEFT JOIN np_xwalk_lot_identity lot ON lot.xwalk_lot_identity_id = bal.lot_xwalk_id
            WHERE bal.validation_state = :readyState
              AND COALESCE(bal.display_quantity, bal.source_quantity, 0) > 0
            """ + str_where,
            dict_params,
        )
        lst_rows = self.__rows(
            obj_connection,
            """
            SELECT
              bal.stg_balance_snapshot_id AS balanceId,
              bal.warehouse_code AS warehouseNo,
              bal.location_code AS warehouseName,
              item.source_item_code AS itemNo,
              item.source_item_name AS itemName,
              lot.source_lot_code AS lotCode,
              COALESCE(bal.display_quantity, bal.source_quantity, 0) AS currentQuantity,
              bal.source_uom AS sourceUom,
              COALESCE(bal.display_uom, uom.display_uom, bal.source_uom) AS displayUom,
              bal.candidate_canonical_uom_code AS candidateCanonicalUomCode,
              bal.source_record_id AS sourceNo,
              bal.validation_state AS qualityStatus,
              bal.snapshot_business_date AS snapshotBusinessDate,
              bal.source_provenance_ref AS sourceProvenanceRef
            FROM np_stg_inventory_balance_snapshot bal
            JOIN np_xwalk_item_identity item ON item.xwalk_item_identity_id = bal.item_xwalk_id
            LEFT JOIN np_xwalk_lot_identity lot ON lot.xwalk_lot_identity_id = bal.lot_xwalk_id
            LEFT JOIN np_xwalk_uom uom ON uom.xwalk_uom_id = bal.uom_xwalk_id
            WHERE bal.validation_state = :readyState
              AND COALESCE(bal.display_quantity, bal.source_quantity, 0) > 0
            """ + str_where + """
            ORDER BY bal.snapshot_business_date DESC, bal.stg_balance_snapshot_id ASC
            LIMIT :count OFFSET :start
            """,
            dict(dict_params, count=n_count, start=n_start),
        )
        return {
            "serverTimestamp": n_query_timestamp,
            "timezone": str_timezone or "UTC",
            "total": n_total,
            "start": n_start,
            "count": len(lst_rows),
            "permissionCode": EInventoryReadPermissionCode.WH_INV_READ,
            "balances": [self.__balance_to_dict(dict_row) for dict_row in lst_rows],
        }

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
        with self.__connect() as obj_connection:
            return self._get_movements_with_connection(
                obj_connection=obj_connection,
                n_date=n_date,
                str_timezone=str_timezone,
                str_warehouse_no=str_warehouse_no,
                n_item_category=n_item_category,
                str_item_no=str_item_no,
                str_lot_code=str_lot_code,
                str_keyword=str_keyword,
                str_start_date=str_start_date,
                str_end_date=str_end_date,
                n_start=n_start,
                n_count=n_count,
            )

    def _get_movements_with_connection(
        self,
        obj_connection,
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
        n_query_timestamp = util_safe_int(n_date) or util_safe_int(time.time())
        n_start, n_count = self.__page(n_start, n_count)
        dict_range = util_build_local_date_range(str_start_date, str_end_date, str_timezone) if str_start_date and str_end_date else None
        dict_params = {
            "readyState": self.READY_STATE,
            "warehouseNo": str_warehouse_no,
            "itemNo": str_item_no,
            "lotCode": str_lot_code,
            "keyword": "%%%s%%" % (str_keyword or "").strip(),
            "queryDate": self.__date_text(n_query_timestamp),
        }
        str_where = self.__movement_where(str_warehouse_no, n_item_category, str_item_no, str_lot_code, str_keyword, dict_range)
        if dict_range:
            dict_params["startDate"] = dict_range.get("startDate", "")
            dict_params["endDate"] = dict_range.get("endDate", "")
        n_total = self.__scalar(
            obj_connection,
            """
            SELECT COUNT(*)
            FROM np_stg_inventory_movement mov
            JOIN np_xwalk_item_identity item ON item.xwalk_item_identity_id = mov.item_xwalk_id
            LEFT JOIN np_xwalk_lot_identity lot ON lot.xwalk_lot_identity_id = mov.lot_xwalk_id
            WHERE mov.validation_state = :readyState
            """ + str_where,
            dict_params,
        )
        lst_rows = self.__rows(
            obj_connection,
            """
            SELECT
              mov.stg_inventory_movement_id AS movementId,
              mov.package_id AS groupNo,
              mov.warehouse_code AS warehouseNo,
              COALESCE(mov.to_location_code, mov.from_location_code, mov.warehouse_code, '') AS warehouseName,
              item.source_item_code AS itemNo,
              item.source_item_name AS itemName,
              lot.source_lot_code AS lotCode,
              mov.source_event_timestamp AS movementTimestamp,
              mov.movement_business_date AS movementBusinessDate,
              mov.movement_type AS movementType,
              mov.source_document_ref AS refNo,
              COALESCE(mov.display_quantity, mov.source_quantity, 0) AS quantity,
              mov.source_uom AS sourceUom,
              COALESCE(mov.display_uom, uom.display_uom, mov.source_uom) AS displayUom,
              mov.candidate_canonical_uom_code AS candidateCanonicalUomCode,
              mov.source_provenance_ref AS sourceProvenanceRef,
              mov.technical_loaded_at AS creationTime
            FROM np_stg_inventory_movement mov
            JOIN np_xwalk_item_identity item ON item.xwalk_item_identity_id = mov.item_xwalk_id
            LEFT JOIN np_xwalk_lot_identity lot ON lot.xwalk_lot_identity_id = mov.lot_xwalk_id
            LEFT JOIN np_xwalk_uom uom ON uom.xwalk_uom_id = mov.uom_xwalk_id
            WHERE mov.validation_state = :readyState
            """ + str_where + """
            ORDER BY mov.movement_business_date DESC, mov.stg_inventory_movement_id DESC
            LIMIT :count OFFSET :start
            """,
            dict(dict_params, count=n_count, start=n_start),
        )
        return {
            "serverTimestamp": n_query_timestamp,
            "timezone": str_timezone or "UTC",
            "total": n_total,
            "start": n_start,
            "count": len(lst_rows),
            "permissionCode": EInventoryReadPermissionCode.WH_INV_READ,
            "range": CInventoryReadService()._range_payload(dict_range),
            "movements": [self.__movement_to_dict(dict_row) for dict_row in lst_rows],
        }

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
        with self.__connect() as obj_connection:
            return self._get_lots_with_connection(
                obj_connection=obj_connection,
                n_date=n_date,
                str_timezone=str_timezone,
                str_warehouse_no=str_warehouse_no,
                n_item_category=n_item_category,
                str_item_no=str_item_no,
                str_lot_code=str_lot_code,
                str_keyword=str_keyword,
                n_start=n_start,
                n_count=n_count,
            )

    def _get_lots_with_connection(
        self,
        obj_connection,
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
        n_query_timestamp = util_safe_int(n_date) or util_safe_int(time.time())
        n_start, n_count = self.__page(n_start, n_count)
        dict_params = {
            "readyState": self.READY_STATE,
            "warehouseNo": str_warehouse_no,
            "itemNo": str_item_no,
            "lotCode": str_lot_code,
            "keyword": "%%%s%%" % (str_keyword or "").strip(),
        }
        str_where = self.__lot_where(str_warehouse_no, n_item_category, str_item_no, str_lot_code, str_keyword)
        n_total = self.__scalar(
            obj_connection,
            """
            SELECT COUNT(*)
            FROM np_stg_lot_snapshot lotstg
            JOIN np_xwalk_item_identity item ON item.xwalk_item_identity_id = lotstg.item_xwalk_id
            JOIN np_xwalk_lot_identity lot ON lot.xwalk_lot_identity_id = lotstg.lot_xwalk_id
            WHERE lotstg.validation_state = :readyState
              AND COALESCE(lotstg.display_quantity, lotstg.source_quantity, 0) > 0
            """ + str_where,
            dict_params,
        )
        lst_rows = self.__rows(
            obj_connection,
            """
            SELECT
              lotstg.stg_lot_snapshot_id AS lotKey,
              lot.source_lot_code AS lotCode,
              lotstg.warehouse_code AS warehouseNo,
              lotstg.location_code AS warehouseName,
              item.source_item_code AS itemNo,
              item.source_item_name AS itemName,
              COALESCE(lotstg.display_quantity, lotstg.source_quantity, 0) AS currentQuantity,
              lotstg.source_uom AS sourceUom,
              COALESCE(lotstg.display_uom, uom.display_uom, lotstg.source_uom) AS displayUom,
              lotstg.candidate_canonical_uom_code AS candidateCanonicalUomCode,
              lotstg.source_lot_status AS qualityStatus,
              lotstg.snapshot_business_date AS snapshotBusinessDate,
              lotstg.source_provenance_ref AS sourceProvenanceRef
            FROM np_stg_lot_snapshot lotstg
            JOIN np_xwalk_item_identity item ON item.xwalk_item_identity_id = lotstg.item_xwalk_id
            JOIN np_xwalk_lot_identity lot ON lot.xwalk_lot_identity_id = lotstg.lot_xwalk_id
            LEFT JOIN np_xwalk_uom uom ON uom.xwalk_uom_id = lotstg.uom_xwalk_id
            WHERE lotstg.validation_state = :readyState
              AND COALESCE(lotstg.display_quantity, lotstg.source_quantity, 0) > 0
            """ + str_where + """
            ORDER BY lotstg.snapshot_business_date DESC, lotstg.stg_lot_snapshot_id ASC
            LIMIT :count OFFSET :start
            """,
            dict(dict_params, count=n_count, start=n_start),
        )
        return {
            "serverTimestamp": n_query_timestamp,
            "timezone": str_timezone or "UTC",
            "total": n_total,
            "start": n_start,
            "count": len(lst_rows),
            "permissionCode": EInventoryReadPermissionCode.WH_INV_READ,
            "summary": {},
            "lots": [self.__lot_to_dict(dict_row, n_query_timestamp) for dict_row in lst_rows],
        }

    def get_lot_trace(self, str_lot_code, str_timezone=""):
        with self.__connect() as obj_connection:
            return self._get_lot_trace_with_connection(obj_connection, str_lot_code, str_timezone)

    def _get_lot_trace_with_connection(self, obj_connection, str_lot_code, str_timezone=""):
        str_lot_code = (str_lot_code or "").strip()
        if not str_lot_code:
            return None
        dict_lot = self.__one(
            obj_connection,
            """
            SELECT
              lot.xwalk_lot_identity_id AS lotXwalkId,
              lot.source_lot_code AS lotCode,
              lot.candidate_lot_code AS candidateLotCode,
              lot.lot_identity_status AS lotIdentityStatus,
              item.source_item_code AS itemNo,
              item.source_item_name AS itemName,
              item.candidate_canonical_item_code AS candidateItemNo,
              lotstg.source_quantity AS currentQuantity,
              lotstg.source_uom AS sourceUom,
              COALESCE(lotstg.display_uom, uom.display_uom, lotstg.source_uom) AS displayUom,
              lotstg.source_lot_status AS lotStatus,
              lotstg.snapshot_business_date AS snapshotBusinessDate,
              lot.source_provenance_ref AS sourceProvenanceRef
            FROM np_xwalk_lot_identity lot
            JOIN np_xwalk_item_identity item ON item.xwalk_item_identity_id = lot.item_xwalk_id
            LEFT JOIN np_stg_lot_snapshot lotstg ON lotstg.lot_xwalk_id = lot.xwalk_lot_identity_id
            LEFT JOIN np_xwalk_uom uom ON uom.xwalk_uom_id = lotstg.uom_xwalk_id
            WHERE (lot.source_lot_code = :lotCode OR lot.candidate_lot_code = :lotCode)
            ORDER BY lotstg.snapshot_business_date DESC
            LIMIT 1
            """,
            {"lotCode": str_lot_code},
        )
        if not dict_lot:
            return None
        lst_movements = self.__rows(
            obj_connection,
            """
            SELECT
              mov.stg_inventory_movement_id AS stepId,
              mov.movement_type AS stepType,
              mov.source_document_ref AS refNo,
              mov.movement_business_date AS movementBusinessDate,
              mov.source_event_timestamp AS movementTimestamp,
              mov.warehouse_code AS warehouseNo,
              COALESCE(mov.to_location_code, mov.from_location_code, mov.warehouse_code, '') AS locationNo,
              COALESCE(mov.display_quantity, mov.source_quantity, 0) AS quantity,
              COALESCE(mov.display_uom, uom.display_uom, mov.source_uom) AS displayUom,
              mov.validation_state AS validationState,
              mov.source_provenance_ref AS sourceProvenanceRef
            FROM np_stg_inventory_movement mov
            LEFT JOIN np_xwalk_uom uom ON uom.xwalk_uom_id = mov.uom_xwalk_id
            WHERE mov.lot_xwalk_id = :lotXwalkId
              AND mov.validation_state = :readyState
            ORDER BY mov.movement_business_date ASC, mov.stg_inventory_movement_id ASC
            """,
            {"lotXwalkId": dict_lot.get("lotXwalkId"), "readyState": self.READY_STATE},
        )
        return {
            "serverTimestamp": util_safe_int(time.time()),
            "permissionCode": EInventoryReadPermissionCode.WH_INV_READ,
            "batch": {
                "batchNo": dict_lot.get("lotCode", ""),
                "candidateBatchNo": dict_lot.get("candidateLotCode", ""),
                "itemNo": dict_lot.get("itemNo", ""),
                "itemName": dict_lot.get("itemName", ""),
                "candidateItemNo": dict_lot.get("candidateItemNo", ""),
                "currentQuantity": util_round_quantity(dict_lot.get("currentQuantity")),
                "unit": dict_lot.get("displayUom", "") or dict_lot.get("sourceUom", ""),
                "status": dict_lot.get("lotStatus", "") or dict_lot.get("lotIdentityStatus", ""),
                "snapshotBusinessDate": self.__date_to_string(dict_lot.get("snapshotBusinessDate")),
                "sourceProvenanceRef": dict_lot.get("sourceProvenanceRef", ""),
            },
            "traceSteps": [self.__trace_step_to_dict(dict_row) for dict_row in lst_movements],
        }

    def __connect(self):
        if self.m_obj_engine is None:
            self.m_obj_engine = create_engine(CMaria().gen_connection_str(), pool_pre_ping=True, echo=False)
        return self.m_obj_engine.connect()

    def __page(self, n_start, n_count):
        n_start = max(util_safe_int(n_start), 0)
        n_count = util_safe_int(n_count) if n_count else 50
        return n_start, min(max(n_count, 1), self.MAX_PAGE_COUNT)

    def __balance_where(self, str_warehouse_no, n_item_category, str_item_no, str_lot_code):
        lst_where = []
        if util_safe_int(n_item_category):
            lst_where.append(" AND 1 = 0")
        if str_warehouse_no:
            lst_where.append(" AND bal.warehouse_code = :warehouseNo")
        if str_item_no:
            lst_where.append(" AND item.source_item_code = :itemNo")
        if str_lot_code:
            lst_where.append(" AND lot.source_lot_code = :lotCode")
        return "".join(lst_where)

    def __movement_where(self, str_warehouse_no, n_item_category, str_item_no, str_lot_code, str_keyword, dict_range):
        lst_where = []
        if util_safe_int(n_item_category):
            lst_where.append(" AND 1 = 0")
        if dict_range:
            lst_where.append(" AND mov.movement_business_date BETWEEN :startDate AND :endDate")
        else:
            lst_where.append(" AND (mov.movement_business_date IS NULL OR mov.movement_business_date <= :queryDate)")
        if str_warehouse_no:
            lst_where.append(" AND mov.warehouse_code = :warehouseNo")
        if str_item_no:
            lst_where.append(" AND item.source_item_code = :itemNo")
        if str_lot_code:
            lst_where.append(" AND lot.source_lot_code = :lotCode")
        if (str_keyword or "").strip():
            lst_where.append(
                " AND (mov.source_document_ref LIKE :keyword OR item.source_item_code LIKE :keyword "
                "OR item.source_item_name LIKE :keyword OR lot.source_lot_code LIKE :keyword "
                "OR mov.warehouse_code LIKE :keyword)"
            )
        return "".join(lst_where)

    def __lot_where(self, str_warehouse_no, n_item_category, str_item_no, str_lot_code, str_keyword):
        lst_where = []
        if util_safe_int(n_item_category):
            lst_where.append(" AND 1 = 0")
        if str_warehouse_no:
            lst_where.append(" AND lotstg.warehouse_code = :warehouseNo")
        if str_item_no:
            lst_where.append(" AND item.source_item_code = :itemNo")
        if str_lot_code:
            lst_where.append(" AND lot.source_lot_code = :lotCode")
        if (str_keyword or "").strip():
            lst_where.append(
                " AND (item.source_item_code LIKE :keyword OR item.source_item_name LIKE :keyword "
                "OR lot.source_lot_code LIKE :keyword OR lotstg.warehouse_code LIKE :keyword)"
            )
        return "".join(lst_where)

    def __balance_to_dict(self, dict_row):
        f_current_quantity = util_round_quantity(dict_row.get("currentQuantity"))
        return {
            "balanceId": dict_row.get("balanceId", ""),
            "warehouseNo": dict_row.get("warehouseNo", ""),
            "warehouseName": dict_row.get("warehouseName", ""),
            "itemNo": dict_row.get("itemNo", ""),
            "itemName": dict_row.get("itemName", ""),
            "itemCategory": 0,
            "itemSubCategory": 0,
            "lotCode": dict_row.get("lotCode", ""),
            "serialNo": "",
            "currentQuantity": f_current_quantity,
            "reservedQuantity": 0.0,
            "qualityHoldQuantity": 0.0,
            "availableQuantity": f_current_quantity,
            "unit": dict_row.get("displayUom", "") or dict_row.get("sourceUom", ""),
            "candidateCanonicalUomCode": dict_row.get("candidateCanonicalUomCode", ""),
            "unitCost": 0.0,
            "inventoryValue": 0,
            "availableValue": 0,
            "sourceRefCategory": 0,
            "sourceNo": dict_row.get("sourceNo", ""),
            "qualityStatus": dict_row.get("qualityStatus", ""),
            "riskTypes": [],
            "sourceProvenanceRef": dict_row.get("sourceProvenanceRef", ""),
        }

    def __movement_to_dict(self, dict_row):
        return {
            "movementId": dict_row.get("movementId", ""),
            "groupNo": dict_row.get("groupNo", ""),
            "warehouseNo": dict_row.get("warehouseNo", ""),
            "warehouseName": dict_row.get("warehouseName", ""),
            "itemNo": dict_row.get("itemNo", ""),
            "itemName": dict_row.get("itemName", ""),
            "itemCategory": 0,
            "lotCode": dict_row.get("lotCode", ""),
            "serialNo": "",
            "movementTimestamp": self.__timestamp(dict_row.get("movementTimestamp"), dict_row.get("movementBusinessDate")),
            "category": dict_row.get("movementType", ""),
            "source": "NP_STAGING",
            "quantity": util_round_quantity(dict_row.get("quantity")),
            "unit": dict_row.get("displayUom", "") or dict_row.get("sourceUom", ""),
            "candidateCanonicalUomCode": dict_row.get("candidateCanonicalUomCode", ""),
            "unitCost": 0.0,
            "amount": 0,
            "refCategory": "NP_STAGING_SOURCE_DOCUMENT",
            "refNo": dict_row.get("refNo", ""),
            "comment": "",
            "creationTime": self.__timestamp(dict_row.get("creationTime"), None),
            "sourceProvenanceRef": dict_row.get("sourceProvenanceRef", ""),
        }

    def __lot_to_dict(self, dict_row, n_query_timestamp):
        f_current_quantity = util_round_quantity(dict_row.get("currentQuantity"))
        return {
            "lotKey": dict_row.get("lotKey", ""),
            "lotCode": dict_row.get("lotCode", ""),
            "warehouseNo": dict_row.get("warehouseNo", ""),
            "warehouseName": dict_row.get("warehouseName", ""),
            "itemCategory": 0,
            "itemNo": dict_row.get("itemNo", ""),
            "itemName": dict_row.get("itemName", ""),
            "currentQuantity": f_current_quantity,
            "reservedQuantity": 0.0,
            "qualityHoldQuantity": 0.0,
            "availableQuantity": f_current_quantity,
            "unit": dict_row.get("displayUom", "") or dict_row.get("sourceUom", ""),
            "candidateCanonicalUomCode": dict_row.get("candidateCanonicalUomCode", ""),
            "unitCost": 0.0,
            "inventoryValue": 0,
            "palletCount": 0.0,
            "firstInboundTimestamp": 0,
            "daysInStock": self.__days_since(dict_row.get("snapshotBusinessDate"), n_query_timestamp),
            "validDate": 0,
            "validDays": 0,
            "safetyStock": 0.0,
            "riskTypes": [],
            "openTaskCount": 0,
            "refCategory": 0,
            "refNo": "",
            "qualityStatus": dict_row.get("qualityStatus", ""),
            "sourceProvenanceRef": dict_row.get("sourceProvenanceRef", ""),
        }

    def __trace_step_to_dict(self, dict_row):
        return {
            "stepId": dict_row.get("stepId", ""),
            "stepType": dict_row.get("stepType", ""),
            "refNo": dict_row.get("refNo", ""),
            "eventTimestamp": self.__timestamp(dict_row.get("movementTimestamp"), dict_row.get("movementBusinessDate")),
            "warehouseNo": dict_row.get("warehouseNo", ""),
            "locationNo": dict_row.get("locationNo", ""),
            "quantity": util_round_quantity(dict_row.get("quantity")),
            "unit": dict_row.get("displayUom", ""),
            "validationState": dict_row.get("validationState", ""),
            "sourceProvenanceRef": dict_row.get("sourceProvenanceRef", ""),
        }

    def __rows(self, obj_connection, str_sql, dict_params):
        obj_result = obj_connection.execute(text(str_sql), dict_params)
        return [dict(obj_row._mapping) for obj_row in obj_result.fetchall()]

    def __one(self, obj_connection, str_sql, dict_params):
        obj_result = obj_connection.execute(text(str_sql), dict_params).fetchone()
        return dict(obj_result._mapping) if obj_result else None

    def __scalar(self, obj_connection, str_sql, dict_params):
        obj_value = obj_connection.execute(text(str_sql), dict_params).scalar()
        return util_safe_int(obj_value)

    def __date_text(self, n_timestamp):
        try:
            return datetime.fromtimestamp(util_safe_int(n_timestamp), timezone.utc).strftime("%Y-%m-%d")
        except Exception:
            return ""

    def __date_to_string(self, obj_value):
        if obj_value is None:
            return ""
        if hasattr(obj_value, "strftime"):
            return obj_value.strftime("%Y-%m-%d")
        return str(obj_value)

    def __timestamp(self, obj_datetime_value, obj_date_value):
        if obj_datetime_value and hasattr(obj_datetime_value, "timestamp"):
            return util_safe_int(obj_datetime_value.replace(tzinfo=timezone.utc).timestamp())
        if obj_datetime_value:
            try:
                return util_safe_int(datetime.fromisoformat(str(obj_datetime_value)).replace(tzinfo=timezone.utc).timestamp())
            except Exception:
                pass
        if obj_date_value:
            try:
                return util_safe_int(datetime.fromisoformat(str(obj_date_value)).replace(tzinfo=timezone.utc).timestamp())
            except Exception:
                return 0
        return 0

    def __days_since(self, obj_date_value, n_query_timestamp):
        if not obj_date_value:
            return 0
        try:
            obj_snapshot = datetime.fromisoformat(str(obj_date_value)).replace(tzinfo=timezone.utc)
            obj_query = datetime.fromtimestamp(util_safe_int(n_query_timestamp), timezone.utc)
            return max((obj_query.date() - obj_snapshot.date()).days, 0)
        except Exception:
            return 0


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
        if self.__is_staging_mode():
            return CInventoryStagingReadService().get_balances(
                n_date=n_date,
                str_timezone=str_timezone,
                str_warehouse_no=str_warehouse_no,
                n_item_category=n_item_category,
                str_item_no=str_item_no,
                str_lot_code=str_lot_code,
                n_start=n_start,
                n_count=n_count,
            )
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
        if self.__is_staging_mode():
            return CInventoryStagingReadService().get_lots(
                n_date=n_date,
                str_timezone=str_timezone,
                str_warehouse_no=str_warehouse_no,
                n_item_category=n_item_category,
                str_item_no=str_item_no,
                str_lot_code=str_lot_code,
                str_keyword=str_keyword,
                n_start=n_start,
                n_count=n_count,
            )
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
        if self.__is_staging_mode():
            return CInventoryStagingReadService().get_movements(
                n_date=n_date,
                str_timezone=str_timezone,
                str_warehouse_no=str_warehouse_no,
                n_item_category=n_item_category,
                str_item_no=str_item_no,
                str_lot_code=str_lot_code,
                str_keyword=str_keyword,
                str_start_date=str_start_date,
                str_end_date=str_end_date,
                n_start=n_start,
                n_count=n_count,
            )
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
        if self.__is_staging_mode():
            return CInventoryStagingReadService().get_lot_trace(
                str_lot_code=str_lot_code,
                str_timezone=str_timezone,
            )
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

    def _range_payload(self, dict_range):
        return self.__range_payload(dict_range)

    def __is_staging_mode(self):
        return (os.getenv("ERP2_WH_INV_STAGING_MODE", "") or "").strip() == "1"

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
