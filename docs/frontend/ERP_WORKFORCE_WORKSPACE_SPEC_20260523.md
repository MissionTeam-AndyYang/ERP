# ERP Workforce Workspace Spec

日期：2026-05-23

## Status

Workforce first-version workspace updated from the early module page into the management workspace pattern.

- Page: `src/app/workforce/page.tsx`
- Mock data: `src/mock/workforce.ts`
- Types: `src/types/workforce.ts`

## First-Version Goal

Help management answer:

1. Are enough people assigned for today's production, warehouse, quality, and logistics work?
2. Do assigned people have the required skills for planned work orders and dispatches?
3. Where are overtime, cross-line support, or shift gaps required?
4. Are certifications or required trainings close to expiry?
5. Which workforce risks affect Planning / APS or Production execution?

## First-Version Tabs

| Tab | Purpose |
| --- | --- |
| 班表覆蓋 | Staff requirement vs assigned staff by line, area, and shift |
| 技能缺口 | Required skills vs available skills for production, quality, warehouse, and logistics |
| 加班/支援 | Overtime, support staff, cross-line movement, and night shift gaps |
| 證照/複訓 | Certification, license, training, and renewal risk |

## Workflow Basis

```txt
planning / production schedule
-> required staff and skills
-> shift coverage check
-> cross-line support or overtime
-> execution readiness
```

## Boundary With Other Workspaces

- Planning / APS: provides required capacity and staff assumptions.
- Production: consumes final staffing readiness for work-order execution.
- Quality: requires inspector availability and qualified inspection skills.
- Warehouse: requires picking, outbound, and cold-storage handling staff.
- Logistics: requires drivers and cold-chain certification coverage.
- Workforce: owns shift coverage, skill gaps, support needs, overtime, and certification risk.

## API Needs

| Need | Candidate restserver Module |
| --- | --- |
| Employee and role data | employee/workforce tables |
| Shift and attendance | attendance, shift tables |
| Skill and certification | employee skill/license/training tables |
| Production staffing needs | `aps`, `workorder`, `processorder` |
| Logistics driver needs | logistics/vehicle/driver tables |

## Deferred

- Payroll.
- Full HR personnel records.
- Leave approval.
- Detailed labor law calculations.
- Automatic shift optimization.

