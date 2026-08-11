# coding=utf8
import time
from collections import defaultdict

from flask import request
from sqlalchemy import func, or_

from package.common.common import EBomVersionState, EErrorCode
from package.dbwrapper.dbmgr import CDBMgr
from package.dbwrapper.table import CTableBOM, CTableBOMItem, CTableProductSpec
from package.log.log import CLogger
from package.util.util import util_round_quantity, util_safe_float, util_safe_int


class CBomCenterService(object):
    def get_dashboard(
        self,
        n_date=0,
        str_keyword="",
        str_bom_no="",
        str_version_state_code="",
        n_start=0,
        n_count=50,
    ):
        with CDBMgr() as obj_dbmgr:
            return self.__get_dashboard_with_session(
                obj_dbmgr.get_session(),
                n_date,
                str_keyword,
                str_bom_no,
                str_version_state_code,
                n_start,
                n_count,
            )

    def get_detail(self, str_bom_no, n_version=0, n_date=0):
        with CDBMgr() as obj_dbmgr:
            return self.__get_detail_with_session(
                obj_dbmgr.get_session(),
                str_bom_no,
                n_version,
                n_date,
            )

    def __get_dashboard_with_session(
        self,
        obj_session,
        n_date,
        str_keyword,
        str_bom_no,
        str_version_state_code,
        n_start,
        n_count,
    ):
        n_query_timestamp = util_safe_int(n_date) or util_safe_int(time.time())
        n_start = max(util_safe_int(n_start), 0)
        n_count = min(max(util_safe_int(n_count), 1), 100)
        lst_boms = self.__query_boms(obj_session, str_keyword, str_bom_no)
        dict_state = self.__build_version_state_map(lst_boms, n_query_timestamp)
        if str_version_state_code:
            lst_boms = [
                obj_bom for obj_bom in lst_boms
                if dict_state.get((obj_bom.no, obj_bom.version), EBomVersionState.UNKNOWN) == str_version_state_code
            ]

        lst_boms = sorted(
            lst_boms,
            key=lambda obj_bom: (
                obj_bom.no or "",
                -util_safe_int(obj_bom.version),
                -util_safe_int(obj_bom.date),
            ),
        )
        n_total = len(lst_boms)
        lst_page_boms = lst_boms[n_start:n_start + n_count]
        lst_bom_nos = list({obj_bom.no for obj_bom in lst_page_boms if obj_bom.no})
        dict_item_counts = self.__load_item_counts(obj_session, lst_bom_nos)
        dict_linked_product_counts = self.__load_linked_product_counts(obj_session, lst_bom_nos)
        dict_summary = self.__build_summary(lst_boms, dict_state)

        return {
            "serverTimestamp": util_safe_int(time.time()),
            "summary": dict_summary,
            "items": [
                self.__build_dashboard_row(
                    obj_bom,
                    dict_state.get((obj_bom.no, obj_bom.version), EBomVersionState.UNKNOWN),
                    dict_item_counts,
                    dict_linked_product_counts,
                )
                for obj_bom in lst_page_boms
            ],
            "total": n_total,
            "start": n_start,
            "count": len(lst_page_boms),
        }

    def __get_detail_with_session(self, obj_session, str_bom_no, n_version, n_date):
        str_bom_no = (str_bom_no or "").strip()
        if not str_bom_no:
            return None
        n_query_timestamp = util_safe_int(n_date) or util_safe_int(time.time())
        lst_boms = (
            obj_session.query(CTableBOM)
            .filter(CTableBOM.no == str_bom_no)
            .all()
        )
        if not lst_boms:
            return None
        dict_state = self.__build_version_state_map(lst_boms, n_query_timestamp)
        obj_selected_bom = self.__select_detail_bom(lst_boms, dict_state, util_safe_int(n_version))
        if not obj_selected_bom:
            return None
        lst_items = (
            obj_session.query(CTableBOMItem)
            .filter(CTableBOMItem.bom_no == str_bom_no)
            .order_by(CTableBOMItem.item_no.asc())
            .all()
        )
        lst_linked_products = (
            obj_session.query(CTableProductSpec)
            .filter(CTableProductSpec.bom_no == str_bom_no)
            .order_by(CTableProductSpec.product_no.asc(), CTableProductSpec.product_version.asc())
            .all()
        )
        return {
            "bom": self.__build_bom_header(
                obj_selected_bom,
                dict_state.get((obj_selected_bom.no, obj_selected_bom.version), EBomVersionState.UNKNOWN),
            ),
            "versions": [
                {
                    "version": util_safe_int(obj_bom.version),
                    "dateTimestamp": util_safe_int(obj_bom.date),
                    "versionStateCode": dict_state.get((obj_bom.no, obj_bom.version), EBomVersionState.UNKNOWN),
                }
                for obj_bom in sorted(lst_boms, key=lambda obj_row: -util_safe_int(obj_row.version))
            ],
            "items": [self.__build_item_row(obj_item) for obj_item in lst_items],
            "linkedProducts": [
                self.__build_linked_product_row(obj_product_spec)
                for obj_product_spec in lst_linked_products
            ],
        }

    def __query_boms(self, obj_session, str_keyword, str_bom_no):
        obj_query = obj_session.query(CTableBOM)
        str_bom_no = (str_bom_no or "").strip()
        str_keyword = (str_keyword or "").strip()
        if str_bom_no:
            obj_query = obj_query.filter(CTableBOM.no == str_bom_no)
        if str_keyword:
            str_like = "%%%s%%" % str_keyword
            lst_item_bom_nos = [
                obj_row.bom_no
                for obj_row in obj_session.query(CTableBOMItem.bom_no)
                .filter(or_(
                    CTableBOMItem.item_no.ilike(str_like),
                    CTableBOMItem.item_name.ilike(str_like),
                ))
                .distinct()
                .all()
            ]
            obj_query = obj_query.filter(or_(
                CTableBOM.no.ilike(str_like),
                CTableBOM.displayName.ilike(str_like),
                CTableBOM.no.in_(lst_item_bom_nos) if lst_item_bom_nos else False,
            ))
        return obj_query.all()

    def __build_version_state_map(self, lst_boms, n_query_timestamp):
        dict_effective_version_by_no = {}
        for obj_bom in lst_boms:
            n_date = util_safe_int(obj_bom.date)
            if n_date > 0 and n_date <= n_query_timestamp:
                str_no = obj_bom.no or ""
                n_version = util_safe_int(obj_bom.version)
                if n_version > dict_effective_version_by_no.get(str_no, 0):
                    dict_effective_version_by_no[str_no] = n_version

        dict_state = {}
        for obj_bom in lst_boms:
            str_no = obj_bom.no or ""
            n_version = util_safe_int(obj_bom.version)
            n_date = util_safe_int(obj_bom.date)
            if n_date <= 0:
                str_state = EBomVersionState.UNKNOWN
            elif n_date > n_query_timestamp:
                str_state = EBomVersionState.FUTURE
            elif n_version == dict_effective_version_by_no.get(str_no, 0):
                str_state = EBomVersionState.EFFECTIVE
            else:
                str_state = EBomVersionState.HISTORICAL
            dict_state[(obj_bom.no, obj_bom.version)] = str_state
        return dict_state

    def __load_item_counts(self, obj_session, lst_bom_nos):
        if not lst_bom_nos:
            return {}
        return {
            obj_row.bom_no: util_safe_int(obj_row.count)
            for obj_row in obj_session.query(
                CTableBOMItem.bom_no,
                func.count(CTableBOMItem.id).label("count"),
            )
            .filter(CTableBOMItem.bom_no.in_(lst_bom_nos))
            .group_by(CTableBOMItem.bom_no)
            .all()
        }

    def __load_linked_product_counts(self, obj_session, lst_bom_nos):
        if not lst_bom_nos:
            return {}
        return {
            obj_row.bom_no: util_safe_int(obj_row.count)
            for obj_row in obj_session.query(
                CTableProductSpec.bom_no,
                func.count(CTableProductSpec.id).label("count"),
            )
            .filter(CTableProductSpec.bom_no.in_(lst_bom_nos))
            .group_by(CTableProductSpec.bom_no)
            .all()
        }

    def __build_summary(self, lst_boms, dict_state):
        dict_counts = defaultdict(int)
        for obj_bom in lst_boms:
            dict_counts[dict_state.get((obj_bom.no, obj_bom.version), EBomVersionState.UNKNOWN)] += 1
        return {
            "bomCount": len({obj_bom.no for obj_bom in lst_boms if obj_bom.no}),
            "versionCount": len(lst_boms),
            "effectiveVersionCount": dict_counts[EBomVersionState.EFFECTIVE],
            "futureVersionCount": dict_counts[EBomVersionState.FUTURE],
            "historicalVersionCount": dict_counts[EBomVersionState.HISTORICAL],
        }

    def __build_dashboard_row(
        self,
        obj_bom,
        str_version_state_code,
        dict_item_counts,
        dict_linked_product_counts,
    ):
        return {
            "bomNo": obj_bom.no or "",
            "bomName": obj_bom.displayName or "",
            "version": util_safe_int(obj_bom.version),
            "dateTimestamp": util_safe_int(obj_bom.date),
            "unit": util_safe_int(obj_bom.unit),
            "weight": util_round_quantity(obj_bom.weight),
            "versionStateCode": str_version_state_code,
            "itemCount": util_safe_int(dict_item_counts.get(obj_bom.no, 0)),
            "linkedProductCount": util_safe_int(dict_linked_product_counts.get(obj_bom.no, 0)),
        }

    def __build_bom_header(self, obj_bom, str_version_state_code):
        dict_row = self.__build_dashboard_row(obj_bom, str_version_state_code, {}, {})
        return {
            "bomNo": dict_row["bomNo"],
            "bomName": dict_row["bomName"],
            "version": dict_row["version"],
            "dateTimestamp": dict_row["dateTimestamp"],
            "unit": dict_row["unit"],
            "weight": dict_row["weight"],
            "comment": obj_bom.comment or "",
            "versionStateCode": dict_row["versionStateCode"],
        }

    def __build_item_row(self, obj_item):
        return {
            "itemNo": obj_item.item_no or "",
            "itemName": obj_item.item_name or "",
            "unit": util_safe_int(obj_item.unit),
            "weight": util_round_quantity(obj_item.weight),
        }

    def __build_linked_product_row(self, obj_product_spec):
        return {
            "productNo": obj_product_spec.product_no or "",
            "productVersion": util_safe_int(obj_product_spec.product_version),
            "level": util_safe_int(obj_product_spec.level),
            "itemType": util_safe_int(obj_product_spec.item_type),
            "itemNo": obj_product_spec.item_no or "",
            "count": util_safe_int(obj_product_spec.count),
            "unit": util_safe_int(obj_product_spec.unit),
            "weight": util_round_quantity(obj_product_spec.weight),
        }

    def __select_detail_bom(self, lst_boms, dict_state, n_version):
        if n_version > 0:
            for obj_bom in lst_boms:
                if util_safe_int(obj_bom.version) == n_version:
                    return obj_bom
            return None
        for obj_bom in lst_boms:
            if dict_state.get((obj_bom.no, obj_bom.version)) == EBomVersionState.EFFECTIVE:
                return obj_bom
        lst_known_boms = [obj_bom for obj_bom in lst_boms if util_safe_int(obj_bom.date) > 0]
        lst_source = lst_known_boms if lst_known_boms else lst_boms
        return sorted(lst_source, key=lambda obj_row: -util_safe_int(obj_row.version))[0]


class CBomCenterDashboard(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CBomCenterService().get_dashboard(
                n_date=request.args.get("date", 0, type=int),
                str_keyword=request.args.get("keyword", "", type=str),
                str_bom_no=request.args.get("bomNo", "", type=str),
                str_version_state_code=request.args.get("versionStateCode", "", type=str),
                n_start=request.args.get("start", 0, type=int),
                n_count=request.args.get("count", 50, type=int),
            )
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CBomCenterDashboard] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CBomCenterDetail(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CBomCenterService().get_detail(
                str_bom_no=str_id,
                n_version=request.args.get("version", 0, type=int),
                n_date=request.args.get("date", 0, type=int),
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
            CLogger().log(CLogger.LOG_LEVELERROR, "[CBomCenterDetail] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data
