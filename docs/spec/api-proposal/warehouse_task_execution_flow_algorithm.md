# Warehouse Task Execution API 流程與演算法提案

狀態：Proposal / Pending Engineer Review
對應 API 提案：`docs/spec/api-proposal/warehouse_task_execution_proposal.md`
對應靜態預覽：`docs/spec/api-proposal/warehouse_task_execution_static_preview.html`
上游 API：`docs/spec/api-proposal/warehouse_task_workbench_proposal.md`

## 文件定位

本文件描述 `WarehouseTaskExecutionScreen` 的後端流程與演算法。此畫面承接已確認或實作中的 Task Workbench read-only API，進一步支援任務執行前確認與 validation。第一版建議先實作：

```txt
GET /api/v2/warehouse/task-execution/tasks/{taskId}
POST /api/v2/warehouse/task-execution/tasks/{taskId}/actions/validate
```

以下 API 會寫入資料，需工程師確認後再實作：

```txt
POST /api/v2/warehouse/task-execution/tasks/{taskId}/actions/commit
```

## 共用規則

1. timestamp 以 UTC timestamp 儲存與回傳。
2. enum 僅回傳 code，前端負責多國語言轉換。
3. validation API 不得寫入任何資料表。
4. commit API 必須使用 transaction；任一寫入失敗需 rollback。
5. 數量欄位取至小數點第 2 位；金額欄位四捨五入取整數。
6. `workflow_task_event` 是 timeline 的 source of truth；查詢 API 不得為了補 timeline 而寫入事件。

## Action Code 建議

| taskType | actionCode | 用途 |
| --- | --- | --- |
| 3 進貨 | `warehouse.task.confirmReceipt` | 確認進貨任務已可進入入庫或品檢流程 |
| 4 入庫 | `warehouse.task.arrangeInbound` | 執行或確認入庫與板位安排 |
| 5 出庫 | `warehouse.task.prepareOutbound` | 執行出庫備貨、扣庫或預備出庫 |
| 6 移倉 | `warehouse.task.arrangeTransfer` | 執行倉位或倉儲間移轉 |
| 8 品檢 | `warehouse.task.waitQualityDecision` | 登錄品檢放行、保留或拒收判定 |
| 9 出貨 | `warehouse.task.prepareShipment` | 執行出貨前備貨與批號確認 |

若 `workflow_task_state.taskStatus = BLOCKED`，actionCode 應轉為：

```txt
warehouse.task.resolveBlocker
```

## GET /api/v2/warehouse/task-execution/tasks/{taskId} 流程

### Step 1：讀取任務主資料

```txt
workflow_task_state.taskId = path.taskId
```

若查無任務：

```txt
payload.task = {}
payload.execution.allowed = false
payload.execution.blockedReasons = ["TASK_NOT_FOUND"]
payload.candidateLots = []
payload.timeline = []
```

### Step 2：判斷任務是否可進入執行畫面

不可執行情境：

| 條件 | blockedReasons |
| --- | --- |
| `taskStatus = DONE` | `TASK_DONE` |
| `taskStatus = CANCELLED` | `TASK_CANCELLED` |
| `taskStatus = BLOCKED` | `TASK_BLOCKED` |
| taskType 不在 3、4、5、6、8、9 | `TASK_TYPE_NOT_SUPPORTED` |

注意：BLOCKED 任務仍可開啟畫面檢視，但 `allowed=false`，除非後續另行設計解除阻塞 mutation。

### Step 3：建立庫存與批號 context

沿用 Warehouse 已確認庫存快照規則：

```txt
inventory_item_month_statistic + inventory_delta
fallback: inventory_record
reservation: warehouse_inventory_reservation
quality hold: warehouse_quality_hold
```

比對鍵：

```txt
warehouse_no + item_no + batchNumber
```

若任務未指定 batchNumber：

```txt
candidateLots = same warehouse_no + item_no lots where currentQuantity > 0
```

若任務已指定 batchNumber：

```txt
candidateLots = exact warehouse_no + item_no + batchNumber lot
```

### Step 4：計算 quantityLimits

```txt
remainingQuantity = max(expectedQuantity - processedQuantity, 0)
availableQuantity = candidate lot availableQuantity or item+warehouse aggregated availableQuantity
reservedQuantity = candidate lot reservedQuantity or aggregated reservedQuantity
qualityHoldQuantity = candidate lot qualityHoldQuantity or aggregated qualityHoldQuantity
```

依任務類型計算：

| taskType | maxExecutableQuantity |
| --- | --- |
| 3 進貨 | `remainingQuantity` |
| 4 入庫 | `remainingQuantity` |
| 5 出庫 | `min(remainingQuantity, availableQuantity)` |
| 6 移倉 | `min(remainingQuantity, availableQuantity)` |
| 8 品檢 | `remainingQuantity` |
| 9 出貨 | `min(remainingQuantity, availableQuantity)` |

### Step 5：建立 candidateLots

每一筆 lot 判斷：

| 條件 | disabledReasons |
| --- | --- |
| `currentQuantity <= 0` | 不回傳 |
| 出庫/移倉/出貨且 `availableQuantity <= 0` | `NO_AVAILABLE_QUANTITY` |
| 出庫/移倉/出貨且 `qualityHoldQuantity > 0` | `QUALITY_HOLD` |
| 批號已過效期 | `EXPIRED_LOT` |

`selectable = disabledReasons is empty`

### Step 6：建立 execution context

```txt
actionCode = match(taskType, taskStatus)
allowed = task is open and maxExecutableQuantity > 0 and no blocking reason
defaultQuantity = min(remainingQuantity, maxExecutableQuantity)
requiresBatch = taskType in (5, 6, 9)
requiresPalletPlan = taskType in (4, 5, 6, 9)
requiresQualityDecision = taskType = 8
```

### Step 7：讀取 sourceRefs 與 timeline

`sourceRefs[]`：

```txt
workflow_task_state.refCategory/ref_no/ref_sub_no
```

`timeline[]`：

```txt
workflow_task_event where taskId = path.taskId order by eventTimestamp asc, id asc
```

## POST /actions/validate 流程

### Step 1：重新讀取 context

不得信任前端帶回的 context。後端必須重新查詢：

```txt
workflow_task_state
inventory snapshot
reservation
quality hold
candidate lots
```

### Step 2：驗證 actionCode

| 條件 | validationErrors |
| --- | --- |
| actionCode 空值 | `ACTION_REQUIRED` |
| actionCode 與 taskType 不相容 | `ACTION_NOT_ALLOWED` |
| taskStatus 為 DONE/CANCELLED | `TASK_CLOSED` |
| taskStatus 為 BLOCKED 且 actionCode 不是 resolve blocker | `TASK_BLOCKED` |

### Step 3：驗證 quantity

| 條件 | validationErrors |
| --- | --- |
| quantity <= 0 | `QUANTITY_MUST_BE_POSITIVE` |
| quantity > remainingQuantity | `QUANTITY_EXCEEDS_REMAINING` |
| 出庫/移倉/出貨且 quantity > availableQuantity | `QUANTITY_EXCEEDS_AVAILABLE` |

### Step 4：驗證 batchNo

| 條件 | validationErrors |
| --- | --- |
| 需指定批號但 batchNo 為空 | `BATCH_REQUIRED` |
| batchNo 不在 candidateLots | `BATCH_NOT_FOUND` |
| candidate lot 不可選 | lot.disabledReasons 對應 reason code |

### Step 5：驗證 warehouseNo / targetWarehouseNo

| taskType | 規則 |
| --- | --- |
| 入庫 | warehouseNo 必須存在，通常等於 task.warehouse_no |
| 出庫 | warehouseNo 必須存在，通常等於 task.warehouse_no |
| 移倉 | warehouseNo 與 targetWarehouseNo 都必填，且不可相同 |
| 出貨 | warehouseNo 必填 |

### Step 6：驗證 qualityDecision

若 taskType = 8：

```txt
qualityDecision in ("release", "hold", "reject")
```

否則忽略或回傳 warning：

```txt
QUALITY_DECISION_IGNORED
```

### Step 7：建立 preview

```txt
processedQuantityAfter = processedQuantity + quantity
remainingQuantityAfter = max(expectedQuantity - processedQuantityAfter, 0)
taskStatusAfter = DONE if remainingQuantityAfter = 0 else PARTIAL
eventCode = event code by actionCode
```

inventoryEffect：

| actionCode | category | 說明 |
| --- | --- | --- |
| `warehouse.task.arrangeInbound` | 入庫方向 | 寫入規則待 commit review |
| `warehouse.task.prepareOutbound` | 出庫方向 | 寫入規則待 commit review |
| `warehouse.task.arrangeTransfer` | 移倉方向 | 可能同時包含來源與目的倉異動 |
| `warehouse.task.prepareShipment` | 出庫方向 | 寫入規則待 commit review |
| `warehouse.task.waitQualityDecision` | 無或依判定 | release/hold/reject 規則待 Quality review |

## POST /actions/commit 流程提案

此 API 尚不建議直接實作。若工程師確認後，建議 transaction 流程如下：

1. 重新執行 validate。
2. 若 validation 失敗，直接回傳錯誤，不寫入。
3. 依 actionCode 寫入必要資料表：
   - `inventory_record`
   - `warehouse_pallet_movement`
   - `warehouse_inventory_reservation`
   - `warehouse_quality_hold`
4. 更新 `workflow_task_state.processedQuantity/taskStatus/updateTime`。
5. 新增 `workflow_task_event`。
6. commit transaction。
7. 回傳更新後 task context。

## 不得推測或需工程師確認

| 項目 | 原因 |
| --- | --- |
| 進貨單、出貨單、工單主檔 join 規則 | 目前 Task Workbench 以 workflow 主檔保存來源，不應在未確認前 join 未定義來源欄位。 |
| `inventory_record.category` 寫入對照 | 需確認各 actionCode 對應入庫、出庫、產間或其他類別。 |
| 移倉是否拆成兩筆 inventory_record | 影響庫存一致性與追溯。 |
| 品檢 release/hold/reject 寫入表 | 可能屬 Quality 模組責任，需要跨模組確認。 |
| 板位是否允許小數 | 目前 warehouse_pallet_movement 支援 float，但實務規則需確認。 |

## 工程師待確認問題

| 項目 | 需確認原因 | 工程師回覆 |
| --- | --- | --- |
| 第一版是否只做 context + validate | 降低 mutation 風險。 | Pending |
| actionCode 命名是否沿用 `warehouse.task.*` | 需與前端多國語系與後端 enum/code 管理一致。 | Pending |
| commit API 是否一次涵蓋所有 taskType | 可能需要先拆入庫/出庫/移倉/品檢。 | Pending |
| validate API 是否需要保存 draft | 若需要暫存操作草稿，需另設資料表。 | Pending |
