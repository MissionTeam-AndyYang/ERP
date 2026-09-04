# coding=utf8
import time
from collections import defaultdict

from flask import request
from sqlalchemy import inspect, or_, text

from package.common.common import (
    EBomVersionState,
    EErrorCode,
    EItemCategory,
    ERoutingSourceCode,
    ERoutingStatusCode,
    ERoutingWarningCode,
)
from package.dbwrapper.dbmgr import CDBMgr
from package.dbwrapper.table import (
    CTableInproduct,
    CTableProcess,
    CTableProcessCapacity,
    CTableProcessFlow,
    CTableProduct,
    CTableProductBOMSpec,
    CTableProductProcess,
    CTableProductSpec,
)
from package.log.log import CLogger
from package.util.util import util_round_quantity, util_safe_float, util_safe_int


class CRoutingProcessFlowService(object):
    def get_dashboard(self, str_keyword="", str_routing_status_code="", n_effective_date=0, n_start=0, n_count=50):
        with CDBMgr() as obj_dbmgr:
            return self.__get_dashboard_with_session(
                obj_dbmgr.get_session(),
                str_keyword,
                str_routing_status_code,
                n_effective_date,
                n_start,
                n_count,
            )

    def get_versions(self, str_item_no, n_effective_date=0):
        with CDBMgr() as obj_dbmgr:
            return self.__get_versions_with_session(obj_dbmgr.get_session(), str_item_no, n_effective_date)

    def get_steps(self, str_routing_version_id, n_effective_date=0):
        with CDBMgr() as obj_dbmgr:
            return self.__get_steps_with_session(obj_dbmgr.get_session(), str_routing_version_id, n_effective_date)

    def get_current(self, str_item_no, n_effective_date=0):
        with CDBMgr() as obj_dbmgr:
            return self.__get_current_with_session(obj_dbmgr.get_session(), str_item_no, n_effective_date)

    def __get_dashboard_with_session(
        self,
        obj_session,
        str_keyword,
        str_routing_status_code,
        n_effective_date,
        n_start,
        n_count,
    ):
        if self.__use_test_support_surface(obj_session):
            return self.__get_test_support_dashboard_with_session(
                obj_session,
                str_keyword,
                str_routing_status_code,
                n_start,
                n_count,
            )
        n_query_timestamp = util_safe_int(n_effective_date) or util_safe_int(time.time())
        n_start = max(util_safe_int(n_start), 0)
        n_count = min(max(util_safe_int(n_count), 1), 100)
        lst_product_processes = self.__query_product_processes(obj_session, str_keyword)
        dict_state = self.__build_version_state_map(lst_product_processes, n_query_timestamp)
        dict_step_counts = self.__load_step_counts(obj_session, [obj_row.no for obj_row in lst_product_processes])
        dict_item_map = self.__load_item_map(obj_session)
        lst_rows = [
            self.__build_dashboard_row(
                obj_row,
                dict_state.get((obj_row.item_no, obj_row.version), EBomVersionState.UNKNOWN),
                dict_step_counts,
                dict_item_map,
            )
            for obj_row in lst_product_processes
        ]
        if str_routing_status_code:
            lst_rows = [dict_row for dict_row in lst_rows if dict_row.get("routingStatusCode") == str_routing_status_code]
        lst_rows = sorted(
            lst_rows,
            key=lambda dict_row: (
                dict_row.get("itemNo", ""),
                -util_safe_int(dict_row.get("routingVersion")),
                -util_safe_int(dict_row.get("dateTimestamp")),
            ),
        )
        n_total = len(lst_rows)
        lst_page = lst_rows[n_start:n_start + n_count]
        return {
            "serverTimestamp": util_safe_int(time.time()),
            "summary": self.__build_summary(lst_rows),
            "routingVersions": lst_page,
            "capabilityBoundary": self.__capability_boundary(),
            "total": n_total,
            "start": n_start,
            "count": len(lst_page),
        }

    def __get_versions_with_session(self, obj_session, str_item_no, n_effective_date):
        str_item_no = (str_item_no or "").strip()
        if not str_item_no:
            return None
        if self.__use_test_support_surface(obj_session):
            return self.__get_test_support_versions_with_session(obj_session, str_item_no)
        n_query_timestamp = util_safe_int(n_effective_date) or util_safe_int(time.time())
        lst_versions = obj_session.query(CTableProductProcess).filter(CTableProductProcess.item_no == str_item_no).all()
        if not lst_versions:
            return None
        dict_state = self.__build_version_state_map(lst_versions, n_query_timestamp)
        dict_step_counts = self.__load_step_counts(obj_session, [obj_row.no for obj_row in lst_versions])
        dict_item_map = self.__load_item_map(obj_session, [str_item_no])
        return {
            "serverTimestamp": util_safe_int(time.time()),
            "item": self.__build_item_header(str_item_no, dict_item_map),
            "versions": [
                self.__build_version_row(
                    obj_row,
                    dict_state.get((obj_row.item_no, obj_row.version), EBomVersionState.UNKNOWN),
                    dict_step_counts,
                    dict_item_map,
                )
                for obj_row in sorted(lst_versions, key=lambda obj_row: -util_safe_int(obj_row.version))
            ],
            "capabilityBoundary": self.__capability_boundary(),
        }

    def __get_steps_with_session(self, obj_session, str_routing_version_id, n_effective_date):
        str_routing_version_id = (str_routing_version_id or "").strip()
        if not str_routing_version_id:
            return None
        if self.__use_test_support_surface(obj_session):
            return self.__get_test_support_steps_with_session(obj_session, str_routing_version_id)
        obj_product_process = (
            obj_session.query(CTableProductProcess)
            .filter(CTableProductProcess.no == str_routing_version_id)
            .first()
        )
        if not obj_product_process:
            return None
        n_query_timestamp = util_safe_int(n_effective_date) or util_safe_int(time.time())
        lst_versions = obj_session.query(CTableProductProcess).filter(CTableProductProcess.item_no == obj_product_process.item_no).all()
        dict_state = self.__build_version_state_map(lst_versions, n_query_timestamp)
        dict_item_map = self.__load_item_map(obj_session, [obj_product_process.item_no])
        dict_process_map = self.__load_process_map(obj_session)
        dict_capacity_map = self.__load_capacity_map(obj_session, n_query_timestamp)
        lst_steps = self.__build_steps(obj_session, obj_product_process, dict_process_map, dict_capacity_map)
        lst_warnings = self.__build_warnings(obj_product_process, lst_steps, dict_item_map)
        return {
            "serverTimestamp": util_safe_int(time.time()),
            "routingVersion": self.__build_routing_header(
                obj_product_process,
                dict_state.get((obj_product_process.item_no, obj_product_process.version), EBomVersionState.UNKNOWN),
                dict_item_map,
                lst_steps,
                lst_warnings,
            ),
            "steps": lst_steps,
            "sourceLineage": self.__source_lineage(obj_product_process),
            "capabilityBoundary": self.__capability_boundary(),
            "warnings": lst_warnings,
        }

    def __get_current_with_session(self, obj_session, str_item_no, n_effective_date):
        str_item_no = (str_item_no or "").strip()
        if not str_item_no:
            return None
        if self.__use_test_support_surface(obj_session):
            dict_versions = self.__get_test_support_versions_with_session(obj_session, str_item_no)
            if not dict_versions or not dict_versions.get("versions"):
                return None
            return self.__get_test_support_steps_with_session(
                obj_session,
                dict_versions["versions"][0].get("routingVersionId", ""),
            )
        n_query_timestamp = util_safe_int(n_effective_date) or util_safe_int(time.time())
        lst_versions = obj_session.query(CTableProductProcess).filter(CTableProductProcess.item_no == str_item_no).all()
        if not lst_versions:
            return None
        dict_state = self.__build_version_state_map(lst_versions, n_query_timestamp)
        obj_selected = self.__select_current_version(lst_versions, dict_state)
        if not obj_selected:
            return None
        return self.__get_steps_with_session(obj_session, obj_selected.no, n_effective_date)

    def __query_product_processes(self, obj_session, str_keyword):
        obj_query = obj_session.query(CTableProductProcess)
        str_keyword = (str_keyword or "").strip()
        if str_keyword:
            str_like = "%%%s%%" % str_keyword
            lst_product_nos = [
                obj_row.no for obj_row in obj_session.query(CTableProduct.no).filter(or_(
                    CTableProduct.no.ilike(str_like),
                    CTableProduct.name.ilike(str_like),
                )).all()
            ]
            lst_inproduct_nos = [
                obj_row.no for obj_row in obj_session.query(CTableInproduct.no).filter(or_(
                    CTableInproduct.no.ilike(str_like),
                    CTableInproduct.name.ilike(str_like),
                )).all()
            ]
            lst_item_nos = list(set(lst_product_nos + lst_inproduct_nos))
            obj_query = obj_query.filter(or_(
                CTableProductProcess.no.ilike(str_like),
                CTableProductProcess.item_no.ilike(str_like),
                CTableProductProcess.item_no.in_(lst_item_nos) if lst_item_nos else False,
            ))
        return obj_query.all()

    def __build_version_state_map(self, lst_versions, n_query_timestamp):
        dict_effective_version_by_item = {}
        for obj_row in lst_versions:
            n_date = util_safe_int(obj_row.date)
            if n_date > 0 and n_date <= n_query_timestamp:
                str_item_no = obj_row.item_no or ""
                n_version = util_safe_int(obj_row.version)
                if n_version > dict_effective_version_by_item.get(str_item_no, 0):
                    dict_effective_version_by_item[str_item_no] = n_version
        dict_state = {}
        for obj_row in lst_versions:
            str_item_no = obj_row.item_no or ""
            n_version = util_safe_int(obj_row.version)
            n_date = util_safe_int(obj_row.date)
            if n_date <= 0:
                str_state = EBomVersionState.UNKNOWN
            elif n_date > n_query_timestamp:
                str_state = EBomVersionState.FUTURE
            elif n_version == dict_effective_version_by_item.get(str_item_no, 0):
                str_state = EBomVersionState.EFFECTIVE
            else:
                str_state = EBomVersionState.HISTORICAL
            dict_state[(str_item_no, n_version)] = str_state
        return dict_state

    def __load_step_counts(self, obj_session, lst_routing_nos):
        lst_routing_nos = list({str_no for str_no in lst_routing_nos or [] if str_no})
        if not lst_routing_nos:
            return {}
        dict_counts = defaultdict(int)
        for obj_row in obj_session.query(CTableProcessFlow).filter(CTableProcessFlow.product_process_no.in_(lst_routing_nos)).all():
            dict_counts[obj_row.product_process_no or ""] += 1
        return dict_counts

    def __load_item_map(self, obj_session, lst_item_nos=None):
        dict_items = {}
        obj_product_query = obj_session.query(CTableProduct)
        obj_inproduct_query = obj_session.query(CTableInproduct)
        if lst_item_nos:
            lst_item_nos = list({str_no for str_no in lst_item_nos if str_no})
            obj_product_query = obj_product_query.filter(CTableProduct.no.in_(lst_item_nos))
            obj_inproduct_query = obj_inproduct_query.filter(CTableInproduct.no.in_(lst_item_nos))
        for obj_row in obj_inproduct_query.all():
            dict_items[obj_row.no] = {
                "itemNo": obj_row.no or "",
                "itemName": obj_row.name or "",
                "itemCategory": EItemCategory.INPRODUCT,
                "itemSubCategory": util_safe_int(obj_row.category),
                "unitProduct": util_safe_int(obj_row.unitProduct),
                "sourceCode": ERoutingSourceCode.INPRODUCT,
            }
        for obj_row in obj_product_query.all():
            dict_items[obj_row.no] = {
                "itemNo": obj_row.no or "",
                "itemName": obj_row.name or "",
                "itemCategory": EItemCategory.PRODUCT,
                "itemSubCategory": util_safe_int(obj_row.category),
                "unitProduct": util_safe_int(obj_row.unitProduct),
                "sourceCode": ERoutingSourceCode.PRODUCT,
            }
        return dict_items

    def __load_process_map(self, obj_session):
        return {
            (util_safe_int(obj_row.oneProcess), util_safe_int(obj_row.secProcess)): obj_row
            for obj_row in obj_session.query(CTableProcess).all()
        }

    def __load_capacity_map(self, obj_session, n_query_timestamp):
        dict_capacity = {}
        lst_rows = (
            obj_session.query(CTableProcessCapacity)
            .filter(CTableProcessCapacity.date <= n_query_timestamp)
            .order_by(CTableProcessCapacity.oneProcess.asc(), CTableProcessCapacity.secProcess.asc(), CTableProcessCapacity.date.desc())
            .all()
        )
        for obj_row in lst_rows:
            tuple_key = (util_safe_int(obj_row.oneProcess), util_safe_int(obj_row.secProcess))
            if tuple_key not in dict_capacity:
                dict_capacity[tuple_key] = obj_row
        return dict_capacity

    def __use_test_support_surface(self, obj_session):
        return (
            not self.__db_object_exists(obj_session, "product_process")
            and self.__db_object_exists(obj_session, "v_test_support_routing_process_flow_readonly")
        )

    def __db_object_exists(self, obj_session, str_object_name):
        str_object_name = (str_object_name or "").strip()
        if not str_object_name:
            return False
        try:
            obj_bind = obj_session.get_bind()
            if obj_bind and obj_bind.dialect.name != "mariadb":
                return inspect(obj_bind).has_table(str_object_name)
            obj_row = obj_session.execute(
                text(
                    "SELECT COUNT(*) FROM information_schema.tables "
                    "WHERE table_schema = DATABASE() AND table_name = :str_object_name"
                ),
                {"str_object_name": str_object_name},
            ).first()
            return util_safe_int(obj_row[0] if obj_row else 0) > 0
        except Exception:
            return False

    def __query_test_support_rows(self, obj_session, str_item_no="", str_route_id=""):
        str_sql = (
            "SELECT test_support_route_id, product_no, product_name, product_version, bom_no, "
            "bom_display_name, bom_version, process_flow_label, test_support_step_id, step_sequence, "
            "step_label, input_ref, output_ref, nonproduction_classification, evidence_boundary, "
            "source_lineage_ref, warning_behavior, acceptance_use "
            "FROM v_test_support_routing_process_flow_readonly "
        )
        dict_params = {}
        lst_where = []
        if str_item_no:
            lst_where.append("product_no = :str_item_no")
            dict_params["str_item_no"] = str_item_no
        if str_route_id:
            lst_where.append("test_support_route_id = :str_route_id")
            dict_params["str_route_id"] = str_route_id
        if lst_where:
            str_sql += "WHERE " + " AND ".join(lst_where) + " "
        str_sql += "ORDER BY product_no ASC, product_version DESC, step_sequence ASC"
        return [
            dict(obj_row._mapping)
            for obj_row in obj_session.execute(text(str_sql), dict_params).all()
        ]

    def __query_test_support_warning_map(self, obj_session):
        if not self.__db_object_exists(obj_session, "v_test_support_routing_source_lineage_warnings"):
            return {}
        dict_warnings = {}
        for obj_row in obj_session.execute(text(
            "SELECT test_support_route_id, source_lineage_ref, warning_behavior, boundary_label "
            "FROM v_test_support_routing_source_lineage_warnings"
        )).all():
            dict_row = dict(obj_row._mapping)
            dict_warnings[dict_row.get("test_support_route_id", "")] = dict_row
        return dict_warnings

    def __get_test_support_dashboard_with_session(
        self,
        obj_session,
        str_keyword,
        str_routing_status_code,
        n_start,
        n_count,
    ):
        n_start = max(util_safe_int(n_start), 0)
        n_count = min(max(util_safe_int(n_count), 1), 100)
        lst_rows = self.__build_test_support_dashboard_rows(
            self.__query_test_support_rows(obj_session),
            str_keyword,
        )
        if str_routing_status_code:
            lst_rows = [dict_row for dict_row in lst_rows if dict_row.get("routingStatusCode") == str_routing_status_code]
        n_total = len(lst_rows)
        lst_page = lst_rows[n_start:n_start + n_count]
        return {
            "serverTimestamp": util_safe_int(time.time()),
            "summary": self.__build_summary(lst_rows),
            "routingVersions": lst_page,
            "capabilityBoundary": self.__capability_boundary(),
            "total": n_total,
            "start": n_start,
            "count": len(lst_page),
        }

    def __get_test_support_versions_with_session(self, obj_session, str_item_no):
        lst_rows = self.__build_test_support_dashboard_rows(
            self.__query_test_support_rows(obj_session, str_item_no),
            "",
        )
        if not lst_rows:
            return None
        return {
            "serverTimestamp": util_safe_int(time.time()),
            "item": {
                "itemNo": str_item_no,
                "itemName": lst_rows[0].get("itemName", ""),
                "itemCategory": lst_rows[0].get("itemCategory", 0),
                "itemSubCategory": lst_rows[0].get("itemSubCategory", 0),
                "sourceCode": ERoutingSourceCode.PRODUCT,
            },
            "versions": lst_rows,
            "capabilityBoundary": self.__capability_boundary(),
        }

    def __get_test_support_steps_with_session(self, obj_session, str_routing_version_id):
        lst_rows = self.__query_test_support_rows(obj_session, str_route_id=str_routing_version_id)
        if not lst_rows:
            return None
        dict_warning_map = self.__query_test_support_warning_map(obj_session)
        lst_steps = [self.__build_test_support_step_row(dict_row) for dict_row in lst_rows]
        lst_warnings = self.__build_test_support_warnings(str_routing_version_id, lst_steps, dict_warning_map)
        dict_routing_row = self.__build_test_support_dashboard_rows(lst_rows, "")[0]
        dict_routing_row["routingStatusCode"] = self.__routing_status_code(
            len(lst_steps),
            [dict_warning.get("warningCode", "") for dict_warning in lst_warnings],
        )
        return {
            "serverTimestamp": util_safe_int(time.time()),
            "routingVersion": dict_routing_row,
            "steps": lst_steps,
            "sourceLineage": {
                "routingVersionSourceCode": ERoutingSourceCode.TEST_SUPPORT,
                "stepSourceCode": ERoutingSourceCode.TEST_SUPPORT,
                "processIdentitySourceCode": ERoutingSourceCode.NOT_RECORDED,
                "recipeReferenceSourceCode": ERoutingSourceCode.PRODUCT_SPEC,
                "packagingContextSourceCode": ERoutingSourceCode.PRODUCT_BOM_SPEC,
                "resourceEligibilitySourceCode": ERoutingSourceCode.NOT_RECORDED,
                "routingVersionId": str_routing_version_id,
            },
            "capabilityBoundary": self.__capability_boundary(),
            "warnings": lst_warnings,
        }

    def __build_test_support_dashboard_rows(self, lst_source_rows, str_keyword):
        str_keyword = (str_keyword or "").strip().lower()
        dict_grouped_rows = {}
        for dict_row in lst_source_rows:
            str_route_id = dict_row.get("test_support_route_id", "")
            if not str_route_id:
                continue
            if str_route_id not in dict_grouped_rows:
                dict_grouped_rows[str_route_id] = {
                    "source": dict_row,
                    "stepCount": 0,
                }
            dict_grouped_rows[str_route_id]["stepCount"] += 1
        lst_rows = []
        for str_route_id, dict_group in dict_grouped_rows.items():
            dict_source = dict_group.get("source", {})
            dict_result = {
                "routingVersionId": str_route_id,
                "itemNo": dict_source.get("product_no", ""),
                "itemName": dict_source.get("product_name", ""),
                "itemCategory": EItemCategory.PRODUCT,
                "itemSubCategory": 0,
                "routingVersion": util_safe_int(dict_source.get("product_version")),
                "versionStateCode": EBomVersionState.EFFECTIVE,
                "routingStatusCode": ERoutingStatusCode.PARTIAL,
                "dateTimestamp": 0,
                "stepCount": util_safe_int(dict_group.get("stepCount")),
                "warningCodes": [ERoutingWarningCode.TEST_SUPPORT_ONLY],
            }
            str_search_body = " ".join([
                dict_result.get("routingVersionId", ""),
                dict_result.get("itemNo", ""),
                dict_result.get("itemName", ""),
            ]).lower()
            if str_keyword and str_keyword not in str_search_body:
                continue
            lst_rows.append(dict_result)
        return sorted(lst_rows, key=lambda dict_row: (dict_row.get("itemNo", ""), -util_safe_int(dict_row.get("routingVersion"))))

    def __build_test_support_step_row(self, dict_source):
        return {
            "stepId": dict_source.get("test_support_step_id", ""),
            "stepOrder": util_safe_int(dict_source.get("step_sequence")),
            "oneProcess": 0,
            "secProcess": 0,
            "processNo": "",
            "processLabel": dict_source.get("step_label", ""),
            "stageCode": "test_support",
            "stageLabel": "test_support",
            "groupCode": "test_support",
            "groupLabel": "test_support",
            "recipeReference": {
                "established": bool(dict_source.get("bom_no", "")),
                "recipeNo": dict_source.get("bom_no", ""),
                "recipeVersion": util_safe_int(dict_source.get("bom_version")),
                "sourceCode": ERoutingSourceCode.TEST_SUPPORT,
            },
            "packagingContext": {
                "established": False,
                "packagingLevel": 0,
                "packagingBomNo": "",
                "quantity": 0,
                "unit": 0,
                "weight": 0.0,
                "sourceCode": ERoutingSourceCode.NOT_RECORDED,
            },
            "resourceEligibility": {
                "governed": False,
                "eligibleResourceRefs": [],
                "sourceCode": ERoutingSourceCode.NOT_RECORDED,
            },
            "standardPerformance": {
                "governed": False,
                "hourlyOutput": 0.0,
                "laborCount": 0,
                "unit": 0,
                "sourceDateTimestamp": 0,
                "sourceCode": ERoutingSourceCode.NOT_RECORDED,
            },
            "sourceLineage": {
                "stepSourceCode": ERoutingSourceCode.TEST_SUPPORT,
                "processSourceCode": ERoutingSourceCode.NOT_RECORDED,
                "standardPerformanceSourceCode": ERoutingSourceCode.NOT_RECORDED,
            },
        }

    def __build_test_support_warnings(self, str_routing_version_id, lst_steps, dict_warning_map):
        lst_warnings = []
        if not lst_steps:
            self.__append_warning(lst_warnings, ERoutingWarningCode.MISSING_STEPS, str_routing_version_id, "")
            return lst_warnings
        self.__append_warning(lst_warnings, ERoutingWarningCode.TEST_SUPPORT_ONLY, str_routing_version_id, "")
        dict_warning = dict_warning_map.get(str_routing_version_id, {})
        if dict_warning.get("warning_behavior"):
            self.__append_warning(lst_warnings, ERoutingWarningCode.RESOURCE_ELIGIBILITY_NOT_GOVERNED, str_routing_version_id, "")
        for dict_step in lst_steps:
            self.__append_warning(lst_warnings, ERoutingWarningCode.MISSING_PROCESS_MASTER, str_routing_version_id, dict_step.get("stepId", ""))
            self.__append_warning(lst_warnings, ERoutingWarningCode.MISSING_STANDARD_PERFORMANCE, str_routing_version_id, dict_step.get("stepId", ""))
        return lst_warnings

    def __build_dashboard_row(self, obj_product_process, str_version_state_code, dict_step_counts, dict_item_map):
        n_step_count = util_safe_int(dict_step_counts.get(obj_product_process.no or "", 0))
        dict_item = dict_item_map.get(obj_product_process.item_no or "", {})
        lst_warning_codes = self.__row_warning_codes(obj_product_process, n_step_count, dict_item)
        return {
            "routingVersionId": obj_product_process.no or "",
            "itemNo": obj_product_process.item_no or "",
            "itemName": dict_item.get("itemName", ""),
            "itemCategory": util_safe_int(dict_item.get("itemCategory")),
            "itemSubCategory": util_safe_int(dict_item.get("itemSubCategory")),
            "routingVersion": util_safe_int(obj_product_process.version),
            "versionStateCode": str_version_state_code,
            "routingStatusCode": self.__routing_status_code(n_step_count, lst_warning_codes),
            "dateTimestamp": util_safe_int(obj_product_process.date),
            "stepCount": n_step_count,
            "warningCodes": lst_warning_codes,
        }

    def __build_version_row(self, obj_product_process, str_version_state_code, dict_step_counts, dict_item_map):
        return self.__build_dashboard_row(obj_product_process, str_version_state_code, dict_step_counts, dict_item_map)

    def __build_item_header(self, str_item_no, dict_item_map):
        dict_item = dict_item_map.get(str_item_no, {})
        return {
            "itemNo": str_item_no,
            "itemName": dict_item.get("itemName", ""),
            "itemCategory": util_safe_int(dict_item.get("itemCategory")),
            "itemSubCategory": util_safe_int(dict_item.get("itemSubCategory")),
            "sourceCode": dict_item.get("sourceCode", ERoutingSourceCode.NOT_RECORDED),
        }

    def __build_steps(self, obj_session, obj_product_process, dict_process_map, dict_capacity_map):
        lst_flow_rows = (
            obj_session.query(CTableProcessFlow)
            .filter(CTableProcessFlow.product_process_no == obj_product_process.no)
            .order_by(CTableProcessFlow.order.asc(), CTableProcessFlow.id.asc())
            .all()
        )
        return [
            self.__build_step_row(obj_session, obj_product_process, obj_row, dict_process_map, dict_capacity_map)
            for obj_row in lst_flow_rows
        ]

    def __build_step_row(self, obj_session, obj_product_process, obj_flow, dict_process_map, dict_capacity_map):
        tuple_key = (util_safe_int(obj_flow.oneProcess), util_safe_int(obj_flow.secProcess))
        obj_process = dict_process_map.get(tuple_key)
        obj_capacity = dict_capacity_map.get(tuple_key)
        return {
            "stepId": obj_flow.no or "",
            "stepOrder": util_safe_int(obj_flow.order),
            "oneProcess": tuple_key[0],
            "secProcess": tuple_key[1],
            "processNo": getattr(obj_process, "no", "") if obj_process else "",
            "processLabel": getattr(obj_process, "comment", "") if obj_process else "",
            "stageCode": self.__stage_code(tuple_key[0]),
            "stageLabel": self.__stage_code(tuple_key[0]),
            "groupCode": self.__group_code(tuple_key[0], tuple_key[1]),
            "groupLabel": self.__group_code(tuple_key[0], tuple_key[1]),
            "recipeReference": self.__recipe_reference(obj_session, obj_product_process),
            "packagingContext": self.__packaging_context(obj_session, obj_product_process),
            "resourceEligibility": {
                "governed": False,
                "eligibleResourceRefs": [],
                "sourceCode": ERoutingSourceCode.NOT_RECORDED,
            },
            "standardPerformance": self.__standard_performance(obj_capacity),
            "sourceLineage": {
                "stepSourceCode": ERoutingSourceCode.PROCESS_FLOW,
                "processSourceCode": ERoutingSourceCode.PROCESS if obj_process else ERoutingSourceCode.NOT_RECORDED,
                "standardPerformanceSourceCode": ERoutingSourceCode.PROCESS_CAPACITY if obj_capacity else ERoutingSourceCode.NOT_RECORDED,
            },
        }

    def __recipe_reference(self, obj_session, obj_product_process):
        lst_product_nos = [obj_product_process.item_no or "", "%s_1" % (obj_product_process.item_no or "")]
        obj_spec = (
            obj_session.query(CTableProductSpec)
            .filter(
                CTableProductSpec.product_no.in_(lst_product_nos),
                CTableProductSpec.product_version == util_safe_int(obj_product_process.version),
            )
            .order_by(CTableProductSpec.id.asc())
            .first()
        )
        if not obj_spec or not obj_spec.bom_no:
            return {"established": False, "recipeNo": "", "recipeVersion": 0, "sourceCode": ERoutingSourceCode.NOT_RECORDED}
        return {
            "established": True,
            "recipeNo": obj_spec.bom_no or "",
            "recipeVersion": util_safe_int(obj_spec.bom_version),
            "sourceCode": ERoutingSourceCode.PRODUCT_SPEC,
        }

    def __packaging_context(self, obj_session, obj_product_process):
        obj_spec = (
            obj_session.query(CTableProductBOMSpec)
            .filter(
                CTableProductBOMSpec.product_no == obj_product_process.item_no,
                CTableProductBOMSpec.product_version == util_safe_int(obj_product_process.version),
            )
            .order_by(CTableProductBOMSpec.level.asc(), CTableProductBOMSpec.id.asc())
            .first()
        )
        if not obj_spec:
            return {
                "established": False,
                "packagingLevel": 0,
                "packagingBomNo": "",
                "quantity": 0,
                "unit": 0,
                "weight": 0.0,
                "sourceCode": ERoutingSourceCode.NOT_RECORDED,
            }
        return {
            "established": True,
            "packagingLevel": util_safe_int(obj_spec.level),
            "packagingBomNo": obj_spec.bom2_no or "",
            "quantity": util_safe_int(obj_spec.count),
            "unit": util_safe_int(obj_spec.unit),
            "weight": util_round_quantity(obj_spec.weight),
            "sourceCode": ERoutingSourceCode.PRODUCT_BOM_SPEC,
        }

    def __standard_performance(self, obj_capacity):
        if not obj_capacity:
            return {
                "governed": False,
                "hourlyOutput": 0.0,
                "laborCount": 0,
                "unit": 0,
                "sourceDateTimestamp": 0,
                "sourceCode": ERoutingSourceCode.NOT_RECORDED,
            }
        return {
            "governed": True,
            "hourlyOutput": util_round_quantity(util_safe_float(obj_capacity.hourlyOutput)),
            "laborCount": util_safe_int(obj_capacity.laborCount),
            "unit": util_safe_int(obj_capacity.unit),
            "sourceDateTimestamp": util_safe_int(obj_capacity.date),
            "sourceCode": ERoutingSourceCode.PROCESS_CAPACITY,
        }

    def __build_routing_header(self, obj_product_process, str_version_state_code, dict_item_map, lst_steps, lst_warnings):
        dict_row = self.__build_dashboard_row(
            obj_product_process,
            str_version_state_code,
            {obj_product_process.no: len(lst_steps)},
            dict_item_map,
        )
        dict_row["routingStatusCode"] = self.__routing_status_code(len(lst_steps), [
            dict_warning.get("warningCode", "") for dict_warning in lst_warnings
        ])
        return dict_row

    def __source_lineage(self, obj_product_process):
        return {
            "routingVersionSourceCode": ERoutingSourceCode.PRODUCT_PROCESS,
            "stepSourceCode": ERoutingSourceCode.PROCESS_FLOW,
            "processIdentitySourceCode": ERoutingSourceCode.PROCESS,
            "recipeReferenceSourceCode": ERoutingSourceCode.PRODUCT_SPEC,
            "packagingContextSourceCode": ERoutingSourceCode.PRODUCT_BOM_SPEC,
            "resourceEligibilitySourceCode": ERoutingSourceCode.NOT_RECORDED,
            "routingVersionId": obj_product_process.no or "",
        }

    def __build_warnings(self, obj_product_process, lst_steps, dict_item_map):
        lst_warnings = []
        if not dict_item_map.get(obj_product_process.item_no or ""):
            self.__append_warning(lst_warnings, ERoutingWarningCode.MISSING_ITEM_MASTER, obj_product_process.item_no or "", "")
        if not lst_steps:
            self.__append_warning(lst_warnings, ERoutingWarningCode.MISSING_STEPS, obj_product_process.no or "", "")
        b_has_recipe = any(dict_step["recipeReference"].get("established") for dict_step in lst_steps)
        b_has_packaging = any(dict_step["packagingContext"].get("established") for dict_step in lst_steps)
        for dict_step in lst_steps:
            if not dict_step.get("processNo"):
                self.__append_warning(lst_warnings, ERoutingWarningCode.MISSING_PROCESS_MASTER, dict_step.get("stepId", ""), "")
            if not dict_step["standardPerformance"].get("governed"):
                self.__append_warning(lst_warnings, ERoutingWarningCode.MISSING_STANDARD_PERFORMANCE, dict_step.get("stepId", ""), "")
            if not dict_step["resourceEligibility"].get("governed"):
                self.__append_warning(lst_warnings, ERoutingWarningCode.RESOURCE_ELIGIBILITY_NOT_GOVERNED, dict_step.get("stepId", ""), "")
        if not b_has_recipe:
            self.__append_warning(lst_warnings, ERoutingWarningCode.MISSING_RECIPE_REFERENCE, obj_product_process.no or "", "")
        if not b_has_packaging:
            self.__append_warning(lst_warnings, ERoutingWarningCode.PACKAGING_CONTEXT_NOT_GOVERNED, obj_product_process.no or "", "")
        return lst_warnings

    def __row_warning_codes(self, obj_product_process, n_step_count, dict_item):
        lst_warnings = []
        if not dict_item:
            lst_warnings.append(ERoutingWarningCode.MISSING_ITEM_MASTER)
        if n_step_count <= 0:
            lst_warnings.append(ERoutingWarningCode.MISSING_STEPS)
        return lst_warnings

    def __routing_status_code(self, n_step_count, lst_warning_codes):
        if n_step_count <= 0:
            return ERoutingStatusCode.MISSING
        if lst_warning_codes:
            return ERoutingStatusCode.PARTIAL
        return ERoutingStatusCode.COMPLETE

    def __build_summary(self, lst_rows):
        return {
            "itemCount": len({dict_row.get("itemNo", "") for dict_row in lst_rows if dict_row.get("itemNo")}),
            "routingVersionCount": len(lst_rows),
            "completeRoutingCount": len([dict_row for dict_row in lst_rows if dict_row.get("routingStatusCode") == ERoutingStatusCode.COMPLETE]),
            "partialRoutingCount": len([dict_row for dict_row in lst_rows if dict_row.get("routingStatusCode") == ERoutingStatusCode.PARTIAL]),
            "missingRoutingCount": len([dict_row for dict_row in lst_rows if dict_row.get("routingStatusCode") == ERoutingStatusCode.MISSING]),
        }

    def __select_current_version(self, lst_versions, dict_state):
        for obj_row in lst_versions:
            if dict_state.get((obj_row.item_no, obj_row.version)) == EBomVersionState.EFFECTIVE:
                return obj_row
        lst_known_versions = [obj_row for obj_row in lst_versions if util_safe_int(obj_row.date) > 0]
        lst_source = lst_known_versions if lst_known_versions else lst_versions
        return sorted(lst_source, key=lambda obj_row: -util_safe_int(obj_row.version))[0]

    def __stage_code(self, n_one_process):
        return {
            1: "preparation",
            2: "processing",
            3: "packaging",
            0: "other",
        }.get(util_safe_int(n_one_process), "unknown")

    def __group_code(self, n_one_process, n_sec_process):
        return "%s:%s" % (util_safe_int(n_one_process), util_safe_int(n_sec_process))

    def __append_warning(self, lst_warnings, str_warning_code, str_ref_no, str_step_id):
        dict_warning = {
            "warningCode": str_warning_code or ERoutingWarningCode.UNKNOWN,
            "refNo": str_ref_no or "",
            "stepId": str_step_id or "",
        }
        for dict_row in lst_warnings:
            if dict_row == dict_warning:
                return
        lst_warnings.append(dict_warning)

    def __capability_boundary(self):
        return {
            "routingWriteSupported": False,
            "processMasterWriteSupported": False,
            "productWriteSupported": False,
            "approvalSupported": False,
            "releaseSupported": False,
            "freezeSupported": False,
            "schedulingExecutionSupported": False,
            "capacityExecutionSupported": False,
            "packagingSpecificationImplementationSupported": False,
            "productionActionSupported": False,
            "costingExcluded": True,
        }


class CRoutingDashboard(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CRoutingProcessFlowService().get_dashboard(
                str_keyword=request.args.get("keyword", "", type=str),
                str_routing_status_code=request.args.get("routingStatusCode", "", type=str),
                n_effective_date=request.args.get("effectiveDate", 0, type=int),
                n_start=request.args.get("start", 0, type=int),
                n_count=request.args.get("count", 50, type=int),
            )
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CRoutingDashboard] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CRoutingVersions(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CRoutingProcessFlowService().get_versions(
                str_item_no=str_id,
                n_effective_date=request.args.get("effectiveDate", 0, type=int),
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
            CLogger().log(CLogger.LOG_LEVELERROR, "[CRoutingVersions] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CRoutingSteps(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CRoutingProcessFlowService().get_steps(
                str_routing_version_id=str_id,
                n_effective_date=request.args.get("effectiveDate", 0, type=int),
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
            CLogger().log(CLogger.LOG_LEVELERROR, "[CRoutingSteps] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CRoutingCurrent(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CRoutingProcessFlowService().get_current(
                str_item_no=str_id,
                n_effective_date=request.args.get("effectiveDate", 0, type=int),
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
            CLogger().log(CLogger.LOG_LEVELERROR, "[CRoutingCurrent] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data
