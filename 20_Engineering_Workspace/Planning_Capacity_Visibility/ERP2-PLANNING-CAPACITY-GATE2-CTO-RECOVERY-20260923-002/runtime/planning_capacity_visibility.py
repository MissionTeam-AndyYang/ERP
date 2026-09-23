"""Independent bounded synthetic Planning / Capacity Gate 2 recovery composition."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping


EVIDENCE_STATES = (
    "PRESENT",
    "ABSENT",
    "INCOMPLETE",
    "PARTIAL",
    "CONFLICTING",
    "UNAVAILABLE",
)

TRUTH_DOMAINS = (
    "planning",
    "schedule",
    "capacity",
    "commitment",
    "authorization",
    "order",
)

COLLECTIONS = (
    "products",
    "demands",
    "processes",
    "routings",
    "resources",
    "capacities",
    "time_windows",
    "constraints",
    "readiness",
    "bottleneck_evidence",
)


class CorrelationError(ValueError):
    """Raised for a missing or inconsistent explicit relationship."""


class HeuristicJoinRejected(CorrelationError):
    """Raised when a display/code field is used as a relationship key."""


def _digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest().upper()


def _index(records: list[Mapping[str, Any]], collection: str) -> dict[str, Mapping[str, Any]]:
    indexed: dict[str, Mapping[str, Any]] = {}
    for record in records:
        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id:
            raise CorrelationError(f"{collection} record lacks an explicit id")
        if record_id in indexed:
            raise CorrelationError(f"duplicate explicit id: {record_id}")
        indexed[record_id] = record
    return indexed


def resolve_explicit_id(
    source: Mapping[str, Any],
    reference_field: str,
    target_index: Mapping[str, Mapping[str, Any]],
) -> Mapping[str, Any]:
    """Resolve a relationship only through a declared singular *_id field."""

    if not reference_field.endswith("_id"):
        raise HeuristicJoinRejected(
            f"heuristic join rejected for non-ID field {reference_field!r}"
        )
    reference_id = source.get(reference_field)
    if not isinstance(reference_id, str) or not reference_id:
        raise CorrelationError(f"missing explicit relationship {reference_field}")
    target = target_index.get(reference_id)
    if target is None or target.get("id") != reference_id:
        raise CorrelationError(f"unresolved explicit relationship {reference_field}={reference_id}")
    return target


def _validate_fixture(fixture: Mapping[str, Any]) -> None:
    if fixture.get("fixture_id") != "ERP2-PLANNING-CAPACITY-GATE2-CTO-RECOVERY-FIXTURE-002":
        raise ValueError("unexpected recovery fixture id")
    if fixture.get("scenario_id") != "ERP2-PLANNING-CAPACITY-GATE2-CTO-RECOVERY-SCENARIO-002":
        raise ValueError("unexpected recovery scenario id")
    if tuple(fixture.get("evidence_states", ())) != EVIDENCE_STATES:
        raise ValueError("six-state evidence catalog changed")
    labels = fixture.get("truth_labels")
    if not isinstance(labels, Mapping) or labels.get("synthetic") is not True:
        raise ValueError("recovery fixture must be synthetic")
    if labels.get("read_only") is not True:
        raise ValueError("recovery fixture must be read-only")
    forbidden = (
        "business_truth",
        "production_truth",
        "planning_truth",
        "schedule_truth",
        "capacity_truth",
        "commitment_truth",
        "authorization_truth",
        "order_truth",
    )
    if any(labels.get(name) is not False for name in forbidden):
        raise ValueError("business and execution truth flags must all be false")
    for collection in COLLECTIONS:
        records = fixture.get(collection)
        if not isinstance(records, list) or not records:
            raise ValueError(f"{collection} must be a non-empty list")
        for record in records:
            if record.get("evidence_state") not in EVIDENCE_STATES:
                raise ValueError("record has unsupported evidence state")


def read_fixture(path: str | Path) -> tuple[dict[str, Any], bytes, str]:
    raw = Path(path).read_bytes()
    fixture = json.loads(raw.decode("utf-8"))
    if not isinstance(fixture, dict):
        raise ValueError("fixture root must be an object")
    _validate_fixture(fixture)
    return fixture, raw, _digest(raw)


def _indices(fixture: Mapping[str, Any]) -> dict[str, dict[str, Mapping[str, Any]]]:
    return {collection: _index(fixture[collection], collection) for collection in COLLECTIONS}


def _summary(chain: list[tuple[str, Mapping[str, Any]]]) -> dict[str, dict[str, Any]]:
    result = {state: {"count": 0, "ids": []} for state in EVIDENCE_STATES}
    for item_type, record in chain:
        state = record["evidence_state"]
        result[state]["count"] += 1
        result[state]["ids"].append(f"{item_type}:{record['id']}")
    return result


def _truth_separation() -> dict[str, dict[str, Any]]:
    claims = {
        "planning": "demand visibility input only",
        "schedule": "process/routing visibility only",
        "capacity": "evidence-derived capacity signal only",
        "commitment": "no commitment created",
        "authorization": "no authorization created",
        "order": "no order created",
    }
    return {
        domain: {"authoritative": False, "truth_flag": False, "claim": claims[domain]}
        for domain in TRUTH_DOMAINS
    }


def _bottleneck(evidence: list[Mapping[str, Any]]) -> dict[str, Any]:
    candidates = [
        {
            "evidence_id": item["id"],
            "resource_id": item["resource_id"],
            "capacity_id": item["capacity_id"],
            "signal": item["signal"],
            "evidence_state": item["evidence_state"],
            "evidence_ref": item["evidence_ref"],
        }
        for item in evidence
        if item.get("evidence_state") == "PRESENT"
    ]
    candidates.sort(key=lambda item: item["evidence_id"])
    return {
        "evidence_derived_only": True,
        "candidates": candidates,
        "resolution_state": "CONFLICTING",
        "authoritative_winner": None,
    }


def compose(fixture: Mapping[str, Any]) -> dict[str, Any]:
    _validate_fixture(fixture)
    index = _indices(fixture)
    product = index["products"][fixture["entrypoint_id"]]
    demand = resolve_explicit_id(product, "demand_id", index["demands"])
    process = resolve_explicit_id(demand, "process_id", index["processes"])
    routing = resolve_explicit_id(process, "routing_id", index["routings"])
    resource = resolve_explicit_id(process, "resource_id", index["resources"])
    capacity = resolve_explicit_id(resource, "capacity_id", index["capacities"])
    window = resolve_explicit_id(capacity, "window_id", index["time_windows"])
    constraint = resolve_explicit_id(window, "constraint_id", index["constraints"])
    readiness = resolve_explicit_id(constraint, "readiness_id", index["readiness"])

    if demand.get("product_id") != product["id"]:
        raise CorrelationError("demand/product IDs disagree")
    if process.get("product_id") != product["id"] or process.get("demand_id") != demand["id"]:
        raise CorrelationError("process/product/demand IDs disagree")
    if routing.get("process_id") != process["id"]:
        raise CorrelationError("routing/process IDs disagree")
    if routing.get("resource_id") != resource["id"]:
        raise CorrelationError("routing/resource IDs disagree")

    chain = [
        ("product", product),
        ("demand", demand),
        ("process", process),
        ("routing", routing),
        ("resource", resource),
        ("capacity", capacity),
        ("time_window", window),
        ("constraint", constraint),
        ("readiness", readiness),
    ]
    return {
        "fixture_id": fixture["fixture_id"],
        "scenario_id": fixture["scenario_id"],
        "correlation_mode": "EXPLICIT_ID_ONLY",
        "composition": {
            item_type: {
                "id": record["id"],
                "evidence_state": record["evidence_state"],
                "evidence_ref": record["evidence_ref"],
            }
            for item_type, record in chain
        },
        "evidence_state_catalog": list(EVIDENCE_STATES),
        "evidence_summary": _summary(chain),
        "truth_separation": _truth_separation(),
        "bottleneck": _bottleneck(fixture["bottleneck_evidence"]),
        "readiness": {
            "id": readiness["id"],
            "status": readiness["status"],
            "evidence_state": readiness["evidence_state"],
        },
        "boundary": {
            "synthetic": True,
            "read_only": True,
            "business_truth": False,
            "production_truth": False,
            "commitment_created": False,
            "authorization_created": False,
            "order_created": False,
        },
    }


def run(path: str | Path) -> dict[str, Any]:
    fixture, raw, fixture_sha256 = read_fixture(path)
    result = compose(fixture)
    result["fixture_sha256"] = fixture_sha256
    result["fixture_byte_length"] = len(raw)
    return result


def replay(path: str | Path) -> dict[str, Any]:
    first = run(path)
    second = run(path)
    first_serialized = json.dumps(first, sort_keys=True, separators=(",", ":"))
    second_serialized = json.dumps(second, sort_keys=True, separators=(",", ":"))
    if first_serialized != second_serialized:
        raise AssertionError("recovery replay is not deterministic")
    return {
        "deterministic": True,
        "result": first,
        "replay_result": second,
        "replay_sha256": _digest(first_serialized.encode("utf-8")),
    }


__all__ = [
    "CorrelationError",
    "EVIDENCE_STATES",
    "HeuristicJoinRejected",
    "compose",
    "read_fixture",
    "replay",
    "resolve_explicit_id",
    "run",
]
