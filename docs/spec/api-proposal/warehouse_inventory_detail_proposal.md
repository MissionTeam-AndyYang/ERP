# Warehouse Inventory Detail API Proposal

> Status: Proposal / Pending Engineer Review
> Target UI Preview: `docs/frontend/preview/warehouse_inventory_detail_static_preview.html`
> Flow / Algorithm: `docs/spec/api-proposal/warehouse_inventory_detail_flow_algorithm.md`
> Purpose: 承接 Warehouse Dashboard 的類別、風險警示與待處理任務點擊情境，提供「庫存明細與批號追蹤」畫面所需 API 規格提案。

## 工程師提問 V2

| 工程師提問 | 理解與回覆 | 提案文件更新 |
| --- | --- | --- |
| `/api/v2/warehouse/inventory/lots` 的 `payload.results[].lastSourceNo`、`payload.results[].lastSourceCategory` 是否應更名為 `refNo`、`refCategory`。 | 採用。此清單欄位描述的是批號來源單據，來源為 `batch_number.ref_no/refCategory`；使用 `refNo/refCategory` 可與資料庫命名一致，也避免與「最近異動」語意混淆。 | List API JSON 與 Field Description 已更名為 `payload.results[].refNo`、`payload.results[].refCategory`。 |
| Detail API 的 `payload.sourceDocuments[]` 是否應更名為 `payload.inventoryRecords[]`。 | 採用。此資料集實際來源為 `inventory_record`，內容是庫存入出異動紀錄，而非一般來源文件摘要；更名為 `inventoryRecords[]` 更貼近資料表與業務語意。 | Detail API JSON、Field Description 與 Processing Flow 已將 `sourceDocuments[]` 改為 `inventoryRecords[]`。 |
| 是否需要同時回傳 `quantity/amount` 絕對值與 `signedQuantity/signedAmount` 帶方向值；是否可改為只保留方向欄位搭配 `quantity/amount`。 | 採用工程師建議，移除 signed 欄位。第一版只回傳 `category` 與 `quantity/amount`，由前端在畫面呈現或統計時依 `category` 判斷入庫/出庫方向。這可降低 API 欄位重複與正負值不一致的風險。 | Detail API 已移除 `signedQuantity/signedAmount`；`direction` 更名為 `category`，來源為 `inventory_record.category`，enum 為 `EInventoryCategory`。 |
| Detail API 的 `payload.sourceDocuments[].direction` 是否應更名為 `payload.inventoryRecords[].category`。 | 採用。資料庫欄位本身為 `inventory_record.category`，用於表示入庫/出庫方向；文件以 `category` 命名可降低轉換層語意差異。 | Detail API 已改為 `payload.inventoryRecords[].category`，值定義為入庫(1)、出庫(2)。 |
| `payload.reservations[].refCategory/refNo` 的資料來源與 enum 定義需說明清楚。 | 採用。兩欄分別取自 `warehouse_inventory_reservation.refCategory/ref_no`；其 refCategory 值定義不是通用 `EInventoryRefCategory`，而是預留來源類別：銷售/訂購(1)、生產/工單(2)、倉庫任務(3)、其他(0)。 | `reservations[]` Field Description 已補上來源資料表與專屬 enum 說明。 |
| `payload.palletMovements[].refCategory/refNo` 的資料來源與 enum 定義需說明清楚。 | 採用。兩欄分別取自 `warehouse_pallet_movement.refCategory/ref_no`；其 refCategory 值定義是板位異動來源類別：入庫(1)、出庫(2)、移倉(3)、預留(4)、品檢保留(5)、釋放(6)。 | `palletMovements[]` Field Description 已補上來源資料表與專屬 enum 說明。 |

## 工程師建議與回覆

| 項目 | 工程師建議 | 工程師回覆 / 規格調整 |
| --- | --- | --- |
| Query enum 設計 | 請評估 `availability`、`sort`、`order` 欄位是否適合採用 ENUM；若改用 String，需說明可擴充性、跨語系顯示與前端對接考量。 | 採用 String + 後端白名單驗證。原因是這三個欄位是查詢控制參數，不需要回傳多國語言文字；前端可直接傳固定英文代碼，後端以 allow-list 驗證並拒絕未定義值。優點是 API 易讀、URL 友善、未來新增排序欄位時不需調整資料庫 enum；缺點是需在文件與後端驗證中維持同一份允許值。 |
| List response 結構 | `/api/v2/warehouse/inventory/lots` 的 Success Response Data 與 Field Description 不相符，需確認最終資料結構。 | 已以本文件 Success Response Data 為最終第一版結構，並補齊所有 `summary` 與 `results[]` 欄位說明。 |
| Detail response 欄位說明 | `/api/v2/warehouse/inventory/lots/{lotKey}` 遺漏 Field Description。 | 已調整 detail API 為階層化路徑 `/api/v2/warehouse/inventory/lots/wh/{warehouseNo}/item/{itemNo}/batch/{batchNo}`，並補齊 `lot`、`inventoryRecords`、`reservations`、`qualityHolds`、`palletMovements`、`workflowTasks` 欄位說明。 |
| lotKey 與路徑設計 | 建議採用階層化路徑，並評估是否仍需保留 `lotKey`。 | Detail API 採用階層化 path parameters 作為後端查詢入口，避免 `|` 組合字串在 URL encoding、路由與人工檢查上產生歧義。`lotKey` 保留在 list response 中，僅作前端 table row key / drill-down key，不作 detail API 必要查詢參數。 |

## 工程師提問

| 工程師提問 | 理解與回覆 | 提案文件更新 |
| --- | --- | --- |
| `lotKey` 是否使用組合字串，或後端需新增穩定 inventory lot id？ | 採用工程師建議的階層化路徑作為 detail API 查詢入口，避免 `|` 組合字串造成 URL encoding、路由解析與人工檢查上的歧義。`lotKey` 不作後端必要查詢參數，只保留作前端 row key。 | Detail API 改為 `GET /api/v2/warehouse/inventory/lots/wh/{warehouseNo}/item/{itemNo}/batch/{batchNo}`；list response 仍回傳 `lotKey`。 |
| `unitCost` 成本算法採用目前 `inventory_record.amount / count`，或需指定加權平均/批次成本？ | 採用工程師回覆：第一版以「總庫存價值 / 庫存數量」計算成本單價，並依數字規則取至小數點第 4 位。此算法可與共用庫存快照的 `inventoryValue/currentQuantity` 保持一致。 | `payload.results[].unitCost` 與 `payload.lot.unitCost` 欄位說明已明確寫入 `inventoryValue / currentQuantity`。 |
| `sourceDocuments` 第一版是否只顯示 `inventory_record.ref_no/refCategory`，或要 join 來源單據名稱？ | 採用工程師回覆：第一版只顯示 `inventory_record.ref_no/refCategory`，不 join 來源單據名稱，以降低查詢複雜度；來源名稱與來源明細待後續模組整合。V2 已將資料集命名調整為 `inventoryRecords[]`。 | `inventoryRecords[]` 欄位說明維持 `refCategory/refNo/refSubNo`，其中 `refSubNo` 第一版無穩定來源時回傳空字串。 |
| `quality_holds` 是否先使用 `warehouse_quality_hold`，未來再串接 Quality 模組檢驗單？ | 採用工程師回覆：第一版先使用 `warehouse_quality_hold` 作為品檢保留資料來源；Quality 模組檢驗單號若尚未串接，`inspectionNo` 可回傳空字串。 | `qualityHolds[]` 欄位說明已標示 `inspectionNo` 第一版可為空字串，資料集來源維持 `warehouse_quality_hold`。 |

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| `/api/v2/warehouse/inventory/lots` | GET | 查詢庫存批號明細清單 | Proposal / Pending Engineer Review | 供明細列表、篩選、排序、分頁與 Dashboard drill-down 使用。 |
| `/api/v2/warehouse/inventory/lots/wh/{warehouseNo}/item/{itemNo}/batch/{batchNo}` | GET | 查詢單一庫存批號追蹤明細 | Proposal / Pending Engineer Review | 供右側明細面板顯示來源、預留、品檢、板位、任務與風險。 |

## Planned Screen List And Naming

以下清單為目前 Warehouse 規劃中需要實作或已實作後需延伸整合的完整畫面範圍。後續討論、API 文件、工程任務與 commit message 應使用此處名稱，避免以「下一步畫面」或「明細畫面」等模糊說法替代。

| Screen Code | 正式畫面名稱 | Route / UI Location | Implementation Status | Primary API | 說明 |
| --- | --- | --- | --- | --- | --- |
| `WarehouseOverviewScreen` | 倉庫中心總覽 | `/warehouse` | 已有第一版，需持續整合 API | `GET /api/v2/warehouse/dashboard` | Warehouse 入口畫面，呈現 KPI、庫存價值分類、倉位容量、風險警示摘要與待處理任務摘要。 |
| `WarehouseInventoryLotListScreen` | 庫存批號明細清單 | 建議 route：`/warehouse/inventory/lots`；也可先嵌入 `/warehouse` 的「庫存明細」工作區 | 待實作 | `GET /api/v2/warehouse/inventory/lots` | 批號層級清單畫面，支援倉庫、料品類別、料號、批號、風險、任務、可用狀態、關鍵字、排序與分頁。 |
| `WarehouseInventoryLotDetailPanel` | 庫存批號追蹤面板 | `WarehouseInventoryLotListScreen` 右側 panel；窄版可作為 detail route 或 drawer | 待實作 | `GET /api/v2/warehouse/inventory/lots/wh/{warehouseNo}/item/{itemNo}/batch/{batchNo}` | 顯示單一批號的庫存摘要、入出庫紀錄、預留、品檢保留、板位異動、未完成任務與風險。 |

### Screen State Naming

以下項目是 `WarehouseInventoryLotListScreen` 的篩選狀態或入口情境，不是獨立畫面。文件與工程任務若提到這些名稱，應明確標示為 list state。

| State Code | 顯示名稱 | 所屬畫面 | 觸發來源 | API Query |
| --- | --- | --- | --- | --- |
| `RiskLotListState` | 風險批號清單狀態 | `WarehouseInventoryLotListScreen` | 從 `WarehouseOverviewScreen` 的風險警示或風險 tab drill-down | `riskType` / `riskOnly` 類條件 |
| `PendingTaskLotListState` | 待處理批號清單狀態 | `WarehouseInventoryLotListScreen` | 從 `WarehouseOverviewScreen` 的待處理入出庫 drill-down | `taskType` 或未完成任務條件 |
| `AvailableLotListState` | 可用庫存批號清單狀態 | `WarehouseInventoryLotListScreen` | 從庫存可用量、追溯或篩選器入口 | `availability=available` |
| `QualityHoldLotListState` | 品檢保留批號清單狀態 | `WarehouseInventoryLotListScreen` | 從品檢保留 KPI、篩選器或 detail drill-down | `availability=quality_hold` |

## Numeric Format Rules

| Numeric Meaning | Format |
|----------|----------|
| 單價 | 四捨五入取至小數點第 4 位 |
| 重量或數量 | 四捨五入取至小數點第 2 位 |
| 金額 | 四捨五入取整數 |

## Screen Intent

此畫面回答 Dashboard 無法完整展開的四個問題：

1. 指定類別、倉儲或批號目前有哪些庫存明細？
2. 該批庫存中，多少已預留、多少品檢保留、多少可用？
3. 該批庫存來自哪張進貨、工單或入庫紀錄，後續又被哪些出庫、工單或出貨任務使用？
4. 若該批庫存有風險，應由哪個部門下一步處理？

## GET /api/v2/warehouse/inventory/lots

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| `/api/v2/warehouse/inventory/lots` | GET | 查詢庫存批號明細清單 |

### Request Header

| Header | Description |
|----------|----------|
| `x-auth-token` | 存取金鑰 |
| `x-timezone` | 前端顯示時區；未提供時以 UTC 回傳 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| `date` | Integer | NO | 查詢基準時間，UTC timestamp；未提供時以伺服器目前時間計算 |
| `warehouse_no` | String | NO | 倉儲別名 no |
| `itemCategory` | Integer | NO | 料品品項類別；原料(1)、物料(2)、膠捲(3)、在製品(4)、製成品(5) |
| `item_no` | String | NO | 料品品項編號 |
| `batchNo` | String | NO | 批號 |
| `riskType` | String | NO | 風險類型；`TURNOVER_OVER_30_DAYS`、`SHELF_LIFE_LT_ONE_THIRD`、`BELOW_SAFETY_STOCK` |
| `taskType` | Integer | NO | 任務類型；請購(1)、採購(2)、進貨(3)、入庫(4)、出庫(5)、移倉(6)、生產(7)、品檢(8)、出貨(9) |
| `availability` | String | NO | 可用狀態代碼；後端以白名單驗證，允許值：`available`、`reserved`、`quality_hold`、`blocked` |
| `keyword` | String | NO | 模糊搜尋：料號、品名、批號、來源單號、倉儲名稱 |
| `sort` | String | NO | 排序欄位代碼；後端以白名單驗證，允許值：`inventoryValue`、`availableQuantity`、`validDate`、`daysInStock` |
| `order` | String | NO | 排序方向代碼；後端以白名單驗證，允許值：`asc`、`desc` |
| `start` | Integer | NO | 分頁起始位置 |
| `count` | Integer | NO | 分頁筆數；建議預設 50 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "timezone": "String",
    "total": "Integer",
    "count": "Integer",
    "start": "Integer",
    "summary": {
      "lotCount": "Integer",
      "itemCount": "Integer",
      "totalQuantity": "Float",
      "totalInventoryValue": "Integer",
      "totalAvailableQuantity": "Float",
      "totalAvailableValue": "Integer",
      "riskLotCount": "Integer",
      "pendingTaskCount": "Integer"
    },
    "results": [
      {
        "lotKey": "String",
        "warehouseNo": "String",
        "warehouseName": "String",
        "itemCategory": "Integer",
        "itemNo": "String",
        "itemName": "String",
        "batchNo": "String",
        "unit": "Integer",
        "currentQuantity": "Float",
        "reservedQuantity": "Float",
        "qualityHoldQuantity": "Float",
        "availableQuantity": "Float",
        "unitCost": "Float",
        "inventoryValue": "Integer",
        "reservedValue": "Integer",
        "qualityHoldValue": "Integer",
        "availableValue": "Integer",
        "palletCount": "Float",
        "firstInboundTimestamp": "Integer",
        "daysInStock": "Integer",
        "validDays": "Integer",
        "validDate": "Integer",
        "remainingShelfLifeRatio": "Float",
        "safetyStock": "Float",
        "riskTypes": ["String"],
        "openTaskCount": "Integer",
        "refNo": "String",
        "refCategory": "Integer"
      }
    ]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| `payload.serverTimestamp` | Integer | 後端產生資料的 UTC timestamp |  |
| `payload.timezone` | String | 本次查詢使用的時區；來源為 `x-timezone`，未提供時為 UTC |  |
| `payload.total` | Integer | 符合篩選條件且分頁前的總筆數 |  |
| `payload.count` | Integer | 本次回傳筆數 |  |
| `payload.start` | Integer | 本次分頁起始位置 |  |
| `payload.summary.lotCount` | Integer | 清單篩選條件下的批號庫存列數 |  |
| `payload.summary.itemCount` | Integer | 清單篩選條件下的不同料品品項數 |  |
| `payload.summary.totalQuantity` | Float | 清單篩選條件下的目前庫存量合計 | Unit |
| `payload.summary.totalInventoryValue` | Integer | 清單篩選條件下的庫存價值合計 |  |
| `payload.summary.totalAvailableQuantity` | Float | 清單篩選條件下的可用數量合計 | Unit |
| `payload.summary.totalAvailableValue` | Integer | 清單篩選條件下的可用價值合計 |  |
| `payload.summary.riskLotCount` | Integer | 清單篩選條件下命中任一風險類型的批號庫存列數 |  |
| `payload.summary.pendingTaskCount` | Integer | 清單篩選條件下未完成 workflow 任務數合計 |  |
| `payload.results[].lotKey` | String | 前端 drill-down 使用的批號庫存識別鍵；建議由 warehouseNo、itemNo、batchNo 組成穩定 key |  |
| `payload.results[].warehouseNo` | String | 倉儲別名 no |  |
| `payload.results[].warehouseName` | String | 倉儲別名名稱 |  |
| `payload.results[].itemCategory` | Integer | 料品品項類別；前端負責轉換顯示文字 | EItemCategory |
| `payload.results[].itemNo` | String | 料品品項編號 |  |
| `payload.results[].itemName` | String | 料品品項名稱 |  |
| `payload.results[].batchNo` | String | 批號 |  |
| `payload.results[].unit` | Integer | 庫存數量單位；前端負責轉換顯示文字 | Unit |
| `payload.results[].currentQuantity` | Float | 目前庫存量 | Unit |
| `payload.results[].reservedQuantity` | Float | 預留數量 | Unit |
| `payload.results[].qualityHoldQuantity` | Float | 品檢保留量 | Unit |
| `payload.results[].availableQuantity` | Float | 可用數量，計算方式為目前庫存量扣除預留數量與品檢保留量 | Unit |
| `payload.results[].unitCost` | Float | 此批庫存計價用單價，計算方式為 `inventoryValue / currentQuantity`，取至小數點第 4 位 |  |
| `payload.results[].inventoryValue` | Integer | 目前庫存價值 |  |
| `payload.results[].reservedValue` | Integer | 預留庫存價值 |  |
| `payload.results[].qualityHoldValue` | Integer | 品檢保留庫存價值 |  |
| `payload.results[].availableValue` | Integer | 可用庫存價值 |  |
| `payload.results[].palletCount` | Float | 此批庫存佔用板數 |  |
| `payload.results[].firstInboundTimestamp` | Integer | 此批庫存在此倉儲的首次入庫時間，UTC timestamp |  |
| `payload.results[].daysInStock` | Integer | 從首次入庫日至查詢日的庫存天數 |  |
| `payload.results[].validDays` | Integer | 批號有效天數；來源為 `batch_number.validDays` |  |
| `payload.results[].validDate` | Integer | 批號效期日，UTC timestamp；來源為 `batch_number.validDate` |  |
| `payload.results[].remainingShelfLifeRatio` | Float | 剩餘效期比例；物料與膠捲可回傳 0 或空值，由前端依類別忽略效期警示 |  |
| `payload.results[].safetyStock` | Float | 此料品於此倉儲或全倉通用的安全水位數量 |  |
| `payload.results[].riskTypes[]` | String | 此批庫存命中的風險類型 | EWarehouseRiskType |
| `payload.results[].openTaskCount` | Integer | 此批庫存尚未完成的 workflow 任務數 |  |
| `payload.results[].refNo` | String | 批號來源單號；來源為 `batch_number.ref_no` |  |
| `payload.results[].refCategory` | Integer | 批號來源類別；來源為 `batch_number.refCategory` | EInventoryRefCategory |

### Processing Flow

1. 讀取查詢條件與分頁條件，建立料品、倉儲、批號、風險、任務與可用狀態篩選。
2. 透過 `CWarehouseInventorySnapshotCalculator` 取得目前庫存快照；主路徑以 `inventory_item_month_statistic` 搭配 `inventory_delta` 補算目前庫存量與庫存價值，當統計資料缺漏或日期覆蓋不足時才由 `inventory_record` 防護性補算。
3. 過濾 `currentQuantity == 0` 的批號庫存列；`currentQuantity < 0` 視為資料異常但保留回傳，方便開發與測試階段追查。
4. 從 `batch_number` 補充有效天數、效期日與批號來源資料；`refNo/refCategory` 以 `batch_number.ref_no/refCategory` 為準。
5. 從 `warehouse_inventory_reservation` 彙總有效預留數量與預留價值。
6. 從 `warehouse_quality_hold` 彙總品檢保留量與品檢保留價值。
7. 從 `warehouse_pallet_movement` 彙總此批庫存佔用板數。
8. 從 `item_safety_stock` 判斷是否低於安全水位。
9. 從 `workflow_task_state` 彙總未完成任務數，並支援 `taskType` 篩選。
10. 套用風險判斷：迴轉超過 30 天、剩餘效期低於三分之一、低於安全水位。
11. 回傳 summary 與分頁後 results；所有 enum 顯示文字由前端轉換。

### Database Tables Used

| Table | Purpose |
|----------|------|
| `inventory_item_month_statistic` | 提供批號層級月結庫存量與庫存價值，作為目前庫存主計算基準 |
| `inventory_delta` | 提供月結日後每日入庫/出庫數量與金額異動，補算至查詢營業日 |
| `inventory_record` | 提供首次入庫時間；在統計資料缺漏或日期覆蓋不足時作為防護性補算依據；detail 時間線可用於列出來源與異動紀錄 |
| `batch_number` | 提供批號、效期與批號來源資訊；`refNo/refCategory` 以 `batch_number.ref_no/refCategory` 為準 |
| `warehouse_inventory_reservation` | 提供預留數量與預留價值 |
| `warehouse_quality_hold` | 提供品檢保留量與品檢保留價值 |
| `warehouse_pallet_movement` | 提供板位佔用狀態 |
| `item_safety_stock` | 提供安全水位 |
| `workflow_task_state` | 提供未完成任務與下一步負責部門 |
| `ship_wh_alias` | 提供倉儲別名與名稱 |

## GET /api/v2/warehouse/inventory/lots/wh/{warehouseNo}/item/{itemNo}/batch/{batchNo}

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| `/api/v2/warehouse/inventory/lots/wh/{warehouseNo}/item/{itemNo}/batch/{batchNo}` | GET | 查詢單一庫存批號追蹤明細 |

### Path Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| `warehouseNo` | String | YES | 倉儲別名 no |
| `itemNo` | String | YES | 料品品項編號 |
| `batchNo` | String | YES | 批號 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| `date` | Integer | NO | 查詢基準時間，UTC timestamp |

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "lot": {
      "lotKey": "String",
      "warehouseNo": "String",
      "warehouseName": "String",
      "itemCategory": "Integer",
      "itemNo": "String",
      "itemName": "String",
      "batchNo": "String",
      "unit": "Integer",
      "currentQuantity": "Float",
      "reservedQuantity": "Float",
      "qualityHoldQuantity": "Float",
      "availableQuantity": "Float",
      "unitCost": "Float",
      "inventoryValue": "Integer",
      "availableValue": "Integer",
      "palletCount": "Float",
      "validDate": "Integer",
      "riskTypes": ["String"]
    },
    "inventoryRecords": [
      {
        "refCategory": "Integer",
        "refNo": "String",
        "refSubNo": "String",
        "date": "Integer",
        "category": "Integer",
        "quantity": "Float",
        "amount": "Integer"
      }
    ],
    "reservations": [
      {
        "reservationNo": "String",
        "refCategory": "Integer",
        "refNo": "String",
        "reservedQuantity": "Float",
        "reservedValue": "Integer",
        "releaseTime": "Integer",
        "status": "Integer"
      }
    ],
    "qualityHolds": [
      {
        "holdNo": "String",
        "inspectionNo": "String",
        "holdQuantity": "Float",
        "holdValue": "Integer",
        "reason": "String",
        "status": "Integer"
      }
    ],
    "palletMovements": [
      {
        "movementNo": "String",
        "date": "Integer",
        "palletGroupNo": "String",
        "palletStatus": "Integer",
        "palletCount": "Float",
        "refCategory": "Integer",
        "refNo": "String"
      }
    ],
    "workflowTasks": [
      {
        "taskId": "String",
        "taskType": "Integer",
        "taskStatus": "Integer",
        "ownerDepartment": "Integer",
        "expectedQuantity": "Float",
        "processedQuantity": "Float",
        "remainingQuantity": "Float",
        "dueTimestamp": "Integer",
        "blockReason": "String"
      }
    ]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| `payload.lot.lotKey` | String | 前端 row key；由 warehouseNo、itemNo、batchNo 組成，僅供前端識別與選取狀態使用 |  |
| `payload.lot.warehouseNo` | String | 倉儲別名 no |  |
| `payload.lot.warehouseName` | String | 倉儲別名名稱 |  |
| `payload.lot.itemCategory` | Integer | 料品品項類別；前端負責轉換顯示文字 | EItemCategory |
| `payload.lot.itemNo` | String | 料品品項編號 |  |
| `payload.lot.itemName` | String | 料品品項名稱 |  |
| `payload.lot.batchNo` | String | 批號 |  |
| `payload.lot.unit` | Integer | 庫存數量單位；前端負責轉換顯示文字 | Unit |
| `payload.lot.currentQuantity` | Float | 目前庫存量；`0` 不回傳 detail，負數於開發階段保留以利 debug |  |
| `payload.lot.reservedQuantity` | Float | 有效預留數量 |  |
| `payload.lot.qualityHoldQuantity` | Float | 品檢保留數量 |  |
| `payload.lot.availableQuantity` | Float | 可用數量，計算方式為 `max(currentQuantity - reservedQuantity - qualityHoldQuantity, 0)` |  |
| `payload.lot.unitCost` | Float | 成本單價，計算方式為 `inventoryValue / currentQuantity`，單價取至小數點第 4 位 |  |
| `payload.lot.inventoryValue` | Integer | 目前庫存價值，金額四捨五入取整數 |  |
| `payload.lot.availableValue` | Integer | 可用庫存價值 |  |
| `payload.lot.palletCount` | Float | 此批庫存目前佔用板數 |  |
| `payload.lot.validDate` | Integer | 批號效期日，UTC timestamp |  |
| `payload.lot.riskTypes[]` | String | 此批庫存命中的風險類型 | EWarehouseRiskType |
| `payload.inventoryRecords[].refCategory` | Integer | 庫存異動來源單據類別；來源為 `inventory_record.refCategory` | EInventoryRefCategory |
| `payload.inventoryRecords[].refNo` | String | 庫存異動來源單號；來源為 `inventory_record.ref_no` |  |
| `payload.inventoryRecords[].refSubNo` | String | 庫存異動來源明細編號；第一版若無穩定來源則回傳空字串 |  |
| `payload.inventoryRecords[].date` | Integer | 庫存異動時間，UTC timestamp；來源為 `inventory_record.date` |  |
| `payload.inventoryRecords[].category` | Integer | 庫存異動類別；來源為 `inventory_record.category`，前端可依此判斷入庫或出庫方向 | EInventoryCategory：入庫(1)、出庫(2) |
| `payload.inventoryRecords[].quantity` | Float | 庫存異動數量；來源為 `inventory_record.count`，前端需帶方向統計時依 `category` 轉換 |  |
| `payload.inventoryRecords[].amount` | Integer | 庫存異動金額；來源為 `inventory_record.amount`，前端需帶方向統計時依 `category` 轉換 |  |
| `payload.reservations[].reservationNo` | String | 預留單識別碼 |  |
| `payload.reservations[].refCategory` | Integer | 預留來源類別；來源為 `warehouse_inventory_reservation.refCategory` | ReservationRefCategory：銷售/訂購(1)、生產/工單(2)、倉庫任務(3)、其他(0) |
| `payload.reservations[].refNo` | String | 預留來源單號；來源為 `warehouse_inventory_reservation.ref_no` |  |
| `payload.reservations[].reservedQuantity` | Float | 預留數量 |  |
| `payload.reservations[].reservedValue` | Integer | 預留庫存價值 |  |
| `payload.reservations[].releaseTime` | Integer | 預留釋放時間，UTC timestamp；無釋放時間可回傳 0 |  |
| `payload.reservations[].status` | Integer | 預留狀態 |  |
| `payload.qualityHolds[].holdNo` | String | 品檢保留識別碼 |  |
| `payload.qualityHolds[].inspectionNo` | String | 對應檢驗單號；第一版若尚未串接 Quality 模組可回傳空字串 |  |
| `payload.qualityHolds[].holdQuantity` | Float | 品檢保留數量 |  |
| `payload.qualityHolds[].holdValue` | Integer | 品檢保留庫存價值 |  |
| `payload.qualityHolds[].reason` | String | 品檢保留原因或備註 |  |
| `payload.qualityHolds[].status` | Integer | 品檢保留狀態 |  |
| `payload.palletMovements[].movementNo` | String | 板位異動識別碼 |  |
| `payload.palletMovements[].date` | Integer | 板位異動時間，UTC timestamp |  |
| `payload.palletMovements[].palletGroupNo` | String | 棧板或板位群組編號；若資料表未提供穩定欄位可回傳空字串 |  |
| `payload.palletMovements[].palletStatus` | Integer | 板位狀態 |  |
| `payload.palletMovements[].palletCount` | Float | 板數 |  |
| `payload.palletMovements[].refCategory` | Integer | 板位異動來源類別；來源為 `warehouse_pallet_movement.refCategory` | PalletMovementRefCategory：入庫(1)、出庫(2)、移倉(3)、預留(4)、品檢保留(5)、釋放(6) |
| `payload.palletMovements[].refNo` | String | 板位異動來源單號；來源為 `warehouse_pallet_movement.ref_no` |  |
| `payload.workflowTasks[].taskId` | String | workflow 任務識別碼 |  |
| `payload.workflowTasks[].taskType` | Integer | 任務類型 | EWorkflowTaskType |
| `payload.workflowTasks[].taskStatus` | Integer | 任務狀態；第一版僅回傳未完成任務 | EWorkflowTaskStatus |
| `payload.workflowTasks[].ownerDepartment` | Integer | 下一步負責部門；前端負責轉換顯示文字 | EDepartment |
| `payload.workflowTasks[].expectedQuantity` | Float | 預計處理數量 |  |
| `payload.workflowTasks[].processedQuantity` | Float | 已處理數量 |  |
| `payload.workflowTasks[].remainingQuantity` | Float | 剩餘待處理數量，計算方式為 `max(expectedQuantity - processedQuantity, 0)` |  |
| `payload.workflowTasks[].dueTimestamp` | Integer | 任務預計完成時間，UTC timestamp |  |
| `payload.workflowTasks[].blockReason` | String | 任務阻塞原因或主管人工判斷備註 |  |

### Processing Flow

1. 解析 path parameters，取得 warehouseNo、itemNo、batchNo。
2. 重新彙總該批庫存目前數量與價值，避免使用前端帶入的暫存值。
3. 查詢該批庫存異動紀錄，組成 `inventoryRecords`；`category=1` 表示入庫，`category=2` 表示出庫。API 不回傳 signed 欄位，前端若需帶方向統計，可依 `category` 搭配 `quantity/amount` 自行換算。
4. 查詢有效預留、品檢保留、板位異動與未完成 workflow 任務。
5. 回傳 enum code，不回傳多國語言顯示文字。

## Frontend Interaction Notes

| UI Action | API Usage |
|----------|----------|
| 從 Dashboard 點選某個料品類別 | 呼叫 list API，帶入 `itemCategory` |
| 從 Dashboard 點選風險警示 | 呼叫 list API，帶入 `riskType`；再選第一筆或使用者點選後呼叫 detail API |
| 從 Dashboard 點選待處理任務 | 呼叫 list API，帶入 `taskType` 或 `keyword=<來源單號>` |
| 使用者點選明細列 | 呼叫 detail API 顯示右側追蹤面板 |
| 使用者切換語系 | 前端依 enum code 轉換顯示文字，API 不需回傳翻譯字串 |
