# ERP BOM API Field Readiness

Date: 2026-05-26
Scope: Frontend field-readiness notes for `GET /api/v1/bom/dashboard`.

## Purpose

This document prepares the BOM support page for a future read-only backend dashboard endpoint.

BOM should help users see recipe/formula versions, lifecycle stage, production readiness and change requests. V1 should not imply approval, activation, formula editing or production release mutations.

## Endpoint

Recommended endpoint:

```txt
GET /api/v1/bom/dashboard
```

Current frontend hook:

```txt
useSupportDashboard("/api/v1/bom/dashboard", bomDashboardMock, "BOM API unavailable")
```

## Current Frontend Shape

The current page consumes this local support-dashboard shape:

```ts
type BomDashboardResponse = {
  kpis: BomKpi[];
  bomCards: BomCard[];
  changeTasks: BomChangeTask[];
  lifecycle: BomLifecycleColumn[];
};
```

## Recommended V1 Response Shape

```ts
type BomDashboardResponse = {
  kpis: BomKpi[];
  bomCards: BomCard[];
  changeTasks: BomChangeTask[];
  lifecycle: BomLifecycleColumn[];
};

type BomKpi = {
  label: string;
  value: string;
  hint: string;
  tone: "success" | "warning" | "danger" | "info" | "neutral";
};

type BomCard = {
  eyebrow: string;
  title: string;
  subtitle: string;
  status: string;
  tone: "success" | "warning" | "danger" | "info" | "neutral";
  rows: Array<{
    label: string;
    value: string;
  }>;
};

type BomChangeTask = {
  id: string;
  title: string;
  detail: string;
  meta: string;
  status: string;
  tone: "success" | "warning" | "danger" | "info" | "neutral";
};

type BomLifecycleColumn = {
  title: string;
  items: Array<{
    id: string;
    title: string;
    detail: string;
    tone: "success" | "warning" | "danger" | "info" | "neutral";
  }>;
};
```

## Required Fields

| Field group | Required | Frontend use |
| --- | --- | --- |
| `kpis` | Yes | KPI strip for total versions, R&D, approved and change-pending counts. |
| `bomCards` | Yes | Main BOM/version overview cards. |
| `changeTasks` | Yes | Change request and review task panel. Valid empty array is allowed. |
| `lifecycle` | Yes | BOM lifecycle board. Valid empty array is allowed. |
| `eyebrow` | Yes | BOM id and version display, such as `BOM-FG-CURRY-101 v3.2`. |
| `title` | Yes | Formula or BOM display name. |
| `subtitle` | Yes | Related item, line or usage context. |
| `status` | Yes | Display status such as production approved, trial, review pending or change pending. |
| `tone` | Yes | Stable display color mapping. |
| `rows` | Yes | Small BOM facts such as main material, critical process parameter and effective date. |
| `changeTasks.id` | Yes | Change request key and search token. |
| `changeTasks.detail` | Yes | Review or change context. |
| `lifecycle.title` | Yes | Lifecycle stage heading. |
| `lifecycle.items` | Yes | Lifecycle entries for R&D, trial, approval and production stages. |

## Search Readiness

Current frontend search covers:

- BOM id.
- Item id and item name text.
- Version text.
- Process parameter rows.
- Lifecycle item text.
- Change task id, title, detail and meta.

Server-side filters can wait until backend field names are stable.

Recommended future filter keys:

```txt
bomId
itemId
version
status
lifecycleStage
effectiveDate
approvedForProduction
hasPendingChange
productionLine
```

## V1 Read-Only Boundary

Allowed in V1:

- Return BOM/version overview cards.
- Return lifecycle board data.
- Return change request summaries.
- Return display-ready status labels while canonical backend codes are stabilizing.
- Support frontend local search.

Not required for V1:

- Create BOM.
- Edit formula lines.
- Approve or reject BOM.
- Activate or deactivate a version.
- Release version to production.
- Change production parameters.
- Create engineering change requests.
- Guard production scheduling by mutation workflow.

## BOM Version Safety Notes

The frontend can display trial or development BOM versions, but Planning and Production must not treat those versions as production-ready unless backend status rules explicitly allow it.

Recommended backend-owned flags:

```txt
approvedForProduction
effectiveFrom
effectiveTo
isCurrentProductionVersion
isTrialVersion
requiresReview
```

These flags are not required for the current support page mock, but they are important before Planning, Orders or Production can rely on BOM data.

## Backend Confirmation Questions

| Question | Why it matters |
| --- | --- |
| Which table or service owns canonical BOM version status? | Prevents inconsistent approved/trial/development labels. |
| Can one item have multiple effective production BOM versions? | Determines whether frontend needs version conflict warnings. |
| How should development, trial, approved and inactive versions be filtered? | Needed before advanced filters or Planning integration. |
| Should critical process parameters be returned as typed fields or display rows? | Typed fields support validation; rows are faster for V1. |
| Are BOM change requests available from backend, or should `changeTasks` be aggregated elsewhere? | Defines task panel source. |
| Can `changeTasks` and `lifecycle` intentionally be empty arrays? | Frontend should show empty state and not refill mock data. |
| Should BOM cards include material line counts and allergen/nutrition readiness? | Useful for food manufacturing but may belong to R&D or Quality. |

## Frontend Integration Notes

- The current `/bom` UI is stable enough for a read-only dashboard endpoint.
- A dedicated `bom-api` service/type file should be added only when the backend response is available.
- Do not add approval, activation or formula-editing UI until authorization, audit and version-control contracts exist.
- Keep BOM separate from Items: Items defines the master record; BOM defines versioned formula and process structure.

## Decision

```txt
bom_api_field_readiness_created
```

The frontend is ready to integrate a read-only BOM dashboard endpoint once the backend can provide BOM cards, lifecycle groups, KPI values and change-task summaries.
