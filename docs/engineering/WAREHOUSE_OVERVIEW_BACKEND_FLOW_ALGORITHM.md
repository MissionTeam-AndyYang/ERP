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
2. 若資料表有 `timezone` 欄位，`date` 代表使用者端日期，並搭配 `timezone` 解讀。
3. API 接收 `date` 與 `timezone` 後，需換算為本地營業日的 UTC 起訖時間。
4. 回傳給前端時，timestamp 保持 UTC timestamp；顯示格式由前端依語系與時區轉換。

## Enum 與多國語言規則

1. 後端回傳 enum code 或穩定 code，例如 `itemCategory = 1`、`riskType = TURNOVER_OVER_30_DAYS`。
2. 前端負責 enum 到多國語言字串的轉換，例如 `1 -> 原料`。
3. 後端可回傳 `messageCode`、`recommendedActionCode` 與參數，前端依語系組成顯示文字。
4. 若第一版需要快速展示，可同時回傳繁中 fallback `message` 與 `recommendedAction`，但不得把它視為唯一語系來源。

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

1. 月底基準：`inventory_item_month_statistic` 或 `inventory_month_statistic`。
2. 月底後異動：`inventory_delta`。
3. 即時明細或補算：`inventory_record`。
4. 工程師回覆：庫存價值以 `inventory_record.amount` 為準。

建議演算法：

```txt
currentQuantity = monthEndQuantity + deltaInCount - deltaOutCount
inventoryValue = monthEndAmount + deltaInAmount - deltaOutAmount
```

若查詢需批號或明細層級：

```txt
currentQuantity = sum(inventory_record.count where category = IN)
                - sum(inventory_record.count where category = OUT)

inventoryValue = sum(inventory_record.amount where category = IN)
               - sum(inventory_record.amount where category = OUT)
```

注意：

- 若統計表與即時計算不同步，需以 `inventory_record` 補算到查詢時間。
- 單位成本可由 `inventoryValue / currentQuantity` 推導；若需標準成本，可參考 `item_price.costPriceWeight`。

### Step 3：計算預留數量與預留價值

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

| sourceType | 來源 |
| --- | --- |
| 銷售 | 銷售訂單、出貨需求。 |
| 生產 | 工單備料、領料需求。 |
| 倉庫任務 | 待出庫、移倉、盤點保留。 |

### Step 4：計算品檢保留量與保留價值

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
warehouse_capacity
```

演算法：

```txt
usedPallets = sum(palletCount where palletStatus = 佔用)
reservedPallets = sum(palletCount where palletStatus = 預留)
totalPallets = warehouse_capacity.totalPallets where status = 啟用
availablePallets = totalPallets - usedPallets - reservedPallets
utilizationRate = usedPallets / totalPallets
```

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

### Step 10：產生風險說明文字與建議處理方式

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
  "recommendedActionCode": "warehouse.action.createPurchaseRequest",
  "message": "目前可用量低於安全水位。",
  "recommendedAction": "建議建立請購或確認已下採購單。"
}
```

多國語言原則：

1. 前端依 code 與 params 產生多語文字。
2. 後端 `message` 與 `recommendedAction` 作為繁中 fallback。

### Step 11：計算任務處理狀態


候選來源單據：

| 任務類型 | 來源 |
| --- | --- |
| 入庫 | `goods_receipt_note`、`process_order` 退料/餘料、廢料、產品入庫、`inventory_order` 入庫 |
| 出庫 | `shipping_order`、`process_order` 領料、`inventory_order` 出庫 |
| 移倉 | `inventory_order` 或後續移倉單 |
| 盤點 | `inventory_order` 或後續盤點單 |

建議新增狀態表：

```txt
warehouse_task_state
```

演算法：

```txt
processedQuantity = sum(inventory_record.count matched by source_no, item_no, batchNumber, warehouse_no)
remainingQuantity = expectedQuantity - processedQuantity

if blockReason exists:
    status = blocked
else if processedQuantity <= 0:
    status = pending
else if processedQuantity < expectedQuantity:
    status = partial
else:
    status = done
```

### Step 12：判斷下一步負責部門

建議規則：

| 條件 | ownerDepartment |
| --- | --- |
| 一般入庫、出庫、移倉、盤點待處理 | 倉庫部 |
| 品檢未放行、品檢保留、檢驗異常 | 品保部 |
| 工單備料不足、工單排程需調整 | 生管部 |
| 銷售出貨資料缺漏或交期調整 | 業務部 |
| 採購入庫資料缺漏或供應商到貨問題 | 採購部 |

若 `warehouse_task_state.ownerDepartment` 已存在，以人工/狀態表設定為準；否則依規則即時計算。

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
