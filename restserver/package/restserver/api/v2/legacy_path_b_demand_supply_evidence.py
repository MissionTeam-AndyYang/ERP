# coding=utf8
"""Deterministic, fixture-backed Legacy Path B evidence composition."""
import json
from pathlib import Path

from flask import request
from package.common.common import EErrorCode


class CLegacyPathBDemandSupplyEvidenceOverview(object):
    SCENARIO = "LPB-G0-SYN-SCENARIO-001"

    def get(self, str_timezone, str_id):
        scenario_id = (request.args.get("scenarioId") or "").strip()
        if not scenario_id:
            return 400, EErrorCode.ERROR_INVAILD_PARAM, "scenarioId is required", {}
        if scenario_id != self.SCENARIO:
            return 404, EErrorCode.ERROR_NO_MORE_ITEMS, "scenario not found", {}
        return 200, EErrorCode.ERROR_SUCCESS, "success", self.__compose(scenario_id)

    def __compose(self, scenario_id):
        fixture = self.__fixture()
        evidence = sorted(fixture["evidence"], key=lambda item: item["evidenceId"])
        by_id = {item["evidenceId"]: item for item in evidence}
        return {
            "requestIdentity": {"scenarioId": scenario_id},
            "correlation": {"fixtureNamespace": fixture["fixtureNamespace"], "scenarioId": scenario_id, "correlationRule": "explicit_parent_or_reference_id_only"},
            "sourceCoverage": fixture["sourceCoverage"],
            "evidence": evidence,
            "chain": {
                "demand": by_id["E-DEMAND-001"],
                "planningInterpretation": by_id["E-PLAN-001"],
                "supplyReference": by_id["E-SUPPLY-001"],
                "receiptInventoryEvidence": [by_id["E-INVENTORY-001"], by_id["E-RECEIPT-001"]]
            },
            "warnings": ["missing_is_not_absent", "unavailable_is_not_absent", "conflict_visible_not_resolved", "no_identity_or_lifecycle_inference"],
            "authoritative_winner": None,
            "truthLabels": {"source_class": "FIXTURE_REPORTED / EVIDENCE_REPORTED", "freshness": "NOT_MEASURED", "confidence": "CONTROLLED_FIXTURE_ONLY", "business_truth": False, "production_truth": False, "customer_commitment": False, "purchase_commitment": False, "actual_receipt": False, "official_inventory_truth": False, "accounting_effect": False},
            "capabilityBoundary": {"readOnly": True, "database": False, "ddl": False, "persistentStorage": False, "runtime": False, "sourceOfTruth": False, "planningCalculation": False, "procurementAuthorization": False, "businessTransaction": False, "inventoryEffect": False, "accountingEffect": False}
        }

    def __fixture(self):
        path = Path(__file__).parent / "fixtures" / "legacy_path_b" / "ERP2-LPB-G0-SYNTHETIC-FIXTURE-001" / "state.json"
        return json.loads(path.read_text(encoding="utf-8"))
