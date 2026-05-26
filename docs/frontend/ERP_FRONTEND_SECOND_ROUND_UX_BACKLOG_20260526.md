# ERP Frontend Second-Round UX Backlog

Date: 2026-05-26
Scope: Proposed second-round UX backlog after first-round low-risk refinement and owner decisions.

## Backlog Principles

1. Do not build mutation workflows until backend mutation contracts exist.
2. Keep API mapping in service files, not page components.
3. Prefer small, page-specific improvements before shared abstractions.
4. Add shared components only when at least three pages need the same behavior and wording is accepted.
5. Avoid changing visual hierarchy before real API payload density is known.

## Work Classification

| Tag | Meaning |
| --- | --- |
| `can_do_now` | Safe to do before backend endpoints are complete. |
| `wait_for_api` | Should wait for real payloads or confirmed field names. |
| `needs_owner_review` | Product/UX judgment needed before implementation. |
| `defer_v2` | Useful but outside V1 visibility/read-only boundary. |

## Priority Backlog

| Priority | Item | Tag | Scope | Notes |
| --- | --- | --- | --- | --- |
| P1 | Add shared runtime verification workflow to API integration process. | `can_do_now` | Docs/process | Template is already created; use it when backend endpoints are ready. |
| P1 | Support page search and empty-state review for Items/BOM/Batches/AI. | `can_do_now` | UX review/code later | Review is complete; Items, BOM, Batches and AI search/empty-state polish are now implemented locally. |
| P1 | Warehouse and Orders real-payload mapper planning. | `wait_for_api` | Service mapping | Mapping checklist is ready; wait for runtime response. |
| P1 | Status code to display-label mapper inventory. | `can_do_now` | Service helper/design | Inventory is documented; mapper code should wait until backend codes are known. |
| P2 | Shared empty state component. | `can_do_now` | Component | Consider only after reviewing current per-page empty states. |
| P2 | i18n extraction for shared shell and stable workspace labels. | `can_do_now` | i18n | Start with empty states, tabs and CTA labels; defer table/detail labels until API fields settle. |
| P2 | Support page dedicated types. | `wait_for_api` | Types/services | Items/BOM/Batches/AI currently use local shapes and `useSupportDashboard`; Items and BOM API readiness notes are now documented. |
| P2 | Cross-page drill-down links. | `wait_for_api` | Navigation | Needs stable ids and route/detail policy. |
| P2 | Advanced filters. | `wait_for_api` | UX/API | Placeholder tooltips already mark filters as pending API fields. |
| P3 | Mobile density pass. | `can_do_now` | UX QA | Use browser smoke after more real data exists. |
| P3 | Table column density and pinning. | `needs_owner_review` | UX | Needs user preference and data density from API. |
| P2 | AI today work status workspace. | `can_do_now` | AI/product/frontend | Owner accepted V1.1 direction and implementation is complete locally: today work status visibility and delayed item presentation first; recovery planning is deferred. |
| P3 | AI recovery planning trust model. | `needs_owner_review` | AI/product | Deferred to V1.3; source, confidence, audit and action boundaries still need backend/product confirmation. |
| P3 | Mutation workflows for dispatch, billing, scheduling, quote, approval. | `defer_v2` | UX/API | Outside accepted V1 CTA boundary. |

## Support Pages Backlog

| Page | Next UX step | Tag | Recommended timing |
| --- | --- | --- | --- |
| Items | Add search, empty states and clearer item/category task grouping. | `can_do_now` | Done locally; browser smoke remains pending because the local Browser plugin runtime is unavailable. |
| BOM | Add search and empty states now; wait on approved/development/trial filters. | `can_do_now` / `wait_for_api` | Search/empty states done locally; version filters should wait for BOM version/source rules. |
| Batches | Shift to item-centered batch operations dashboard. | `can_do_now` / `wait_for_api` | Done locally as a read-only item summary, batch distribution and selected batch detail workspace. Backend mapper should wait for the real payload. |
| AI | Shift from generic insights to today's work status and delayed item visibility. | `can_do_now` | V1.1 implementation is complete locally. Recovery planning is deferred to V1.3. |

## Core Pages Backlog

| Page group | Second-round item | Tag |
| --- | --- | --- |
| Warehouse / Orders | Real API mapper and runtime verification. | `wait_for_api` |
| Production / Quality | Status vocabulary mapper and blocker consistency. | `wait_for_api` |
| Planning / Purchasing | Material/work-order/receiving source alignment. | `wait_for_api` |
| Logistics / Finance | POD/billing-ready and AR/AP source alignment. | `wait_for_api` |
| Traceability / Batches | Boundary and shared batch identifiers. | `needs_owner_review` |
| Settings / i18n | Stable vocabulary extraction. | `can_do_now` |

## Suggested Next Concrete Tasks

Recommended sequence before backend is ready:

1. Wait for the real Batches payload, then add a dedicated `/batches` mapper/service.
2. Wait for Items/BOM endpoint priority, then add dedicated mapper/service files using the readiness notes.
3. Use the status-display mapper inventory when Warehouse, Orders or support endpoints return real status codes.
4. Re-run lint/build/route smoke after any mapper or payload-shape adjustment.
5. Keep broader mutation workflows deferred until backend authorization and audit contracts exist.

Recommended sequence after backend is ready:

1. Warehouse runtime verification.
2. Warehouse service mapper adjustment.
3. Orders runtime verification.
4. Orders service mapper adjustment.
5. Production and Quality status/blocker mapping.

## Open Owner Review Items

| Topic | Question | Why it matters |
| --- | --- | --- |
| Batches vs Traceability | Accepted: Batches should be item-centered batch operations; Traceability remains chain/recall investigation. | Prevents duplicate pages. |
| AI V1 boundary | Accepted: AI V1.1 should show today's work status and delayed items first. Recovery planning moves to V1.3. | Prevents unsupported action promises while making AI operationally useful. |
| Support pages priority | Should Items/BOM/Batches/AI be polished before backend core API is ready? | Accepted: start with Items as the lowest-risk support page polish. |
| i18n timing | Should stable labels move into dictionary before API integration? | Affects code churn during mapper work. |

## Current Decision

```txt
backlog_created_with_batches_traceability_boundary_accepted
```

Accepted page boundary:

```txt
Batches = item-centered batch operations dashboard.
Traceability = trace chain, document completeness and recall-scope investigation workspace.
```

Batches should become an item-centered operational workspace focused on item-level batch aggregation, multi-batch distribution, warehouse/location split, quantity availability, QA release/hold, expiry, quarantine and related work impact. Traceability should emphasize chain visualization, upstream/downstream investigation, document gaps and affected customers/shipments.

Batches operational workspace spec:

```txt
docs/frontend/ERP_BATCHES_OPERATIONAL_WORKSPACE_SPEC_20260526.md
```

Batches API field readiness:

```txt
docs/frontend/ERP_BATCHES_API_FIELD_READINESS_20260526.md
```

Batches implementation review:

```txt
docs/frontend/ERP_BATCHES_OPERATIONAL_WORKSPACE_IMPLEMENTATION_REVIEW_20260526.md
```

Items API field readiness:

```txt
docs/frontend/ERP_ITEMS_API_FIELD_READINESS_20260526.md
```

BOM API field readiness:

```txt
docs/frontend/ERP_BOM_API_FIELD_READINESS_20260526.md
```

Status display mapper inventory:

```txt
docs/frontend/ERP_STATUS_DISPLAY_MAPPER_INVENTORY_20260526.md
```

Accepted AI direction:

```txt
AI V1.1 = today work status visibility + delayed item presentation.
AI V1.2 = delayed reason analysis.
AI V1.3 = AI-assisted recovery planning.
```

AI should first help managers see today's work clearly: scheduled items, in-progress items, attention items and already-delayed items across orders, purchasing, warehouse, production, quality, logistics, documents and finance. Recovery plan generation is a later enhancement after the delay visibility model is stable. AI must not directly execute ERP mutations in V1.

AI V1.1 work-status spec:

```txt
docs/frontend/ERP_AI_TODAY_WORK_STATUS_WORKSPACE_SPEC_20260526.md
```

AI V1.1 implementation review:

```txt
docs/frontend/ERP_AI_V1_1_WORK_STATUS_IMPLEMENTATION_REVIEW_20260526.md
```

AI planning boundary note:

```txt
docs/frontend/ERP_AI_V1_RECOVERY_PLANNING_LAYOUT_NOTE_20260526.md
```

Accepted support page polish priority:

```txt
Items first, then BOM, then Batches.
```

Items is the lowest-risk support page because it is a master-data overview and does not strongly overlap with Traceability, Batches or AI. BOM is the next safe support page because search and empty states improve findability without implying unsupported approval, activation or formula mutation. Batches is safe for the same low-risk pattern now that its boundary with Traceability is accepted; this pass improves batch lifecycle findability without adding recall investigation or batch mutation UI. AI is safe for search and empty states only; larger recovery-planning layout changes should wait for accepted data shape and trust rules. These polish passes preserve the current Phase 1.5 overview structure and avoid mutation UI.

The safest default is still to wait for backend API readiness before broad UI changes, while using any spare frontend time on small support-page improvements and documentation.
