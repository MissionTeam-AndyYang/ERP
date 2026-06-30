# Warehouse Task Workbench API 流程與演算法提案

狀態：Proposal / Pending Engineer Review
對應 API 提案：`docs/spec/api-proposal/warehouse_task_workbench_proposal.md`
對應靜態預覽：`docs/spec/api-proposal/warehouse_task_workbench_static_preview.html`
對應資料表提案：`docs/spec/api-proposal/warehouse_task_workbench_db_extension_proposal.md`
目的：補充 Warehouse Task Workbench API 的後端查詢流程、欄位來源、風險判斷與限制，供工程師 review 後再決定是否實作。

## 文件定位

本文件是 API 提案的流程與演算法說明，不代表目前 `restserver/` 已實作。

目前已實作或已進入確認中的 Warehouse API：

```txt
GET /api/v2/warehouse/dashboard
GET /api/v2/warehouse/inventory
GET /api/v2/warehouse/tasks
GET /api/v2/warehouse/inventory/lots
GET /api/v2/warehouse/inventory/lots/wh/{warehouseNo}/item/{itemNo}/batch/{batchNo}
```

本文件討論的下一步 proposed API：

```txt
GET /api/v2/warehouse/task-workbench
GET /api/v2/warehouse/task-workbench/tasks/{taskId}
```

## 共用規則

1. 第一版為 read-only，不更新任務狀態、不完成任務、不產生出入庫紀錄。
2. 所有 timestamp 欄位均以 UTC timestamp 回傳，前端依 `x-timezone` 顯示。
3. 所有 enum 欄位只回傳 code，不回傳多國語言顯示文字。
4. 數字格式沿用 Warehouse API 規則：
   - 單價取至小數點第 4 位。
   - 重量或數量取至小數點第 2 位。
   - 金額四捨五入取整數。
5. 尚未能從資料庫穩定取得的資料不得以假資料回傳；需回傳 0、空字串或空陣列，並在文件標示限制。

## 任務範圍

第一版工作台聚焦以下 taskType：

| taskType | 名稱 | 是否納入第一版 | 主要畫面 lane |
| --- | --- | --- | --- |
| 3 | 進貨 | YES | inbound |
| 4 | 入庫 | YES | inbound |
| 5 | 出庫 | YES | outbound |
| 6 | 移倉 | YES | outbound |
| 8 | 品檢 | YES | quality |
| 9 | 出貨 | YES | shipment |
| 1 | 請購 | NO | 非 Warehouse 主責，僅可作關聯任務 |
| 2 | 採購 | NO | 非 Warehouse 主責，僅可作關聯任務 |
| 7 | 生產 | NO | 非 Warehouse 主責，僅可作關聯任務 |

## GET /api/v2/warehouse/task-workbench 流程

### Step 1：解析查詢條件

輸入條件：

```txt
date
dateRange
warehouse_no
taskType
status
ownerDepartment
riskOnly
keyword
sort
order
start
count
```

處理規則：

1. `date` 未提供時使用伺服器目前 UTC timestamp。
2. `x-timezone` 未提供時使用 UTC。
3. `dateRange` 預設 `today`。
4. `status` 未提供時預設只回傳未完成狀態：`PENDING`、`PARTIAL`、`BLOCKED`。
5. `riskOnly=true` 在風險計算完成後套用。

### Step 2：建立日期範圍

依 `x-timezone` 將 `date` 轉為本地營業日起訖：

| dateRange | startTimestamp | endTimestamp | 補充 |
| --- | --- | --- | --- |
| `today` | 查詢日 00:00:00 | 查詢日 23:59:59 | 工作台首頁預設 |
| `next_7_days` | 查詢日 00:00:00 | 查詢日 + 6 天 23:59:59 | 用於近期任務 |
| `overdue` | 0 | 查詢日 00:00:00 - 1 | 只看逾期未完成 |
| `all_open` | 不限制 | 不限制 | 只依未完成狀態查詢 |

### Step 3：查詢 workflow_task_state

主要資料表：

```txt
workflow_task_state
```

基礎條件：

```txt
taskType in (3, 4, 5, 6, 8, 9)
taskStatus in requested statuses
```

可選條件：

```txt
warehouse_no = query.warehouse_no
taskType = query.taskType
ownerDepartment = query.ownerDepartment
dueTimestamp between range.startTimestamp and range.endTimestamp
keyword matches taskId/ref_no/ref_sub_no/item_no/item_name/batchNumber
```

排序預設：

```txt
dueTimestamp asc, taskType asc, id asc
```

### Step 4：補齊倉儲名稱

主要資料表：

```txt
ship_wh_alias
```

演算法：

```txt
warehouseName = ship_wh_alias.name where ship_wh_alias.no = workflow_task_state.warehouse_no
```

查無資料時回傳空字串。

### Step 5：取得庫存快照

主要物件：

```txt
CWarehouseInventorySnapshotCalculator
```

主要資料來源：

```txt
inventory_item_month_statistic
inventory_delta
inventory_record
warehouse_inventory_reservation
warehouse_quality_hold
```

庫存快照鍵：

```txt
warehouse_no + item_no + batchNumber
```

處理規則：

1. 若任務有 `batchNumber`，只比對同倉、同料品、同批號。
2. 若任務沒有 `batchNumber`，可先以同倉、同料品彙總候選批號可用量，但需在 response 中保留 `batchNo=""`，避免誤認任務已指定批號。
3. `currentQuantity == 0` 的批號庫存列不作為可用庫存候選。
4. `currentQuantity < 0` 保留供工程師追查，但計算可用量時不得抵銷其他批號的可用量。

### Step 6：計算任務數量

欄位來源：

| 回傳欄位 | 來源 / 算法 |
| --- | --- |
| expectedQuantity | `workflow_task_state.expectedQuantity` |
| processedQuantity | `workflow_task_state.processedQuantity` |
| remainingQuantity | `max(expectedQuantity - processedQuantity, 0)` |
| availableQuantity | 對應庫存快照的 `availableQuantity`；若無法對應回傳 0 |
| reservedQuantity | 對應庫存快照的 `reservedQuantity`；若無法對應回傳 0 |
| qualityHoldQuantity | 對應庫存快照的 `qualityHoldQuantity`；若無法對應回傳 0 |
| inventoryValue | 對應庫存快照的 `inventoryValue`；若無法對應回傳 0 |

### Step 7：計算風險

風險類型：

| riskType | 判斷規則 | 適用任務 |
| --- | --- | --- |
| `OVERDUE` | `dueTimestamp < queryTimestamp` 且任務未完成 | 全部 |
| `BLOCKED` | `taskStatus = BLOCKED` | 全部 |
| `INVENTORY_SHORTAGE` | `remainingQuantity > availableQuantity` | 出庫(5)、移倉(6)、生產領料關聯、出貨(9) |
| `QUALITY_HOLD` | `qualityHoldQuantity > 0` 且任務需要使用該批庫存 | 出庫(5)、移倉(6)、出貨(9) |
| `BATCH_NOT_ASSIGNED` | 任務需要批號但 `batchNumber` 為空 | 出庫(5)、移倉(6)、出貨(9) |

riskLevel 建議：

| 條件 | riskLevel |
| --- | --- |
| BLOCKED 或 OVERDUE | DANGER |
| INVENTORY_SHORTAGE 或 QUALITY_HOLD | WARNING |
| 無風險 | NORMAL |

### Step 8：決定 laneCode

| taskType / 狀態 | laneCode |
| --- | --- |
| taskStatus = BLOCKED | blocked |
| taskType in (3, 4) | inbound |
| taskType in (5, 6) | outbound |
| taskType = 8 | quality |
| taskType = 9 | shipment |

若同時符合 blocked 與其他任務類型，第一版 lane 優先歸入 `blocked`，但 taskType 仍保留原值。

### Step 9：決定 nextActionCode

此欄位只是前端提示，不代表 API 可執行 mutation。

| 條件 | nextActionCode |
| --- | --- |
| taskStatus = BLOCKED | `warehouse.task.resolveBlocker` |
| taskType = 3 | `warehouse.task.confirmReceipt` |
| taskType = 4 | `warehouse.task.arrangeInbound` |
| taskType = 5 | `warehouse.task.prepareOutbound` |
| taskType = 6 | `warehouse.task.arrangeTransfer` |
| taskType = 8 | `warehouse.task.waitQualityDecision` |
| taskType = 9 | `warehouse.task.prepareShipment` |

### Step 10：建立 summary 與 lanes

summary：

```txt
openTaskCount = count(open tasks)
overdueTaskCount = count(riskTypes contains OVERDUE)
blockedTaskCount = count(taskStatus = BLOCKED)
inboundTaskCount = count(taskType in 3,4)
outboundTaskCount = count(taskType in 5,6)
qualityTaskCount = count(taskType = 8)
shipmentTaskCount = count(taskType = 9)
inventoryShortageTaskCount = count(riskTypes contains INVENTORY_SHORTAGE)
```

lanes：

```txt
group by laneCode
taskCount = count(tasks in lane)
riskCount = count(tasks in lane where riskTypes not empty)
```

### Step 11：排序與分頁

允許排序欄位：

| sort | 對應欄位 |
| --- | --- |
| `dueTimestamp` | `dueTimestamp` |
| `taskType` | `taskType` |
| `remainingQuantity` | `remainingQuantity` |
| `riskLevel` | `riskLevel` |

分頁需在全部篩選與排序完成後執行。

## GET /api/v2/warehouse/task-workbench/tasks/{taskId} 流程

### Step 1：查詢任務主資料

```txt
workflow_task_state.taskId = path.taskId
```

若查無任務：

```txt
payload.task = {}
payload.quantity = {}
payload.relatedLots = []
payload.sourceRefs = []
payload.timeline = []
```

工程師已確認第一版回傳成功空 payload，不回傳 404。

### Step 2：補齊任務欄位

沿用 list API 的欄位計算規則：

```txt
remainingQuantity
riskTypes
riskLevel
nextActionCode
warehouseName
```

### Step 3：查詢 relatedLots

若任務已有 batchNumber：

```txt
relatedLots = inventory lots where warehouse_no + item_no + batchNumber match task
```

若任務沒有 batchNumber：

```txt
relatedLots = inventory lots where warehouse_no + item_no match task
sort by risk first, validDate asc, availableQuantity desc
```

每筆 relatedLot 應包含：

```txt
lotKey
warehouseNo
itemNo
itemName
batchNo
currentQuantity
availableQuantity
qualityHoldQuantity
validDate
riskTypes
```

### Step 4：建立 sourceRefs

`payload.task.refCategory/refNo/refSubNo` 表示主任務來源，直接取自 `workflow_task_state`：

```txt
refCategory = workflow_task_state.refCategory
refNo = workflow_task_state.ref_no
refSubNo = workflow_task_state.ref_sub_no
```

`payload.sourceRefs[]` 表示主任務來源集合：

1. `workflow_task_state.taskId` 為 UK，因此第一版明確採用「一個 taskId 對應一個主任務來源」。
2. `sourceRefs[]` 保留 array 型態，但第一版固定只回傳 `workflow_task_state.refCategory/ref_no/ref_sub_no` 對應的主任務來源，通常為一筆。
3. `workflow_task_event.refCategory/ref_no/ref_sub_no` 僅表示事件發生時的來源上下文，不彙總進 `sourceRefs[]`，也不改變主任務來源。
4. 不 join 尚未確認的來源主檔；`descriptionCode` 僅用穩定 code 表示來源用途，由前端轉換顯示文字。

`descriptionCode` 由 taskType 與 refCategory 產生穩定 code，例如：

```txt
warehouse.source.goodsReceipt
warehouse.source.workOrder
warehouse.source.shipment
```

若無法穩定判斷，回傳空字串。

### Step 5：建立 timeline

工程師已確認需要完整流程歷史，建議新增 `workflow_task_event` 保存任務事件。timeline 來源規則：

```txt
timelineRows = workflow_task_event where taskId = path.taskId order by eventTimestamp asc, id asc
```

回傳欄位：

```txt
eventCode = workflow_task_event.eventCode
eventTimestamp = workflow_task_event.eventTimestamp
department = workflow_task_event.toDepartment or workflow_task_event.fromDepartment
status = workflow_task_event.toStatus or workflow_task_event.fromStatus
comment = workflow_task_event.comment
```

`workflow_task_event` 與 `workflow_task_state` 的關係為一任務多事件：

```txt
workflow_task_state.taskId 1 -> N workflow_task_event.taskId
```

事件表中的 `refCategory/ref_no/ref_sub_no` 只是該事件的來源上下文。若未來確認單一事件需要同時關聯多張來源單據，需另行設計 `workflow_task_event_ref` child table；第一版不納入。

若 `workflow_task_event` 尚未導入或該 taskId 尚無事件資料，第一版可回傳空陣列，不以 `workflow_task_state` 推測完整歷史。新增資料表提案：

```txt
docs/spec/api-proposal/warehouse_task_workbench_db_extension_proposal.md
```

此表仍為提案，不代表目前正式資料庫已存在。

## 工程師待確認問題

| 項目 | 需確認原因 | 工程師回覆 |
| --- | --- | --- |
| 查無 taskId 時回傳 404 或成功空 payload | 影響前端錯誤處理與 API convention。 | 回傳成功空 payload  |
| 任務未指定批號時是否可彙總同倉同料品候選批號 | 影響出庫與出貨任務的可用庫存判斷。 | 工程師回覆：可以。 |
| `blocked` lane 是否優先於 taskType lane | 影響看板視覺分類與主管處理順序。 |  `blocked` lane 優先於 taskType lane |
| 是否需要 `workflow_task_event` 任務歷史表 | 影響 detail timeline 是否能呈現完整流程。 | 工程師回覆：需要完整流程歷史；已新增資料表提案 `warehouse_task_workbench_db_extension_proposal.md`。 |
| `nextActionCode` 是否由後端回傳 | 若前端自行依 taskType 推導，可省略此欄；若後端回傳可保持跨端一致。 | 由後端回傳 |
| `taskId` 為 UK 時，`sourceRefs[]` 是否代表一任務多來源 | 避免 `workflow_task_state` 主來源設計與 detail API 欄位語意衝突。 | 已確認不代表一任務多主任務來源；第一版一個 taskId 僅對應一個主任務來源，`sourceRefs[]` 固定回傳該主任務來源。 |
