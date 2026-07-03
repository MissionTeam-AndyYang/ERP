# Warehouse Inventory Movement Ledger API Proposal

> Status: Proposal / Pending Engineer Review
> Target UI Preview: `docs/spec/api-proposal/warehouse_inventory_movement_ledger_static_preview.html`
> Flow / Algorithm: `docs/spec/api-proposal/warehouse_inventory_movement_ledger_flow_algorithm.md`
> Related V1 Rule: Warehouse V1 frontend is read-only; this proposal contains GET APIs only.

## Screen Intent

`WarehouseInventoryMovementLedgerScreen` 是 `WarehouseAnalyticsScreen` 後建議的下一個 read-only 畫面。此畫面用於查詢「庫存異動流水帳」，協助管理者、倉庫主管與工程師確認庫存數量、庫存價值、批號來源與入出庫紀錄是否一致。

此畫面回答以下問題：

1. 某個期間內，指定倉庫、料品、批號或來源單據發生了哪些入庫、出庫或調整異動？
2. 庫存價值趨勢變動時，可以追溯到哪些 `inventory_record` 明細？
3. 批號明細中的目前庫存，是由哪些入庫紀錄累積、又被哪些出庫紀錄扣減？
4. 任務工作台或 Analytics drill-down 時，能否用同一組條件追溯到實際庫存異動？

本提案不包含庫存調整、入庫確認、出庫確認、移倉執行、任務完成或任何 POST / PUT / DELETE API。若後續需要執行庫存異動，應延至 V2 mutation API 設計。

## API Summary

| URL | Method | Description | Status | Review Note |
| --- | --- | --- | --- | --- |
| `/api/v2/warehouse/inventory/movements` | GET | 查詢庫存異動流水帳明細 | Proposal / Pending Engineer Review | 以 `inventory_record` 為主要資料來源，支援期間、倉庫、料品、批號、來源單據、異動方向、排序與分頁。 |
| `/api/v2/warehouse/inventory/movements/summary` | GET | 查詢庫存異動摘要 | Proposal / Pending Engineer Review | 以同一組篩選條件回傳入庫、出庫、淨異動與異動筆數摘要，供頁面 KPI 與圖表使用。 |

## Shared Query Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| date | Integer | NO | 查詢基準/截止時間，UTC timestamp；未提供時使用伺服器目前時間。 |
| period | String | NO | 查詢期間代碼；第一版建議支援 `7d`、`30d`、`90d`，預設 `30d`。 |
| bucket | String | NO | 摘要趨勢粒度；第一版支援 `day`、`week`、`month`，預設 `day`。 |
| warehouse_no | String | NO | 倉儲別名 no；對應 `inventory_record.warehouse_no` / `ship_wh_alias.no`。 |
| itemCategory | Integer | NO | 料品品項類別；原料(1)、物料(2)、膠捲(3)、在製品(4)、製成品(5)。 |
| item_no | String | NO | 料品 no；對應 `inventory_record.item_no`。 |
| batchNo | String | NO | 批號；對應 `inventory_record.batchNumber` 與 `batch_number.no`。 |
| refCategory | Integer | NO | 來源單據類別；對應 `inventory_record.refCategory`。 |
| ref_no | String | NO | 來源單據 no；對應 `inventory_record.ref_no`。 |
| category | Integer | NO | 庫存異動方向；對應 `inventory_record.category`，例如入庫(1)、出庫(2)。 |
| keyword | String | NO | 關鍵字；第一版可搜尋 `item_no`、`item_name`、`batchNumber`、`ref_no`。 |
| sort | String | NO | 排序欄位；允許 `date`、`item_no`、`batchNo`、`quantity`、`amount`，預設 `date`。 |
| order | String | NO | 排序方向；允許 `asc`、`desc`，預設 `desc`。 |
| start | Integer | NO | 分頁起始位置，預設 0。 |
| count | Integer | NO | 分頁筆數，預設 50，第一版上限 100。 |

## Numeric Format Rules

| Numeric Meaning | Format |
| --- | --- |
| 單價 | 四捨五入取至小數點第 4 位 |
| 重量或數量 | 四捨五入取至小數點第 2 位 |
| 金額 | 四捨五入取整數 |

## GET /api/v2/warehouse/inventory/movements

### Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v2/warehouse/inventory/movements` | GET | 查詢庫存異動流水帳明細 |

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "timezone": "String",
    "range": {
      "period": "String",
      "bucket": "String",
      "startTimestamp": "Integer",
      "endTimestamp": "Integer"
    },
    "pagination": {
      "start": "Integer",
      "count": "Integer",
      "total": "Integer",
      "hasMore": "Boolean"
    },
    "summary": {
      "movementCount": "Integer",
      "inboundQuantity": "Float",
      "outboundQuantity": "Float",
      "netQuantity": "Float",
      "inboundValue": "Integer",
      "outboundValue": "Integer",
      "netValue": "Integer"
    },
    "results": [
      {
        "movementId": "Integer",
        "movementTimestamp": "Integer",
        "warehouseNo": "String",
        "warehouseName": "String",
        "itemNo": "String",
        "itemName": "String",
        "itemCategory": "Integer",
        "itemType": "Integer",
        "batchNo": "String",
        "category": "Integer",
        "refCategory": "Integer",
        "refNo": "String",
        "serialNo": "String",
        "quantity": "Float",
        "unit": "Integer",
        "unitCost": "Float",
        "amount": "Integer",
        "sourceTable": "String",
        "sourceId": "Integer",
        "batchRefCategory": "Integer",
        "batchRefNo": "String",
        "comment": "String"
      }
    ]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
| --- | --- | --- | --- |
| payload.serverTimestamp | Integer | 後端產生 response 的 UTC timestamp。 |  |
| payload.timezone | String | 後端採用的時區代碼；預設可依 `x-timezone` header 或 UTC 回傳。 |  |
| payload.range.period | String | 實際採用的查詢期間代碼。 |  |
| payload.range.bucket | String | 實際採用的趨勢粒度。 |  |
| payload.range.startTimestamp | Integer | 本次查詢起始 UTC timestamp，由 `date - period` 推算。 |  |
| payload.range.endTimestamp | Integer | 本次查詢截止 UTC timestamp，由 request `date` 或伺服器目前時間決定。 |  |
| payload.pagination.start | Integer | 本次分頁起始位置。 |  |
| payload.pagination.count | Integer | 本次分頁回傳筆數。 |  |
| payload.pagination.total | Integer | 符合查詢條件的總筆數。 |  |
| payload.pagination.hasMore | Boolean | 是否仍有下一頁資料。 |  |
| payload.summary.movementCount | Integer | 符合查詢條件的庫存異動筆數。 |  |
| payload.summary.inboundQuantity | Float | 入庫方向異動數量加總；混合單位情境下僅供同條件內參考。 |  |
| payload.summary.outboundQuantity | Float | 出庫方向異動數量加總；混合單位情境下僅供同條件內參考。 |  |
| payload.summary.netQuantity | Float | 淨異動數量；公式為 `inboundQuantity - outboundQuantity`。 |  |
| payload.summary.inboundValue | Integer | 入庫方向異動金額加總。 |  |
| payload.summary.outboundValue | Integer | 出庫方向異動金額加總。 |  |
| payload.summary.netValue | Integer | 淨異動金額；公式為 `inboundValue - outboundValue`。 |  |
| payload.results[].movementId | Integer | 庫存異動紀錄 ID，來源為 `inventory_record.id`。 |  |
| payload.results[].movementTimestamp | Integer | 異動時間，來源為 `inventory_record.date`；若為 0 才可 fallback 至 `creationTime`。 |  |
| payload.results[].warehouseNo | String | 倉儲別名 no，來源為 `inventory_record.warehouse_no`。 |  |
| payload.results[].warehouseName | String | 倉儲名稱，優先使用 `inventory_record.warehouse_displayName`，缺漏時可由 `ship_wh_alias.name` 補齊。 |  |
| payload.results[].itemNo | String | 料品 no，來源為 `inventory_record.item_no`。 |  |
| payload.results[].itemName | String | 料品名稱，來源為 `inventory_record.item_name`。 |  |
| payload.results[].itemCategory | Integer | 料品品項類別，前端負責多國語系轉換。 | EItemCategory |
| payload.results[].itemType | Integer | 料品類型，來源為 `inventory_record.itemType`。 |  |
| payload.results[].batchNo | String | 批號，來源為 `inventory_record.batchNumber`。 |  |
| payload.results[].category | Integer | 庫存異動方向，來源為 `inventory_record.category`；前端負責 enum 顯示文字轉換。 | EInventoryCategory |
| payload.results[].refCategory | Integer | 異動來源單據類別，來源為 `inventory_record.refCategory`。 |  |
| payload.results[].refNo | String | 異動來源單據 no，來源為 `inventory_record.ref_no`。 |  |
| payload.results[].serialNo | String | 序號，來源為 `inventory_record.serialNo`。 |  |
| payload.results[].quantity | Float | 異動數量，來源為 `inventory_record.count`，固定回傳正值；方向由 `category` 判斷。 |  |
| payload.results[].unit | Integer | 數量單位代碼，來源為 `inventory_record.unit`；前端負責 enum 顯示文字轉換。 |  |
| payload.results[].unitCost | Float | 異動單價，優先來源為 `inventory_record.price`；若缺漏且 `count > 0`，可用 `amount / count` 補算。 |  |
| payload.results[].amount | Integer | 異動金額，來源為 `inventory_record.amount`，金額四捨五入取整數。 |  |
| payload.results[].sourceTable | String | 第一版固定回傳 `inventory_record`，供前端與工程師 debug 使用。 |  |
| payload.results[].sourceId | Integer | 第一版固定等於 `inventory_record.id`。 |  |
| payload.results[].batchRefCategory | Integer | 批號原始產生來源類別，來源為 `batch_number.refCategory`；若找不到批號資料回傳 0。 |  |
| payload.results[].batchRefNo | String | 批號原始產生來源單據 no，來源為 `batch_number.ref_no`；若找不到批號資料回傳空字串。 |  |
| payload.results[].comment | String | 異動備註，來源為 `inventory_record.comment`。 |  |

## GET /api/v2/warehouse/inventory/movements/summary

### Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v2/warehouse/inventory/movements/summary` | GET | 查詢庫存異動摘要 |

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "timezone": "String",
    "range": {
      "period": "String",
      "bucket": "String",
      "startTimestamp": "Integer",
      "endTimestamp": "Integer"
    },
    "summary": {
      "movementCount": "Integer",
      "inboundQuantity": "Float",
      "outboundQuantity": "Float",
      "netQuantity": "Float",
      "inboundValue": "Integer",
      "outboundValue": "Integer",
      "netValue": "Integer"
    },
    "trend": [
      {
        "bucketStart": "Integer",
        "bucketLabel": "String",
        "category": "Integer",
        "quantity": "Float",
        "amount": "Integer",
        "movementCount": "Integer"
      }
    ],
    "summaryByCategory": [
      {
        "itemCategory": "Integer",
        "inboundValue": "Integer",
        "outboundValue": "Integer",
        "netValue": "Integer",
        "movementCount": "Integer"
      }
    ]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
| --- | --- | --- | --- |
| payload.summary | Object | 使用與 movements list 相同篩選條件計算的總摘要。 |  |
| payload.trend[].bucketStart | Integer | 此趨勢 bucket 的起始 UTC timestamp。 |  |
| payload.trend[].bucketLabel | String | 前端圖表可顯示的 bucket 標籤。 |  |
| payload.trend[].category | Integer | 入庫或出庫方向，來源為 `inventory_record.category`。 | EInventoryCategory |
| payload.trend[].quantity | Float | 該 bucket、該異動方向的數量加總。 |  |
| payload.trend[].amount | Integer | 該 bucket、該異動方向的金額加總。 |  |
| payload.trend[].movementCount | Integer | 該 bucket、該異動方向的異動筆數。 |  |
| payload.summaryByCategory[].itemCategory | Integer | 料品品項類別，前端負責多國語系轉換。 | EItemCategory |
| payload.summaryByCategory[].inboundValue | Integer | 該料品品項類別入庫金額加總。 |  |
| payload.summaryByCategory[].outboundValue | Integer | 該料品品項類別出庫金額加總。 |  |
| payload.summaryByCategory[].netValue | Integer | 該料品品項類別淨異動金額。 |  |
| payload.summaryByCategory[].movementCount | Integer | 該料品品項類別異動筆數。 |  |

## Frontend Interaction Notes

| UI Action | API Behavior |
| --- | --- |
| 從 Analytics 庫存價值趨勢 drill-down | 前端帶入 `date`、`period`、`itemCategory` 呼叫 movements list 或 summary。 |
| 從批號明細 panel 的入出庫紀錄展開 | 前端帶入 `warehouse_no`、`item_no`、`batchNo` 呼叫 movements list。 |
| 搜尋來源單據 | 前端帶入 `ref_no` 或 `keyword` 呼叫 movements list。 |
| 切換入庫/出庫方向 | 前端帶入 `category` 呼叫 movements list 與 summary。 |
| 換頁或排序 | 前端調整 `start`、`count`、`sort`、`order`，後端需使用資料庫層分頁。 |

## Database Tables Used

| Table | Purpose |
| --- | --- |
| inventory_record | 主要庫存異動流水帳資料來源。 |
| batch_number | 補充批號原始產生來源 `batchRefCategory` / `batchRefNo`。 |
| ship_wh_alias | 補充倉儲名稱。 |
| workflow_task_state | 第一版不作主要 join；若後續需要從任務 drill-down，可只用 query 條件導向此 API。 |

## Engineer Review Questions

| 項目 | 需確認原因 | 工程師回覆 | Codex 建議 |
| --- | --- | --- | --- |
| 是否同意 Analytics 後下一個 read-only 畫面為 `WarehouseInventoryMovementLedgerScreen` | 確認 V1 下一步仍聚焦查詢與追溯，不進入 mutation。 | 待工程師回覆 | 建議採用，因可支援 Analytics、批號明細與任務追蹤的共同 drill-down。 |
| `category` 是否足以表示入庫/出庫方向 | 需確認 `inventory_record.category` enum 與現有資料一致。 | 待工程師回覆 | 建議第一版直接使用 `inventory_record.category`，不新增 `direction` 欄位。 |
| `batchRefCategory` / `batchRefNo` 是否需要回傳 | 可協助區分批號由採購進貨或產製流程產生。 | 待工程師回覆 | 建議保留，來源為 `batch_number.refCategory/ref_no`。 |
| summary 數量在混合單位時是否只作參考 | 多料品混合查詢時數量單位可能不同。 | 待工程師回覆 | 建議金額摘要作為主要分析指標；數量摘要僅在同料品或同單位篩選下精確解讀。 |
| 正式實作前是否先整合至 `docs/spec/api/warehouse.md` | 遵循 `docs/spec/design_coding.md`。 | 待工程師回覆 | 工程師確認後，正式實作前應先整合至正式 API 文件。 |
