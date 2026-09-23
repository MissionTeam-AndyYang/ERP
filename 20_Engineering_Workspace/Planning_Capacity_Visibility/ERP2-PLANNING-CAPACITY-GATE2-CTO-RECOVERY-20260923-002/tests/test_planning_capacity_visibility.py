from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path


TEST_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = TEST_DIR.parent
sys.path.insert(0, str(PACKAGE_DIR / "runtime"))

from planning_capacity_visibility import (  # noqa: E402
    CorrelationError,
    EVIDENCE_STATES,
    HeuristicJoinRejected,
    compose,
    read_fixture,
    replay,
    resolve_explicit_id,
    run,
)


FIXTURE_PATH = PACKAGE_DIR / "fixture" / "planning_capacity_fixture.json"


class RecoveryPlanningCapacityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture, self.raw_before, self.fixture_hash = read_fixture(FIXTURE_PATH)
        self.result = compose(self.fixture)

    def test_recovery_identity(self) -> None:
        self.assertEqual(
            self.fixture["fixture_id"], "ERP2-PLANNING-CAPACITY-GATE2-CTO-RECOVERY-FIXTURE-002"
        )
        self.assertEqual(
            self.fixture["scenario_id"], "ERP2-PLANNING-CAPACITY-GATE2-CTO-RECOVERY-SCENARIO-002"
        )

    def test_required_explicit_ids(self) -> None:
        required = {
            "PRODUCT-001",
            "DEMAND-001",
            "PROCESS-MIX-001",
            "ROUTING-001",
            "RESOURCE-LINE-01",
            "CAPACITY-001",
            "WINDOW-001",
            "CONSTRAINT-001",
        }
        actual = {
            record["id"]
            for collection in (
                "products",
                "demands",
                "processes",
                "routings",
                "resources",
                "capacities",
                "time_windows",
                "constraints",
            )
            for record in self.fixture[collection]
        }
        self.assertTrue(required.issubset(actual))

    def test_six_evidence_states_are_present_in_replay(self) -> None:
        self.assertEqual(tuple(self.result["evidence_state_catalog"]), EVIDENCE_STATES)
        self.assertTrue(all(self.result["evidence_summary"][state]["count"] > 0 for state in EVIDENCE_STATES))

    def test_chain_is_explicit_id_only(self) -> None:
        self.assertEqual(self.result["correlation_mode"], "EXPLICIT_ID_ONLY")
        expected = {
            "product": "PRODUCT-001",
            "demand": "DEMAND-001",
            "process": "PROCESS-MIX-001",
            "routing": "ROUTING-001",
            "resource": "RESOURCE-LINE-01",
            "capacity": "CAPACITY-001",
            "time_window": "WINDOW-001",
            "constraint": "CONSTRAINT-001",
            "readiness": "READINESS-001",
        }
        self.assertEqual(
            {key: value["id"] for key, value in self.result["composition"].items()}, expected
        )

    def test_heuristic_join_is_rejected(self) -> None:
        with self.assertRaises(HeuristicJoinRejected):
            resolve_explicit_id(
                {"product_code": "RECOVERY-SYNTHETIC-PRODUCT-001"},
                "product_code",
                {"PRODUCT-001": {"id": "PRODUCT-001"}},
            )

    def test_missing_id_is_rejected(self) -> None:
        with self.assertRaises(CorrelationError):
            resolve_explicit_id({}, "demand_id", {"DEMAND-001": {"id": "DEMAND-001"}})

    def test_inconsistent_id_chain_is_rejected(self) -> None:
        broken = json.loads(json.dumps(self.fixture))
        broken["processes"][0]["demand_id"] = "DEMAND-999"
        with self.assertRaises(CorrelationError):
            compose(broken)

    def test_truth_flags_and_authority_are_false(self) -> None:
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
        self.assertTrue(all(self.fixture["truth_labels"][name] is False for name in forbidden))
        self.assertTrue(all(not item["authoritative"] for item in self.result["truth_separation"].values()))

    def test_planning_schedule_capacity_commitment_authorization_order_are_distinct(self) -> None:
        self.assertEqual(
            set(self.result["truth_separation"]),
            {"planning", "schedule", "capacity", "commitment", "authorization", "order"},
        )
        self.assertFalse(self.result["boundary"]["commitment_created"])
        self.assertFalse(self.result["boundary"]["authorization_created"])
        self.assertFalse(self.result["boundary"]["order_created"])

    def test_bottleneck_is_evidence_derived_without_winner(self) -> None:
        self.assertTrue(self.result["bottleneck"]["evidence_derived_only"])
        self.assertEqual(self.result["bottleneck"]["authoritative_winner"], None)
        self.assertEqual(self.result["bottleneck"]["candidates"][0]["capacity_id"], "CAPACITY-001")

    def test_unavailable_and_conflict_states_are_not_collapsed(self) -> None:
        self.assertEqual(self.result["composition"]["time_window"]["evidence_state"], "UNAVAILABLE")
        self.assertEqual(self.result["composition"]["constraint"]["evidence_state"], "CONFLICT")
        self.assertEqual(self.result["readiness"]["status"], "CONDITIONALLY_READY")

    def test_fixture_bytes_are_unchanged(self) -> None:
        raw_after = FIXTURE_PATH.read_bytes()
        self.assertEqual(self.raw_before, raw_after)
        self.assertEqual(self.fixture_hash, hashlib.sha256(raw_after).hexdigest().upper())

    def test_replay_is_deterministic(self) -> None:
        result = replay(FIXTURE_PATH)
        self.assertTrue(result["deterministic"])
        self.assertEqual(result["result"], result["replay_result"])

    def test_run_reports_fixture_provenance(self) -> None:
        result = run(FIXTURE_PATH)
        self.assertEqual(result["fixture_sha256"], self.fixture_hash)
        self.assertEqual(result["fixture_byte_length"], len(self.raw_before))
        self.assertTrue(result["boundary"]["synthetic"])
        self.assertTrue(result["boundary"]["read_only"])


if __name__ == "__main__":
    unittest.main()
