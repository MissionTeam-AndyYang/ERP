# ERP Support Pages Refinement Review

Date: 2026-05-26
Scope: Items, BOM, Batches and AI pages after first-round core workspace refinement.

## Review Summary

Items, BOM, Batches and AI are currently useful Phase 1.5 support pages, but they do not yet match the refined core workspace pattern used by Warehouse, Orders, Production, Quality, Planning, Purchasing, Logistics, Finance, R&D, Workforce, Traceability and Settings.

They are stable enough to remain in the product, but the next UX pass should decide whether each support page should become:

1. A full operational workspace.
2. A compact master-data/support view.
3. A read-only landing/overview until API contracts exist.

## Shared Findings

| Area | Current state | UX impact | Recommendation |
| --- | --- | --- | --- |
| Page structure | Uses `ModuleHero`, KPI cards, process board, detail cards and compact task list. | Clear high-level overview, but less operational than core workspaces. | Keep for now; refine only after role and API scope are clearer. |
| Search | No page-level search. | Users cannot quickly find item/BOM/batch/AI insight records. | Add search in second-round refinement. |
| Tabs/views | No scoped workspace tabs. | Harder to separate categories, lifecycle, tasks and risks. | Add tabs only if the page becomes a full workspace. |
| Detail sync | Cards are static; no selected row/detail panel pattern. | No drill-in workflow comparable to core pages. | Add selected detail only after API detail fields are known. |
| Empty states | No explicit empty state for API empty arrays. | If API returns empty arrays, panels may appear blank. | Add shared empty states before runtime integration. |
| API hook | Uses generic `useSupportDashboard` shallow merge. | Simple and stable, but less schema-aware than dedicated services. | Keep until support page APIs are prioritized. |
| Types | Data shape is local to each page. | Makes mapping harder when real APIs arrive. | Add page-specific types when integration begins. |
| i18n | Text is hardcoded in components. | Consistent with current prototype, but not i18n-ready. | Move stable labels after final page role is confirmed. |

## Items Review

Route:

```txt
/items
```

Current purpose:

```txt
Item/material/product master data overview.
```

Current strengths:

- Clear master-data categories: finished goods, WIP, raw materials, packaging.
- Good task list for missing specs and alternate material setup.
- Strong relation to Warehouse, R&D, BOM and Purchasing.

Current gaps:

| Gap | Priority | Dependency |
| --- | --- | --- |
| No search by item no, item name, category or supplier. | High | Can do before API. |
| No item detail panel for shelf life, temperature, safety stock and applicable lines. | Medium | Wait for API field confirmation. |
| No clear distinction between active/inactive/prototype item states. | Medium | Needs status vocabulary confirmation. |
| Local data shape is not typed as an integration contract. | Medium | Can do when API spec is drafted. |

Recommended next step:

```txt
Keep as support page until Warehouse/Orders API integration starts.
Then decide whether Items needs full workspace refinement or only search + empty state.
```

## BOM Review

Route:

```txt
/bom
```

Current purpose:

```txt
BOM/formula version and process parameter overview.
```

Current strengths:

- Lifecycle board communicates R&D, trial, approval and production status.
- Detail cards show version, major materials and process parameters.
- Good bridge between R&D, Production and Planning.

Current gaps:

| Gap | Priority | Dependency |
| --- | --- | --- |
| No search by BOM no, item, version or parameter. | High | Can do before API. |
| No version comparison or approved-production-only filter. | High | Needs BOM API fields. |
| Change tasks are static and not grouped by owner/approval state. | Medium | Needs backend workflow source. |
| No clear guard against Planning using development BOMs. | High | Needs API/business rule confirmation. |

Recommended next step:

```txt
Treat BOM as a high-priority support page after Planning API mapping begins.
Do not build mutation or approval UI until BOM authorization and workflow APIs exist.
```

## Batches Review

Route:

```txt
/batches
```

Current purpose:

```txt
Batch lifecycle overview across raw material, WIP, finished goods and shipment.
```

Current strengths:

- Strong lifecycle representation.
- Useful expiry and QA risk examples.
- Natural link to Warehouse, Quality and Traceability.

Current gaps:

| Gap | Priority | Dependency |
| --- | --- | --- |
| No search by batch no, item, work order or shipment. | High | Can do before API. |
| No selected batch detail panel. | High | Needs batch trace/detail fields. |
| Expiry/QA/warehouse state are not normalized across modules. | Medium | Needs Warehouse/Quality status mapping. |
| Could overlap with Traceability unless page role is clarified. | High | Product decision needed. |

Recommended next step:

```txt
Clarify Batches versus Traceability:
Batches should manage batch status/lifecycle; Traceability should explain upstream/downstream chain and recall scope.
```

## AI Review

Route:

```txt
/ai
```

Current purpose:

```txt
AI insights, late-progress detection and recovery planning assist overview.
```

Current strengths:

- Communicates AI value clearly: insight, warning, recommendation and confirmation.
- Examples are operationally relevant.
- Works as a future decision-assist surface.
- Can become the cross-module recovery planning layer, not just an integrated message center.

Current gaps:

| Gap | Priority | Dependency |
| --- | --- | --- |
| AI data source and trust model are not defined. | High | Requires product/backend decision. |
| No confidence/explanation standard beyond static rows. | High | Needs AI design spec. |
| Assistant actions look executable but are not wired. | High | Needs V1 CTA boundary review. |
| No audit trail for AI recommendations. | Medium | Needs backend/audit design. |
| Late-progress detection and recovery plan structure are not yet modeled. | High | Needs AI V1 information architecture and source fields. |

Recommended next step:

```txt
Keep AI read-only in V1, but expand the page concept from insights to recovery planning assist.
AI should identify late or at-risk progress and recommend a recovery plan without directly executing ERP operations.
```

Recommended AI V1 sections:

| Section | Purpose |
| --- | --- |
| Late progress | Orders, work orders, purchasing arrivals, quality release, dispatch, workforce, documents or billing items that are behind or at risk. |
| Root cause | Cross-module reason summary, such as material shortage, capacity conflict, quality hold or missing document. |
| Recovery plan | Suggested steps, affected modules, expected recovered time, risk reduction and confidence score. |
| Evidence | Source records and signals used by AI. |
| Supervisor review | Read-only decision state such as `待確認`, `已讀`, `待追蹤`, not direct mutation. |

## Decision

Current decision:

```txt
reviewed_for_second_round_backlog
```

The support pages should not be deeply refactored before backend API contracts for core pages are proven. They are good candidates for targeted second-round improvements: search, empty states and clearer page role boundaries.

## Immediate Follow-Up

| Item | Owner | Timing |
| --- | --- | --- |
| Add support pages to second-round UX backlog. | Frontend | Now |
| Decide Batches versus Traceability boundary. | Owner / Frontend | Before Batches refinement |
| Decide AI V1 trust/action boundary. | Owner / Frontend | Before AI refinement |
| Create API field readiness docs for Items/BOM/Batches/AI only if backend will implement their endpoints. | Frontend | After backend priority confirmation |
