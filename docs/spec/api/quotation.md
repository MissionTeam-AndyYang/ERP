# quotation API Group

> Source: `restserver/package/restserver/api/quotation_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/quotation](#get-api-v1-quotation) | GET | 查詢報價 | OK | OK |

## GET /api/v1/quotation

<a id="get-api-v1-quotation"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/quotation | GET | 查詢報價 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | Integer | NO | 分頁筆數 |
| start | Integer | NO | 分頁起始位置 |
| type | Integer | NO | 類型篩選 |

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
        "date": "Integer",
        "category": "Integer",
        "type": "Integer",
        "itemStyle": "Integer",
        "item_ref_no": "String",
        "item_ref_displayName": "String",
        "item_no": "String",
        "item_name": "String",
        "unit": "Integer",
        "price": "Float",
        "count": "Float",
        "amount": "Float",
        "comment": "String",
        "creationTime": "Integer",
        "transItemCategory": "Integer",
        "transItemAttr": "Integer",
        "paymentType": "Integer",
        "paymentDate": "Integer",
        "paymentPeriod": "Integer",
        "unitWarehouse": "Integer"
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
| payload.results[].no | String | 編號篩選 |  |
| payload.results[].date | Integer | 日期 |  |
| payload.results[].category | Integer | 類別篩選 |  |
| payload.results[].type | Integer | 類型篩選 |  |
| payload.results[].itemStyle | Integer | 品項樣式 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | item_name 回傳欄位 |  |
| payload.results[].unit | Integer | unit 回傳欄位 |  |
| payload.results[].price | Float | price 回傳欄位 |  |
| payload.results[].count | Float | 本次回傳筆數 |  |
| payload.results[].amount | Float | amount 回傳欄位 |  |
| payload.results[].comment | String | comment 回傳欄位 |  |
| payload.results[].creationTime | Integer | creationTime 回傳欄位 |  |
| payload.results[].transItemCategory | Integer | transItemCategory 回傳欄位 |  |
| payload.results[].transItemAttr | Integer | transItemAttr 回傳欄位 |  |
| payload.results[].paymentType | Integer | paymentType 回傳欄位 |  |
| payload.results[].paymentDate | Integer | paymentDate 回傳欄位 |  |
| payload.results[].paymentPeriod | Integer | paymentPeriod 回傳欄位 |  |
| payload.results[].unitWarehouse | Integer | unitWarehouse 回傳欄位 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start、type
2. 查詢資料表並套用條件：company、payment
3. 組裝回傳 payload 欄位：payload.total、payload.results[].id、payload.results[].no、payload.results[].date、payload.results[].category、payload.results[].type、payload.results[].itemStyle、payload.results[].item_ref_no、payload.results[].item_ref_displayName、payload.results[].item_no、payload.results[].item_name、payload.results[].unit、payload.results[].price、payload.results[].count、payload.results[].amount、payload.results[].comment、payload.results[].creationTime、payload.results[].transItemCategory、payload.results[].transItemAttr、payload.results[].paymentType、payload.results[].paymentDate、payload.results[].paymentPeriod、payload.results[].unitWarehouse、payload.count

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 提供報價單據、合約、帳款或統計資料 |
| payment | 提供報價單據、合約、帳款或統計資料 |
