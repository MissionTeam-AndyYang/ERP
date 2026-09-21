# coding=utf8
"""Synthetic, read-only Manufacturing Definition candidate fixture.

This bounded Gate 2 service intentionally has no database, scheduler, or
business-effect dependency.  It is not a Manufacturing Standard authority.
"""
import time

from flask import request

from package.common.common import EErrorCode, EItemCategory
from package.util.util import util_safe_int


class CManufacturingDefinitionOverview(object):
    PRODUCT = "ERP2-BMP-FG-001"
    WIP = "ERP2-BMP-WIP-001"

    def get(self, str_timezone, str_id):
        str_item_no = (request.args.get("itemNo") or "").strip()
        n_category = util_safe_int(request.args.get("itemCategory"))
        if not str_item_no:
            return 400, EErrorCode.ERROR_INVAILD_PARAM, "itemNo is required", {}
        if n_category not in (EItemCategory.PRODUCT, EItemCategory.INPRODUCT):
            return 400, EErrorCode.ERROR_INVAILD_PARAM, "invalid itemCategory", {}
        if (n_category == EItemCategory.PRODUCT and str_item_no != self.PRODUCT) or (n_category == EItemCategory.INPRODUCT and str_item_no != self.WIP):
            return 404, EErrorCode.ERROR_NO_MORE_ITEMS, "record not found", {}
        return 200, EErrorCode.ERROR_SUCCESS, "success", self.__payload(str_item_no, n_category, str_timezone)

    def __payload(self, str_item_no, n_category, str_timezone):
        f_wip = n_category == EItemCategory.INPRODUCT
        str_resolution = "PARTIAL_CANDIDATE" if f_wip else "RESOLVED_WITH_WARNINGS"
        str_status = "partial" if f_wip else "candidate"
        lst_warnings = [{
            "domain": "routing" if f_wip else "packaging",
            "warningCode": "wip_routing_unavailable" if f_wip else "packaging_evidence_incomplete",
            "refNo": str_item_no,
        }]
        dict_references = {
            "bom": self.__domain("bom", "PRESENT", [{"bomNo": "BMP-BOM-001", "bomVersion": 1, "bomName": "Synthetic BOM", "versionStateCode": "candidate"}]),
            "recipe": self.__domain("recipe", "MULTIPLE_CANDIDATES", [
                {"recipeNo": "BMP-RECIPE-001", "recipeVersion": 1, "versionStateCode": "candidate"},
                {"recipeNo": "BMP-RECIPE-002", "recipeVersion": 2, "versionStateCode": "candidate"},
            ]),
            "routing": self.__domain("routing", "UNAVAILABLE" if f_wip else "PRESENT", [] if f_wip else [{"routingVersionId": "BMP-ROUTE-001", "routingVersion": 1, "routingStatusCode": "candidate"}]),
            "packaging": self.__domain("packaging", "INCOMPLETE", []),
            "a15": self.__domain("a15", "ABSENT", []),
            "inventory": self.__domain("inventory", "PARTIAL", []),
        }
        return {
            "serverTimestamp": int(time.time()),
            "timezone": str_timezone or "Asia/Taipei",
            "requestIdentity": {"itemNo": str_item_no, "itemCategory": n_category},
            "subject": {"itemNo": str_item_no, "itemName": "Synthetic Partial WIP" if f_wip else "Synthetic Product", "itemCategory": n_category, "productVersion": 1, "unitWarehouse": 2, "unitProduct": 2, "sourceCode": "fixture_reported", "masterStatusCode": "candidate"},
            "definitionCandidate": {"definitionId": "BMP-MD-WIP-001" if f_wip else "BMP-MD-PRODUCT-001", "definitionStatus": str_status, "bomVersion": {"bomNo": "BMP-BOM-001", "bomVersion": 1}, "recipeVersions": [{"recipeNo": "BMP-RECIPE-001", "recipeVersion": 1}, {"recipeNo": "BMP-RECIPE-002", "recipeVersion": 2}], "routingVersion": None if f_wip else {"routingVersionId": "BMP-ROUTE-001", "routingVersion": 1}, "packagingSpecVersion": []},
            "domainReferences": dict_references,
            "quantityAuthorities": [{"domain": "bom", "valueType": "structural_quantity", "value": 1, "unit": 2, "sourceCode": "fixture_reported", "sourceRef": "BMP-BOM-001", "authorityCaveat": "quantity displayed is not an authority transfer"}],
            "weightAuthorities": [{"domain": "recipe", "valueType": "formula_weight", "value": 1, "unit": 2, "sourceCode": "fixture_reported", "sourceRef": "BMP-RECIPE-001", "authorityCaveat": "weight displayed is not an approved policy"}],
            "effectivity": {"asOfDate": 0, "domains": [{"domain": "bom", "currentActive": None, "retiredInactive": None, "statusCode": "candidate", "evidenceRef": "BMP-BOM-001", "conflictState": "NOT_MEASURED"}]},
            "resolutionStatus": str_resolution,
            "warnings": lst_warnings,
            "sourceLineage": [{"domain": key, "sourceCode": "fixture_reported", "sourceRef": "BMP-GATE2-FIXTURE-001", "sourceParticipant": "CTO-owned bounded execution", "acceptedEvidenceClass": "CONTROLLED_FIXTURE_ONLY", "acceptanceState": value["moduleReadiness"][0]["statusCode"], "authorityCaveat": "not official business truth"} for key, value in dict_references.items()],
            "planningReadiness": {"classification": "EVIDENCE_COVERAGE_ONLY", "status": "PARTIAL", "calculationSupported": False, "scheduleSupported": False, "productionOrderSupported": False, "missingEvidence": ["packaging", "a15"] + (["routing"] if f_wip else [])},
            "freezeCompatibility": {"statusCode": "NOT_READY", "resolutionStatus": str_resolution, "previewOnly": True, "freezeReady": False, "approvalSupported": False, "releaseSupported": False, "freezeSupported": False, "productionOrderFreezeImplemented": False, "warningCount": len(lst_warnings)},
            "capabilityBoundary": {"readOnly": True, "manufacturingDefinitionWriteSupported": False, "productWriteSupported": False, "bomWriteSupported": False, "recipeWriteSupported": False, "routingWriteSupported": False, "packagingWriteSupported": False, "approvalSupported": False, "releaseSupported": False, "freezeSupported": False, "sourceOfTruthTransitionSupported": False, "cutoverSupported": False, "goLiveSupported": False, "database": False, "ddl": False, "planningCalculation": False, "scheduleExecution": False, "productionTruth": False, "businessTruth": False},
        }

    def __domain(self, str_domain, str_state, lst_versions):
        return {"moduleReadiness": [{"moduleCode": str_domain, "statusCode": str_state, "sourceCode": "fixture_reported", "warningCodes": []}], "versions": lst_versions, "sourceLineage": {str_domain: {"sourceCode": "fixture_reported", "sourceRef": "BMP-GATE2-FIXTURE-001"}}, "warnings": []}
