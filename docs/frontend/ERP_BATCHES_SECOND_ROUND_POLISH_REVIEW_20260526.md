# ERP Batches Second-Round Polish Review

Date: 2026-05-26
Scope: Batches support page low-risk polish before backend API integration.

## Review Metadata

| Field | Value |
| --- | --- |
| Page / route | Batches / `/batches` |
| Related API endpoint | `GET /api/v1/batches/dashboard` |
| Data source during review | `mock` with generic support-dashboard API fallback |
| Change scope | Search, empty states and item-centered read-only workspace refactor |
| Mutation scope | None |

## UX Polish Completed

| Item | Result |
| --- | --- |
| Search behavior | Added page-level search for item summaries, selected-item batch distribution and batch operational detail fields. |
| Search fields | Search covers item, batch no, warehouse, location, QA status, batch stage, related work and risk tags. |
| Empty state | Added controlled empty states for item summary, selected-item distribution and selected batch detail. |
| Existing structure | Refactored from lifecycle board/cards to item summary, batch distribution and selected batch detail. |
| API contract | Mock fallback now uses `itemSummaries`; page still uses `useSupportDashboard("/api/v1/batches/dashboard", ...)`. |
| V1 boundary | No release, quarantine, adjustment, recall or shipment mutation UI added. |

## Boundary Confirmation

Accepted page boundary:

```txt
Batches = item-centered batch operations dashboard.
Traceability = trace chain, document completeness and recall-scope investigation workspace.
```

This polish stays inside the Batches boundary by showing item-level aggregation, batch distribution and operational detail. It does not add trace-chain visualization, recall-scope investigation or customer/shipment impact analysis.

Workspace spec:

```txt
docs/frontend/ERP_BATCHES_OPERATIONAL_WORKSPACE_SPEC_20260526.md
```

Implementation review:

```txt
docs/frontend/ERP_BATCHES_OPERATIONAL_WORKSPACE_IMPLEMENTATION_REVIEW_20260526.md
```

## Verification

| Check | Result | Notes |
| --- | --- | --- |
| `npm.cmd run lint` | Pass | ESLint completed successfully. |
| `npm.cmd run build` | Pass | Next.js production build completed successfully. |
| `/batches` HTTP route responds | Pass | `Invoke-WebRequest http://127.0.0.1:3000/batches` returned HTTP 200. |
| Browser interaction smoke | Blocked | In-app browser runtime is currently unavailable because the Browser plugin cache is missing `scripts/browser-client.mjs`. |
| Desktop/mobile overflow | Not run | Requires browser runtime to inspect viewport width. |

## Remaining Follow-Up

| Item | Priority | Dependency |
| --- | --- | --- |
| Re-run browser smoke for search, empty states and mobile overflow. | High | Browser runtime restored. |
| Create item-centered Batches API field readiness notes. | Done | `docs/frontend/ERP_BATCHES_API_FIELD_READINESS_20260526.md` |
| Design the future item summary + batch distribution workspace. | Done | Implemented locally with mock fallback. |
| Decide selected batch detail panel fields. | Done for V1 mock | Backend detail endpoint can expand later. |
| Align batch status vocabulary with Warehouse and Quality. | Medium | Backend status codes and mapper rules. |
| Consider shared empty-state component after AI or another support page repeats the same pattern. | Low | At least three support pages using same pattern. |

## Decision

```txt
batches_item_centered_polish_implemented_with_browser_smoke_pending
```

Reason:

The change upgrades Batches from a lifecycle overview into a practical read-only batch operations workspace without changing the accepted Batches versus Traceability boundary or promising unsupported batch operations.
