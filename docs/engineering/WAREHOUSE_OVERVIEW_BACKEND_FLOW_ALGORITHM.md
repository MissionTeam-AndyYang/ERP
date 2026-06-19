# 倉庫經營總覽後端流程與演算法規劃

日期：2026-06-11
狀態：草案 / 待工程師 Review
對應 API 草案：`docs/spec/api-proposal/warehouse_overview_api.md`
對應 DB 新增規劃：`docs/spec/database/WAREHOUSE_OVERVIEW_DB_EXTENSION_PLAN.md`

## 工程師提問與建議:

1. Step 3：計算預留數量與預留價值
    - 請進一步說明『預留數量』與『品檢保留量』的定義及差異?
    - 能否詳細說明，哪些來源訂單會新增至 `warehouse_inventory_reservation`？例如：請購單是否會納入？ 進貨單是否會納入？銷貨單是否會納入？工單領料是否也會納入？
    
2. Step 4：計算品檢保留量與保留價值
    - 能否詳細說明，哪些來源訂單會新增至 `warehouse_quality_hold`？例如：請購單是否會納入？ 進貨單是否會納入？銷貨單是否會納入？工單領料是否也會納入？

3. Step 11：計算任務處理狀態
    - 為什麼需要盤點單呢？能否分享你的想法？
    - 在實務情境中，是否可能出現『已處理數量』小於『預期處理數量』的情況？例如：採購進貨時，廠商送貨到場後經檢查發現部分料品損壞。此時，任務狀態應如何轉換為「已完成」?

4. Step 12：判斷下一步負責部門
    - 建議建立資料表以完整紀錄「下一步負責部門」，涵蓋從請購 → 採購 → 進貨 → 產製 → 訂購出貨的各環節，將整體流程納入考量

## 本次調整決議

| 項目 | 決議 |
| --- | --- |
| `sourceType` 命名 | 更名為 `refCategory`，用於表示 `ref_no` 指向的業務來源類別。 |
| 來源欄位命名 | 使用 `ref_no` / `ref_sub_no`，以符合既有資料庫命名規則。 |
| `id` 與 `no` | 維持原設計：`id` 作 PK，`no` 作 UK 與業務識別碼。 |
| `warehouse_pallet_movement` | 維持原設計，不分散整合至其他表。 |
| 倉儲容量來源 | 取消新增 `warehouse_capacity`，改由 `ship_wh.maxCapacity` 搭配 `ship_wh_contract`、`ship_wh_alias` 取得。 |
| 任務狀態 | 改用跨模組 `workflow_task_state`，Warehouse dashboard 僅篩選與倉庫待處理相關的任務。 |
| 盤點 | 第一版 Warehouse dashboard 暫不處理盤點。 |

## 文件定位

本文件只描述流程與演算法，不進行程式實作。
待工程師確認後，才開始建立 SQL schema、ORM model、API route 與 service layer。

## API Route 建議

依工程師回覆，Warehouse dashboard 建議使用新的 v2 route：

```txt
GET /api/v2/warehouse/dashboard
GET /api/v2/warehouse/inventory
GET /api/v2/warehouse/tasks
```

v1 文件可保留為討論歷史；實作時以 v2 route 為準。

## 共用時間規則

1. DB 的 `date`、`time`、`creationTime` 若為 timestamp，統一視為 UTC timestamp。
2. 新增規劃表不個別保存 `timezone`；`date`、`time`、`creationTime` 一律保存 UTC timestamp。
3. API 接收 `date` 與 `timezone` 後，需換算為本地營業日的 UTC 起訖時間。
4. 回傳給前端時，timestamp 保持 UTC timestamp；顯示格式由前端依語系與時區轉換。

## Enum 與多國語言規則

1. 後端回傳 enum code 或穩定 code，例如 `itemCategory = 1`、`riskType = TURNOVER_OVER_30_DAYS`。
2. 前端負責 enum 到多國語言字串的轉換，例如 `1 -> 原料`。
3. 後端回傳 `messageCode`、`messageParams`、`recommendedActionCode`，前端依語系組成顯示文字。
4. 第一版不回傳繁中 fallback `message` 與 `recommendedAction`，避免後端與前端多國語言職責重疊。

## 類別庫存量顯示規則

「料品品項類別」層級的庫存量通常混合不同單位，因此：

1. `inventoryValueByCategory[].quantity` 可保留作參考或計算欄位。
2. 前端類別統計畫面不顯示庫存單位。
3. 後端若回傳 `unit`，混合單位時建議回傳 `0`。
4. 明細層級 `inventory[].unit`、`riskAlerts[].unit`、`tasks[].unit` 仍保留，因為明細通常可對應單一單位。

## Dashboard 聚合流程

### Step 1：建立查詢範圍

輸入：

```txt
date
timezone
warehouse_no
itemCategory
includeInventory
riskOnly
```

處理：

1. 將 `date` 轉為使用者時區的營業日。
2. 取得營業日起訖 UTC timestamp。
3. 建立倉儲、料品類別與風險篩選條件。

### Step 2：計算目前庫存數量與庫存價值

建議來源：

1. 月底基準：第一版直接採用 `inventory_item_month_statistic` 的批號層級月結結存。
2. 月底後異動：採用 `inventory_delta` 補算月結日後至查詢營業日的每日異動。
3. 明細輔助：`inventory_record` 保留作為首次入庫日、最近來源單據與統計資料未涵蓋特定庫存列時的防護性補算依據。
4. 工程師最新回覆：第一版實作直接採用月結統計表計算。(`inventory_item_month_statistic` / `inventory_delta`)

建議演算法：

```txt
currentQuantity = monthEndQuantity + deltaInCount - deltaOutCount
inventoryValue = monthEndAmount + deltaInAmount - deltaOutAmount
```

最佳化後的補算觸發流程：

```txt
statisticResult = inventory_item_month_statistic + inventory_delta

if statisticResult is empty:
    return inventory_record aggregate result

if latestStatisticDate < queryDate and latestDeltaDate < queryDate:
    return inventory_record aggregate result

recordStockKeys = distinct warehouseNo + itemNo + batchNo from inventory_record
missingStockKeys = recordStockKeys - statisticResult.stockKeys

if missingStockKeys is not empty:
    append inventory_record aggregate result for missingStockKeys only

return statisticResult
```

注意：

- 正式第一版主路徑以 `inventory_item_month_statistic` 搭配 `inventory_delta` 為準。
- 正常資料完整時，不再同時完整計算 `inventory_record`；僅先查詢 `inventory_record` 的 distinct stock key，用於判斷是否有統計結果缺漏的庫存列。
- 若 `inventory_delta` 最新日期早於查詢營業日，例如查詢 2026/06/17 但 delta 僅到 2026/06/15，視為統計覆蓋不足，該次查詢改以 `inventory_record` 即時計算，避免少算缺漏日期。
- 若測試環境或過渡資料尚未建立統計表，或統計表只涵蓋部分料品/批號，程式會以 `warehouseNo + itemNo + batchNo` 作為庫存鍵，僅針對統計結果缺漏的庫存列使用 `inventory_record` 彙總補上。
- 防護性補算不得覆蓋已由月結統計表與每日異動產生且日期覆蓋完整的庫存列，以避免同一批號重複計算。
- 單位成本可由 `inventoryValue / currentQuantity` 推導；若需標準成本，可參考 `item_price.costPriceWeight`。

缺漏情境與處理策略：

| 情境 | 範例 | 處理策略 |
| --- | --- | --- |
| 無月結統計資料 | 查無 `inventory_item_month_statistic` | 改用 `inventory_record` 依查詢時間即時彙總。 |
| delta 日期落後 | 查詢 2026/06/17，但 `inventory_delta` 只到 2026/06/15 | 改用 `inventory_record` 依查詢時間即時彙總，確保 2026/06/16 至 2026/06/17 的異動被納入。 |
| 月結日期較舊但 delta 完整 | 月結到 2026/02/01 或 2026/05/01，delta 到 2026/06/17 | 使用月結加 delta，不需改用 `inventory_record`。 |
| 統計結果缺漏特定庫存列 | 某批號存在於 `inventory_record`，但不存在於統計結果 | 僅針對缺漏的 `warehouseNo + itemNo + batchNo` 使用 `inventory_record` 補算。 |
| 月結與 delta 交錯缺漏 | 部分批號有月結無 delta，部分批號有 delta 無月結 | 若 delta 整體日期覆蓋不足，改用 `inventory_record`；若日期覆蓋完整，統計結果缺漏的 stock key 才補算。 |
| 跨月份查詢 | 月結在 2026/05/01，查詢 2026/06/17 | delta 覆蓋到查詢日則使用統計路徑；delta 未覆蓋到查詢日則改用 `inventory_record`。 |
| 統計批次異常中斷 | 月結或 delta 更新程序中斷 | 以最新 delta 日期判斷覆蓋度；不足時改用 `inventory_record`，並應由排程監控另行告警。 |

共用封裝評估：

目前 `GET /api/v2/warehouse/dashboard` 與 `GET /api/v2/warehouse/inventory` 都會使用目前庫存快照計算；`valueTrend` / `trend7Days` 也需要同一套庫存快照或短區間即時計算邏輯。程式已新增 `CWarehouseInventorySnapshotCalculator`，集中處理「統計路徑、補算觸發、缺漏 stock key 補算、日期覆蓋檢查」等決策，避免 Dashboard、Inventory Detail 與 Trend 各自實作不同版本。

### Step 3：計算預留數量與預留價值

預留數量指「現有庫存已分配給特定業務需求，但尚未完成出庫或釋放」的數量。
品檢保留量則是「實體庫存已存在，但因品保未放行、異常或隔離而不可用」的數量。兩者都會扣減可用量，但來源、責任部門與解除條件不同。

建議新增來源：

```txt
warehouse_inventory_reservation
```

有效預留條件：

```txt
status = 有效
releaseTime is null or releaseTime > 查詢時間
```

演算法：

```txt
reservedQuantity = sum(reservedQuantity)
reservedValue = sum(reservedValue)
```

若 `reservedValue` 未保存：

```txt
reservedValue = reservedQuantity * unitCost
```

預留來源建議：

| refCategory | 來源 | 是否納入預留 |
| --- | --- | --- |
| 銷售/訂購 | `product_order`、`shipping_order` | 是，用於製成品出貨需求。 |
| 生產/工單 | `work_order`、`process_order` 領料需求 | 是，用於原料、物料、膠捲或半成品備料。 |
| 倉庫任務 | `inventory_order` 出庫或移倉 | 是，用於人工出庫或移倉前預留。 |
| 請購 | `purchase_request` | 否，請購是補貨需求，不佔用現有庫存。 |
| 採購 | `purchase_order` | 否，採購是未到貨供給，不佔用現有庫存。 |
| 進貨 | `goods_receipt_note` | 否，進貨完成後進入庫存或品檢保留，不作為預留來源。 |

### Step 4：計算品檢保留量與保留價值

品檢保留量只處理已到貨、已產出或已由倉庫隔離的實體庫存；尚未成為實體庫存的請購、採購、報價或訂購，不進入品檢保留。

建議新增來源：

```txt
warehouse_quality_hold
```

有效品檢保留條件：

```txt
status = 保留中
```

演算法：

```txt
qualityHoldQuantity = sum(holdQuantity)
qualityHoldValue = sum(holdValue)
```

若 `holdValue` 未保存：

```txt
qualityHoldValue = qualityHoldQuantity * unitCost
```

品檢保留來源建議：

| refCategory | 來源 | 是否納入品檢保留 |
| --- | --- | --- |
| 進貨 | `goods_receipt_note` | 是，用於材料到貨檢驗或隔離。 |
| 生產 | `process_order` 產品入庫、餘料、退料、廢料相關檢驗 | 是，用於產出或製程回庫後的品檢。 |
| 倉庫任務 | `inventory_order` 人工隔離或轉倉 | 是，用於倉庫發現異常後轉品檢。 |
| 請購/採購/報價/訂購 | `purchase_request`、`purchase_order`、`quotation`、`product_order` | 否，尚未形成需品檢保留的實體庫存。 |

### Step 5：計算可用數量與可用價值


演算法：

```txt
availableQuantity = currentQuantity - reservedQuantity - qualityHoldQuantity
availableValue = inventoryValue - reservedValue - qualityHoldValue
```

保護條件：

```txt
if availableQuantity < 0 then availableQuantity = 0
if availableValue < 0 then availableValue = 0
```

若預留或品檢資料尚未建置，第一版可以回傳：

```txt
reservedQuantity = 0
qualityHoldQuantity = 0
availableQuantity = currentQuantity
```

但必須在 runtime verification 註明限制。

### Step 6：計算佔用板數與可用板位

既有資料：

```txt
batchno_serialno_group.group
```

工程師回覆：目前只規劃棧板與批號對應關係，出入庫紀錄與棧板對應關係尚未規劃與實作。

建議新增來源：

```txt
warehouse_pallet_movement
ship_wh
ship_wh_contract
ship_wh_alias
```

演算法：

```txt
usedPallets = sum(palletCount where palletStatus = 佔用)
reservedPallets = sum(palletCount where palletStatus = 預留)
totalPallets = 透過啟用中的 ship_wh_contract 與 ship_wh_alias 取得 ship_wh.maxCapacity
availablePallets = totalPallets - usedPallets - reservedPallets
utilizationRate = usedPallets / totalPallets
```

注意：

1. 第一版優先使用 `ship_wh.maxCapacity` 作為容量來源。
2. 若自有倉沒有對應 `ship_wh_contract` 或 `ship_wh`，需由工程師確認既有資料是否會補齊；未確認前不新增 `warehouse_capacity`。

分類佔用板數：

```txt
categoryPalletCount = sum(palletCount group by itemCategory)
```

倉儲佔用板數：

```txt
warehousePalletCount = sum(palletCount group by warehouse_no)
```

### Step 7：計算安全水位風險

建議新增來源：

```txt
item_safety_stock
```

水位選擇規則：

1. 優先使用指定 `warehouse_no + item_no` 的安全水位。
2. 若沒有，使用 `item_no` 全倉通用安全水位。
3. 若仍沒有，不產生低於安全水位警示。

演算法：

```txt
if availableQuantity < safetyStock:
    riskType = BELOW_SAFETY_STOCK
```

注意：

- 低於安全水位需以 `availableQuantity` 判斷，而不是 `currentQuantity`。因為已預留或品檢保留的庫存雖然仍在倉內，但不可視為可立即使用。

### Step 8：計算效期風險

來源：

```txt
batch_number.validDays
batch_number.validDate
```

工程師回覆：物料、膠捲排除。

演算法：

```txt
remainingSeconds = validDate - queryTimestamp
oneThirdSeconds = validDays * 86400 / 3

if itemCategory not in (物料, 膠捲)
   and validDate > 0
   and remainingSeconds <= oneThirdSeconds:
       riskType = SHELF_LIFE_LT_ONE_THIRD
```

### Step 9：計算迴轉週期風險

來源：

```txt
inventory_record.date
```

演算法：

```txt
firstInboundTimestamp = min(inventory_record.date where category = IN group by warehouse_no, batchNumber)
daysInStock = floor((queryTimestamp - firstInboundTimestamp) / 86400)

if daysInStock > 30:
    riskType = TURNOVER_OVER_30_DAYS
```

### Step 10：產生風險訊息代碼與建議處理方式代碼

建議來源：

```txt
warehouse_risk_rule
```

後端回傳建議：

```json
{
  "riskType": "BELOW_SAFETY_STOCK",
  "messageCode": "warehouse.risk.belowSafetyStock",
  "messageParams": {
    "currentQuantity": 3200,
    "safetyStock": 6000
  },
  "recommendedActionCode": "warehouse.action.createPurchaseRequest"
}
```

多國語言原則：

1. 前端依 code 與 params 產生多語文字。
2. 後端不回傳 `message` 與 `recommendedAction` 繁中 fallback。

### Step 11：計算任務處理狀態


候選來源單據：

| 任務類型 | 來源 |
| --- | --- |
| 入庫 | `goods_receipt_note`、`process_order` 退料/餘料、廢料、產品入庫、`inventory_order` 入庫 |
| 出庫 | `shipping_order`、`process_order` 領料、`inventory_order` 出庫 |
| 移倉 | `inventory_order` 或後續移倉單 |

第一版 Warehouse dashboard 暫不處理盤點任務。

建議新增狀態表：

```txt
workflow_task_state
```

第一版任務狀態原則：

```txt
taskStatus 由各部門主管人工判斷與確認。
系統保存主管確認後的 taskStatus、ownerDepartment、blockReason、acceptedQuantity、rejectedQuantity、cancelledQuantity。
自動數量計算僅作為主管判斷時的參考資訊，不作為第一版自動結案依據。
```

參考計算：

```txt
processedQuantity = sum(inventory_record.count matched by ref_no, item_no, batchNumber, warehouse_no)
remainingQuantity = expectedQuantity - processedQuantity
```

Dashboard 待處理任務篩選：

```txt
taskStatus in (待處理, 部分完成, 阻塞)
and dueTimestamp <= queryBusinessDayEndTimestamp
```

參考結案資訊：

```txt
closedQuantity = acceptedQuantity + rejectedQuantity + cancelledQuantity
```

例如採購進貨預期 100，現場檢查後接受 90、拒收 10，雖然實際入庫數量小於預期數量，但主管可依差異分類結果人工確認任務是否轉為 `done`。

進貨單任務建立規則：

```txt
新增一筆 goods_receipt_note 時，系統可同時建立兩筆 workflow_task_state：

1. taskType = 進貨(3)
   - ref_no = goods_receipt_note.no
   - 用於處理到貨、驗收、數量分類與異常確認。

2. taskType = 入庫(4)
   - ref_no = goods_receipt_note.no
   - 用於處理入庫、上架、庫存紀錄、倉位與棧板關聯。
```

兩筆任務使用同一個來源單號，但 `taskId` 不同。若進貨需品檢，入庫任務可先維持 `pending` 或 `blocked`，待品保放行後再由倉庫主管人工確認完成。

### workflow_task_state 任務類型完成條件

第一版任務完成與否由各部門主管人工判斷；下表為主管判斷時的參考要點，不作為第一版自動結案規則。

| taskType | 主要來源 | 第一版人工判斷參考要點 | 常見下一步 |
| --- | --- | --- | --- |
| 請購(1) | `purchase_request` | 主管確認請購已核准、轉採購、取消或結案。 | 採購部建立採購單，或需求部門補資料。 |
| 採購(2) | `purchase_order` | 採購主管確認供應商、合約、交期與採購處理狀態。 | 採購部追供應商，或倉庫等待進貨。 |
| 進貨(3) | `goods_receipt_note` | 倉庫或品保主管確認到貨驗收、數量分類與異常處理狀態。 | 倉庫入庫或品保檢驗。 |
| 入庫(4) | `goods_receipt_note`、`process_order`、`inventory_order` | 倉庫主管確認入庫、上架、倉儲/批號/棧板關聯或差異結案。 | 倉庫完成上架，或品保處理未放行。 |
| 出庫(5) | `shipping_order`、`process_order`、`inventory_order` | 倉庫主管確認出庫、短出、取消或差異結案。 | 倉庫出庫，或業務/生管處理短缺。 |
| 移倉(6) | `inventory_order` | 倉庫主管確認來源倉移出與目的倉移入狀態。 | 倉庫完成移倉確認。 |
| 生產(7) | `work_order`、`process_order`、`production_data` | 製造或生管主管確認產出、領退餘廢、生產數據與差異處理狀態。 | 製造部補生產資料，或生管調整排程。 |
| 品檢(8) | 品檢單或 `warehouse_quality_hold` | 品保主管確認檢驗結果、放行、退回、報廢或異常結案。 | 品保部判定，或倉庫依判定入庫/退回/報廢。 |
| 出貨(9) | `shipping_order`、`shipping_record` | 業務或倉庫主管確認出貨、物流紀錄、短出、取消或結案。 | 業務確認交期/客戶資料，或倉庫安排出貨。 |

任務狀態判斷以 `workflow_task_state` 中主管人工確認的狀態為準。

### Step 12：判斷下一步負責部門

建議新增規則表：

```txt
workflow_next_owner_rule
```

`workflow_task_state.ownerDepartment` 保存任務目前的下一步負責部門；`workflow_next_owner_rule` 保存可重複使用的部門判斷規則。後端產生或更新任務時，先依規則表決定 owner，再寫入 `workflow_task_state.ownerDepartment`。

規則匹配順序：

```txt
1. 依 module + taskType + refCategory + taskStatus + blockReasonCode 精準匹配
2. 若無結果，放寬 blockReasonCode
3. 若無結果，放寬 refCategory
4. 若無結果，使用 taskType 預設規則
5. 若仍無結果，ownerDepartment = 來源單據目前負責部門或系統預設部門
```

建議初始規則：

| 條件 | ownerDepartment |
| --- | --- |
| 請購待核准或請購資料缺漏 | 生管部或需求提出部門 |
| 採購單待建立、供應商或合約資料缺漏 | 採購部 |
| 進貨到場待入庫 | 倉庫部 |
| 進貨需檢驗或檢驗異常 | 品保部 |
| 一般入庫、出庫、移倉待處理 | 倉庫部 |
| 品檢未放行、品檢保留、檢驗異常 | 品保部 |
| 工單備料不足、工單排程需調整 | 生管部 |
| 生產執行中或生產數據待補 | 製造部 |
| 銷售出貨資料缺漏或交期調整 | 業務部 |
| 採購入庫資料缺漏或供應商到貨問題 | 採購部 |
| 請購、採購、進貨、生產、訂購出貨跨流程任務 | 依 `workflow_task_state.ownerDepartment` 保存結果 |

樣本資料：

| no | module | taskType | refCategory | taskStatus | blockReasonCode | fromDepartment | ownerDepartment | rulePriority | comment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WONR-PR-001 | 生管(3) | 請購(1) | 請購(1) | 待處理(1) |  |  | 生管部(3) | 10 | 請購建立後由生管或需求主管確認。 |
| WONR-PO-001 | 採購(1) | 採購(2) | 採購(2) | 待處理(1) |  | 生管部(3) | 採購部(1) | 10 | 請購確認後交由採購建立或追蹤採購單。 |
| WONR-GRN-001 | 倉庫(5) | 進貨(3) | 進貨(3) | 待處理(1) |  | 採購部(1) | 倉庫部(5) | 10 | 進貨單建立後先由倉庫處理到貨驗收。 |
| WONR-GRN-002 | 品保(6) | 進貨(3) | 進貨(3) | 阻塞(4) | QUALITY_REQUIRED | 倉庫部(5) | 品保部(6) | 5 | 進貨需檢驗或檢驗異常時交由品保。 |
| WONR-IN-001 | 倉庫(5) | 入庫(4) | 進貨(3) | 待處理(1) |  | 品保部(6) | 倉庫部(5) | 10 | 進貨驗收或品保放行後由倉庫入庫上架。 |
| WONR-WO-001 | 生管(3) | 生產(7) | 工單(6) | 阻塞(4) | MATERIAL_SHORTAGE | 製造部(4) | 生管部(3) | 5 | 工單缺料或排程需調整時交由生管。 |
| WONR-QA-001 | 品保(6) | 品檢(8) | 進貨(3) | 待處理(1) |  | 倉庫部(5) | 品保部(6) | 10 | 材料到貨需檢驗時由品保判定。 |
| WONR-SHIP-001 | 業務(2) | 出貨(9) | 銷貨(5) | 阻塞(4) | CUSTOMER_OR_DATE_ISSUE | 倉庫部(5) | 業務部(2) | 5 | 出貨資料、客戶確認或交期異常交由業務。 |

更新流程：

```txt
if workflow_task_state.ownerDepartment exists and is manually assigned:
    keep existing ownerDepartment
else:
    ownerDepartment = match(workflow_next_owner_rule)
    update workflow_task_state.ownerDepartment
```

這樣可完整涵蓋「請購 -> 採購 -> 進貨 -> 產製 -> 訂購出貨」各環節，且 Warehouse dashboard 只需篩選與倉庫、品檢、出入庫相關的任務。

## Dashboard Response 組裝

建議組裝順序：

1. `summary`
2. `inventoryValueByCategory`
3. `capacityByWarehouse`
4. `riskAlerts`
5. `pendingTasks`
6. `valueTrend`
7. `inventory`，僅在 `includeInventory=true` 時回傳明細。

## 驗收條件

工程師 review 通過後，後續實作應能滿足：

1. `/api/v2/warehouse/dashboard` 可回傳管理者總覽資料。
2. 類別庫存量畫面不依賴單位顯示。
3. Enum 顯示文字由前端轉換。
4. 預留、可用、品檢保留、板數、安全水位、任務狀態皆有明確資料來源或明確 fallback。
5. 尚未實作的資料來源不得用假資料偽裝成正式值。
6. 第一版 Warehouse dashboard 不顯示盤點任務。
7. `workflow_task_state` 每個任務類型都有主管人工判斷參考要點。
8. `workflow_next_owner_rule` 可保存並套用下一步負責部門規則。
