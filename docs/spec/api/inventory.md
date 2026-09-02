# inventory API Group

> Source: `restserver/package/restserver/api/inventory_uri.py`
> V2 Source: `restserver/package/restserver/api/v2/inventory_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/inventory](#get-api-v1-inventory) | GET | 查詢庫存 | OK | OK |
| [/api/v1/inventory/items](#get-api-v1-inventory-items) | GET | 查詢庫存 / 品項清單 | OK | OK |
| [/api/v1/inventory/months](#get-api-v1-inventory-months) | GET | 查詢庫存 / 月資料 | OK | OK |
| [/api/v1/inventory/price](#get-api-v1-inventory-price) | GET | 查詢庫存 / 價格 | OK | OK |
| [/api/v1/inventory/statistics](#get-api-v1-inventory-statistics) | GET | 查詢庫存 / 統計 | OK | OK |
| [/api/v2/inventory/balances](#get-api-v2-inventory-balances) | GET | 查詢倉庫目前庫存餘額 | Implemented / Pending Runtime Review | `ERP2-API-WH-INV-STAGING-ALIGN-001` controlled staging path 已支援七張授權 `np_*` 物件；保留 UOM Option B，不進行單位換算。 |
| [/api/v2/inventory/movements](#get-api-v2-inventory-movements) | GET | 查詢倉庫庫存異動紀錄 | Implemented / Pending Runtime Review | `ERP2-API-WH-INV-STAGING-ALIGN-001` controlled staging path 已支援 `np_stg_inventory_movement`。 |
| [/api/v2/lots](#get-api-v2-lots) | GET | 查詢目前仍有庫存的批號清單 | Implemented / Pending Runtime Review | `ERP2-API-WH-INV-STAGING-ALIGN-001` controlled staging path 已支援 `np_stg_lot_snapshot`；批號庫存量為 0 的列不回傳。 |
| [/api/v2/lots/{lot_code}/trace](#get-api-v2-lots-lot-code-trace) | GET | 查詢指定批號溯源資料 | Implemented / Pending Runtime Review | `ERP2-API-WH-INV-STAGING-ALIGN-001` controlled staging path 僅以授權 `np_*` 批號、料品與異動關聯回傳受控溯源資料。 |

## GET /api/v1/inventory

<a id="get-api-v1-inventory"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/inventory | GET | 查詢庫存 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | String | NO | 分頁筆數 |
| start | String | NO | 分頁起始位置 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "total": "Integer",
    "count": "Integer",
    "results": [
      {
        "id": "Integer",
        "date": "Integer",
        "no": "String",
        "creator_no": "String",
        "ref_no": "String",
        "refCategory": "Integer",
        "item_no": "String",
        "item_name": "String",
        "item_ref_no": "String",
        "item_ref_displayName": "String",
        "itemCategory": "Integer",
        "itemSubCategory": "Integer",
        "itemType": "Integer",
        "unit": "Integer",
        "expectedCount": "Float",
        "checkedCount": "Float",
        "validDays": "Integer",
        "validDate": "Integer",
        "validDateNo": "String",
        "comment": "String",
        "creationTime": "Integer"
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].date | Integer | 日期時間 |  |
| payload.results[].no | String | 資料編號 |  |
| payload.results[].creator_no | String | 製單人員編號 |  |
| payload.results[].ref_no | String | 來源單號 |  |
| payload.results[].refCategory | Integer | 來源類別 |  |
| payload.results[].item_no | String | 「料品品項」編號 |  |
| payload.results[].item_name | String | 「料品品項」名稱 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].itemCategory | Integer | 料品類別 |  |
| payload.results[].itemSubCategory | Integer | 料品子類別 |  |
| payload.results[].itemType | Integer | 料品類型 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].expectedCount | Float | 預期數量 |  |
| payload.results[].checkedCount | Float | 已確認數量 |  |
| payload.results[].validDays | Integer | 有效天數 |  |
| payload.results[].validDate | Integer | 效期日期 |  |
| payload.results[].validDateNo | String | 效期日期編號 |  |
| payload.results[].comment | String | 備註 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 batch_number、inventory_record、process_order 取得庫存資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 提供庫存查詢、統計或紀錄資料 |
| inventory_record | 提供庫存查詢、統計或紀錄資料 |
| process_order | 提供庫存查詢、統計或紀錄資料 |

## GET /api/v2/inventory/balances

<a id="get-api-v2-inventory-balances"></a>

### Basic Information

| URL | Method | Description |
|---|---|---|
| /api/v2/inventory/balances | GET | 查詢倉庫目前庫存餘額 |

### Request Header

| Header | Description |
|---|---|
| x-auth-token | 存取金鑰。 |
| x-timezone | 時區代碼，例如 `Asia/Taipei`；未提供時使用 `UTC`。 |

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| date | Integer | NO | 查詢基準 UTC timestamp；未提供時使用伺服器目前時間。 |
| warehouse_no | String | NO | 倉庫 no，對應 `inventory_record.warehouse_no`。 |
| itemCategory | Integer | NO | 料品類別，對應 `inventory_record.itemCategory`。 |
| item_no | String | NO | 料品 no，對應 `inventory_record.item_no`。 |
| lotCode | String | NO | 批號，對應 `inventory_record.batchNumber`。 |
| start | Integer | NO | 分頁起始位置，預設 0。 |
| count | Integer | NO | 分頁筆數，預設 50，上限 100。 |

### Request Body

None

### Controlled Staging Mode Note

本 API 在一般模式下維持既有正式 ERP 查詢邏輯；於 `ERP2_WH_INV_STAGING_MODE=1` 時，啟用 `ERP2-API-WH-INV-STAGING-ALIGN-001` 受控非正式測試路徑。此路徑僅讀取授權七張 `np_*` 物件，不建立、不要求、也不寫入正式 ERP operational tables。因 `np_*` 物件未提供正式料品類別欄位，controlled staging path 若收到 `itemCategory` 條件，會回傳空集合以避免錯誤分類。

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "timezone": "String",
    "total": "Integer",
    "start": "Integer",
    "count": "Integer",
    "permissionCode": "String",
    "balances": [{
      "balanceId": "String",
      "warehouseNo": "String",
      "warehouseName": "String",
      "itemNo": "String",
      "itemName": "String",
      "itemCategory": "Integer",
      "itemSubCategory": "Integer",
      "lotCode": "String",
      "serialNo": "String",
      "currentQuantity": "Float",
      "reservedQuantity": "Float",
      "qualityHoldQuantity": "Float",
      "availableQuantity": "Float",
      "unit": "Integer | String",
      "candidateCanonicalUomCode": "String",
      "unitCost": "Float",
      "inventoryValue": "Integer",
      "availableValue": "Integer",
      "sourceRefCategory": "Integer",
      "sourceNo": "String",
      "qualityStatus": "String",
      "riskTypes": ["String"],
      "sourceProvenanceRef": "String"
    }]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
|---|---|---|---|
| payload.serverTimestamp | Integer | Response 產生時間，UTC timestamp。 |  |
| payload.timezone | String | 本次查詢採用的時區代碼。 |  |
| payload.total | Integer | 符合查詢條件的庫存餘額總筆數。 |  |
| payload.start | Integer | 本次分頁起始位置。 |  |
| payload.count | Integer | 本次實際回傳筆數。 |  |
| payload.permissionCode | String | 此 read-only API 對應的權限代碼。 | `WH_INV_READ` |
| payload.balances[].balanceId | String | 庫存餘額識別值，由倉庫、料品、批號與序號組成。 |  |
| payload.balances[].warehouseNo | String | 倉庫 no。 |  |
| payload.balances[].warehouseName | String | 倉庫顯示名稱。 |  |
| payload.balances[].itemNo | String | 料品 no。 |  |
| payload.balances[].itemName | String | 料品名稱。 |  |
| payload.balances[].itemCategory | Integer | 料品類別。 | `EItemCategory` |
| payload.balances[].itemSubCategory | Integer | 料品子類別。 |  |
| payload.balances[].lotCode | String | 批號，來源為 `inventory_record.batchNumber`，並以 `batch_number.no` 補足來源單據。 |  |
| payload.balances[].serialNo | String | 序號；無序號時回傳空字串。 |  |
| payload.balances[].currentQuantity | Float | 目前庫存數量，入庫數量扣除出庫數量，取至小數點第 2 位。 |  |
| payload.balances[].reservedQuantity | Float | 目前有效預留數量，取至小數點第 2 位。 |  |
| payload.balances[].qualityHoldQuantity | Float | 目前品檢保留數量，取至小數點第 2 位。 |  |
| payload.balances[].availableQuantity | Float | 可用數量，計算為目前庫存扣除預留與品檢保留，取至小數點第 2 位。 |  |
| payload.balances[].unit | Integer \| String | 一般模式回傳原始庫存單位 code；controlled staging path 回傳來源顯示單位，例如 `公斤`。保留 UOM Option B，不於後端換算或翻譯。 | `EUnit` |
| payload.balances[].candidateCanonicalUomCode | String | controlled staging path 的候選標準單位代碼，例如 `KG`；僅作為對照 metadata，不代表已換算。 |  |
| payload.balances[].unitCost | Float | 單價，依庫存價值除以目前庫存數量推算，取至小數點第 4 位。 |  |
| payload.balances[].inventoryValue | Integer | 目前庫存價值，四捨五入取整數。 |  |
| payload.balances[].availableValue | Integer | 可用庫存價值，四捨五入取整數。 |  |
| payload.balances[].sourceRefCategory | Integer | 批號來源單據類別，來源為 `batch_number.refCategory`。 |  |
| payload.balances[].sourceNo | String | 批號來源單號，來源為 `batch_number.ref_no`。 |  |
| payload.balances[].qualityStatus | String | 品檢狀態代碼；後端僅回傳代碼，顯示文字由前端轉換。 | `hold`, `released` |
| payload.balances[].riskTypes | Array | 庫存風險類型代碼清單；顯示文字由前端轉換。 | `EWarehouseRiskType` |
| payload.balances[].sourceProvenanceRef | String | controlled staging path 的非正式測試來源證據識別；一般模式不回傳此欄位。 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|---|---|---|---|
| code | Integer | API 錯誤代碼。 | `EErrorCode` |
| message | String | API 錯誤訊息。 |  |
| payload | Object | 錯誤時多為空物件。 |  |

### Processing Flow

1. 檢查 request header 是否提供 `x-auth-token`，並套用既有 API token 流程。
2. 宣告本 API read-only 權限代碼為 `WH_INV_READ`。
3. 一般模式依查詢條件呼叫既有 Warehouse 庫存快照計算邏輯。
4. 一般模式以 `inventory_item_month_statistic`、`inventory_delta` 與必要時 `inventory_record` 補算目前庫存數量與庫存價值，並以 `batch_number` 取得批號來源單據。
5. controlled staging path 僅在環境旗標 `ERP2_WH_INV_STAGING_MODE=1` 時啟用，直接讀取授權 `np_*` staging/crosswalk 物件，不初始化正式 ERP ORM 自動建表流程。
6. controlled staging path 從 `np_stg_inventory_balance_snapshot` 讀取庫存餘額，並以 `np_xwalk_item_identity`、`np_xwalk_lot_identity`、`np_xwalk_uom` 補足料品、批號與 UOM 對照資訊。
7. controlled staging path 僅回傳 `validation_state = READY_FOR_READ_ONLY_API` 且來源或顯示數量大於 0 的資料列。
8. 回傳符合 UOM Option B 的庫存餘額資料，保留來源數量與來源顯示單位，不進行單位換算。

### Database Tables Used

| Table | Purpose |
|---|---|
| inventory_record | 庫存異動與防護性補算依據。 |
| inventory_item_month_statistic | 月結庫存快照。 |
| inventory_delta | 月結後庫存異動。 |
| batch_number | 批號主檔與來源單據。 |
| warehouse_inventory_reservation | 預留數量與預留價值。 |
| warehouse_quality_hold | 品檢保留數量與保留價值。 |
| warehouse_pallet_movement | 板位佔用資訊。 |
| warehouse_risk_rule | 庫存風險規則。 |
| np_stg_inventory_balance_snapshot | controlled staging path 的目前庫存餘額來源。 |
| np_xwalk_item_identity | controlled staging path 的料品 identity 對照來源。 |
| np_xwalk_lot_identity | controlled staging path 的批號 identity 對照來源。 |
| np_xwalk_uom | controlled staging path 的來源單位、顯示單位與候選標準單位 metadata。 |

## GET /api/v2/inventory/movements

<a id="get-api-v2-inventory-movements"></a>

### Basic Information

| URL | Method | Description |
|---|---|---|
| /api/v2/inventory/movements | GET | 查詢倉庫庫存異動紀錄 |

### Request Header

| Header | Description |
|---|---|
| x-auth-token | 存取金鑰。 |
| x-timezone | 時區代碼，例如 `Asia/Taipei`；未提供時使用 `UTC`。 |

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| date | Integer | NO | 查詢基準 UTC timestamp；未提供日期區間時，查詢此時間以前的異動。 |
| startDate | String | NO | 查詢起始日，格式 `YYYY-MM-DD`；需與 `endDate` 同時提供。 |
| endDate | String | NO | 查詢結束日，格式 `YYYY-MM-DD`；包含當日。 |
| warehouse_no | String | NO | 倉庫 no，對應 `inventory_record.warehouse_no`。 |
| itemCategory | Integer | NO | 料品類別，對應 `inventory_record.itemCategory`。 |
| item_no | String | NO | 料品 no，對應 `inventory_record.item_no`。 |
| lotCode | String | NO | 批號，對應 `inventory_record.batchNumber`。 |
| keyword | String | NO | 搜尋來源單號、料品 no、料品名稱、批號、倉庫 no 或倉庫名稱。 |
| start | Integer | NO | 分頁起始位置，預設 0。 |
| count | Integer | NO | 分頁筆數，預設 50，上限 100。 |

### Request Body

None

### Controlled Staging Mode Note

本 API 在一般模式下維持既有正式 ERP 查詢邏輯；於 `ERP2_WH_INV_STAGING_MODE=1` 時，啟用 `ERP2-API-WH-INV-STAGING-ALIGN-001` 受控非正式測試路徑。此路徑僅讀取授權七張 `np_*` 物件，不建立、不要求、也不寫入正式 ERP operational tables。因 `np_*` 物件未提供正式料品類別欄位，controlled staging path 若收到 `itemCategory` 條件，會回傳空集合以避免錯誤分類。

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "timezone": "String",
    "total": "Integer",
    "start": "Integer",
    "count": "Integer",
    "permissionCode": "String",
    "range": {"period": "String", "startDate": "String", "endDate": "String", "startTimestamp": "Integer", "endTimestamp": "Integer"},
    "movements": [{
      "movementId": "Integer | String",
      "groupNo": "String",
      "warehouseNo": "String",
      "warehouseName": "String",
      "itemNo": "String",
      "itemName": "String",
      "itemCategory": "Integer",
      "lotCode": "String",
      "serialNo": "String",
      "movementTimestamp": "Integer",
      "category": "Integer | String",
      "source": "Integer | String",
      "quantity": "Float",
      "unit": "Integer | String",
      "candidateCanonicalUomCode": "String",
      "unitCost": "Float",
      "amount": "Integer",
      "refCategory": "Integer | String",
      "refNo": "String",
      "comment": "String",
      "creationTime": "Integer",
      "sourceProvenanceRef": "String"
    }]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
|---|---|---|---|
| payload.permissionCode | String | 此 read-only API 對應的權限代碼。 | `WH_INV_READ` |
| payload.range | Object | 提供 `startDate` 與 `endDate` 時回傳實際查詢區間；未提供時為空物件。 |  |
| payload.movements[].movementId | Integer \| String | 一般模式來源為 `inventory_record.id`；controlled staging path 來源為 `np_stg_inventory_movement.stg_inventory_movement_id`。 |  |
| payload.movements[].groupNo | String | 庫存異動群組編號，來源為 `inventory_record.group`。 |  |
| payload.movements[].warehouseNo | String | 倉庫 no。 |  |
| payload.movements[].warehouseName | String | 倉庫顯示名稱。 |  |
| payload.movements[].itemNo | String | 料品 no。 |  |
| payload.movements[].itemName | String | 料品名稱。 |  |
| payload.movements[].itemCategory | Integer | 料品類別。 | `EItemCategory` |
| payload.movements[].lotCode | String | 批號，來源為 `inventory_record.batchNumber`。 |  |
| payload.movements[].serialNo | String | 序號；無序號時回傳空字串。 |  |
| payload.movements[].movementTimestamp | Integer | 庫存異動時間，UTC timestamp。 |  |
| payload.movements[].category | Integer \| String | 一般模式為庫存異動方向；controlled staging path 回傳來源異動類型，例如 `RECEIPT`、`ISSUE`、`TRANSFER`。 | `EInventoryCategory` |
| payload.movements[].source | Integer \| String | 一般模式為庫存異動來源類型；controlled staging path 固定為 `NP_STAGING`。 | `EInventorySrc` |
| payload.movements[].quantity | Float | 異動數量，保留原始單位，取至小數點第 2 位。 |  |
| payload.movements[].unit | Integer \| String | 一般模式回傳原始異動單位 code；controlled staging path 回傳來源顯示單位，例如 `公斤`。保留 UOM Option B，不於後端換算或翻譯。 | `EUnit` |
| payload.movements[].candidateCanonicalUomCode | String | controlled staging path 的候選標準單位代碼，例如 `KG`；僅作為對照 metadata，不代表已換算。 |  |
| payload.movements[].unitCost | Float | 單價，依金額除以數量推算，取至小數點第 4 位。 |  |
| payload.movements[].amount | Integer | 異動金額，四捨五入取整數。 |  |
| payload.movements[].refCategory | Integer \| String | 一般模式為來源單據類別；controlled staging path 固定為 `NP_STAGING_SOURCE_DOCUMENT`。 |  |
| payload.movements[].refNo | String | 來源單號。 |  |
| payload.movements[].comment | String | 備註。 |  |
| payload.movements[].creationTime | Integer | 資料建立時間。 |  |
| payload.movements[].sourceProvenanceRef | String | controlled staging path 的非正式測試來源證據識別；一般模式不回傳此欄位。 |  |

### Processing Flow

1. 檢查 request header 是否提供 `x-auth-token`，並套用既有 API token 流程。
2. 宣告本 API read-only 權限代碼為 `WH_INV_READ`。
3. 若提供 `startDate` 與 `endDate`，依 `x-timezone` 轉為 UTC 查詢區間；否則查詢 `date` 以前的資料。
4. 一般模式依倉庫、料品類別、料品 no、批號與關鍵字篩選 `inventory_record`。
5. controlled staging path 僅在環境旗標 `ERP2_WH_INV_STAGING_MODE=1` 時啟用，從 `np_stg_inventory_movement` 讀取庫存異動，並以 `np_xwalk_item_identity`、`np_xwalk_lot_identity`、`np_xwalk_uom` 補足料品、批號與 UOM 對照資訊。
6. controlled staging path 僅回傳 `validation_state = READY_FOR_READ_ONLY_API` 的資料列，並支援日期區間、倉庫、料品 no、批號與關鍵字篩選。
7. controlled staging path 若收到 `itemCategory` 篩選，因授權 `np_*` 欄位未提供正式料品類別，回傳空集合以避免錯誤分類。
8. 依異動日期與資料識別值倒序分頁；數量保留來源單位，不進行單位換算。

### Database Tables Used

| Table | Purpose |
|---|---|
| inventory_record | 庫存異動紀錄來源。 |
| np_stg_inventory_movement | controlled staging path 的庫存異動紀錄來源。 |
| np_xwalk_item_identity | controlled staging path 的料品 identity 對照來源。 |
| np_xwalk_lot_identity | controlled staging path 的批號 identity 對照來源。 |
| np_xwalk_uom | controlled staging path 的來源單位、顯示單位與候選標準單位 metadata。 |

## GET /api/v2/lots

<a id="get-api-v2-lots"></a>

### Basic Information

| URL | Method | Description |
|---|---|---|
| /api/v2/lots | GET | 查詢目前仍有庫存的批號清單 |

### Request Header

| Header | Description |
|---|---|
| x-auth-token | 存取金鑰。 |
| x-timezone | 時區代碼，例如 `Asia/Taipei`；未提供時使用 `UTC`。 |

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| date | Integer | NO | 查詢基準 UTC timestamp；未提供時使用伺服器目前時間。 |
| warehouse_no | String | NO | 倉庫 no。 |
| itemCategory | Integer | NO | 料品類別。 |
| item_no | String | NO | 料品 no。 |
| lotCode | String | NO | 批號。 |
| keyword | String | NO | 搜尋料品 no、料品名稱、批號、來源單號或倉庫名稱。 |
| start | Integer | NO | 分頁起始位置，預設 0。 |
| count | Integer | NO | 分頁筆數，預設 50，上限 100。 |

### Request Body

None

### Controlled Staging Mode Note

本 API 在一般模式下維持既有正式 ERP 查詢邏輯；於 `ERP2_WH_INV_STAGING_MODE=1` 時，啟用 `ERP2-API-WH-INV-STAGING-ALIGN-001` 受控非正式測試路徑。此路徑僅讀取授權七張 `np_*` 物件，不建立、不要求、也不寫入正式 ERP operational tables。因 `np_*` 物件未提供正式料品類別欄位，controlled staging path 若收到 `itemCategory` 條件，會回傳空集合以避免錯誤分類。

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "timezone": "String",
    "total": "Integer",
    "start": "Integer",
    "count": "Integer",
    "permissionCode": "String",
    "summary": {},
    "lots": [{
      "lotKey": "String",
      "lotCode": "String",
      "warehouseNo": "String",
      "warehouseName": "String",
      "itemCategory": "Integer",
      "itemNo": "String",
      "itemName": "String",
      "currentQuantity": "Float",
      "reservedQuantity": "Float",
      "qualityHoldQuantity": "Float",
      "availableQuantity": "Float",
      "unit": "Integer | String",
      "candidateCanonicalUomCode": "String",
      "unitCost": "Float",
      "inventoryValue": "Integer",
      "palletCount": "Float",
      "firstInboundTimestamp": "Integer",
      "daysInStock": "Integer",
      "validDate": "Integer",
      "validDays": "Integer",
      "safetyStock": "Float",
      "riskTypes": ["String"],
      "openTaskCount": "Integer",
      "refCategory": "Integer",
      "refNo": "String",
      "qualityStatus": "String",
      "sourceProvenanceRef": "String"
    }]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
|---|---|---|---|
| payload.permissionCode | String | 此 read-only API 對應的權限代碼。 | `WH_INV_READ` |
| payload.summary | Object | 批號清單摘要，沿用 Warehouse 庫存批號服務的彙總結果。 |  |
| payload.lots[].lotKey | String | 批號庫存識別值，由倉庫、料品與批號組成。 |  |
| payload.lots[].lotCode | String | 批號。 |  |
| payload.lots[].warehouseNo | String | 倉庫 no。 |  |
| payload.lots[].warehouseName | String | 倉庫顯示名稱。 |  |
| payload.lots[].itemCategory | Integer | 料品類別。 | `EItemCategory` |
| payload.lots[].itemNo | String | 料品 no。 |  |
| payload.lots[].itemName | String | 料品名稱。 |  |
| payload.lots[].currentQuantity | Float | 目前批號庫存數量，取至小數點第 2 位。 |  |
| payload.lots[].reservedQuantity | Float | 目前有效預留數量，取至小數點第 2 位。 |  |
| payload.lots[].qualityHoldQuantity | Float | 目前品檢保留數量，取至小數點第 2 位。 |  |
| payload.lots[].availableQuantity | Float | 可用數量，取至小數點第 2 位。 |  |
| payload.lots[].unit | Integer \| String | 一般模式回傳原始庫存單位 code；controlled staging path 回傳來源顯示單位，例如 `公斤`。保留 UOM Option B，不於後端換算或翻譯。 | `EUnit` |
| payload.lots[].candidateCanonicalUomCode | String | controlled staging path 的候選標準單位代碼，例如 `KG`；僅作為對照 metadata，不代表已換算。 |  |
| payload.lots[].unitCost | Float | 單價，取至小數點第 4 位。 |  |
| payload.lots[].inventoryValue | Integer | 批號庫存價值，四捨五入取整數。 |  |
| payload.lots[].palletCount | Float | 批號佔用板數，取至小數點第 2 位。 |  |
| payload.lots[].firstInboundTimestamp | Integer | 首次入庫時間，UTC timestamp。 |  |
| payload.lots[].daysInStock | Integer | 存放天數。 |  |
| payload.lots[].validDate | Integer | 批號效期時間，UTC timestamp。 |  |
| payload.lots[].validDays | Integer | 批號有效天數。 |  |
| payload.lots[].safetyStock | Float | 安全水位數量，取至小數點第 2 位。 |  |
| payload.lots[].riskTypes | Array | 庫存風險類型代碼清單；顯示文字由前端轉換。 | `EWarehouseRiskType` |
| payload.lots[].openTaskCount | Integer | 與此批號庫存相關的未完成倉庫任務數。 |  |
| payload.lots[].refCategory | Integer | 批號來源單據類別，來源為 `batch_number.refCategory`。 |  |
| payload.lots[].refNo | String | 批號來源單號，來源為 `batch_number.ref_no`。 |  |
| payload.lots[].qualityStatus | String | controlled staging path 的來源批號狀態代碼；一般模式不回傳此欄位。 |  |
| payload.lots[].sourceProvenanceRef | String | controlled staging path 的非正式測試來源證據識別；一般模式不回傳此欄位。 |  |

### Processing Flow

1. 檢查 request header 是否提供 `x-auth-token`，並套用既有 API token 流程。
2. 宣告本 API read-only 權限代碼為 `WH_INV_READ`。
3. 一般模式依查詢條件呼叫既有 Warehouse 庫存批號服務。
4. controlled staging path 僅在環境旗標 `ERP2_WH_INV_STAGING_MODE=1` 時啟用，從 `np_stg_lot_snapshot` 讀取批號庫存，並以 `np_xwalk_item_identity`、`np_xwalk_lot_identity`、`np_xwalk_uom` 補足料品、批號與 UOM 對照資訊。
5. controlled staging path 僅回傳 `validation_state = READY_FOR_READ_ONLY_API` 且來源或顯示數量大於 0 的資料列。
6. controlled staging path 若收到 `itemCategory` 篩選，因授權 `np_*` 欄位未提供正式料品類別，回傳空集合以避免錯誤分類。
7. 保留批號來源顯示單位，不進行單位換算或顯示文字轉換。

### Database Tables Used

| Table | Purpose |
|---|---|
| inventory_record | 批號庫存數量與入出庫紀錄。 |
| inventory_item_month_statistic | 月結庫存快照。 |
| inventory_delta | 月結後庫存異動。 |
| batch_number | 批號主檔與來源單據。 |
| warehouse_inventory_reservation | 預留數量與預留價值。 |
| warehouse_quality_hold | 品檢保留數量與保留價值。 |
| warehouse_pallet_movement | 板位佔用資訊。 |
| workflow_task_state | 未完成倉庫任務數。 |
| np_stg_lot_snapshot | controlled staging path 的批號庫存快照來源。 |
| np_xwalk_item_identity | controlled staging path 的料品 identity 對照來源。 |
| np_xwalk_lot_identity | controlled staging path 的批號 identity 對照來源。 |
| np_xwalk_uom | controlled staging path 的來源單位、顯示單位與候選標準單位 metadata。 |

## GET /api/v2/lots/{lot_code}/trace

<a id="get-api-v2-lots-lot-code-trace"></a>

### Basic Information

| URL | Method | Description |
|---|---|---|
| /api/v2/lots/{lot_code}/trace | GET | 查詢指定批號溯源資料 |

### Request Header

| Header | Description |
|---|---|
| x-auth-token | 存取金鑰。 |
| x-timezone | 時區代碼，例如 `Asia/Taipei`；未提供時使用 `UTC`。 |

### Query Parameters

None

### Request Body

None

### Controlled Staging Mode Note

本 API 在一般模式下維持既有 Traceability Center 查詢邏輯；於 `ERP2_WH_INV_STAGING_MODE=1` 時，啟用 `ERP2-API-WH-INV-STAGING-ALIGN-001` 受控非正式測試路徑。此路徑僅讀取授權七張 `np_*` 物件，不建立、不要求、也不寫入正式 ERP operational tables。

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "permissionCode": "String",
    "batch": {
      "batchNo": "String",
      "candidateBatchNo": "String",
      "itemNo": "String",
      "itemName": "String",
      "candidateItemNo": "String",
      "currentQuantity": "Float",
      "unit": "String",
      "status": "String",
      "snapshotBusinessDate": "String",
      "sourceProvenanceRef": "String"
    },
    "traceSteps": [{
      "stepId": "String",
      "stepType": "String",
      "refNo": "String",
      "eventTimestamp": "Integer",
      "warehouseNo": "String",
      "locationNo": "String",
      "quantity": "Float",
      "unit": "String",
      "validationState": "String",
      "sourceProvenanceRef": "String"
    }]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
|---|---|---|---|
| payload.serverTimestamp | Integer | Response 產生時間，UTC timestamp。 |  |
| payload.permissionCode | String | 此 read-only API 對應的權限代碼。 | `WH_INV_READ` |
| payload.batch.batchNo | String | 查詢批號，controlled staging path 來源為 `np_xwalk_lot_identity.source_lot_code`。 |  |
| payload.batch.candidateBatchNo | String | 候選批號，controlled staging path 來源為 `np_xwalk_lot_identity.candidate_lot_code`。 |  |
| payload.batch.itemNo | String | 來源料品 no。 |  |
| payload.batch.itemName | String | 來源料品名稱。 |  |
| payload.batch.candidateItemNo | String | 候選標準料品 no。 |  |
| payload.batch.currentQuantity | Float | 批號目前來源庫存數量，取至小數點第 2 位。 |  |
| payload.batch.unit | String | 批號來源顯示單位；保留 UOM Option B，不進行換算。 |  |
| payload.batch.status | String | 來源批號狀態或 identity 對照狀態。 |  |
| payload.batch.snapshotBusinessDate | String | 批號快照業務日期，格式 `YYYY-MM-DD`。 |  |
| payload.batch.sourceProvenanceRef | String | controlled staging path 的非正式測試來源證據識別。 |  |
| payload.traceSteps[].stepId | String | 批號關聯 staging 異動識別值。 |  |
| payload.traceSteps[].stepType | String | 來源異動類型，例如 `RECEIPT`、`ISSUE`、`TRANSFER`。 |  |
| payload.traceSteps[].refNo | String | 來源文件識別值。 |  |
| payload.traceSteps[].eventTimestamp | Integer | 來源異動時間，UTC timestamp；無時間時回傳 0。 |  |
| payload.traceSteps[].warehouseNo | String | 倉庫代碼。 |  |
| payload.traceSteps[].locationNo | String | 來源或目的庫位代碼。 |  |
| payload.traceSteps[].quantity | Float | 異動來源數量，取至小數點第 2 位。 |  |
| payload.traceSteps[].unit | String | 異動來源顯示單位；保留 UOM Option B，不進行換算。 |  |
| payload.traceSteps[].validationState | String | staging 異動資料驗證狀態。 |  |
| payload.traceSteps[].sourceProvenanceRef | String | controlled staging path 的非正式測試來源證據識別。 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|---|---|---|---|
| code | Integer | API 錯誤代碼。 | `EErrorCode` |
| message | String | API 錯誤訊息；查無批號時回傳 `record not found`。 |  |
| payload | Object | 錯誤時多為空物件。 |  |

### Processing Flow

1. 檢查 request header 是否提供 `x-auth-token`，並套用既有 API token 流程。
2. 宣告本 API read-only 權限代碼為 `WH_INV_READ`。
3. 一般模式以 `{lot_code}` 作為批號查詢條件，呼叫既有 Traceability Center 批號總覽服務。
4. controlled staging path 僅在環境旗標 `ERP2_WH_INV_STAGING_MODE=1` 時啟用，從 `np_xwalk_lot_identity` 查詢指定批號，並以 `np_stg_lot_snapshot`、`np_xwalk_item_identity`、`np_xwalk_uom` 補足批號總覽。
5. controlled staging path 從 `np_stg_inventory_movement` 查詢同一批號的 `READY_FOR_READ_ONLY_API` 異動資料，組成受控溯源步驟。
6. 若查無批號，回傳既有錯誤合約。
7. 若查詢成功，回傳批號主檔與溯源步驟；不新增交易、調整或任何資料異動。

### Database Tables Used

| Table | Purpose |
|---|---|
| batch_number | 批號主檔與來源單據。 |
| inventory_record | 批號庫存與異動證據。 |
| production_data | 生產工單與批號關聯。 |
| production_data_input | 生產投入批號。 |
| production_data_output | 生產產出批號。 |
| warehouse_quality_hold | 品檢保留狀態。 |
| workflow_task_event | 批號相關事件時間。 |
| np_xwalk_lot_identity | controlled staging path 的批號 identity 對照來源。 |
| np_xwalk_item_identity | controlled staging path 的料品 identity 對照來源。 |
| np_stg_lot_snapshot | controlled staging path 的批號庫存快照來源。 |
| np_stg_inventory_movement | controlled staging path 的批號異動與溯源步驟來源。 |
| np_xwalk_uom | controlled staging path 的來源單位、顯示單位與候選標準單位 metadata。 |

## GET /api/v1/inventory/items

<a id="get-api-v1-inventory-items"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/inventory/items | GET | 查詢庫存 / 品項清單 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| commit | String | NO | 是否提交/確認統計條件 |
| date | String | NO | 日期 |
| end_time | String | NO | 查詢結束時間 |
| itemCategory | String | NO | 料品類別 |
| item_no | String | NO | 「料品品項」編號 |
| start_time | String | NO | 查詢開始時間 |
| type | String | NO | 類型篩選 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "total": "Integer",
    "results": [
      {
        "kind": "Integer",
        "specified_no": "String",
        "specified_name": "String",
        "specified_ref_no": "String",
        "beginCount": "Float",
        "beginAmount": "Float",
        "inCount": "Float",
        "inAmount": "Float",
        "outCount": "Float",
        "outAmount": "Float",
        "endCount": "Float",
        "endAmount": "Float",
        "itemCategory": "Integer",
        "itemSubCategory": "Integer",
        "unit": "Integer",
        "price": "Float",
        "nearExpiryCount": "Float",
        "nearExpiryAmount": "Float",
        "expiredCount": "Float",
        "expiredAmount": "Float",
        "batchNo": [
          {
            "specified_no": "String",
            "specified_name": "String",
            "specified_ref_no": "String",
            "endCount": "Float",
            "endAmount": "Float",
            "validDate": "Integer",
            "itemType": "Integer"
          }
        ]
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.results[].kind | Integer | 庫存統計類型 |  |
| payload.results[].specified_no | String | 指定料品或批號編號 |  |
| payload.results[].specified_name | String | 指定料品或批號名稱 |  |
| payload.results[].specified_ref_no | String | 指定料品參照編號 |  |
| payload.results[].beginCount | Float | 期初庫存數量 |  |
| payload.results[].beginAmount | Float | 期初庫存金額 |  |
| payload.results[].inCount | Float | 入庫數量 |  |
| payload.results[].inAmount | Float | 入庫金額 |  |
| payload.results[].outCount | Float | 出庫數量 |  |
| payload.results[].outAmount | Float | 出庫金額 |  |
| payload.results[].endCount | Float | 期末庫存數量 |  |
| payload.results[].endAmount | Float | 期末庫存金額 |  |
| payload.results[].itemCategory | Integer | 料品類別 |  |
| payload.results[].itemSubCategory | Integer | 料品子類別 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].price | Float | 單價 |  |
| payload.results[].nearExpiryCount | Float | 即期庫存數量 |  |
| payload.results[].nearExpiryAmount | Float | 即期庫存金額 |  |
| payload.results[].expiredCount | Float | 已過期庫存數量 |  |
| payload.results[].expiredAmount | Float | 已過期庫存金額 |  |
| payload.results[].batchNo[].specified_no | String | 指定料品或批號編號 |  |
| payload.results[].batchNo[].specified_name | String | 指定料品或批號名稱 |  |
| payload.results[].batchNo[].specified_ref_no | String | 指定料品參照編號 |  |
| payload.results[].batchNo[].endCount | Float | 期末庫存數量 |  |
| payload.results[].batchNo[].endAmount | Float | 期末庫存金額 |  |
| payload.results[].batchNo[].validDate | Integer | 效期日期 |  |
| payload.results[].batchNo[].itemType | Integer | 料品類型 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：commit、date、end_time、itemCategory、item_no、start_time、type
2. 取得庫存 / 品項清單資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

None

## GET /api/v1/inventory/months

<a id="get-api-v1-inventory-months"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/inventory/months | GET | 查詢庫存 / 月資料 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| end_time | String | NO | 查詢結束時間 |
| start_time | String | NO | 查詢開始時間 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "total": "Integer",
    "results": [
      {
        "id": "Integer",
        "warehouse_no": "String",
        "warehouse_displayName": "String",
        "date": "String",
        "timezone": "String",
        "category": "Integer",
        "startAmount": "Float",
        "inAmount": "Float",
        "outAmount": "Float",
        "inPurchaseAmount": "Float",
        "endAmount": "Float",
        "creationTime": "Integer"
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].warehouse_no | String | 倉庫no，關連至ship_wh_alias |  |
| payload.results[].warehouse_displayName | String | 倉儲別名名稱，關聯至ship_wh_alias資料表 |  |
| payload.results[].date | String | 日期時間 |  |
| payload.results[].timezone | String | 用戶端時區 |  |
| payload.results[].category | Integer | 類別 |  |
| payload.results[].startAmount | Float | 期初庫存價值 (含稅價，小數點4位) |  |
| payload.results[].inAmount | Float | 入庫金額 |  |
| payload.results[].outAmount | Float | 出庫金額 |  |
| payload.results[].inPurchaseAmount | Float | 採購累計庫存價值 (含稅價，小數點4位) |  |
| payload.results[].endAmount | Float | 期末庫存金額 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：end_time、start_time
2. 查詢 inventory_month_statistic 取得庫存 / 月資料資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| inventory_month_statistic | 提供庫存查詢、統計或紀錄資料 |

## GET /api/v1/inventory/price

<a id="get-api-v1-inventory-price"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/inventory/price | GET | 查詢庫存 / 價格 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | Integer | NO | 分頁筆數 |
| start | Integer | NO | 分頁起始位置 |
| type | Integer | YES | 類型篩選 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "total": "Integer",
    "results": [
      {
        "contract": {
          "contract": {
            "displayName": "String",
            "category": "String",
            "type": "String",
            "itemStyle": "String",
            "unit": "String",
            "price": "String",
            "comment": "String"
          }
        }
      }
    ],
    "count": "Integer"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.results[].contract.contract.displayName | String | 顯示名稱 |  |
| payload.results[].contract.contract.category | String | 類別 |  |
| payload.results[].contract.contract.type | String | 類型 |  |
| payload.results[].contract.contract.itemStyle | String | 品項樣式 |  |
| payload.results[].contract.contract.unit | String | 單位 |  |
| payload.results[].contract.contract.price | String | 單價 |  |
| payload.results[].contract.contract.comment | String | 備註 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start、type
2. 查詢 item_price、trans_items 取得庫存 / 價格資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| item_price | 提供庫存查詢、統計或紀錄資料 |
| trans_items | 提供庫存查詢、統計或紀錄資料 |

## GET /api/v1/inventory/statistics

<a id="get-api-v1-inventory-statistics"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/inventory/statistics | GET | 查詢庫存 / 統計 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| batchNumber | String | YES | 批號 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "results": {
      "warehouse": [
        {
          "id": "Integer",
          "creator_no": "String",
          "group": "String",
          "refCategory": "Integer",
          "ref_no": "String",
          "warehouse_no": "String",
          "warehouse_displayName": "String",
          "date": "Integer",
          "category": "Integer",
          "source": "Integer",
          "batchNumber": "String",
          "serialNo": "String",
          "item_no": "String",
          "item_name": "String",
          "item_ref_no": "String",
          "item_ref_displayName": "String",
          "itemCategory": "Integer",
          "itemType": "Integer",
          "unit": "Integer",
          "count": "Float",
          "price": "Float",
          "amount": "Integer",
          "comment": "String",
          "registerDevId": "String",
          "creationTime": "Integer"
        }
      ]
    }
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.results.warehouse[].id | Integer | 資料 ID |  |
| payload.results.warehouse[].creator_no | String | 製單人員編號 |  |
| payload.results.warehouse[].group | String | 群組編號 |  |
| payload.results.warehouse[].refCategory | Integer | 來源類別 |  |
| payload.results.warehouse[].ref_no | String | 來源單號 |  |
| payload.results.warehouse[].warehouse_no | String | 倉庫no，關連至ship_wh_alias |  |
| payload.results.warehouse[].warehouse_displayName | String | 倉儲別名名稱，關聯至ship_wh_alias資料表 |  |
| payload.results.warehouse[].date | Integer | 日期時間 |  |
| payload.results.warehouse[].category | Integer | 類別 |  |
| payload.results.warehouse[].source | Integer | 源由 |  |
| payload.results.warehouse[].batchNumber | String | 出入庫批號 |  |
| payload.results.warehouse[].serialNo | String | 流水號 |  |
| payload.results.warehouse[].item_no | String | 「料品品項」編號 |  |
| payload.results.warehouse[].item_name | String | 「料品品項」名稱 |  |
| payload.results.warehouse[].item_ref_no | String | 交易對象編號 |  |
| payload.results.warehouse[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results.warehouse[].itemCategory | Integer | 料品類別 |  |
| payload.results.warehouse[].itemType | Integer | 料品類型 |  |
| payload.results.warehouse[].unit | Integer | 單位 |  |
| payload.results.warehouse[].count | Float | 本次回傳筆數 |  |
| payload.results.warehouse[].price | Float | 單價 |  |
| payload.results.warehouse[].amount | Integer | 金額或需求量 |  |
| payload.results.warehouse[].comment | String | 備註 |  |
| payload.results.warehouse[].registerDevId | String | 註冊之設備ID |  |
| payload.results.warehouse[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：batchNumber
2. 查詢 inventory_record 取得庫存 / 統計資料
3. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| inventory_record | 提供庫存查詢、統計或紀錄資料 |
