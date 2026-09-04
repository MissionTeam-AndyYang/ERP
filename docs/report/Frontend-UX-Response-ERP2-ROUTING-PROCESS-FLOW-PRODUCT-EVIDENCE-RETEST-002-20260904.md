# Frontend UX Response - ERP2 Routing / Process Flow Product Evidence Retest 002

- Work item: ERP2-ROUTING-PROCESS-FLOW-PRODUCT-EVIDENCE-RETEST-002
- Authorization: ERP2-CIO-ROUTING-PROCESS-FLOW-SHARED-DEV-DATA-SURFACE-001
- Date: 2026-09-04
- Scope: bounded non-production Frontend / UX acceptance retest readiness check for `/routing`

## Assignment

Frontend / UX was asked to validate `/routing` against the real Backend service after Backend confirms real Shared DEV DB-backed Routing API readiness.

Required validation areas:

- real Backend path, not mock
- Product and WIP selector behavior
- Routing Version display
- ordered steps
- stage / group
- process identity / label
- Recipe and non-Recipe step display
- Packaging context
- resource eligibility
- standard performance
- source lineage
- warnings
- empty / error state
- no silent mock fallback
- no write / edit / approve / release controls

## Readiness Evidence Reviewed

Latest Backend evidence reviewed:

- Commit: `b54bc6b Clarify routing Shared DEV data surface blocker`
- Report: `docs/report/Backend-API-Response-ERP2-ROUTING-PROCESS-FLOW-PRODUCT-EVIDENCE-RETEST-001-20260904-001.md`

Backend classification:

**SAFE STOP - SHARED DEV ROUTING DATA SURFACE NOT READY**

The Backend report states that Shared DEV contains adjacent Product / WIP / BOM context tables, but does not contain the accepted Routing / Process Flow source tables required for the real DB-backed Routing Product contract.

## Shared DEV Data Surface Status

| Required source | Shared DEV status | Impact |
|---|---|---|
| `product_process` | MISSING | Cannot validate Routing Version identity |
| `process_flow` | MISSING | Cannot validate ordered Routing steps |
| `process` | MISSING | Cannot validate Process Master identity / labels |
| `process_capacity` | MISSING | Cannot validate governed standard performance |
| `product` | PRESENT | Adjacent Product context only |
| `inproduct` | PRESENT | Adjacent WIP context only |
| `product_spec` | PRESENT | Adjacent Recipe reference context only |
| `product_bom_spec` | PRESENT | Adjacent Packaging context only |

Because the Routing source tables are missing, Frontend / UX cannot truthfully validate Product/WIP Routing Version, ordered steps, Process Master identity, or governed standard-performance evidence against real DB-backed data.

## Service Window Check

No active Backend service window was found on the local ports used by prior retests or expected defaults during this readiness check.

Checked ports:

- `5000`
- `5013`
- `5025`
- `5027`
- `5031`
- `5033`
- `5035`

No real DB-backed Routing service URL was available for Retest 002 execution.

## Frontend Disposition

Frontend / UX did not execute a fake Product Evidence PASS using mock data.

Reason:

- The assignment explicitly requires real Backend validation after Backend readiness confirmation.
- The latest Backend evidence explicitly states Shared DEV Routing data surface is not ready.
- Using mock data or adjacent Product/BOM context to claim Routing Product Evidence PASS would misrepresent the acceptance result.

Already completed frontend evidence remains valid:

- `/routing` is aligned to the confirmed read-only Backend route family.
- API mode displays errors without silently substituting mock data.
- Manual mock mode remains available only by user selection.
- No Routing write / edit / approve / release controls are present.

## Retest 002 Status

| Area | Status |
|---|---|
| Real Backend path, not mock | BLOCKED - no ready real DB-backed Routing service window |
| Product / WIP selector real data | BLOCKED - required Routing source tables missing |
| Routing Version real data | BLOCKED - `product_process` missing |
| Ordered steps real data | BLOCKED - `process_flow` missing |
| Stage / group real data | BLOCKED - `process` / `process_flow` missing |
| Process identity / label real data | BLOCKED - `process` missing |
| Recipe and non-Recipe step display | BLOCKED for real Routing evidence; frontend mapping already implemented |
| Packaging context | BLOCKED for real Routing acceptance; adjacent table present but Routing linkage missing |
| Resource eligibility | BLOCKED - accepted governing source not available |
| Standard performance | BLOCKED - `process_capacity` missing |
| Source lineage | BLOCKED - accepted Routing lineage sources missing |
| Warnings | BLOCKED for real data; frontend warning mapping already implemented |
| Empty / error state | PASS by prior browser retest and implementation |
| No silent mock fallback | PASS by prior browser retest and implementation |
| No write / edit / approve / release controls | PASS by code inspection and prior retest |

## Required Next Action

Engineering A / Engineering B should provide one of the following before Frontend / UX reruns Retest 002:

1. A ready non-production Shared DEV Routing / Process Flow fixture containing `product_process`, `process_flow`, `process`, and `process_capacity`, plus representative Product and WIP routing rows.
2. An officially accepted alternate source-of-evidence mapping for the Routing Product contract, if the Shared DEV model should not expose those direct tables.
3. A reachable read-only Backend service window backed by that accepted data surface.

## Final Classification

**ROUTING_PROCESS_FLOW_PRODUCT_EVIDENCE_RETEST_002_SAFE_STOP_BACKEND_DATA_SURFACE_NOT_READY**

Frontend / UX is ready to rerun the real Backend browser validation after Shared DEV Routing data-surface readiness is confirmed. Retest 002 cannot be honestly completed as a PASS at this time because the latest Backend evidence explicitly classifies the required real DB-backed Routing source surface as not ready.
