# batches API Group

> Source: `restserver/package/restserver/api/v2/batches_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v2/batches/dashboard](#get-api-v2-batches-dashboard) | GET | 查詢批號中心 KPI、料品層級批號摘要、篩選與分頁清單 | OK | 依 `batch_center_proposal.md` 實作 |
| [/api/v2/batches/items/{item_no}/distribution](#get-api-v2-batches-items-item_no-distribution) | GET | 查詢指定料品的批號與倉庫／產製中分布 | OK | 依 `batch_center_proposal.md` 實作 |
| [/api/v2/batches/{batch_no}/detail](#get-api-v2-batches-batch_no-detail) | GET | 查詢指定批號跨倉庫庫存、來源單據、預留、品檢、板位與未完成任務 | OK | 依 `batch_center_proposal.md` 實作 |

## GET /api/v2/batches/dashboard

<a id="get-api-v2-batches-dashboard"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/batches/dashboard | GET | 查詢批號中心 KPI、料品層級批號摘要、篩選與分頁清單 |

### Request Header

| Header | Description |
|----------|----------|
| x-timezone | 前端顯示偏好的 IANA timezone；後端不改寫資料庫 UTC timestamp |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| date | Integer | NO | 查詢基準時間 UTC timestamp；未提供時使用 API 執行當下時間 |
| keyword | String | NO | 料品 no、料品名稱、批號、來源單號或倉庫 no 關鍵字 |
| itemCategory | Integer | NO | 料品品項類別 code |
| itemSubCategory | Integer | NO | 料品品項子類別 code |
| itemType | Integer | NO | 品項型態 code |
| warehouseNo | String | NO | 倉儲別名 no |
| batchNo | String | NO | 批號 |
| riskLevelCode | String | NO | 風險等級 code |
| qaStatusCode | String | NO | 品檢狀態 code |
| batchStageCode | String | NO | 批號作業階段 code |
| availabilityCode | String | NO | 可用性篩選 code |
| start | Integer | NO | 分頁起點，預設 0 |
| count | Integer | NO | 回傳筆數，預設 50，最大 100 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
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
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| payload.serverTimestamp | Integer | API 回應建立時間，UTC timestamp |  |
| payload.summary.stockItemCount | Integer | 套用篩選後仍有目前庫存量大於 0 的不重複料品數 |  |
| payload.summary.highRiskItemCount | Integer | `riskLevelCode=high_risk` 的料品數 |  |
| payload.summary.stockBatchCount | Integer | 套用篩選後仍有目前庫存量大於 0 的不重複批號數 |  |
| payload.summary.qualityHoldQuantity | Float | 品檢保留量總和，取至小數點第 2 位 |  |
| payload.summary.nearExpiryBatchCount | Integer | 少於到期日 1/3 效期或已逾期批號數，不包含物料與膠捲類別 |  |
| payload.items[].itemNo | String | 料品 no |  |
| payload.items[].itemName | String | 料品名稱 |  |
| payload.items[].itemCategory | Integer | 料品品項類別 code |  |
| payload.items[].itemSubCategory | Integer | 料品品項子類別 code |  |
| payload.items[].itemType | Integer | 品項型態 code |  |
| payload.items[].totalBatchCount | Integer | 此料品目前庫存量大於 0 的不重複批號數 |  |
| payload.items[].warehouseCount | Integer | 此料品目前庫存量大於 0 的不重複倉庫數 |  |
| payload.items[].currentQuantity | Float | 此料品目前庫存數量總和，取至小數點第 2 位 |  |
| payload.items[].availableQuantity | Float | 目前可用數量，扣除預留量與品檢保留量後不小於 0 |  |
| payload.items[].reservedQuantity | Float | 已預留但尚未出庫或領用的數量總和 |  |
| payload.items[].qualityHoldQuantity | Float | 品檢保留數量總和 |  |
| payload.items[].earliestValidDate | Integer | 此料品目前庫存批號中最早有效期限 UTC timestamp |  |
| payload.items[].qaHoldBatchCount | Integer | 此料品中存在品檢保留量的批號數 |  |
| payload.items[].nearExpiryBatchCount | Integer | 此料品中少於 1/3 效期或已逾期的批號數 |  |
| payload.items[].riskLevelCode | String | 此料品所有批號分布列的最高風險等級 code | normal、attention、high_risk |
| payload.items[].riskCode | String | 此料品最主要風險 code | normal、expired、near_expiry、quality_hold、reserved、stock_shortage、workflow_blocked、unknown |
| payload.items[].ownerDepartment | Integer | 目前建議下一步負責部門 code；無明確任務時回傳 0 |  |
| payload.total | Integer | 套用篩選後的料品筆數 |  |
| payload.start | Integer | 本次分頁起點 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Processing Flow

1. 讀取查詢條件並轉換為後端型別。
2. 透過 Warehouse 庫存快照共用邏輯取得目前庫存、預留、品檢保留、風險、板數與批號來源。
3. 過濾 `currentQuantity <= 0` 的庫存列。
4. 依料品彙總批號數、倉庫數、庫存數量、可用數量、預留數量、品檢保留量、效期與風險。
5. 套用篩選與固定排序：原料、物料、膠捲、在製品、製成品、貨品、其他；同類別再依風險、效期與料號排序。
6. 套用分頁並回傳 payload。

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 批號主檔與批號來源單據 |
| inventory_record | 庫存快照防護性補算與出入庫紀錄 |
| inventory_item_month_statistic | 批號庫存月結基準 |
| inventory_delta | 批號庫存異動補算 |
| warehouse_inventory_reservation | 預留數量 |
| warehouse_quality_hold | 品檢保留數量 |
| warehouse_pallet_movement | 板數 |
| workflow_task_state | 未完成任務與下一步負責部門 |

## GET /api/v2/batches/items/{item_no}/distribution

<a id="get-api-v2-batches-items-item_no-distribution"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/batches/items/{item_no}/distribution | GET | 查詢指定料品的批號與倉庫／產製中分布 |

### Request Header

| Header | Description |
|----------|----------|
| x-timezone | 前端顯示偏好的 IANA timezone |

### Query Parameters

同 `GET /api/v2/batches/dashboard`。

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
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
        "riskCodes": ["String"],
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
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| payload.item.itemNo | String | 料品 no |  |
| payload.item.itemName | String | 料品名稱 |  |
| payload.item.itemCategory | Integer | 料品品項類別 code |  |
| payload.item.itemSubCategory | Integer | 料品品項子類別 code |  |
| payload.item.itemType | Integer | 品項型態 code |  |
| payload.item.unit | Integer | 此料品主要庫存單位 code |  |
| payload.batches[].batchNo | String | 批號 |  |
| payload.batches[].warehouseNo | String | 倉儲別名 no；產製中分布列無倉庫時回傳空字串 |  |
| payload.batches[].warehouseName | String | 倉儲別名名稱；無值時回傳空字串 |  |
| payload.batches[].locationCode | String | 主要板位或倉位代碼；無資料時回傳空字串 |  |
| payload.batches[].palletCount | Float | 此批號於此倉庫目前佔用板數，取至小數點第 2 位 |  |
| payload.batches[].currentQuantity | Float | 此分布列目前數量，取至小數點第 2 位 |  |
| payload.batches[].availableQuantity | Float | 此分布列可用數量 |  |
| payload.batches[].reservedQuantity | Float | 此分布列預留數量 |  |
| payload.batches[].qualityHoldQuantity | Float | 此分布列品檢保留數量 |  |
| payload.batches[].unit | Integer | 此分布列單位 code |  |
| payload.batches[].validDate | Integer | 批號有效期限 UTC timestamp |  |
| payload.batches[].validDays | Integer | 批號有效天數 |  |
| payload.batches[].qaStatusCode | String | 品檢狀態 code | released、inspection、quality_hold、blocked、unknown |
| payload.batches[].batchStageCode | String | 此分布列批號作業階段 code，維持 String enum code | inbound_pending、stocked、available、reserved、quality_hold、production_input、production_output、shipped、unknown |
| payload.batches[].riskLevelCode | String | 此批號分布列風險等級 code | normal、attention、high_risk |
| payload.batches[].riskCodes[] | String | 此批號分布列命中的風險 code 清單 | expired、near_expiry、quality_hold、reserved、stock_shortage、workflow_blocked |
| payload.batches[].refCategory | Integer | 批號建立時的來源單據類別，固定以 `batch_number.refCategory` 為準 |  |
| payload.batches[].refNo | String | 批號建立時的來源單號，固定以 `batch_number.ref_no` 為準 |  |
| payload.batches[].relatedDocuments[].refCategory | Integer | 與此分布列目前或近期作業相關的單據類別 |  |
| payload.batches[].relatedDocuments[].refNo | String | 與此分布列目前或近期作業相關的單據 no |  |
| payload.total | Integer | 套用篩選後的分布列總數 |  |
| payload.start | Integer | 本次分頁起點 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Processing Flow

1. 驗證 `item_no`。
2. 建立 Batch Center 共用庫存資料集合，強制套用 `itemNo=item_no`。
3. 以 `batchNo + warehouseNo + batchStageCode` 建立分布列；同批號同時存在倉庫與產製中數量時回傳多列。
4. 回填批號主檔、倉庫名稱、板位、預留、品檢、風險、來源單據與關聯文件。
5. `relatedDocuments[]` 由 `workflow_task_state`、`warehouse_inventory_reservation`、`warehouse_quality_hold`、`inventory_record`，以及產製中情境的 `production_data_input` / `production_data_output` 彙整並以 `refCategory + refNo` 去重。
6. 套用篩選、排序與分頁後回傳。

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 批號主檔與批號來源單據 |
| inventory_record | 出入庫與近期關聯文件 |
| warehouse_inventory_reservation | 預留分布與關聯文件 |
| warehouse_quality_hold | 品檢保留與關聯文件 |
| warehouse_pallet_movement | 板數 |
| workflow_task_state | 未完成任務與關聯文件 |
| production_data_input | 產製投入批號分布 |
| production_data_output | 產製產出批號分布 |

## GET /api/v2/batches/{batch_no}/detail

<a id="get-api-v2-batches-batch_no-detail"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/batches/{batch_no}/detail | GET | 查詢指定批號跨倉庫庫存、來源單據、預留、品檢、板位與未完成任務 |

### Request Header

| Header | Description |
|----------|----------|
| x-timezone | 前端顯示偏好的 IANA timezone |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| date | Integer | NO | 查詢基準時間 UTC timestamp |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
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
        "taskId": "String",
        "taskType": "Integer",
        "taskStatus": "Integer",
        "nextOwnerDepartment": "Integer",
        "dueTimestamp": "Integer",
        "refCategory": "Integer",
        "refNo": "String"
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| payload.batch.batchNo | String | 批號 |  |
| payload.batch.itemNo | String | 料品 no |  |
| payload.batch.itemName | String | 料品名稱 |  |
| payload.batch.itemCategory | Integer | 料品品項類別 code |  |
| payload.batch.itemSubCategory | Integer | 料品品項子類別 code |  |
| payload.batch.itemType | Integer | 品項型態 code |  |
| payload.batch.unit | Integer | 批號單位 code |  |
| payload.batch.validDate | Integer | 有效期限 UTC timestamp |  |
| payload.batch.validDays | Integer | 有效天數 |  |
| payload.batch.refCategory | Integer | 批號建立時的來源單據類別 |  |
| payload.batch.refNo | String | 批號建立時的來源單號 |  |
| payload.batch.creatorNo | String | 批號建立人員 no |  |
| payload.batch.creationTime | Integer | 批號資料建立時間 UTC timestamp |  |
| payload.stockByWarehouse[] | Array | 此批號跨倉庫庫存摘要；欄位同 distribution 的倉庫庫存欄位子集合 |  |
| payload.inventoryRecords[] | Array | 最近出入庫紀錄，最多 100 筆 |  |
| payload.reservations[] | Array | 此批號預留紀錄 |  |
| payload.qualityHolds[] | Array | 此批號品檢保留紀錄 |  |
| payload.palletMovements[] | Array | 此批號最近板位異動，最多 100 筆 |  |
| payload.tasks[] | Array | 此批號未完成 workflow task |  |

| payload.stockByWarehouse[].warehouseNo | String | 此批號目前所在倉儲別名 no；只回傳目前庫存數量大於 0 的倉庫列 |  |
| payload.stockByWarehouse[].warehouseName | String | 此批號目前所在倉儲別名名稱；無值時回傳空字串 |  |
| payload.stockByWarehouse[].locationCode | String | 此批號於此倉庫的主要板位或倉位代碼；目前程式保留為空字串 |  |
| payload.stockByWarehouse[].palletCount | Float | 此批號於此倉庫目前佔用板數，取至小數點第 2 位 |  |
| payload.stockByWarehouse[].currentQuantity | Float | 此批號於此倉庫目前庫存數量，取至小數點第 2 位；0 或小於 0 的庫存列不回傳 |  |
| payload.stockByWarehouse[].availableQuantity | Float | 此批號於此倉庫目前可用數量，等於目前庫存扣除預留與品檢保留後不小於 0 的數量，取至小數點第 2 位 |  |
| payload.stockByWarehouse[].reservedQuantity | Float | 此批號於此倉庫已預留但尚未出庫或領用的數量，取至小數點第 2 位 |  |
| payload.stockByWarehouse[].qualityHoldQuantity | Float | 此批號於此倉庫品檢保留數量，取至小數點第 2 位 |  |
| payload.stockByWarehouse[].unit | Integer | 此庫存列的單位 code；前端負責顯示文字 |  |
| payload.stockByWarehouse[].riskLevelCode | String | 此倉庫批號列的風險等級 code；前端負責顯示文字與 tone | normal、attention、high_risk |
| payload.stockByWarehouse[].riskCodes[] | String | 此倉庫批號列命中的風險 code 清單；若無風險則包含 normal | normal、expired、near_expiry、quality_hold、reserved、stock_shortage、workflow_blocked、unknown |
| payload.inventoryRecords[].recordTime | Integer | 出入庫紀錄時間，UTC timestamp |  |
| payload.inventoryRecords[].refCategory | Integer | 出入庫紀錄來源或關聯單據類別 code |  |
| payload.inventoryRecords[].refNo | String | 出入庫紀錄來源或關聯單據 no |  |
| payload.inventoryRecords[].warehouseNo | String | 出入庫紀錄所屬倉儲別名 no |  |
| payload.inventoryRecords[].category | Integer | 庫存異動類別 code；依 `inventory_record.category` 回傳 |  |
| payload.inventoryRecords[].source | Integer | 出入庫來源 code；依 `inventory_record.source` 回傳 |  |
| payload.inventoryRecords[].quantity | Float | 出入庫數量，取至小數點第 2 位 |  |
| payload.inventoryRecords[].unit | Integer | 出入庫單位 code；前端負責顯示文字 |  |
| payload.inventoryRecords[].amount | Integer | 出入庫金額，四捨五入取整數 |  |
| payload.reservations[].reservationNo | String | 預留紀錄 no；若資料表 no 無值，程式以 id 轉字串回傳 |  |
| payload.reservations[].refCategory | Integer | 預留來源或關聯單據類別 code |  |
| payload.reservations[].refNo | String | 預留來源或關聯單據 no |  |
| payload.reservations[].warehouseNo | String | 預留所屬倉儲別名 no |  |
| payload.reservations[].reservedQuantity | Float | 預留數量，取至小數點第 2 位 |  |
| payload.reservations[].status | Integer | 預留狀態 code；前端負責顯示文字 |  |
| payload.reservations[].expiryTimestamp | Integer | 預留釋放或失效時間，UTC timestamp；無值時回傳 0 |  |
| payload.qualityHolds[].holdNo | String | 品檢保留紀錄 no；若資料表 no 無值，程式以 id 轉字串回傳 |  |
| payload.qualityHolds[].warehouseNo | String | 品檢保留所屬倉儲別名 no |  |
| payload.qualityHolds[].holdQuantity | Float | 品檢保留數量，取至小數點第 2 位 |  |
| payload.qualityHolds[].status | Integer | 品檢保留狀態 code；前端負責顯示文字 |  |
| payload.qualityHolds[].reasonCode | String | 品檢保留原因 code；前端負責顯示文字與多國語言 |  |
| payload.qualityHolds[].createdTimestamp | Integer | 品檢保留建立時間，UTC timestamp；無值時回傳 0 |  |
| payload.palletMovements[].movementNo | String | 板位異動紀錄 no；若資料表 no 無值，程式以 id 轉字串回傳 |  |
| payload.palletMovements[].warehouseNo | String | 板位異動所屬倉儲別名 no |  |
| payload.palletMovements[].palletNo | String | 棧板群組或棧板編號；無值時回傳空字串 |  |
| payload.palletMovements[].palletCount | Float | 板數，取至小數點第 2 位 |  |
| payload.palletMovements[].palletStatus | Integer | 棧板狀態 code；前端負責顯示文字 |  |
| payload.palletMovements[].movementTimestamp | Integer | 板位異動時間，UTC timestamp；無值時回傳 0 |  |
| payload.tasks[].taskId | String | workflow 任務識別值；優先回傳 `workflow_task_state.taskId`，無值時以 id 轉字串回傳 |  |
| payload.tasks[].taskType | Integer | 任務類型：請購(1)、採購(2)、進貨(3)、入庫(4)、出庫(5)、移倉(6)、生產(7)、品檢(8)、出貨(9) |  |
| payload.tasks[].taskStatus | Integer | 任務狀態 code；只回傳 pending、partial、blocked 等未完成任務 |  |
| payload.tasks[].nextOwnerDepartment | Integer | 下一步負責部門 code；依目前程式取 `workflow_task_state.ownerDepartment` 回傳 |  |
| payload.tasks[].dueTimestamp | Integer | 任務到期時間，UTC timestamp；無值時回傳 0 |  |
| payload.tasks[].refCategory | Integer | 任務來源或關聯單據類別 code |  |
| payload.tasks[].refNo | String | 任務來源或關聯單據 no |  |

各 array 節點本身不另列說明。Detail API 只回傳此批號的資料，不回傳完整上下游追溯鏈。

### Processing Flow

1. 驗證 `batch_no` 並查詢 `batch_number`。
2. 不存在時回傳 not found。
3. 建立 Batch Center 共用庫存資料集合，強制套用 `batchNo=batch_no`。
4. `stockByWarehouse[]` 由庫存快照加上 reservation、quality hold、pallet movement 彙整，只保留 `currentQuantity > 0`。
5. 查詢此批號的出入庫紀錄、預留紀錄、品檢保留紀錄、板位異動與未完成 workflow task。
6. 合法空集合回傳空陣列。

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 批號主檔 |
| inventory_record | 出入庫紀錄 |
| warehouse_inventory_reservation | 預留紀錄 |
| warehouse_quality_hold | 品檢保留紀錄 |
| warehouse_pallet_movement | 板位異動 |
| workflow_task_state | 未完成任務 |
