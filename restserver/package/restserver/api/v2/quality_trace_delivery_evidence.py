# coding=utf8
"""Deterministic, fixture-backed Candidate C evidence composition."""
import json
from pathlib import Path

from flask import request
from package.common.common import EErrorCode


class CQualityTraceDeliveryEvidenceOverview(object):
    LOT = "CAND-C-LOT-001"
    DELIVERY = "CAND-C-DELIVERY-001"

    def get(self, str_timezone, str_id):
        lot_no = (request.args.get("lotNo") or "").strip()
        delivery_reference = (request.args.get("deliveryReference") or "").strip()
        if not lot_no or not delivery_reference:
            return 400, EErrorCode.ERROR_INVAILD_PARAM, "lotNo and deliveryReference are required", {}
        if lot_no != self.LOT or delivery_reference != self.DELIVERY:
            return 404, EErrorCode.ERROR_NO_MORE_ITEMS, "record not found", {}
        return 200, EErrorCode.ERROR_SUCCESS, "success", self.__compose(lot_no, delivery_reference)

    def __compose(self, lot_no, delivery_reference):
        fixture = self.__fixture()
        ordered = sorted(fixture["evidence"], key=lambda item: item["evidenceId"])
        linked = [item for item in ordered if item.get("lotNo") == lot_no and item.get("deliveryReference") == delivery_reference]
        unlinked = [item for item in ordered if item.get("deliveryReference") == delivery_reference and "lotNo" not in item]
        return {
            "requestIdentity": {"lotNo": lot_no, "deliveryReference": delivery_reference},
            "correlation": fixture["correlation"],
            "sourceCoverage": fixture["sourceCoverage"],
            "evidence": ordered,
            "lotToDelivery": {"state": "PRESENT", "evidenceIds": [item["evidenceId"] for item in linked], "correlationRule": "explicit_lot_or_explicit_reference_only"},
            "unlinkedDeliveryEvidence": unlinked,
            "warnings": ["unavailable_is_not_absent", "conflict_visible_not_resolved", "observed_lineage_not_inferred_genealogy"],
            "authoritative_winner": None,
            "truthLabels": {"source_class": "FIXTURE_REPORTED / EVIDENCE_REPORTED", "freshness": "NOT_MEASURED", "confidence": "CONTROLLED_FIXTURE_ONLY", "business_truth": False, "production_truth": False, "official_quality_disposition": False, "official_hold_release": False, "official_recall": False, "official_delivery_effect": False, "official_receipt_effect": False, "official_inventory_effect": False, "official_customer_effect": False, "official_accounting_effect": False},
            "capabilityBoundary": {"readOnly": True, "database": False, "ddl": False, "persistentStorage": False, "qualityDisposition": False, "deliveryExecution": False, "sourceOfTruth": False}
        }

    def __fixture(self):
        path = Path(__file__).parent / "fixtures" / "quality_trace_delivery_evidence" / "CAND-C-GATE2-FIXTURE-001" / "state.json"
        return json.loads(path.read_text(encoding="utf-8"))
