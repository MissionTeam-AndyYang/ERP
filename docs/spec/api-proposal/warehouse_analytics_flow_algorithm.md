# Warehouse Analytics API 流程與演算法提案

狀態：Proposal / Pending Engineer Review
對應 API 提案：`docs/spec/api-proposal/warehouse_analytics_proposal.md`
對應靜態預覽：`docs/spec/api-proposal/warehouse_analytics_static_preview.html`

## 文件定位

本文件描述 `WarehouseAnalyticsScreen` 所需 read-only API 的後端查詢流程與演算法。此畫面延續 Warehouse V1 read-only 原則，不執行任何 POST / PUT / DELETE，不更新任務狀態、不建立庫存異動、不修改安全水位、不產生 workflow event。

第一版建議 endpoint：

```txt
GET /api/v2/warehouse/analytics/overview
GET /api/v2/warehouse/analytics/value-trend
GET /api/v2/warehouse/analytics/space-utilization
GET /api/v2/warehouse/analytics/risk-breakdown
GET /api/v2/warehouse/analytics/task-sla
```

## 共用規則

1. 所有 API 僅讀取資料，不寫入任何資料表。
2. enum 僅回傳 code，前端負責多國語系轉換。
3. 金額四捨五入取整數；數量與板數取至小數點第 2 位；比率取至小數點第 2 位。
4. 查詢期間第一版建議限制在 `7d`、`30d`、`90d`，避免長區間即時計算造成效能風險。
5. 若資料不足，API 應回傳空陣列或 0 值，並保留資料來源說明，不得推測不存在的歷史事件。

## 共用 Step 1：解析查詢期間

輸入：

```txt
date
period
bucket
x-timezone
warehouse_no
itemCategory
taskType
```

建議流程：

1. Query parameter 命名沿用既有 Warehouse API 風格；倉儲篩選使用 `warehouse_no`，response payload 仍可使用 `warehouseNo`。
2. `date` 為查詢基準/截止 UTC timestamp；未提供時使用伺服器目前 UTC timestamp。
3. `period` 為回溯區間；未提供時預設 `30d`。
4. `bucket` 未提供時預設 `day`。
5. 若 `period` 不在允許清單，第一版建議 fallback 至 `30d`，並在 response.range 回傳實際採用值。
6. 後端依 `date + period` 推算 range：`endTimestamp = date`，`startTimestamp = date - period`。
7. 不接收 `dateFrom/dateTo` 作為第一版 Analytics API query parameter，避免前端與後端對查詢區間產生雙重來源。
8. 不使用 `dateRange`，避免與任務工作台的 `today`、`overdue`、`next_7_days` 等語意型範圍混淆。

## 共用 Step 2：建立庫存快照與趨勢資料

建議優先重用既有 `CWarehouseInventorySnapshotCalculator` 或 Dashboard 的庫存快照計算物件，避免 Warehouse Overview、Inventory Lot List 與 Analytics 使用不同算法。

資料來源優先順序：

1. `inventory_item_month_statistic` / `inventory_month_statistic`：作為月結基準。
2. `inventory_delta`：補算月結後異動。
3. `inventory_record`：當月結或 delta 缺漏時做短區間防護性補算。

演算法原則：

```txt
snapshot(bucketEnd) = latest_month_statistic_before_bucket + inventory_delta_between_month_start_and_bucketEnd
fallback_snapshot(bucketEnd) = inventory_record_rollup_until_bucketEnd
```

若統計表與 delta 可完整覆蓋查詢期間，使用統計表 + delta。
若統計表或 delta 缺漏，才使用 inventory_record 做缺漏 bucket 的補算，不覆蓋已由統計表產生的 bucket。

## GET /analytics/overview 流程

### Step 1：建立 range

依共用 Step 1 建立查詢區間。

### Step 2：取得 KPI

KPI 來源：

| KPI | 來源與算法 |
| --- | --- |
| totalInventoryValue | 查詢截止時間庫存快照加總 inventoryValue |
| valueChangeRate | `(endValue - startValue) / startValue * 100`；startValue 為 0 時回傳 0.0 |
| usedPallets | 查詢截止時間 `warehouse_pallet_movement` 中仍佔用或保留的板數 |
| spaceUtilizationRate | `usedPallets / totalPallets * 100`；totalPallets 為 0 時回傳 0.0 |
| riskLotCount | riskBreakdown 中具風險批號去重計數 |
| openTaskCount | `workflow_task_state` 中 pending、partial、blocked 任務數 |
| overdueTaskRate | 逾期任務數 / 開放任務數 * 100 |

### Step 3：取得 valueTrend

依 bucket 建立每個 bucket 的庫存價值：

```txt
for each bucket:
  for each itemCategory:
    inventoryValue = snapshot(bucketEnd, itemCategory).inventoryValue
    availableValue = inventoryValue - reservedValue - qualityHoldValue
```

### Step 4：取得 spaceTrend

資料來源：

```txt
warehouse_pallet_movement
ship_wh_alias
warehouse_inventory_reservation
warehouse_quality_hold
```

第一版可先回傳 bucket end 的 used/reserved/available pallets。
若 `warehouse_pallet_movement` 尚無足夠歷史資料，僅回傳資料可證明的 bucket；可將目前 snapshot 作為最後 bucket，其他無資料 bucket 不推測歷史，可回傳空陣列或 0。

### Step 5：取得 riskBreakdown

可重用 Warehouse Dashboard / Inventory 的風險判斷：

| riskType | 判斷邏輯 |
| --- | --- |
| TURNOVER_OVER_30_DAYS | daysInStock > 30 |
| SHELF_LIFE_LT_ONE_THIRD | remainingShelfLifeRatio < 1/3，不包含物料、膠捲 |
| BELOW_SAFETY_STOCK | availableQuantity < safetyStock |
| QUALITY_HOLD | qualityHoldQuantity > 0 |
| INVENTORY_SHORTAGE | workflow_task_state remainingQuantity > availableQuantity |

### Step 6：取得 taskSla

資料來源：

```txt
workflow_task_state
workflow_task_event
```

`workflow_task_event` 第一版已規劃的主要事件代碼：

| eventCode | 用途 |
| --- | --- |
| workflow.task.created | 任務建立 |
| workflow.task.assigned | 任務指派或責任部門移轉 |
| workflow.task.started | 任務開始處理 |
| workflow.task.partiallyProcessed | 任務部分處理 |
| workflow.task.blocked | 任務進入阻塞 |
| workflow.task.blockResolved | 阻塞解除 |
| workflow.task.completed | 任務完成 |
| workflow.task.cancelled | 任務取消 |
| workflow.task.refLinked | 任務關聯來源單據 |
| workflow.task.quantityAdjusted | 任務數量調整 |

建議算法：

1. 依 taskType 分組。
2. openTaskCount：taskStatus in pending / partial / blocked。
3. completedTaskCount：查詢期間內 workflow_task_event 中有 `workflow.task.completed` 的任務數；不得只以 `workflow_task_state.updateTime` 推測完成時間。
4. overdueTaskCount：dueTimestamp < now 且尚未 done / cancelled。
5. blockedTaskCount：taskStatus blocked。
6. onTimeRate：completed on time / completedTaskCount；completedTaskCount 為 0 時回傳 0.0。
7. averageLeadTimeHours：若有 event，以 first event 到 completed event 計算；若無 completed event，回傳 0.0。
8. 若查詢期間完全沒有 `workflow_task_event` 可用，`taskSla[]` 可回傳空陣列；`workflow_task_state` 仍可用於 overview KPI 的 openTaskCount 與目前逾期判斷，但不得用 creationTime/updateTime 反推完成時間或 lead time。

## GET /analytics/value-trend 流程

此 endpoint 可直接重用 overview Step 2/3，只回傳 valueTrend 與 category summary。

建議 response：

```txt
payload.range
payload.summaryByCategory[]
payload.valueTrend[]
```

不得回傳批號層級趨勢，除非工程師確認第一版畫面需要批號趨勢。

## GET /analytics/space-utilization 流程

此 endpoint 可重用 overview Step 4。

建議 response：

```txt
payload.range
payload.summaryByWarehouse[]
payload.spaceTrend[]
```

若總板數來自 `ship_wh_alias` 或倉儲合約資料，需明確限制 `ship_wh_contract.category = 2` 只取倉儲合約。

## GET /analytics/risk-breakdown 流程

此 endpoint 可重用 overview Step 5。

建議 response：

```txt
payload.range
payload.riskSummary
payload.riskBreakdown[]
payload.topRiskLots[]
```

`topRiskLots[]` 僅回傳 read-only 摘要欄位，例如 lotKey、warehouseNo、itemNo、batchNo、riskTypes、inventoryValue、quantity。

## GET /analytics/task-sla 流程

此 endpoint 可重用 overview Step 6。

建議 response：

```txt
payload.range
payload.summaryByTaskType[]
payload.summaryByDepartment[]
payload.overdueTrend[]
```

第一版不產生任務、不變更任務、不新增 workflow_task_event。

## 效能注意事項

1. `overview` 聚合 API 查詢較重，第一版建議 period 預設 `30d`，且前端不要高頻輪詢。
2. `value-trend` 與 `space-utilization` 可分開 lazy load，避免首屏等待所有圖表完成。
3. 長區間趨勢若未來超過 `90d`，建議新增每日彙總表或 cache，不建議長期依 `inventory_record` 即時計算。
4. 風險批號清單 drill-down 應由前端依 `riskType` 與目前畫面狀態組合 query string，導向既有 `GET /api/v2/warehouse/inventory/lots`，避免 analytics API 回傳大量明細或前端路由字串。
5. 任務明細 drill-down 應由前端依 `taskType` 與目前畫面狀態組合 query string，導向既有 `GET /api/v2/warehouse/task-workbench` 與 `GET /api/v2/warehouse/task-workbench/tasks/{taskId}`。

## 不得推測或需工程師確認

1. 不得設計 POST / PUT / DELETE。
2. 不得在查詢時補寫 workflow_task_event。
3. 不得在查詢時建立安全水位、風險規則或倉位容量資料。
4. 若 `warehouse_pallet_movement` 無歷史資料，不得推測歷史板位趨勢。
5. 若 workflow_task_event 無 completed event，不得自行推測完成時間；第一版以 0.0 或空陣列處理，不使用 `workflow_task_state.creationTime/updateTime` 作為 completed time fallback。

## 工程師提問

| 項目 | 需確認原因 | 工程師回覆 | 理解與確認 | 文件更新 |
| --- | --- | --- | --- | --- |
| 是否同意 `WarehouseAnalyticsScreen` 作為略過 Task Execution 後的下一個 read-only 畫面 | 確認前端第一版方向。 | 畫面實作依照規劃執行，現階段優先開發顯示資料的畫面（串接 GET API）。 | 已確認本畫面維持 read-only，優先串接 GET API。 | 文件定位維持 Warehouse V1 read-only。 |
| 是否同意 `overview` + 4 個 detail GET endpoints | 影響 API 切分與效能策略。 | 你建議採取何種方式，能夠達到最佳化？ | 建議採 `overview` 首屏輕量聚合，detail endpoint 依圖表 lazy load；共用後端計算模組但分段回傳資料。 | 已在效能注意事項與 API 提案 Detail Endpoints 補充最佳化策略。 |
| `period` 第一版是否限制為 7d / 30d / 90d | 避免長區間即時計算壓力。 | 可以，後續如有需求再新增。 | 已確認第一版限制為 `7d`、`30d`、`90d`，預設 `30d`。 | 共用 Step 1 維持此限制。 |
| `spaceTrend` 歷史資料不足時是否可只回傳目前 bucket | 避免推測不存在的倉位歷史。 | 可以 | 已確認，不補造倉位歷史；只回傳資料可證明的 bucket。 | Step 4 已更新。 |
| task SLA 是否允許用 workflow_task_state creationTime/updateTime fallback | workflow_task_event 可能尚未完整導入。 | 當 workflow_task_event 無資料時，回傳空陣列即可，還是有其他需要考量的情況？ | 不使用 `creationTime/updateTime` 推測完成時間。若期間完全無 `workflow_task_event`，`taskSla[]` 可回傳空陣列；open task KPI 仍可由 `workflow_task_state` 計算。 | Step 6 與不得推測規則已更新。 |
