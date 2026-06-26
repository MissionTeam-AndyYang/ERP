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
3. 保存事件發生當下的來源上下文。
4. 支援 `WarehouseTaskDetailPanel.timeline[]`。
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
| `quantity` | DECIMAL | NO | 事件關聯數量；僅保存正數。 |
| `direction` | INTEGER | NO | 數量方向；建議 1 表示增加或入庫方向，-1 表示減少或出庫方向，0 表示無數量方向或僅狀態事件。 |
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

`sourceRefs[]` 第一版只包含 `workflow_task_state.refCategory/ref_no/ref_sub_no` 對應的主任務來源，通常為一筆。

`workflow_task_event.refCategory/ref_no/ref_sub_no` 僅作為事件來源上下文，不彙總進第一版 `sourceRefs[]`，避免與 `workflow_task_state.taskId` 為 UK、且一個 taskId 對應一個主任務來源的設計混淆。

```txt
payload.sourceRefs[0] = workflow_task_state.refCategory + ref_no + ref_sub_no
```

若未來確認單一任務或單一事件需要同時關聯多張來源單據，建議另行設計 child table，例如：

```txt
workflow_task_event_ref
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
| `workflow_task_state` 是否已有 creation/update timestamp 可用於初始事件 | 影響 backfill 與 detail timeline 第一筆事件。 | 工程師回覆：`workflow_task_state` 已定義 `updateTime` 與 `creationTime`。理解與更新：此設計符合目前需求，`creationTime` 可作為任務建立或 backfill 初始事件時間；`updateTime` 可作為任務目前狀態最後更新時間與缺少 event 時的參考資訊。第一版不需新增額外時間欄位，但 timeline 正式顯示仍以 `workflow_task_event.eventTimestamp` 為準。 |
| 是否需保存 actorId/actorName | 影響後續審計與權限追蹤。 | 工程師回覆：保存 `actorId/actorName`。理解與更新：維持欄位，供後續人工操作、主管判斷、系統排程或 API mutation 追蹤使用；第一版 read-only 若無操作人資料可回傳空字串或 NULL。 |
| `quantity` 是否需要 direction 欄位 | 若後續要直接在事件表統計入出方向，可能需增加 direction；第一版建議由 `eventCode` 判斷。 | 工程師回覆：同意。理解與更新：已新增 `direction` 欄位，避免後續僅依 `eventCode` 判斷數量方向造成維護困難。 |
| 是否允許同一事件關聯多張來源單據 | 若需要，可能需拆成 event header + event_ref child table。 | 工程師提問：請說明單一事件同時關聯多張來源單據的情境。理解與更新：可能情境包含入庫事件同時關聯進貨單與庫存紀錄、出庫事件同時關聯訂單或出貨單與庫存紀錄、生產入庫同時關聯工單或領退餘廢產單與批號。但第一版為降低複雜度，`workflow_task_event` 僅保存一組主要事件來源上下文；若後續確認需要一事件多來源，再新增 `workflow_task_event_ref` child table。 |
| mutation API 導入前是否先只寫 system-generated events | 影響第一版 read-only 工作台是否能先有完整 timeline。 | 工程師提問：`workflow_task_event` 中存在什麼資料，工作台就直接顯示相對應資料，請確認是否合理。理解與更新：此邏輯合理，`workflow_task_event` 是 timeline 的 source of truth；read-only API 不應在查詢時寫入事件，避免查詢產生副作用。若要讓既有未完成任務具備 baseline timeline，可由一次性 backfill 或後台批次建立 system-generated events；若沒有 event，API 回傳空 `timeline[]`。 |

