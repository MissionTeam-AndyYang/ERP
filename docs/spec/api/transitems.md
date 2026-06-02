# transitems API Group

> Source: `restserver/package/restserver/api/transitems_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/transitems](#get-api-v1-transitems) | GET | 查詢交易品項 | OK | OK |
| [/api/v1/transitems/item](#get-api-v1-transitems-item) | GET | 查詢交易品項 / 品項 | OK | OK |

## GET /api/v1/transitems

<a id="get-api-v1-transitems"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/transitems | GET | 查詢交易品項 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| category | Integer | NO | 類別篩選 |
| count | String | NO | 分頁筆數 |
| start | String | NO | 分頁起始位置 |
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
    "count": "Integer",
    "results": [
      {
        "item": {},
        "paidPayment": {},
        "receivedPayment": {}
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

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：category、count、start、type
2. 查詢資料表並套用條件：company、payment、trans_items、trans_items2
3. 組裝回傳 payload 欄位：payload.total、payload.count

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 提供交易品項主檔、配方或價格資料 |
| payment | 提供交易品項主檔、配方或價格資料 |
| trans_items | 提供交易品項主檔、配方或價格資料 |
| trans_items2 | 提供交易品項主檔、配方或價格資料 |

## GET /api/v1/transitems/item

<a id="get-api-v1-transitems-item"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/transitems/item | GET | 查詢交易品項 / 品項 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| item_no | String | YES | 料品/品項編號 |

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
        "transItem": {
          "id": "Integer",
          "no": "String",
          "name": "String",
          "category": "Integer",
          "attribute": "Integer",
          "company_no": "String",
          "company_displayName": "String",
          "item_no": "String",
          "item_name": "String",
          "comment": "String",
          "creationTime": "Integer"
        },
        "paidPayment": {},
        "receivedPayment": {}
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
| payload.results[].transItem.id | Integer | 資料 ID |  |
| payload.results[].transItem.no | String | 編號篩選 |  |
| payload.results[].transItem.name | String | 名稱 |  |
| payload.results[].transItem.category | Integer | 類別篩選 |  |
| payload.results[].transItem.attribute | Integer | attribute 回傳欄位 |  |
| payload.results[].transItem.company_no | String | company_no 回傳欄位 |  |
| payload.results[].transItem.company_displayName | String | company_displayName 回傳欄位 |  |
| payload.results[].transItem.item_no | String | 料品/品項編號 |  |
| payload.results[].transItem.item_name | String | item_name 回傳欄位 |  |
| payload.results[].transItem.comment | String | comment 回傳欄位 |  |
| payload.results[].transItem.creationTime | Integer | creationTime 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：item_no
2. 查詢資料表並套用條件：company、payment、trans_items
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results[].transItem.id、payload.results[].transItem.no、payload.results[].transItem.name、payload.results[].transItem.category、payload.results[].transItem.attribute、payload.results[].transItem.company_no、payload.results[].transItem.company_displayName、payload.results[].transItem.item_no、payload.results[].transItem.item_name、payload.results[].transItem.comment、payload.results[].transItem.creationTime

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 提供交易品項主檔、配方或價格資料 |
| payment | 提供交易品項主檔、配方或價格資料 |
| trans_items | 提供交易品項主檔、配方或價格資料 |
