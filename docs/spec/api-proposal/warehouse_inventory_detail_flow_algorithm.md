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
GET /api/v2/warehouse/inventory/lots/wh/{warehouseNo}/item/{itemNo}/batch/{batchNo}
```

## 工程師建議與回覆

| 項目 | 工程師建議 | 工程師回覆 / 規格調整 |
| --- | --- | --- |
| Step 2 庫存快照計算 | 請評估是否適合由 `CWarehouseInventorySnapshotCalculator` 物件取得目前庫存數量與庫存價值。 | 採用。Inventory Detail list/detail 與 Warehouse Dashboard / Inventory API 應共用同一個庫存快照計算物件，避免統計表、delta 與防護性補算邏輯分裂。 |
| `currentQuantity <= 0` 過濾 | 請說明為何不回傳 `currentQuantity <= 0`，並建議 `currentQuantity < 0` 可回傳。 | 調整為只過濾 `currentQuantity == 0`。零庫存批號不具備管理者畫面上的可操作庫存意義，且會干擾風險警示；負庫存代表資料異常或補登落差，開發與測試階段應保留回傳，方便工程師追查。 |
| `sourceDocuments.quantity` 正負方向 | 請說明出庫是否以負數表示，如何影響前端時間線與金額方向，並提出建議處理方式。 | 建議同時回傳 `direction`、`quantity/amount` 絕對值與 `signedQuantity/signedAmount` 帶方向值。前端時間線用 `direction` 呈現入庫/出庫標籤，數量顯示使用絕對值；若要畫趨勢或計算餘量，使用 signed 欄位。 |
| workflow task 範圍 | 第一版 workflowTasks 是否只顯示未完成任務。 | 採用。第一版只顯示未完成任務；歷史任務後續可透過查詢參數擴充。 |

## 共用規則

1. 所有 timestamp 欄位均以 UTC timestamp 回傳，前端依 `x-timezone` 顯示。
2. 所有 enum 欄位只回傳 code，不回傳多國語言顯示文字。
3. 風險警示只回傳 `riskTypes`、`messageCode`、`messageParams` 或相關 code，不回傳繁中 fallback 文字。
4. 數字格式沿用 Warehouse API 規則：
   - 單價取至小數點第 4 位。
   - 重量或數量取至小數點第 2 位。
   - 金額四捨五入取整數。
5. 尚未能從資料庫取得的資料不得以假資料回傳；需回傳 0、空字串或空陣列，並在文件標示限制。

## lotKey 與階層化路徑建議

Detail API 第一版採用階層化路徑：

```txt
GET /api/v2/warehouse/inventory/lots/wh/{warehouseNo}/item/{itemNo}/batch/{batchNo}
```

`lotKey` 仍可由 list API 回傳，但僅作為前端 table row key / drill-down key，不作 detail API 必要查詢參數。

第一版 `lotKey` 建議使用可讀、可解析的組合 key：

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

主要物件：

```txt
CWarehouseInventorySnapshotCalculator
```

主要資料來源：

```txt
inventory_item_month_statistic
inventory_delta
inventory_record
```

庫存鍵維度：

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
snapshotRows = CWarehouseInventorySnapshotCalculator.query_inventory_rows(...)

主路徑：
currentQuantity = monthEndQuantity + deltaInCount - deltaOutCount
inventoryValue = monthEndAmount + deltaInAmount - deltaOutAmount

fallback：
若統計資料為空、delta 覆蓋不足，或統計結果缺漏特定 stock key，
才使用 inventory_record 依 warehouse_no + item_no + batchNumber 防護性補算。
```

保護規則：

1. `currentQuantity == 0` 的列不回傳，因為零庫存批號不具備第一版管理者畫面的可操作庫存意義，也不應產生風險警示。
2. `currentQuantity < 0` 的列保留回傳，因為負庫存通常代表補登、沖銷或資料異常，開發與測試階段需要直接呈現以利工程師追查。
3. `inventoryValue < 0` 時仍保留原計算結果供工程師檢查；若前端不適合顯示負值，可由 API review 再確認是否歸零或加註異常樣式。

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
| lastSourceNo | `batch_number.ref_no` | 無資料時回傳空字串。 |
| lastSourceCategory | `batch_number.refCategory` | 無資料時回傳 0。 |

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

## GET /api/v2/warehouse/inventory/lots/wh/{warehouseNo}/item/{itemNo}/batch/{batchNo} 流程

### Step 1：解析 path parameters

1. 從 path parameters 取得 `warehouseNo`、`itemNo`、`batchNo`。
2. 任一必要參數為空時回傳參數錯誤。
3. 不採信前端其他暫存資料，重新查詢後端資料。

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
| direction | 由 `inventory_record.category` 轉換；入庫為 `IN`，出庫為 `OUT` |
| quantity | `abs(inventory_record.count)`，給前端時間線直接顯示數量 |
| signedQuantity | 入庫為 `inventory_record.count`，出庫為 `-inventory_record.count`，給前端趨勢或餘量計算 |
| amount | `abs(inventory_record.amount)`，給前端時間線直接顯示金額 |
| signedAmount | 入庫為 `inventory_record.amount`，出庫為 `-inventory_record.amount`，給前端顯示資金方向或計算餘額 |

設計理由：

1. 前端時間線通常以「事件」呈現，使用 `direction` 搭配正數 `quantity/amount` 可避免使用者看到負數而誤解。
2. 分析圖、累計餘量與金額流向需要方向，使用 `signedQuantity/signedAmount` 可避免前端自行推導造成邏輯不一致。
3. 若未來需顯示退貨、沖銷或調整，可擴充 `direction` 值，而不破壞既有正數顯示欄位。

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
| `lotKey` 是否採組合 key | 影響 API path、前端路由與未來流水號層級擴充。 | 採用工程師建議：detail API 改為階層化路徑 `GET /api/v2/warehouse/inventory/lots/wh/{warehouseNo}/item/{itemNo}/batch/{batchNo}`；`lotKey` 僅保留為前端 row key。 |
| `sourceDocuments.quantity` 出庫是否以負數表示 | 影響前端時間線呈現與金額方向。 | 採用雙欄位策略：`quantity/amount` 回傳絕對值供時間線顯示，`signedQuantity/signedAmount` 回傳帶方向值供趨勢與餘量計算，並以 `direction` 明確標示 `IN/OUT`。 |
| `inventoryValue < 0` 是否保留 | 影響資料異常時的呈現方式。 | 採用工程師建議：開發階段保留負值以利 debug；同時調整為只過濾 `currentQuantity == 0`，`currentQuantity < 0` 保留回傳供資料異常追查。 |
| `workflowTasks` 是否只顯示未完成任務 | 第一版建議只顯示未完成；歷史任務可後續加參數。 | 採用工程師建議：第一版只顯示未完成任務。 |
