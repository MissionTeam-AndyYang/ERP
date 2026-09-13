# coding=utf8
"""Read-only Warehouse P0 adapter for the isolated non-production fixture."""

import hashlib
import json
from pathlib import Path

from package.common.common import EErrorCode


class CWarehouseFixtureP0(object):
    FIXTURE_ROOT = Path(r"C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\Warehouse_Operations\ERP2-WH-P0-ALT-FIXTURE-001")
    MANIFEST_PATH = FIXTURE_ROOT / "fixture-manifest.json"
    SEED_PATH = FIXTURE_ROOT / "seed.json"
    SCENARIO_PATH = Path(r"C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\Warehouse_Operations\ERP2-WH-P1-EXCEPTION-FIXTURE-001\scenarios.json")
    SCENARIO_FIXTURE_ID = "ERP2-WH-P1-EXCEPTION-FIXTURE-001"
    SCENARIO_FIXTURE_VERSION = "1.0.0"
    SCENARIO_IDS = {
        "CONFIRMED_BALANCE",
        "ZERO_BALANCE",
        "MISSING_RECORD",
        "UNAVAILABLE_SOURCE",
        "PARTIAL_LINKAGE",
        "CONFLICTING_INPUT",
        "DERIVED_BALANCE",
        "NOT_MEASURED_FRESHNESS",
        "CONTROLLED_FIXTURE_ONLY_CONFIDENCE",
    }
    FIXTURE_ID = "ERP2-WH-P0-ALT-FIXTURE-001"
    FIXTURE_VERSION = "1.0.0"

    def get(self, str_timezone, str_id):
        from flask import request

        if "scenarioId" in request.args:
            return self.__get_scenario(request.args.get("scenarioId"), str_timezone or "UTC")
        str_item_no = (self.__request_item_no() or "").strip()
        if not str_item_no:
            return 400, EErrorCode.ERROR_INVAILD_PARAM, "itemNo is required", {}
        str_item_category = (self.__request_item_category() or "").strip()
        if str_item_category and str_item_category != "5":
            return 400, EErrorCode.ERROR_INVAILD_PARAM, "fixture supports itemCategory=5 only", {}
        try:
            dict_manifest = self.__read_json(self.MANIFEST_PATH)
            dict_seed = self.__read_json(self.SEED_PATH)
            self.__validate_fixture(dict_manifest, dict_seed)
            dict_payload = self.__build_payload(dict_manifest, dict_seed, str_item_no, str_timezone or "UTC")
        except FileNotFoundError:
            return 503, EErrorCode.ERROR_OTHER_ERROR, "controlled fixture unavailable", self.__error_payload("FIXTURE_UNAVAILABLE")
        except (ValueError, KeyError) as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "controlled fixture invalid: %s" % (str(error)), self.__error_payload("FIXTURE_INVALID")
        except Exception as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "controlled fixture read error: %s" % (str(error)), self.__error_payload("FIXTURE_READ_ERROR")
        if not dict_payload:
            return 404, EErrorCode.ERROR_NO_MORE_ITEMS, "fixture item not found", self.__error_payload("ITEM_NOT_FOUND")
        return 200, EErrorCode.ERROR_SUCCESS, "success", dict_payload

    def __request_item_no(self):
        from flask import request
        return request.args.get("itemNo")

    def __request_item_category(self):
        from flask import request
        return request.args.get("itemCategory")

    def __read_json(self, obj_path):
        with obj_path.open("r", encoding="utf-8") as obj_file:
            return json.load(obj_file)

    def __validate_fixture(self, dict_manifest, dict_seed):
        if dict_manifest.get("fixture_id") != self.FIXTURE_ID or dict_seed.get("fixture_id") != self.FIXTURE_ID:
            raise ValueError("fixture identity mismatch")
        if dict_manifest.get("fixture_version") != self.FIXTURE_VERSION or dict_seed.get("fixture_version") != self.FIXTURE_VERSION:
            raise ValueError("fixture version mismatch")
        if dict_manifest.get("business_truth") is not False or dict_manifest.get("production_truth") is not False:
            raise ValueError("fixture truth flags are not false")
        if dict_manifest.get("classification") != "NON-PRODUCTION TEST FIXTURE":
            raise ValueError("fixture classification mismatch")
        if dict_manifest.get("secondary_label") != "SYNTHETIC / CONTROLLED VALIDATION DATA":
            raise ValueError("fixture secondary label mismatch")
        if dict_manifest.get("labels", {}).get("source_class") != "SYNTHETIC_FIXTURE":
            raise ValueError("fixture source class mismatch")
        if dict_manifest.get("labels", {}).get("freshness") != "NOT_MEASURED":
            raise ValueError("fixture freshness label mismatch")
        if dict_manifest.get("labels", {}).get("confidence") != "CONTROLLED_FIXTURE_ONLY":
            raise ValueError("fixture confidence label mismatch")

    def __build_payload(self, dict_manifest, dict_seed, str_item_no, str_timezone):
        lst_items = dict_seed.get("item_material", [])
        dict_item = next((row for row in lst_items if row.get("item_no") == str_item_no), None)
        if not dict_item:
            return None
        str_item_id = dict_item.get("item_id")
        dict_warehouse = self.__one_by_id(dict_seed.get("warehouse", []), "warehouse_id", "fixture-warehouse-001")
        dict_receipt = self.__one_by_id(dict_seed.get("warehouse_receipt", []), "receipt_id", "fixture-receipt-001")
        dict_movement = self.__one_by_id(dict_seed.get("inventory_movement", []), "movement_id", "fixture-movement-001")
        dict_balance = self.__one_by_id(dict_seed.get("inventory_balance_snapshot", []), "balance_id", "fixture-balance-001")
        dict_evidence = self.__one_by_id(dict_seed.get("evidence_link", []), "evidence_link_id", "fixture-evidence-001")
        self.__validate_links(str_item_id, dict_warehouse, dict_receipt, dict_movement, dict_balance, dict_evidence)
        str_seed_hash = self.__sha256(self.SEED_PATH)
        str_manifest_hash = self.__sha256(self.MANIFEST_PATH)
        return {
            "fixture": {
                "fixtureId": dict_manifest["fixture_id"],
                "fixtureVersion": dict_manifest["fixture_version"],
                "classification": dict_manifest["classification"],
                "secondaryLabel": dict_manifest["secondary_label"],
                "businessTruth": False,
                "productionTruth": False,
                "sourceClass": "SYNTHETIC_FIXTURE",
                "freshness": "NOT_MEASURED",
                "confidence": "CONTROLLED_FIXTURE_ONLY",
                "timezone": str_timezone,
                "manifestSha256": str_manifest_hash,
                "seedSha256": str_seed_hash,
            },
            "subject": {
                "itemId": dict_item["item_id"],
                "itemNo": dict_item["item_no"],
                "itemCategory": dict_item["item_category"],
                "sourceClass": dict_item["source_class"],
                "businessTruth": dict_item["business_truth"],
                "productionTruth": False,
            },
            "workflow": {
                "itemMaterial": {"itemId": dict_item["item_id"], "itemNo": dict_item["item_no"]},
                "warehouseReceipt": self.__receipt_payload(dict_receipt),
                "inventoryMovement": self.__movement_payload(dict_movement),
                "currentBalance": {
                    "balanceId": dict_balance["balance_id"],
                    "sourceReported": {
                        "openingBalance": dict_balance["opening_balance"],
                        "receiptQuantity": dict_balance["receipt_quantity"],
                        "movementEffect": dict_balance["movement_effect"],
                        "uom": dict_balance["uom"],
                        "sourceClass": dict_balance["source_class"],
                    },
                    "current_balance_derived": dict_balance["current_balance_derived"],
                    "derivedFields": ["current_balance_derived"],
                    "derivation": "opening_balance + receipt_quantity + movement_effect",
                    "freshness": dict_balance["freshness"],
                    "confidence": dict_balance["confidence"],
                    "lineageRef": dict_balance["lineage_ref"],
                },
                "warehouseVisibility": {
                    "warehouseId": dict_warehouse["warehouse_id"],
                    "warehouseCode": dict_warehouse["warehouse_code"],
                    "sourceClass": dict_warehouse["source_class"],
                    "businessTruth": dict_warehouse["business_truth"],
                },
                "evidenceLink": {
                    "evidenceLinkId": dict_evidence["evidence_link_id"],
                    "receiptId": dict_evidence["receipt_id"],
                    "movementId": dict_evidence["movement_id"],
                    "balanceId": dict_evidence["balance_id"],
                    "lineageStatus": dict_evidence["lineage_status"],
                    "sourceClass": dict_evidence["source_class"],
                    "businessTruth": dict_evidence["business_truth"],
                },
            },
            "sourceLineage": {
                "fixtureId": dict_manifest["fixture_id"],
                "itemId": str_item_id,
                "warehouseId": dict_warehouse["warehouse_id"],
                "receiptId": dict_receipt["receipt_id"],
                "movementId": dict_movement["movement_id"],
                "balanceId": dict_balance["balance_id"],
                "evidenceLinkId": dict_evidence["evidence_link_id"],
                "status": dict_evidence["lineage_status"],
                "sourceClass": "SYNTHETIC_FIXTURE",
                "freshness": "NOT_MEASURED",
                "confidence": "CONTROLLED_FIXTURE_ONLY",
            },
            "capabilityBoundary": {
                "readOnly": True,
                "writesSupported": False,
                "liveC1Binding": False,
                "governedSourceBinding": False,
                "businessTruth": False,
                "productionTruth": False,
            },
            "reset": dict_manifest["reset_rebuild"],
            "warnings": ["CONTROLLED_FIXTURE_ONLY", "SYNTHETIC_NOT_BUSINESS_TRUTH"],
        }

    def __receipt_payload(self, dict_receipt):
        return {
            "receiptId": dict_receipt["receipt_id"],
            "receiptNo": dict_receipt["receipt_no"],
            "itemId": dict_receipt["item_id"],
            "warehouseId": dict_receipt["warehouse_id"],
            "quantity": dict_receipt["quantity"],
            "uom": dict_receipt["uom"],
            "sourceClass": dict_receipt["source_class"],
            "lineageRef": dict_receipt["lineage_ref"],
            "freshness": dict_receipt["freshness"],
            "confidence": dict_receipt["confidence"],
        }

    def __movement_payload(self, dict_movement):
        return {
            "movementId": dict_movement["movement_id"],
            "movementType": dict_movement["movement_type"],
            "effect": dict_movement["effect"],
            "itemId": dict_movement["item_id"],
            "warehouseId": dict_movement["warehouse_id"],
            "receiptId": dict_movement["receipt_id"],
            "quantity": dict_movement["quantity"],
            "uom": dict_movement["uom"],
            "sourceClass": dict_movement["source_class"],
            "lineageRef": dict_movement["lineage_ref"],
            "freshness": dict_movement["freshness"],
            "confidence": dict_movement["confidence"],
        }

    def __validate_links(self, str_item_id, dict_warehouse, dict_receipt, dict_movement, dict_balance, dict_evidence):
        if not all((dict_warehouse, dict_receipt, dict_movement, dict_balance, dict_evidence)):
            raise KeyError("required workflow entity missing")
        if any("business_truth" in dict_row and dict_row.get("business_truth") is not False for dict_row in (dict_warehouse, dict_receipt, dict_movement, dict_balance, dict_evidence)):
            raise ValueError("selected entity truth flag is not false")
        if dict_receipt["item_id"] != str_item_id or dict_movement["item_id"] != str_item_id or dict_balance["item_id"] != str_item_id or dict_evidence["item_id"] != str_item_id:
            raise ValueError("item identity link mismatch")
        if dict_receipt["warehouse_id"] != dict_warehouse["warehouse_id"] or dict_movement["warehouse_id"] != dict_warehouse["warehouse_id"] or dict_balance["warehouse_id"] != dict_warehouse["warehouse_id"]:
            raise ValueError("warehouse identity link mismatch")
        if dict_movement["receipt_id"] != dict_receipt["receipt_id"]:
            raise ValueError("receipt movement link mismatch")
        if dict_evidence["receipt_id"] != dict_receipt["receipt_id"] or dict_evidence["movement_id"] != dict_movement["movement_id"] or dict_evidence["balance_id"] != dict_balance["balance_id"]:
            raise ValueError("evidence link mismatch")

    def __one_by_id(self, lst_rows, str_key, str_value):
        return next((dict_row for dict_row in lst_rows if dict_row.get(str_key) == str_value), None)

    def __sha256(self, obj_path):
        obj_hash = hashlib.sha256()
        with obj_path.open("rb") as obj_file:
            for obj_chunk in iter(lambda: obj_file.read(1024 * 1024), b""):
                obj_hash.update(obj_chunk)
        return obj_hash.hexdigest().upper()

    def __error_payload(self, str_code):
        return {
            "status": str_code,
            "fixtureId": self.FIXTURE_ID,
            "fixtureVersion": self.FIXTURE_VERSION,
            "sourceClass": "SYNTHETIC_FIXTURE",
            "businessTruth": False,
            "productionTruth": False,
            "freshness": "NOT_MEASURED",
            "confidence": "CONTROLLED_FIXTURE_ONLY",
            "capabilityBoundary": {"readOnly": True, "writesSupported": False, "liveC1Binding": False},
        }

    def __get_scenario(self, str_scenario_id, str_timezone):
        str_scenario_id = (str_scenario_id or "").strip()
        if not str_scenario_id:
            return 400, EErrorCode.ERROR_INVAILD_PARAM, "scenarioId is required", self.__scenario_error_payload("SCENARIO_REQUIRED", str_scenario_id)
        try:
            dict_document = self.__read_json(self.SCENARIO_PATH)
            self.__validate_scenario_document(dict_document)
            if isinstance(dict_document["scenarios"], dict):
                dict_scenario = dict_document["scenarios"].get(str_scenario_id)
            else:
                dict_scenario = next((dict_row for dict_row in dict_document["scenarios"] if dict_row.get("scenario_id") == str_scenario_id), None)
            if dict_scenario is None:
                return 400, EErrorCode.ERROR_INVAILD_PARAM, "unknown controlled scenario", self.__scenario_error_payload("SCENARIO_UNKNOWN", str_scenario_id)
            dict_payload = self.__scenario_payload(dict_document, dict_scenario, str_timezone)
        except FileNotFoundError:
            return 503, EErrorCode.ERROR_OTHER_ERROR, "controlled exception fixture unavailable", self.__scenario_error_payload("FIXTURE_UNAVAILABLE", str_scenario_id)
        except (ValueError, KeyError, TypeError) as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "controlled exception fixture invalid: %s" % str(error), self.__scenario_error_payload("FIXTURE_INVALID", str_scenario_id)
        except Exception as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "controlled exception fixture read error: %s" % str(error), self.__scenario_error_payload("FIXTURE_READ_ERROR", str_scenario_id)

        n_status_code = dict_scenario["http_status"]
        if n_status_code == 200:
            n_code = EErrorCode.ERROR_SUCCESS
        elif n_status_code == 404:
            n_code = EErrorCode.ERROR_NO_MORE_ITEMS
        else:
            n_code = EErrorCode.ERROR_OTHER_ERROR
        return n_status_code, n_code, dict_payload["scenario"].get("message", self.__scenario_message(dict_payload["scenario"]["status"])), dict_payload

    def __read_json(self, obj_path):
        with obj_path.open("r", encoding="utf-8") as obj_file:
            return json.load(obj_file)

    def __validate_scenario_document(self, dict_document):
        if dict_document.get("fixture_id") != self.SCENARIO_FIXTURE_ID:
            raise ValueError("scenario fixture identity mismatch")
        if dict_document.get("fixture_version") != self.SCENARIO_FIXTURE_VERSION:
            raise ValueError("scenario fixture version mismatch")
        if dict_document.get("classification") != "NON-PRODUCTION TEST FIXTURE":
            raise ValueError("scenario fixture classification mismatch")
        if dict_document.get("secondary_label") != "SYNTHETIC / CONTROLLED VALIDATION DATA":
            raise ValueError("scenario fixture label mismatch")
        if dict_document.get("business_truth") is not False or dict_document.get("production_truth") is not False:
            raise ValueError("scenario fixture truth flags are not false")
        if dict_document.get("no_live_source") is not True:
            raise ValueError("scenario fixture live source flag is not disabled")
        obj_scenarios = dict_document.get("scenarios")
        if isinstance(obj_scenarios, dict):
            set_scenario_ids = set(obj_scenarios)
        elif isinstance(obj_scenarios, list):
            set_scenario_ids = {dict_row.get("scenario_id") for dict_row in obj_scenarios}
        else:
            set_scenario_ids = set()
        if set_scenario_ids != {"confirmed_balance", "zero_balance", "missing_record", "unavailable_source", "partial_linkage", "conflicting_input", "derived_balance", "not_measured_freshness", "controlled_fixture_only_confidence"} and set_scenario_ids != self.SCENARIO_IDS:
            raise ValueError("scenario catalog mismatch")

    def __scenario_payload(self, dict_document, dict_scenario, str_timezone):
        if isinstance(dict_scenario.get("subject"), dict) and isinstance(dict_scenario.get("balance"), dict):
            return self.__scenario_payload_keyed(dict_document, dict_scenario, str_timezone)
        dict_observed = dict_scenario["observed"]
        dict_source = dict_scenario.get("source_values")
        dict_derived = dict_scenario.get("derived_values")
        dict_labels = {
            "classification": dict_document["classification"],
            "secondaryLabel": dict_document["secondary_label"],
            "businessTruth": False,
            "productionTruth": False,
            "freshness": dict_scenario.get("labels", {}).get("freshness", "NOT_MEASURED"),
            "confidence": dict_scenario.get("labels", {}).get("confidence", "CONTROLLED_FIXTURE_ONLY"),
        }
        str_status = self.__scenario_status(dict_scenario)
        return {
            "fixture": {
                "fixtureId": dict_document["fixture_id"],
                "fixtureVersion": dict_document["fixture_version"],
                "classification": dict_document["classification"],
                "secondaryLabel": dict_document["secondary_label"],
                "businessTruth": False,
                "productionTruth": False,
                "sourceClass": "SYNTHETIC_FIXTURE",
                "freshness": dict_labels["freshness"],
                "confidence": dict_labels["confidence"],
                "timezone": str_timezone,
                "scenarioFileSha256": self.__sha256(self.SCENARIO_PATH),
                "noLiveSource": True,
            },
            "scenario": {
                "scenarioId": dict_scenario["scenario_id"],
                "label": dict_scenario["description"],
                "status": str_status,
                "sourceStatus": dict_scenario["status"],
                "balanceStatus": self.__balance_status(dict_scenario),
                "httpStatus": dict_scenario["http_status"],
            },
            "subject": {
                "itemId": dict_observed.get("item"),
                "warehouseId": dict_observed.get("warehouse"),
                "receiptId": dict_observed.get("receipt"),
                "movementId": dict_observed.get("movement"),
                "balanceId": dict_observed.get("balance"),
                "evidenceLinkId": dict_observed.get("evidence"),
            },
            "balance": {
                "sourceReported": self.__source_payload(dict_source),
                "derived": (dict_derived or {}).get("current_balance_derived"),
                "balanceKind": self.__balance_kind(dict_scenario),
                "derivedFields": list(dict_derived.keys()) if dict_derived else [],
                "derivation": "opening_balance + receipt_quantity + movement_effect" if dict_derived else None,
                "freshness": dict_labels["freshness"],
                "confidence": dict_labels["confidence"],
            },
            "sourceLineage": {
                "status": dict_scenario["lineage"]["status"],
                "resolution": dict_scenario["lineage"].get("resolution"),
                "missingEntity": dict_scenario["lineage"].get("missing_entity"),
                "itemId": dict_observed.get("item"),
                "warehouseId": dict_observed.get("warehouse"),
                "receiptId": dict_observed.get("receipt"),
                "movementId": dict_observed.get("movement"),
                "balanceId": dict_observed.get("balance"),
                "evidenceLinkId": dict_observed.get("evidence"),
                "sourceClass": "SYNTHETIC_FIXTURE",
                "freshness": dict_labels["freshness"],
                "confidence": dict_labels["confidence"],
            },
            "labels": dict_labels,
            "capabilityBoundary": {
                "readOnly": True,
                "writesSupported": False,
                "mockFallback": False,
                "silentFallback": False,
                "liveC1Binding": False,
                "governedSourceBinding": False,
                "businessTruth": False,
                "productionTruth": False,
            },
            "reset": dict_document["reset_rebuild"],
            "cleanup": {"owner": dict_document["reset_rebuild"]["cleanup_owner"], "action": dict_document["reset_rebuild"]["method"]},
            "caveats": dict_scenario.get("caveats", []),
            "warnings": ["CONTROLLED_FIXTURE_ONLY", "SYNTHETIC_NOT_BUSINESS_TRUTH", "NO_LIVE_SOURCE"],
        }

    def __scenario_payload_keyed(self, dict_document, dict_scenario, str_timezone):
        dict_expected = dict_scenario["expected"]
        dict_balance = dict_scenario["balance"]
        dict_subject = dict_scenario["subject"]
        dict_lineage = dict_scenario["lineage"]
        dict_labels = {
            "classification": dict_document["classification"],
            "secondaryLabel": dict_document["secondary_label"],
            "businessTruth": False,
            "productionTruth": False,
            "freshness": dict_expected.get("freshness", "NOT_MEASURED"),
            "confidence": dict_expected.get("confidence", "CONTROLLED_FIXTURE_ONLY"),
        }
        dict_source = dict_balance.get("source_reported")
        if dict_source is not None:
            dict_source = dict(dict_source)
            dict_source["sourceClass"] = "SYNTHETIC_FIXTURE"
        str_balance_status = {
            "SOURCE_CONFIRMED": "CONFIRMED_BALANCE",
            "ZERO": "ZERO_BALANCE",
            "MISSING": "MISSING_RECORD",
            "UNAVAILABLE": "UNAVAILABLE_SOURCE",
            "PARTIAL": "PARTIAL_LINKAGE",
            "CONFLICT": "CONFLICTING_INPUT",
            "DERIVED": "DERIVED_BALANCE",
        }.get(dict_expected.get("balance_status"), dict_expected.get("balance_status"))
        return {
            "fixture": {
                "fixtureId": dict_document["fixture_id"],
                "fixtureVersion": dict_document["fixture_version"],
                "classification": dict_document["classification"],
                "secondaryLabel": dict_document["secondary_label"],
                "businessTruth": False,
                "productionTruth": False,
                "sourceClass": "SYNTHETIC_FIXTURE",
                "freshness": dict_labels["freshness"],
                "confidence": dict_labels["confidence"],
                "timezone": str_timezone,
                "scenarioFileSha256": self.__sha256(self.SCENARIO_PATH),
                "noLiveSource": True,
            },
            "scenario": {
                "scenarioId": dict_scenario["scenario_id"],
                "label": dict_scenario.get("label", dict_expected["message"]),
                "status": dict_expected["status"],
                "sourceStatus": dict_expected.get("balance_status"),
                "balanceStatus": str_balance_status,
                "httpStatus": dict_expected["http_status"],
                "message": dict_expected["message"],
            },
            "subject": dict_subject,
            "balance": {
                "sourceReported": dict_source,
                "derived": dict_balance.get("derived"),
                "balanceKind": dict_balance.get("balance_kind"),
                "derivedFields": dict_balance.get("derived_fields", []),
                "derivation": dict_balance.get("derivation"),
                "freshness": dict_labels["freshness"],
                "confidence": dict_labels["confidence"],
            },
            "sourceLineage": {
                "fixtureId": dict_lineage.get("fixture_id", self.SCENARIO_FIXTURE_ID),
                "status": dict_lineage.get("status"),
                "resolution": dict_lineage.get("resolution"),
                "itemId": dict_lineage.get("itemId"),
                "warehouseId": dict_lineage.get("warehouseId"),
                "receiptId": dict_lineage.get("receiptId"),
                "movementId": dict_lineage.get("movementId"),
                "balanceId": dict_lineage.get("balanceId"),
                "evidenceLinkId": dict_lineage.get("evidenceLinkId"),
                "sourceClass": dict_lineage.get("source_class", "SYNTHETIC_FIXTURE"),
                "freshness": dict_labels["freshness"],
                "confidence": dict_labels["confidence"],
            },
            "labels": dict_labels,
            "capabilityBoundary": {
                "readOnly": True,
                "writesSupported": False,
                "mockFallback": False,
                "silentFallback": False,
                "liveC1Binding": False,
                "governedSourceBinding": False,
                "businessTruth": False,
                "productionTruth": False,
            },
            "reset": dict_document["reset_rebuild"],
            "cleanup": dict_scenario.get("cleanup", {"owner": dict_document["reset_rebuild"]["cleanup_owner"]}),
            "warnings": ["CONTROLLED_FIXTURE_ONLY", "SYNTHETIC_NOT_BUSINESS_TRUTH", "NO_LIVE_SOURCE"],
        }

    def __source_payload(self, dict_source):
        if not dict_source:
            return None
        return {
            "openingBalance": dict_source.get("opening_balance"),
            "receiptQuantity": dict_source.get("receipt_quantity"),
            "movementEffect": dict_source.get("movement_effect"),
            "reportedBalance": dict_source.get("reported_balance"),
            "uom": dict_source.get("uom"),
            "sourceClass": "SYNTHETIC_FIXTURE",
        }

    def __scenario_status(self, dict_scenario):
        return {
            "CONFIRMED": "CONFIRMED_BALANCE",
            "ZERO": "ZERO_BALANCE",
            "MISSING": "MISSING_RECORD",
            "UNAVAILABLE": "UNAVAILABLE_SOURCE",
            "PARTIAL": "PARTIAL_LINKAGE",
            "CONFLICTING": "CONFLICTING_INPUT",
            "DERIVED": "DERIVED_BALANCE",
        }.get(dict_scenario["status"], dict_scenario["status"])

    def __balance_status(self, dict_scenario):
        if dict_scenario["scenario_id"] == "NOT_MEASURED_FRESHNESS":
            return "CONFIRMED_BALANCE"
        if dict_scenario["scenario_id"] == "CONTROLLED_FIXTURE_ONLY_CONFIDENCE":
            return "CONFIRMED_BALANCE"
        return self.__scenario_status(dict_scenario)

    def __balance_kind(self, dict_scenario):
        return {
            "CONFIRMED": "SOURCE_CONFIRMED",
            "ZERO": "SOURCE_CONFIRMED",
            "DERIVED": "DERIVED_BALANCE",
            "CONFLICTING": "CONFLICTING_SOURCE_AND_DERIVED",
            "PARTIAL": "PARTIAL_LINKAGE",
        }.get(dict_scenario["status"], "NOT_AVAILABLE")

    def __scenario_message(self, str_status):
        return {
            "CONFIRMED_BALANCE": "controlled balance confirmed",
            "ZERO_BALANCE": "controlled zero balance",
            "MISSING_RECORD": "controlled record missing",
            "UNAVAILABLE_SOURCE": "controlled source unavailable",
            "PARTIAL_LINKAGE": "controlled linkage is partial",
            "CONFLICTING_INPUT": "controlled source and derived balances conflict",
            "DERIVED_BALANCE": "controlled balance derived",
        }.get(str_status, "controlled fixture state")

    def __scenario_error_payload(self, str_code, str_scenario_id):
        return {
            "status": str_code,
            "fixtureId": self.SCENARIO_FIXTURE_ID,
            "fixtureVersion": self.SCENARIO_FIXTURE_VERSION,
            "sourceClass": "SYNTHETIC_FIXTURE",
            "businessTruth": False,
            "productionTruth": False,
            "freshness": "NOT_MEASURED",
            "confidence": "CONTROLLED_FIXTURE_ONLY",
            "scenarioId": str_scenario_id,
            "capabilityBoundary": {
                "readOnly": True,
                "writesSupported": False,
                "mockFallback": False,
                "silentFallback": False,
                "liveC1Binding": False,
            },
        }


class CWarehouseFixtureP1(object):
    """Read-only exception visibility adapter for the isolated P1 fixture."""

    SCENARIO_PATH = Path(r"C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\Warehouse_Operations\ERP2-WH-P1-EXCEPTION-FIXTURE-001\scenarios.json")
    FIXTURE_ID = "ERP2-WH-P1-EXCEPTION-FIXTURE-001"
    FIXTURE_VERSION = "1.0.0"
    REQUIRED_SCENARIOS = {
        "confirmed_balance",
        "zero_balance",
        "missing_record",
        "unavailable_source",
        "partial_linkage",
        "conflicting_input",
        "derived_balance",
        "not_measured_freshness",
        "controlled_fixture_only_confidence",
    }

    def get(self, str_timezone, str_id):
        from flask import request

        str_scenario_id = (request.args.get("scenario") or "").strip()
        if not str_scenario_id:
            return 400, EErrorCode.ERROR_INVAILD_PARAM, "scenario is required", self.__error_payload("SCENARIO_REQUIRED")
        try:
            dict_document = self.__read_json(self.SCENARIO_PATH)
            self.__validate_document(dict_document)
            dict_scenario = dict_document["scenarios"].get(str_scenario_id)
            if dict_scenario is None:
                return 400, EErrorCode.ERROR_INVAILD_PARAM, "unknown controlled scenario", self.__error_payload("SCENARIO_UNKNOWN", str_scenario_id)
            self.__validate_scenario(str_scenario_id, dict_scenario)
            dict_payload = self.__build_payload(dict_document, dict_scenario, str_timezone or "UTC")
        except FileNotFoundError:
            return 503, EErrorCode.ERROR_OTHER_ERROR, "controlled exception fixture unavailable", self.__error_payload("FIXTURE_UNAVAILABLE")
        except (ValueError, KeyError, TypeError) as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "controlled exception fixture invalid: %s" % str(error), self.__error_payload("FIXTURE_INVALID")
        except Exception as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "controlled exception fixture read error: %s" % str(error), self.__error_payload("FIXTURE_READ_ERROR")

        n_status_code = dict_scenario["expected"]["http_status"]
        if n_status_code == 200:
            n_code = EErrorCode.ERROR_SUCCESS
        elif n_status_code == 404:
            n_code = EErrorCode.ERROR_NO_MORE_ITEMS
        else:
            n_code = EErrorCode.ERROR_OTHER_ERROR
        return n_status_code, n_code, dict_scenario["expected"]["message"], dict_payload

    def __read_json(self, obj_path):
        with obj_path.open("r", encoding="utf-8") as obj_file:
            return json.load(obj_file)

    def __validate_document(self, dict_document):
        if dict_document.get("fixture_id") != self.FIXTURE_ID:
            raise ValueError("fixture identity mismatch")
        if dict_document.get("fixture_version") != self.FIXTURE_VERSION:
            raise ValueError("fixture version mismatch")
        if dict_document.get("classification") != "NON-PRODUCTION TEST FIXTURE":
            raise ValueError("fixture classification mismatch")
        if dict_document.get("secondary_label") != "SYNTHETIC / CONTROLLED VALIDATION DATA":
            raise ValueError("fixture secondary label mismatch")
        if dict_document.get("business_truth") is not False or dict_document.get("production_truth") is not False:
            raise ValueError("fixture truth flags are not false")
        dict_labels = dict_document.get("labels", {})
        if dict_labels.get("freshness") != "NOT_MEASURED":
            raise ValueError("fixture freshness label mismatch")
        if dict_labels.get("confidence") != "CONTROLLED_FIXTURE_ONLY":
            raise ValueError("fixture confidence label mismatch")
        if dict_document.get("no_live_source") is not True:
            raise ValueError("live source flag is not disabled")
        if set(dict_document.get("scenarios", {})) != self.REQUIRED_SCENARIOS:
            raise ValueError("scenario catalog mismatch")

    def __validate_scenario(self, str_scenario_id, dict_scenario):
        if dict_scenario.get("scenario_id") != str_scenario_id:
            raise ValueError("scenario identity mismatch")
        if dict_scenario.get("no_live_source") is not True:
            raise ValueError("scenario live source flag is not disabled")
        dict_expected = dict_scenario.get("expected", {})
        if dict_expected.get("freshness") != "NOT_MEASURED":
            raise ValueError("scenario freshness label mismatch")
        if dict_expected.get("confidence") != "CONTROLLED_FIXTURE_ONLY":
            raise ValueError("scenario confidence label mismatch")
        if dict_scenario.get("lineage", {}).get("source_class") != "SYNTHETIC_FIXTURE":
            raise ValueError("scenario source class mismatch")

    def __build_payload(self, dict_document, dict_scenario, str_timezone):
        dict_expected = dict_scenario["expected"]
        dict_lineage = dict_scenario["lineage"]
        dict_balance = dict_scenario["balance"]
        return {
            "fixture": {
                "fixtureId": dict_document["fixture_id"],
                "fixtureVersion": dict_document["fixture_version"],
                "classification": dict_document["classification"],
                "secondaryLabel": dict_document["secondary_label"],
                "businessTruth": False,
                "productionTruth": False,
                "sourceClass": "SYNTHETIC_FIXTURE",
                "freshness": dict_document["labels"]["freshness"],
                "confidence": dict_document["labels"]["confidence"],
                "timezone": str_timezone,
                "scenarioFileSha256": self.__sha256(self.SCENARIO_PATH),
                "noLiveSource": True,
            },
            "scenario": {
                "scenarioId": dict_scenario["scenario_id"],
                "label": dict_scenario["label"],
                "status": dict_expected["status"],
                "balanceStatus": dict_expected["balance_status"],
                "httpStatus": dict_expected["http_status"],
                "message": dict_expected["message"],
            },
            "subject": dict_scenario["subject"],
            "balance": {
                "sourceReported": dict_balance["source_reported"],
                "derived": dict_balance["derived"],
                "balanceKind": dict_balance["balance_kind"],
                "derivedFields": dict_balance["derived_fields"],
                "derivation": dict_balance["derivation"],
                "freshness": dict_expected["freshness"],
                "confidence": dict_expected["confidence"],
            },
            "sourceLineage": dict_lineage,
            "labels": {
                "classification": "NON-PRODUCTION TEST FIXTURE",
                "secondaryLabel": "SYNTHETIC / CONTROLLED VALIDATION DATA",
                "businessTruth": False,
                "productionTruth": False,
                "freshness": dict_expected["freshness"],
                "confidence": dict_expected["confidence"],
            },
            "capabilityBoundary": {
                "readOnly": True,
                "writesSupported": False,
                "mockFallback": False,
                "silentFallback": False,
                "liveC1Binding": False,
                "governedSourceBinding": False,
                "businessTruth": False,
                "productionTruth": False,
            },
            "reset": dict_document["reset_rebuild"],
            "cleanup": dict_scenario["cleanup"],
            "warnings": ["CONTROLLED_FIXTURE_ONLY", "SYNTHETIC_NOT_BUSINESS_TRUTH", "NO_LIVE_SOURCE"],
        }

    def __sha256(self, obj_path):
        obj_hash = hashlib.sha256()
        with obj_path.open("rb") as obj_file:
            for obj_chunk in iter(lambda: obj_file.read(1024 * 1024), b""):
                obj_hash.update(obj_chunk)
        return obj_hash.hexdigest().upper()

    def __error_payload(self, str_code, str_scenario_id=None):
        dict_payload = {
            "status": str_code,
            "fixtureId": self.FIXTURE_ID,
            "fixtureVersion": self.FIXTURE_VERSION,
            "sourceClass": "SYNTHETIC_FIXTURE",
            "businessTruth": False,
            "productionTruth": False,
            "freshness": "NOT_MEASURED",
            "confidence": "CONTROLLED_FIXTURE_ONLY",
            "scenarioId": str_scenario_id,
            "capabilityBoundary": {
                "readOnly": True,
                "writesSupported": False,
                "mockFallback": False,
                "silentFallback": False,
                "liveC1Binding": False,
            },
        }
        return dict_payload


class CWarehouseFixtureP2(object):
    """Read-only multi-item and multi-location adapter for the isolated P2 fixture."""

    SCENARIO_PATH = Path(r"C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\Warehouse_Operations\ERP2-WH-P2-MULTI-LOCATION-FIXTURE-001\scenarios.json")
    FIXTURE_ID = "ERP2-WH-P2-MULTI-LOCATION-FIXTURE-001"
    FIXTURE_VERSION = "1.0.0"
    SCENARIO_IDS = {
        "normal",
        "zero_balance",
        "missing_record",
        "unavailable_source",
        "partial_linkage",
        "conflicting_input",
        "derived_balance",
        "not_measured_freshness",
        "controlled_fixture_only_confidence",
    }

    def get(self, str_timezone, str_id):
        from flask import request

        str_scenario_id = (request.args.get("scenario") or "").strip()
        if not str_scenario_id:
            return 400, EErrorCode.ERROR_INVAILD_PARAM, "scenario is required", self.__error_payload("SCENARIO_REQUIRED", str_scenario_id)
        try:
            dict_document = self.__read_json(self.SCENARIO_PATH)
            self.__validate_document(dict_document)
            dict_scenario = dict_document["scenarios"].get(str_scenario_id)
            if dict_scenario is None:
                return 400, EErrorCode.ERROR_INVAILD_PARAM, "unknown P2 scenario", self.__error_payload("SCENARIO_UNKNOWN", str_scenario_id)
            self.__validate_scenario(str_scenario_id, dict_scenario)
            dict_payload = self.__build_payload(dict_document, dict_scenario, str_timezone or "UTC")
        except FileNotFoundError:
            return 503, EErrorCode.ERROR_OTHER_ERROR, "P2 fixture unavailable", self.__error_payload("FIXTURE_UNAVAILABLE", str_scenario_id)
        except (ValueError, KeyError, TypeError) as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P2 fixture invalid: %s" % str(error), self.__error_payload("FIXTURE_INVALID", str_scenario_id)
        except Exception as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P2 fixture read error: %s" % str(error), self.__error_payload("FIXTURE_READ_ERROR", str_scenario_id)

        n_status_code = dict_scenario["http_status"]
        if n_status_code == 200:
            n_code = EErrorCode.ERROR_SUCCESS
        elif n_status_code == 404:
            n_code = EErrorCode.ERROR_NO_MORE_ITEMS
        else:
            n_code = EErrorCode.ERROR_OTHER_ERROR
        return n_status_code, n_code, dict_scenario["message"], dict_payload

    def __read_json(self, obj_path):
        with obj_path.open("r", encoding="utf-8") as obj_file:
            return json.load(obj_file)

    def __validate_document(self, dict_document):
        if dict_document.get("fixture_id") != self.FIXTURE_ID:
            raise ValueError("fixture identity mismatch")
        if dict_document.get("fixture_version") != self.FIXTURE_VERSION:
            raise ValueError("fixture version mismatch")
        if dict_document.get("classification") != "NON-PRODUCTION TEST FIXTURE":
            raise ValueError("fixture classification mismatch")
        if dict_document.get("secondary_label") != "SYNTHETIC / CONTROLLED VALIDATION DATA":
            raise ValueError("fixture label mismatch")
        if dict_document.get("business_truth") is not False or dict_document.get("production_truth") is not False:
            raise ValueError("fixture truth flags are not false")
        if dict_document.get("no_live_source") is not True:
            raise ValueError("live source flag is not disabled")
        if set(dict_document.get("scenarios", {})) != self.SCENARIO_IDS:
            raise ValueError("scenario catalog mismatch")
        if len(dict_document.get("items", [])) != 2:
            raise ValueError("item cardinality mismatch")
        if len(dict_document.get("locations", [])) != 2:
            raise ValueError("location cardinality mismatch")
        if len(dict_document.get("rows", [])) != 4:
            raise ValueError("row cardinality mismatch")
        if len(dict_document.get("warehouses", [])) != 1:
            raise ValueError("warehouse cardinality mismatch")

    def __validate_scenario(self, str_scenario_id, dict_scenario):
        if dict_scenario.get("scenario_id") != str_scenario_id:
            raise ValueError("scenario identity mismatch")
        if dict_scenario.get("no_live_source") is not True:
            raise ValueError("scenario live source flag is not disabled")
        if dict_scenario.get("freshness") != "NOT_MEASURED":
            raise ValueError("scenario freshness mismatch")
        if dict_scenario.get("confidence") != "CONTROLLED_FIXTURE_ONLY":
            raise ValueError("scenario confidence mismatch")

    def __build_payload(self, dict_document, dict_scenario, str_timezone):
        lst_rows = self.__scenario_rows(dict_document["rows"], dict_scenario)
        return {
            "fixture": {
                "fixtureId": dict_document["fixture_id"],
                "fixtureVersion": dict_document["fixture_version"],
                "classification": dict_document["classification"],
                "secondaryLabel": dict_document["secondary_label"],
                "businessTruth": False,
                "productionTruth": False,
                "sourceClass": "SYNTHETIC_FIXTURE",
                "freshness": dict_scenario["freshness"],
                "confidence": dict_scenario["confidence"],
                "timezone": str_timezone,
                "scenarioFileSha256": self.__sha256(self.SCENARIO_PATH),
                "noLiveSource": True,
            },
            "scenario": {
                "scenarioId": dict_scenario["scenario_id"],
                "status": dict_scenario["status"],
                "httpStatus": dict_scenario["http_status"],
                "message": dict_scenario["message"],
                "rowMode": dict_scenario["row_mode"],
            },
            "warehouse": dict_document["warehouses"][0],
            "items": dict_document["items"],
            "locations": dict_document["locations"],
            "rows": [self.__row_payload(dict_row) for dict_row in lst_rows],
            "crosswalk": [self.__crosswalk_payload(dict_row) for dict_row in lst_rows],
            "aggregates": self.__aggregates(lst_rows, dict_document),
            "sourceLineage": {
                "sourceClass": "SYNTHETIC_FIXTURE",
                "fixtureId": dict_document["fixture_id"],
                "freshness": dict_scenario["freshness"],
                "confidence": dict_scenario["confidence"],
                "noLiveSource": True,
            },
            "labels": {
                "classification": dict_document["classification"],
                "secondaryLabel": dict_document["secondary_label"],
                "businessTruth": False,
                "productionTruth": False,
                "freshness": dict_scenario["freshness"],
                "confidence": dict_scenario["confidence"],
            },
            "capabilityBoundary": {
                "readOnly": True,
                "writesSupported": False,
                "mockFallback": False,
                "silentFallback": False,
                "liveC1Binding": False,
                "governedSourceBinding": False,
                "businessTruth": False,
                "productionTruth": False,
            },
            "reset": dict_document["reset_rebuild"],
            "cleanup": {"owner": dict_document["reset_rebuild"]["cleanup_owner"], "state": "NO_PERSISTED_RUNTIME_STATE"},
            "caveats": dict_scenario.get("caveats", []),
            "warnings": ["CONTROLLED_FIXTURE_ONLY", "SYNTHETIC_NOT_BUSINESS_TRUTH", "NO_LIVE_SOURCE"],
        }

    def __scenario_rows(self, lst_source_rows, dict_scenario):
        if dict_scenario["row_mode"] == "UNAVAILABLE":
            return []
        lst_rows = [json.loads(json.dumps(dict_row)) for dict_row in lst_source_rows]
        str_target_row = dict_scenario.get("target_row_id")
        for dict_row in lst_rows:
            if dict_scenario["row_mode"] == "ZERO":
                dict_row["source_reported"] = {"opening_balance": 0, "receipt_quantity": 0, "movement_effect": 0, "reported_balance": 0, "uom": "EA"}
                dict_row["current_balance_derived"] = 0
            elif dict_row["row_id"] == str_target_row and dict_scenario["row_mode"] == "MISSING":
                dict_row["source_reported"] = None
                dict_row["current_balance_derived"] = None
                dict_row["evidence_link_id"] = None
                dict_row["lineage_status"] = "MISSING_RECORD"
            elif dict_row["row_id"] == str_target_row and dict_scenario["row_mode"] == "PARTIAL":
                dict_row["current_balance_derived"] = None
                dict_row["evidence_link_id"] = None
                dict_row["lineage_status"] = "PARTIAL_LINKAGE"
            elif dict_row["row_id"] == str_target_row and dict_scenario["row_mode"] == "CONFLICTING":
                dict_row["source_reported"]["reported_balance"] = dict_scenario["conflicting_reported_balance"]
                dict_row["lineage_status"] = "CONFLICTING_INPUT"
            elif dict_scenario["row_mode"] == "DERIVED":
                dict_row["source_reported"]["reported_balance"] = None
                dict_row["lineage_status"] = "DERIVED_ONLY"
        return lst_rows

    def __row_payload(self, dict_row):
        dict_source = dict_row.get("source_reported")
        return {
            "rowId": dict_row["row_id"],
            "itemId": dict_row["item_id"],
            "itemNo": dict_row["item_no"],
            "warehouseId": dict_row["warehouse_id"],
            "warehouseCode": dict_row["warehouse_code"],
            "locationId": dict_row["location_id"],
            "locationCode": dict_row["location_code"],
            "balanceId": dict_row["balance_id"],
            "receiptId": dict_row["receipt_id"],
            "movementId": dict_row["movement_id"],
            "evidenceLinkId": dict_row.get("evidence_link_id"),
            "sourceReported": dict_source,
            "current_balance_derived": dict_row.get("current_balance_derived"),
            "derivedFields": ["current_balance_derived"] if dict_row.get("current_balance_derived") is not None else [],
            "lineageStatus": dict_row["lineage_status"],
            "sourceClass": "SYNTHETIC_FIXTURE",
            "freshness": dict_row["freshness"],
            "confidence": dict_row["confidence"],
        }

    def __crosswalk_payload(self, dict_row):
        return {
            "rowId": dict_row["row_id"],
            "itemId": dict_row["item_id"],
            "warehouseId": dict_row["warehouse_id"],
            "locationId": dict_row["location_id"],
            "balanceId": dict_row["balance_id"],
            "receiptId": dict_row["receipt_id"],
            "movementId": dict_row["movement_id"],
            "evidenceLinkId": dict_row.get("evidence_link_id"),
        }

    def __aggregates(self, lst_rows, dict_document):
        dict_items = {}
        for dict_item in dict_document["items"]:
            lst_item_rows = [dict_row for dict_row in lst_rows if dict_row["item_id"] == dict_item["itemId"]]
            dict_items[dict_item["itemId"]] = self.__aggregate_row_set(lst_item_rows)
        return {"byItem": dict_items, "byWarehouse": self.__aggregate_row_set(lst_rows)}

    def __aggregate_row_set(self, lst_rows):
        if not lst_rows:
            return {"rowCount": 0, "sourceReported": None, "current_balance_derived": None, "status": "UNAVAILABLE"}
        if any(dict_row.get("source_reported") is None or dict_row["source_reported"].get("reported_balance") is None or dict_row.get("current_balance_derived") is None for dict_row in lst_rows):
            return {"rowCount": len(lst_rows), "sourceReported": None, "current_balance_derived": None, "status": "PARTIAL"}
        return {
            "rowCount": len(lst_rows),
            "sourceReported": sum(dict_row["source_reported"]["reported_balance"] for dict_row in lst_rows),
            "current_balance_derived": sum(dict_row["current_balance_derived"] for dict_row in lst_rows),
            "status": "AVAILABLE",
        }

    def __sha256(self, obj_path):
        obj_hash = hashlib.sha256()
        with obj_path.open("rb") as obj_file:
            for obj_chunk in iter(lambda: obj_file.read(1024 * 1024), b""):
                obj_hash.update(obj_chunk)
        return obj_hash.hexdigest().upper()

    def __error_payload(self, str_code, str_scenario_id):
        return {
            "status": str_code,
            "fixtureId": self.FIXTURE_ID,
            "fixtureVersion": self.FIXTURE_VERSION,
            "sourceClass": "SYNTHETIC_FIXTURE",
            "businessTruth": False,
            "productionTruth": False,
            "freshness": "NOT_MEASURED",
            "confidence": "CONTROLLED_FIXTURE_ONLY",
            "scenarioId": str_scenario_id,
            "capabilityBoundary": {"readOnly": True, "writesSupported": False, "mockFallback": False, "silentFallback": False, "liveC1Binding": False},
        }


class CWarehouseFixtureP3(object):
    """Bounded receipt-to-movement adapter for the isolated P3 fixture."""

    STATE_PATH = Path(r"C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\Warehouse_Operations\ERP2-WH-P3-RECEIPT-MOVEMENT-FIXTURE-001\state.json")
    FIXTURE_ID = "ERP2-WH-P3-RECEIPT-MOVEMENT-FIXTURE-001"
    FIXTURE_VERSION = "1.0.0"
    REQUIRED_BODY_FIELDS = {
        "fixtureId",
        "itemNo",
        "itemCategory",
        "warehouseCode",
        "locationCode",
        "receiptNo",
        "quantity",
        "uom",
        "transactionType",
        "effectivity",
    }

    class ValidationError(ValueError):
        def __init__(self, str_code, str_message, n_status_code=400):
            super().__init__(str_message)
            self.str_code = str_code
            self.n_status_code = n_status_code

    def get(self, str_timezone, str_id):
        try:
            dict_state = self.__read_state()
            self.__validate_state(dict_state)
            return 200, EErrorCode.ERROR_SUCCESS, "success", self.__payload(
                dict_state, "GET", self.__sha256(self.STATE_PATH)
            )
        except FileNotFoundError:
            return 503, EErrorCode.ERROR_OTHER_ERROR, "P3 fixture unavailable", self.__error_payload("FIXTURE_UNAVAILABLE", None)
        except (ValueError, KeyError, TypeError) as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P3 fixture invalid: %s" % str(error), self.__error_payload("FIXTURE_INVALID", None)
        except Exception as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P3 fixture read error: %s" % str(error), self.__error_payload("FIXTURE_READ_ERROR", None)

    def post(self, str_timezone, str_id):
        from flask import request

        try:
            dict_state = self.__read_state()
            self.__validate_state(dict_state)
            str_before_hash = self.__sha256(self.STATE_PATH)
            dict_body = request.get_json(silent=True)
            self.__validate_request(dict_state, dict_body)
            dict_state = self.__apply_receipt(dict_state, dict_body)
            self.__write_state(dict_state)
            str_after_hash = self.__sha256(self.STATE_PATH)
            return 201, EErrorCode.ERROR_SUCCESS, "receipt accepted", self.__payload(
                dict_state,
                "POST_RECEIPT",
                str_after_hash,
                str_before_hash,
                str_after_hash,
            )
        except self.ValidationError as error:
            str_state_hash = self.__sha256(self.STATE_PATH) if self.STATE_PATH.exists() else None
            return error.n_status_code, EErrorCode.ERROR_INVAILD_PARAM, str(error), self.__error_payload(error.str_code, str_state_hash)
        except FileNotFoundError:
            return 503, EErrorCode.ERROR_OTHER_ERROR, "P3 fixture unavailable", self.__error_payload("FIXTURE_UNAVAILABLE", None)
        except (ValueError, KeyError, TypeError) as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P3 fixture invalid: %s" % str(error), self.__error_payload("FIXTURE_INVALID", None)
        except Exception as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P3 fixture write error: %s" % str(error), self.__error_payload("FIXTURE_WRITE_ERROR", None)

    def __read_state(self):
        with self.STATE_PATH.open("r", encoding="utf-8") as obj_file:
            return json.load(obj_file)

    def __write_state(self, dict_state):
        str_state = json.dumps(dict_state, indent=2, ensure_ascii=True) + "\n"
        self.STATE_PATH.write_text(str_state, encoding="utf-8")

    def __validate_state(self, dict_state):
        if dict_state.get("fixture_id") != self.FIXTURE_ID:
            raise ValueError("fixture identity mismatch")
        if dict_state.get("fixture_version") != self.FIXTURE_VERSION:
            raise ValueError("fixture version mismatch")
        if dict_state.get("classification") != "NON-PRODUCTION / CONTROLLED VALIDATION DATA":
            raise ValueError("fixture classification mismatch")
        if dict_state.get("source_class") != "SYNTHETIC_FIXTURE":
            raise ValueError("fixture source classification mismatch")
        if dict_state.get("freshness") != "NOT_MEASURED":
            raise ValueError("fixture freshness mismatch")
        if dict_state.get("confidence") != "CONTROLLED_FIXTURE_ONLY":
            raise ValueError("fixture confidence mismatch")
        if dict_state.get("business_truth") is not False or dict_state.get("production_truth") is not False:
            raise ValueError("fixture truth flags are not false")
        if dict_state.get("no_live_source") is not True:
            raise ValueError("live source flag is not disabled")
        if not isinstance(dict_state.get("receipts"), list) or len(dict_state["receipts"]) > 1:
            raise ValueError("receipt cardinality mismatch")
        if not isinstance(dict_state.get("movements"), list) or len(dict_state["movements"]) > 1:
            raise ValueError("movement cardinality mismatch")
        dict_item = dict_state["item"]
        dict_warehouse = dict_state["warehouse"]
        dict_location = dict_state["location"]
        dict_balance = dict_state["balance"]
        if dict_location["warehouse_id"] != dict_warehouse["warehouse_id"]:
            raise ValueError("location warehouse link mismatch")
        if dict_balance["item_id"] != dict_item["item_id"] or dict_balance["warehouse_id"] != dict_warehouse["warehouse_id"] or dict_balance["location_id"] != dict_location["location_id"]:
            raise ValueError("balance crosswalk mismatch")
        if not isinstance(dict_balance["current_balance"], (int, float)) or isinstance(dict_balance["current_balance"], bool):
            raise ValueError("balance quantity invalid")
        if len(dict_state["receipts"]) != len(dict_state["movements"]):
            raise ValueError("receipt movement cardinality mismatch")
        if dict_state["receipts"]:
            self.__validate_existing_transaction(dict_state)

    def __validate_existing_transaction(self, dict_state):
        dict_receipt = dict_state["receipts"][0]
        dict_movement = dict_state["movements"][0]
        if dict_receipt["receipt_id"] != "fixture-receipt-p3-001" or dict_movement["movement_id"] != "fixture-movement-p3-001":
            raise ValueError("transaction identity mismatch")
        if dict_movement["receipt_id"] != dict_receipt["receipt_id"]:
            raise ValueError("movement receipt link mismatch")
        if dict_receipt["item_id"] != dict_state["item"]["item_id"] or dict_receipt["warehouse_id"] != dict_state["warehouse"]["warehouse_id"] or dict_receipt["location_id"] != dict_state["location"]["location_id"]:
            raise ValueError("receipt crosswalk mismatch")
        if dict_movement["before_balance"] + dict_movement["movement_quantity"] != dict_movement["after_balance"]:
            raise ValueError("balance invariant mismatch")
        if dict_state["balance"]["current_balance"] != dict_movement["after_balance"]:
            raise ValueError("current balance mismatch")

    def __validate_request(self, dict_state, dict_body):
        if not isinstance(dict_body, dict):
            raise self.ValidationError("INVALID_BODY", "receipt body must be an object")
        if set(dict_body) != self.REQUIRED_BODY_FIELDS:
            raise self.ValidationError("INVALID_FIELDS", "receipt body must contain exactly the supported fields")
        for str_field in self.REQUIRED_BODY_FIELDS:
            if dict_body[str_field] is None or (isinstance(dict_body[str_field], str) and not dict_body[str_field].strip()):
                raise self.ValidationError("MISSING_FIELD", "%s is required" % str_field)
        if dict_body["fixtureId"] != self.FIXTURE_ID:
            raise self.ValidationError("WRONG_FIXTURE_IDENTITY", "fixtureId does not match the controlled fixture")
        dict_expected = dict_state["valid_receipt"]
        dict_mapping = {
            "itemNo": "item_no",
            "itemCategory": "item_category",
            "warehouseCode": "warehouse_code",
            "locationCode": "location_code",
            "receiptNo": "receipt_no",
            "uom": "uom",
            "transactionType": "transaction_type",
            "effectivity": "effectivity",
        }
        for str_body_field, str_state_field in dict_mapping.items():
            if dict_body[str_body_field] != dict_expected[str_state_field]:
                raise self.ValidationError("WRONG_%s" % str_body_field.upper(), "%s is not the authorized P3 identity or value" % str_body_field)
        if isinstance(dict_body["quantity"], bool) or not isinstance(dict_body["quantity"], (int, float)) or dict_body["quantity"] <= 0:
            raise self.ValidationError("INVALID_QUANTITY", "quantity must be positive")
        if dict_body["quantity"] != dict_expected["quantity"]:
            raise self.ValidationError("UNSUPPORTED_QUANTITY", "only the authorized deterministic receipt quantity is supported")
        if dict_state["receipts"]:
            raise self.ValidationError("DUPLICATE_RECEIPT", "receiptNo has already been applied", 409)

    def __apply_receipt(self, dict_state, dict_body):
        dict_item = dict_state["item"]
        dict_warehouse = dict_state["warehouse"]
        dict_location = dict_state["location"]
        dict_balance = dict_state["balance"]
        n_before = dict_balance["current_balance"]
        n_movement = dict_body["quantity"]
        n_after = n_before + n_movement
        dict_receipt = {
            "receipt_id": "fixture-receipt-p3-001",
            "receipt_no": dict_body["receiptNo"],
            "item_id": dict_item["item_id"],
            "item_no": dict_item["item_no"],
            "item_category": dict_item["item_category"],
            "warehouse_id": dict_warehouse["warehouse_id"],
            "warehouse_code": dict_warehouse["warehouse_code"],
            "location_id": dict_location["location_id"],
            "location_code": dict_location["location_code"],
            "quantity": n_movement,
            "uom": dict_body["uom"],
            "transaction_type": dict_body["transactionType"],
            "effectivity": dict_body["effectivity"],
            "source_class": "SYNTHETIC_FIXTURE",
            "lineage_ref": "fixture-evidence-p3-001",
            "freshness": "NOT_MEASURED",
            "confidence": "CONTROLLED_FIXTURE_ONLY",
        }
        dict_movement = {
            "movement_id": "fixture-movement-p3-001",
            "transaction_id": "fixture-transaction-p3-001",
            "receipt_id": dict_receipt["receipt_id"],
            "item_id": dict_item["item_id"],
            "item_no": dict_item["item_no"],
            "warehouse_id": dict_warehouse["warehouse_id"],
            "warehouse_code": dict_warehouse["warehouse_code"],
            "location_id": dict_location["location_id"],
            "location_code": dict_location["location_code"],
            "quantity": n_movement,
            "uom": dict_body["uom"],
            "transaction_type": dict_body["transactionType"],
            "effectivity": dict_body["effectivity"],
            "before_balance": n_before,
            "movement_quantity": n_movement,
            "after_balance": n_after,
            "source_class": "SYNTHETIC_FIXTURE",
            "lineage_ref": "fixture-evidence-p3-001",
            "freshness": "NOT_MEASURED",
            "confidence": "CONTROLLED_FIXTURE_ONLY",
        }
        dict_state["receipts"] = [dict_receipt]
        dict_state["movements"] = [dict_movement]
        dict_balance["current_balance"] = n_after
        return dict_state

    def __payload(self, dict_state, str_operation, str_state_hash, str_before_hash=None, str_after_hash=None):
        dict_receipt = dict_state["receipts"][0] if dict_state["receipts"] else None
        dict_movement = dict_state["movements"][0] if dict_state["movements"] else None
        dict_balance = dict_state["balance"]
        n_before = dict_movement["before_balance"] if dict_movement else dict_balance["opening_balance"]
        n_movement = dict_movement["movement_quantity"] if dict_movement else 0
        n_after = dict_balance["current_balance"]
        return {
            "operation": {
                "name": str_operation,
                "mutationApplied": str_operation == "POST_RECEIPT",
                "stateSha256Before": str_before_hash,
                "stateSha256After": str_after_hash,
            },
            "fixture": {
                "fixtureId": dict_state["fixture_id"],
                "fixtureVersion": dict_state["fixture_version"],
                "classification": dict_state["classification"],
                "sourceClass": dict_state["source_class"],
                "freshness": dict_state["freshness"],
                "confidence": dict_state["confidence"],
                "businessTruth": dict_state["business_truth"],
                "productionTruth": dict_state["production_truth"],
                "noLiveSource": dict_state["no_live_source"],
                "stateSha256": str_state_hash,
            },
            "item": self.__item_payload(dict_state["item"]),
            "warehouse": self.__warehouse_payload(dict_state["warehouse"]),
            "location": self.__location_payload(dict_state["location"]),
            "receipt": self.__receipt_payload(dict_receipt),
            "movement": self.__movement_payload(dict_movement),
            "balance": {
                "balanceId": dict_balance["balance_id"],
                "itemId": dict_balance["item_id"],
                "warehouseId": dict_balance["warehouse_id"],
                "locationId": dict_balance["location_id"],
                "uom": dict_balance["uom"],
                "beforeBalance": n_before,
                "movementQuantity": n_movement,
                "afterBalance": n_after,
                "invariant": "BEFORE BALANCE + VALID MOVEMENT = AFTER BALANCE",
                "invariantValid": n_before + n_movement == n_after,
            },
            "transactions": [self.__transaction_payload(dict_receipt, dict_movement)] if dict_receipt and dict_movement else [],
            "crosswalk": self.__crosswalk_payload(dict_state, dict_receipt, dict_movement),
            "sourceLineage": {
                "sourceClass": dict_state["source_class"],
                "lineageRef": "fixture-evidence-p3-001",
                "freshness": dict_state["freshness"],
                "confidence": dict_state["confidence"],
                "noLiveSource": dict_state["no_live_source"],
            },
            "capabilityBoundary": {
                "readOnly": False,
                "writesSupported": True,
                "boundedReceiptOnly": True,
                "arbitraryUpdateDelete": False,
                "bulkImport": False,
                "balanceOverride": False,
                "sql": False,
                "liveC1Binding": False,
                "productionTruth": False,
            },
            "reset": dict_state["reset_rebuild"],
            "cleanup": {"owner": dict_state["reset_rebuild"]["cleanup_owner"], "state": "RESET_REQUIRED_AFTER_VALIDATION" if dict_receipt else "INITIAL_STATE"},
            "caveats": dict_state["caveats"],
        }

    def __item_payload(self, dict_item):
        return {
            "itemId": dict_item["item_id"],
            "itemNo": dict_item["item_no"],
            "itemCategory": dict_item["item_category"],
            "description": dict_item["description"],
        }

    def __warehouse_payload(self, dict_warehouse):
        return {
            "warehouseId": dict_warehouse["warehouse_id"],
            "warehouseCode": dict_warehouse["warehouse_code"],
            "name": dict_warehouse["name"],
        }

    def __location_payload(self, dict_location):
        return {
            "locationId": dict_location["location_id"],
            "locationCode": dict_location["location_code"],
            "warehouseId": dict_location["warehouse_id"],
            "name": dict_location["name"],
        }

    def __receipt_payload(self, dict_receipt):
        if not dict_receipt:
            return None
        return {
            "receiptId": dict_receipt["receipt_id"],
            "receiptNo": dict_receipt["receipt_no"],
            "itemId": dict_receipt["item_id"],
            "itemNo": dict_receipt["item_no"],
            "itemCategory": dict_receipt["item_category"],
            "warehouseId": dict_receipt["warehouse_id"],
            "warehouseCode": dict_receipt["warehouse_code"],
            "locationId": dict_receipt["location_id"],
            "locationCode": dict_receipt["location_code"],
            "quantity": dict_receipt["quantity"],
            "uom": dict_receipt["uom"],
            "transactionType": dict_receipt["transaction_type"],
            "effectivity": dict_receipt["effectivity"],
            "sourceClass": dict_receipt["source_class"],
            "lineageRef": dict_receipt["lineage_ref"],
            "freshness": dict_receipt["freshness"],
            "confidence": dict_receipt["confidence"],
        }

    def __movement_payload(self, dict_movement):
        if not dict_movement:
            return None
        return {
            "movementId": dict_movement["movement_id"],
            "transactionId": dict_movement["transaction_id"],
            "receiptId": dict_movement["receipt_id"],
            "itemId": dict_movement["item_id"],
            "itemNo": dict_movement["item_no"],
            "warehouseId": dict_movement["warehouse_id"],
            "warehouseCode": dict_movement["warehouse_code"],
            "locationId": dict_movement["location_id"],
            "locationCode": dict_movement["location_code"],
            "quantity": dict_movement["quantity"],
            "uom": dict_movement["uom"],
            "transactionType": dict_movement["transaction_type"],
            "effectivity": dict_movement["effectivity"],
            "beforeBalance": dict_movement["before_balance"],
            "movementQuantity": dict_movement["movement_quantity"],
            "afterBalance": dict_movement["after_balance"],
            "sourceClass": dict_movement["source_class"],
            "lineageRef": dict_movement["lineage_ref"],
            "freshness": dict_movement["freshness"],
            "confidence": dict_movement["confidence"],
            "invariantValid": dict_movement["before_balance"] + dict_movement["movement_quantity"] == dict_movement["after_balance"],
        }

    def __transaction_payload(self, dict_receipt, dict_movement):
        return {
            "transactionId": dict_movement["transaction_id"],
            "receiptId": dict_receipt["receipt_id"],
            "movementId": dict_movement["movement_id"],
            "receiptNo": dict_receipt["receipt_no"],
            "transactionType": dict_movement["transaction_type"],
            "effectivity": dict_movement["effectivity"],
            "evidenceLinkId": "fixture-evidence-p3-001",
        }

    def __crosswalk_payload(self, dict_state, dict_receipt, dict_movement):
        return {
            "itemId": dict_state["item"]["item_id"],
            "itemNo": dict_state["item"]["item_no"],
            "warehouseId": dict_state["warehouse"]["warehouse_id"],
            "warehouseCode": dict_state["warehouse"]["warehouse_code"],
            "locationId": dict_state["location"]["location_id"],
            "locationCode": dict_state["location"]["location_code"],
            "balanceId": dict_state["balance"]["balance_id"],
            "receiptId": dict_receipt["receipt_id"] if dict_receipt else None,
            "movementId": dict_movement["movement_id"] if dict_movement else None,
            "transactionId": dict_movement["transaction_id"] if dict_movement else None,
            "evidenceLinkId": "fixture-evidence-p3-001" if dict_movement else None,
        }

    def __error_payload(self, str_code, str_state_hash):
        return {
            "status": str_code,
            "fixtureId": self.FIXTURE_ID,
            "fixtureVersion": self.FIXTURE_VERSION,
            "sourceClass": "SYNTHETIC_FIXTURE",
            "classification": "NON-PRODUCTION / CONTROLLED VALIDATION DATA",
            "freshness": "NOT_MEASURED",
            "confidence": "CONTROLLED_FIXTURE_ONLY",
            "businessTruth": False,
            "productionTruth": False,
            "stateSha256": str_state_hash,
            "mutationApplied": False,
            "capabilityBoundary": {
                "boundedReceiptOnly": True,
                "arbitraryUpdateDelete": False,
                "bulkImport": False,
                "balanceOverride": False,
                "sql": False,
                "liveC1Binding": False,
            },
        }

    def __sha256(self, obj_path):
        obj_hash = hashlib.sha256()
        with obj_path.open("rb") as obj_file:
            for obj_chunk in iter(lambda: obj_file.read(1024 * 1024), b""):
                obj_hash.update(obj_chunk)
        return obj_hash.hexdigest().upper()


class CWarehouseFixtureP4(object):
    """Bounded reversal and idempotency adapter for the isolated P4 fixture."""

    STATE_PATH = Path(r"C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\Warehouse_Operations\ERP2-WH-P4-REVERSAL-IDEMPOTENCY-FIXTURE-001\state.json")
    FIXTURE_ID = "ERP2-WH-P4-REVERSAL-IDEMPOTENCY-FIXTURE-001"
    FIXTURE_VERSION = "1.0.0"
    REQUIRED_BODY_FIELDS = {
        "fixtureId",
        "originalTransactionId",
        "originalReceiptId",
        "itemCategory",
        "idempotencyKey",
        "reason",
        "effectivity",
    }

    class ValidationError(ValueError):
        def __init__(self, str_code, str_message, n_status_code=400):
            super().__init__(str_message)
            self.str_code = str_code
            self.n_status_code = n_status_code

    def get(self, str_timezone, str_id):
        try:
            dict_state = self.__read_state()
            self.__validate_state(dict_state)
            return 200, EErrorCode.ERROR_SUCCESS, "success", self.__payload(
                dict_state, "GET", self.__sha256(self.STATE_PATH)
            )
        except FileNotFoundError:
            return 503, EErrorCode.ERROR_OTHER_ERROR, "P4 fixture unavailable", self.__error_payload("FIXTURE_UNAVAILABLE", None)
        except (ValueError, KeyError, TypeError) as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P4 fixture invalid: %s" % str(error), self.__error_payload("FIXTURE_INVALID", None)
        except Exception as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P4 fixture read error: %s" % str(error), self.__error_payload("FIXTURE_READ_ERROR", None)

    def post(self, str_timezone, str_id):
        from flask import request

        try:
            dict_state = self.__read_state()
            self.__validate_state(dict_state)
            str_before_hash = self.__sha256(self.STATE_PATH)
            dict_body = request.get_json(silent=True)
            self.__validate_body_shape(dict_body)
            if dict_state["reversals"]:
                if dict_body == self.__expected_request(dict_state):
                    return 200, EErrorCode.ERROR_SUCCESS, "reversal replay", self.__payload(
                        dict_state, "POST_REVERSAL", str_before_hash, str_before_hash, str_before_hash, True
                    )
                if dict_body.get("idempotencyKey") == dict_state["valid_reversal"]["idempotency_key"]:
                    raise self.ValidationError("IDEMPOTENCY_CONFLICT", "same idempotency key has a conflicting payload", 409)
                raise self.ValidationError("DUPLICATE_REVERSAL", "only one controlled reversal is supported", 409)
            self.__validate_request(dict_state, dict_body)
            dict_state = self.__apply_reversal(dict_state, dict_body)
            self.__write_state(dict_state)
            str_after_hash = self.__sha256(self.STATE_PATH)
            return 201, EErrorCode.ERROR_SUCCESS, "reversal accepted", self.__payload(
                dict_state, "POST_REVERSAL", str_after_hash, str_before_hash, str_after_hash, False
            )
        except self.ValidationError as error:
            str_state_hash = self.__sha256(self.STATE_PATH) if self.STATE_PATH.exists() else None
            return error.n_status_code, EErrorCode.ERROR_INVAILD_PARAM, str(error), self.__error_payload(error.str_code, str_state_hash)
        except FileNotFoundError:
            return 503, EErrorCode.ERROR_OTHER_ERROR, "P4 fixture unavailable", self.__error_payload("FIXTURE_UNAVAILABLE", None)
        except (ValueError, KeyError, TypeError) as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P4 fixture invalid: %s" % str(error), self.__error_payload("FIXTURE_INVALID", None)
        except Exception as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P4 fixture write error: %s" % str(error), self.__error_payload("FIXTURE_WRITE_ERROR", None)

    def __read_state(self):
        with self.STATE_PATH.open("r", encoding="utf-8") as obj_file:
            return json.load(obj_file)

    def __write_state(self, dict_state):
        self.STATE_PATH.write_text(json.dumps(dict_state, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    def __validate_state(self, dict_state):
        if dict_state.get("fixture_id") != self.FIXTURE_ID:
            raise ValueError("fixture identity mismatch")
        if dict_state.get("fixture_version") != self.FIXTURE_VERSION:
            raise ValueError("fixture version mismatch")
        if dict_state.get("classification") != "NON-PRODUCTION / CONTROLLED VALIDATION DATA":
            raise ValueError("fixture classification mismatch")
        if dict_state.get("source_class") != "SYNTHETIC_FIXTURE":
            raise ValueError("fixture source classification mismatch")
        if dict_state.get("freshness") != "NOT_MEASURED" or dict_state.get("confidence") != "CONTROLLED_FIXTURE_ONLY":
            raise ValueError("fixture evidence labels mismatch")
        if dict_state.get("business_truth") is not False or dict_state.get("production_truth") is not False or dict_state.get("live_governed_binding") is not False:
            raise ValueError("fixture truth or binding flags are not disabled")
        if not isinstance(dict_state.get("reversals"), list) or len(dict_state["reversals"]) > 1:
            raise ValueError("reversal cardinality mismatch")
        dict_item = dict_state["item"]
        dict_warehouse = dict_state["warehouse"]
        dict_location = dict_state["location"]
        dict_balance = dict_state["balance"]
        dict_receipt = dict_state["original_receipt"]
        dict_movement = dict_state["original_movement"]
        dict_transaction = dict_state["original_transaction"]
        if dict_location["warehouse_id"] != dict_warehouse["warehouse_id"]:
            raise ValueError("location warehouse link mismatch")
        if dict_balance["item_id"] != dict_item["item_id"] or dict_balance["warehouse_id"] != dict_warehouse["warehouse_id"] or dict_balance["location_id"] != dict_location["location_id"]:
            raise ValueError("balance crosswalk mismatch")
        if dict_receipt["item_id"] != dict_item["item_id"] or dict_receipt["warehouse_id"] != dict_warehouse["warehouse_id"] or dict_receipt["location_id"] != dict_location["location_id"]:
            raise ValueError("original receipt crosswalk mismatch")
        if dict_movement["transaction_id"] != dict_transaction["transaction_id"] or dict_movement["receipt_id"] != dict_receipt["receipt_id"]:
            raise ValueError("original transaction links mismatch")
        if dict_movement["before_balance"] + dict_movement["movement_quantity"] != dict_movement["after_balance"]:
            raise ValueError("original balance invariant mismatch")
        if not dict_state["reversals"] and dict_balance["current_balance"] != dict_movement["after_balance"]:
            raise ValueError("baseline current balance mismatch")
        if dict_state["reversals"]:
            self.__validate_existing_reversal(dict_state)

    def __validate_existing_reversal(self, dict_state):
        dict_reversal = dict_state["reversals"][0]
        if dict_reversal["transaction_id"] != "fixture-transaction-p4-reversal-001" or dict_reversal["movement_id"] != "fixture-movement-p4-reversal-001":
            raise ValueError("reversal identity mismatch")
        if dict_reversal["original_transaction_id"] != dict_state["original_transaction"]["transaction_id"] or dict_reversal["original_receipt_id"] != dict_state["original_receipt"]["receipt_id"]:
            raise ValueError("reversal lineage mismatch")
        if dict_reversal["movement_quantity"] != -dict_state["original_receipt"]["quantity"]:
            raise ValueError("reversal quantity is not derived from original receipt")
        if dict_reversal["before_balance"] + dict_reversal["movement_quantity"] != dict_reversal["after_balance"]:
            raise ValueError("reversal balance invariant mismatch")
        if dict_state["balance"]["current_balance"] != dict_reversal["after_balance"]:
            raise ValueError("reversal current balance mismatch")

    def __validate_body_shape(self, dict_body):
        if not isinstance(dict_body, dict):
            raise self.ValidationError("INVALID_BODY", "reversal body must be an object")
        if set(dict_body) != self.REQUIRED_BODY_FIELDS:
            raise self.ValidationError("INVALID_FIELDS", "reversal body must contain exactly the supported fields")
        for str_field in self.REQUIRED_BODY_FIELDS:
            if dict_body[str_field] is None or (isinstance(dict_body[str_field], str) and not dict_body[str_field].strip()):
                raise self.ValidationError("MISSING_FIELD", "%s is required" % str_field)

    def __expected_request(self, dict_state):
        dict_original = dict_state["original_transaction"]
        dict_valid = dict_state["valid_reversal"]
        return {
            "fixtureId": self.FIXTURE_ID,
            "originalTransactionId": dict_original["transaction_id"],
            "originalReceiptId": dict_state["original_receipt"]["receipt_id"],
            "itemCategory": dict_state["item"]["item_category"],
            "idempotencyKey": dict_valid["idempotency_key"],
            "reason": dict_valid["reason"],
            "effectivity": dict_valid["effectivity"],
        }

    def __validate_request(self, dict_state, dict_body):
        if dict_body["fixtureId"] != self.FIXTURE_ID:
            raise self.ValidationError("WRONG_FIXTURE_IDENTITY", "fixtureId does not match the controlled fixture")
        if dict_body["originalTransactionId"] != dict_state["original_transaction"]["transaction_id"]:
            raise self.ValidationError("WRONG_ORIGINAL_TRANSACTION", "originalTransactionId does not match the completed receipt")
        if dict_body["originalReceiptId"] != dict_state["original_receipt"]["receipt_id"]:
            raise self.ValidationError("WRONG_ORIGINAL_RECEIPT", "originalReceiptId does not match the completed receipt")
        if dict_body["itemCategory"] != dict_state["item"]["item_category"]:
            raise self.ValidationError("WRONG_ITEM_CATEGORY", "itemCategory does not match the original material")
        dict_expected = dict_state["valid_reversal"]
        if dict_body["idempotencyKey"] != dict_expected["idempotency_key"]:
            raise self.ValidationError("UNSUPPORTED_IDEMPOTENCY_KEY", "only the authorized deterministic idempotency key is supported")
        if dict_body["reason"] != dict_expected["reason"]:
            raise self.ValidationError("UNSUPPORTED_REASON", "only RECEIPT_REVERSAL is supported")
        if dict_body["effectivity"] != dict_expected["effectivity"]:
            raise self.ValidationError("INVALID_EFFECTIVITY", "effectivity must be the authorized deterministic value")

    def __apply_reversal(self, dict_state, dict_body):
        dict_original_receipt = dict_state["original_receipt"]
        dict_original_transaction = dict_state["original_transaction"]
        dict_balance = dict_state["balance"]
        n_before = dict_balance["current_balance"]
        n_quantity = dict_original_receipt["quantity"]
        n_after = n_before - n_quantity
        dict_state["reversals"] = [{
            "transaction_id": "fixture-transaction-p4-reversal-001",
            "movement_id": "fixture-movement-p4-reversal-001",
            "original_transaction_id": dict_original_transaction["transaction_id"],
            "original_receipt_id": dict_original_receipt["receipt_id"],
            "evidence_link_id": "fixture-evidence-p4-reversal-001",
            "idempotency_key": dict_body["idempotencyKey"],
            "reason": dict_body["reason"],
            "item_id": dict_state["item"]["item_id"],
            "item_no": dict_state["item"]["item_no"],
            "warehouse_id": dict_state["warehouse"]["warehouse_id"],
            "warehouse_code": dict_state["warehouse"]["warehouse_code"],
            "location_id": dict_state["location"]["location_id"],
            "location_code": dict_state["location"]["location_code"],
            "quantity": n_quantity,
            "uom": dict_original_receipt["uom"],
            "transaction_type": "REVERSAL",
            "effectivity": dict_body["effectivity"],
            "before_balance": n_before,
            "movement_quantity": -n_quantity,
            "after_balance": n_after,
            "source_class": "SYNTHETIC_FIXTURE",
            "lineage_ref": "fixture-evidence-p4-reversal-001",
            "freshness": "NOT_MEASURED",
            "confidence": "CONTROLLED_FIXTURE_ONLY",
        }]
        dict_balance["current_balance"] = n_after
        return dict_state

    def __payload(self, dict_state, str_operation, str_state_hash, str_before_hash=None, str_after_hash=None, f_replay=False):
        dict_original_receipt = dict_state["original_receipt"]
        dict_original_movement = dict_state["original_movement"]
        dict_original_transaction = dict_state["original_transaction"]
        dict_reversal = dict_state["reversals"][0] if dict_state["reversals"] else None
        dict_balance = dict_state["balance"]
        n_before = dict_reversal["before_balance"] if dict_reversal else dict_balance["current_balance"]
        n_movement = dict_reversal["movement_quantity"] if dict_reversal else 0
        n_after = dict_balance["current_balance"]
        return {
            "operation": {
                "name": str_operation,
                "mutationApplied": str_operation == "POST_REVERSAL" and not f_replay,
                "replay": f_replay,
                "conflictStatus": "REPLAY" if f_replay else "NONE",
                "stateSha256Before": str_before_hash,
                "stateSha256After": str_after_hash,
            },
            "fixture": {
                "fixtureId": dict_state["fixture_id"],
                "fixtureVersion": dict_state["fixture_version"],
                "classification": dict_state["classification"],
                "sourceClass": dict_state["source_class"],
                "freshness": dict_state["freshness"],
                "confidence": dict_state["confidence"],
                "businessTruth": dict_state["business_truth"],
                "productionTruth": dict_state["production_truth"],
                "liveGovernedBinding": dict_state["live_governed_binding"],
                "stateSha256": str_state_hash,
            },
            "item": self.__item_payload(dict_state["item"]),
            "warehouse": self.__warehouse_payload(dict_state["warehouse"]),
            "location": self.__location_payload(dict_state["location"]),
            "originalReceipt": self.__receipt_payload(dict_state, dict_original_receipt),
            "originalMovement": self.__original_movement_payload(dict_state, dict_original_movement),
            "originalTransaction": self.__original_transaction_payload(dict_original_transaction),
            "reversalTransaction": self.__reversal_transaction_payload(dict_reversal),
            "reversalMovement": self.__reversal_movement_payload(dict_reversal),
            "balance": {
                "balanceId": dict_balance["balance_id"],
                "itemId": dict_balance["item_id"],
                "warehouseId": dict_balance["warehouse_id"],
                "locationId": dict_balance["location_id"],
                "uom": dict_balance["uom"],
                "beforeBalance": n_before,
                "movementQuantity": n_movement,
                "afterBalance": n_after,
                "invariant": "BEFORE BALANCE + VALID MOVEMENT = AFTER BALANCE",
                "invariantValid": n_before + n_movement == n_after,
            },
            "lineage": {
                "relation": "REVERSAL_OF",
                "originalTransactionId": dict_original_transaction["transaction_id"],
                "originalReceiptId": dict_original_receipt["receipt_id"],
                "originalMovementId": dict_original_movement["movement_id"],
                "reversalTransactionId": dict_reversal["transaction_id"] if dict_reversal else None,
                "reversalMovementId": dict_reversal["movement_id"] if dict_reversal else None,
                "evidenceLinkId": dict_reversal["evidence_link_id"] if dict_reversal else dict_original_transaction["evidence_link_id"],
            },
            "crosswalk": self.__crosswalk_payload(dict_state, dict_original_receipt, dict_original_movement, dict_original_transaction, dict_reversal),
            "capabilityBoundary": {
                "boundedReversalOnly": True,
                "derivedQuantityFromOriginalReceipt": True,
                "arbitraryMovementQuantity": False,
                "balanceOverride": False,
                "correction": False,
                "bulkImport": False,
                "sql": False,
                "liveGovernedBinding": False,
                "productionTruth": False,
            },
            "reset": dict_state["reset_rebuild"],
            "cleanup": {"owner": dict_state["reset_rebuild"]["cleanup_owner"], "state": "RESET_REQUIRED_AFTER_VALIDATION" if dict_reversal else "INITIAL_STATE"},
            "caveats": dict_state["caveats"],
        }

    def __item_payload(self, dict_item):
        return {
            "itemId": dict_item["item_id"],
            "itemNo": dict_item["item_no"],
            "itemCategory": dict_item["item_category"],
            "description": dict_item["description"],
        }

    def __warehouse_payload(self, dict_warehouse):
        return {
            "warehouseId": dict_warehouse["warehouse_id"],
            "warehouseCode": dict_warehouse["warehouse_code"],
            "name": dict_warehouse["name"],
        }

    def __location_payload(self, dict_location):
        return {
            "locationId": dict_location["location_id"],
            "locationCode": dict_location["location_code"],
            "warehouseId": dict_location["warehouse_id"],
            "name": dict_location["name"],
        }

    def __receipt_payload(self, dict_state, dict_receipt):
        return {
            "receiptId": dict_receipt["receipt_id"],
            "receiptNo": dict_receipt["receipt_no"],
            "itemId": dict_receipt["item_id"],
            "itemNo": dict_state["item"]["item_no"],
            "itemCategory": dict_state["item"]["item_category"],
            "warehouseId": dict_receipt["warehouse_id"],
            "warehouseCode": dict_state["warehouse"]["warehouse_code"],
            "locationId": dict_receipt["location_id"],
            "locationCode": dict_state["location"]["location_code"],
            "quantity": dict_receipt["quantity"],
            "uom": dict_receipt["uom"],
            "transactionType": dict_receipt["transaction_type"],
            "effectivity": dict_receipt["effectivity"],
            "sourceClass": dict_receipt["source_class"],
            "lineageRef": dict_receipt["lineage_ref"],
            "freshness": dict_receipt["freshness"],
            "confidence": dict_receipt["confidence"],
        }

    def __original_movement_payload(self, dict_state, dict_movement):
        return {
            "movementId": dict_movement["movement_id"],
            "transactionId": dict_movement["transaction_id"],
            "receiptId": dict_movement["receipt_id"],
            "itemId": dict_state["item"]["item_id"],
            "warehouseId": dict_state["warehouse"]["warehouse_id"],
            "locationId": dict_state["location"]["location_id"],
            "quantity": dict_movement["movement_quantity"],
            "uom": dict_state["balance"]["uom"],
            "transactionType": "RECEIPT",
            "effectivity": dict_state["original_receipt"]["effectivity"],
            "beforeBalance": dict_movement["before_balance"],
            "movementQuantity": dict_movement["movement_quantity"],
            "afterBalance": dict_movement["after_balance"],
            "sourceClass": dict_movement["source_class"],
            "lineageRef": dict_movement["lineage_ref"],
            "freshness": dict_movement["freshness"],
            "confidence": dict_movement["confidence"],
            "invariantValid": dict_movement["before_balance"] + dict_movement["movement_quantity"] == dict_movement["after_balance"],
        }

    def __original_transaction_payload(self, dict_transaction):
        return {
            "transactionId": dict_transaction["transaction_id"],
            "receiptId": dict_transaction["receipt_id"],
            "movementId": dict_transaction["movement_id"],
            "evidenceLinkId": dict_transaction["evidence_link_id"],
            "transactionType": dict_transaction["transaction_type"],
            "effectivity": dict_transaction["effectivity"],
        }

    def __reversal_transaction_payload(self, dict_reversal):
        if not dict_reversal:
            return None
        return {
            "transactionId": dict_reversal["transaction_id"],
            "originalTransactionId": dict_reversal["original_transaction_id"],
            "originalReceiptId": dict_reversal["original_receipt_id"],
            "movementId": dict_reversal["movement_id"],
            "evidenceLinkId": dict_reversal["evidence_link_id"],
            "idempotencyKey": dict_reversal["idempotency_key"],
            "reason": dict_reversal["reason"],
            "transactionType": dict_reversal["transaction_type"],
            "effectivity": dict_reversal["effectivity"],
        }

    def __reversal_movement_payload(self, dict_reversal):
        if not dict_reversal:
            return None
        return {
            "movementId": dict_reversal["movement_id"],
            "transactionId": dict_reversal["transaction_id"],
            "originalTransactionId": dict_reversal["original_transaction_id"],
            "originalReceiptId": dict_reversal["original_receipt_id"],
            "itemId": dict_reversal["item_id"],
            "itemNo": dict_reversal["item_no"],
            "warehouseId": dict_reversal["warehouse_id"],
            "warehouseCode": dict_reversal["warehouse_code"],
            "locationId": dict_reversal["location_id"],
            "locationCode": dict_reversal["location_code"],
            "quantity": dict_reversal["quantity"],
            "uom": dict_reversal["uom"],
            "transactionType": dict_reversal["transaction_type"],
            "reason": dict_reversal["reason"],
            "effectivity": dict_reversal["effectivity"],
            "beforeBalance": dict_reversal["before_balance"],
            "movementQuantity": dict_reversal["movement_quantity"],
            "afterBalance": dict_reversal["after_balance"],
            "sourceClass": dict_reversal["source_class"],
            "lineageRef": dict_reversal["lineage_ref"],
            "freshness": dict_reversal["freshness"],
            "confidence": dict_reversal["confidence"],
            "invariantValid": dict_reversal["before_balance"] + dict_reversal["movement_quantity"] == dict_reversal["after_balance"],
        }

    def __crosswalk_payload(self, dict_state, dict_receipt, dict_movement, dict_transaction, dict_reversal):
        return {
            "itemId": dict_state["item"]["item_id"],
            "itemNo": dict_state["item"]["item_no"],
            "warehouseId": dict_state["warehouse"]["warehouse_id"],
            "warehouseCode": dict_state["warehouse"]["warehouse_code"],
            "locationId": dict_state["location"]["location_id"],
            "locationCode": dict_state["location"]["location_code"],
            "balanceId": dict_state["balance"]["balance_id"],
            "originalReceiptId": dict_receipt["receipt_id"],
            "originalMovementId": dict_movement["movement_id"],
            "originalTransactionId": dict_transaction["transaction_id"],
            "originalEvidenceLinkId": dict_transaction["evidence_link_id"],
            "reversalTransactionId": dict_reversal["transaction_id"] if dict_reversal else None,
            "reversalMovementId": dict_reversal["movement_id"] if dict_reversal else None,
            "reversalEvidenceLinkId": dict_reversal["evidence_link_id"] if dict_reversal else None,
        }

    def __error_payload(self, str_code, str_state_hash):
        return {
            "status": str_code,
            "fixtureId": self.FIXTURE_ID,
            "fixtureVersion": self.FIXTURE_VERSION,
            "classification": "NON-PRODUCTION / CONTROLLED VALIDATION DATA",
            "sourceClass": "SYNTHETIC_FIXTURE",
            "freshness": "NOT_MEASURED",
            "confidence": "CONTROLLED_FIXTURE_ONLY",
            "businessTruth": False,
            "productionTruth": False,
            "stateSha256": str_state_hash,
            "mutationApplied": False,
            "replay": False,
            "capabilityBoundary": {
                "boundedReversalOnly": True,
                "derivedQuantityFromOriginalReceipt": True,
                "arbitraryMovementQuantity": False,
                "balanceOverride": False,
                "correction": False,
                "bulkImport": False,
                "sql": False,
                "liveGovernedBinding": False,
            },
        }

    def __sha256(self, obj_path):
        obj_hash = hashlib.sha256()
        with obj_path.open("rb") as obj_file:
            for obj_chunk in iter(lambda: obj_file.read(1024 * 1024), b""):
                obj_hash.update(obj_chunk)
        return obj_hash.hexdigest().upper()


class CWarehouseFixtureP5(object):
    """Bounded signed adjustment and reconciliation adapter for P5."""

    STATE_PATH = Path(r"C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\Warehouse_Operations\ERP2-WH-P5-ADJUSTMENT-RECONCILIATION-FIXTURE-001\state.json")
    FIXTURE_ID = "ERP2-WH-P5-ADJUSTMENT-RECONCILIATION-FIXTURE-001"
    FIXTURE_VERSION = "1.0.0"
    REQUIRED_BODY_FIELDS = {
        "fixtureId",
        "itemNo",
        "itemCategory",
        "warehouseCode",
        "locationCode",
        "referenceTransactionId",
        "idempotencyKey",
        "signedAdjustmentDelta",
        "uom",
        "operationType",
        "reason",
        "effectivity",
    }

    class ValidationError(ValueError):
        def __init__(self, str_code, str_message, n_status_code=400):
            super().__init__(str_message)
            self.str_code = str_code
            self.n_status_code = n_status_code

    def get(self, str_timezone, str_id):
        try:
            dict_state = self.__read_state()
            self.__validate_state(dict_state)
            return 200, EErrorCode.ERROR_SUCCESS, "success", self.__payload(
                dict_state, "GET", self.__sha256(self.STATE_PATH)
            )
        except FileNotFoundError:
            return 503, EErrorCode.ERROR_OTHER_ERROR, "P5 fixture unavailable", self.__error_payload("FIXTURE_UNAVAILABLE", None)
        except (ValueError, KeyError, TypeError) as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P5 fixture invalid: %s" % str(error), self.__error_payload("FIXTURE_INVALID", None)
        except Exception as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P5 fixture read error: %s" % str(error), self.__error_payload("FIXTURE_READ_ERROR", None)

    def post(self, str_timezone, str_id):
        from flask import request

        try:
            dict_state = self.__read_state()
            self.__validate_state(dict_state)
            str_before_hash = self.__sha256(self.STATE_PATH)
            dict_body = request.get_json(silent=True)
            self.__validate_body_shape(dict_body)
            if dict_state["adjustments"]:
                if dict_body == self.__expected_request(dict_state):
                    return 200, EErrorCode.ERROR_SUCCESS, "adjustment replay", self.__payload(
                        dict_state, "POST_ADJUSTMENT", str_before_hash, str_before_hash, str_before_hash, True
                    )
                if dict_body.get("idempotencyKey") == dict_state["valid_adjustment"]["idempotency_key"]:
                    raise self.ValidationError("IDEMPOTENCY_CONFLICT", "same idempotency key has a conflicting payload", 409)
                raise self.ValidationError("DUPLICATE_REFERENCE_ADJUSTMENT", "only one adjustment for the reference transaction is supported", 409)
            self.__validate_request(dict_state, dict_body)
            dict_state = self.__apply_adjustment(dict_state, dict_body)
            self.__write_state(dict_state)
            str_after_hash = self.__sha256(self.STATE_PATH)
            return 201, EErrorCode.ERROR_SUCCESS, "adjustment accepted", self.__payload(
                dict_state, "POST_ADJUSTMENT", str_after_hash, str_before_hash, str_after_hash, False
            )
        except self.ValidationError as error:
            str_state_hash = self.__sha256(self.STATE_PATH) if self.STATE_PATH.exists() else None
            return error.n_status_code, EErrorCode.ERROR_INVAILD_PARAM, str(error), self.__error_payload(error.str_code, str_state_hash)
        except FileNotFoundError:
            return 503, EErrorCode.ERROR_OTHER_ERROR, "P5 fixture unavailable", self.__error_payload("FIXTURE_UNAVAILABLE", None)
        except (ValueError, KeyError, TypeError) as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P5 fixture invalid: %s" % str(error), self.__error_payload("FIXTURE_INVALID", None)
        except Exception as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P5 fixture write error: %s" % str(error), self.__error_payload("FIXTURE_WRITE_ERROR", None)

    def __read_state(self):
        with self.STATE_PATH.open("r", encoding="utf-8") as obj_file:
            return json.load(obj_file)

    def __write_state(self, dict_state):
        self.STATE_PATH.write_text(json.dumps(dict_state, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    def __validate_state(self, dict_state):
        if dict_state.get("fixture_id") != self.FIXTURE_ID:
            raise ValueError("fixture identity mismatch")
        if dict_state.get("fixture_version") != self.FIXTURE_VERSION:
            raise ValueError("fixture version mismatch")
        if dict_state.get("classification") != "NON-PRODUCTION / CONTROLLED VALIDATION DATA":
            raise ValueError("fixture classification mismatch")
        if dict_state.get("source_class") != "SYNTHETIC_FIXTURE":
            raise ValueError("fixture source classification mismatch")
        if dict_state.get("freshness") != "NOT_MEASURED" or dict_state.get("confidence") != "CONTROLLED_FIXTURE_ONLY":
            raise ValueError("fixture evidence labels mismatch")
        if dict_state.get("business_truth") is not False or dict_state.get("production_truth") is not False or dict_state.get("live_governed_binding") is not False:
            raise ValueError("fixture truth or binding flags are not disabled")
        if not isinstance(dict_state.get("adjustments"), list) or len(dict_state["adjustments"]) > 1:
            raise ValueError("adjustment cardinality mismatch")
        dict_item = dict_state["item"]
        dict_warehouse = dict_state["warehouse"]
        dict_location = dict_state["location"]
        dict_balance = dict_state["balance"]
        dict_reference = dict_state["reference_transaction"]
        if dict_location["warehouse_id"] != dict_warehouse["warehouse_id"]:
            raise ValueError("location warehouse link mismatch")
        if dict_balance["item_id"] != dict_item["item_id"] or dict_balance["warehouse_id"] != dict_warehouse["warehouse_id"] or dict_balance["location_id"] != dict_location["location_id"]:
            raise ValueError("balance crosswalk mismatch")
        if dict_reference["baseline_balance"] != dict_balance["opening_balance"]:
            raise ValueError("reference baseline mismatch")
        if not dict_state["adjustments"] and dict_balance["current_balance"] != dict_reference["baseline_balance"]:
            raise ValueError("baseline current balance mismatch")
        if dict_state["adjustments"]:
            self.__validate_existing_adjustment(dict_state)

    def __validate_existing_adjustment(self, dict_state):
        dict_adjustment = dict_state["adjustments"][0]
        if dict_adjustment["transaction_id"] != "fixture-transaction-p5-adjustment-001" or dict_adjustment["movement_id"] != "fixture-movement-p5-adjustment-001":
            raise ValueError("adjustment identity mismatch")
        if dict_adjustment["reference_transaction_id"] != dict_state["reference_transaction"]["transaction_id"]:
            raise ValueError("adjustment reference link mismatch")
        if dict_adjustment["before_balance"] + dict_adjustment["signed_adjustment_delta"] != dict_adjustment["after_balance"]:
            raise ValueError("adjustment balance invariant mismatch")
        if dict_state["balance"]["current_balance"] != dict_adjustment["after_balance"]:
            raise ValueError("adjustment current balance mismatch")

    def __validate_body_shape(self, dict_body):
        if not isinstance(dict_body, dict):
            raise self.ValidationError("INVALID_BODY", "adjustment body must be an object")
        if set(dict_body) != self.REQUIRED_BODY_FIELDS:
            raise self.ValidationError("INVALID_FIELDS", "adjustment body must contain exactly the supported fields")
        for str_field in self.REQUIRED_BODY_FIELDS:
            if dict_body[str_field] is None or (isinstance(dict_body[str_field], str) and not dict_body[str_field].strip()):
                raise self.ValidationError("MISSING_FIELD", "%s is required" % str_field)

    def __expected_request(self, dict_state):
        dict_valid = dict_state["valid_adjustment"]
        return {
            "fixtureId": self.FIXTURE_ID,
            "itemNo": dict_valid["item_no"],
            "itemCategory": dict_valid["item_category"],
            "warehouseCode": dict_valid["warehouse_code"],
            "locationCode": dict_valid["location_code"],
            "referenceTransactionId": dict_valid["reference_transaction_id"],
            "idempotencyKey": dict_valid["idempotency_key"],
            "signedAdjustmentDelta": dict_valid["signed_adjustment_delta"],
            "uom": dict_valid["uom"],
            "operationType": dict_valid["operation_type"],
            "reason": dict_valid["reason"],
            "effectivity": dict_valid["effectivity"],
        }

    def __validate_request(self, dict_state, dict_body):
        if dict_body["fixtureId"] != self.FIXTURE_ID:
            raise self.ValidationError("WRONG_FIXTURE_IDENTITY", "fixtureId does not match the controlled fixture")
        dict_item = dict_state["item"]
        dict_warehouse = dict_state["warehouse"]
        dict_location = dict_state["location"]
        if dict_body["itemNo"] != dict_item["item_no"]:
            raise self.ValidationError("WRONG_ITEM_IDENTITY", "itemNo does not match the controlled material")
        if dict_body["itemCategory"] != dict_item["item_category"]:
            raise self.ValidationError("WRONG_ITEM_CATEGORY", "itemCategory does not match the controlled material")
        if dict_body["warehouseCode"] != dict_warehouse["warehouse_code"] or dict_body["locationCode"] != dict_location["location_code"]:
            raise self.ValidationError("WRONG_LOCATION_IDENTITY", "Warehouse or location does not match the controlled balance")
        if dict_body["referenceTransactionId"] != dict_state["reference_transaction"]["transaction_id"]:
            raise self.ValidationError("WRONG_REFERENCE_TRANSACTION", "referenceTransactionId does not match the controlled baseline")
        if isinstance(dict_body["signedAdjustmentDelta"], bool) or not isinstance(dict_body["signedAdjustmentDelta"], (int, float)):
            raise self.ValidationError("INVALID_DELTA", "signedAdjustmentDelta must be numeric")
        if dict_body["signedAdjustmentDelta"] == 0:
            raise self.ValidationError("ZERO_DELTA", "signedAdjustmentDelta must be non-zero")
        if abs(dict_body["signedAdjustmentDelta"]) > dict_state["max_abs_delta"]:
            raise self.ValidationError("DELTA_OVERFLOW", "signedAdjustmentDelta exceeds the controlled bound")
        dict_valid = dict_state["valid_adjustment"]
        if dict_body["signedAdjustmentDelta"] != dict_valid["signed_adjustment_delta"]:
            raise self.ValidationError("UNSUPPORTED_DELTA", "only the authorized deterministic signed delta is supported")
        for str_body_field, str_state_field in (("idempotencyKey", "idempotency_key"), ("uom", "uom"), ("operationType", "operation_type"), ("reason", "reason"), ("effectivity", "effectivity")):
            if dict_body[str_body_field] != dict_valid[str_state_field]:
                str_code = "UNSUPPORTED_REASON" if str_body_field == "reason" else "INVALID_EFFECTIVITY" if str_body_field == "effectivity" else "UNSUPPORTED_%s" % str_body_field.upper()
                raise self.ValidationError(str_code, "%s is not the authorized deterministic value" % str_body_field)

    def __apply_adjustment(self, dict_state, dict_body):
        dict_balance = dict_state["balance"]
        n_before = dict_balance["current_balance"]
        n_delta = dict_body["signedAdjustmentDelta"]
        n_after = n_before + n_delta
        dict_state["adjustments"] = [{
            "transaction_id": "fixture-transaction-p5-adjustment-001",
            "movement_id": "fixture-movement-p5-adjustment-001",
            "evidence_link_id": "fixture-evidence-p5-adjustment-001",
            "reference_transaction_id": dict_body["referenceTransactionId"],
            "idempotency_key": dict_body["idempotencyKey"],
            "item_id": dict_state["item"]["item_id"],
            "item_no": dict_state["item"]["item_no"],
            "warehouse_id": dict_state["warehouse"]["warehouse_id"],
            "warehouse_code": dict_state["warehouse"]["warehouse_code"],
            "location_id": dict_state["location"]["location_id"],
            "location_code": dict_state["location"]["location_code"],
            "item_category": dict_state["item"]["item_category"],
            "signed_adjustment_delta": n_delta,
            "uom": dict_body["uom"],
            "operation_type": dict_body["operationType"],
            "reason": dict_body["reason"],
            "effectivity": dict_body["effectivity"],
            "before_balance": n_before,
            "after_balance": n_after,
            "source_class": "SYNTHETIC_FIXTURE",
            "lineage_ref": "fixture-evidence-p5-adjustment-001",
            "freshness": "NOT_MEASURED",
            "confidence": "CONTROLLED_FIXTURE_ONLY",
        }]
        dict_balance["current_balance"] = n_after
        return dict_state

    def __payload(self, dict_state, str_operation, str_state_hash, str_before_hash=None, str_after_hash=None, f_replay=False):
        dict_item = dict_state["item"]
        dict_warehouse = dict_state["warehouse"]
        dict_location = dict_state["location"]
        dict_reference = dict_state["reference_transaction"]
        dict_adjustment = dict_state["adjustments"][0] if dict_state["adjustments"] else None
        dict_balance = dict_state["balance"]
        n_before = dict_adjustment["before_balance"] if dict_adjustment else dict_balance["current_balance"]
        n_delta = dict_adjustment["signed_adjustment_delta"] if dict_adjustment else 0
        n_after = dict_balance["current_balance"]
        return {
            "operation": {
                "name": str_operation,
                "mutationApplied": str_operation == "POST_ADJUSTMENT" and not f_replay,
                "replay": f_replay,
                "conflictStatus": "REPLAY" if f_replay else "NONE",
                "stateSha256Before": str_before_hash,
                "stateSha256After": str_after_hash,
            },
            "fixture": {
                "fixtureId": dict_state["fixture_id"],
                "fixtureVersion": dict_state["fixture_version"],
                "classification": dict_state["classification"],
                "sourceClass": dict_state["source_class"],
                "freshness": dict_state["freshness"],
                "confidence": dict_state["confidence"],
                "businessTruth": dict_state["business_truth"],
                "productionTruth": dict_state["production_truth"],
                "liveGovernedBinding": dict_state["live_governed_binding"],
                "stateSha256": str_state_hash,
            },
            "item": self.__item_payload(dict_item),
            "warehouse": self.__warehouse_payload(dict_warehouse),
            "location": self.__location_payload(dict_location),
            "referenceTransaction": {
                "transactionId": dict_reference["transaction_id"],
                "movementId": dict_reference["movement_id"],
                "evidenceLinkId": dict_reference["evidence_link_id"],
                "transactionType": dict_reference["transaction_type"],
                "effectivity": dict_reference["effectivity"],
                "baselineBalance": dict_reference["baseline_balance"],
            },
            "adjustmentTransaction": self.__adjustment_transaction_payload(dict_adjustment),
            "adjustmentMovement": self.__adjustment_movement_payload(dict_adjustment),
            "balance": {
                "balanceId": dict_balance["balance_id"],
                "itemId": dict_balance["item_id"],
                "warehouseId": dict_balance["warehouse_id"],
                "locationId": dict_balance["location_id"],
                "uom": dict_balance["uom"],
                "baselineBalance": n_before,
                "signedAdjustmentDelta": n_delta,
                "afterBalance": n_after,
                "invariant": "BASELINE BALANCE + SIGNED ADJUSTMENT DELTA = AFTER BALANCE",
                "invariantValid": n_before + n_delta == n_after,
            },
            "reconciliation": {
                "referenceAfterBalance": dict_state["reconciliation_reference_after_balance"],
                "computedAfterBalance": n_after,
                "difference": n_after - dict_state["reconciliation_reference_after_balance"],
                "status": "CONFLICTING" if n_after != dict_state["reconciliation_reference_after_balance"] else "CONFIRMED",
                "automaticResolution": False,
            },
            "crosswalk": self.__crosswalk_payload(dict_state, dict_reference, dict_adjustment),
            "sourceLineage": {
                "sourceClass": dict_state["source_class"],
                "lineageRef": dict_adjustment["lineage_ref"] if dict_adjustment else "fixture-evidence-p5-reference-001",
                "freshness": dict_state["freshness"],
                "confidence": dict_state["confidence"],
                "noLiveSource": True,
            },
            "capabilityBoundary": {
                "boundedAdjustmentOnly": True,
                "signedDeltaRequired": True,
                "correctionReplacement": False,
                "arbitraryMovementQuantity": False,
                "balanceOverride": False,
                "bulkImport": False,
                "sql": False,
                "liveGovernedBinding": False,
                "productionTruth": False,
            },
            "reset": dict_state["reset_rebuild"],
            "cleanup": {"owner": dict_state["reset_rebuild"]["cleanup_owner"], "state": "RESET_REQUIRED_AFTER_VALIDATION" if dict_adjustment else "INITIAL_STATE"},
            "caveats": dict_state["caveats"],
        }

    def __item_payload(self, dict_item):
        return {"itemId": dict_item["item_id"], "itemNo": dict_item["item_no"], "itemCategory": dict_item["item_category"], "description": dict_item["description"]}

    def __warehouse_payload(self, dict_warehouse):
        return {"warehouseId": dict_warehouse["warehouse_id"], "warehouseCode": dict_warehouse["warehouse_code"], "name": dict_warehouse["name"]}

    def __location_payload(self, dict_location):
        return {"locationId": dict_location["location_id"], "locationCode": dict_location["location_code"], "warehouseId": dict_location["warehouse_id"], "name": dict_location["name"]}

    def __adjustment_transaction_payload(self, dict_adjustment):
        if not dict_adjustment:
            return None
        return {
            "transactionId": dict_adjustment["transaction_id"],
            "referenceTransactionId": dict_adjustment["reference_transaction_id"],
            "movementId": dict_adjustment["movement_id"],
            "evidenceLinkId": dict_adjustment["evidence_link_id"],
            "idempotencyKey": dict_adjustment["idempotency_key"],
            "operationType": dict_adjustment["operation_type"],
            "reason": dict_adjustment["reason"],
            "effectivity": dict_adjustment["effectivity"],
        }

    def __adjustment_movement_payload(self, dict_adjustment):
        if not dict_adjustment:
            return None
        return {
            "movementId": dict_adjustment["movement_id"],
            "transactionId": dict_adjustment["transaction_id"],
            "referenceTransactionId": dict_adjustment["reference_transaction_id"],
            "itemId": dict_adjustment["item_id"],
            "itemNo": dict_adjustment["item_no"],
            "itemCategory": dict_adjustment["item_category"],
            "warehouseId": dict_adjustment["warehouse_id"],
            "warehouseCode": dict_adjustment["warehouse_code"],
            "locationId": dict_adjustment["location_id"],
            "locationCode": dict_adjustment["location_code"],
            "signedAdjustmentDelta": dict_adjustment["signed_adjustment_delta"],
            "movementQuantity": dict_adjustment["signed_adjustment_delta"],
            "quantity": abs(dict_adjustment["signed_adjustment_delta"]),
            "uom": dict_adjustment["uom"],
            "operationType": dict_adjustment["operation_type"],
            "reason": dict_adjustment["reason"],
            "effectivity": dict_adjustment["effectivity"],
            "beforeBalance": dict_adjustment["before_balance"],
            "afterBalance": dict_adjustment["after_balance"],
            "sourceClass": dict_adjustment["source_class"],
            "lineageRef": dict_adjustment["lineage_ref"],
            "freshness": dict_adjustment["freshness"],
            "confidence": dict_adjustment["confidence"],
            "invariantValid": dict_adjustment["before_balance"] + dict_adjustment["signed_adjustment_delta"] == dict_adjustment["after_balance"],
        }

    def __crosswalk_payload(self, dict_state, dict_reference, dict_adjustment):
        return {
            "itemId": dict_state["item"]["item_id"],
            "itemNo": dict_state["item"]["item_no"],
            "warehouseId": dict_state["warehouse"]["warehouse_id"],
            "warehouseCode": dict_state["warehouse"]["warehouse_code"],
            "locationId": dict_state["location"]["location_id"],
            "locationCode": dict_state["location"]["location_code"],
            "balanceId": dict_state["balance"]["balance_id"],
            "referenceTransactionId": dict_reference["transaction_id"],
            "referenceMovementId": dict_reference["movement_id"],
            "referenceEvidenceLinkId": dict_reference["evidence_link_id"],
            "adjustmentTransactionId": dict_adjustment["transaction_id"] if dict_adjustment else None,
            "adjustmentMovementId": dict_adjustment["movement_id"] if dict_adjustment else None,
            "adjustmentEvidenceLinkId": dict_adjustment["evidence_link_id"] if dict_adjustment else None,
        }

    def __error_payload(self, str_code, str_state_hash):
        return {
            "status": str_code,
            "fixtureId": self.FIXTURE_ID,
            "fixtureVersion": self.FIXTURE_VERSION,
            "classification": "NON-PRODUCTION / CONTROLLED VALIDATION DATA",
            "sourceClass": "SYNTHETIC_FIXTURE",
            "freshness": "NOT_MEASURED",
            "confidence": "CONTROLLED_FIXTURE_ONLY",
            "businessTruth": False,
            "productionTruth": False,
            "stateSha256": str_state_hash,
            "mutationApplied": False,
            "replay": False,
            "capabilityBoundary": {
                "boundedAdjustmentOnly": True,
                "signedDeltaRequired": True,
                "correctionReplacement": False,
                "arbitraryMovementQuantity": False,
                "balanceOverride": False,
                "bulkImport": False,
                "sql": False,
                "liveGovernedBinding": False,
            },
        }

    def __sha256(self, obj_path):
        obj_hash = hashlib.sha256()
        with obj_path.open("rb") as obj_file:
            for obj_chunk in iter(lambda: obj_file.read(1024 * 1024), b""):
                obj_hash.update(obj_chunk)
        return obj_hash.hexdigest().upper()


class CWarehouseFixtureP6(object):
    """Non-effective correction proposal and impact-preview adapter for P6."""

    STATE_PATH = Path(r"C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\Warehouse_Operations\ERP2-WH-P6-PROPOSAL-ONLY-FIXTURE-001\state.json")
    FIXTURE_ID = "ERP2-WH-P6-PROPOSAL-ONLY-FIXTURE-001"
    FIXTURE_VERSION = "1.0.0"
    PREVIEW_LABEL = "PREVIEW ONLY / NOT OFFICIAL BALANCE"
    BLOCKED_LABEL = "REVIEW / BLOCKED PREVIEW CONDITION"
    REQUIRED_BODY_FIELDS = {
        "proposalId",
        "originalTransactionId",
        "originalSource",
        "originalSourceRecordId",
        "originalTransactionType",
        "originalItemId",
        "originalItemCategory",
        "warehouseCode",
        "locationCode",
        "proposalType",
        "proposedQuantity",
        "reasonCode",
        "reasonText",
        "proposerId",
        "proposerRole",
        "createdAt",
        "proposedEffectiveDate",
        "idempotencyKey",
        "reviewNote",
        "policyReference",
    }
    ALLOWED_STATUS_SET = {"DRAFT", "PROPOSED", "REVIEW_REQUIRED", "REJECTED", "CANCELLED"}

    class ValidationError(ValueError):
        def __init__(self, str_code, str_message, n_status_code=400):
            super().__init__(str_message)
            self.str_code = str_code
            self.n_status_code = n_status_code

    def get(self, str_timezone, str_id):
        try:
            dict_state = self.__read_state()
            self.__validate_state(dict_state)
            return 200, EErrorCode.ERROR_SUCCESS, "success", self.__payload(
                dict_state, "GET", self.__sha256(self.STATE_PATH)
            )
        except FileNotFoundError:
            return 503, EErrorCode.ERROR_OTHER_ERROR, "P6 fixture unavailable", self.__error_payload("FIXTURE_UNAVAILABLE", None, [])
        except (ValueError, KeyError, TypeError) as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P6 fixture invalid: %s" % str(error), self.__error_payload("FIXTURE_INVALID", None, [])
        except Exception as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P6 fixture read error: %s" % str(error), self.__error_payload("FIXTURE_READ_ERROR", None, [])

    def post(self, str_timezone, str_id):
        from flask import request

        try:
            dict_state = self.__read_state()
            self.__validate_state(dict_state)
            str_before_hash = self.__sha256(self.STATE_PATH)
            dict_body = request.get_json(silent=True)
            self.__validate_body_shape(dict_body)
            if dict_state["proposals"]:
                if dict_body == self.__expected_request(dict_state):
                    return 200, EErrorCode.ERROR_SUCCESS, "proposal replay", self.__payload(
                        dict_state, "POST_PROPOSAL", str_before_hash, str_before_hash, str_before_hash, True
                    )
                if dict_body.get("idempotencyKey") == dict_state["valid_proposal"]["idempotency_key"]:
                    raise self.ValidationError("IDEMPOTENCY_CONFLICT", "same idempotency key has conflicting proposal content", 409)
                raise self.ValidationError("DUPLICATE_PROPOSAL_REFERENCE", "only one proposal for the original reference is supported", 409)
            self.__validate_request(dict_state, dict_body)
            dict_state = self.__apply_proposal(dict_state, dict_body)
            self.__write_state(dict_state)
            str_after_hash = self.__sha256(self.STATE_PATH)
            return 201, EErrorCode.ERROR_SUCCESS, "proposal created for preview", self.__payload(
                dict_state, "POST_PROPOSAL", str_after_hash, str_before_hash, str_after_hash, False
            )
        except self.ValidationError as error:
            str_state_hash = self.__sha256(self.STATE_PATH) if self.STATE_PATH.exists() else None
            lst_conditions = [{"code": error.str_code, "message": str(error)}]
            return error.n_status_code, EErrorCode.ERROR_INVAILD_PARAM, str(error), self.__error_payload(error.str_code, str_state_hash, lst_conditions)
        except FileNotFoundError:
            return 503, EErrorCode.ERROR_OTHER_ERROR, "P6 fixture unavailable", self.__error_payload("FIXTURE_UNAVAILABLE", None, [])
        except (ValueError, KeyError, TypeError) as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P6 fixture invalid: %s" % str(error), self.__error_payload("FIXTURE_INVALID", None, [])
        except Exception as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P6 fixture write error: %s" % str(error), self.__error_payload("FIXTURE_WRITE_ERROR", None, [])

    def __read_state(self):
        with self.STATE_PATH.open("r", encoding="utf-8") as obj_file:
            return json.load(obj_file)

    def __write_state(self, dict_state):
        self.STATE_PATH.write_text(json.dumps(dict_state, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    def __validate_state(self, dict_state):
        if dict_state.get("fixture_id") != self.FIXTURE_ID:
            raise ValueError("fixture identity mismatch")
        if dict_state.get("fixture_version") != self.FIXTURE_VERSION:
            raise ValueError("fixture version mismatch")
        if dict_state.get("classification") != "NON-PRODUCTION / CONTROLLED VALIDATION DATA":
            raise ValueError("fixture classification mismatch")
        if dict_state.get("source_class") != "SYNTHETIC_FIXTURE":
            raise ValueError("fixture source classification mismatch")
        if dict_state.get("freshness") != "NOT_MEASURED" or dict_state.get("confidence") != "CONTROLLED_FIXTURE_ONLY":
            raise ValueError("fixture evidence labels mismatch")
        if dict_state.get("business_truth") is not False or dict_state.get("production_truth") is not False or dict_state.get("live_governed_binding") is not False:
            raise ValueError("fixture truth or binding flags are not disabled")
        if set(dict_state.get("allowed_statuses", [])) != self.ALLOWED_STATUS_SET:
            raise ValueError("proposal status catalog mismatch")
        if not isinstance(dict_state.get("proposals"), list) or len(dict_state["proposals"]) > 1:
            raise ValueError("proposal cardinality mismatch")
        dict_item = dict_state["item"]
        dict_warehouse = dict_state["warehouse"]
        dict_location = dict_state["location"]
        dict_balance = dict_state["balance"]
        dict_original = dict_state["original_evidence"]
        if dict_location["warehouse_id"] != dict_warehouse["warehouse_id"]:
            raise ValueError("location warehouse link mismatch")
        if dict_balance["item_id"] != dict_item["item_id"] or dict_balance["warehouse_id"] != dict_warehouse["warehouse_id"] or dict_balance["location_id"] != dict_location["location_id"]:
            raise ValueError("balance crosswalk mismatch")
        if dict_original["item_id"] != dict_item["item_id"] or dict_original["item_category"] != dict_item["item_category"] or dict_original["warehouse_code"] != dict_warehouse["warehouse_code"] or dict_original["location_code"] != dict_location["location_code"]:
            raise ValueError("original evidence crosswalk mismatch")
        if dict_original.get("original_evidence_sha256") and dict_original["original_evidence_sha256"] != self.__original_evidence_hash(dict_original):
            raise ValueError("original evidence hash mismatch")
        if dict_state["proposals"]:
            self.__validate_existing_proposal(dict_state)

    def __validate_existing_proposal(self, dict_state):
        dict_proposal = dict_state["proposals"][0]
        if dict_proposal["status"] not in self.ALLOWED_STATUS_SET:
            raise ValueError("proposal status outside non-effective catalog")
        if dict_proposal["original_transaction_id"] != dict_state["original_evidence"]["transaction_id"]:
            raise ValueError("proposal original lineage mismatch")
        if dict_proposal["before_quantity"] + dict_proposal["proposed_delta"] != dict_proposal["after_quantity"]:
            raise ValueError("proposal preview invariant mismatch")
        if dict_proposal["proposal_evidence_sha256"] != self.__proposal_evidence_hash(dict_proposal):
            raise ValueError("proposal evidence hash mismatch")
        if dict_state["balance"]["current_balance"] != dict_state["original_evidence"]["quantity"]:
            raise ValueError("authoritative fixture balance changed")

    def __validate_body_shape(self, dict_body):
        if not isinstance(dict_body, dict):
            raise self.ValidationError("MALFORMED_INPUT", "proposal body must be an object")
        if set(dict_body) != self.REQUIRED_BODY_FIELDS:
            raise self.ValidationError("MALFORMED_INPUT", "proposal body must contain exactly the supported fields")

    def __expected_request(self, dict_state):
        dict_valid = dict_state["valid_proposal"]
        return {
            "proposalId": "fixture-proposal-p6-001",
            "originalTransactionId": dict_state["original_evidence"]["transaction_id"],
            "originalSource": "P6_CONTROLLED_ORIGINAL_EVIDENCE",
            "originalSourceRecordId": "fixture-source-record-p6-original-001",
            "originalTransactionType": "RECEIPT",
            "originalItemId": dict_state["item"]["item_id"],
            "originalItemCategory": dict_state["item"]["item_category"],
            "warehouseCode": dict_state["warehouse"]["warehouse_code"],
            "locationCode": dict_state["location"]["location_code"],
            "proposalType": dict_valid["proposal_type"],
            "proposedQuantity": dict_valid["proposed_quantity"],
            "reasonCode": dict_valid["reason_code"],
            "reasonText": dict_valid["reason_text"],
            "proposerId": dict_valid["proposer_id"],
            "proposerRole": dict_valid["proposer_role"],
            "createdAt": dict_valid["created_at"],
            "proposedEffectiveDate": dict_valid["proposed_effective_date"],
            "idempotencyKey": dict_valid["idempotency_key"],
            "reviewNote": dict_valid["review_note"],
            "policyReference": dict_valid["policy_reference"],
        }

    def __validate_request(self, dict_state, dict_body):
        dict_original = dict_state["original_evidence"]
        dict_item = dict_state["item"]
        dict_warehouse = dict_state["warehouse"]
        dict_location = dict_state["location"]
        if not dict_body["originalTransactionId"] or not dict_body["originalSource"] or not dict_body["originalSourceRecordId"] or not dict_body["originalItemId"]:
            raise self.ValidationError("MISSING_LINEAGE", "%s: immutable original lineage is required" % self.BLOCKED_LABEL, 409)
        if dict_body["originalTransactionId"] != dict_original["transaction_id"] or dict_body["originalSource"] != dict_original["source"] or dict_body["originalSourceRecordId"] != dict_original["source_record_id"] or dict_body["originalTransactionType"] != dict_original["transaction_type"] or dict_body["originalItemId"] != dict_item["item_id"] or dict_body["originalItemCategory"] != dict_item["item_category"] or dict_body["warehouseCode"] != dict_warehouse["warehouse_code"] or dict_body["locationCode"] != dict_location["location_code"]:
            raise self.ValidationError("INVALID_LINEAGE", "%s: original evidence identity does not match" % self.BLOCKED_LABEL, 409)
        if dict_body["proposalType"] == "REPLACEMENT_DETAIL_PROPOSAL":
            raise self.ValidationError("REPLACEMENT_ORDER_DEPENDENCY", "%s: replacement-order dependency is preview-blocked" % self.BLOCKED_LABEL, 409)
        if not dict_body["reasonCode"] or not dict_body["reasonText"] or dict_body["reasonCode"] != dict_state["valid_proposal"]["reason_code"]:
            raise self.ValidationError("INVALID_REASON", "%s: reason is not package-approved" % self.BLOCKED_LABEL, 409)
        if isinstance(dict_body["proposedQuantity"], bool) or not isinstance(dict_body["proposedQuantity"], (int, float)):
            raise self.ValidationError("MALFORMED_INPUT", "proposedQuantity must be numeric")
        if dict_body["proposedQuantity"] <= 0:
            raise self.ValidationError("NEGATIVE_STOCK_RISK", "%s: projected balance is not safe" % self.BLOCKED_LABEL, 409)
        if dict_body["reviewNote"] == "DOWNSTREAM_DEPENDENCY":
            raise self.ValidationError("DOWNSTREAM_DEPENDENCY", "%s: downstream dependency requires review" % self.BLOCKED_LABEL, 409)
        if str(dict_body["proposedEffectiveDate"]) < "2026-09-01":
            raise self.ValidationError("CLOSED_PERIOD", "%s: proposed effective date is in a closed period" % self.BLOCKED_LABEL, 409)
        dict_valid = dict_state["valid_proposal"]
        if dict_body["proposedQuantity"] != dict_valid["proposed_quantity"]:
            raise self.ValidationError("UNSUPPORTED_PROPOSED_VALUE", "%s: only the bounded preview value is supported" % self.BLOCKED_LABEL, 409)
        for str_body_field, str_state_field in (("proposalType", "proposal_type"), ("proposerId", "proposer_id"), ("proposerRole", "proposer_role"), ("createdAt", "created_at"), ("proposedEffectiveDate", "proposed_effective_date"), ("idempotencyKey", "idempotency_key"), ("reviewNote", "review_note"), ("policyReference", "policy_reference")):
            if dict_body[str_body_field] != dict_valid[str_state_field]:
                raise self.ValidationError("INVALID_PROPOSAL_INPUT", "%s: %s is not the authorized deterministic value" % (self.BLOCKED_LABEL, str_body_field), 409)

    def __apply_proposal(self, dict_state, dict_body):
        dict_original = dict_state["original_evidence"]
        n_before = dict_original["quantity"]
        n_after = dict_body["proposedQuantity"]
        dict_proposal = {
            "proposal_id": dict_body["proposalId"],
            "original_transaction_id": dict_body["originalTransactionId"],
            "original_evidence_ref": dict_original["evidence_ref"],
            "proposal_type": dict_body["proposalType"],
            "before_quantity": n_before,
            "proposed_quantity": n_after,
            "proposed_delta": n_after - n_before,
            "after_quantity": n_after,
            "reason_code": dict_body["reasonCode"],
            "reason_text": dict_body["reasonText"],
            "proposer_id": dict_body["proposerId"],
            "proposer_role": dict_body["proposerRole"],
            "created_at": dict_body["createdAt"],
            "proposed_effective_date": dict_body["proposedEffectiveDate"],
            "idempotency_key": dict_body["idempotencyKey"],
            "review_note": dict_body["reviewNote"],
            "policy_reference": dict_body["policyReference"],
            "status": "REVIEW_REQUIRED",
            "lineage_ref": "fixture-lineage-p6-proposes-correction-for-001",
            "proposal_evidence_ref": "fixture-evidence-p6-proposal-001",
            "proposal_evidence_sha256": "",
        }
        dict_proposal["proposal_evidence_sha256"] = self.__proposal_evidence_hash(dict_proposal)
        dict_state["proposals"] = [dict_proposal]
        return dict_state

    def __payload(self, dict_state, str_operation, str_state_hash, str_before_hash=None, str_after_hash=None, f_replay=False):
        dict_item = dict_state["item"]
        dict_warehouse = dict_state["warehouse"]
        dict_location = dict_state["location"]
        dict_original = dict_state["original_evidence"]
        dict_proposal = dict_state["proposals"][0] if dict_state["proposals"] else None
        n_current = dict_state["balance"]["current_balance"]
        n_delta = dict_proposal["proposed_delta"] if dict_proposal else None
        n_projected = dict_proposal["after_quantity"] if dict_proposal else None
        return {
            "operation": {
                "name": str_operation,
                "mutationApplied": str_operation == "POST_PROPOSAL" and not f_replay,
                "replay": f_replay,
                "authoritativeStateChanged": False,
                "conflictStatus": "REPLAY" if f_replay else "NONE",
                "stateSha256Before": str_before_hash,
                "stateSha256After": str_after_hash,
            },
            "fixture": {
                "fixtureId": dict_state["fixture_id"],
                "fixtureVersion": dict_state["fixture_version"],
                "classification": dict_state["classification"],
                "sourceClass": dict_state["source_class"],
                "freshness": dict_state["freshness"],
                "confidence": dict_state["confidence"],
                "businessTruth": dict_state["business_truth"],
                "productionTruth": dict_state["production_truth"],
                "liveGovernedBinding": dict_state["live_governed_binding"],
                "stateSha256": str_state_hash,
            },
            "original": {
                "immutable": True,
                "transactionId": dict_original["transaction_id"],
                "source": dict_original["source"],
                "sourceRecordId": dict_original["source_record_id"],
                "transactionType": dict_original["transaction_type"],
                "itemId": dict_original["item_id"],
                "itemCategory": dict_original["item_category"],
                "warehouseCode": dict_original["warehouse_code"],
                "locationCode": dict_original["location_code"],
                "quantity": dict_original["quantity"],
                "uom": dict_original["uom"],
                "timestamp": dict_original["timestamp"],
                "evidenceRef": dict_original["evidence_ref"],
                "evidenceSha256": self.__original_evidence_hash(dict_original),
            },
            "item": self.__item_payload(dict_item),
            "warehouse": self.__warehouse_payload(dict_warehouse),
            "location": self.__location_payload(dict_location),
            "proposal": self.__proposal_payload(dict_proposal),
            "preview": {
                "label": self.PREVIEW_LABEL,
                "status": self.BLOCKED_LABEL if dict_proposal else self.PREVIEW_LABEL,
                "currentBalance": n_current,
                "currentBalanceLabel": self.PREVIEW_LABEL,
                "proposedDelta": n_delta,
                "proposedDeltaLabel": self.PREVIEW_LABEL,
                "projectedBalance": n_projected,
                "projectedBalanceLabel": self.PREVIEW_LABEL,
                "reconciliationReference": dict_state["reconciliation_reference_after_balance"] if dict_proposal else None,
                "reconciliationComputed": n_projected,
                "reconciliationDifference": n_projected - dict_state["reconciliation_reference_after_balance"] if dict_proposal else None,
                "reconciliationStatus": "CONFLICTING" if dict_proposal and n_projected != dict_state["reconciliation_reference_after_balance"] else "NOT_EVALUATED",
                "automaticResolution": False,
                "blockedConditions": ([{"code": "RECONCILIATION_MISMATCH", "label": self.BLOCKED_LABEL, "message": "reference and computed preview balances differ"}] if dict_proposal and n_projected != dict_state["reconciliation_reference_after_balance"] else []),
            },
            "lineage": {
                "relation": "proposes_correction_for" if dict_proposal else None,
                "originalTransactionId": dict_original["transaction_id"],
                "originalEvidenceRef": dict_original["evidence_ref"],
                "originalEvidenceSha256": self.__original_evidence_hash(dict_original),
                "proposalId": dict_proposal["proposal_id"] if dict_proposal else None,
                "proposalEvidenceRef": dict_proposal["proposal_evidence_ref"] if dict_proposal else None,
                "proposalEvidenceSha256": dict_proposal["proposal_evidence_sha256"] if dict_proposal else None,
            },
            "audit": {
                "proposerId": dict_proposal["proposer_id"] if dict_proposal else None,
                "proposerRole": dict_proposal["proposer_role"] if dict_proposal else None,
                "reasonCode": dict_proposal["reason_code"] if dict_proposal else None,
                "reasonText": dict_proposal["reason_text"] if dict_proposal else None,
                "createdAt": dict_proposal["created_at"] if dict_proposal else None,
                "reviewNote": dict_proposal["review_note"] if dict_proposal else None,
                "policyReference": dict_proposal["policy_reference"] if dict_proposal else None,
            },
            "allowedStatuses": dict_state["allowed_statuses"],
            "labels": {
                "preview": self.PREVIEW_LABEL,
                "blockedCondition": self.BLOCKED_LABEL,
                "sourceClass": dict_state["source_class"],
                "freshness": dict_state["freshness"],
                "confidence": dict_state["confidence"],
            },
            "capabilityBoundary": {
                "proposalOnly": True,
                "previewOnly": True,
                "officialBalanceEffect": False,
                "officialCorrection": False,
                "officialReplacement": False,
                "approvalToEffective": False,
                "authoritativeStateMutation": False,
                "delete": False,
                "automaticResolution": False,
                "liveGovernedBinding": False,
                "sql": False,
            },
            "reset": dict_state["reset_rebuild"],
            "cleanup": {"owner": dict_state["reset_rebuild"]["cleanup_owner"], "state": "RESET_REQUIRED_AFTER_VALIDATION" if dict_proposal else "INITIAL_STATE"},
            "caveats": dict_state["caveats"],
        }

    def __proposal_payload(self, dict_proposal):
        if not dict_proposal:
            return None
        return {
            "proposalId": dict_proposal["proposal_id"],
            "originalTransactionId": dict_proposal["original_transaction_id"],
            "originalEvidenceRef": dict_proposal["original_evidence_ref"],
            "proposalType": dict_proposal["proposal_type"],
            "status": dict_proposal["status"],
            "before": {"quantity": dict_proposal["before_quantity"], "label": self.PREVIEW_LABEL},
            "after": {"quantity": dict_proposal["after_quantity"], "label": self.PREVIEW_LABEL},
            "proposedDelta": dict_proposal["proposed_delta"],
            "reasonCode": dict_proposal["reason_code"],
            "reasonText": dict_proposal["reason_text"],
            "proposerId": dict_proposal["proposer_id"],
            "proposerRole": dict_proposal["proposer_role"],
            "createdAt": dict_proposal["created_at"],
            "proposedEffectiveDate": dict_proposal["proposed_effective_date"],
            "idempotencyKey": dict_proposal["idempotency_key"],
            "reviewNote": dict_proposal["review_note"],
            "policyReference": dict_proposal["policy_reference"],
            "lineageRef": dict_proposal["lineage_ref"],
            "proposalEvidenceRef": dict_proposal["proposal_evidence_ref"],
            "proposalEvidenceSha256": dict_proposal["proposal_evidence_sha256"],
            "effective": False,
        }

    def __item_payload(self, dict_item):
        return {"itemId": dict_item["item_id"], "itemNo": dict_item["item_no"], "itemCategory": dict_item["item_category"], "description": dict_item["description"]}

    def __warehouse_payload(self, dict_warehouse):
        return {"warehouseId": dict_warehouse["warehouse_id"], "warehouseCode": dict_warehouse["warehouse_code"], "name": dict_warehouse["name"]}

    def __location_payload(self, dict_location):
        return {"locationId": dict_location["location_id"], "locationCode": dict_location["location_code"], "warehouseId": dict_location["warehouse_id"], "name": dict_location["name"]}

    def __original_evidence_hash(self, dict_original):
        dict_copy = dict(dict_original)
        dict_copy.pop("original_evidence_sha256", None)
        return hashlib.sha256(json.dumps(dict_copy, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest().upper()

    def __proposal_evidence_hash(self, dict_proposal):
        dict_copy = dict(dict_proposal)
        dict_copy["proposal_evidence_sha256"] = ""
        return hashlib.sha256(json.dumps(dict_copy, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest().upper()

    def __error_payload(self, str_code, str_state_hash, lst_conditions):
        return {
            "status": str_code,
            "previewStatus": self.BLOCKED_LABEL,
            "fixtureId": self.FIXTURE_ID,
            "fixtureVersion": self.FIXTURE_VERSION,
            "classification": "NON-PRODUCTION / CONTROLLED VALIDATION DATA",
            "sourceClass": "SYNTHETIC_FIXTURE",
            "freshness": "NOT_MEASURED",
            "confidence": "CONTROLLED_FIXTURE_ONLY",
            "businessTruth": False,
            "productionTruth": False,
            "stateSha256": str_state_hash,
            "mutationApplied": False,
            "authoritativeStateChanged": False,
            "blockedConditions": lst_conditions,
            "labels": {"preview": self.PREVIEW_LABEL, "blockedCondition": self.BLOCKED_LABEL},
            "capabilityBoundary": {
                "proposalOnly": True,
                "previewOnly": True,
                "officialBalanceEffect": False,
                "authoritativeStateMutation": False,
                "automaticResolution": False,
                "liveGovernedBinding": False,
                "sql": False,
            },
        }

    def __sha256(self, obj_path):
        obj_hash = hashlib.sha256()
        with obj_path.open("rb") as obj_file:
            for obj_chunk in iter(lambda: obj_file.read(1024 * 1024), b""):
                obj_hash.update(obj_chunk)
        return obj_hash.hexdigest().upper()


class CWarehouseFixtureP7(object):
    """Bounded pick/outbound decrement adapter for the isolated P7 fixture."""

    STATE_PATH = Path(r"C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\Warehouse_Operations\ERP2-WH-P7-OUTBOUND-PICK-INVENTORY-DECREMENT-FIXTURE-001\state.json")
    FIXTURE_ID = "ERP2-WH-P7-OUTBOUND-PICK-INVENTORY-DECREMENT-FIXTURE-001"
    FIXTURE_VERSION = "1.0.0"
    REQUIRED_BODY_FIELDS = {
        "fixtureId",
        "itemNo",
        "itemCategory",
        "warehouseCode",
        "locationCode",
        "outboundRequestId",
        "idempotencyKey",
        "quantity",
        "uom",
        "operationType",
        "effectivity",
        "requesterId",
        "requesterRole",
    }

    class ValidationError(ValueError):
        def __init__(self, str_code, str_message, n_status_code=400):
            super().__init__(str_message)
            self.str_code = str_code
            self.n_status_code = n_status_code

    def get(self, str_timezone, str_id):
        try:
            dict_state = self.__read_state()
            self.__validate_state(dict_state)
            return 200, EErrorCode.ERROR_SUCCESS, "success", self.__payload(dict_state, "GET", self.__sha256(self.STATE_PATH))
        except FileNotFoundError:
            return 503, EErrorCode.ERROR_OTHER_ERROR, "P7 fixture unavailable", self.__error_payload("FIXTURE_UNAVAILABLE", None)
        except (ValueError, KeyError, TypeError) as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P7 fixture invalid: %s" % str(error), self.__error_payload("FIXTURE_INVALID", None)
        except Exception as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P7 fixture read error: %s" % str(error), self.__error_payload("FIXTURE_READ_ERROR", None)

    def post(self, str_timezone, str_id):
        from flask import request

        try:
            dict_state = self.__read_state()
            self.__validate_state(dict_state)
            str_before_hash = self.__sha256(self.STATE_PATH)
            dict_body = request.get_json(silent=True)
            self.__validate_body_shape(dict_body)
            if dict_state["outbounds"]:
                if dict_body == self.__expected_request(dict_state):
                    return 200, EErrorCode.ERROR_SUCCESS, "outbound replay", self.__payload(dict_state, "POST_OUTBOUND", str_before_hash, str_before_hash, str_before_hash, True)
                if dict_body.get("idempotencyKey") == dict_state["valid_outbound"]["idempotency_key"]:
                    raise self.ValidationError("IDEMPOTENCY_CONFLICT", "same idempotency key has conflicting outbound content", 409)
                raise self.ValidationError("DUPLICATE_OUTBOUND_REQUEST", "only one outbound request is supported", 409)
            self.__validate_request(dict_state, dict_body)
            dict_state = self.__apply_outbound(dict_state, dict_body)
            self.__write_state(dict_state)
            str_after_hash = self.__sha256(self.STATE_PATH)
            return 201, EErrorCode.ERROR_SUCCESS, "outbound accepted", self.__payload(dict_state, "POST_OUTBOUND", str_after_hash, str_before_hash, str_after_hash, False)
        except self.ValidationError as error:
            str_state_hash = self.__sha256(self.STATE_PATH) if self.STATE_PATH.exists() else None
            return error.n_status_code, EErrorCode.ERROR_INVAILD_PARAM, str(error), self.__error_payload(error.str_code, str_state_hash)
        except FileNotFoundError:
            return 503, EErrorCode.ERROR_OTHER_ERROR, "P7 fixture unavailable", self.__error_payload("FIXTURE_UNAVAILABLE", None)
        except (ValueError, KeyError, TypeError) as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P7 fixture invalid: %s" % str(error), self.__error_payload("FIXTURE_INVALID", None)
        except Exception as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P7 fixture write error: %s" % str(error), self.__error_payload("FIXTURE_WRITE_ERROR", None)

    def __read_state(self):
        with self.STATE_PATH.open("r", encoding="utf-8") as obj_file:
            return json.load(obj_file)

    def __write_state(self, dict_state):
        self.STATE_PATH.write_text(json.dumps(dict_state, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    def __validate_state(self, dict_state):
        if dict_state.get("fixture_id") != self.FIXTURE_ID or dict_state.get("fixture_version") != self.FIXTURE_VERSION:
            raise ValueError("fixture identity or version mismatch")
        if dict_state.get("classification") != "NON-PRODUCTION / CONTROLLED VALIDATION DATA" or dict_state.get("source_class") != "SYNTHETIC_FIXTURE":
            raise ValueError("fixture classification mismatch")
        if dict_state.get("freshness") != "NOT_MEASURED" or dict_state.get("confidence") != "CONTROLLED_FIXTURE_ONLY":
            raise ValueError("fixture evidence labels mismatch")
        if dict_state.get("business_truth") is not False or dict_state.get("production_truth") is not False or dict_state.get("live_governed_binding") is not False:
            raise ValueError("fixture truth or binding flags are not disabled")
        if not isinstance(dict_state.get("outbounds"), list) or len(dict_state["outbounds"]) > 1:
            raise ValueError("outbound cardinality mismatch")
        dict_item = dict_state["item"]
        dict_warehouse = dict_state["warehouse"]
        dict_location = dict_state["location"]
        dict_balance = dict_state["balance"]
        dict_baseline = dict_state["baseline_transaction"]
        if dict_location["warehouse_id"] != dict_warehouse["warehouse_id"]:
            raise ValueError("location warehouse link mismatch")
        if dict_balance["item_id"] != dict_item["item_id"] or dict_balance["warehouse_id"] != dict_warehouse["warehouse_id"] or dict_balance["location_id"] != dict_location["location_id"]:
            raise ValueError("balance crosswalk mismatch")
        if dict_baseline["balance"] != dict_balance["opening_balance"] or dict_balance["current_balance"] > dict_balance["opening_balance"]:
            raise ValueError("baseline balance mismatch")
        if dict_state["outbounds"]:
            self.__validate_existing_outbound(dict_state)

    def __validate_existing_outbound(self, dict_state):
        dict_outbound = dict_state["outbounds"][0]
        if dict_outbound["transaction_id"] != "fixture-transaction-p7-outbound-001" or dict_outbound["movement_id"] != "fixture-movement-p7-outbound-001":
            raise ValueError("outbound identity mismatch")
        if dict_outbound["before_balance"] - dict_outbound["quantity"] != dict_outbound["after_balance"]:
            raise ValueError("outbound balance invariant mismatch")
        if dict_state["balance"]["current_balance"] != dict_outbound["after_balance"]:
            raise ValueError("outbound current balance mismatch")
        if dict_outbound["after_balance"] < 0:
            raise ValueError("negative balance mutation")

    def __validate_body_shape(self, dict_body):
        if not isinstance(dict_body, dict):
            raise self.ValidationError("MALFORMED_INPUT", "outbound body must be an object")
        if self.REQUIRED_BODY_FIELDS - set(dict_body):
            raise self.ValidationError("MISSING_FIELD", "outbound body is missing a required field")
        if set(dict_body) != self.REQUIRED_BODY_FIELDS:
            raise self.ValidationError("MALFORMED_INPUT", "outbound body must contain exactly the supported fields")
        for str_field in self.REQUIRED_BODY_FIELDS:
            if dict_body[str_field] is None or (isinstance(dict_body[str_field], str) and not dict_body[str_field].strip()):
                raise self.ValidationError("MISSING_FIELD", "%s is required" % str_field)

    def __expected_request(self, dict_state):
        dict_valid = dict_state["valid_outbound"]
        return {
            "fixtureId": self.FIXTURE_ID,
            "itemNo": dict_valid["item_no"],
            "itemCategory": dict_valid["item_category"],
            "warehouseCode": dict_valid["warehouse_code"],
            "locationCode": dict_valid["location_code"],
            "outboundRequestId": dict_valid["outbound_request_id"],
            "idempotencyKey": dict_valid["idempotency_key"],
            "quantity": dict_valid["quantity"],
            "uom": dict_valid["uom"],
            "operationType": dict_valid["operation_type"],
            "effectivity": dict_valid["effectivity"],
            "requesterId": dict_valid["requester_id"],
            "requesterRole": dict_valid["requester_role"],
        }

    def __validate_request(self, dict_state, dict_body):
        dict_item = dict_state["item"]
        dict_warehouse = dict_state["warehouse"]
        dict_location = dict_state["location"]
        if dict_body["fixtureId"] != self.FIXTURE_ID:
            raise self.ValidationError("WRONG_FIXTURE_IDENTITY", "fixtureId does not match the controlled fixture")
        if dict_body["itemNo"] != dict_item["item_no"]:
            raise self.ValidationError("WRONG_ITEM_IDENTITY", "itemNo does not match the controlled material")
        if dict_body["itemCategory"] != dict_item["item_category"]:
            raise self.ValidationError("WRONG_ITEM_CATEGORY", "itemCategory does not match the controlled material")
        if dict_body["warehouseCode"] != dict_warehouse["warehouse_code"] or dict_body["locationCode"] != dict_location["location_code"]:
            raise self.ValidationError("WRONG_LOCATION_IDENTITY", "Warehouse or location does not match the controlled balance")
        if isinstance(dict_body["quantity"], bool) or not isinstance(dict_body["quantity"], (int, float)):
            raise self.ValidationError("INVALID_QUANTITY", "quantity must be numeric")
        if dict_body["quantity"] <= 0:
            raise self.ValidationError("INVALID_QUANTITY", "quantity must be positive")
        if dict_body["quantity"] > dict_state["balance"]["current_balance"]:
            raise self.ValidationError("INSUFFICIENT_QUANTITY", "outbound quantity exceeds available controlled balance", 409)
        if dict_body["quantity"] > dict_state["max_quantity"]:
            raise self.ValidationError("QUANTITY_OVERFLOW", "quantity exceeds the controlled outbound bound")
        dict_valid = dict_state["valid_outbound"]
        for str_body_field, str_state_field in (("outboundRequestId", "outbound_request_id"), ("idempotencyKey", "idempotency_key"), ("uom", "uom"), ("operationType", "operation_type"), ("effectivity", "effectivity"), ("requesterId", "requester_id"), ("requesterRole", "requester_role")):
            if dict_body[str_body_field] != dict_valid[str_state_field]:
                raise self.ValidationError("UNSUPPORTED_%s" % str_body_field.upper(), "%s is not the authorized deterministic value" % str_body_field)
        if dict_body["quantity"] != dict_valid["quantity"]:
            raise self.ValidationError("UNSUPPORTED_QUANTITY", "only the authorized deterministic outbound quantity is supported")

    def __apply_outbound(self, dict_state, dict_body):
        dict_item = dict_state["item"]
        dict_warehouse = dict_state["warehouse"]
        dict_location = dict_state["location"]
        dict_balance = dict_state["balance"]
        n_before = dict_balance["current_balance"]
        n_quantity = dict_body["quantity"]
        n_after = n_before - n_quantity
        dict_state["outbounds"] = [{
            "transaction_id": "fixture-transaction-p7-outbound-001",
            "movement_id": "fixture-movement-p7-outbound-001",
            "evidence_link_id": "fixture-evidence-p7-outbound-001",
            "outbound_request_id": dict_body["outboundRequestId"],
            "idempotency_key": dict_body["idempotencyKey"],
            "item_id": dict_item["item_id"],
            "item_no": dict_item["item_no"],
            "item_category": dict_item["item_category"],
            "warehouse_id": dict_warehouse["warehouse_id"],
            "warehouse_code": dict_warehouse["warehouse_code"],
            "location_id": dict_location["location_id"],
            "location_code": dict_location["location_code"],
            "quantity": n_quantity,
            "uom": dict_body["uom"],
            "operation_type": dict_body["operationType"],
            "effectivity": dict_body["effectivity"],
            "requester_id": dict_body["requesterId"],
            "requester_role": dict_body["requesterRole"],
            "before_balance": n_before,
            "movement_quantity": -n_quantity,
            "after_balance": n_after,
            "source_class": "SYNTHETIC_FIXTURE",
            "lineage_ref": "fixture-evidence-p7-outbound-001",
            "freshness": "NOT_MEASURED",
            "confidence": "CONTROLLED_FIXTURE_ONLY",
        }]
        dict_balance["current_balance"] = n_after
        return dict_state

    def __payload(self, dict_state, str_operation, str_state_hash, str_before_hash=None, str_after_hash=None, f_replay=False):
        dict_item = dict_state["item"]
        dict_warehouse = dict_state["warehouse"]
        dict_location = dict_state["location"]
        dict_baseline = dict_state["baseline_transaction"]
        dict_outbound = dict_state["outbounds"][0] if dict_state["outbounds"] else None
        dict_balance = dict_state["balance"]
        n_before = dict_outbound["before_balance"] if dict_outbound else dict_balance["current_balance"]
        n_quantity = dict_outbound["quantity"] if dict_outbound else 0
        n_after = dict_balance["current_balance"]
        return {
            "operation": {"name": str_operation, "mutationApplied": str_operation == "POST_OUTBOUND" and not f_replay, "replay": f_replay, "authoritativeStateChanged": False, "stateSha256Before": str_before_hash, "stateSha256After": str_after_hash},
            "fixture": {"fixtureId": dict_state["fixture_id"], "fixtureVersion": dict_state["fixture_version"], "classification": dict_state["classification"], "sourceClass": dict_state["source_class"], "freshness": dict_state["freshness"], "confidence": dict_state["confidence"], "businessTruth": dict_state["business_truth"], "productionTruth": dict_state["production_truth"], "liveGovernedBinding": dict_state["live_governed_binding"], "stateSha256": str_state_hash},
            "item": self.__item_payload(dict_item),
            "warehouse": self.__warehouse_payload(dict_warehouse),
            "location": self.__location_payload(dict_location),
            "baselineTransaction": {"transactionId": dict_baseline["transaction_id"], "movementId": dict_baseline["movement_id"], "evidenceLinkId": dict_baseline["evidence_link_id"], "transactionType": dict_baseline["transaction_type"], "effectivity": dict_baseline["effectivity"], "balance": dict_baseline["balance"]},
            "outboundTransaction": self.__outbound_transaction_payload(dict_outbound),
            "movement": self.__movement_payload(dict_outbound),
            "balance": {"balanceId": dict_balance["balance_id"], "itemId": dict_balance["item_id"], "warehouseId": dict_balance["warehouse_id"], "locationId": dict_balance["location_id"], "uom": dict_balance["uom"], "beforeBalance": n_before, "outboundQuantity": n_quantity, "afterBalance": n_after, "invariant": "BEFORE BALANCE - VALID OUTBOUND QUANTITY = AFTER BALANCE", "invariantValid": n_before - n_quantity == n_after},
            "crosswalk": self.__crosswalk_payload(dict_state, dict_outbound),
            "reconciliation": {"readbackBalanceReference": dict_state["readback_balance_reference"], "computedAfterBalance": n_after, "difference": n_after - dict_state["readback_balance_reference"], "status": "CONFLICTING" if dict_outbound and n_after != dict_state["readback_balance_reference"] else "NOT_EVALUATED", "automaticResolution": False},
            "sourceLineage": {"sourceClass": dict_state["source_class"], "lineageRef": dict_outbound["lineage_ref"] if dict_outbound else "fixture-evidence-p7-baseline-001", "freshness": dict_state["freshness"], "confidence": dict_state["confidence"], "noLiveSource": True},
            "capabilityBoundary": {"boundedOutboundOnly": True, "pickOutboundOnly": True, "positiveQuantityRequired": True, "insufficientQuantityBlocked": True, "negativeBalanceMutation": False, "officialInventoryEffect": False, "officialAccountingEffect": False, "arbitraryUpdateDelete": False, "sql": False, "liveGovernedBinding": False},
            "reset": dict_state["reset_rebuild"],
            "cleanup": {"owner": dict_state["reset_rebuild"]["cleanup_owner"], "state": "RESET_REQUIRED_AFTER_VALIDATION" if dict_outbound else "INITIAL_STATE"},
            "caveats": dict_state["caveats"],
        }

    def __item_payload(self, dict_item):
        return {"itemId": dict_item["item_id"], "itemNo": dict_item["item_no"], "itemCategory": dict_item["item_category"], "description": dict_item["description"]}

    def __warehouse_payload(self, dict_warehouse):
        return {"warehouseId": dict_warehouse["warehouse_id"], "warehouseCode": dict_warehouse["warehouse_code"], "name": dict_warehouse["name"]}

    def __location_payload(self, dict_location):
        return {"locationId": dict_location["location_id"], "locationCode": dict_location["location_code"], "warehouseId": dict_location["warehouse_id"], "name": dict_location["name"]}

    def __outbound_transaction_payload(self, dict_outbound):
        if not dict_outbound:
            return None
        return {"transactionId": dict_outbound["transaction_id"], "outboundRequestId": dict_outbound["outbound_request_id"], "movementId": dict_outbound["movement_id"], "evidenceLinkId": dict_outbound["evidence_link_id"], "idempotencyKey": dict_outbound["idempotency_key"], "operationType": dict_outbound["operation_type"], "effectivity": dict_outbound["effectivity"], "requesterId": dict_outbound["requester_id"], "requesterRole": dict_outbound["requester_role"]}

    def __movement_payload(self, dict_outbound):
        if not dict_outbound:
            return None
        return {"movementId": dict_outbound["movement_id"], "transactionId": dict_outbound["transaction_id"], "outboundRequestId": dict_outbound["outbound_request_id"], "itemId": dict_outbound["item_id"], "itemNo": dict_outbound["item_no"], "itemCategory": dict_outbound["item_category"], "warehouseId": dict_outbound["warehouse_id"], "warehouseCode": dict_outbound["warehouse_code"], "locationId": dict_outbound["location_id"], "locationCode": dict_outbound["location_code"], "quantity": dict_outbound["quantity"], "movementQuantity": dict_outbound["movement_quantity"], "uom": dict_outbound["uom"], "operationType": dict_outbound["operation_type"], "effectivity": dict_outbound["effectivity"], "beforeBalance": dict_outbound["before_balance"], "afterBalance": dict_outbound["after_balance"], "sourceClass": dict_outbound["source_class"], "lineageRef": dict_outbound["lineage_ref"], "freshness": dict_outbound["freshness"], "confidence": dict_outbound["confidence"], "invariantValid": dict_outbound["before_balance"] - dict_outbound["quantity"] == dict_outbound["after_balance"]}

    def __crosswalk_payload(self, dict_state, dict_outbound):
        return {"itemId": dict_state["item"]["item_id"], "itemNo": dict_state["item"]["item_no"], "warehouseId": dict_state["warehouse"]["warehouse_id"], "warehouseCode": dict_state["warehouse"]["warehouse_code"], "locationId": dict_state["location"]["location_id"], "locationCode": dict_state["location"]["location_code"], "balanceId": dict_state["balance"]["balance_id"], "baselineTransactionId": dict_state["baseline_transaction"]["transaction_id"], "baselineMovementId": dict_state["baseline_transaction"]["movement_id"], "baselineEvidenceLinkId": dict_state["baseline_transaction"]["evidence_link_id"], "outboundTransactionId": dict_outbound["transaction_id"] if dict_outbound else None, "outboundMovementId": dict_outbound["movement_id"] if dict_outbound else None, "outboundEvidenceLinkId": dict_outbound["evidence_link_id"] if dict_outbound else None}

    def __error_payload(self, str_code, str_state_hash):
        return {"status": str_code, "fixtureId": self.FIXTURE_ID, "fixtureVersion": self.FIXTURE_VERSION, "classification": "NON-PRODUCTION / CONTROLLED VALIDATION DATA", "sourceClass": "SYNTHETIC_FIXTURE", "freshness": "NOT_MEASURED", "confidence": "CONTROLLED_FIXTURE_ONLY", "businessTruth": False, "productionTruth": False, "stateSha256": str_state_hash, "mutationApplied": False, "authoritativeStateChanged": False, "capabilityBoundary": {"boundedOutboundOnly": True, "pickOutboundOnly": True, "insufficientQuantityBlocked": True, "negativeBalanceMutation": False, "officialInventoryEffect": False, "arbitraryUpdateDelete": False, "sql": False, "liveGovernedBinding": False}}

    def __sha256(self, obj_path):
        obj_hash = hashlib.sha256()
        with obj_path.open("rb") as obj_file:
            for obj_chunk in iter(lambda: obj_file.read(1024 * 1024), b""):
                obj_hash.update(obj_chunk)
        return obj_hash.hexdigest().upper()


class CWarehouseFixtureP8(object):
    """Bounded source-to-destination Warehouse transfer adapter for P8."""

    STATE_PATH = Path(r"C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\Warehouse_Operations\ERP2-WH-P8-CONTROLLED-WAREHOUSE-TRANSFER-FIXTURE-001\state.json")
    FIXTURE_ID = "ERP2-WH-P8-CONTROLLED-WAREHOUSE-TRANSFER-FIXTURE-001"
    FIXTURE_VERSION = "1.0.0"
    REQUIRED_BODY_FIELDS = {
        "fixtureId",
        "itemNo",
        "itemCategory",
        "sourceWarehouseCode",
        "sourceLocationCode",
        "destinationWarehouseCode",
        "destinationLocationCode",
        "transferRequestId",
        "idempotencyKey",
        "quantity",
        "uom",
        "operationType",
        "effectivity",
        "requesterId",
        "requesterRole",
    }

    class ValidationError(ValueError):
        def __init__(self, str_code, str_message, n_status_code=400):
            super().__init__(str_message)
            self.str_code = str_code
            self.n_status_code = n_status_code

    def get(self, str_timezone, str_id):
        try:
            dict_state = self.__read_state()
            self.__validate_state(dict_state)
            return 200, EErrorCode.ERROR_SUCCESS, "success", self.__payload(dict_state, "GET", self.__sha256(self.STATE_PATH))
        except FileNotFoundError:
            return 503, EErrorCode.ERROR_OTHER_ERROR, "P8 fixture unavailable", self.__error_payload("FIXTURE_UNAVAILABLE", None)
        except (ValueError, KeyError, TypeError) as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P8 fixture invalid: %s" % str(error), self.__error_payload("FIXTURE_INVALID", None)
        except Exception as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P8 fixture read error: %s" % str(error), self.__error_payload("FIXTURE_READ_ERROR", None)

    def post(self, str_timezone, str_id):
        from flask import request

        try:
            dict_state = self.__read_state()
            self.__validate_state(dict_state)
            str_before_hash = self.__sha256(self.STATE_PATH)
            dict_body = request.get_json(silent=True)
            self.__validate_body_shape(dict_body)
            if dict_state["transfers"]:
                if dict_body == self.__expected_request(dict_state):
                    return 200, EErrorCode.ERROR_SUCCESS, "transfer replay", self.__payload(dict_state, "POST_TRANSFER", str_before_hash, str_before_hash, str_before_hash, True)
                if dict_body.get("idempotencyKey") == dict_state["valid_transfer"]["idempotency_key"]:
                    raise self.ValidationError("IDEMPOTENCY_CONFLICT", "same idempotency key has conflicting transfer content", 409)
                raise self.ValidationError("DUPLICATE_TRANSFER_REQUEST", "only one controlled transfer is supported", 409)
            self.__validate_request(dict_state, dict_body)
            dict_state = self.__apply_transfer(dict_state, dict_body)
            self.__write_state(dict_state)
            str_after_hash = self.__sha256(self.STATE_PATH)
            return 201, EErrorCode.ERROR_SUCCESS, "transfer accepted", self.__payload(dict_state, "POST_TRANSFER", str_after_hash, str_before_hash, str_after_hash, False)
        except self.ValidationError as error:
            str_state_hash = self.__sha256(self.STATE_PATH) if self.STATE_PATH.exists() else None
            return error.n_status_code, EErrorCode.ERROR_INVAILD_PARAM, str(error), self.__error_payload(error.str_code, str_state_hash)
        except FileNotFoundError:
            return 503, EErrorCode.ERROR_OTHER_ERROR, "P8 fixture unavailable", self.__error_payload("FIXTURE_UNAVAILABLE", None)
        except (ValueError, KeyError, TypeError) as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P8 fixture invalid: %s" % str(error), self.__error_payload("FIXTURE_INVALID", None)
        except Exception as error:
            return 500, EErrorCode.ERROR_OTHER_ERROR, "P8 fixture write error: %s" % str(error), self.__error_payload("FIXTURE_WRITE_ERROR", None)

    def __read_state(self):
        with self.STATE_PATH.open("r", encoding="utf-8") as obj_file:
            return json.load(obj_file)

    def __write_state(self, dict_state):
        self.STATE_PATH.write_text(json.dumps(dict_state, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    def __validate_state(self, dict_state):
        if dict_state.get("fixture_id") != self.FIXTURE_ID or dict_state.get("fixture_version") != self.FIXTURE_VERSION:
            raise ValueError("fixture identity or version mismatch")
        if dict_state.get("classification") != "NON-PRODUCTION / CONTROLLED VALIDATION DATA" or dict_state.get("source_class") != "SYNTHETIC_FIXTURE":
            raise ValueError("fixture classification mismatch")
        if dict_state.get("freshness") != "NOT_MEASURED" or dict_state.get("confidence") != "CONTROLLED_FIXTURE_ONLY":
            raise ValueError("fixture evidence labels mismatch")
        if dict_state.get("business_truth") is not False or dict_state.get("production_truth") is not False or dict_state.get("live_governed_binding") is not False:
            raise ValueError("fixture truth or binding flags are not disabled")
        if not isinstance(dict_state.get("transfers"), list) or len(dict_state["transfers"]) > 1:
            raise ValueError("transfer cardinality mismatch")
        dict_item = dict_state["item"]
        dict_source = dict_state["source"]
        dict_destination = dict_state["destination"]
        dict_source_balance = dict_state["source_balance"]
        dict_destination_balance = dict_state["destination_balance"]
        dict_baseline = dict_state["baseline_transaction"]
        if dict_source["warehouse_id"] == dict_destination["warehouse_id"] and dict_source["location_id"] == dict_destination["location_id"]:
            raise ValueError("fixture source and destination are identical")
        if dict_source_balance["item_id"] != dict_item["item_id"] or dict_destination_balance["item_id"] != dict_item["item_id"]:
            raise ValueError("balance item crosswalk mismatch")
        if dict_source_balance["warehouse_id"] != dict_source["warehouse_id"] or dict_source_balance["location_id"] != dict_source["location_id"] or dict_destination_balance["warehouse_id"] != dict_destination["warehouse_id"] or dict_destination_balance["location_id"] != dict_destination["location_id"]:
            raise ValueError("balance location crosswalk mismatch")
        if dict_baseline["total_balance"] != dict_source_balance["opening_balance"] + dict_destination_balance["opening_balance"]:
            raise ValueError("baseline total mismatch")
        if not dict_state["transfers"] and (dict_source_balance["current_balance"] != dict_source_balance["opening_balance"] or dict_destination_balance["current_balance"] != dict_destination_balance["opening_balance"]):
            raise ValueError("baseline balances changed")
        if dict_state["transfers"]:
            self.__validate_existing_transfer(dict_state)

    def __validate_existing_transfer(self, dict_state):
        dict_transfer = dict_state["transfers"][0]
        if dict_transfer["transaction_id"] != "fixture-transaction-p8-transfer-001" or dict_transfer["source_movement_id"] != "fixture-movement-p8-source-001" or dict_transfer["destination_movement_id"] != "fixture-movement-p8-destination-001":
            raise ValueError("transfer identity mismatch")
        if dict_transfer["source_before"] - dict_transfer["quantity"] != dict_transfer["source_after"]:
            raise ValueError("source transfer invariant mismatch")
        if dict_transfer["destination_before"] + dict_transfer["quantity"] != dict_transfer["destination_after"]:
            raise ValueError("destination transfer invariant mismatch")
        if dict_transfer["source_before"] + dict_transfer["destination_before"] != dict_transfer["source_after"] + dict_transfer["destination_after"]:
            raise ValueError("total transfer conservation mismatch")
        if dict_transfer["source_after"] < 0:
            raise ValueError("negative source balance mutation")
        if dict_state["source_balance"]["current_balance"] != dict_transfer["source_after"] or dict_state["destination_balance"]["current_balance"] != dict_transfer["destination_after"]:
            raise ValueError("transfer current balance mismatch")

    def __validate_body_shape(self, dict_body):
        if not isinstance(dict_body, dict):
            raise self.ValidationError("MALFORMED_INPUT", "transfer body must be an object")
        if self.REQUIRED_BODY_FIELDS - set(dict_body):
            raise self.ValidationError("MISSING_FIELD", "transfer body is missing a required field")
        if set(dict_body) != self.REQUIRED_BODY_FIELDS:
            raise self.ValidationError("MALFORMED_INPUT", "transfer body must contain exactly the supported fields")
        for str_field in self.REQUIRED_BODY_FIELDS:
            if dict_body[str_field] is None or (isinstance(dict_body[str_field], str) and not dict_body[str_field].strip()):
                raise self.ValidationError("MISSING_FIELD", "%s is required" % str_field)

    def __expected_request(self, dict_state):
        dict_valid = dict_state["valid_transfer"]
        return {
            "fixtureId": self.FIXTURE_ID,
            "itemNo": dict_valid["item_no"],
            "itemCategory": dict_valid["item_category"],
            "sourceWarehouseCode": dict_valid["source_warehouse_code"],
            "sourceLocationCode": dict_valid["source_location_code"],
            "destinationWarehouseCode": dict_valid["destination_warehouse_code"],
            "destinationLocationCode": dict_valid["destination_location_code"],
            "transferRequestId": dict_valid["transfer_request_id"],
            "idempotencyKey": dict_valid["idempotency_key"],
            "quantity": dict_valid["quantity"],
            "uom": dict_valid["uom"],
            "operationType": dict_valid["operation_type"],
            "effectivity": dict_valid["effectivity"],
            "requesterId": dict_valid["requester_id"],
            "requesterRole": dict_valid["requester_role"],
        }

    def __validate_request(self, dict_state, dict_body):
        dict_item = dict_state["item"]
        dict_source = dict_state["source"]
        dict_destination = dict_state["destination"]
        if dict_body["fixtureId"] != self.FIXTURE_ID:
            raise self.ValidationError("WRONG_FIXTURE_IDENTITY", "fixtureId does not match the controlled fixture")
        if dict_body["itemNo"] != dict_item["item_no"]:
            raise self.ValidationError("WRONG_ITEM_IDENTITY", "itemNo does not match the controlled material")
        if dict_body["itemCategory"] != dict_item["item_category"]:
            raise self.ValidationError("WRONG_ITEM_CATEGORY", "itemCategory does not match the controlled material")
        if dict_body["sourceWarehouseCode"] == dict_body["destinationWarehouseCode"] and dict_body["sourceLocationCode"] == dict_body["destinationLocationCode"]:
            raise self.ValidationError("SAME_SOURCE_DESTINATION", "source and destination must be different", 409)
        if dict_body["sourceWarehouseCode"] != dict_source["warehouse_code"] or dict_body["sourceLocationCode"] != dict_source["location_code"]:
            raise self.ValidationError("WRONG_SOURCE_IDENTITY", "source Warehouse or location does not match the controlled fixture")
        if dict_body["destinationWarehouseCode"] != dict_destination["warehouse_code"] or dict_body["destinationLocationCode"] != dict_destination["location_code"]:
            raise self.ValidationError("WRONG_DESTINATION_IDENTITY", "destination Warehouse or location does not match the controlled fixture")
        if isinstance(dict_body["quantity"], bool) or not isinstance(dict_body["quantity"], (int, float)):
            raise self.ValidationError("INVALID_QUANTITY", "quantity must be numeric")
        if dict_body["quantity"] <= 0:
            raise self.ValidationError("INVALID_QUANTITY", "quantity must be positive")
        if dict_body["quantity"] > dict_state["source_balance"]["current_balance"]:
            raise self.ValidationError("INSUFFICIENT_SOURCE_QUANTITY", "transfer quantity exceeds source balance", 409)
        if dict_body["quantity"] > dict_state["max_quantity"]:
            raise self.ValidationError("QUANTITY_OVERFLOW", "quantity exceeds the controlled transfer bound")
        dict_valid = dict_state["valid_transfer"]
        for str_body_field, str_state_field in (("transferRequestId", "transfer_request_id"), ("idempotencyKey", "idempotency_key"), ("uom", "uom"), ("operationType", "operation_type"), ("effectivity", "effectivity"), ("requesterId", "requester_id"), ("requesterRole", "requester_role")):
            if dict_body[str_body_field] != dict_valid[str_state_field]:
                raise self.ValidationError("UNSUPPORTED_%s" % str_body_field.upper(), "%s is not the authorized deterministic value" % str_body_field)
        if dict_body["quantity"] != dict_valid["quantity"]:
            raise self.ValidationError("UNSUPPORTED_QUANTITY", "only the authorized deterministic transfer quantity is supported")

    def __apply_transfer(self, dict_state, dict_body):
        dict_source_balance = dict_state["source_balance"]
        dict_destination_balance = dict_state["destination_balance"]
        n_source_before = dict_source_balance["current_balance"]
        n_destination_before = dict_destination_balance["current_balance"]
        n_quantity = dict_body["quantity"]
        n_source_after = n_source_before - n_quantity
        n_destination_after = n_destination_before + n_quantity
        dict_state["transfers"] = [{
            "transaction_id": "fixture-transaction-p8-transfer-001",
            "source_movement_id": "fixture-movement-p8-source-001",
            "destination_movement_id": "fixture-movement-p8-destination-001",
            "evidence_link_id": "fixture-evidence-p8-transfer-001",
            "transfer_request_id": dict_body["transferRequestId"],
            "idempotency_key": dict_body["idempotencyKey"],
            "quantity": n_quantity,
            "uom": dict_body["uom"],
            "operation_type": dict_body["operationType"],
            "effectivity": dict_body["effectivity"],
            "requester_id": dict_body["requesterId"],
            "requester_role": dict_body["requesterRole"],
            "source_before": n_source_before,
            "source_after": n_source_after,
            "destination_before": n_destination_before,
            "destination_after": n_destination_after,
            "source_class": "SYNTHETIC_FIXTURE",
            "lineage_ref": "fixture-evidence-p8-transfer-001",
            "freshness": "NOT_MEASURED",
            "confidence": "CONTROLLED_FIXTURE_ONLY",
        }]
        dict_source_balance["current_balance"] = n_source_after
        dict_destination_balance["current_balance"] = n_destination_after
        return dict_state

    def __payload(self, dict_state, str_operation, str_state_hash, str_before_hash=None, str_after_hash=None, f_replay=False):
        dict_transfer = dict_state["transfers"][0] if dict_state["transfers"] else None
        dict_source_balance = dict_state["source_balance"]
        dict_destination_balance = dict_state["destination_balance"]
        n_source_before = dict_transfer["source_before"] if dict_transfer else dict_source_balance["current_balance"]
        n_destination_before = dict_transfer["destination_before"] if dict_transfer else dict_destination_balance["current_balance"]
        n_quantity = dict_transfer["quantity"] if dict_transfer else 0
        n_source_after = dict_source_balance["current_balance"]
        n_destination_after = dict_destination_balance["current_balance"]
        n_total_before = n_source_before + n_destination_before
        n_total_after = n_source_after + n_destination_after
        return {
            "operation": {"name": str_operation, "mutationApplied": str_operation == "POST_TRANSFER" and not f_replay, "replay": f_replay, "authoritativeStateChanged": False, "stateSha256Before": str_before_hash, "stateSha256After": str_after_hash},
            "fixture": {"fixtureId": dict_state["fixture_id"], "fixtureVersion": dict_state["fixture_version"], "classification": dict_state["classification"], "sourceClass": dict_state["source_class"], "freshness": dict_state["freshness"], "confidence": dict_state["confidence"], "businessTruth": dict_state["business_truth"], "productionTruth": dict_state["production_truth"], "liveGovernedBinding": dict_state["live_governed_binding"], "stateSha256": str_state_hash},
            "item": self.__item_payload(dict_state["item"]),
            "source": self.__node_payload(dict_state["source"]),
            "destination": self.__node_payload(dict_state["destination"]),
            "baselineTransaction": {"transactionId": dict_state["baseline_transaction"]["transaction_id"], "evidenceLinkId": dict_state["baseline_transaction"]["evidence_link_id"], "transactionType": dict_state["baseline_transaction"]["transaction_type"], "effectivity": dict_state["baseline_transaction"]["effectivity"], "totalBalance": dict_state["baseline_transaction"]["total_balance"]},
            "transferTransaction": self.__transfer_transaction_payload(dict_transfer),
            "sourceMovement": self.__movement_payload(dict_transfer, "SOURCE"),
            "destinationMovement": self.__movement_payload(dict_transfer, "DESTINATION"),
            "balances": {"source": {"balanceId": dict_source_balance["balance_id"], "before": n_source_before, "transferQuantity": n_quantity, "after": n_source_after, "invariant": "SOURCE BEFORE - TRANSFER QTY = SOURCE AFTER", "invariantValid": n_source_before - n_quantity == n_source_after}, "destination": {"balanceId": dict_destination_balance["balance_id"], "before": n_destination_before, "transferQuantity": n_quantity, "after": n_destination_after, "invariant": "DESTINATION BEFORE + TRANSFER QTY = DESTINATION AFTER", "invariantValid": n_destination_before + n_quantity == n_destination_after}, "total": {"before": n_total_before, "after": n_total_after, "invariant": "TOTAL ITEM QUANTITY BEFORE = TOTAL ITEM QUANTITY AFTER", "invariantValid": n_total_before == n_total_after}},
            "crosswalk": self.__crosswalk_payload(dict_state, dict_transfer),
            "reconciliation": {"readbackTotalReference": dict_state["readback_total_reference"], "computedTotalAfter": n_total_after, "difference": n_total_after - dict_state["readback_total_reference"], "status": "CONFLICTING" if dict_transfer and n_total_after != dict_state["readback_total_reference"] else "NOT_EVALUATED", "automaticResolution": False},
            "sourceLineage": {"sourceClass": dict_state["source_class"], "lineageRef": dict_transfer["lineage_ref"] if dict_transfer else "fixture-evidence-p8-baseline-001", "freshness": dict_state["freshness"], "confidence": dict_state["confidence"], "noLiveSource": True},
            "capabilityBoundary": {"boundedTransferOnly": True, "sourceDecrementOnlyThroughTransfer": True, "destinationIncrementOnlyThroughTransfer": True, "totalConservationRequired": True, "insufficientSourceBlocked": True, "sameLocationBlocked": True, "negativeBalanceMutation": False, "officialInventoryEffect": False, "officialAccountingEffect": False, "arbitraryUpdateDelete": False, "sql": False, "liveGovernedBinding": False},
            "reset": dict_state["reset_rebuild"],
            "cleanup": {"owner": dict_state["reset_rebuild"]["cleanup_owner"], "state": "RESET_REQUIRED_AFTER_VALIDATION" if dict_transfer else "INITIAL_STATE"},
            "caveats": dict_state["caveats"],
        }

    def __item_payload(self, dict_item):
        return {"itemId": dict_item["item_id"], "itemNo": dict_item["item_no"], "itemCategory": dict_item["item_category"], "description": dict_item["description"]}

    def __node_payload(self, dict_node):
        return {"warehouseId": dict_node["warehouse_id"], "warehouseCode": dict_node["warehouse_code"], "locationId": dict_node["location_id"], "locationCode": dict_node["location_code"], "name": dict_node["name"]}

    def __transfer_transaction_payload(self, dict_transfer):
        if not dict_transfer:
            return None
        return {"transactionId": dict_transfer["transaction_id"], "transferRequestId": dict_transfer["transfer_request_id"], "sourceMovementId": dict_transfer["source_movement_id"], "destinationMovementId": dict_transfer["destination_movement_id"], "evidenceLinkId": dict_transfer["evidence_link_id"], "idempotencyKey": dict_transfer["idempotency_key"], "operationType": dict_transfer["operation_type"], "effectivity": dict_transfer["effectivity"], "requesterId": dict_transfer["requester_id"], "requesterRole": dict_transfer["requester_role"]}

    def __movement_payload(self, dict_transfer, str_side):
        if not dict_transfer:
            return None
        f_source = str_side == "SOURCE"
        return {"movementId": dict_transfer["source_movement_id"] if f_source else dict_transfer["destination_movement_id"], "transactionId": dict_transfer["transaction_id"], "transferRequestId": dict_transfer["transfer_request_id"], "side": str_side, "quantity": dict_transfer["quantity"], "movementQuantity": -dict_transfer["quantity"] if f_source else dict_transfer["quantity"], "uom": dict_transfer["uom"], "operationType": dict_transfer["operation_type"], "effectivity": dict_transfer["effectivity"], "beforeBalance": dict_transfer["source_before"] if f_source else dict_transfer["destination_before"], "afterBalance": dict_transfer["source_after"] if f_source else dict_transfer["destination_after"], "sourceClass": dict_transfer["source_class"], "lineageRef": dict_transfer["lineage_ref"], "freshness": dict_transfer["freshness"], "confidence": dict_transfer["confidence"], "invariantValid": (dict_transfer["source_before"] - dict_transfer["quantity"] == dict_transfer["source_after"]) if f_source else (dict_transfer["destination_before"] + dict_transfer["quantity"] == dict_transfer["destination_after"])}

    def __crosswalk_payload(self, dict_state, dict_transfer):
        return {"itemId": dict_state["item"]["item_id"], "itemNo": dict_state["item"]["item_no"], "sourceWarehouseId": dict_state["source"]["warehouse_id"], "sourceWarehouseCode": dict_state["source"]["warehouse_code"], "sourceLocationId": dict_state["source"]["location_id"], "sourceLocationCode": dict_state["source"]["location_code"], "destinationWarehouseId": dict_state["destination"]["warehouse_id"], "destinationWarehouseCode": dict_state["destination"]["warehouse_code"], "destinationLocationId": dict_state["destination"]["location_id"], "destinationLocationCode": dict_state["destination"]["location_code"], "sourceBalanceId": dict_state["source_balance"]["balance_id"], "destinationBalanceId": dict_state["destination_balance"]["balance_id"], "baselineTransactionId": dict_state["baseline_transaction"]["transaction_id"], "transferTransactionId": dict_transfer["transaction_id"] if dict_transfer else None, "sourceMovementId": dict_transfer["source_movement_id"] if dict_transfer else None, "destinationMovementId": dict_transfer["destination_movement_id"] if dict_transfer else None, "evidenceLinkId": dict_transfer["evidence_link_id"] if dict_transfer else None}

    def __error_payload(self, str_code, str_state_hash):
        return {"status": str_code, "fixtureId": self.FIXTURE_ID, "fixtureVersion": self.FIXTURE_VERSION, "classification": "NON-PRODUCTION / CONTROLLED VALIDATION DATA", "sourceClass": "SYNTHETIC_FIXTURE", "freshness": "NOT_MEASURED", "confidence": "CONTROLLED_FIXTURE_ONLY", "businessTruth": False, "productionTruth": False, "stateSha256": str_state_hash, "mutationApplied": False, "authoritativeStateChanged": False, "capabilityBoundary": {"boundedTransferOnly": True, "sourceDecrementOnlyThroughTransfer": True, "destinationIncrementOnlyThroughTransfer": True, "totalConservationRequired": True, "insufficientSourceBlocked": True, "sameLocationBlocked": True, "negativeBalanceMutation": False, "officialInventoryEffect": False, "arbitraryUpdateDelete": False, "sql": False, "liveGovernedBinding": False}}

    def __sha256(self, obj_path):
        obj_hash = hashlib.sha256()
        with obj_path.open("rb") as obj_file:
            for obj_chunk in iter(lambda: obj_file.read(1024 * 1024), b""):
                obj_hash.update(obj_chunk)
        return obj_hash.hexdigest().upper()
