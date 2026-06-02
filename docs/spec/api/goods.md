# goods API Group

> Source: `restserver/package/restserver/api/goods_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/goods](#get-api-v1-goods) | GET | 查詢貨品 | OK | OK |

## GET /api/v1/goods

<a id="get-api-v1-goods"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/goods | GET | 查詢貨品 |

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
    "count": "Integer",
    "results": [
      {
        "id": "Integer",
        "no": "String",
        "category": "Integer",
        "subCategory": "Integer",
        "name": "String",
        "unitShipping": "Integer",
        "unitWarehouse": "Integer",
        "unitProduct": "Integer",
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
| payload.results[].no | String | 編號篩選 |  |
| payload.results[].category | Integer | 類別篩選 |  |
| payload.results[].subCategory | Integer | 子類別篩選 |  |
| payload.results[].name | String | 名稱 |  |
| payload.results[].unitShipping | Integer | unitShipping 回傳欄位 |  |
| payload.results[].unitWarehouse | Integer | unitWarehouse 回傳欄位 |  |
| payload.results[].unitProduct | Integer | unitProduct 回傳欄位 |  |
| payload.results[].comment | String | comment 回傳欄位 |  |
| payload.results[].creationTime | Integer | creationTime 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start
2. 查詢資料表並套用條件：goods
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results[].id、payload.results[].no、payload.results[].category、payload.results[].subCategory、payload.results[].name、payload.results[].unitShipping、payload.results[].unitWarehouse、payload.results[].unitProduct、payload.results[].comment、payload.results[].creationTime

### Database Tables Used

| Table | Purpose |
|----------|------|
| goods | 提供貨品主檔、配方或價格資料 |
