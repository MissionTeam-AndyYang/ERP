# coding=utf8
import time
from collections import defaultdict

from flask import request

from package.common.common import EErrorCode, EItemCategory
from package.dbwrapper.dbmgr import CDBMgr
from package.dbwrapper.table import (
    CTableBOM2,
    CTableBOM2Number,
    CTableInproduct,
    CTableProduct,
    CTableProductBOMSpec,
    CTableProductSpec,
)
from package.log.log import CLogger
from package.util.util import util_round_quantity, util_safe_float, util_safe_int


class CPackagingSpecificationStatusCode(object):
    COMPLETE = "complete"
    PARTIAL = "partial"
    UNAVAILABLE = "unavailable"
    ERROR = "error"


class CPackagingSpecificationSourceCode(object):
    PRODUCT = "product"
    INPRODUCT = "inproduct"
    PRODUCT_BOM_SPEC = "product_bom_spec"
    BOM2_NUMBER = "bom2_number"
    BOM2 = "bom2"
    PRODUCT_SPEC = "product_spec"
    NOT_RECORDED = "not_recorded"


class CPackagingSpecificationWarningCode(object):
    MISSING_PACKAGING_SPEC = "missing_packaging_spec"
    MISSING_PACKAGING_BOM_MASTER = "missing_packaging_bom_master"
    MISSING_PACKAGING_BOM_LINES = "missing_packaging_bom_lines"
    WIP_PACKAGING_CONTEXT_FROM_DOWNSTREAM_PRODUCT = "wip_packaging_context_from_downstream_product"
    MODULE_UNAVAILABLE = "module_unavailable"


class CPackagingSpecificationOverview(object):
    def get(self, str_timezone, str_id):
        str_item_no = (request.args.get("itemNo") or "").strip()
        n_item_category = util_safe_int(request.args.get("itemCategory"))
        n_product_version = util_safe_int(request.args.get("productVersion"))
        n_effective_date = util_safe_int(request.args.get("effectiveDate"))

        if not str_item_no:
            return 400, EErrorCode.ERROR_INVAILD_PARAM, "itemNo is required", {}
        if n_item_category not in (EItemCategory.INPRODUCT, EItemCategory.PRODUCT):
            return 400, EErrorCode.ERROR_INVAILD_PARAM, "invalid itemCategory", {}

        try:
            dict_payload = CPackagingSpecificationService().get_overview(
                str_item_no=str_item_no,
                n_item_category=n_item_category,
                n_product_version=n_product_version,
                n_effective_date=n_effective_date,
                str_timezone=str_timezone,
            )
            if not dict_payload:
                return 404, EErrorCode.ERROR_NO_MORE_ITEMS, "record not found", {}
            return 200, EErrorCode.ERROR_SUCCESS, "success", dict_payload
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, "[CPackagingSpecificationOverview] throw exception (error: %s)" % str(error))
            return 400, EErrorCode.ERROR_OTHER_ERROR, "throw exception (error: %s)" % str(error), {}


class CPackagingSpecificationService(object):
    def get_overview(
        self,
        str_item_no,
        n_item_category,
        n_product_version=0,
        n_effective_date=0,
        str_timezone="",
    ):
        with CDBMgr() as obj_dbmgr:
            return self.__get_overview_with_session(
                obj_dbmgr.get_session(),
                str_item_no,
                n_item_category,
                n_product_version,
                n_effective_date,
                str_timezone,
            )

    def __get_overview_with_session(
        self,
        obj_session,
        str_item_no,
        n_item_category,
        n_product_version=0,
        n_effective_date=0,
        str_timezone="",
    ):
        str_item_no = (str_item_no or "").strip()
        n_item_category = util_safe_int(n_item_category)
        n_effective_date = util_safe_int(n_effective_date) or util_safe_int(time.time())
        dict_subject = self.__query_subject(obj_session, str_item_no, n_item_category)
        if not dict_subject:
            return None
        n_product_version = util_safe_int(n_product_version) or util_safe_int(dict_subject.get("productVersion"))

        try:
            lst_specs, lst_warnings, str_source_code = self.__query_packaging_specs(
                obj_session,
                str_item_no,
                n_item_category,
                n_product_version,
            )
            str_status_code = self.__status_code(lst_specs, lst_warnings)
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, "[CPackagingSpecificationService] module error (error: %s)" % str(error))
            lst_specs = []
            lst_warnings = [self.__warning(CPackagingSpecificationWarningCode.MODULE_UNAVAILABLE, str_item_no)]
            str_source_code = CPackagingSpecificationSourceCode.NOT_RECORDED
            str_status_code = CPackagingSpecificationStatusCode.ERROR

        return {
            "serverTimestamp": util_safe_int(time.time()),
            "timezone": str_timezone or "UTC",
            "requestIdentity": {
                "itemNo": str_item_no,
                "itemCategory": n_item_category,
                "productVersion": n_product_version,
                "effectiveDate": n_effective_date,
            },
            "subject": dict_subject,
            "summary": self.__summary(lst_specs),
            "packagingSpecs": lst_specs,
            "sourceLineage": {
                "subjectSourceCode": dict_subject.get("sourceCode", ""),
                "packagingSpecSourceCode": str_source_code,
                "packagingBomMasterSourceCode": CPackagingSpecificationSourceCode.BOM2_NUMBER,
                "packagingBomLineSourceCode": CPackagingSpecificationSourceCode.BOM2,
            },
            "warnings": lst_warnings,
            "moduleReadiness": [{
                "moduleCode": "packagingSpecification",
                "statusCode": str_status_code,
                "sourceCode": str_source_code,
                "warningCodes": [
                    dict_warning.get("warningCode", "")
                    for dict_warning in lst_warnings
                    if dict_warning.get("warningCode")
                ],
            }],
            "capabilityBoundary": self.__capability_boundary(),
        }

    def __query_subject(self, obj_session, str_item_no, n_item_category):
        obj_model = CTableProduct if n_item_category == EItemCategory.PRODUCT else CTableInproduct
        obj_row = obj_session.query(obj_model).filter(obj_model.no == str_item_no).first()
        if not obj_row:
            return None
        return {
            "itemNo": obj_row.no or "",
            "itemName": obj_row.name or "",
            "itemCategory": n_item_category,
            "itemSubCategory": util_safe_int(obj_row.category),
            "productVersion": util_safe_int(getattr(obj_row, "version", 0)),
            "unitShipping": util_safe_int(obj_row.unitShipping),
            "unitWarehouse": util_safe_int(obj_row.unitWarehouse),
            "unitProduct": util_safe_int(obj_row.unitProduct),
            "comment": obj_row.comment or "",
            "sourceCode": CPackagingSpecificationSourceCode.PRODUCT if n_item_category == EItemCategory.PRODUCT else CPackagingSpecificationSourceCode.INPRODUCT,
        }

    def __query_packaging_specs(self, obj_session, str_item_no, n_item_category, n_product_version):
        lst_warnings = []
        if n_item_category == EItemCategory.PRODUCT:
            lst_specs = self.__query_product_packaging_specs(obj_session, str_item_no, n_product_version, "")
            if not lst_specs:
                lst_warnings.append(self.__warning(CPackagingSpecificationWarningCode.MISSING_PACKAGING_SPEC, str_item_no))
            lst_warnings.extend(self.__warnings_for_specs(lst_specs))
            return lst_specs, lst_warnings, CPackagingSpecificationSourceCode.PRODUCT_BOM_SPEC if lst_specs else CPackagingSpecificationSourceCode.NOT_RECORDED

        lst_product_refs = self.__query_downstream_products_for_wip(obj_session, str_item_no)
        for dict_ref in lst_product_refs:
            lst_warnings.append(self.__warning(
                CPackagingSpecificationWarningCode.WIP_PACKAGING_CONTEXT_FROM_DOWNSTREAM_PRODUCT,
                dict_ref.get("productNo", ""),
            ))
        lst_specs = []
        for dict_ref in lst_product_refs:
            lst_specs.extend(self.__query_product_packaging_specs(
                obj_session,
                dict_ref.get("productNo", ""),
                util_safe_int(dict_ref.get("productVersion")),
                str_item_no,
            ))
        if not lst_specs:
            lst_warnings.append(self.__warning(CPackagingSpecificationWarningCode.MISSING_PACKAGING_SPEC, str_item_no))
        lst_warnings.extend(self.__warnings_for_specs(lst_specs))
        return lst_specs, lst_warnings, CPackagingSpecificationSourceCode.PRODUCT_SPEC if lst_specs else CPackagingSpecificationSourceCode.NOT_RECORDED

    def __query_product_packaging_specs(self, obj_session, str_product_no, n_product_version, str_wip_no):
        if not str_product_no:
            return []
        obj_query = obj_session.query(CTableProductBOMSpec).filter(CTableProductBOMSpec.product_no == str_product_no)
        if util_safe_int(n_product_version):
            obj_query = obj_query.filter(CTableProductBOMSpec.product_version == util_safe_int(n_product_version))
        lst_rows = obj_query.order_by(
            CTableProductBOMSpec.product_version.desc(),
            CTableProductBOMSpec.level.asc(),
            CTableProductBOMSpec.id.asc(),
        ).all()
        lst_bom_nos = [obj_row.bom2_no for obj_row in lst_rows if obj_row.bom2_no]
        dict_masters = self.__query_bom2_masters(obj_session, lst_bom_nos)
        dict_lines = self.__query_bom2_lines(obj_session, lst_bom_nos)
        return [
            self.__packaging_spec_to_dict(obj_row, dict_masters, dict_lines, str_wip_no)
            for obj_row in lst_rows
        ]

    def __query_downstream_products_for_wip(self, obj_session, str_wip_no):
        lst_refs = []
        lst_rows = (
            obj_session.query(CTableProductSpec)
            .filter(CTableProductSpec.item_no == str_wip_no)
            .order_by(CTableProductSpec.product_no.asc(), CTableProductSpec.product_version.desc())
            .all()
        )
        set_seen = set()
        for obj_row in lst_rows:
            str_product_no = self.__normalize_product_no(obj_row.product_no or "")
            tpl_key = (str_product_no, util_safe_int(obj_row.product_version))
            if not str_product_no or tpl_key in set_seen:
                continue
            set_seen.add(tpl_key)
            lst_refs.append({
                "productNo": str_product_no,
                "productVersion": util_safe_int(obj_row.product_version),
            })
        return lst_refs

    def __normalize_product_no(self, str_product_no):
        if str_product_no.endswith("_1"):
            return str_product_no[:-2]
        return str_product_no

    def __query_bom2_masters(self, obj_session, lst_bom_nos):
        lst_bom_nos = [str_no for str_no in lst_bom_nos if str_no]
        if not lst_bom_nos:
            return {}
        return {
            obj_row.no: obj_row
            for obj_row in obj_session.query(CTableBOM2Number).filter(CTableBOM2Number.no.in_(lst_bom_nos)).all()
        }

    def __query_bom2_lines(self, obj_session, lst_bom_nos):
        lst_bom_nos = [str_no for str_no in lst_bom_nos if str_no]
        if not lst_bom_nos:
            return {}
        dict_result = defaultdict(list)
        lst_rows = (
            obj_session.query(CTableBOM2)
            .filter(CTableBOM2.parent_no.in_(lst_bom_nos))
            .order_by(CTableBOM2.parent_no.asc(), CTableBOM2.id.asc())
            .all()
        )
        for obj_row in lst_rows:
            dict_result[obj_row.parent_no or ""].append(self.__bom2_line_to_dict(obj_row))
        return dict_result

    def __packaging_spec_to_dict(self, obj_row, dict_masters, dict_lines, str_wip_no):
        str_bom_no = obj_row.bom2_no or ""
        obj_master = dict_masters.get(str_bom_no)
        lst_lines = dict_lines.get(str_bom_no, [])
        return {
            "specId": "%s:%s:%s" % (obj_row.product_no or "", util_safe_int(obj_row.product_version), str_bom_no),
            "productNo": obj_row.product_no or "",
            "productVersion": util_safe_int(obj_row.product_version),
            "wipNo": str_wip_no or "",
            "packagingLevel": util_safe_int(obj_row.level),
            "packagingBomNo": str_bom_no,
            "packagingBomName": obj_master.displayName if obj_master else "",
            "count": util_safe_int(obj_row.count),
            "unit": util_safe_int(obj_row.unit),
            "weight": util_round_quantity(obj_row.weight),
            "masterUnit": util_safe_int(obj_master.unit) if obj_master else 0,
            "masterWeight": util_round_quantity(obj_master.weight) if obj_master else 0.0,
            "linkedBomNo": obj_master.bom_no if obj_master else "",
            "linkedBomVersion": util_safe_int(obj_master.bom_version) if obj_master else 0,
            "lineCount": len(lst_lines),
            "lines": lst_lines,
            "sourceCode": CPackagingSpecificationSourceCode.PRODUCT_BOM_SPEC,
            "masterSourceCode": CPackagingSpecificationSourceCode.BOM2_NUMBER if obj_master else CPackagingSpecificationSourceCode.NOT_RECORDED,
            "lineSourceCode": CPackagingSpecificationSourceCode.BOM2 if lst_lines else CPackagingSpecificationSourceCode.NOT_RECORDED,
        }

    def __bom2_line_to_dict(self, obj_row):
        return {
            "parentBomNo": obj_row.parent_no or "",
            "parentBomName": obj_row.parent_name or "",
            "childCategory": util_safe_int(obj_row.child_category),
            "childNo": obj_row.child_id or "",
            "childName": obj_row.child_name or "",
            "childUnit": util_safe_int(obj_row.childUnit),
            "count": util_safe_int(obj_row.count),
            "childUnit2": util_safe_int(obj_row.childUnit2),
            "weight": util_round_quantity(obj_row.weight),
            "length": util_round_quantity(obj_row.length),
            "expectedLoss": util_round_quantity(obj_row.expectedLoss),
            "actualLoss": util_round_quantity(obj_row.actualLoss),
            "processCount": util_round_quantity(obj_row.processCount),
            "comment": obj_row.comment or "",
        }

    def __summary(self, lst_specs):
        return {
            "packagingSpecCount": len(lst_specs),
            "packagingBomCount": len({dict_row.get("packagingBomNo") for dict_row in lst_specs if dict_row.get("packagingBomNo")}),
            "packageLevelCount": len({util_safe_int(dict_row.get("packagingLevel")) for dict_row in lst_specs if util_safe_int(dict_row.get("packagingLevel"))}),
            "materialLineCount": sum(util_safe_int(dict_row.get("lineCount")) for dict_row in lst_specs),
            "totalCount": sum(util_safe_int(dict_row.get("count")) for dict_row in lst_specs),
            "totalWeight": util_round_quantity(sum(util_safe_float(dict_row.get("weight")) for dict_row in lst_specs)),
        }

    def __warnings_for_specs(self, lst_specs):
        lst_warnings = []
        set_seen = set()
        for dict_spec in lst_specs:
            str_bom_no = dict_spec.get("packagingBomNo", "")
            if dict_spec.get("masterSourceCode") == CPackagingSpecificationSourceCode.NOT_RECORDED:
                tpl_key = (CPackagingSpecificationWarningCode.MISSING_PACKAGING_BOM_MASTER, str_bom_no)
                if tpl_key not in set_seen:
                    lst_warnings.append(self.__warning(CPackagingSpecificationWarningCode.MISSING_PACKAGING_BOM_MASTER, str_bom_no))
                    set_seen.add(tpl_key)
            if dict_spec.get("lineSourceCode") == CPackagingSpecificationSourceCode.NOT_RECORDED:
                tpl_key = (CPackagingSpecificationWarningCode.MISSING_PACKAGING_BOM_LINES, str_bom_no)
                if tpl_key not in set_seen:
                    lst_warnings.append(self.__warning(CPackagingSpecificationWarningCode.MISSING_PACKAGING_BOM_LINES, str_bom_no))
                    set_seen.add(tpl_key)
        return lst_warnings

    def __status_code(self, lst_specs, lst_warnings):
        if not lst_specs:
            return CPackagingSpecificationStatusCode.UNAVAILABLE
        if lst_warnings or any(
            dict_row.get("masterSourceCode") == CPackagingSpecificationSourceCode.NOT_RECORDED
            or dict_row.get("lineSourceCode") == CPackagingSpecificationSourceCode.NOT_RECORDED
            for dict_row in lst_specs
        ):
            return CPackagingSpecificationStatusCode.PARTIAL
        return CPackagingSpecificationStatusCode.COMPLETE

    def __warning(self, str_warning_code, str_ref_no):
        return {
            "moduleCode": "packagingSpecification",
            "warningCode": str_warning_code,
            "refNo": str_ref_no or "",
        }

    def __capability_boundary(self):
        return {
            "readOnly": True,
            "packagingWriteSupported": False,
            "packagingApprovalSupported": False,
            "packagingReleaseSupported": False,
            "sourceOfTruthTransitionSupported": False,
            "cutoverSupported": False,
            "goLiveSupported": False,
        }
