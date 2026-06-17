# Warehouse API 欄位與邏輯檢視報告

日期：2026-06-17

## 檢視範圍

本次重新檢視下列文件與程式碼是否一致：

| 類別 | 檔案 |
| --- | --- |
| API proposal | `docs/spec/api-proposal/warehouse_overview_api.md` |
| Backend flow | `docs/engineering/WAREHOUSE_OVERVIEW_BACKEND_FLOW_ALGORITHM.md` |
| Formal API doc | `docs/spec/api/warehouse.md` |
| Backend code | `restserver/package/restserver/api/v2/warehouse.py` |
| Test | `restserver/tests/test_warehouse_dashboard.py` |

已檢視 API：

```txt
GET /api/v2/warehouse/dashboard
GET /api/v2/warehouse/inventory
GET /api/v2/warehouse/tasks
```

## 本次發現並已修正項目

| 項目 | 原狀態 | 修正結果 |
| --- | --- | --- | 
| 查詢營業日 | `range` 以 UTC 日切分，未依 `x-timezone` 換算。 | 已依 `x-timezone` 將 `date` 換算為本地營業日，再轉 UTC 起訖 timestamp。 |
| 目前庫存量與庫存價值 | `inventory_record` 彙總未限制查詢時間。 | 已只納入 `inventory_record.date <= queryTimestamp`。 |  
| 預留、品檢、板位 | 未排除查詢時間之後的資料。 | 已對 `warehouse_inventory_reservation.date`、`warehouse_quality_hold.date`、`warehouse_pallet_movement.date` 加上查詢時間限制。 |  
| 安全水位風險 | 使用 `currentQuantity < safetyStock`。 | 已改為 `availableQuantity < safetyStock`。 |   
| 風險文字 | 已移除 fallback，但需確認文件一致。 | 程式與文件皆改為只回傳 `messageCode`、`messageParams`、`recommendedActionCode`。 |   
| Dashboard 待處理任務 | 未依今日/逾期範圍限制。 | 已只回傳查詢營業日結束前仍未完成的任務。 |  
| 任務倉儲名稱 | `warehouseName` 固定空字串。 | 已由 `ship_wh_alias.name` 回填，查無才回傳空字串。 |  
| `riskOnly` | 參數未影響回傳。 | 聚合資料保持完整；若 `includeInventory=true`，`inventory` 只回傳有風險的列。 |  

## Dashboard 欄位檢視

### payload

| Field | 來源 / 計算 | 狀態 |
| --- | --- | --- |
| `serverTimestamp` | 查詢基準時間，未提供 `date` 時取伺服器目前時間。 | OK |
| `timezone` | request header `x-timezone`；未提供回傳 `UTC`。 | OK |
| `range.date` | 查詢基準時間依 `x-timezone` 換算後的本地日期。 | OK |
| `range.startTimestamp` | 本地營業日 00:00 轉 UTC timestamp。 | OK |
| `range.endTimestamp` | `startTimestamp + 86399`。 | OK |

### summary

| Field | 來源 / 計算 | 狀態 |
| --- | --- | --- |
| `totalInventoryValue` | `inventory_record.amount` 入庫加總減出庫加總，限制 `date <= queryTimestamp`。 | OK |
| `reservedInventoryValue` | 有效 `warehouse_inventory_reservation.reservedValue` 加總。 | OK |
| `availableInventoryValue` | `totalInventoryValue - reservedInventoryValue - qualityHoldInventoryValue`，低於 0 則回 0。 | OK |
| `qualityHoldInventoryValue` | 有效 `warehouse_quality_hold.holdValue` 加總。 | OK |
| `totalPallets` | `ship_wh_contract.category = 2` 關聯 `ship_wh.maxCapacity` 加總。 | OK |
| `usedPallets` | `warehouse_pallet_movement.palletStatus = 1` 加總。 | OK |
| `reservedPallets` | `warehouse_pallet_movement.palletStatus = 2` 加總。 | OK |
| `availablePallets` | `totalPallets - usedPallets - reservedPallets`，低於 0 則回 0。 | OK |
| `riskAlertCount` | `riskAlerts` 筆數。 | OK |
| `pendingInboundCount` | `pendingTasks` 中 taskType 為進貨或入庫的筆數。 | OK |
| `pendingOutboundCount` | `pendingTasks` 中 taskType 為出庫或出貨的筆數。 | OK |

### inventoryValueByCategory

| Field | 來源 / 計算 | 狀態 |
| --- | --- | --- |
| `itemCategory` | `inventory_record.itemCategory`，只統計原料、物料、膠捲、在製品、製成品。 | OK |
| `inventoryValue` | 同類別 `inventoryValue` 加總。 | OK |
| `reservedValue` | 同類別有效預留價值加總。 | OK |
| `availableValue` | `inventoryValue - reservedValue - qualityHoldValue`。 | OK |
| `qualityHoldValue` | 同類別品檢保留價值加總。 | OK |
| `quantity` | 同類別目前庫存量加總；混合單位時僅供參考。 | OK |
| `unit` | 類別彙總固定回傳 `0`，由前端不顯示單位。 | OK |
| `palletCount` | 同類別已佔用板數加總。 | OK |
| `itemCount` | 同類別 distinct `itemNo` 筆數。 | OK |
| `valueRatio` | `inventoryValue / totalInventoryValue * 100`。 | OK |
| `trend7Days` | 第一版保留欄位，固定回傳 `0.0`。 | Pending Future |

### capacityByWarehouse

| Field | 來源 / 計算 | 狀態 |
| --- | --- | --- |
| `warehouseNo` | `ship_wh_contract.sw_alias_no`。 | OK |
| `warehouseName` | `ship_wh_alias.name`。 | OK |
| `warehouseType` | `ship_wh_alias.type`。 | OK |
| `totalPallets` | `ship_wh.maxCapacity` 加總。 | OK |
| `usedPallets` | 同倉儲 `warehouse_pallet_movement.palletStatus = 1` 加總。 | OK |
| `reservedPallets` | 同倉儲 `warehouse_pallet_movement.palletStatus = 2` 加總。 | OK |
| `availablePallets` | `totalPallets - usedPallets - reservedPallets`。 | OK |
| `utilizationRate` | `usedPallets / totalPallets * 100`。 | OK |
| `riskLevel` | 使用率 >= 90 為危險，>= 75 為警示，其餘正常。 | OK |

### riskAlerts

| Field | 來源 / 計算 | 狀態 |
| --- | --- | --- |
| `alertId` | `riskType + warehouseNo + itemNo + batchNo` 組合。 | OK |
| `riskType` | 迴轉、效期、安全水位三類規則產生。 | OK |
| `riskLevel` | 優先 `warehouse_risk_rule.riskLevel`，缺漏時依風險類型 fallback。 | OK |
| `itemNo` / `itemName` / `itemCategory` | 庫存彙總列來源。 | OK |
| `batchNo` | `inventory_record.batchNumber`。 | OK |
| `warehouseNo` / `warehouseName` | `inventory_record.warehouse_no` / `warehouse_displayName`。 | OK |
| `quantity` | 目前庫存量。 | OK |
| `unit` | `inventory_record.unit`。 | OK |
| `inventoryValue` | 目前庫存價值。 | OK |
| `daysInStock` | `queryTimestamp - firstInboundTimestamp` 換算天數。 | OK |
| `validDate` | `batch_number.validDate`。 | OK |
| `remainingShelfLifeRatio` | `(validDate - queryTimestamp) / (validDays * 86400)`，低於 0 則 0。 | OK |
| `safetyStock` | 優先 `item_no + warehouse_no`，其次 `item_no` 全倉通用。 | OK |
| `messageCode` | 優先 `warehouse_risk_rule.messageCode`，缺漏時使用內建 code。 | OK |
| `messageParams` | currentQuantity、daysInStock、validDate、remainingShelfLifeRatio、safetyStock。 | OK |
| `recommendedActionCode` | 優先 `warehouse_risk_rule.recommendedActionCode`，缺漏時使用內建 code。 | OK |

### pendingTasks

| Field | 來源 / 計算 | 狀態 |
| --- | --- | --- |
| `taskId` | `workflow_task_state.taskId`。 | OK |
| `taskType` | `workflow_task_state.taskType`。 | OK |
| `refCategory` | `workflow_task_state.refCategory`。 | OK |
| `sourceNo` / `sourceSubNo` | `workflow_task_state.ref_no` / `ref_sub_no`。 | OK |
| `itemNo` / `itemName` / `itemCategory` | `workflow_task_state` 對應欄位。 | OK |
| `batchNo` | `workflow_task_state.batchNumber`。 | OK |
| `expectedQuantity` | `workflow_task_state.expectedQuantity`。 | OK |
| `processedQuantity` | `workflow_task_state.processedQuantity`。 | OK |
| `remainingQuantity` | `max(expectedQuantity - processedQuantity, 0)`。 | OK |
| `unit` | `workflow_task_state.unit`。 | OK |
| `palletCount` | `workflow_task_state.palletCount`。 | OK |
| `warehouseNo` | `workflow_task_state.warehouse_no`。 | OK |
| `warehouseName` | `ship_wh_alias.name`。 | OK |
| `dueTimestamp` | `workflow_task_state.dueTimestamp`。 | OK |
| `taskStatus` | `workflow_task_state.taskStatus`。 | OK |
| `ownerDepartment` | `workflow_task_state.ownerDepartment`。 | OK |
| `blockReason` | `workflow_task_state.blockReason`。 | OK |

### valueTrend / inventory

| Field | 來源 / 計算 | 狀態 |
| --- | --- | --- |
| `valueTrend` | 第一版保留空陣列。 | Pending Future |
| `inventory[]` | `includeInventory=true` 時回傳批號層級庫存明細；`riskOnly=true` 時只回傳有風險列。 | OK |

## Inventory API 欄位檢視

| Field | 來源 / 計算 | 狀態 |
| --- | --- | --- |
| `total` / `count` / `start` | 篩選後總筆數、本頁筆數、分頁起點。 | OK |
| `inventoryId` | `warehouseNo|itemNo|batchNo|serialNo` 組合。 | OK |
| `warehouseNo` / `warehouseName` | 庫存彙總列來源。 | OK |
| `itemNo` / `itemName` / `itemCategory` | 庫存彙總列來源。 | OK |
| `itemSubCategory` | 優先 `batch_number.itemSubCategory`，缺漏時依料品類別回查 `material / inproduct / product / goods`。 | OK |
| `itemType` | 優先 `batch_number.itemType`，缺漏時取 `inventory_record.itemType`。 | OK |
| `batchNo` / `serialNo` | 批號層級回傳 `batchNo`，`serialNo` 第一版為空字串。 | OK |
| `currentQuantity` | 查詢時間以前入庫減出庫。 | OK |
| `reservedQuantity` | 有效預留量。 | OK |
| `availableQuantity` | `currentQuantity - reservedQuantity - qualityHoldQuantity`。 | OK |
| `qualityHoldQuantity` | 有效品檢保留量。 | OK |
| `unit` | `inventory_record.unit`。 | OK |
| `unitCost` | `inventoryValue / currentQuantity`，取至小數點第 4 位。 | OK |
| `inventoryValue` | 查詢時間以前入庫金額減出庫金額。 | OK |
| `reservedValue` / `availableValue` / `qualityHoldValue` | 預留、可用、品檢保留價值。 | OK |
| `palletCount` | 查詢時間以前已佔用板數。 | OK |
| `safetyStock` | 對應風險資訊中的安全水位。 | OK |
| `validDays` / `validDate` | `batch_number`。 | OK |
| `firstInboundTimestamp` | 同倉儲、料品、批號最早入庫時間。 | OK |
| `daysInStock` | 查詢時間減首次入庫時間。 | OK |
| `sourceType` | 依最近一次入庫 `refCategory` 轉為穩定字串。 | Need Review |
| `sourceNo` | 查詢時間以前最近一次入庫 `inventory_record.ref_no`。 | OK |
| `sourceRefCategory` | 查詢時間以前最近一次入庫 `inventory_record.refCategory`。 | OK |
| `qualityStatus` | `qualityHoldQuantity > 0` 回 `hold`，否則 `released`。 | OK |
| `riskTypes` | 該庫存列命中的風險類型陣列。 | OK |

## Tasks API 欄位檢視

Tasks API 欄位來源與 Dashboard `pendingTasks` 相同；差異如下：

| 項目 | 說明 | 狀態 |
| --- | --- | --- |
| status filter | 若提供 `status`，依指定狀態查詢；未提供時預設 pending、partial、blocked。 | OK |
| date filter | 若提供 `date`，依 `x-timezone` 換算營業日，回傳該營業日結束前仍待處理的任務。 | OK |
| pagination | 先依 dueTimestamp 排序，再套用 start/count。 | OK |

## 仍需工程師確認

| 項目 | 說明 | 工程師回覆 |
| --- | --- | --- |
| 月結統計表使用時機 | 目前第一版實作以 `inventory_record` 直接彙總，符合正式 API 文件；`inventory_item_month_statistic` / `inventory_delta` 可作為後續效能優化或大量資料情境。 | 第一版實作直接採用月結統計表計算。(`inventory_item_month_statistic` / `inventory_delta`)|
| `sourceType` 對應 | 目前依 `refCategory` 簡化轉為 PURCHASE / SALE / WORK / OTHER，需工程師確認是否與所有來源單據 enum 完全一致。 |正確; <br>PURCHASE: 關聯至`goods_receipt_note`資料表 <br>SALE: 關聯至`shipping_order`資料表<br>WORK: 關聯至`process_order`資料表<br>OTHER: 關聯至`inventory_order`資料表|
| `valueTrend` / `trend7Days` | 目前為保留欄位，尚未計算。若前端第一版需要趨勢，需另訂資料來源與演算法。 |請規劃 資料來源 與 演算法設計，並撰寫對應的提案文件，提案文件放置docs\spec\api-proposal\下，以便工程師檢視。|
| 批號流水號層級 | 目前庫存明細為批號層級，`serialNo` 保留空字串；若需流水號層級，需擴充 group by 與資料集。 |請確認目前畫面是否已有呈現流水號層級。若已有呈現，則需進一步擴充至完整的流水號層級，並同步檢查程式邏輯與 API 文件是否一致|



## 驗證結果

已執行：

```txt
.\.venv\Scripts\python.exe -m py_compile restserver\package\restserver\api\v2\warehouse.py restserver\tests\test_warehouse_dashboard.py
.\.venv\Scripts\python.exe -m pytest restserver\tests\test_warehouse_dashboard.py
```

結果：

```txt
6 passed
```
