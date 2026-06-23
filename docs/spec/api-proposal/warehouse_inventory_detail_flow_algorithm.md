# Warehouse Inventory Detail API 流程與演算法提案

狀態：Proposal / Pending Engineer Review
對應 API 提案：`docs/spec/api-proposal/warehouse_inventory_detail_proposal.md`
對應靜態預覽：`docs/frontend/preview/warehouse_inventory_detail_static_preview.html`
目的：補充 Warehouse Inventory Detail API 的後端查詢流程、欄位來源與計算規則，供工程師 review 後再決定是否實作。

## 文件定位

本文件是 API 提案的流程與演算法說明，不代表目前 `restserver/` 已實作。

目前已確認可實作並已進入程式碼的 API 為：

```txt
GET /api/v2/warehouse/dashboard
GET /api/v2/warehouse/inventory
GET /api/v2/warehouse/tasks
```

本文件討論的 API 尚待工程師確認：

```txt
GET /api/v2/warehouse/inventory/lots
GET /api/v2/warehouse/inventory/lots/{lotKey}
```

## 工程師建議
1. Step 2：彙總目前庫存量與庫存價值
   請評估是否適合由 CWarehouseInventorySnapshotCalculator 物件來取得 目前庫存數量 與 庫存價值

## 共用規則

1. 所有 timestamp 欄位均以 UTC timestamp 回傳，前端依 `x-timezone` 顯示。
2. 所有 enum 欄位只回傳 code，不回傳多國語言顯示文字。
3. 風險警示只回傳 `riskTypes`、`messageCode`、`messageParams` 或相關 code，不回傳繁中 fallback 文字。
4. 數字格式沿用 Warehouse API 規則：
   - 單價取至小數點第 4 位。
   - 重量或數量取至小數點第 2 位。
   - 金額四捨五入取整數。
5. 尚未能從資料庫取得的資料不得以假資料回傳；需回傳 0、空字串或空陣列，並在文件標示限制。

## lotKey 建議

第一版建議使用可讀、可解析的組合 key：

```txt
lotKey = warehouseNo + "|" + itemNo + "|" + batchNo
```

解析規則：

| Segment | 對應欄位 | 說明 |
| --- | --- | --- |
| warehouseNo | `warehouse_no` | 倉儲別名 no。 |
| itemNo | `item_no` | 料品品項編號。 |
| batchNo | `batchNumber` / `batch_number.no` | 批號。 |

若後續需要支援流水號層級，可延伸為：

```txt
warehouseNo|itemNo|batchNo|serialNo
```

## GET /api/v2/warehouse/inventory/lots 流程

### Step 1：解析查詢條件

輸入條件：

```txt
date
warehouse_no
itemCategory
item_no
batchNo
riskType
taskType
availability
keyword
sort
order
start
count
```

處理規則：

1. `date` 未提供時使用伺服器目前 UTC timestamp。
2. `warehouse_no`、`itemCategory`、`item_no`、`batchNo` 直接作為庫存彙總篩選條件。
3. `riskType` 在風險計算完成後套用。
4. `taskType` 在 `workflow_task_state` 彙總未完成任務時套用。
5. `availability` 在可用量計算後套用：
   - `available`：`availableQuantity > 0`
   - `reserved`：`reservedQuantity > 0`
   - `quality_hold`：`qualityHoldQuantity > 0`
   - `blocked`：存在未完成且狀態為阻塞的 workflow task

### Step 2：彙總目前庫存量與庫存價值

主要資料表：

```txt
inventory_record
```

彙總維度：

```txt
warehouse_no
warehouse_displayName
itemCategory
item_no
item_name
itemType
batchNumber
unit
```

演算法：

```txt
currentQuantity = sum(count where category = IN)
                - sum(count where category = OUT)

inventoryValue = sum(amount where category = IN)
               - sum(amount where category = OUT)

firstInboundTimestamp = min(date where category = IN)
```

保護規則：

1. `currentQuantity <= 0` 的列不回傳。
2. `inventoryValue < 0` 時仍保留原計算結果供工程師檢查；若前端不適合顯示負值，可由 API review 再確認是否歸零。

### Step 3：補齊批號與料品資訊

主要資料表：

```txt
batch_number
material
inproduct
product
goods
```

欄位來源：

| 回傳欄位 | 優先來源 | 補充來源 |
| --- | --- | --- |
| itemSubCategory | `batch_number.itemSubCategory` | 原料/物料/膠捲取 `material.subCategory`；在製品取 `inproduct.category`；製成品取 `product.category`；貨品取 `goods.subCategory`。 |
| itemType | `batch_number.itemType` | `inventory_record.itemType`。 |
| validDays | `batch_number.validDays` | 無資料時回傳 0。 |
| validDate | `batch_number.validDate` | 無資料時回傳 0。 |

### Step 4：彙總預留與品檢保留

預留來源：

```txt
warehouse_inventory_reservation
```

有效條件：

```txt
status = 1
releaseTime is null or releaseTime > queryTimestamp
```

品檢保留來源：

```txt
warehouse_quality_hold
```

有效條件：

```txt
status = 1
```

演算法：

```txt
reservedQuantity = sum(reservedQuantity)
reservedValue = sum(reservedValue)

qualityHoldQuantity = sum(holdQuantity)
qualityHoldValue = sum(holdValue)

availableQuantity = max(currentQuantity - reservedQuantity - qualityHoldQuantity, 0)
availableValue = max(inventoryValue - reservedValue - qualityHoldValue, 0)
```

### Step 5：彙總板數

主要資料表：

```txt
warehouse_pallet_movement
```

演算法：

```txt
palletCount = sum(palletCount where palletStatus = 1)
```

第一版 `palletStatus = 1` 代表已佔用板數；預留板數若需顯示，可另以 `palletStatus = 2` 彙總。

### Step 6：計算風險

風險類型：

| riskType | 判斷規則 |
| --- | --- |
| `TURNOVER_OVER_30_DAYS` | `daysInStock > 30` |
| `SHELF_LIFE_LT_ONE_THIRD` | `remainingShelfLifeRatio <= 0.3333`，且排除物料、膠捲。 |
| `BELOW_SAFETY_STOCK` | `availableQuantity < safetyStock` |

安全水位來源：

```txt
item_safety_stock
```

選擇順序：

1. 優先取 `item_no + warehouse_no` 且啟用、生效中的設定。
2. 若無，取 `item_no` 全倉通用設定。
3. 若仍無，`safetyStock = 0` 且不產生低於安全水位風險。

### Step 7：彙總未完成任務

主要資料表：

```txt
workflow_task_state
```

未完成狀態：

```txt
taskStatus in (待處理, 部分完成, 阻塞)
```

批號對應條件：

```txt
warehouse_no
item_no
batchNumber
```

演算法：

```txt
openTaskCount = count(workflow_task_state where taskStatus in pending/partial/blocked)
```

若查詢參數提供 `taskType`，需額外套用任務類型篩選。

### Step 8：排序、分頁與 summary

排序欄位建議：

| sort | 對應資料 |
| --- | --- |
| inventoryValue | `inventoryValue` |
| availableQuantity | `availableQuantity` |
| validDate | `validDate` |
| daysInStock | `daysInStock` |

summary 演算法：

```txt
lotCount = count(results before paging)
itemCount = distinct count(itemNo)
totalQuantity = sum(currentQuantity)
totalInventoryValue = sum(inventoryValue)
totalAvailableQuantity = sum(availableQuantity)
totalAvailableValue = sum(availableValue)
riskLotCount = count(rows where riskTypes is not empty)
pendingTaskCount = sum(openTaskCount)
```

## GET /api/v2/warehouse/inventory/lots/{lotKey} 流程

### Step 1：解析 lotKey

1. 依 `|` 分割 `lotKey`。
2. 若格式不足三段，回傳參數錯誤。
3. 取得 `warehouseNo`、`itemNo`、`batchNo` 後，不採信前端其他暫存資料，重新查詢後端資料。

### Step 2：重算 lot 主資料

沿用 list API 的 Step 2 至 Step 6，只針對單一 `warehouseNo + itemNo + batchNo` 回傳 `lot` 物件。

### Step 3：查詢來源與異動紀錄

主要資料表：

```txt
inventory_record
```

查詢條件：

```txt
warehouse_no = warehouseNo
item_no = itemNo
batchNumber = batchNo
```

回傳 `sourceDocuments`：

| 欄位 | 來源 |
| --- | --- |
| refCategory | `inventory_record.refCategory` |
| refNo | `inventory_record.ref_no` |
| refSubNo | 第一版若無來源明細欄位，回傳空字串 |
| date | `inventory_record.date` |
| quantity | `inventory_record.count`，出庫可用負數或另由 category 判斷，待 review 確認 |
| amount | `inventory_record.amount` |

### Step 4：查詢預留、品檢、板位與任務

| 回傳資料集 | 資料表 | 條件 |
| --- | --- | --- |
| reservations | `warehouse_inventory_reservation` | `item_no + batchNumber + warehouse_no` |
| qualityHolds | `warehouse_quality_hold` | `item_no + batchNumber + warehouse_no` |
| palletMovements | `warehouse_pallet_movement` | `item_no + batchNumber + warehouse_no` |
| workflowTasks | `workflow_task_state` | `item_no + batchNumber + warehouse_no` |

### Step 5：回傳限制

1. 不回傳 enum 顯示文字。
2. 不回傳繁中風險 fallback 文字。
3. 若來源單據名稱或明細尚無穩定 join 規則，第一版只回傳來源類別與來源單號。
4. 若 Quality 模組尚未正式串接，品檢資訊先以 `warehouse_quality_hold` 為準。

## 工程師待確認問題

| 項目 | 需確認原因 | 工程師回覆 |
| --- | --- | --- |
| `lotKey` 是否採組合 key | 影響 API path、前端路由與未來流水號層級擴充。 |建議採用階層化路徑，例如: GET /api/v2/warehouse/inventory/lots/wh/{warehouseNo}/item/{itemNo}/batch/{batchNo} |
| `sourceDocuments.quantity` 出庫是否以負數表示 | 影響前端時間線呈現與金額方向。 |請詳細說明此邏輯如何影響 前端時間線的呈現 與 金額方向的顯示，並請提出你建議的 處理方式。|
| `inventoryValue < 0` 是否保留 | 影響資料異常時的呈現方式。 |目前處於開發階段，先保留 原始資料的呈現，以方便進行 debug。待進入後續測試或正式上線階段，再依需求調整資料顯示方式。另外， 請說明為什麼`currentQuantity <= 0` 的列不回傳? 是否有其他設計上的考量? 建議`currentQuantity < 0` 的列可回傳。|
| `workflowTasks` 是否只顯示未完成任務 | 第一版建議只顯示未完成；歷史任務可後續加參數。 |第一版先實作顯示未完成|
