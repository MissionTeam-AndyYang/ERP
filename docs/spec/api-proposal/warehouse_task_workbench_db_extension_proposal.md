# Warehouse Task Workbench DB Extension Proposal

> Status: Proposal / Pending Engineer Review
> Related API Proposal: `docs/spec/api-proposal/warehouse_task_workbench_proposal.md`
> Related Flow / Algorithm: `docs/spec/api-proposal/warehouse_task_workbench_flow_algorithm.md`
> Purpose: 規劃跨模組 workflow task 所需的完整任務流程歷史資料來源，補足 `workflow_task_state` 只能呈現目前狀態的限制；Warehouse Task Workbench 第一版僅使用其中與倉庫任務相關的子集合。

## 工程師提問 

| 工程師提問 | 工程師回覆 | 文件更新 |
| --- | --- | --- |
| 請確認目前的資料表設計是否適用於所有任務類型，例如：請購(1)、採購(2)、進貨(3)、入庫(4)、出庫(5)、移倉(6)、生產(7)、品檢(8)、出貨(9)、其他(0)。建議評估是否能設計一個「一體適用」的資料表，以涵蓋上述各類任務，避免因任務類型差異而產生結構不一致或維護困難。 | 採用一體適用設計。`workflow_task_event` 不應設計成倉庫專用事件表，也不應依任務類型拆成多張表。任務類型、負責模組、來源類別與主來源單據由 `workflow_task_state` 保存；`workflow_task_event` 只以 `taskId` 對應任務主檔，保存該任務的事件歷史。各任務類型的差異以 nullable context 欄位承接，例如倉庫任務可使用 `warehouse_no/item_no/batchNumber/quantity/unit`，請購或採購任務可只使用 `refCategory/ref_no/ref_sub_no` 與狀態/部門欄位；數量方向不另設欄位，改由 `eventCode` 判斷。 | 已將文件定位更新為跨模組 workflow event table；新增「一體適用設計原則」與「任務類型適用性」；將 eventCode 建議由 `warehouse.task.*` 調整為 `workflow.task.*`，避免事件表被誤解為 Warehouse-only。 |

## 一體適用設計原則

`workflow_task_event` 採用「一張事件表支援所有 workflow 任務類型」的設計：

1. `workflow_task_state` 是任務目前狀態與主任務來源的主檔；一筆 `taskId` 對應一個主任務來源。
2. `workflow_task_event` 是任務歷史事件表；一筆 `taskId` 可對應多筆事件。
3. 不依任務類型建立不同 event table，避免後續查詢 timeline、審計歷史與前端顯示規則分裂。
4. 共通欄位保存所有任務都會用到的事件資訊，例如狀態、部門、處理人、時間、原因與備註。
5. 任務類型差異以可為空的 context 欄位保存；不適用的欄位保持 NULL 或空值，不用額外建立類型專用欄位。
6. 若未來某些任務需要高度結構化的專屬明細，可另外設計該模組的 detail table，但 timeline 仍由 `workflow_task_event` 統一呈現。

## Scope

本文件為資料表擴充提案，不代表目前資料庫已存在此表，也不代表第一版 read-only API 必須立即完成 mutation 行為。

`workflow_task_event` 的目的：

1. 保存任務狀態變化歷史。
2. 保存責任部門與處理人移轉紀錄。
3. 保存事件發生當下的來源上下文。
4. 支援 `WarehouseTaskDetailPanel.timeline[]`，並可延伸支援其他模組的 task timeline。
5. 為後續完成任務、解除阻塞、放行、指派等 mutation API 留下可追溯基礎。

## 任務類型適用性

| taskType | 任務類型 | 適用方式 |
| --- | --- | --- |
| 1 | 請購 | 使用 `taskId/eventCode/eventTimestamp/fromStatus/toStatus/fromDepartment/toDepartment/actorId/actorName/refCategory/ref_no/ref_sub_no/reasonCode/comment`；料品或數量欄位可視請購明細是否已進入任務狀態而填入。 |
| 2 | 採購 | 使用共通欄位與採購來源單號；若事件與採購料品、數量有關，可填入 `item_no/quantity/unit`，數量方向由 `eventCode` 判斷。 |
| 3 | 進貨 | 使用共通欄位、進貨來源單號與料品/數量 context；如已產生批號可填入 `batchNumber`。 |
| 4 | 入庫 | 使用共通欄位，並可填入 `warehouse_no/item_no/batchNumber/quantity/unit`，數量方向由 `eventCode` 判斷。 |
| 5 | 出庫 | 使用共通欄位，並可填入 `warehouse_no/item_no/batchNumber/quantity/unit`，數量方向由 `eventCode` 判斷。 |
| 6 | 移倉 | 使用共通欄位；若未來需同時記錄來源倉與目的倉，第一版以 `comment` 或來源單據追溯，後續可再評估新增 `fromWarehouse_no/toWarehouse_no`。 |
| 7 | 生產 | 使用共通欄位、工單或領退餘廢產單來源；若涉及產出或領料，可填入料品、批號、數量與單位，方向由 `eventCode` 判斷。 |
| 8 | 品檢 | 使用共通欄位、品檢來源單號與料品/批號 context；若涉及品檢保留或釋放數量，方向由 `eventCode` 判斷。 |
| 9 | 出貨 | 使用共通欄位、銷貨或出貨來源單號；若涉及庫存出貨，可填入倉儲、料品、批號、數量與單位，方向由 `eventCode` 判斷。 |
| 0 | 其他 | 使用共通欄位與來源單據欄位；無法結構化的補充資訊放在 `reasonCode` 或 `comment`。 |

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
| `quantity` | DECIMAL | NO | 事件關聯數量；僅保存正數。數量方向不另存欄位，需由 `eventCode` 判斷。 |
| `unit` | INTEGER | NO | 數量單位，沿用 Unit enum。 |
| `reasonCode` | VARCHAR | NO | 阻塞、退回、取消或調整原因代碼。 |
| `comment` | TEXT | NO | 人工備註或系統訊息；第一版可為空字串。 |
| `creationTime` | BIGINT | YES | 建立時間，UTC timestamp；命名與既有資料庫慣例一致。 |
| `updateTime` | BIGINT | YES | 更新時間，UTC timestamp；命名與既有資料庫慣例一致。 |

不建議在 `workflow_task_event` 重複保存 `module` 或 `taskType`，避免與 `workflow_task_state` 產生同步不一致。查詢時以 `taskId` join `workflow_task_state` 取得任務類型、模組、主任務來源與目前狀態。

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
| `workflow.task.created` | 任務建立。 |
| `workflow.task.assigned` | 任務指派或責任部門移轉。 |
| `workflow.task.started` | 任務開始處理。 |
| `workflow.task.partiallyProcessed` | 任務部分處理。 |
| `workflow.task.blocked` | 任務進入阻塞。 |
| `workflow.task.blockResolved` | 阻塞解除。 |
| `workflow.task.completed` | 任務完成。 |
| `workflow.task.cancelled` | 任務取消。 |
| `workflow.task.refLinked` | 任務關聯來源單據。 |
| `workflow.task.quantityAdjusted` | 任務數量調整。 |

若前端需要顯示倉庫、採購、生產或品檢專屬文字，應依 `workflow_task_state.module/taskType` 搭配 `eventCode` 轉換多國語系文字，不應在事件表使用模組專屬 eventCode 作為資料表結構差異。

若事件涉及數量，數量方向亦由 `eventCode` 判斷，不在 `workflow_task_event` 另存 `direction` 欄位。例如入庫、進貨完成、品檢釋放、生產產出等事件可視為增加方向；出庫、出貨、領料、採購退回等事件可視為減少方向；僅狀態流轉或指派事件則視為無數量方向。

## API Mapping

### `payload.timeline[]`

| API Field | Source |
| --- | --- |
| `eventCode` | `workflow_task_event.eventCode` |
| `eventTimestamp` | `workflow_task_event.eventTimestamp` |
| `department` | 優先 `toDepartment`，無值時使用 `fromDepartment` |
| `status` | 優先 `toStatus`，無值時使用 `fromStatus` |
| `comment` | `workflow_task_event.comment` |

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
| 新增 workflow task | `workflow.task.created` |
| 指派或改變下一步部門 | `workflow.task.assigned` |
| 任務開始處理 | `workflow.task.started` |
| 部分處理，例如部分採購、部分入庫、部分出庫、部分移倉或部分生產 | `workflow.task.partiallyProcessed` |
| 庫存不足、品檢保留、來源單據缺漏、主管判定阻塞或其他流程阻塞 | `workflow.task.blocked` |
| 阻塞原因解除 | `workflow.task.blockResolved` |
| 任務完成 | `workflow.task.completed` |
| 任務取消 | `workflow.task.cancelled` |
| 任務產生或關聯新來源單據 | `workflow.task.refLinked` |

## Backfill Strategy

若既有資料沒有歷史事件，導入初期可對每筆未完成任務建立一筆系統事件：

```txt
eventCode = workflow.task.created
eventTimestamp = workflow_task_state.creationTime or workflow_task_state.updateTime or dueTimestamp
fromStatus = null
toStatus = workflow_task_state.taskStatus
fromDepartment = null
toDepartment = workflow_task_state.ownerDepartment
comment = ""
```

若上述時間欄位不存在，需由工程師確認可用欄位，不應由 API 任意推測。

## Review Questions

| Question | Reason | 工程師回覆 |
| --- | --- | --- |
| `workflow_task_state` 是否已有 creation/update timestamp 可用於初始事件 | 影響 backfill 與 detail timeline 第一筆事件。 | 工程師回覆：`workflow_task_state` 已定義 `updateTime` 與 `creationTime`。理解與更新：此設計符合目前需求，`creationTime` 可作為任務建立或 backfill 初始事件時間；`updateTime` 可作為任務目前狀態最後更新時間與缺少 event 時的參考資訊。第一版不需新增額外時間欄位，但 timeline 正式顯示仍以 `workflow_task_event.eventTimestamp` 為準。 |
| 是否需保存 actorId/actorName | 影響後續審計與權限追蹤。 | 工程師回覆：保存 `actorId/actorName`。理解與更新：維持欄位，供後續人工操作、主管判斷、系統排程或 API mutation 追蹤使用；第一版 read-only 若無操作人資料可回傳空字串或 NULL。 |
| `quantity` 是否需要 direction 欄位 | 若後續要直接在事件表統計入出方向，可能需增加 direction；第一版建議由 `eventCode` 判斷。 | 最新確認：移除 `direction` 欄位，改由 `eventCode` 判斷數量方向。理解與更新：`workflow_task_event.quantity` 僅保存正數，入庫/出庫/領料/產出/保留/釋放等方向語意由事件代碼決定，避免資料表同時保存 `eventCode` 與 `direction` 造成兩者不一致。 |
| 是否允許同一事件關聯多張來源單據 | 若需要，可能需拆成 event header + event_ref child table。 | 工程師提問：請說明單一事件同時關聯多張來源單據的情境。理解與更新：可能情境包含入庫事件同時關聯進貨單與庫存紀錄、出庫事件同時關聯訂單或出貨單與庫存紀錄、生產入庫同時關聯工單或領退餘廢產單與批號。但第一版為降低複雜度，`workflow_task_event` 僅保存一組主要事件來源上下文；若後續確認需要一事件多來源，再新增 `workflow_task_event_ref` child table。 |
| mutation API 導入前是否先只寫 system-generated events | 影響第一版 read-only 工作台是否能先有完整 timeline。 | 工程師提問：`workflow_task_event` 中存在什麼資料，工作台就直接顯示相對應資料，請確認是否合理。理解與更新：此邏輯合理，`workflow_task_event` 是 timeline 的 source of truth；read-only API 不應在查詢時寫入事件，避免查詢產生副作用。若要讓既有未完成任務具備 baseline timeline，可由一次性 backfill 或後台批次建立 system-generated events；若沒有 event，API 回傳空 `timeline[]`。 |

