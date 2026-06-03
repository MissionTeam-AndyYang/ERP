# aps API Group

> Source: `restserver/package/restserver/api/aps_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/aps/quantity](#get-api-v1-aps-quantity) | GET | 查詢APS 資料 / 製造需求數量 | OK | OK |

## GET /api/v1/aps/quantity

<a id="get-api-v1-aps-quantity"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/aps/quantity | GET | 查詢APS 資料 / 製造需求數量 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | Integer | NO | 分頁筆數 |
| start | Integer | NO | 分頁起始位置 |

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
        "no": "String",
        "product_order_no": "String",
        "oneProcess": "Integer",
        "secProcess": "Integer",
        "item_no": "String",
        "item_name": "String",
        "itemCategory": "Integer",
        "unit": "Integer",
        "amount": "Float",
        "minutes": "Integer",
        "laborCount": "Integer",
        "creationTime": "Integer"
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
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].no | String | 資料編號 |  |
| payload.results[].product_order_no | String | 訂購單號 |  |
| payload.results[].oneProcess | Integer | 主製程 |  |
| payload.results[].secProcess | Integer | 次製程 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | 料品/品項名稱 |  |
| payload.results[].itemCategory | Integer | 料品類別 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].amount | Float | 金額或需求量 |  |
| payload.results[].minutes | Integer | 分鐘數 |  |
| payload.results[].laborCount | Integer | 人力需求數 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 aps_quantity、contract、product_order 取得APS 資料 / 製造需求數量資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| aps_quantity | 提供APS排程、生產或產能資料 |
| contract | 提供APS排程、生產或產能資料 |
| product_order | 提供APS排程、生產或產能資料 |
