# ERP i18n And Frontend Cleanup Inventory

Date: 2026-05-26
Scope: Inventory of frontend cleanup work that can wait until API contracts stabilize.

## Current i18n State

`src/i18n/dictionary.ts` currently covers:

- App shell labels.
- Navigation labels.
- Basic language selector labels.
- One Warehouse layout title.

Most workspace-specific headings, tab labels, table headers, empty states and CTA labels still live directly in page components.

## Recommended Extraction Order

| Priority | Area | Reason |
| --- | --- | --- |
| 1 | Shared empty state labels | These are repeated across all refined pages and unlikely to change structurally. |
| 2 | Tab labels and tab descriptions | These define stable workspace language and should be consistent across locales. |
| 3 | Header CTA labels and tooltips | These encode the V1 view-navigation boundary. |
| 4 | Table headers | Useful after API field names stabilize. |
| 5 | Detail panel field labels | Best after real payload confirms field names and optionality. |
| 6 | Status labels | Best after backend vocabulary is confirmed. |

## i18n Keys To Consider Later

| Key family | Example |
| --- | --- |
| `workspace.<name>.layoutTitle` | `workspace.warehouse.layoutTitle` |
| `workspace.<name>.heroTitle` | `workspace.orders.heroTitle` |
| `workspace.<name>.tabs.<tab>` | `workspace.logistics.tabs.dispatchRisk` |
| `workspace.<name>.empty.search` | `workspace.finance.empty.search` |
| `workspace.<name>.cta.primary` | `workspace.traceability.cta.query` |
| `status.risk.normal` | `status.risk.normal` |
| `status.workflow.blocked` | `status.workflow.blocked` |

## Low-Risk Cleanup Review

| Area | Current state | Recommendation |
| --- | --- | --- |
| Service fallback | Dashboard services now share `withFallbackArray` for array fields. | Keep. |
| Hook pattern | Hooks initialize mock data, fetch service result, guard unmounted updates. | Keep for V1. |
| Page search helpers | Each page currently owns local search helper functions. | Keep until cross-page requirements settle; avoid premature abstraction. |
| Empty state component | Each page has a small local `EmptyState`. | Consider shared component only after wording is finalized. |
| CTA behavior | CTAs switch views rather than mutating data. | Keep until mutation APIs exist. |
| Support pages | Items, BOM, Batches, AI use `useSupportDashboard` and are less refined. | Review in second-round refinement, not in API integration first pass. |

## Cleanup Deferrals

Do not do these before backend runtime data is available:

1. Strict runtime schema validation.
2. Broad shared table abstraction.
3. Moving every label into i18n.
4. Cross-page drill-down links.
5. Mutation modals for create/update actions.

Reason:

These changes become easier and safer after real API fields and status vocabularies are known.
