# ERP Product R&D / Costing Workspace Spec

日期：2026-05-23

## Status

Product R&D / Costing first-version workspace added as the pre-order source for ODM food product development, BOM control, costing, and quotation basis.

- Page: `src/app/rd/page.tsx`
- Mock data: `src/mock/rd.ts`
- Types: `src/types/rd.ts`

## Why This Core Exists

For ODM food manufacturing, orders often start before a product becomes a stable mass-production item. The ERP therefore needs a pre-order workspace that controls:

1. Customer product development requests.
2. Supplier material options provided through Purchasing.
3. Recipe and BOM versions.
4. Trial production, sample delivery, and customer selection status.
5. Unit cost simulation after supplier quote and contract assumptions are available.
6. Target margin and quotation basis.
7. Transfer to mass-production master data.

Without this workspace, Orders and Finance would not have a reliable source for quotation margin and BOM version assumptions.

## First-Version Tabs

| Tab | Purpose |
| --- | --- |
| 開發案 | Customer request, product concept, sample due date, stage, owner, and launch target |
| BOM 版本 | Development, trial, quotation, and mass-production BOM version control |
| 成本試算 | Material, packaging, labor, overhead, logistics, and loss-rate cost simulation |
| 報價基礎 | Target margin, suggested quote, minimum quote, quotation readiness, and transfer risk |

## Workflow Basis

```txt
customer request
-> product development project
-> supplier material sourcing
-> trial recipe / BOM version
-> sample and trial production
-> customer selection
-> supplier quote / supplier contract basis
-> cost simulation
-> quotation basis
-> sales quote / negotiation
-> customer contract
-> approved production BOM
-> item/BOM master data
-> Orders / Planning / Production / Finance
```

## Boundary With Other Workspaces

- Product R&D / Costing: owns development projects, trial recipe, sample status, customer selection, BOM version intent, trial costing, target margin, and quotation basis.
- Purchasing: owns supplier material search, sample material acquisition, supplier quote, and supplier contract basis.
- Items: owns item master data after product definition is approved.
- BOM: owns formal BOM master/version maintenance once a version is approved.
- Orders: consumes quotation-ready products, suggested quote, minimum quote, target margin, sales quote, customer negotiation, and customer contract status.
- Planning / APS: consumes approved mass-production BOM only.
- Production: consumes released BOM and process parameters.
- Quality: consumes inspection rules and release requirements created during development.
- Finance: compares quoted cost/margin against actual cost/margin after execution.

## First-Version Data Shape

R&D projects are shaped around:

- `customer`, `productName`, `targetChannel`
- `stage`, `decision`, `priority`, `owner`
- `targetLaunchDate`, `sampleDueDate`
- `bomNo`, `bomVersion`, `bomStatus`
- `targetPrice`, `suggestedQuote`, `minimumQuote`
- `targetMarginRate`, `estimatedMarginRate`
- `totalUnitCost`
- `materialCost`, `packagingCost`, `laborCost`, `overheadCost`, `logisticsCost`
- `lossRate`
- `quoteRiskReason`
- `transferReadiness`
- `costLines`
- `workflow`

Future data shape should also include:

- supplier material candidates
- supplier quote status
- supplier contract status
- sample submission status
- customer selection status
- sales quote status
- customer contract status

## API Needs

| Need | Candidate restserver Module |
| --- | --- |
| R&D project list/detail | R&D/project tables if available, otherwise product/item extension |
| BOM version and recipe | `bom`, item master tables |
| Material/packaging price | `purchase`, supplier price, item cost tables |
| Supplier material sourcing | `purchase`, supplier/company data, item master extension |
| Supplier quote/contract | `purchase`, supplier contract table if available |
| Labor and overhead rate | production cost/rate tables |
| Logistics estimate | logistics/freight cost tables |
| Quotation | `sale`, quotation table if available |
| Customer contract | `sale`, customer contract table if available |
| Transfer to master data | item/BOM master data APIs |

## Deferred

- Full recipe authoring editor.
- Nutrition/allergen compliance workflow.
- Sensory evaluation records.
- Customer sample approval portal.
- Full quotation approval.
- Supplier contract approval.
- Customer contract approval.
- Automatic transfer to item/BOM master data.
