# ERP Items API Field Readiness

Date: 2026-05-26
Scope: Frontend field-readiness notes for `GET /api/v1/items/dashboard`.

## Purpose

This document prepares the Items support page for a future read-only backend dashboard endpoint.

The Items page is a master-data overview. It should help users find item/SKU/material records, understand category coverage, and see master-data maintenance risks without implying create, edit, delete or approval workflows.

## Endpoint

Recommended endpoint:

```txt
GET /api/v1/items/dashboard
```

Current frontend hook:

```txt
useSupportDashboard("/api/v1/items/dashboard", itemsDashboardMock, "Items API unavailable")
```

## Current Frontend Shape

The current page consumes this local support-dashboard shape:

```ts
type ItemsDashboardResponse = {
  kpis: ItemKpi[];
  itemCards: ItemCard[];
  masterTasks: MasterDataTask[];
  categories: ItemCategoryColumn[];
};
```

## Recommended V1 Response Shape

```ts
type ItemsDashboardResponse = {
  kpis: ItemKpi[];
  itemCards: ItemCard[];
  masterTasks: MasterDataTask[];
  categories: ItemCategoryColumn[];
};

type ItemKpi = {
  label: string;
  value: string;
  hint: string;
  tone: "success" | "warning" | "danger" | "info" | "neutral";
};

type ItemCard = {
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

type MasterDataTask = {
  id: string;
  title: string;
  detail: string;
  meta: string;
  status: string;
  tone: "success" | "warning" | "danger" | "info" | "neutral";
};

type ItemCategoryColumn = {
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
| `kpis` | Yes | KPI strip for item count, finished goods, maintenance gaps and inactive items. |
| `itemCards` | Yes | Main item/SKU/material overview cards. |
| `masterTasks` | Yes | Master-data maintenance task panel. Valid empty array is allowed. |
| `categories` | Yes | Item category board. Valid empty array is allowed. |
| `eyebrow` | Yes | Item id/SKU display and card key. |
| `title` | Yes | Item display name. |
| `subtitle` | Yes | Item type, storage condition, source, production line or category context. |
| `status` | Yes | Display status such as mass production, low stock, maintenance needed or inactive. |
| `tone` | Yes | Stable display color mapping. |
| `rows` | Yes | Small item facts such as unit, shelf life, storage, spec, safety stock or BOM reference. |
| `masterTasks.id` | Yes | Task key and search token. |
| `masterTasks.detail` | Yes | Maintenance context. |
| `categories.title` | Yes | Category column heading. |
| `categories.items` | Yes | Category entries for the board. |

## Search Readiness

Current frontend search covers:

- Item id/SKU.
- Item name.
- Category detail.
- BOM reference.
- Status text.
- Card row labels and values.
- Master-data task id, title, detail and meta.

Server-side filters can wait until backend field names are stable.

Recommended future filter keys:

```txt
itemId
itemType
status
storageCondition
productionLine
hasBom
hasSpecGap
isActive
```

## V1 Read-Only Boundary

Allowed in V1:

- Return item overview cards.
- Return category board data.
- Return master-data maintenance tasks.
- Return display-ready status labels while canonical backend codes are stabilizing.
- Support frontend local search.

Not required for V1:

- Create item.
- Edit item master data.
- Deactivate/reactivate item.
- Approve item specification.
- Change BOM assignment.
- Change supplier, safety stock or storage rules.
- Upload or approve specification documents.

## Backend Confirmation Questions

| Question | Why it matters |
| --- | --- |
| Should `/items/dashboard` return all active items or only highlighted/risky items? | Defines page density and performance. |
| Are item quantities or stock signals sourced from Inventory/Warehouse or only item master? | Prevents master-data page from duplicating Warehouse responsibility. |
| Which item categories are canonical: finished goods, WIP, raw material, packaging or backend-owned codes? | Required for stable category board. |
| Should inactive items appear by default? | Affects search and status counts. |
| Should `rows` be display-ready strings or typed fields such as unit, shelf life and storage condition? | Typed fields are better for later filters; strings are faster for V1. |
| Does item status come from master data, production readiness, quality approval or inventory state? | Prevents inconsistent status mapping. |
| Can `masterTasks` be an empty array when no maintenance tasks exist? | Frontend should show empty state and not refill mock data. |

## Frontend Integration Notes

- The current `/items` UI is stable enough for a read-only dashboard endpoint.
- A dedicated `items-api` service/type file should be added only when the backend response is available.
- Avoid mutation buttons until authorization, audit and validation contracts exist.
- Keep Items separate from Batches: Items defines the master record; Batches manages operational batch distribution.

## Decision

```txt
items_api_field_readiness_created
```

The frontend is ready to integrate a read-only Items dashboard endpoint once the backend can provide item cards, category groups, KPI values and master-data task summaries.
