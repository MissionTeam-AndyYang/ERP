# CONV-05 API / Source / App-Registration / Test Conformance

## Candidate Identity

- Branch: `codex/erp2-common-baseline-20260918-001`
- CONV-04 parent: `19efd0e222b2e792c444d3ab6d2e161b750e27f3`
- Original authorized base: `main@89b374109312720b3ff6669a9664fb0cf8f9a6ba`
- Scope: committed, local, non-Production common collaboration candidate only.

This record reconciles existing committed contracts, source, application registration, focused tests, and evidence/runbook references. It introduces no endpoint, source behavior, schema, runtime, or test-semantic change.

## Conformance Matrix

| Surface | Formal contract | Committed source / registration | Focused test | Candidate result |
|---|---|---|---|---|
| Product/WIP 360 | `docs/spec/api/product_wip_360.md` — `GET /api/v2/product-wip-360/overview` | `api/v2/product_wip_360.py`, `product_wip_360_uri.py`, registered in `app.py` | `restserver/tests/test_product_wip_360_api.py` | `SYNCHRONIZED FOR BOUNDED CANDIDATE` |
| Packaging Specification | `docs/spec/api/packaging_specification.md` — `GET /api/v2/packaging-specification/overview` | `api/v2/packaging_specification.py`, URI, registered in `app.py` | `restserver/tests/test_packaging_specification_api.py` | `SYNCHRONIZED FOR BOUNDED CANDIDATE / FIXTURE LIMITATION PRESERVED` |
| Inventory | `docs/spec/api/inventory.md` | committed v2 inventory modules | `restserver/tests/test_inventory_read_api.py` | `SYNCHRONIZED FOR BOUNDED CANDIDATE` |
| Traceability | `docs/spec/api/trace.md` | committed trace URI/service surfaces | `restserver/tests/test_traceability_api.py` | `SYNCHRONIZED FOR BOUNDED CANDIDATE` |
| Warehouse dashboard | `docs/spec/api/warehouse.md` | committed warehouse modules | `restserver/tests/test_warehouse_dashboard.py` | `SYNCHRONIZED FOR BOUNDED CANDIDATE` |
| Warehouse receipt movement | `docs/spec/api/warehouse.md` | committed warehouse modules | `restserver/tests/test_warehouse_receipt_movement_api.py` | `SYNCHRONIZED FOR BOUNDED CANDIDATE` |
| Warehouse outbound pick | `docs/spec/api/warehouse.md` | committed warehouse modules | `restserver/tests/test_warehouse_outbound_pick_api.py` | `SYNCHRONIZED FOR BOUNDED CANDIDATE` |
| Warehouse reversal/idempotency | `docs/spec/api/warehouse.md` | committed warehouse modules | `restserver/tests/test_warehouse_reversal_idempotency_api.py` | `SYNCHRONIZED FOR BOUNDED CANDIDATE` |
| Warehouse transfer | `docs/spec/api/warehouse.md` | committed warehouse modules | `restserver/tests/test_warehouse_transfer_api.py` | `SYNCHRONIZED FOR BOUNDED CANDIDATE` |
| Warehouse proposal-only | `docs/spec/api/warehouse.md` | committed warehouse modules | `restserver/tests/test_warehouse_proposal_only_api.py` | `SYNCHRONIZED FOR BOUNDED CANDIDATE` |
| Warehouse adjustment reconciliation | `docs/spec/api/warehouse.md` | committed warehouse modules | `restserver/tests/test_warehouse_adjustment_reconciliation_api.py` | `SYNCHRONIZED FOR BOUNDED CANDIDATE` |

## Explicit Exceptions

| Exception | Classification | Treatment |
|---|---|---|
| Product/WIP evidence-field additions in protected `main` working tree | `OUT OF SCOPE / UNCOMMITTED / UNVERIFIED` | Not copied to this candidate; requires separate admission, contract update, and fresh testing |
| Manufacturing Definition backend and registration candidate | `OUT OF SCOPE / UNTRACKED / NOT INTEGRATED` | Not copied; formal API contract, dedicated tests, and bounded runtime validation require separate authority |
| Phase 8-12 custody and M11.1 artifacts | `SEPARATE GOVERNED EVIDENCE` | Preserved; not merged, promoted, or published by CONV-05 |
| Remote publication/upstream/CONV-07 | `NOT AUTHORIZED` | No action |

## Runbook / Evidence Correlation

- DB conformance and extension treatment: `docs/spec/database/CONV-04-DB-CONFORMANCE-MATRIX-20260918.md` and its JSON manifest.
- API/source/registration/test scope: this record.
- The focused test set is attributable to the branch/commit identified above and must be run without Production database, actual data, or external-service activation.
- Passing tests demonstrate only the bounded committed candidate; they do not accept excluded local deltas or select a canonical Source-of-Truth.

## Integrated Validation Preconditions

1. CONV-04 is committed and gate eligible.
2. This record is committed on the same local branch.
3. Named focused tests pass from the isolated worktree.
4. Branch remains local-only with no upstream or remote publication.
5. Protected main remains untouched.

## Boundary

No schema migration, API semantic redesign, new implementation, Source-of-Truth selection, L5, Production/Actual, Product Version 3, remote publication, upstream, push, or CONV-07 action is authorized by this document.

