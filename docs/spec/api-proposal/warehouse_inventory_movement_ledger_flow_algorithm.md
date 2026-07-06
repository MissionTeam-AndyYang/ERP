# Warehouse Inventory Movement Ledger API 流程與演算法提案

狀態：Deferred to next version / Not in current V1 core scope
對應 API 提案：`docs/spec/api-proposal/warehouse_inventory_movement_ledger_proposal.md`
對應靜態預覽：`docs/spec/api-proposal/warehouse_inventory_movement_ledger_static_preview.html`

## 文件定位

本文件描述 `WarehouseInventoryMovementLedgerScreen` 所需 read-only API 的後端查詢流程與演算法。此畫面用於查詢庫存異動流水帳，不建立、不修改、不刪除任何庫存資料，也不更新 workflow task。

依 2026-07-06 規劃確認，第一版前端畫面優先實作 phase 為 core 的畫面；`WarehouseInventoryMovementLedgerScreen` 延至下一版，本版不進行工程師 review、後端實作或前端串接。本文件僅保留作為下一版追溯畫面設計基礎。

第一版建議 endpoint：

```txt
GET /api/v2/warehouse/inventory/movements
GET /api/v2/warehouse/inventory/movements/summary
```

## 共用規則

1. 所有 API 僅讀取資料，不寫入任何資料表。
2. enum 僅回傳 code，前端負責多國語系轉換。
3. 金額四捨五入取整數；數量取至小數點第 2 位；單價取至小數點第 4 位。
4. 後端不得回傳前端路由用的 `drilldownQuery`；前端依目前畫面狀態自行組合 query string。
5. 第一版以 `inventory_record` 作為唯一庫存異動明細真實來源，不從月結表反推流水帳。
6. 分頁必須在資料庫查詢層完成，不可一次取回全部資料後再切片。

## 共用 Step 1：解析查詢期間與分頁

輸入：

```txt
date
period
bucket
x-timezone
start
count
sort
order
```

建議流程：

1. `date` 為查詢截止 UTC timestamp；未提供時使用伺服器目前 UTC timestamp。
2. `period` 支援 `7d`、`30d`、`90d`；未提供或不支援時 fallback 至 `30d`，並在 response.range 回傳實際採用值。
3. `bucket` 支援 `day`、`week`、`month`；未提供或不支援時 fallback 至 `day`。
4. `start` 小於 0 時以 0 處理。
5. `count` 未提供時預設 50，最大值 100。
6. `sort` 使用白名單：`date`、`item_no`、`batchNo`、`quantity`、`amount`。
7. `order` 使用白名單：`asc`、`desc`。

## 共用 Step 2：建立查詢條件

主要資料表：

```txt
inventory_record
```

基本條件：

```txt
inventory_record.date >= range.startTimestamp
inventory_record.date <= range.endTimestamp
```

若 `inventory_record.date` 可能為 0，工程師確認後才可改用 `creationTime` fallback；第一版建議仍以 `date` 作為主要查詢欄位，避免異動日與建檔日語意混淆。

篩選條件：

| Query Parameter | Table Field | Rule |
| --- | --- | --- |
| warehouse_no | inventory_record.warehouse_no | 等於指定倉儲 no |
| itemCategory | inventory_record.itemCategory | 等於指定料品品項類別 |
| item_no | inventory_record.item_no | 等於指定料品 no |
| batchNo | inventory_record.batchNumber | 等於指定批號 |
| refCategory | inventory_record.refCategory | 等於指定來源單據類別 |
| ref_no | inventory_record.ref_no | 等於指定來源單據 no |
| category | inventory_record.category | 等於指定入庫/出庫方向 |
| keyword | inventory_record.item_no / item_name / batchNumber / ref_no | 模糊搜尋 |

## 共用 Step 3：補充批號與倉儲資料

補充資料表：

```txt
batch_number
ship_wh_alias
```

建議 join 策略：

1. 以 `inventory_record.batchNumber = batch_number.no` 左外連接 `batch_number`，取得 `batch_number.refCategory/ref_no`。
2. 以 `inventory_record.warehouse_no = ship_wh_alias.no` 左外連接 `ship_wh_alias`，補充倉儲名稱。
3. 若 `inventory_record.warehouse_displayName` 有值，優先使用該欄位；若缺漏，再使用 `ship_wh_alias.name`。

## GET /inventory/movements 流程

### Step 1：建立 range 與 filters

依共用 Step 1 與 Step 2 建立查詢條件。

### Step 2：計算 total 與 summary

1. 使用相同 filters 計算 `total`。
2. 使用相同 filters group by `inventory_record.category` 計算入庫、出庫數量與金額。
3. `quantity` 與 `amount` 固定以正值回傳；入庫/出庫方向由 `category` 判斷。
4. 若現有資料存在負數，建議以 `abs(count)` 與 `abs(amount)` 進入入庫/出庫摘要，避免方向與正負值重複表達。

### Step 3：使用資料庫層分頁查詢明細

1. 套用 sort / order。
2. 套用 offset / limit。
3. 第一版預設排序：`date desc, id desc`。
4. 不可一次取回全部資料再由 Python 擷取第 n 筆至第 n+50 筆。

### Step 4：組裝 results

每筆明細以 `inventory_record` 為主：

| Response Field | Source / Algorithm |
| --- | --- |
| movementId | `inventory_record.id` |
| movementTimestamp | `inventory_record.date` |
| warehouseNo | `inventory_record.warehouse_no` |
| warehouseName | `inventory_record.warehouse_displayName` 或 `ship_wh_alias.name` |
| itemNo | `inventory_record.item_no` |
| itemName | `inventory_record.item_name` |
| itemCategory | `inventory_record.itemCategory` |
| itemType | `inventory_record.itemType` |
| batchNo | `inventory_record.batchNumber` |
| category | `inventory_record.category` |
| refCategory | `inventory_record.refCategory` |
| refNo | `inventory_record.ref_no` |
| serialNo | `inventory_record.serialNo` |
| quantity | `abs(inventory_record.count)` |
| unit | `inventory_record.unit` |
| unitCost | `inventory_record.price`；若為 0 且 count > 0，以 `amount / count` 補算 |
| amount | `abs(inventory_record.amount)` |
| sourceTable | 固定 `inventory_record` |
| sourceId | `inventory_record.id` |
| batchRefCategory | `batch_number.refCategory`，缺漏時 0 |
| batchRefNo | `batch_number.ref_no`，缺漏時空字串 |
| comment | `inventory_record.comment` |

## GET /inventory/movements/summary 流程

### Step 1：建立 range 與 filters

使用與 list API 完全相同的期間與篩選邏輯。

### Step 2：計算 summary

使用 filters group by `inventory_record.category`：

```txt
inboundQuantity = sum(abs(count)) where category = inbound
outboundQuantity = sum(abs(count)) where category = outbound
netQuantity = inboundQuantity - outboundQuantity
inboundValue = sum(abs(amount)) where category = inbound
outboundValue = sum(abs(amount)) where category = outbound
netValue = inboundValue - outboundValue
movementCount = count(*)
```

### Step 3：計算 trend

依 `bucket` 建立期間分桶：

1. `day`：以查詢時區的日為 bucket。
2. `week`：以查詢時區的週為 bucket。
3. `month`：以查詢時區的月份為 bucket。

每個 bucket 依 `inventory_record.category` group by：

```txt
quantity = sum(abs(count))
amount = sum(abs(amount))
movementCount = count(*)
```

### Step 4：計算 summaryByCategory

依 `inventory_record.itemCategory` group by：

```txt
inboundValue
outboundValue
netValue
movementCount
```

## 效能注意事項

1. `inventory_record.date`、`warehouse_no`、`item_no`、`batchNumber`、`ref_no` 建議具備可支援查詢的索引；若目前缺漏，需由工程師評估是否加入資料庫索引提案。
2. 分頁必須使用 SQL offset / limit。
3. `summary` 與 `list` 使用同一組 filters，但可分開查詢；不要為了組 summary 而載入全部明細。
4. `keyword` 模糊搜尋可能較慢，第一版僅在使用者主動輸入時套用。
5. 若未來要支援超過 90 天或多年追溯，建議新增彙總表或使用離線索引，不建議長期以即時 `inventory_record` 全表掃描。

## 不得推測或需工程師確認

1. 不得從月結表或 delta 表反推出不存在的流水帳明細。
2. 不得在查詢時補寫 `inventory_record`、`workflow_task_event` 或任何倉庫任務資料。
3. `category` enum 值需由工程師確認是否完整涵蓋入庫與出庫方向。
4. `inventory_record.date = 0` 時是否可 fallback 至 `creationTime`，需工程師確認後再實作。
5. `summary` 的數量在混合單位條件下僅供參考，前端需以金額作為跨品項主要比較指標。

## Engineer Review Questions

| 項目 | 需確認原因 | 工程師回覆 | Codex 建議 |
| --- | --- | --- | --- |
| 是否同意此畫面作為 Analytics 後的下一個 V1 read-only 畫面 | 2026-07-06 已調整為第一版優先 phase core 畫面。 | 已延至下一版 | 本版略過，不進行 review / 實作。 |
| `inventory_record.category` 的 enum 是否可直接作為 API `category` | 影響入庫/出庫方向判斷。 | 待工程師回覆 | 建議直接沿用資料庫欄位，不新增 `direction`。 |
| `inventory_record.date = 0` 是否允許 fallback 至 `creationTime` | 影響異動時間查詢準確性。 | 待工程師回覆 | 建議第一版不 fallback，除非工程師確認歷史資料需要。 |
| 是否需要新增索引 | 影響大資料量下查詢效能。 | 待工程師回覆 | 建議實測後評估 `date + warehouse_no + item_no + batchNumber` 或 `date + ref_no` 組合索引。 |
