# coding=utf8
import time

from flask import request

from package.common.common import EErrorCode, EItemCategory
from package.dbwrapper.dbmgr import CDBMgr
from package.dbwrapper.table import CTableContract, CTableInproduct, CTableProduct, CTableTransItems
from package.log.log import CLogger
from package.restserver.api.v2.bom import CBomCenterService
from package.restserver.api.v2.items import CItemCenterService
from package.restserver.api.v2.recipe_formula import CRecipeFormulaService
from package.restserver.api.v2.routing import CRoutingProcessFlowService
from package.restserver.api.v2.warehouse import CWarehouseInventoryService
from package.util.util import util_round_amount, util_round_price, util_round_quantity, util_safe_float, util_safe_int


class CProductWip360ModuleCode(object):
    ITEM = "item"
    TRANSACTION_ITEM = "transactionItem"
    WAREHOUSE = "warehouse"
    BOM = "bom"
    RECIPE = "recipe"
    ROUTING = "routing"


class CProductWip360StatusCode(object):
    COMPLETE = "complete"
    PARTIAL = "partial"
    UNAVAILABLE = "unavailable"
    TEST_SUPPORT = "test_support"
    ERROR = "error"


class CProductWip360SourceCode(object):
    PRODUCT = "product"
    INPRODUCT = "inproduct"
    TRANS_ITEMS = "trans_items"
    CONTRACT = "contract"
    INVENTORY = "inventory_snapshot"
    PRODUCT_STRUCTURE = "product_structure"
    RECIPE_FORMULA = "recipe_formula"
    ROUTING = "routing_process_flow"
    NOT_RECORDED = "not_recorded"


class CProductWip360WarningCode(object):
    MODULE_UNAVAILABLE = "module_unavailable"
    PRODUCT_WRITE_NOT_SUPPORTED = "product_write_not_supported"
    WIP_STRUCTURE_NOT_GOVERNED = "wip_structure_not_governed"
    WIP_RECIPE_NOT_GOVERNED = "wip_recipe_not_governed"
    MISSING_TRANSACTION_ITEM = "missing_transaction_item"
    MISSING_WAREHOUSE_STOCK = "missing_warehouse_stock"
    TEST_SUPPORT_ONLY = "test_support_only"


class CProductWip360Overview(object):
    def get(self, str_timezone, str_id):
        str_item_no = (request.args.get("itemNo") or "").strip()
        n_item_category = util_safe_int(request.args.get("itemCategory"))
        n_effective_date = util_safe_int(request.args.get("effectiveDate"))
        n_inventory_date = util_safe_int(request.args.get("inventoryDate"))
        n_product_version = util_safe_int(request.args.get("productVersion"))
        lst_include_modules = self.__parse_include_modules(request.args.get("includeModules"))

        if not str_item_no:
            return 400, EErrorCode.ERROR_INVAILD_PARAM, "itemNo is required", {}
        if n_item_category not in (EItemCategory.INPRODUCT, EItemCategory.PRODUCT):
            return 400, EErrorCode.ERROR_INVAILD_PARAM, "invalid itemCategory", {}

        try:
            dict_payload = CProductWip360OverviewService().get_overview(
                str_item_no=str_item_no,
                n_item_category=n_item_category,
                n_effective_date=n_effective_date,
                n_inventory_date=n_inventory_date,
                n_product_version=n_product_version,
                lst_include_modules=lst_include_modules,
                str_timezone=str_timezone,
            )
            if not dict_payload:
                return 404, EErrorCode.ERROR_NO_MORE_ITEMS, "record not found", {}
            return 200, EErrorCode.ERROR_SUCCESS, "success", dict_payload
        except ValueError as error:
            return 400, EErrorCode.ERROR_INVAILD_PARAM, str(error), {}
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, "[CProductWip360Overview] throw exception (error: %s)" % str(error))
            return 400, EErrorCode.ERROR_OTHER_ERROR, "throw exception (error: %s)" % str(error), {}

    def __parse_include_modules(self, str_modules):
        lst_default = [
            CProductWip360ModuleCode.ITEM,
            CProductWip360ModuleCode.TRANSACTION_ITEM,
            CProductWip360ModuleCode.WAREHOUSE,
            CProductWip360ModuleCode.BOM,
            CProductWip360ModuleCode.RECIPE,
            CProductWip360ModuleCode.ROUTING,
        ]
        if not str_modules:
            return lst_default
        set_allowed = set(lst_default)
        lst_modules = []
        for str_module in str_modules.split(","):
            str_module = str_module.strip()
            if str_module and str_module in set_allowed:
                lst_modules.append(str_module)
        return lst_modules or lst_default


class CProductWip360OverviewService(object):
    def get_overview(
        self,
        str_item_no,
        n_item_category,
        n_effective_date=0,
        n_inventory_date=0,
        n_product_version=0,
        lst_include_modules=None,
        str_timezone="",
    ):
        with CDBMgr() as obj_dbmgr:
            return self.__get_overview_with_session(
                obj_dbmgr.get_session(),
                str_item_no,
                n_item_category,
                n_effective_date,
                n_inventory_date,
                n_product_version,
                lst_include_modules,
                str_timezone,
            )

    def __get_overview_with_session(
        self,
        obj_session,
        str_item_no,
        n_item_category,
        n_effective_date=0,
        n_inventory_date=0,
        n_product_version=0,
        lst_include_modules=None,
        str_timezone="",
    ):
        str_item_no = (str_item_no or "").strip()
        n_item_category = util_safe_int(n_item_category)
        n_effective_date = util_safe_int(n_effective_date) or util_safe_int(time.time())
        n_inventory_date = util_safe_int(n_inventory_date) or n_effective_date
        lst_include_modules = lst_include_modules or [
            CProductWip360ModuleCode.ITEM,
            CProductWip360ModuleCode.TRANSACTION_ITEM,
            CProductWip360ModuleCode.WAREHOUSE,
            CProductWip360ModuleCode.BOM,
            CProductWip360ModuleCode.RECIPE,
            CProductWip360ModuleCode.ROUTING,
        ]

        dict_subject = self.__query_subject(obj_session, str_item_no, n_item_category)
        if not dict_subject:
            return None
        if n_item_category == EItemCategory.PRODUCT and not n_product_version:
            n_product_version = util_safe_int(dict_subject.get("productVersion"))

        dict_payload = {
            "serverTimestamp": util_safe_int(time.time()),
            "timezone": str_timezone or "UTC",
            "requestIdentity": {
                "itemNo": str_item_no,
                "itemCategory": n_item_category,
                "effectiveDate": n_effective_date,
                "inventoryDate": n_inventory_date,
                "productVersion": n_product_version,
            },
            "effectiveDate": n_effective_date,
            "inventoryDate": n_inventory_date,
            "productVersion": n_product_version,
            "subject": dict_subject,
            "itemDetail": {},
            "transactionContext": {
                "linkedTransactionItemStatusCode": CProductWip360StatusCode.UNAVAILABLE,
                "transactionItems": [],
                "total": 0,
            },
            "inventoryOverview": self.__empty_inventory_overview(),
            "batchHighlights": [],
            "productStructure": {},
            "recipeFormula": {},
            "routingProcess": {},
            "moduleReadiness": [],
            "sourceLineage": {},
            "warnings": [],
            "capabilityBoundary": self.__capability_boundary(),
        }

        for str_module_code in lst_include_modules:
            self.__append_module(
                dict_payload,
                str_module_code,
                lambda str_code=str_module_code: self.__build_module(
                    obj_session,
                    str_code,
                    str_item_no,
                    n_item_category,
                    n_effective_date,
                    n_inventory_date,
                    n_product_version,
                    str_timezone,
                ),
            )
        return dict_payload

    def __query_subject(self, obj_session, str_item_no, n_item_category):
        obj_model = CTableProduct if n_item_category == EItemCategory.PRODUCT else CTableInproduct
        obj_row = obj_session.query(obj_model).filter(obj_model.no == str_item_no).first()
        if not obj_row:
            return None
        str_source_code = CProductWip360SourceCode.PRODUCT if n_item_category == EItemCategory.PRODUCT else CProductWip360SourceCode.INPRODUCT
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
            "sourceCode": str_source_code,
        }

    def __build_module(
        self,
        obj_session,
        str_module_code,
        str_item_no,
        n_item_category,
        n_effective_date,
        n_inventory_date,
        n_product_version,
        str_timezone,
    ):
        if str_module_code == CProductWip360ModuleCode.ITEM:
            return self.__build_item_module(str_item_no, n_inventory_date, str_timezone)
        if str_module_code == CProductWip360ModuleCode.TRANSACTION_ITEM:
            return self.__build_transaction_item_module(obj_session, str_item_no, n_item_category)
        if str_module_code == CProductWip360ModuleCode.WAREHOUSE:
            return self.__build_warehouse_module(str_item_no, n_item_category, n_inventory_date, str_timezone)
        if str_module_code == CProductWip360ModuleCode.BOM:
            return self.__build_bom_module(str_item_no, n_item_category, n_product_version, n_effective_date)
        if str_module_code == CProductWip360ModuleCode.RECIPE:
            return self.__build_recipe_module(str_item_no, n_item_category, n_product_version, n_effective_date)
        if str_module_code == CProductWip360ModuleCode.ROUTING:
            return self.__build_routing_module(str_item_no, n_effective_date)
        return self.__empty_module(str_module_code)

    def __append_module(self, dict_payload, str_module_code, fn_builder):
        try:
            dict_result = fn_builder()
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, "[CProductWip360OverviewService] module error (module: %s, error: %s)" % (str_module_code, str(error)))
            dict_result = {
                "moduleCode": str_module_code,
                "statusCode": CProductWip360StatusCode.ERROR,
                "sourceCode": CProductWip360SourceCode.NOT_RECORDED,
                "data": {},
                "warnings": [self.__warning(str_module_code, CProductWip360WarningCode.MODULE_UNAVAILABLE, "")],
            }
        dict_payload["moduleReadiness"].append({
            "moduleCode": str_module_code,
            "statusCode": dict_result.get("statusCode", CProductWip360StatusCode.UNAVAILABLE),
            "sourceCode": dict_result.get("sourceCode", CProductWip360SourceCode.NOT_RECORDED),
            "warningCodes": [
                dict_warning.get("warningCode", "")
                for dict_warning in dict_result.get("warnings", [])
                if dict_warning.get("warningCode")
            ],
        })
        dict_payload["sourceLineage"][str_module_code] = {
            "sourceCode": dict_result.get("sourceCode", CProductWip360SourceCode.NOT_RECORDED),
            "sourceRefNo": dict_result.get("sourceRefNo", ""),
        }
        dict_payload["warnings"].extend(dict_result.get("warnings", []))
        self.__merge_module_payload(dict_payload, str_module_code, dict_result)

    def __merge_module_payload(self, dict_payload, str_module_code, dict_result):
        dict_data = dict_result.get("data", {}) or {}
        str_status_code = dict_result.get("statusCode", CProductWip360StatusCode.UNAVAILABLE)
        if str_module_code == CProductWip360ModuleCode.ITEM:
            dict_payload["itemDetail"] = dict_data
        elif str_module_code == CProductWip360ModuleCode.TRANSACTION_ITEM:
            dict_payload["transactionContext"] = {
                "linkedTransactionItemStatusCode": str_status_code,
                "transactionItems": dict_data.get("items", []),
                "total": util_safe_int(dict_data.get("total")),
            }
        elif str_module_code == CProductWip360ModuleCode.WAREHOUSE:
            dict_summary = dict_data.get("summary", {}) or {}
            dict_payload["inventoryOverview"] = {
                "hasStock": util_safe_float(dict_summary.get("currentQuantity")) > 0,
                "currentQuantity": util_round_quantity(dict_summary.get("currentQuantity")),
                "availableQuantity": util_round_quantity(dict_summary.get("availableQuantity")),
                "reservedQuantity": util_round_quantity(dict_summary.get("reservedQuantity")),
                "qualityHoldQuantity": util_round_quantity(dict_summary.get("qualityHoldQuantity")),
                "inventoryValue": util_round_amount(dict_summary.get("inventoryValue")),
                "availableValue": util_round_amount(dict_summary.get("availableValue")),
                "warehouseCount": util_safe_int(dict_summary.get("warehouseCount")),
                "batchCount": util_safe_int(dict_summary.get("batchCount")),
                "riskTypes": dict_summary.get("riskTypes", []),
            }
            dict_payload["batchHighlights"] = dict_data.get("batchHighlights", [])
        elif str_module_code == CProductWip360ModuleCode.BOM:
            dict_payload["productStructure"] = dict_data.get("productStructure", {}) or {}
        elif str_module_code == CProductWip360ModuleCode.RECIPE:
            dict_payload["recipeFormula"] = dict_data.get("recipeFormula", {}) or {}
        elif str_module_code == CProductWip360ModuleCode.ROUTING:
            dict_payload["routingProcess"] = dict_data.get("routing", {}) or {}

    def __build_item_module(self, str_item_no, n_inventory_date, str_timezone):
        dict_data = CItemCenterService().get_detail(str_item_no, n_inventory_date, str_timezone)
        if not dict_data:
            return self.__empty_module(CProductWip360ModuleCode.ITEM)
        return self.__module(
            CProductWip360ModuleCode.ITEM,
            CProductWip360StatusCode.COMPLETE,
            CProductWip360SourceCode.PRODUCT,
            dict_data,
            "",
            [],
        )

    def __build_transaction_item_module(self, obj_session, str_item_no, n_item_category):
        lst_rows = (
            obj_session.query(CTableTransItems)
            .filter(CTableTransItems.item_no == str_item_no)
            .order_by(CTableTransItems.no.asc())
            .all()
        )
        dict_contracts = self.__latest_contracts(obj_session, [obj_row.no for obj_row in lst_rows])
        lst_transaction_items = []
        for obj_row in lst_rows:
            obj_contract = dict_contracts.get(obj_row.no or "")
            lst_transaction_items.append({
                "transItemNo": obj_row.no or "",
                "transItemName": obj_row.name or "",
                "transItemCategory": util_safe_int(obj_row.category),
                "companyNo": obj_row.company_no or "",
                "companyName": obj_row.company_displayName or "",
                "linkedItemNo": obj_row.item_no or "",
                "linkedItemName": obj_row.item_name or "",
                "contractNo": obj_contract.no if obj_contract else "",
                "contractDate": util_safe_int(obj_contract.date) if obj_contract else 0,
                "tradeUnit": util_safe_int(obj_contract.unit) if obj_contract else 0,
                "tradePrice": util_round_price(obj_contract.price) if obj_contract else 0.0,
            })
        lst_warnings = []
        str_status_code = CProductWip360StatusCode.COMPLETE
        if not lst_transaction_items:
            str_status_code = CProductWip360StatusCode.PARTIAL if n_item_category == EItemCategory.PRODUCT else CProductWip360StatusCode.UNAVAILABLE
            lst_warnings.append(self.__warning(CProductWip360ModuleCode.TRANSACTION_ITEM, CProductWip360WarningCode.MISSING_TRANSACTION_ITEM, str_item_no))
        return self.__module(
            CProductWip360ModuleCode.TRANSACTION_ITEM,
            str_status_code,
            CProductWip360SourceCode.TRANS_ITEMS if lst_transaction_items else CProductWip360SourceCode.NOT_RECORDED,
            {
                "total": len(lst_transaction_items),
                "items": lst_transaction_items,
            },
            "",
            lst_warnings,
        )

    def __latest_contracts(self, obj_session, lst_trans_item_nos):
        lst_trans_item_nos = [str_no for str_no in lst_trans_item_nos if str_no]
        if not lst_trans_item_nos:
            return {}
        dict_result = {}
        lst_rows = (
            obj_session.query(CTableContract)
            .filter(CTableContract.item_no.in_(lst_trans_item_nos))
            .order_by(CTableContract.item_no.asc(), CTableContract.date.desc(), CTableContract.creationTime.desc())
            .all()
        )
        for obj_row in lst_rows:
            if obj_row.item_no not in dict_result:
                dict_result[obj_row.item_no] = obj_row
        return dict_result

    def __build_warehouse_module(self, str_item_no, n_item_category, n_inventory_date, str_timezone):
        dict_inventory = CWarehouseInventoryService().get_inventory(
            n_date=n_inventory_date,
            str_timezone=str_timezone,
            n_item_category=n_item_category,
            str_item_no=str_item_no,
            n_start=0,
            n_count=20,
        )
        lst_rows = dict_inventory.get("results", []) if dict_inventory else []
        f_current_quantity = sum(util_safe_float(dict_row.get("currentQuantity")) for dict_row in lst_rows)
        n_inventory_value = sum(util_safe_int(dict_row.get("inventoryValue")) for dict_row in lst_rows)
        lst_warnings = []
        if not lst_rows:
            lst_warnings.append(self.__warning(CProductWip360ModuleCode.WAREHOUSE, CProductWip360WarningCode.MISSING_WAREHOUSE_STOCK, str_item_no))
        return self.__module(
            CProductWip360ModuleCode.WAREHOUSE,
            CProductWip360StatusCode.COMPLETE if lst_rows else CProductWip360StatusCode.PARTIAL,
            CProductWip360SourceCode.INVENTORY if lst_rows else CProductWip360SourceCode.NOT_RECORDED,
            {
                "summary": {
                    "currentQuantity": util_round_quantity(f_current_quantity),
                    "availableQuantity": util_round_quantity(sum(util_safe_float(dict_row.get("availableQuantity")) for dict_row in lst_rows)),
                    "reservedQuantity": util_round_quantity(sum(util_safe_float(dict_row.get("reservedQuantity")) for dict_row in lst_rows)),
                    "qualityHoldQuantity": util_round_quantity(sum(util_safe_float(dict_row.get("qualityHoldQuantity")) for dict_row in lst_rows)),
                    "inventoryValue": util_round_amount(n_inventory_value),
                    "availableValue": util_round_amount(sum(util_safe_int(dict_row.get("availableValue")) for dict_row in lst_rows)),
                    "batchCount": len({dict_row.get("batchNo") for dict_row in lst_rows if dict_row.get("batchNo")}),
                    "warehouseCount": len({dict_row.get("warehouseNo") for dict_row in lst_rows if dict_row.get("warehouseNo")}),
                    "riskTypes": sorted({
                        str_risk
                        for dict_row in lst_rows
                        for str_risk in dict_row.get("riskTypes", [])
                    }),
                },
                "batchHighlights": lst_rows[:10],
            },
            "",
            lst_warnings,
        )

    def __build_bom_module(self, str_item_no, n_item_category, n_product_version, n_effective_date):
        if n_item_category != EItemCategory.PRODUCT:
            return self.__module(
                CProductWip360ModuleCode.BOM,
                CProductWip360StatusCode.PARTIAL,
                CProductWip360SourceCode.NOT_RECORDED,
                {"productStructure": None},
                "",
                [self.__warning(CProductWip360ModuleCode.BOM, CProductWip360WarningCode.WIP_STRUCTURE_NOT_GOVERNED, str_item_no)],
            )
        dict_data = CBomCenterService().get_product_structure(str_item_no, n_product_version, 3, n_effective_date)
        return self.__wrap_nested_module(CProductWip360ModuleCode.BOM, CProductWip360SourceCode.PRODUCT_STRUCTURE, dict_data, "productStructure")

    def __build_recipe_module(self, str_item_no, n_item_category, n_product_version, n_effective_date):
        if n_item_category != EItemCategory.PRODUCT:
            return self.__module(
                CProductWip360ModuleCode.RECIPE,
                CProductWip360StatusCode.PARTIAL,
                CProductWip360SourceCode.NOT_RECORDED,
                {"recipeFormula": None},
                "",
                [self.__warning(CProductWip360ModuleCode.RECIPE, CProductWip360WarningCode.WIP_RECIPE_NOT_GOVERNED, str_item_no)],
            )
        dict_data = CRecipeFormulaService().get_by_product(str_item_no, n_product_version, n_effective_date)
        return self.__wrap_nested_module(CProductWip360ModuleCode.RECIPE, CProductWip360SourceCode.RECIPE_FORMULA, dict_data, "recipeFormula")

    def __build_routing_module(self, str_item_no, n_effective_date):
        dict_data = CRoutingProcessFlowService().get_current(str_item_no, n_effective_date)
        str_source_code = CProductWip360SourceCode.ROUTING
        if dict_data and dict_data.get("sourceLineage", {}).get("routingVersionSourceCode") == "test_support":
            str_source_code = "test_support"
        return self.__wrap_nested_module(CProductWip360ModuleCode.ROUTING, str_source_code, dict_data, "routing")

    def __wrap_nested_module(self, str_module_code, str_source_code, dict_data, str_ref_key):
        if not dict_data:
            return self.__empty_module(str_module_code)
        lst_warnings = self.__normalize_warnings(str_module_code, dict_data.get("warnings", []))
        str_status_code = CProductWip360StatusCode.COMPLETE
        if str_source_code == "test_support" or self.__has_warning(lst_warnings, CProductWip360WarningCode.TEST_SUPPORT_ONLY):
            str_status_code = CProductWip360StatusCode.TEST_SUPPORT
        elif lst_warnings:
            str_status_code = CProductWip360StatusCode.PARTIAL
        return self.__module(str_module_code, str_status_code, str_source_code, {str_ref_key: dict_data}, self.__source_ref_no(dict_data), lst_warnings)

    def __empty_module(self, str_module_code):
        return self.__module(
            str_module_code,
            CProductWip360StatusCode.UNAVAILABLE,
            CProductWip360SourceCode.NOT_RECORDED,
            {},
            "",
            [self.__warning(str_module_code, CProductWip360WarningCode.MODULE_UNAVAILABLE, "")],
        )

    def __module(self, str_module_code, str_status_code, str_source_code, dict_data, str_source_ref_no, lst_warnings):
        return {
            "moduleCode": str_module_code,
            "statusCode": str_status_code,
            "sourceCode": str_source_code,
            "sourceRefNo": str_source_ref_no or "",
            "data": dict_data or {},
            "warnings": lst_warnings or [],
        }

    def __normalize_warnings(self, str_module_code, lst_warnings):
        lst_result = []
        for obj_warning in lst_warnings or []:
            if isinstance(obj_warning, dict):
                lst_result.append(self.__warning(
                    str_module_code,
                    obj_warning.get("warningCode", "") or obj_warning.get("code", ""),
                    obj_warning.get("refNo", "") or obj_warning.get("stepId", ""),
                ))
            else:
                lst_result.append(self.__warning(str_module_code, str(obj_warning), ""))
        return lst_result

    def __has_warning(self, lst_warnings, str_warning_code):
        return str_warning_code in [dict_warning.get("warningCode", "") for dict_warning in lst_warnings]

    def __source_ref_no(self, dict_data):
        for str_key in ("productStructure", "recipe", "recipeVersion", "routingVersion"):
            dict_ref = dict_data.get(str_key, {})
            if isinstance(dict_ref, dict):
                for str_ref_key in ("structureNo", "recipeNo", "routingVersionId", "bomNo"):
                    if dict_ref.get(str_ref_key):
                        return dict_ref.get(str_ref_key)
        return ""

    def __warning(self, str_module_code, str_warning_code, str_ref_no):
        return {
            "moduleCode": str_module_code,
            "warningCode": str_warning_code or CProductWip360WarningCode.MODULE_UNAVAILABLE,
            "refNo": str_ref_no or "",
        }

    def __capability_boundary(self):
        return {
            "readOnly": True,
            "productWriteSupported": False,
            "bomWriteSupported": False,
            "recipeWriteSupported": False,
            "routingWriteSupported": False,
            "wipWriteSupported": False,
            "sourceOfTruthTransitionSupported": False,
            "cutoverSupported": False,
            "goLiveSupported": False,
        }

    def __empty_inventory_overview(self):
        return {
            "hasStock": False,
            "currentQuantity": 0.0,
            "availableQuantity": 0.0,
            "reservedQuantity": 0.0,
            "qualityHoldQuantity": 0.0,
            "inventoryValue": 0,
            "availableValue": 0,
            "warehouseCount": 0,
            "batchCount": 0,
            "riskTypes": [],
        }
