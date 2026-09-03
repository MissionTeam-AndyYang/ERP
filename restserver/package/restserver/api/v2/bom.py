# coding=utf8
import time
from collections import defaultdict

from flask import request
from sqlalchemy import func, or_

from package.common.common import (
    EBomCategory,
    EBomVersionState,
    EErrorCode,
    EItemCategory,
    EProductStructureStatusCode,
    EProductStructureWarningCode,
)
from package.dbwrapper.dbmgr import CDBMgr
from package.dbwrapper.table import (
    CTableBOM,
    CTableBOMItem,
    CTableGoods,
    CTableInproduct,
    CTableInproductBOMSpec,
    CTableMaterial,
    CTableProduct,
    CTableProductSpec,
)
from package.log.log import CLogger
from package.util.util import util_round_quantity, util_safe_int


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

    def get_product_structure(self, str_product_no, n_product_version=0, n_depth=3, n_effective_date=0):
        with CDBMgr() as obj_dbmgr:
            return self.__get_product_structure_with_session(
                obj_dbmgr.get_session(),
                str_product_no,
                n_product_version,
                n_depth,
                n_effective_date,
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
            "linkedProducts": self.__build_linked_products(obj_session, lst_linked_products),
        }

    def __get_product_structure_with_session(
        self,
        obj_session,
        str_product_no,
        n_product_version,
        n_depth,
        n_effective_date,
    ):
        str_product_no = (str_product_no or "").strip()
        if not str_product_no:
            return None
        obj_product = obj_session.query(CTableProduct).filter(CTableProduct.no == str_product_no).first()
        if not obj_product:
            return None
        n_query_timestamp = util_safe_int(n_effective_date) or util_safe_int(time.time())
        n_selected_version = self.__select_product_structure_version(
            obj_session,
            str_product_no,
            util_safe_int(n_product_version),
            util_safe_int(obj_product.version),
        )
        n_depth = min(max(util_safe_int(n_depth) or 3, 1), 5)
        dict_item_map = self.__load_structure_item_map(obj_session)
        lst_warnings = []
        str_root_node_id = "product:%s:%s" % (str_product_no, n_selected_version)
        lst_children = self.__build_product_structure_children(
            obj_session,
            str_product_no,
            n_selected_version,
            str_root_node_id,
            1,
            n_depth,
            dict_item_map,
            lst_warnings,
            set([str_root_node_id]),
        )
        str_structure_status_code = self.__product_structure_status_code(lst_children, lst_warnings)
        return {
            "serverTimestamp": util_safe_int(time.time()),
            "rootProduct": {
                "productNo": str_product_no,
                "productName": obj_product.name or "",
                "productVersion": n_selected_version,
                "productCategory": util_safe_int(obj_product.category),
                "unitProduct": util_safe_int(obj_product.unitProduct),
                "structureStatusCode": str_structure_status_code,
            },
            "bomEvidence": self.__build_product_structure_bom_evidence(
                obj_session,
                str_product_no,
                n_selected_version,
                n_query_timestamp,
            ),
            "children": lst_children,
            "warnings": lst_warnings,
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
        dict_result = defaultdict(set)
        lst_rows = (
            obj_session.query(CTableProductSpec)
            .filter(CTableProductSpec.bom_no.in_(lst_bom_nos))
            .all()
        )
        for obj_row in lst_rows:
            if not obj_row.bom_no:
                continue
            dict_result[obj_row.bom_no].add(
                (
                    self.__normalize_product_no(obj_row.product_no),
                    util_safe_int(obj_row.product_version),
                )
            )
        return {
            str_bom_no: len(set_product_keys)
            for str_bom_no, set_product_keys in dict_result.items()
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

    def __build_linked_products(self, obj_session, lst_product_specs):
        if not lst_product_specs:
            return []
        dict_product_names = self.__load_product_map(
            obj_session,
            {self.__normalize_product_no(obj_row.product_no) for obj_row in lst_product_specs},
        )
        dict_inproduct_names = self.__load_inproduct_name_map(
            obj_session,
            {obj_row.item_no for obj_row in lst_product_specs if util_safe_int(obj_row.item_type) == 1},
        )
        dict_content_product_names = self.__load_product_map(
            obj_session,
            {obj_row.item_no for obj_row in lst_product_specs if util_safe_int(obj_row.item_type) == 2},
        )

        dict_grouped_rows = defaultdict(list)
        for obj_row in lst_product_specs:
            str_product_no = self.__normalize_product_no(obj_row.product_no)
            n_product_version = util_safe_int(obj_row.product_version)
            dict_grouped_rows[(str_product_no, n_product_version)].append(obj_row)

        lst_results = []
        for tuple_key in sorted(dict_grouped_rows.keys()):
            str_product_no, n_product_version = tuple_key
            lst_group_rows = dict_grouped_rows[tuple_key]
            lst_parent_rows = [
                obj_row for obj_row in lst_group_rows
                if self.__is_parent_product_no(obj_row.product_no, str_product_no)
            ]
            lst_content_rows = lst_parent_rows if lst_parent_rows else lst_group_rows
            dict_product = dict_product_names.get(str_product_no, {})
            lst_results.append({
                "productNo": str_product_no,
                "productName": dict_product.get("name", ""),
                "productVersion": n_product_version,
                "productCategory": util_safe_int(dict_product.get("category", 0)),
                "contents": [
                    self.__build_linked_product_content_row(
                        obj_row,
                        dict_inproduct_names,
                        dict_content_product_names,
                    )
                    for obj_row in sorted(
                        lst_content_rows,
                        key=lambda obj_content: (
                            util_safe_int(obj_content.item_type),
                            obj_content.item_no or "",
                            util_safe_int(obj_content.id),
                        ),
                    )
                ],
            })
        return lst_results

    def __build_linked_product_content_row(self, obj_product_spec, dict_inproduct_names, dict_product_names):
        n_item_type = util_safe_int(obj_product_spec.item_type)
        str_item_no = obj_product_spec.item_no or ""
        if n_item_type == 1:
            str_item_name = dict_inproduct_names.get(str_item_no, "")
        elif n_item_type == 2:
            str_item_name = dict_product_names.get(str_item_no, {}).get("name", "")
        else:
            str_item_name = ""
        return {
            "itemType": n_item_type,
            "itemNo": str_item_no,
            "itemName": str_item_name,
            "count": util_safe_int(obj_product_spec.count),
            "unit": util_safe_int(obj_product_spec.unit),
            "weight": util_round_quantity(obj_product_spec.weight),
        }

    def __load_product_map(self, obj_session, set_product_nos):
        lst_product_nos = [str_no for str_no in set_product_nos if str_no]
        if not lst_product_nos:
            return {}
        return {
            obj_row.no: {
                "name": obj_row.name or "",
                "category": util_safe_int(obj_row.category),
            }
            for obj_row in obj_session.query(CTableProduct)
            .filter(CTableProduct.no.in_(lst_product_nos))
            .all()
        }

    def __load_inproduct_name_map(self, obj_session, set_inproduct_nos):
        lst_inproduct_nos = [str_no for str_no in set_inproduct_nos if str_no]
        if not lst_inproduct_nos:
            return {}
        return {
            obj_row.no: obj_row.name or ""
            for obj_row in obj_session.query(CTableInproduct)
            .filter(CTableInproduct.no.in_(lst_inproduct_nos))
            .all()
        }

    def __normalize_product_no(self, str_product_no):
        str_value = (str_product_no or "").strip()
        if str_value.endswith("_1"):
            return str_value[:-2]
        return str_value

    def __is_parent_product_no(self, str_product_no, str_normalized_product_no):
        return (str_product_no or "").strip() == "%s_1" % (str_normalized_product_no or "")

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

    def __select_product_structure_version(self, obj_session, str_product_no, n_product_version, n_product_master_version):
        if n_product_version > 0:
            return n_product_version
        lst_versions = [
            util_safe_int(obj_row.product_version)
            for obj_row in obj_session.query(CTableProductSpec.product_version)
            .filter(CTableProductSpec.product_no.in_([str_product_no, "%s_1" % str_product_no]))
            .distinct()
            .all()
        ]
        lst_versions = [n_version for n_version in lst_versions if n_version > 0]
        if lst_versions:
            return max(lst_versions)
        return util_safe_int(n_product_master_version)

    def __build_product_structure_children(
        self,
        obj_session,
        str_product_no,
        n_product_version,
        str_parent_node_id,
        n_level,
        n_depth,
        dict_item_map,
        lst_warnings,
        set_path,
    ):
        if n_level > n_depth:
            self.__append_structure_warning(
                lst_warnings,
                EProductStructureWarningCode.DEPTH_LIMITED,
                str_parent_node_id,
                "",
            )
            return []
        lst_specs = self.__query_product_structure_specs(obj_session, str_product_no, n_product_version)
        if n_level == 1 and not lst_specs:
            self.__append_structure_warning(
                lst_warnings,
                EProductStructureWarningCode.MISSING_PRODUCT_SPEC,
                str_parent_node_id,
                str_product_no,
            )
            return []
        lst_children = []
        for obj_spec in lst_specs:
            str_child_no = obj_spec.item_no or ""
            if not str_child_no or self.__is_self_product_structure_row(str_product_no, obj_spec):
                continue
            n_item_category = EItemCategory.INPRODUCT if util_safe_int(obj_spec.item_type) == 1 else EItemCategory.PRODUCT
            dict_child = self.__build_structure_node(
                str_parent_node_id,
                n_level,
                str_child_no,
                n_item_category,
                util_safe_int(obj_spec.count),
                obj_spec.weight,
                obj_spec.unit,
                obj_spec.bom_no,
                obj_spec.bom_version,
                dict_item_map,
                lst_warnings,
            )
            str_node_id = dict_child["nodeId"]
            if str_node_id in set_path:
                self.__append_structure_warning(
                    lst_warnings,
                    EProductStructureWarningCode.CIRCULAR_REFERENCE,
                    str_node_id,
                    str_child_no,
                )
            elif n_item_category == EItemCategory.INPRODUCT:
                dict_child["children"] = self.__build_inproduct_structure_children(
                    obj_session,
                    str_child_no,
                    obj_spec,
                    str_node_id,
                    n_level + 1,
                    n_depth,
                    dict_item_map,
                    lst_warnings,
                    set_path | set([str_node_id]),
                )
                dict_child["hasChildren"] = bool(dict_child["children"])
            elif n_item_category == EItemCategory.PRODUCT:
                dict_child["children"] = self.__build_product_structure_children(
                    obj_session,
                    str_child_no,
                    util_safe_int(obj_spec.bom_version) or n_product_version,
                    str_node_id,
                    n_level + 1,
                    n_depth,
                    dict_item_map,
                    lst_warnings,
                    set_path | set([str_node_id]),
                )
                dict_child["hasChildren"] = bool(dict_child["children"])
            lst_children.append(dict_child)
        return lst_children

    def __query_product_structure_specs(self, obj_session, str_product_no, n_product_version):
        lst_product_nos = [str_product_no, "%s_1" % str_product_no]
        lst_rows = (
            obj_session.query(CTableProductSpec)
            .filter(
                CTableProductSpec.product_no.in_(lst_product_nos),
                CTableProductSpec.product_version == n_product_version,
            )
            .order_by(CTableProductSpec.level.asc(), CTableProductSpec.id.asc())
            .all()
        )
        lst_parent_rows = [obj_row for obj_row in lst_rows if (obj_row.product_no or "") == "%s_1" % str_product_no]
        return lst_parent_rows if lst_parent_rows else lst_rows

    def __build_inproduct_structure_children(
        self,
        obj_session,
        str_inproduct_no,
        obj_parent_spec,
        str_parent_node_id,
        n_level,
        n_depth,
        dict_item_map,
        lst_warnings,
        set_path,
    ):
        if n_level > n_depth:
            self.__append_structure_warning(
                lst_warnings,
                EProductStructureWarningCode.DEPTH_LIMITED,
                str_parent_node_id,
                "",
            )
            return []
        lst_children = []
        lst_bom_spec_rows = (
            obj_session.query(CTableInproductBOMSpec)
            .filter(CTableInproductBOMSpec.inproduct_no == str_inproduct_no)
            .order_by(CTableInproductBOMSpec.category.asc(), CTableInproductBOMSpec.id.asc())
            .all()
        )
        for obj_bom_spec in lst_bom_spec_rows:
            if util_safe_int(obj_bom_spec.category) == EBomCategory.PM:
                lst_children.extend(self.__build_bom_item_structure_children(
                    obj_session,
                    obj_bom_spec.bom12_no or obj_parent_spec.bom_no or "",
                    util_safe_int(obj_bom_spec.item_version) or util_safe_int(obj_parent_spec.bom_version),
                    str_parent_node_id,
                    n_level,
                    n_depth,
                    dict_item_map,
                    lst_warnings,
                ))
            elif obj_bom_spec.item_no:
                lst_children.append(self.__build_structure_node(
                    str_parent_node_id,
                    n_level,
                    obj_bom_spec.item_no,
                    self.__resolve_item_category(dict_item_map, obj_bom_spec.item_no),
                    util_safe_int(obj_bom_spec.count),
                    obj_bom_spec.weight,
                    obj_bom_spec.unit,
                    obj_bom_spec.bom12_no,
                    obj_bom_spec.item_version,
                    dict_item_map,
                    lst_warnings,
                ))
        if not lst_children and obj_parent_spec.bom_no:
            lst_children.extend(self.__build_bom_item_structure_children(
                obj_session,
                obj_parent_spec.bom_no or "",
                util_safe_int(obj_parent_spec.bom_version),
                str_parent_node_id,
                n_level,
                n_depth,
                dict_item_map,
                lst_warnings,
            ))
        return lst_children

    def __build_bom_item_structure_children(
        self,
        obj_session,
        str_bom_no,
        n_bom_version,
        str_parent_node_id,
        n_level,
        n_depth,
        dict_item_map,
        lst_warnings,
    ):
        if n_level > n_depth:
            self.__append_structure_warning(
                lst_warnings,
                EProductStructureWarningCode.DEPTH_LIMITED,
                str_parent_node_id,
                str_bom_no,
            )
            return []
        str_bom_no = (str_bom_no or "").strip()
        if not str_bom_no:
            return []
        lst_rows = (
            obj_session.query(CTableBOMItem)
            .filter(CTableBOMItem.bom_no == str_bom_no)
            .order_by(CTableBOMItem.item_no.asc(), CTableBOMItem.id.asc())
            .all()
        )
        if not lst_rows:
            self.__append_structure_warning(
                lst_warnings,
                EProductStructureWarningCode.MISSING_BOM_ITEMS,
                str_parent_node_id,
                str_bom_no,
            )
        return [
            self.__build_structure_node(
                str_parent_node_id,
                n_level,
                obj_row.item_no or "",
                self.__resolve_item_category(dict_item_map, obj_row.item_no or ""),
                0,
                obj_row.weight,
                obj_row.unit,
                str_bom_no,
                n_bom_version,
                dict_item_map,
                lst_warnings,
            )
            for obj_row in lst_rows
            if obj_row.item_no
        ]

    def __build_structure_node(
        self,
        str_parent_node_id,
        n_level,
        str_item_no,
        n_item_category,
        n_relationship_quantity,
        f_relationship_weight,
        n_unit,
        str_bom_no,
        n_bom_version,
        dict_item_map,
        lst_warnings,
    ):
        dict_item = dict_item_map.get(str_item_no, {})
        if not dict_item:
            self.__append_structure_warning(
                lst_warnings,
                EProductStructureWarningCode.MISSING_ITEM_MASTER,
                str_parent_node_id,
                str_item_no,
            )
        n_resolved_category = util_safe_int(dict_item.get("itemCategory")) or util_safe_int(n_item_category)
        return {
            "nodeId": "%s:%s:%s" % (self.__structure_node_type_code(n_resolved_category), str_item_no, n_level),
            "parentNodeId": str_parent_node_id,
            "level": util_safe_int(n_level),
            "itemNo": str_item_no,
            "itemName": dict_item.get("itemName", ""),
            "itemCategory": n_resolved_category,
            "itemSubCategory": util_safe_int(dict_item.get("itemSubCategory")),
            "relationshipQuantity": util_safe_int(n_relationship_quantity),
            "relationshipWeight": util_round_quantity(f_relationship_weight),
            "unit": util_safe_int(n_unit),
            "bomNo": str_bom_no or "",
            "bomVersion": util_safe_int(n_bom_version),
            "hasChildren": False,
            "children": [],
        }

    def __build_product_structure_bom_evidence(self, obj_session, str_product_no, n_product_version, n_query_timestamp):
        lst_bom_keys = []
        for obj_row in (
            obj_session.query(CTableProductSpec)
            .filter(
                CTableProductSpec.product_no.in_([str_product_no, "%s_1" % str_product_no]),
                CTableProductSpec.product_version == n_product_version,
            )
            .all()
        ):
            if obj_row.bom_no:
                lst_bom_keys.append((obj_row.bom_no, util_safe_int(obj_row.bom_version)))
        lst_bom_nos = list({str_bom_no for str_bom_no, _ in lst_bom_keys if str_bom_no})
        if not lst_bom_nos:
            return []
        lst_boms = obj_session.query(CTableBOM).filter(CTableBOM.no.in_(lst_bom_nos)).all()
        dict_state = self.__build_version_state_map(lst_boms, n_query_timestamp)
        dict_boms = {(obj_bom.no, util_safe_int(obj_bom.version)): obj_bom for obj_bom in lst_boms}
        lst_results = []
        for str_bom_no, n_bom_version in sorted(set(lst_bom_keys)):
            obj_bom = dict_boms.get((str_bom_no, n_bom_version))
            if not obj_bom:
                continue
            lst_results.append({
                "bomNo": str_bom_no,
                "bomVersion": n_bom_version,
                "bomName": obj_bom.displayName or "",
                "versionStateCode": dict_state.get((str_bom_no, n_bom_version), EBomVersionState.UNKNOWN),
                "dateTimestamp": util_safe_int(obj_bom.date),
            })
        return lst_results

    def __load_structure_item_map(self, obj_session):
        dict_items = {}
        for obj_row in obj_session.query(CTableMaterial).all():
            dict_items[obj_row.no] = {
                "itemName": obj_row.name or "",
                "itemCategory": util_safe_int(obj_row.category),
                "itemSubCategory": util_safe_int(obj_row.subCategory),
            }
        for obj_row in obj_session.query(CTableInproduct).all():
            dict_items[obj_row.no] = {
                "itemName": obj_row.name or "",
                "itemCategory": EItemCategory.INPRODUCT,
                "itemSubCategory": util_safe_int(obj_row.category),
            }
        for obj_row in obj_session.query(CTableProduct).all():
            dict_items[obj_row.no] = {
                "itemName": obj_row.name or "",
                "itemCategory": EItemCategory.PRODUCT,
                "itemSubCategory": util_safe_int(obj_row.category),
            }
        for obj_row in obj_session.query(CTableGoods).all():
            dict_items[obj_row.no] = {
                "itemName": obj_row.name or "",
                "itemCategory": EItemCategory.GOODS,
                "itemSubCategory": util_safe_int(obj_row.subCategory),
            }
        return dict_items

    def __resolve_item_category(self, dict_item_map, str_item_no):
        return util_safe_int(dict_item_map.get(str_item_no or "", {}).get("itemCategory"))

    def __structure_node_type_code(self, n_item_category):
        return {
            EItemCategory.PM: "material",
            EItemCategory.MA: "material",
            EItemCategory.AF: "material",
            EItemCategory.INPRODUCT: "inproduct",
            EItemCategory.PRODUCT: "product",
            EItemCategory.GOODS: "goods",
        }.get(util_safe_int(n_item_category), "item")

    def __is_self_product_structure_row(self, str_product_no, obj_spec):
        return (
            util_safe_int(obj_spec.item_type) == 2
            and (obj_spec.item_no or "") == str_product_no
            and (obj_spec.product_no or "") == "%s_1" % str_product_no
        )

    def __product_structure_status_code(self, lst_children, lst_warnings):
        if not lst_children:
            return EProductStructureStatusCode.MISSING
        if lst_warnings:
            return EProductStructureStatusCode.PARTIAL
        return EProductStructureStatusCode.COMPLETE

    def __append_structure_warning(self, lst_warnings, str_warning_code, str_node_id, str_ref_no):
        dict_warning = {
            "warningCode": str_warning_code or EProductStructureWarningCode.UNKNOWN,
            "nodeId": str_node_id or "",
            "refNo": str_ref_no or "",
        }
        str_key = "%s|%s|%s" % (
            dict_warning["warningCode"],
            dict_warning["nodeId"],
            dict_warning["refNo"],
        )
        for dict_row in lst_warnings:
            if "%s|%s|%s" % (
                dict_row.get("warningCode", ""),
                dict_row.get("nodeId", ""),
                dict_row.get("refNo", ""),
            ) == str_key:
                return
        lst_warnings.append(dict_warning)


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


class CProductStructure(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CBomCenterService().get_product_structure(
                str_product_no=str_id,
                n_product_version=request.args.get("productVersion", 0, type=int),
                n_depth=request.args.get("depth", 3, type=int),
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
            CLogger().log(CLogger.LOG_LEVELERROR, "[CProductStructure] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data
