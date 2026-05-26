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
| P1 | Status code to display-label mapper inventory. | `can_do_now` | Service helper/design | Status vocabulary accepted; mapper code should wait until backend codes are known. |
| P2 | Shared empty state component. | `can_do_now` | Component | Consider only after reviewing current per-page empty states. |
| P2 | i18n extraction for shared shell and stable workspace labels. | `can_do_now` | i18n | Start with empty states, tabs and CTA labels; defer table/detail labels until API fields settle. |
| P2 | Support page dedicated types. | `wait_for_api` | Types/services | Items/BOM/Batches/AI currently use local shapes and `useSupportDashboard`. |
| P2 | Cross-page drill-down links. | `wait_for_api` | Navigation | Needs stable ids and route/detail policy. |
| P2 | Advanced filters. | `wait_for_api` | UX/API | Placeholder tooltips already mark filters as pending API fields. |
| P3 | Mobile density pass. | `can_do_now` | UX QA | Use browser smoke after more real data exists. |
| P3 | Table column density and pinning. | `needs_owner_review` | UX | Needs user preference and data density from API. |
| P3 | AI insight trust model. | `needs_owner_review` | AI/product | Recovery-planning layout note is created; source, confidence, audit and action boundaries still need backend/product confirmation. |
| P3 | Mutation workflows for dispatch, billing, scheduling, quote, approval. | `defer_v2` | UX/API | Outside accepted V1 CTA boundary. |

## Support Pages Backlog

| Page | Next UX step | Tag | Recommended timing |
| --- | --- | --- | --- |
| Items | Add search, empty states and clearer item/category task grouping. | `can_do_now` | Done locally; browser smoke remains pending because the local Browser plugin runtime is unavailable. |
| BOM | Add search and empty states now; wait on approved/development/trial filters. | `can_do_now` / `wait_for_api` | Search/empty states done locally; version filters should wait for BOM version/source rules. |
| Batches | Add search and empty states now; wait on selected batch detail pattern. | `can_do_now` / `wait_for_api` | Search/empty states done locally; selected detail should wait for batch detail fields. |
| AI | Keep read-only, but expand from insight summary to recovery planning assist with late-progress detection and recommended recovery plans. | `needs_owner_review` | Search/empty states done locally; larger recovery-planning UI should wait for data-shape acceptance. |

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

1. Review Batches versus Traceability boundary with owner.
2. Review AI V1 trust/action boundary with owner.
3. Review whether a shared empty-state component is worth extracting after four support pages now use the same pattern.
4. Optionally create API field readiness docs for Items, BOM, Batches and AI if backend will implement those endpoints soon.

Recommended sequence after backend is ready:

1. Warehouse runtime verification.
2. Warehouse service mapper adjustment.
3. Orders runtime verification.
4. Orders service mapper adjustment.
5. Production and Quality status/blocker mapping.

## Open Owner Review Items

| Topic | Question | Why it matters |
| --- | --- | --- |
| Batches vs Traceability | Should Batches be batch lifecycle management while Traceability remains chain/recall investigation? | Prevents duplicate pages. |
| AI V1 boundary | Should AI remain read-only, while adding late-progress detection and recovery plan recommendations? | Prevents unsupported action promises while making AI operationally useful. |
| Support pages priority | Should Items/BOM/Batches/AI be polished before backend core API is ready? | Accepted: start with Items as the lowest-risk support page polish. |
| i18n timing | Should stable labels move into dictionary before API integration? | Affects code churn during mapper work. |

## Current Decision

```txt
backlog_created_with_batches_traceability_boundary_accepted
```

Accepted page boundary:

```txt
Batches = batch lifecycle and operational control workspace.
Traceability = trace chain, document completeness and recall-scope investigation workspace.
```

Batches should become a dense operational table workspace focused on batch status, QA release, expiry, quarantine, location, quantity and batch tasks. Traceability should emphasize chain visualization, upstream/downstream investigation, document gaps and affected customers/shipments.

Accepted AI direction:

```txt
AI V1 = read-only insights + recovery planning assist.
```

AI should identify late or at-risk progress across orders, production, purchasing, quality, logistics, workforce, documents and finance, then propose a recovery plan with reasons, affected modules, expected recovered time, risk reduction and confidence. AI must not directly execute ERP mutations in V1.

AI recovery-planning layout note:

```txt
docs/frontend/ERP_AI_V1_RECOVERY_PLANNING_LAYOUT_NOTE_20260526.md
```

Accepted support page polish priority:

```txt
Items first, then BOM, then Batches.
```

Items is the lowest-risk support page because it is a master-data overview and does not strongly overlap with Traceability, Batches or AI. BOM is the next safe support page because search and empty states improve findability without implying unsupported approval, activation or formula mutation. Batches is safe for the same low-risk pattern now that its boundary with Traceability is accepted; this pass improves batch lifecycle findability without adding recall investigation or batch mutation UI. AI is safe for search and empty states only; larger recovery-planning layout changes should wait for accepted data shape and trust rules. These polish passes preserve the current Phase 1.5 overview structure and avoid mutation UI.

The safest default is still to wait for backend API readiness before broad UI changes, while using any spare frontend time on small support-page improvements and documentation.
