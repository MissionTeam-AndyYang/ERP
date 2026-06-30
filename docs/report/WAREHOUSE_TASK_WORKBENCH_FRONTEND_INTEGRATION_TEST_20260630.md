# Warehouse Task Workbench Frontend Integration Test

Date: 2026-06-30
Scope: `WarehouseTaskWorkbenchScreen` and `WarehouseTaskDetailPanel`
Frontend route: `/warehouse/task-workbench`

## Implementation Summary

This frontend integration adds the first implementation of the warehouse task workbench and task detail panel.

Implemented API calls:

| API | Frontend usage |
| --- | --- |
| `GET /api/v2/warehouse/task-workbench` | Loads task workbench summary, lanes, filters, sorting, pagination-ready task list. |
| `GET /api/v2/warehouse/task-workbench/tasks/{taskId}` | Loads right-side task tracking detail panel for the selected task. |

Related frontend files:

| File | Purpose |
| --- | --- |
| `src/app/warehouse/task-workbench/page.tsx` | New workbench screen and task detail panel. |
| `src/services/warehouse-api.ts` | Task workbench API query builder, mapper, detail API mapper, mock fallback. |
| `src/types/warehouse.ts` | Task workbench and task detail TypeScript models. |
| `src/i18n/warehouse-enums.ts` | Multilingual enum/code label conversion helper. |
| `src/app/warehouse/page.tsx` | Adds entry link to the task workbench. |

## Enum And Multilingual Conversion

Frontend enum conversion now supports multilingual labels for warehouse task workbench code values. The helper keeps API payloads code-based and converts labels at UI render time using the active language from `LanguageProvider`.

Covered code groups:

| Code group | Examples |
| --- | --- |
| `taskType` | Receiving(3), Inbound(4), Outbound(5), Transfer(6), Quality(8), Shipment(9). |
| `taskStatus` | Pending(1), Partial(2), Done(3), Blocked(4), Cancelled(5). |
| `unit` | Other(0), gram(1), kilogram(2), centimeter(51), piece(101), pallet(201). |
| `department` | Sales(1), Purchasing(3), Quality(6), Warehouse(7), Logistics(8). |
| `riskType` | `OVERDUE`, `BLOCKED`, `INVENTORY_SHORTAGE`, `QUALITY_HOLD`, `BATCH_NOT_ASSIGNED`. |
| `laneCode` | `inbound`, `outbound`, `quality`, `shipment`, `blocked`. |
| `nextActionCode` | `warehouse.task.resolveBlocker`, `warehouse.task.arrangeInbound`, `warehouse.task.prepareShipment`. |
| `eventCode` | `workflow.task.created`, `workflow.task.assigned`, `workflow.task.blocked`, `workflow.task.completed`. |

Supported UI languages:

```txt
zh-TW, en, ja, vi
```

## Test Results

| Test | Result | Notes |
| --- | --- | --- |
| `npm.cmd run lint` | PASS | ESLint completed without errors. |
| `npm.cmd run build` | PASS | Next.js production build completed successfully. |
| Build route check | PASS | Build output includes `/warehouse/task-workbench`. |
| HTTP smoke: `/warehouse` | PASS | Returned HTTP 200, raw content length 62508. |
| HTTP smoke: `/warehouse/task-workbench` | PASS | Returned HTTP 200, raw content length 53048. |
| Browser visual smoke | BLOCKED | In-app browser/node kernel failed with Windows sandbox permission error: `EPERM: operation not permitted, lstat 'C:\Users\andyy\AppData\Local\OpenAI\Codex'`. |

## Manual Review Notes

Expected behavior after backend API is available:

1. Opening `/warehouse/task-workbench` calls `GET /api/v2/warehouse/task-workbench`.
2. Changing date range, task type, risk-only filter, sort, order, or keyword rebuilds the workbench query.
3. Selecting a task row calls `GET /api/v2/warehouse/task-workbench/tasks/{taskId}`.
4. If either API fails, the screen remains usable with mock fallback and displays a warning banner.
5. Enum/code values are converted in the UI layer according to the active language.

## Remaining Follow-Up

Browser visual verification should be retried in an environment where the Codex in-app Browser or Playwright kernel can access its local runtime directory. No route/build failure was observed during command-line verification.

