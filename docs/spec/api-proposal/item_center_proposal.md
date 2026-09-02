# 工程師提問V2
1. 請移除 bomRoleCode與unitShipping 欄位，該資訊目前規劃暫不顯示。
2. 建議將 masterTasks 欄位更名，以避免與 workflow task 混淆。
3. 請重新檢視回傳欄位，僅設計並保留目前畫面所需的欄位，其他暫不需要的欄位請先移除。

## 工程師回覆V2

| 項目 | 回覆與文件調整 |
|---|---|
| 移除 `bomRoleCode` | 已移除 dashboard 與 detail 回傳中的 `bomRoleCode`。第一版畫面只需要判斷是否有 BOM 關聯與 BOM 筆數；BOM 中的角色語意交由 `BOMCenterScreen` 或後續 detail 擴充處理。 |
| 移除 `unitShipping` | 已移除 `items[].unitShipping` 與 `item.unitShipping`。第一版品項中心僅保留目前畫面使用的 `unitWarehouse` 與 `unitProduct`。 |
| `masterTasks` 更名 | 已將 `masterTasks[]` 更名為 `maintenanceSuggestions[]`，明確表示此資料只是 read-only 主檔維護建議，不是 workflow task，也不代表部門轉交或待辦寫入。 |
| 欄位收斂 | 已重新檢視 Success Response Data 與 Field Description，移除目前畫面未顯示或容易造成誤解的欄位；保留 KPI、分類摘要、品項清單、單品明細、庫存摘要、BOM 使用清單、近期批號與維護建議所需欄位。 |

# 工程師提問
1. 請僅設計並保留目前畫面所需的欄位，其他暫不需要的欄位請先移除。
2. 針對 /api/v2/items/dashboard
   - 請說明 masterStatusCode 定義中 attention、missing_required_data的差異，並評估 summary.attentionItemCount 與 summary.missingRequiredDataCount  是否可整合為單一欄位。
   - 請確認 items[].latestBatchNo 與 items[].latestActivityTimestamp 是否為目前畫面所需欄位，若無使用請移除。
   - 請說明為何僅有料品品項資訊時，仍需建立 task 與設定下一步轉交部門。並請舉例說明 masterTasks 欄位在回傳時所包含的資料內容。   
3. 請詳細說明 bomRoleCode 各數值的定義。

## 工程師回覆

| 項目 | 回覆與文件調整 |
|---|---|
| 第一版欄位範圍 | 已依目前 `ItemCenterScreen` 畫面收斂欄位，只保留 KPI、分類摘要、品項卡片清單與右側主檔維護建議需要的資料。移除暫未使用的文件摘要、下一步負責部門、來源單據與處理期限等欄位。 |
| `attention` 與 `missing_required_data` | 第一版不再拆成兩個 `masterStatusCode`。兩者本質皆為「主檔待維護」訊號，只是風險原因不同；因此整合為 `masterStatusCode=maintenance_needed`，並以 `maintenanceRiskCode` 表示原因，例如 `missing_unit`、`missing_bom`、`missing_stock_signal`。 |
| `summary.attentionItemCount` 與 `summary.missingRequiredDataCount` | 已整合為單一欄位 `summary.maintenanceItemCount`，對應畫面 KPI「待維護」。 |
| `items[].latestBatchNo`、`items[].latestActivityTimestamp` | 目前畫面未直接使用，已自 dashboard API 移除。若後續需要近期批號或活動時間，應由批號中心或品項 detail 延伸欄位再行規劃。 |
| `masterTasks` 定位 | 第一版不建立 workflow task，也不回傳下一步轉交部門。依工程師提問 V2，原 `masterTasks[]` 已更名為 `maintenanceSuggestions[]`，僅作為 read-only UI 維護建議。 |
| `bomRoleCode` 定義 | 依工程師提問 V2，第一版畫面暫不顯示 BOM 角色，因此已移除 `bomRoleCode` 與其 enum 詳細說明。 |

# ItemCenterScreen API 提案

> Status: Engineer Confirmed / Backend API Implemented / Pending Engineer Runtime Review  
> Screen: `ItemCenterScreen`  
> Route: `/items`  
> Scope: V1 read-only Core  
> Design basis: `AGENTS.md`、`src/app/items/page.tsx`、`docs/frontend/ERP_ITEMS_API_FIELD_READINESS_20260526.md`、`docs/spec/database/index.md`

## 1. 畫面定位

「品項中心」第一版定位為料品主資料 read-only 工作區，協助管理者快速確認原料、物料、膠捲、在製品、製成品與貨品的主檔完整度、庫存訊號、BOM 關聯與主檔維護建議。

此畫面不取代 `WarehouseOverviewScreen`、`BatchCenterScreen`、`BOMCenterScreen` 或 `RDCostWorkspaceScreen`：

| 畫面 | 主視角 | 本版邊界 |
|---|---|---|
| `ItemCenterScreen` | 料品主資料、主檔完整度、BOM/批號/庫存摘要 | 檢視料品是否可被採購、生產、倉庫與研發流程正確引用。 |
| `BatchCenterScreen` | 料品 -> 批號 -> 倉庫分布 | 批號可用性、效期、品檢保留與批號層級任務。 |
| `BOMCenterScreen` | BOM 版本與配方明細 | BOM 版本、有效日期、配方與產品版本關聯。 |
| `RDCostWorkspaceScreen` | 研發成本與報價基礎 | 成本試算、報價與合約基礎。 |

第一版不提供 POST、PUT、DELETE，不建立或修改料品主檔。後端只回傳 enum code、數值與資料庫欄位；顯示文字與多國語言由前端處理。

## 2. V1 API 清單

| API | Method | 用途 |
|---|---|---|
| `/api/v2/items/dashboard` | GET | 查詢品項中心 KPI、分類摘要、品項清單與主檔待維護事項。 |
| `/api/v2/items/{item_no}/detail` | GET | 查詢單一品項主檔、庫存摘要、批號摘要、BOM 使用情形與主檔維護建議。 |

> 工程師確認前，本文件為 API 提案；確認後才整合至 `docs/spec/api/` 正式 API 文件並進行後端實作。

## 3. 共用 Query Parameters / Header

| Parameter / Header | Type | Required | Description |
|---|---|---:|---|
| `keyword` | String | No | 料品 no、料品名稱、BOM no、批號、供應商或備註關鍵字。 |
| `itemCategory` | Integer | No | 料品品項類別 code。 |
| `itemSubCategory` | Integer | No | 料品品項子類別 code。 |
| `masterStatusCode` | String | No | 主檔狀態 code；第一版支援 `ready`、`maintenance_needed`、`unknown`。 |
| `hasStock` | Boolean | No | 是否只查詢目前仍有庫存的料品。 |
| `hasBom` | Boolean | No | 是否只查詢已關聯 BOM 或被 BOM 使用的料品。 |
| `start` | Integer | No | 分頁起點，預設 0；負值視為 0。 |
| `count` | Integer | No | 回傳筆數，預設 50，最大 100。 |
| `x-timezone` | Header String | No | 前端顯示偏好的 IANA timezone；後端不改寫資料庫 UTC timestamp。 |

## 4. GET `/api/v2/items/dashboard`

### 4.1 Success Response Data

```json
{
  "serverTimestamp": "Integer",
  "summary": {
    "totalItemCount": "Integer",
    "activeItemCount": "Integer",
    "finishedGoodsCount": "Integer",
    "maintenanceItemCount": "Integer"
  },
  "categorySummary": [
    {
      "itemCategory": "Integer",
      "itemCount": "Integer",
      "stockItemCount": "Integer",
      "bomLinkedItemCount": "Integer",
      "maintenanceItemCount": "Integer"
    }
  ],
  "items": [
    {
      "itemNo": "String",
      "itemName": "String",
      "itemCategory": "Integer",
      "itemSubCategory": "Integer",
      "unitWarehouse": "Integer",
      "unitProduct": "Integer",
      "masterStatusCode": "String",
      "maintenanceRiskCode": "String",
      "hasStock": "Boolean",
      "currentQuantity": "Float",
      "batchCount": "Integer",
      "bomCount": "Integer"
    }
  ],
  "maintenanceSuggestions": [
    {
      "suggestionId": "String",
      "itemNo": "String",
      "suggestionTypeCode": "String",
      "riskLevelCode": "String"
    }
  ],
  "total": "Integer",
  "start": "Integer",
  "count": "Integer"
}
```

### 4.2 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `serverTimestamp` | Integer | API 回應建立時間，UTC timestamp。 | 系統時間 |
| `summary.totalItemCount` | Integer | 套用篩選前可納入品項中心的料品總數。 | `material`、`inproduct`、`product`、`goods` |
| `summary.activeItemCount` | Integer | 主檔可被業務流程引用的料品數；若現有資料表無停用欄位，第一版以可查得主檔者視為 active。 | 主檔彙總 |
| `summary.finishedGoodsCount` | Integer | `itemCategory=5` 的製成品數。 | `product` |
| `summary.maintenanceItemCount` | Integer | `masterStatusCode=maintenance_needed` 的料品數，對應畫面 KPI「待維護」。 | 後端規則 |
| `categorySummary[].itemCategory` | Integer | 料品品項類別 code。 | `EItemCategory` |
| `categorySummary[].itemCount` | Integer | 此品項類別的料品數。 | 主檔彙總 |
| `categorySummary[].stockItemCount` | Integer | 此品項類別目前仍有庫存的料品數。 | Warehouse 輕量品項庫存摘要共用邏輯 |
| `categorySummary[].bomLinkedItemCount` | Integer | 此品項類別已與 BOM 或產品規格建立關聯的料品數。 | `bom_item`、`product_spec`、`product_bom_spec`、`inproduct_bom_spec` |
| `categorySummary[].maintenanceItemCount` | Integer | 此品項類別需要維護的料品數，計算來源為 `masterStatusCode=maintenance_needed`。 | 後端規則 |
| `items[].itemNo` | String | 料品 no。 | 各料品主檔 |
| `items[].itemName` | String | 料品名稱。 | 各料品主檔 |
| `items[].itemCategory` | Integer | 料品品項類別 code。 | `EItemCategory` |
| `items[].itemSubCategory` | Integer | 料品品項子類別 code；主檔無此欄位時回傳 0。 | 各料品主檔 |
| `items[].unitWarehouse` | Integer | 倉庫庫存單位 code；前端負責顯示文字。 | 各料品主檔 |
| `items[].unitProduct` | Integer | 生產用量單位 code；前端負責顯示文字。 | 各料品主檔 |
| `items[].masterStatusCode` | String | 主檔狀態 code。 | ready、maintenance_needed、unknown |
| `items[].maintenanceRiskCode` | String | 主檔主要維護風險 code。 | normal、missing_unit、missing_bom、missing_stock_signal、unknown |
| `items[].hasStock` | Boolean | 此料品目前是否仍有庫存量大於 0。 | Warehouse 輕量品項庫存摘要共用邏輯 |
| `items[].currentQuantity` | Float | 此料品目前庫存數量總和，取至小數點第 2 位；混合單位風險由前端以單位 code 輔助呈現。 | Warehouse 輕量品項庫存摘要共用邏輯 |
| `items[].batchCount` | Integer | 此料品目前仍有庫存或近期建立的不重複批號數。 | `batch_number`、庫存快照 |
| `items[].bomCount` | Integer | 此料品已關聯或被使用的 BOM / 產品規格數。 | BOM 相關資料表 |
| `maintenanceSuggestions[].suggestionId` | String | 主檔維護建議識別值，供前端列表 key 使用；此欄位不是 workflow task id。 | 後端組合 |
| `maintenanceSuggestions[].itemNo` | String | 維護建議對應料品 no。 | 後端規則 |
| `maintenanceSuggestions[].suggestionTypeCode` | String | 維護建議類型 code。 | missing_unit、missing_bom、missing_stock_signal |
| `maintenanceSuggestions[].riskLevelCode` | String | 維護建議風險等級 code。 | normal、attention、high_risk |
| `total` | Integer | 套用篩選後的料品筆數。 |  |
| `start` | Integer | 本次分頁起點。 |  |
| `count` | Integer | 本次回傳筆數。 |  |

## 5. GET `/api/v2/items/{item_no}/detail`

### 5.1 Success Response Data

```json
{
  "serverTimestamp": "Integer",
  "item": {
    "itemNo": "String",
    "itemName": "String",
    "itemCategory": "Integer",
    "itemSubCategory": "Integer",
    "unitWarehouse": "Integer",
    "unitProduct": "Integer",
    "masterStatusCode": "String",
    "maintenanceRiskCode": "String",
    "creationTime": "Integer"
  },
  "inventorySummary": {
    "hasStock": "Boolean",
    "currentQuantity": "Float",
    "availableQuantity": "Float",
    "reservedQuantity": "Float",
    "qualityHoldQuantity": "Float",
    "warehouseCount": "Integer",
    "batchCount": "Integer"
  },
  "bomUsage": [
    {
      "bomNo": "String",
      "bomVersion": "Integer",
      "quantity": "Float",
      "unit": "Integer",
      "effectiveTimestamp": "Integer"
    }
  ],
  "recentBatches": [
    {
      "batchNo": "String",
      "refCategory": "Integer",
      "refNo": "String",
      "currentQuantity": "Float",
      "unit": "Integer",
      "validDate": "Integer",
      "riskLevelCode": "String"
    }
  ],
  "maintenanceSuggestions": [
    {
      "suggestionId": "String",
      "suggestionTypeCode": "String",
      "riskLevelCode": "String"
    }
  ]
}
```

### 5.2 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `serverTimestamp` | Integer | API 回應建立時間，UTC timestamp。 | 系統時間 |
| `item.itemNo` | String | 查詢料品 no。 | 各料品主檔 |
| `item.itemName` | String | 料品名稱。 | 各料品主檔 |
| `item.itemCategory` | Integer | 料品品項類別 code。 | `EItemCategory` |
| `item.itemSubCategory` | Integer | 料品品項子類別 code；主檔無此欄位時回傳 0。 | 各料品主檔 |
| `item.unitWarehouse` | Integer | 倉庫庫存單位 code。 | 各料品主檔 |
| `item.unitProduct` | Integer | 生產用量單位 code。 | 各料品主檔 |
| `item.masterStatusCode` | String | 主檔狀態 code。 | ready、maintenance_needed、unknown |
| `item.maintenanceRiskCode` | String | 主檔主要維護風險 code。 | normal、missing_unit、missing_bom、missing_stock_signal、unknown |
| `item.creationTime` | Integer | 主檔建立時間 UTC timestamp；無資料時回傳 0。 | 各料品主檔 |
| `inventorySummary.hasStock` | Boolean | 此料品目前是否仍有庫存量大於 0。 | Warehouse 輕量品項庫存摘要共用邏輯 |
| `inventorySummary.currentQuantity` | Float | 此料品目前庫存數量總和，取至小數點第 2 位。 | Warehouse 輕量品項庫存摘要共用邏輯 |
| `inventorySummary.availableQuantity` | Float | 此料品目前可用數量總和。 | Warehouse 輕量品項庫存摘要共用邏輯 |
| `inventorySummary.reservedQuantity` | Float | 此料品目前預留數量總和。 | Warehouse 輕量品項庫存摘要共用邏輯 |
| `inventorySummary.qualityHoldQuantity` | Float | 此料品目前品檢保留數量總和。 | Warehouse 輕量品項庫存摘要共用邏輯 |
| `inventorySummary.warehouseCount` | Integer | 此料品目前庫存所在的不重複倉庫數。 | Warehouse 輕量品項庫存摘要共用邏輯 |
| `inventorySummary.batchCount` | Integer | 此料品目前仍有庫存的不重複批號數。 | Warehouse 輕量品項庫存摘要共用邏輯 |
| `bomUsage[].bomNo` | String | 關聯 BOM no。 | BOM 相關資料表 |
| `bomUsage[].bomVersion` | Integer | 關聯 BOM 版本。 | BOM 相關資料表 |
| `bomUsage[].quantity` | Float | 此 BOM 關聯用量，取至小數點第 2 位。 | BOM 相關資料表 |
| `bomUsage[].unit` | Integer | 此 BOM 關聯單位 code。 | BOM 相關資料表 |
| `bomUsage[].effectiveTimestamp` | Integer | BOM 版本有效日期 UTC timestamp；無資料時回傳 0。 | `bom.date` |
| `recentBatches[].batchNo` | String | 此料品近期批號。 | `batch_number.no` |
| `recentBatches[].refCategory` | Integer | 批號來源單據類別。 | `batch_number.refCategory` |
| `recentBatches[].refNo` | String | 批號來源單號。 | `batch_number.ref_no` |
| `recentBatches[].currentQuantity` | Float | 此批號目前庫存數量，取至小數點第 2 位。 | Warehouse 輕量品項庫存摘要共用邏輯 |
| `recentBatches[].unit` | Integer | 批號單位 code。 | `batch_number.unit` |
| `recentBatches[].validDate` | Integer | 批號有效期限 UTC timestamp。 | `batch_number.validDate` |
| `recentBatches[].riskLevelCode` | String | 批號風險等級 code。 | normal、attention、high_risk |
| `maintenanceSuggestions[].suggestionId` | String | 主檔維護建議識別值；此欄位不是 workflow task id。 | 後端組合 |
| `maintenanceSuggestions[].suggestionTypeCode` | String | 維護建議類型 code。 | missing_unit、missing_bom、missing_stock_signal |
| `maintenanceSuggestions[].riskLevelCode` | String | 維護建議風險等級 code。 | normal、attention、high_risk |

## 6. Enum 建議

| Enum | Values |
|---|---|
| `masterStatusCode` | `ready`、`maintenance_needed`、`unknown` |
| `maintenanceRiskCode` | `normal`、`missing_unit`、`missing_bom`、`missing_stock_signal`、`unknown` |
| `suggestionTypeCode` | `missing_unit`、`missing_bom`、`missing_stock_signal` |

## 7. Database Tables Used

| Table | Purpose |
|---|---|
| `material` | 原料、物料、膠捲主檔 |
| `inproduct` | 在製品主檔 |
| `product` | 製成品主檔 |
| `goods` | 貨品主檔 |
| `batch_number` | 料品近期批號、來源單據與效期 |
| `inventory_record` | Warehouse 輕量品項庫存摘要共用邏輯使用的庫存異動來源 |
| `warehouse_inventory_reservation` | Warehouse 輕量品項庫存摘要共用邏輯使用的預留數量來源 |
| `warehouse_quality_hold` | Warehouse 輕量品項庫存摘要共用邏輯使用的品檢保留數量來源 |
| `bom` | BOM 版本與有效日期 |
| `bom_item` | BOM 直接配方明細 |
| `product_spec` | 製成品與 BOM / 料品規格關聯 |
| `product_bom_spec` | 製成品 BOM 階層關聯 |
| `inproduct_bom_spec` | 在製品 BOM 關聯 |

## 8. 備註

1. 第一版 `items[]` 應以資料表可確認的主檔資料為準，不推測不存在的品項。
2. 若 `material.category` 對應 `EItemCategory.PM / MA / AF`，後端需保持原始 code；中文類別名稱由前端轉換。
3. `hasStock`、`currentQuantity`、`batchCount` 應使用 Warehouse 輕量品項庫存摘要共用邏輯，避免為品項中心查詢建立完整 Warehouse Dashboard payload。
4. `maintenanceSuggestions[]` 是後端依缺漏規則產生的 read-only 維護建議，不代表 workflow task 寫入、待辦建立或部門轉交。
5. 現有主檔停用／啟用功能第一版暫不規劃，因此本版不回傳 `inactive` 狀態；若後續新增停用欄位，再另行擴充 enum 與查詢條件。
