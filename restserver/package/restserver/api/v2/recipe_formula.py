# coding=utf8
import time
from collections import defaultdict

from flask import request
from sqlalchemy import or_

from package.common.common import (
    EBomVersionState,
    EErrorCode,
    EItemCategory,
    ERecipeFormulaSourceCode,
    ERecipeFormulaStatusCode,
    ERecipeFormulaWarningCode,
)
from package.dbwrapper.dbmgr import CDBMgr
from package.dbwrapper.table import (
    CTableBOM,
    CTableBOMItem,
    CTableGoods,
    CTableInproduct,
    CTableMaterial,
    CTableProduct,
    CTableProductSpec,
)
from package.log.log import CLogger
from package.util.util import util_round_quantity, util_safe_int


class CRecipeFormulaService(object):
    def get_dashboard(self, str_keyword="", str_status_code="", n_start=0, n_count=50, n_effective_date=0):
        with CDBMgr() as obj_dbmgr:
            return self.__get_dashboard_with_session(
                obj_dbmgr.get_session(),
                str_keyword,
                str_status_code,
                n_start,
                n_count,
                n_effective_date,
            )

    def get_versions(self, str_recipe_no, n_effective_date=0):
        with CDBMgr() as obj_dbmgr:
            return self.__get_versions_with_session(
                obj_dbmgr.get_session(),
                str_recipe_no,
                n_effective_date,
            )

    def get_composition(self, str_recipe_no, n_version, n_effective_date=0):
        with CDBMgr() as obj_dbmgr:
            return self.__get_composition_with_session(
                obj_dbmgr.get_session(),
                str_recipe_no,
                n_version,
                n_effective_date,
            )

    def get_by_product(self, str_product_no, n_product_version=0, n_effective_date=0):
        with CDBMgr() as obj_dbmgr:
            return self.__get_by_product_with_session(
                obj_dbmgr.get_session(),
                str_product_no,
                n_product_version,
                n_effective_date,
            )

    def __get_dashboard_with_session(
        self,
        obj_session,
        str_keyword,
        str_status_code,
        n_start,
        n_count,
        n_effective_date,
    ):
        n_query_timestamp = util_safe_int(n_effective_date) or util_safe_int(time.time())
        n_start = max(util_safe_int(n_start), 0)
        n_count = min(max(util_safe_int(n_count), 1), 100)
        lst_boms = self.__query_boms(obj_session, str_keyword)
        dict_state = self.__build_version_state_map(lst_boms, n_query_timestamp)
        dict_input_counts = self.__load_input_counts(obj_session, [obj_bom.no for obj_bom in lst_boms])
        dict_output_counts = self.__load_output_counts(obj_session, [(obj_bom.no, util_safe_int(obj_bom.version)) for obj_bom in lst_boms])
        lst_rows = [
            self.__build_dashboard_row(
                obj_bom,
                dict_state.get((obj_bom.no, obj_bom.version), EBomVersionState.UNKNOWN),
                dict_input_counts,
                dict_output_counts,
            )
            for obj_bom in lst_boms
        ]
        if str_status_code:
            lst_rows = [dict_row for dict_row in lst_rows if dict_row.get("formulaStatusCode") == str_status_code]
        lst_rows = sorted(
            lst_rows,
            key=lambda dict_row: (
                dict_row.get("recipeNo", ""),
                -util_safe_int(dict_row.get("recipeVersion")),
            ),
        )
        n_total = len(lst_rows)
        lst_page = lst_rows[n_start:n_start + n_count]
        return {
            "serverTimestamp": util_safe_int(time.time()),
            "summary": self.__build_summary(lst_rows),
            "recipes": lst_page,
            "capabilityBoundary": self.__capability_boundary(),
            "total": n_total,
            "start": n_start,
            "count": len(lst_page),
        }

    def __get_versions_with_session(self, obj_session, str_recipe_no, n_effective_date):
        str_recipe_no = (str_recipe_no or "").strip()
        if not str_recipe_no:
            return None
        n_query_timestamp = util_safe_int(n_effective_date) or util_safe_int(time.time())
        lst_boms = obj_session.query(CTableBOM).filter(CTableBOM.no == str_recipe_no).all()
        if not lst_boms:
            return None
        dict_state = self.__build_version_state_map(lst_boms, n_query_timestamp)
        return {
            "serverTimestamp": util_safe_int(time.time()),
            "recipe": self.__build_recipe_header(lst_boms[0]),
            "versions": [
                self.__build_version_row(
                    obj_bom,
                    dict_state.get((obj_bom.no, obj_bom.version), EBomVersionState.UNKNOWN),
                )
                for obj_bom in sorted(lst_boms, key=lambda obj_row: -util_safe_int(obj_row.version))
            ],
            "capabilityBoundary": self.__capability_boundary(),
        }

    def __get_composition_with_session(self, obj_session, str_recipe_no, n_version, n_effective_date):
        str_recipe_no = (str_recipe_no or "").strip()
        n_version = util_safe_int(n_version)
        if not str_recipe_no or n_version <= 0:
            return None
        n_query_timestamp = util_safe_int(n_effective_date) or util_safe_int(time.time())
        obj_bom = (
            obj_session.query(CTableBOM)
            .filter(CTableBOM.no == str_recipe_no, CTableBOM.version == n_version)
            .first()
        )
        if not obj_bom:
            return None
        lst_boms = obj_session.query(CTableBOM).filter(CTableBOM.no == str_recipe_no).all()
        dict_state = self.__build_version_state_map(lst_boms, n_query_timestamp)
        dict_item_map = self.__load_item_map(obj_session)
        lst_inputs = self.__build_inputs(obj_session, obj_bom, dict_item_map)
        lst_output_candidates = self.__build_output_candidates(obj_session, obj_bom)
        lst_warnings = self.__build_formula_warnings(obj_bom, lst_inputs, lst_output_candidates)
        dict_output = self.__select_formula_output(lst_output_candidates)
        return {
            "serverTimestamp": util_safe_int(time.time()),
            "recipe": self.__build_recipe_header(obj_bom),
            "version": self.__build_version_row(
                obj_bom,
                dict_state.get((obj_bom.no, obj_bom.version), EBomVersionState.UNKNOWN),
            ),
            "formula": {
                "recipeNo": obj_bom.no or "",
                "recipeVersion": util_safe_int(obj_bom.version),
                "formulaStatusCode": self.__formula_status_code(lst_inputs, lst_output_candidates, lst_warnings),
                "weight": util_round_quantity(obj_bom.weight),
                "unit": util_safe_int(obj_bom.unit),
                "weightSourceCode": ERecipeFormulaSourceCode.BOM,
            },
            "inputs": lst_inputs,
            "output": dict_output,
            "sourceLineage": self.__source_lineage(obj_bom, dict_output),
            "capabilityBoundary": self.__capability_boundary(),
            "warnings": lst_warnings,
        }

    def __get_by_product_with_session(self, obj_session, str_product_no, n_product_version, n_effective_date):
        str_product_no = (str_product_no or "").strip()
        if not str_product_no:
            return None
        n_product_version = util_safe_int(n_product_version)
        obj_query = obj_session.query(CTableProductSpec).filter(
            or_(
                CTableProductSpec.product_no == str_product_no,
                CTableProductSpec.product_no == "%s_1" % str_product_no,
            )
        )
        if n_product_version > 0:
            obj_query = obj_query.filter(CTableProductSpec.product_version == n_product_version)
        lst_specs = obj_query.order_by(CTableProductSpec.product_version.desc(), CTableProductSpec.bom_no.asc()).all()
        if not lst_specs:
            return None
        lst_keys = sorted({
            (obj_row.bom_no, util_safe_int(obj_row.bom_version))
            for obj_row in lst_specs
            if obj_row.bom_no and util_safe_int(obj_row.bom_version) > 0
        })
        return {
            "serverTimestamp": util_safe_int(time.time()),
            "productNo": str_product_no,
            "productVersion": n_product_version,
            "recipeVersions": [
                self.__get_composition_with_session(obj_session, str_recipe_no, n_version, n_effective_date)
                for str_recipe_no, n_version in lst_keys
            ],
            "capabilityBoundary": self.__capability_boundary(),
        }

    def __query_boms(self, obj_session, str_keyword):
        obj_query = obj_session.query(CTableBOM)
        str_keyword = (str_keyword or "").strip()
        if str_keyword:
            str_like = "%%%s%%" % str_keyword
            obj_query = obj_query.filter(or_(CTableBOM.no.ilike(str_like), CTableBOM.displayName.ilike(str_like)))
        return obj_query.all()

    def __build_version_state_map(self, lst_boms, n_query_timestamp):
        dict_effective_version_by_no = {}
        for obj_bom in lst_boms:
            n_date = util_safe_int(obj_bom.date)
            if n_date > 0 and n_date <= n_query_timestamp:
                n_version = util_safe_int(obj_bom.version)
                if n_version > dict_effective_version_by_no.get(obj_bom.no or "", 0):
                    dict_effective_version_by_no[obj_bom.no or ""] = n_version
        dict_state = {}
        for obj_bom in lst_boms:
            n_date = util_safe_int(obj_bom.date)
            n_version = util_safe_int(obj_bom.version)
            if n_date <= 0:
                str_state = EBomVersionState.UNKNOWN
            elif n_date > n_query_timestamp:
                str_state = EBomVersionState.FUTURE
            elif n_version == dict_effective_version_by_no.get(obj_bom.no or "", 0):
                str_state = EBomVersionState.EFFECTIVE
            else:
                str_state = EBomVersionState.HISTORICAL
            dict_state[(obj_bom.no, obj_bom.version)] = str_state
        return dict_state

    def __load_input_counts(self, obj_session, lst_recipe_nos):
        lst_recipe_nos = list({str_no for str_no in lst_recipe_nos or [] if str_no})
        if not lst_recipe_nos:
            return {}
        dict_counts = defaultdict(int)
        for obj_row in obj_session.query(CTableBOMItem).filter(CTableBOMItem.bom_no.in_(lst_recipe_nos)).all():
            dict_counts[obj_row.bom_no or ""] += 1
        return dict_counts

    def __load_output_counts(self, obj_session, lst_recipe_keys):
        set_recipe_keys = set(lst_recipe_keys or [])
        if not set_recipe_keys:
            return {}
        lst_recipe_nos = list({str_recipe_no for str_recipe_no, _ in set_recipe_keys if str_recipe_no})
        dict_counts = defaultdict(set)
        for obj_row in obj_session.query(CTableProductSpec).filter(CTableProductSpec.bom_no.in_(lst_recipe_nos)).all():
            tuple_key = (obj_row.bom_no, util_safe_int(obj_row.bom_version))
            if tuple_key in set_recipe_keys and obj_row.product_no:
                dict_counts[tuple_key].add(self.__normalize_product_no(obj_row.product_no))
        return {
            tuple_key: len(set_values)
            for tuple_key, set_values in dict_counts.items()
        }

    def __build_dashboard_row(self, obj_bom, str_version_state_code, dict_input_counts, dict_output_counts):
        n_input_count = util_safe_int(dict_input_counts.get(obj_bom.no or "", 0))
        n_output_count = util_safe_int(dict_output_counts.get((obj_bom.no, util_safe_int(obj_bom.version)), 0))
        lst_warnings = self.__build_row_warnings(obj_bom, n_input_count, n_output_count)
        return {
            "recipeNo": obj_bom.no or "",
            "recipeName": obj_bom.displayName or "",
            "recipeVersion": util_safe_int(obj_bom.version),
            "versionStateCode": str_version_state_code,
            "formulaStatusCode": self.__formula_status_code_by_counts(n_input_count, n_output_count, lst_warnings),
            "inputCount": n_input_count,
            "outputCount": n_output_count,
            "weight": util_round_quantity(obj_bom.weight),
            "unit": util_safe_int(obj_bom.unit),
            "dateTimestamp": util_safe_int(obj_bom.date),
            "warningCodes": [dict_warning.get("warningCode", "") for dict_warning in lst_warnings],
        }

    def __build_summary(self, lst_rows):
        return {
            "recipeCount": len({dict_row.get("recipeNo", "") for dict_row in lst_rows if dict_row.get("recipeNo")}),
            "versionCount": len(lst_rows),
            "completeFormulaCount": len([dict_row for dict_row in lst_rows if dict_row.get("formulaStatusCode") == ERecipeFormulaStatusCode.COMPLETE]),
            "partialFormulaCount": len([dict_row for dict_row in lst_rows if dict_row.get("formulaStatusCode") == ERecipeFormulaStatusCode.PARTIAL]),
            "missingFormulaCount": len([dict_row for dict_row in lst_rows if dict_row.get("formulaStatusCode") == ERecipeFormulaStatusCode.MISSING]),
        }

    def __build_recipe_header(self, obj_bom):
        return {
            "recipeNo": obj_bom.no or "",
            "recipeName": obj_bom.displayName or "",
            "recipeSourceCode": ERecipeFormulaSourceCode.BOM,
        }

    def __build_version_row(self, obj_bom, str_version_state_code):
        return {
            "recipeNo": obj_bom.no or "",
            "recipeVersion": util_safe_int(obj_bom.version),
            "versionStateCode": str_version_state_code,
            "dateTimestamp": util_safe_int(obj_bom.date),
            "weight": util_round_quantity(obj_bom.weight),
            "unit": util_safe_int(obj_bom.unit),
        }

    def __build_inputs(self, obj_session, obj_bom, dict_item_map):
        lst_rows = (
            obj_session.query(CTableBOMItem)
            .filter(CTableBOMItem.bom_no == obj_bom.no)
            .order_by(CTableBOMItem.item_no.asc(), CTableBOMItem.id.asc())
            .all()
        )
        return [
            {
                "inputNo": obj_row.item_no or "",
                "inputName": dict_item_map.get(obj_row.item_no or "", {}).get("itemName", obj_row.item_name or ""),
                "inputCategory": util_safe_int(dict_item_map.get(obj_row.item_no or "", {}).get("itemCategory")),
                "inputSubCategory": util_safe_int(dict_item_map.get(obj_row.item_no or "", {}).get("itemSubCategory")),
                "quantity": 0,
                "weight": util_round_quantity(obj_row.weight),
                "unit": util_safe_int(obj_row.unit),
                "lossRate": 0.0,
                "lossSourceCode": ERecipeFormulaSourceCode.NOT_RECORDED,
                "weightSourceCode": ERecipeFormulaSourceCode.BOM_ITEM,
            }
            for obj_row in lst_rows
        ]

    def __build_output_candidates(self, obj_session, obj_bom):
        dict_products = {
            obj_row.no: obj_row
            for obj_row in obj_session.query(CTableProduct).all()
        }
        dict_candidates = {}
        lst_rows = (
            obj_session.query(CTableProductSpec)
            .filter(
                CTableProductSpec.bom_no == obj_bom.no,
                CTableProductSpec.bom_version == util_safe_int(obj_bom.version),
            )
            .order_by(CTableProductSpec.product_no.asc(), CTableProductSpec.product_version.asc())
            .all()
        )
        for obj_row in lst_rows:
            str_product_no = self.__normalize_product_no(obj_row.product_no)
            if not str_product_no or str_product_no in dict_candidates:
                continue
            obj_product = dict_products.get(str_product_no)
            dict_candidates[str_product_no] = {
                "outputNo": str_product_no,
                "outputName": getattr(obj_product, "name", "") or "",
                "outputCategory": EItemCategory.PRODUCT,
                "productVersion": util_safe_int(obj_row.product_version),
                "quantity": 1,
                "weight": util_round_quantity(obj_bom.weight),
                "unit": util_safe_int(obj_bom.unit),
                "weightSourceCode": ERecipeFormulaSourceCode.BOM,
                "sourceCode": ERecipeFormulaSourceCode.PRODUCT_SPEC,
            }
        return [dict_candidates[str_key] for str_key in sorted(dict_candidates.keys())]

    def __select_formula_output(self, lst_output_candidates):
        if not lst_output_candidates:
            return {
                "outputNo": "",
                "outputName": "",
                "outputCategory": 0,
                "productVersion": 0,
                "quantity": 0,
                "weight": 0.0,
                "unit": 0,
                "weightSourceCode": ERecipeFormulaSourceCode.NOT_RECORDED,
                "sourceCode": ERecipeFormulaSourceCode.NOT_RECORDED,
            }
        return lst_output_candidates[0]

    def __source_lineage(self, obj_bom, dict_output):
        return {
            "recipeSourceCode": ERecipeFormulaSourceCode.BOM,
            "inputSourceCode": ERecipeFormulaSourceCode.BOM_ITEM,
            "outputSourceCode": dict_output.get("sourceCode", ERecipeFormulaSourceCode.NOT_RECORDED),
            "productStructureReference": {
                "productNo": dict_output.get("outputNo", ""),
                "productVersion": util_safe_int(dict_output.get("productVersion")),
                "bomNo": obj_bom.no or "",
                "bomVersion": util_safe_int(obj_bom.version),
            },
            "routingContextRefs": [],
            "productionObservationRefs": [],
        }

    def __build_formula_warnings(self, obj_bom, lst_inputs, lst_output_candidates):
        lst_warnings = []
        if not lst_inputs:
            self.__append_warning(lst_warnings, ERecipeFormulaWarningCode.MISSING_INPUTS, obj_bom.no or "")
        if not lst_output_candidates:
            self.__append_warning(lst_warnings, ERecipeFormulaWarningCode.MISSING_OUTPUT, obj_bom.no or "")
        if len(lst_output_candidates) > 1:
            self.__append_warning(lst_warnings, ERecipeFormulaWarningCode.MULTIPLE_OUTPUTS, obj_bom.no or "")
        if util_round_quantity(obj_bom.weight) <= 0:
            self.__append_warning(lst_warnings, ERecipeFormulaWarningCode.MISSING_OUTPUT_WEIGHT, obj_bom.no or "")
        for dict_input in lst_inputs:
            if util_round_quantity(dict_input.get("weight")) <= 0:
                self.__append_warning(lst_warnings, ERecipeFormulaWarningCode.MISSING_INPUT_WEIGHT, dict_input.get("inputNo", ""))
            if dict_input.get("lossSourceCode") == ERecipeFormulaSourceCode.NOT_RECORDED:
                self.__append_warning(lst_warnings, ERecipeFormulaWarningCode.MISSING_LOSS_SOURCE, dict_input.get("inputNo", ""))
        return lst_warnings

    def __build_row_warnings(self, obj_bom, n_input_count, n_output_count):
        lst_warnings = []
        if n_input_count <= 0:
            self.__append_warning(lst_warnings, ERecipeFormulaWarningCode.MISSING_INPUTS, obj_bom.no or "")
        if n_output_count <= 0:
            self.__append_warning(lst_warnings, ERecipeFormulaWarningCode.MISSING_OUTPUT, obj_bom.no or "")
        if n_output_count > 1:
            self.__append_warning(lst_warnings, ERecipeFormulaWarningCode.MULTIPLE_OUTPUTS, obj_bom.no or "")
        if util_round_quantity(obj_bom.weight) <= 0:
            self.__append_warning(lst_warnings, ERecipeFormulaWarningCode.MISSING_OUTPUT_WEIGHT, obj_bom.no or "")
        return lst_warnings

    def __formula_status_code(self, lst_inputs, lst_output_candidates, lst_warnings):
        if not lst_inputs or not lst_output_candidates:
            return ERecipeFormulaStatusCode.MISSING
        if lst_warnings:
            return ERecipeFormulaStatusCode.PARTIAL
        return ERecipeFormulaStatusCode.COMPLETE

    def __formula_status_code_by_counts(self, n_input_count, n_output_count, lst_warnings):
        if n_input_count <= 0 or n_output_count <= 0:
            return ERecipeFormulaStatusCode.MISSING
        if lst_warnings:
            return ERecipeFormulaStatusCode.PARTIAL
        return ERecipeFormulaStatusCode.COMPLETE

    def __append_warning(self, lst_warnings, str_warning_code, str_ref_no):
        dict_warning = {
            "warningCode": str_warning_code or ERecipeFormulaWarningCode.UNKNOWN,
            "refNo": str_ref_no or "",
        }
        for dict_row in lst_warnings:
            if dict_row == dict_warning:
                return
        lst_warnings.append(dict_warning)

    def __load_item_map(self, obj_session):
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
        for obj_row in obj_session.query(CTableGoods).all():
            dict_items[obj_row.no] = {
                "itemName": obj_row.name or "",
                "itemCategory": EItemCategory.GOODS,
                "itemSubCategory": util_safe_int(obj_row.subCategory),
            }
        for obj_row in obj_session.query(CTableProduct).all():
            dict_items[obj_row.no] = {
                "itemName": obj_row.name or "",
                "itemCategory": EItemCategory.PRODUCT,
                "itemSubCategory": util_safe_int(obj_row.category),
            }
        return dict_items

    def __normalize_product_no(self, str_product_no):
        str_value = (str_product_no or "").strip()
        if str_value.endswith("_1"):
            return str_value[:-2]
        return str_value

    def __capability_boundary(self):
        return {
            "recipeWriteSupported": False,
            "bomWriteSupported": False,
            "productWriteSupported": False,
            "productStructureSeparated": True,
            "routingReferenceOnly": True,
            "productionObservationSeparated": True,
            "costingExcluded": True,
        }


class CRecipeFormulaDashboard(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CRecipeFormulaService().get_dashboard(
                str_keyword=request.args.get("keyword", "", type=str),
                str_status_code=request.args.get("formulaStatusCode", "", type=str),
                n_start=request.args.get("start", 0, type=int),
                n_count=request.args.get("count", 50, type=int),
                n_effective_date=request.args.get("effectiveDate", 0, type=int),
            )
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CRecipeFormulaDashboard] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CRecipeFormulaVersions(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CRecipeFormulaService().get_versions(
                str_recipe_no=str_id,
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
            CLogger().log(CLogger.LOG_LEVELERROR, "[CRecipeFormulaVersions] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CRecipeFormulaComposition(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            str_recipe_no, str_version = (str_id or "|").split("|", 1)
            dict_extra_data = CRecipeFormulaService().get_composition(
                str_recipe_no=str_recipe_no,
                n_version=util_safe_int(str_version),
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
            CLogger().log(CLogger.LOG_LEVELERROR, "[CRecipeFormulaComposition] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CRecipeFormulaByProduct(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CRecipeFormulaService().get_by_product(
                str_product_no=str_id,
                n_product_version=request.args.get("productVersion", 0, type=int),
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
            CLogger().log(CLogger.LOG_LEVELERROR, "[CRecipeFormulaByProduct] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data
