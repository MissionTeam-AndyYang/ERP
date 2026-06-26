# Warehouse Center V1 Screen Coverage And Next API Readiness

> Status: Working Note / Ready for Discussion
> Related naming file: `docs/spec/api-proposal/planned_screen_list_naming.md`
> Next API proposal: `docs/spec/api-proposal/warehouse_task_workbench_proposal.md`
> Backend flow: `docs/spec/api-proposal/warehouse_task_workbench_flow_algorithm.md`
> Frontend static preview: `docs/spec/api-proposal/warehouse_task_workbench_static_preview.html`

## Purpose

本文件用於確認第一版「倉庫中心」畫面清單是否完整，並集中列出下一步實作 `WarehouseTaskWorkbenchScreen` 與 `WarehouseTaskDetailPanel` 所需的 API、後端流程與前端靜態預覽文件。

## Coverage Conclusion

`planned_screen_list_naming.md` 目前已涵蓋第一版「倉庫中心」所需實作的全部畫面。

第一版範圍包含：

| Code | Type | 正式畫面名稱 | Status | 備註 |
| --- | --- | --- | --- | --- |
| `WarehouseOverviewScreen` | Screen | 倉庫中心總覽 | 已有第一版 | 倉庫中心入口與管理摘要。 |
| `WarehouseValueSpaceView` | View | 價值與倉位視圖 | 已有第一版 | 屬於總覽頁內部頁籤，不是獨立 route。 |
| `WarehouseRiskAlertView` | View | 風險警示視圖 | 已有第一版 | 屬於總覽頁內部頁籤，不是獨立 route。 |
| `WarehousePendingTaskView` | View | 待處理入出庫視圖 | 已有第一版 | 屬於總覽頁摘要入口，不等同於任務工作台。 |
| `WarehouseInventorySummaryView` | View | 庫存明細摘要視圖 | 已有第一版 | 屬於總覽頁摘要入口，完整功能由批號清單承接。 |
| `WarehouseCurrentLotPanel` | Panel | 目前批號資訊面板 | 已有第一版 | 屬於總覽頁右側摘要 panel。 |
| `WarehouseTaskWorkbenchScreen` | Screen | 倉庫任務工作台 | 待實作 | 下一步主要實作畫面。 |
| `WarehouseTaskDetailPanel` | Panel | 倉庫任務追蹤面板 | 待實作 | 下一步主要實作 panel。 |
| `WarehouseInventoryLotListScreen` | Screen | 庫存批號明細清單 | 已有第一版 | 已串接 inventory lots API。 |
| `WarehouseInventoryLotDetailPanel` | Panel | 庫存批號追蹤面板 | 已有第一版 | 已串接 inventory lot detail API。 |

因此，在 `WarehouseTaskWorkbenchScreen` 與 `WarehouseTaskDetailPanel` 完成後，第一版「倉庫中心」的畫面骨架即可視為完整。後續工作會進入 runtime review、資料欄位細緻化、跨模組 drill-down 與 mutation API 設計，而不是新增第一版必備畫面。

## Next Implementation Target

下一步實作目標為：

1. `WarehouseTaskWorkbenchScreen`
   - Route 建議：`/warehouse/task-workbench`
   - API：`GET /api/v2/warehouse/task-workbench`
   - 功能：任務摘要、kanban/list、日期範圍、風險篩選、任務類型篩選、排序、分頁、點選任務 drill-down。

2. `WarehouseTaskDetailPanel`
   - UI location：`WarehouseTaskWorkbenchScreen` 右側 panel；窄版可改為 drawer。
   - API：`GET /api/v2/warehouse/task-workbench/tasks/{taskId}`
   - 功能：單一任務來源、相關批號、庫存可用性、阻塞原因、下一步負責部門與任務時間線。

## Required Documents

| 文件 | 狀態 | 用途 |
| --- | --- | --- |
| `warehouse_task_workbench_proposal.md` | 已建立，待工程師確認 | API contract、request/response、欄位語意與 review questions。 |
| `warehouse_task_workbench_flow_algorithm.md` | 已建立，待工程師確認 | 後端查詢流程、資料來源、風險計算、lane 分類與限制。 |
| `warehouse_task_workbench_static_preview.html` | 已建立，可供討論 | 前端靜態畫面，用於確認工作台資訊層級、篩選與 detail panel 需求。 |
| `planned_screen_list_naming.md` | 已建立，持續維護 | 第一版畫面清單與命名基準。 |

## API Design Summary

| Endpoint | Method | 對應畫面 | 第一版定位 |
| --- | --- | --- | --- |
| `/api/v2/warehouse/task-workbench` | GET | `WarehouseTaskWorkbenchScreen` | Read-only list/kanban API。 |
| `/api/v2/warehouse/task-workbench/tasks/{taskId}` | GET | `WarehouseTaskDetailPanel` | Read-only task tracking detail API。 |

第一版不包含完成任務、指派任務、解除阻塞、放行出庫或修改品檢狀態等 mutation API。這些行為需等工程師確認權限、資料表與部門責任流程後再另行設計。

## Backend Flow Summary

後端流程第一版應以 `workflow_task_state` 為主資料來源，補充：

| 資料 | 建議來源 |
| --- | --- |
| 任務主資料 | `workflow_task_state` |
| 倉庫名稱 | `ship_wh_alias` |
| 庫存可用性 | `CWarehouseInventorySnapshotCalculator` |
| 預留數量 | `warehouse_inventory_reservation` |
| 品檢保留量 | `warehouse_quality_hold` |
| 批號效期 | `batch_number` |

風險判斷包含逾期、阻塞、庫存不足、品檢保留與未指定批號。第一版 timeline 若尚無任務歷史表，僅呈現目前狀態事件，不推測不存在的歷史紀錄。

## Frontend Static Preview Scope

靜態預覽應用於確認以下 UX：

1. 管理者一眼看見今日、逾期、阻塞與庫存不足任務。
2. 任務可用 kanban 或 list 方式掃描。
3. 篩選不造成畫面過重，優先支援日期範圍、任務類型、風險與關鍵字。
4. 點選任務後，右側 panel 呈現來源單據、相關批號、數量、負責部門、阻塞原因與時間線。

## Engineer Review Items

| 項目 | 影響 |
| --- | --- |
| 查無 `taskId` 時回傳 404 或成功空 payload | 影響前端 detail panel 錯誤狀態。 |
| 任務未指定批號時是否可彙總同倉同料品候選批號 | 影響出庫、移倉、出貨任務的可用庫存判斷。 |
| `blocked` lane 是否優先於任務類型 lane | 影響 kanban 分類與管理者處理順序。 |
| 第一版是否只允許 read-only | 影響是否需要同步設計 mutation API。 |
| 是否需要新增任務歷史表 | 影響 `WarehouseTaskDetailPanel` timeline 完整度。 |

