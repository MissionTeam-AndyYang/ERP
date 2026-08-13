# 工程師提問
1. 品檢保留量與隔離量在定義上有何差異？是否可簡化設計，僅保留其中一種方式？
2. 針對 /api/v2/batches/dashboard
   - summary.managedItemCount 更名為 stockItemCount；
summary.distributedBatchCount 更名為 stockBatchCount。
變數名稱請採用易懂且語意相近的命名方式，以提升可讀性與一致性。
   - items[].highestRiskLevelCode 更名為 items[].riskLevelCode ； items[].primaryRiskCode 更名為 items[].riskCode
   - items[].demandSignals[] 目前規劃設計的畫面是否會使用到？若未使用，請先移除該欄位。
3. 針對 /api/v2/batches/items/{item_no}/distribution
   - 若同一批號的部分數量位於倉庫，另一部分處於產製中，batches[].batchStageCode 應如何顯示？
   - 請舉例說明 batches[].sourceRefCategory / batches[].sourceNo 與 batches[].relatedDocuments[].documentTypeCode / batches[].relatedDocuments[].documentNo 在批號來源單據與關聯單據上的差異。
4. 針對 /api/v2/batches/{batch_no}/detail
   - inventoryRecords[].movementCategory 更名為  inventoryRecords[].category ; inventoryRecords[].movementSource 更名為  inventoryRecords[].source
5. 若欄位描述涉及來源單據或關聯訂單類，參數名稱建議統一命名為 refCategory / refNo，例如：sourceRefCategory / sourceNo。

# 工程師回覆

| 項目 | 回覆理解 | 本次提案採用結論 |
|---|---|---|
| 品檢保留量與隔離量 | 第一版尚未建立隔離的獨立資料設計，為避免後端推測不存在的狀態，批號中心 V1 僅保留品檢保留量。 | 移除 `quarantineQuantity`、`quarantineBatchCount`、`quarantine` risk / stage enum；若未來需要隔離流程，另以正式資料表或 `warehouse_quality_hold.reasonCode` 規劃下一版。 |
| Dashboard 欄位命名 | 採用語意更清楚且接近畫面用途的命名。 | `summary.managedItemCount` 改為 `summary.stockItemCount`；`summary.distributedBatchCount` 改為 `summary.stockBatchCount`；`items[].highestRiskLevelCode` 改為 `items[].riskLevelCode`；`items[].primaryRiskCode` 改為 `items[].riskCode`。 |
| `items[].demandSignals[]` | 目前 Batch Center 第一版畫面未使用此區塊，依 AGENTS.md 原則不預留未使用欄位。 | Dashboard API 移除 `items[].demandSignals[]`；需求或任務影響後續由 detail、task 或下一版工作台畫面承接。 |
| 同批號分布於倉庫與產製中 | `batchStageCode` 不應被視為整個批號唯一狀態，而是分布列的目前作業階段。 | `/distribution` 以分布列回傳階段；同一批號若同時存在倉庫庫存與產製中數量，回傳多筆分布列，各列依所屬情境給不同 `batchStageCode`。 |
| 批號來源與關聯單據 | 批號來源表示此批號建立時的原始來源；關聯單據表示此批號目前或近期相關的任務、品檢、出貨、移倉等文件。 | 批號來源欄位統一為 `refCategory` / `refNo`，來源固定取 `batch_number.refCategory` / `batch_number.ref_no`；關聯單據改為 `relatedDocuments[].refCategory` / `relatedDocuments[].refNo`。 |
| Detail 出入庫欄位命名 | 採用資料庫欄位語意與簡潔命名。 | `inventoryRecords[].movementCategory` 改為 `inventoryRecords[].category`；`inventoryRecords[].movementSource` 改為 `inventoryRecords[].source`。 |

# BatchCenterScreen API 提案

> Status: API Proposal / Pending Engineer Review  
> Screen: `BatchCenterScreen`  
> Route: `/batches`  
> Scope: V1 read-only Core  
> Design basis: `AGENTS.md`、`src/app/batches/page.tsx`、`docs/spec/api/batchnumber.md`、`docs/spec/database/index.md`、既有 Warehouse V2 API 設計

## 1. 畫面定位

「批號中心」是以料品與批號為主視角的 read-only 工作區，協助管理者與倉庫／品保／生管人員快速掌握同一料品目前有哪些批號、分布在哪些倉庫、可用數量、預留數量、品檢保留量、效期風險與關聯任務。

本畫面與既有畫面的分工如下：

| 畫面 | 主視角 | 本版邊界 |
|---|---|---|
| `BatchCenterScreen` | 料品 → 批號 → 倉庫分布 | 管理批號分布、可用性、品檢與效期狀態；read-only。 |
| `WarehouseInventoryLotListScreen` | 倉庫庫存批號列 | 倉庫作業與庫存明細 drill-down，保留 warehouse-first 操作視角。 |
| `TraceabilityWorkspaceScreen` | 追溯鏈與召回 | 完整來源、流向、文件鏈與召回情境，非本次 API 範圍。 |

第一版不提供 POST、PUT、DELETE，不建立批號、不調整批號、不執行放行、不做出貨或領料 commit。

## 2. V1 API 清單

| API | Method | 用途 |
|---|---|---|
| `/api/v2/batches/dashboard` | GET | 批號中心 KPI、料品層級批號摘要、篩選與分頁清單 |
| `/api/v2/batches/items/{item_no}/distribution` | GET | 指定料品的批號與倉庫分布 |
| `/api/v2/batches/{batch_no}/detail` | GET | 指定批號跨倉庫的庫存、來源單據、預留、品檢、板位與未完成任務 |

> 工程師確認前，本文件為 API 提案；確認後才整合至 `docs/spec/api/` 正式 API 文件並進行後端實作。

## 3. 共用 Query Parameters / Header

| Parameter / Header | Type | Required | Description |
|---|---|---:|---|
| `date` | Integer | No | 查詢基準時間 UTC timestamp；未提供時使用 API 執行當下時間。 |
| `keyword` | String | No | 料品 no、料品名稱、批號、來源單號或倉庫 no 的關鍵字。 |
| `itemCategory` | Integer | No | 料品品項類別 code：原料(1)、物料(2)、膠捲(3)、在製品(4)、製成品(5)、貨品(6)、其他(0)。 |
| `itemSubCategory` | Integer | No | 料品品項子類別 code，定義依 `docs/spec/database/index.md` 的 `batch_number.itemSubCategory`。 |
| `itemType` | Integer | No | 品項型態 code：新料(1)、餘料(2)、廢料(3)、其他(0)。 |
| `warehouseNo` | String | No | 倉儲別名 no，對應 `ship_wh_alias.no`。 |
| `batchNo` | String | No | 批號，對應 `batch_number.no` 或庫存紀錄中的批號欄位。 |
| `riskLevelCode` | String | No | 風險等級 code；由前端提供 enum code，不傳顯示文字。 |
| `qaStatusCode` | String | No | 品檢狀態 code；由前端提供 enum code，不傳顯示文字。 |
| `batchStageCode` | String | No | 批號目前階段 code；由前端提供 enum code，不傳顯示文字。 |
| `availabilityCode` | String | No | 可用性篩選 code；例如 `available`、`reserved`、`quality_hold`、`empty`。 |
| `start` | Integer | No | 分頁起點，預設 0。負值視為 0。 |
| `count` | Integer | No | 回傳筆數，預設 50，最大 100。 |
| `x-timezone` | Header String | No | 前端顯示偏好的 IANA timezone；後端不以此改寫資料庫保存的 UTC timestamp。 |

## 4. GET `/api/v2/batches/dashboard`

### 4.1 Success Response Data

```json
{
  "serverTimestamp": "Integer",
  "summary": {
    "stockItemCount": "Integer",
    "highRiskItemCount": "Integer",
    "stockBatchCount": "Integer",
    "qualityHoldQuantity": "Float",
    "nearExpiryBatchCount": "Integer"
  },
  "items": [
    {
      "itemNo": "String",
      "itemName": "String",
      "itemCategory": "Integer",
      "itemSubCategory": "Integer",
      "itemType": "Integer",
      "totalBatchCount": "Integer",
      "warehouseCount": "Integer",
      "currentQuantity": "Float",
      "availableQuantity": "Float",
      "reservedQuantity": "Float",
      "qualityHoldQuantity": "Float",
      "earliestValidDate": "Integer",
      "qaHoldBatchCount": "Integer",
      "nearExpiryBatchCount": "Integer",
      "riskLevelCode": "String",
      "riskCode": "String",
      "ownerDepartment": "Integer"
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
| `summary.stockItemCount` | Integer | 套用篩選後，仍有目前庫存量大於 0 的不重複料品數。 | 庫存快照結果 |
| `summary.highRiskItemCount` | Integer | `riskLevelCode=high_risk` 的料品數。 | 風險彙總結果 |
| `summary.stockBatchCount` | Integer | 套用篩選後，仍有目前庫存量大於 0 的不重複批號數。 | 庫存快照結果、`batch_number.no` |
| `summary.qualityHoldQuantity` | Float | 品檢保留量總和，數量欄位取至小數點第 2 位。 | `warehouse_quality_hold` |
| `summary.nearExpiryBatchCount` | Integer | 少於到期日 1/3 效期或已逾期的批號數，不包含物料與膠捲類別。 | `batch_number.validDays`、`batch_number.validDate` |
| `items[].itemNo` | String | 料品 no。 | `batch_number.item_no`，庫存快照 fallback |
| `items[].itemName` | String | 料品名稱；無值時回傳空字串。 | `batch_number.item_name`，庫存快照 fallback |
| `items[].itemCategory` | Integer | 料品品項類別 code；前端負責多國語系顯示。 | `batch_number.itemCategory` |
| `items[].itemSubCategory` | Integer | 料品品項子類別 code。 | `batch_number.itemSubCategory` |
| `items[].itemType` | Integer | 品項型態 code；前端負責多國語系顯示。 | `batch_number.itemType` |
| `items[].totalBatchCount` | Integer | 此料品目前庫存量大於 0 的不重複批號數。 | 庫存快照結果 |
| `items[].warehouseCount` | Integer | 此料品目前庫存量大於 0 的不重複倉庫數。 | 庫存快照結果 |
| `items[].currentQuantity` | Float | 此料品目前庫存數量總和，取至小數點第 2 位；不同單位混用時，前端仍只顯示數值摘要並由 detail 顯示原單位 code。 | `CWarehouseInventorySnapshotCalculator` |
| `items[].availableQuantity` | Float | 目前可用數量，等於目前庫存數量扣除預留量與品檢保留量後不小於 0 的值，取至小數點第 2 位。 | 庫存快照、`warehouse_inventory_reservation`、`warehouse_quality_hold` |
| `items[].reservedQuantity` | Float | 已預留但尚未出庫或領用的數量總和，取至小數點第 2 位。 | `warehouse_inventory_reservation` |
| `items[].qualityHoldQuantity` | Float | 品檢保留數量總和，取至小數點第 2 位。 | `warehouse_quality_hold` |
| `items[].earliestValidDate` | Integer | 此料品目前庫存批號中最早有效期限 UTC timestamp；無有效期限時回傳 0。 | `batch_number.validDate` |
| `items[].qaHoldBatchCount` | Integer | 此料品中存在品檢保留量的批號數。 | `warehouse_quality_hold` |
| `items[].nearExpiryBatchCount` | Integer | 此料品中少於到期日 1/3 效期或已逾期的批號數，不包含物料與膠捲類別。 | `batch_number.validDays`、`batch_number.validDate` |
| `items[].riskLevelCode` | String | 此料品所有批號風險中的最高等級 code；前端負責顯示文字與 tone。 | `normal`、`attention`、`high_risk` |
| `items[].riskCode` | String | 此料品最主要風險 code；前端負責多國語系顯示。 | `normal`、`expired`、`near_expiry`、`quality_hold`、`reserved`、`stock_shortage`、`workflow_blocked`、`unknown` |
| `items[].ownerDepartment` | Integer | 目前建議下一步負責部門 code；無明確任務時回傳 0。 | `workflow_task_state.nextOwnerDepartment`、`workflow_next_owner_rule` |
| `total` | Integer | 套用篩選後的料品筆數。 | 查詢結果 |
| `start` | Integer | 本次分頁起點。 | Query parameter |
| `count` | Integer | 本次回傳筆數。 | Query parameter / 實際筆數 |

`items[]` 節點本身不另列說明。API 不回傳 `categoryName`、`message`、`recommendedAction`、`riskLabel` 或其他繁中字串 fallback。

## 5. GET `/api/v2/batches/items/{item_no}/distribution`

### 5.1 Success Response Data

```json
{
  "item": {
    "itemNo": "String",
    "itemName": "String",
    "itemCategory": "Integer",
    "itemSubCategory": "Integer",
    "itemType": "Integer",
    "unit": "Integer"
  },
  "batches": [
    {
      "batchNo": "String",
      "warehouseNo": "String",
      "warehouseName": "String",
      "locationCode": "String",
      "palletCount": "Float",
      "currentQuantity": "Float",
      "availableQuantity": "Float",
      "reservedQuantity": "Float",
      "qualityHoldQuantity": "Float",
      "unit": "Integer",
      "validDate": "Integer",
      "validDays": "Integer",
      "qaStatusCode": "String",
      "batchStageCode": "String",
      "riskLevelCode": "String",
      "riskCodes": [
        "String"
      ],
      "refCategory": "Integer",
      "refNo": "String",
      "relatedDocuments": [
        {
          "refCategory": "Integer",
          "refNo": "String"
        }
      ]
    }
  ],
  "total": "Integer",
  "start": "Integer",
  "count": "Integer"
}
```

### 5.2 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `item.itemNo` | String | 料品 no。 | `batch_number.item_no` |
| `item.itemName` | String | 料品名稱；無值時回傳空字串。 | `batch_number.item_name` |
| `item.itemCategory` | Integer | 料品品項類別 code。 | `batch_number.itemCategory` |
| `item.itemSubCategory` | Integer | 料品品項子類別 code。 | `batch_number.itemSubCategory` |
| `item.itemType` | Integer | 品項型態 code。 | `batch_number.itemType` |
| `item.unit` | Integer | 此料品的主要庫存單位 code；若不同批號單位不一致，仍以批號列的 `unit` 為準。 | `batch_number.unit` |
| `batches[].batchNo` | String | 批號。 | `batch_number.no`、庫存快照 batch key |
| `batches[].warehouseNo` | String | 倉儲別名 no。 | 庫存快照 `warehouseNo` |
| `batches[].warehouseName` | String | 倉儲別名名稱；無值時回傳空字串。 | `ship_wh_alias.displayName` 或 `inventory_record.warehouse_displayName` |
| `batches[].locationCode` | String | 主要板位或倉位代碼；無可判斷資料時回傳空字串。 | `warehouse_pallet_movement`、`batchno_serialno_group.group` |
| `batches[].palletCount` | Float | 此批號於此倉庫目前佔用板數，取至小數點第 2 位。 | `warehouse_pallet_movement` |
| `batches[].currentQuantity` | Float | 此批號於此倉庫目前庫存數量，取至小數點第 2 位；0 或小於 0 的列不回傳。 | `CWarehouseInventorySnapshotCalculator` |
| `batches[].availableQuantity` | Float | 此批號於此倉庫可用數量，取至小數點第 2 位。 | 庫存快照、reservation、quality hold |
| `batches[].reservedQuantity` | Float | 此批號於此倉庫預留數量，取至小數點第 2 位。 | `warehouse_inventory_reservation` |
| `batches[].qualityHoldQuantity` | Float | 此批號於此倉庫品檢保留數量，取至小數點第 2 位。 | `warehouse_quality_hold` |
| `batches[].unit` | Integer | 此批號庫存單位 code。 | `batch_number.unit`、庫存快照 fallback |
| `batches[].validDate` | Integer | 批號有效期限 UTC timestamp；無值時回傳 0。 | `batch_number.validDate` |
| `batches[].validDays` | Integer | 批號有效天數；無值時回傳 0。 | `batch_number.validDays` |
| `batches[].qaStatusCode` | String | 品檢狀態 code；前端負責顯示文字。 | `released`、`inspection`、`quality_hold`、`blocked`、`unknown` |
| `batches[].batchStageCode` | String | 此分布列的批號作業階段 code；同一批號若同時位於倉庫與產製中，需回傳多筆分布列，各列依實際情境給不同階段。 | `inbound_pending`、`stocked`、`available`、`reserved`、`quality_hold`、`production_input`、`production_output`、`shipped`、`unknown` |
| `batches[].riskLevelCode` | String | 此批號風險等級 code。 | `normal`、`attention`、`high_risk` |
| `batches[].riskCodes[]` | String | 此批號命中的風險 code 清單。 | `expired`、`near_expiry`、`quality_hold`、`reserved`、`stock_shortage`、`workflow_blocked` |
| `batches[].refCategory` | Integer | 批號建立時的來源單據類別，固定以 `batch_number.refCategory` 為準；例如採購進貨批號來自進貨單，產製批號來自工單或製程單。 | `batch_number.refCategory` |
| `batches[].refNo` | String | 批號建立時的來源單號，固定以 `batch_number.ref_no` 為準；不以後續出入庫紀錄覆蓋。 | `batch_number.ref_no` |
| `batches[].relatedDocuments[].refCategory` | Integer | 與此批號目前狀態或作業相關的單據類別；例如品檢任務、預留出貨、移倉或生產任務，不代表批號原始建立來源。 | workflow、reservation、quality hold 或 inventory record 相關來源 |
| `batches[].relatedDocuments[].refNo` | String | 關聯單據 no；無值時回傳空字串。 | workflow、reservation、quality hold 或 inventory record 相關來源 |
| `total` | Integer | 套用篩選後的批號倉庫分布列總數。 | 查詢結果 |
| `start` | Integer | 本次分頁起點。 | Query parameter |
| `count` | Integer | 本次回傳筆數。 | Query parameter / 實際筆數 |

`batches[]`、`riskCodes[]` 與 `relatedDocuments[]` 節點本身不另列說明。

### 5.3 批號來源與關聯單據範例

| 情境 | `batches[].refCategory` / `refNo` | `batches[].relatedDocuments[].refCategory` / `refNo` |
|---|---|---|
| 採購進貨產生批號 | 回傳建立批號時的進貨單類別與進貨單號，例如 `goods_receipt_note` 對應的 code 與 `GRN-20260801-001`。 | 若此批號正在品檢、預留出貨或移倉，回傳品檢任務、出庫任務或移倉任務的類別與單號。 |
| 生產產出產生批號 | 回傳建立批號時的工單／製程單類別與單號，例如 `MO-20260801-003`。 | 若此批號後續入庫、品檢或被出貨預留，回傳對應入庫、品檢或出貨相關單據。 |
| 同批號同時位於倉庫與產製中 | 每一分布列皆保留相同的批號建立來源 `refCategory` / `refNo`。 | 倉庫列可關聯預留、品檢或移倉文件；產製列可關聯工單、製程或待入庫任務。 |

## 6. GET `/api/v2/batches/{batch_no}/detail`

### 6.1 Success Response Data

```json
{
  "batch": {
    "batchNo": "String",
    "itemNo": "String",
    "itemName": "String",
    "itemCategory": "Integer",
    "itemSubCategory": "Integer",
    "itemType": "Integer",
    "unit": "Integer",
    "validDate": "Integer",
    "validDays": "Integer",
    "refCategory": "Integer",
    "refNo": "String",
    "creatorNo": "String",
    "creationTime": "Integer"
  },
  "stockByWarehouse": [
    {
      "warehouseNo": "String",
      "warehouseName": "String",
      "locationCode": "String",
      "palletCount": "Float",
      "currentQuantity": "Float",
      "availableQuantity": "Float",
      "reservedQuantity": "Float",
      "qualityHoldQuantity": "Float",
      "unit": "Integer",
      "riskLevelCode": "String",
      "riskCodes": [
        "String"
      ]
    }
  ],
  "inventoryRecords": [
    {
      "recordTime": "Integer",
      "refCategory": "Integer",
      "refNo": "String",
      "warehouseNo": "String",
      "category": "Integer",
      "source": "Integer",
      "quantity": "Float",
      "unit": "Integer",
      "amount": "Integer"
    }
  ],
  "reservations": [
    {
      "reservationNo": "String",
      "refCategory": "Integer",
      "refNo": "String",
      "warehouseNo": "String",
      "reservedQuantity": "Float",
      "status": "Integer",
      "expiryTimestamp": "Integer"
    }
  ],
  "qualityHolds": [
    {
      "holdNo": "String",
      "warehouseNo": "String",
      "holdQuantity": "Float",
      "status": "Integer",
      "reasonCode": "String",
      "createdTimestamp": "Integer"
    }
  ],
  "palletMovements": [
    {
      "movementNo": "String",
      "warehouseNo": "String",
      "palletNo": "String",
      "palletCount": "Float",
      "palletStatus": "Integer",
      "movementTimestamp": "Integer"
    }
  ],
  "tasks": [
    {
      "taskId": "Integer",
      "taskType": "Integer",
      "taskStatus": "Integer",
      "nextOwnerDepartment": "Integer",
      "dueTimestamp": "Integer",
      "refCategory": "Integer",
      "refNo": "String"
    }
  ]
}
```

### 6.2 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `batch.batchNo` | String | 批號。 | `batch_number.no` |
| `batch.itemNo` | String | 料品 no。 | `batch_number.item_no` |
| `batch.itemName` | String | 料品名稱。 | `batch_number.item_name` |
| `batch.itemCategory` | Integer | 料品品項類別 code。 | `batch_number.itemCategory` |
| `batch.itemSubCategory` | Integer | 料品品項子類別 code。 | `batch_number.itemSubCategory` |
| `batch.itemType` | Integer | 品項型態 code。 | `batch_number.itemType` |
| `batch.unit` | Integer | 批號單位 code。 | `batch_number.unit` |
| `batch.validDate` | Integer | 有效期限 UTC timestamp；無值時回傳 0。 | `batch_number.validDate` |
| `batch.validDays` | Integer | 有效天數；無值時回傳 0。 | `batch_number.validDays` |
| `batch.refCategory` | Integer | 批號建立時的來源單據類別，固定以 `batch_number.refCategory` 為準。 | `batch_number.refCategory` |
| `batch.refNo` | String | 批號建立時的來源單號，固定以 `batch_number.ref_no` 為準。 | `batch_number.ref_no` |
| `batch.creatorNo` | String | 批號建立人員 no；無值時回傳空字串。 | `batch_number.creator_no` |
| `batch.creationTime` | Integer | 批號資料建立時間 UTC timestamp；無值時回傳 0。 | `batch_number.creationTime` |
| `stockByWarehouse[].warehouseNo` | String | 倉儲別名 no。 | 庫存快照 |
| `stockByWarehouse[].warehouseName` | String | 倉儲別名名稱；無值時回傳空字串。 | `ship_wh_alias.displayName` 或 `inventory_record.warehouse_displayName` |
| `stockByWarehouse[].locationCode` | String | 主要板位或倉位代碼；無值時回傳空字串。 | `warehouse_pallet_movement`、`batchno_serialno_group.group` |
| `stockByWarehouse[].palletCount` | Float | 此批號於此倉庫目前佔用板數，取至小數點第 2 位。 | `warehouse_pallet_movement` |
| `stockByWarehouse[].currentQuantity` | Float | 此批號於此倉庫目前庫存數量，取至小數點第 2 位；0 或小於 0 的列不回傳。 | `CWarehouseInventorySnapshotCalculator` |
| `stockByWarehouse[].availableQuantity` | Float | 此批號於此倉庫可用數量，取至小數點第 2 位。 | 庫存快照、reservation、quality hold |
| `stockByWarehouse[].reservedQuantity` | Float | 此批號於此倉庫預留數量，取至小數點第 2 位。 | `warehouse_inventory_reservation` |
| `stockByWarehouse[].qualityHoldQuantity` | Float | 此批號於此倉庫品檢保留數量，取至小數點第 2 位。 | `warehouse_quality_hold` |
| `stockByWarehouse[].unit` | Integer | 此庫存列單位 code。 | `batch_number.unit`、庫存快照 fallback |
| `stockByWarehouse[].riskLevelCode` | String | 此倉庫批號列風險等級 code。 | `normal`、`attention`、`high_risk` |
| `stockByWarehouse[].riskCodes[]` | String | 此倉庫批號列命中的風險 code。 | risk enum |
| `inventoryRecords[].recordTime` | Integer | 出入庫紀錄時間 UTC timestamp。 | `inventory_record.date` |
| `inventoryRecords[].refCategory` | Integer | 出入庫紀錄關聯訂單類型。 | `inventory_record.refCategory` |
| `inventoryRecords[].refNo` | String | 出入庫紀錄來源單號。 | `inventory_record.ref_no` |
| `inventoryRecords[].warehouseNo` | String | 出入庫紀錄倉儲別名 no。 | `inventory_record.warehouse_no` |
| `inventoryRecords[].category` | Integer | 庫存型態：入庫(1)、出庫(2)。 | `inventory_record.category` |
| `inventoryRecords[].source` | Integer | 出入庫源由 code。 | `inventory_record.source` |
| `inventoryRecords[].quantity` | Float | 出入庫數量，取至小數點第 2 位。 | `inventory_record.count` |
| `inventoryRecords[].unit` | Integer | 出入庫單位 code。 | `inventory_record.unit` |
| `inventoryRecords[].amount` | Integer | 出入庫金額，四捨五入取整數。 | `inventory_record.amount` |
| `reservations[].reservationNo` | String | 預留紀錄 no；若資料表以 id 為主鍵，回傳 id 字串。 | `warehouse_inventory_reservation` |
| `reservations[].refCategory` | Integer | 預留來源單據類別。 | `warehouse_inventory_reservation.refCategory` |
| `reservations[].refNo` | String | 預留來源單號。 | `warehouse_inventory_reservation.ref_no` |
| `reservations[].warehouseNo` | String | 預留倉儲別名 no。 | `warehouse_inventory_reservation.warehouse_no` |
| `reservations[].reservedQuantity` | Float | 預留數量，取至小數點第 2 位。 | `warehouse_inventory_reservation.reservedQuantity` |
| `reservations[].status` | Integer | 預留狀態 code。 | `warehouse_inventory_reservation.status` |
| `reservations[].expiryTimestamp` | Integer | 預留失效時間 UTC timestamp；無值時回傳 0。 | `warehouse_inventory_reservation.expiryTimestamp` |
| `qualityHolds[].holdNo` | String | 品檢保留紀錄 no；若資料表以 id 為主鍵，回傳 id 字串。 | `warehouse_quality_hold` |
| `qualityHolds[].warehouseNo` | String | 品檢保留倉儲別名 no。 | `warehouse_quality_hold.warehouse_no` |
| `qualityHolds[].holdQuantity` | Float | 品檢保留數量，取至小數點第 2 位。 | `warehouse_quality_hold.holdQuantity` |
| `qualityHolds[].status` | Integer | 品檢保留狀態 code。 | `warehouse_quality_hold.status` |
| `qualityHolds[].reasonCode` | String | 品檢保留原因 code；前端負責顯示文字。 | `warehouse_quality_hold.reasonCode` |
| `qualityHolds[].createdTimestamp` | Integer | 品檢保留建立時間 UTC timestamp；無值時回傳 0。 | `warehouse_quality_hold.createdTimestamp` |
| `palletMovements[].movementNo` | String | 板位異動紀錄 no；若資料表以 id 為主鍵，回傳 id 字串。 | `warehouse_pallet_movement` |
| `palletMovements[].warehouseNo` | String | 板位異動倉儲別名 no。 | `warehouse_pallet_movement.warehouse_no` |
| `palletMovements[].palletNo` | String | 棧板編號；無值時回傳空字串。 | `warehouse_pallet_movement.palletNo` |
| `palletMovements[].palletCount` | Float | 板數，取至小數點第 2 位。 | `warehouse_pallet_movement.palletCount` |
| `palletMovements[].palletStatus` | Integer | 棧板狀態 code。 | `warehouse_pallet_movement.palletStatus` |
| `palletMovements[].movementTimestamp` | Integer | 板位異動時間 UTC timestamp；無值時回傳 0。 | `warehouse_pallet_movement.date` |
| `tasks[].taskId` | Integer | workflow 任務主鍵。 | `workflow_task_state.id` |
| `tasks[].taskType` | Integer | 任務類型：請購(1)、採購(2)、進貨(3)、入庫(4)、出庫(5)、移倉(6)、生產(7)、品檢(8)、出貨(9)。 | `workflow_task_state.taskType` |
| `tasks[].taskStatus` | Integer | 任務狀態 code。 | `workflow_task_state.taskStatus` |
| `tasks[].nextOwnerDepartment` | Integer | 下一步負責部門 code。 | `workflow_task_state.nextOwnerDepartment` |
| `tasks[].dueTimestamp` | Integer | 任務到期時間 UTC timestamp；無值時回傳 0。 | `workflow_task_state.dueTimestamp` |
| `tasks[].refCategory` | Integer | 任務來源單據類別。 | `workflow_task_state.refCategory` |
| `tasks[].refNo` | String | 任務來源單號。 | `workflow_task_state.ref_no` |

各 array 節點本身不另列說明。Detail API 只回傳此批號的資料，不回傳完整上下游追溯鏈。

## 7. Enum 與前端多國語系

後端只回傳 enum code 或資料庫 code，不回傳繁中顯示文字。前端負責將以下 code 轉換為繁中、英文或其他語系：

| Enum | 建議值 |
|---|---|
| `riskLevelCode` | `normal`、`attention`、`high_risk` |
| `riskCode` / `riskCodes[]` | `normal`、`expired`、`near_expiry`、`quality_hold`、`reserved`、`stock_shortage`、`workflow_blocked`、`unknown` |
| `qaStatusCode` | `released`、`inspection`、`quality_hold`、`blocked`、`unknown` |
| `batchStageCode` | `inbound_pending`、`stocked`、`available`、`reserved`、`quality_hold`、`production_input`、`production_output`、`shipped`、`unknown` |

若後續多個後端檔案共用這些 enum，需集中定義於 `restserver/package/common/common.py`。

## 8. V1 不包含的功能

- 批號新增、修改、合併、拆分、作廢或手動調整。
- 品檢放行、預留解除、出庫 commit 或移倉 commit。
- 隔離流程與隔離數量；第一版僅以 `qualityHoldQuantity` 表示品檢保留，待隔離資料模型確認後另案設計。
- 完整追溯鏈、召回清單、客戶流向與文件包匯出。
- 盤點流程。
- 沒有資料庫欄位或既有 workflow 支援的預測性建議文字。

## 9. 工程師提問與待確認

| 項目 | 提問 | 暫定提案 | 工程師回覆 |   
|---|---|---|---|
| API path | V2 path 是否採 `/api/v2/batches/...`，或為了與既有 `batchnumber.md` 命名一致改為 `/api/v2/batchnumber/...`？ | 建議前端畫面使用 `/batches`，API 使用 `/api/v2/batches/...`；既有 `/api/v1/batchnumber` 保留為舊版批號清單 API。 | 採用 `/api/v2/batches/...`|
| 隔離量 | `quarantineQuantity` 是否有獨立資料表／欄位，或需由 `warehouse_quality_hold.status` / `reasonCode` 映射？ | 第一版移除隔離量欄位，僅保留 `qualityHoldQuantity`；未來若建立隔離資料模型，再另案新增。 | 目前尚未設計關於隔離的呈現方式，可先參照你的建議進行規劃。 |
| 品檢狀態 | `qaStatusCode` 是否可由 `warehouse_quality_hold` 與品檢 workflow 任務狀態共同判斷？ | 建議優先以 `warehouse_quality_hold` active hold 判斷 `quality_hold` / `blocked`，無 hold 且無未完成品檢任務時為 `released`。 | 目前尚未設計關於狀態或階段的呈現方式，可先參照你的建議進行規劃。 |
| 批號階段 | `batchStageCode` 是否以庫存、預留、品檢、來源單據與任務共同推導？ | 建議以分布列為單位推導：quality hold > reserved > available > stocked > inbound pending > production input/output > unknown；同批號跨情境時回傳多列。 | 目前尚未設計關於狀態或階段的呈現方式，可先參照你的建議進行規劃。 |
| 需求影響 | `demandSignals[]` 是否只使用 workflow task 與 reservation，暫不接 APS 或訂單短缺演算法？ | 第一版畫面未使用，依規範自 Dashboard API 移除；後續需求影響由任務或 detail 相關 API 補充。 |目前尚未設計關於需求影響的呈現方式，可先參照你的建議進行規劃。 |
| 來源單據 | `sourceRefCategory`、`sourceNo` 是否一律以 `batch_number.refCategory`、`batch_number.ref_no` 為準？ | 採用 `refCategory`、`refNo` 命名；若 inventory record 來源不同，只在 detail 的 `inventoryRecords[]` 中呈現，不覆蓋 batch source。 | 若 `sourceRefCategory`、`sourceNo` 用於表示批號資訊，則應以 `batch_number.refCategory`、`batch_number.ref_no` 為準。 |
