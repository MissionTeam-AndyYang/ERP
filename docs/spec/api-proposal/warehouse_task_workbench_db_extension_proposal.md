# Warehouse Task Workbench DB Extension Proposal

> Status: Proposal / Pending Engineer Review
> Related API Proposal: `docs/spec/api-proposal/warehouse_task_workbench_proposal.md`
> Related Flow / Algorithm: `docs/spec/api-proposal/warehouse_task_workbench_flow_algorithm.md`
> Purpose: 規劃 `WarehouseTaskDetailPanel` 所需的完整任務流程歷史資料來源，補足 `workflow_task_state` 只能呈現目前狀態的限制。

## Scope

本文件為資料表擴充提案，不代表目前資料庫已存在此表，也不代表第一版 read-only API 必須立即完成 mutation 行為。

`workflow_task_event` 的目的：

1. 保存任務狀態變化歷史。
2. 保存責任部門與處理人移轉紀錄。
3. 保存任務關聯來源單據集合。
4. 支援 `WarehouseTaskDetailPanel.timeline[]` 與 `WarehouseTaskDetailPanel.sourceRefs[]`。
5. 為後續完成任務、解除阻塞、放行、指派等 mutation API 留下可追溯基礎。

## Proposed Table

### `workflow_task_event`

| Column | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | BIGINT | YES | 自動遞增流水號。 |
| `taskId` | VARCHAR | YES | 對應 `workflow_task_state.taskId`。 |
| `eventCode` | VARCHAR | YES | 任務事件代碼，前端依 code 轉換顯示文字。 |
| `eventTimestamp` | BIGINT | YES | 事件發生時間，UTC timestamp。 |
| `fromStatus` | INTEGER | NO | 事件前任務狀態。 |
| `toStatus` | INTEGER | NO | 事件後任務狀態。 |
| `fromDepartment` | INTEGER | NO | 事件前負責部門。 |
| `toDepartment` | INTEGER | NO | 事件後負責部門。 |
| `actorId` | VARCHAR | NO | 操作人或系統程序識別碼；第一版可為空字串。 |
| `actorName` | VARCHAR | NO | 操作人顯示名稱；第一版可為空字串。 |
| `refCategory` | INTEGER | NO | 事件關聯來源類別。 |
| `ref_no` | VARCHAR | NO | 事件關聯來源單號；命名與 `workflow_task_state.ref_no` 一致。 |
| `ref_sub_no` | VARCHAR | NO | 事件關聯來源明細編號；命名與 `workflow_task_state.ref_sub_no` 一致。 |
| `warehouse_no` | VARCHAR | NO | 事件關聯倉儲別名 no；命名與 `workflow_task_state.warehouse_no` 一致。 |
| `item_no` | VARCHAR | NO | 事件關聯料號；命名與 `workflow_task_state.item_no` 一致。 |
| `batchNumber` | VARCHAR | NO | 事件關聯批號；命名與 `workflow_task_state.batchNumber` 一致。 |
| `quantity` | DECIMAL | NO | 事件關聯數量；僅保存正數，方向由 `eventCode` 判斷。 |
| `unit` | INTEGER | NO | 數量單位，沿用 Unit enum。 |
| `reasonCode` | VARCHAR | NO | 阻塞、退回、取消或調整原因代碼。 |
| `note` | TEXT | NO | 人工備註或系統訊息；第一版可為空字串。 |
| `createdAt` | BIGINT | YES | 建立時間，UTC timestamp。 |
| `updatedAt` | BIGINT | YES | 更新時間，UTC timestamp。 |

## Suggested Indexes

| Index | Columns | Purpose |
| --- | --- | --- |
| `idx_workflow_task_event_task_time` | `taskId`, `eventTimestamp`, `id` | 支援單一任務 timeline 查詢。 |
| `idx_workflow_task_event_ref` | `refCategory`, `ref_no`, `ref_sub_no` | 支援由來源單據反查任務事件。 |
| `idx_workflow_task_event_lot` | `warehouse_no`, `item_no`, `batchNumber` | 支援由批號追溯相關任務事件。 |

## Event Codes

第一版建議先定義穩定 code，不在 API 回傳翻譯文字。

| eventCode | Description |
| --- | --- |
| `warehouse.task.created` | 任務建立。 |
| `warehouse.task.assigned` | 任務指派或責任部門移轉。 |
| `warehouse.task.started` | 任務開始處理。 |
| `warehouse.task.partiallyProcessed` | 任務部分處理。 |
| `warehouse.task.blocked` | 任務進入阻塞。 |
| `warehouse.task.blockResolved` | 阻塞解除。 |
| `warehouse.task.completed` | 任務完成。 |
| `warehouse.task.cancelled` | 任務取消。 |
| `warehouse.task.refLinked` | 任務關聯來源單據。 |
| `warehouse.task.quantityAdjusted` | 任務數量調整。 |

## API Mapping

### `payload.timeline[]`

| API Field | Source |
| --- | --- |
| `eventCode` | `workflow_task_event.eventCode` |
| `eventTimestamp` | `workflow_task_event.eventTimestamp` |
| `department` | 優先 `toDepartment`，無值時使用 `fromDepartment` |
| `status` | 優先 `toStatus`，無值時使用 `fromStatus` |
| `note` | `workflow_task_event.note` |

### `payload.sourceRefs[]`

`sourceRefs[]` 第一版至少應包含 `workflow_task_state.refCategory/ref_no/ref_sub_no` 對應的主任務來源。

若導入 `workflow_task_event`，可額外彙總事件中的 `refCategory/ref_no/ref_sub_no`，並去重後回傳為 API 欄位 `refCategory/refNo/refSubNo`：

```txt
distinct by refCategory + ref_no + ref_sub_no
```

## Write Timing Proposal

| Trigger | Suggested Event |
| --- | --- |
| 新增 workflow task | `warehouse.task.created` |
| 指派或改變下一步部門 | `warehouse.task.assigned` |
| 任務開始處理 | `warehouse.task.started` |
| 部分入庫、部分出庫或部分移倉 | `warehouse.task.partiallyProcessed` |
| 庫存不足、品檢保留、來源單據缺漏 | `warehouse.task.blocked` |
| 阻塞原因解除 | `warehouse.task.blockResolved` |
| 任務完成 | `warehouse.task.completed` |
| 任務取消 | `warehouse.task.cancelled` |
| 任務產生或關聯新來源單據 | `warehouse.task.refLinked` |

## Backfill Strategy

若既有資料沒有歷史事件，導入初期可對每筆未完成任務建立一筆系統事件：

```txt
eventCode = warehouse.task.created
eventTimestamp = workflow_task_state.creationTime or workflow_task_state.updateTime or dueTimestamp
fromStatus = null
toStatus = workflow_task_state.taskStatus
fromDepartment = null
toDepartment = workflow_task_state.ownerDepartment
note = ""
```

若上述時間欄位不存在，需由工程師確認可用欄位，不應由 API 任意推測。

## Review Questions

| Question | Reason | 工程師回覆 |
| --- | --- | --- |
| `workflow_task_state` 是否已有 creation/update timestamp 可用於初始事件 | 影響 backfill 與 detail timeline 第一筆事件。 | 在資料庫文件 docs\spec\database\index.md 中，資料表 workflow_task_state 已定義欄位 updateTime 與 creationTime。 請確認這兩個欄位的設計是否符合你的需求，並說明其在任務狀態管理或工作台顯示邏輯上的作用。若有不足或需要額外補充的欄位，請提出建議，以便後續調整與更新。|
| 是否需保存 actorId/actorName | 影響後續審計與權限追蹤。 | 保存 actorId/actorName |
| `quantity` 是否需要 direction 欄位 | 若後續要直接在事件表統計入出方向，可能需增加 direction；第一版建議由 `eventCode` 判斷。 | 同意 |
| 是否允許同一事件關聯多張來源單據 | 若需要，可能需拆成 event header + event_ref child table。 | 請說明在什麼樣的情況下，單一事件會同時關聯到多張來源單據。|
| mutation API 導入前是否先只寫 system-generated events | 影響第一版 read-only 工作台是否能先有完整 timeline。 | 目前尚不清楚此設計可能帶來的影響。 依我的認知，`workflow_task_event` 中存在什麼資料，工作台就會直接顯示相對應的資料。請協助說明此邏輯是否合理，並指出可能的影響或需要注意的地方，以便後續設計與實作能更完善。 |

