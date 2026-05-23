# ERP Master Data / Settings Workspace Spec

日期：2026-05-23

## Status

Settings first-version workspace updated from the early system settings page into the master-data governance workspace.

- Page: `src/app/settings/page.tsx`
- Mock data: `src/mock/settings.ts`
- Types: `src/types/settings.ts`

## First-Version Goal

Help management answer:

1. Which master data domains are required for the ERP first version?
2. Which master data is incomplete or needs approval?
3. Which workflows are affected by incomplete item, BOM, warehouse, line, permission, or language data?
4. Which roles and permissions must be reviewed before enabling write actions?
5. Which localization terms still need dictionary coverage?

## First-Version Tabs

| Tab | Purpose |
| --- | --- |
| 主檔治理 | Item, BOM, customer, supplier, warehouse location, line, and core master-data completeness |
| 角色權限 | Role permissions, approval scope, and high-risk operation control |
| 系統串接 | Database, API, PDA, barcode, device, and external system integration basics |
| 語言/用詞 | Multilingual labels, workflow vocabulary, and shop-floor terminology |

## Boundary With Other Workspaces

- Items / BOM: own detailed item and recipe maintenance.
- Warehouse: consumes item, batch, location, and pallet master data.
- Planning / APS: consumes BOM, line, capacity, and substitution rules.
- Production: consumes line, process, and standard capacity data.
- Purchasing: consumes supplier, lead time, and purchase rule data.
- Quality: consumes inspection rules, release criteria, and document requirements.
- Settings: owns governance visibility, permission scope, integration readiness, and localization readiness.

## Deferred

- Full CRUD master-data editor.
- Approval engine.
- Audit trail viewer.
- Full multilingual dictionary editor.
- External integration configuration UI.

