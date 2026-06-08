# product API Group

> Source: `restserver/package/restserver/api/product_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/product](#get-api-v1-product) | GET | 查詢製成品 | OK | OK |

## GET /api/v1/product

<a id="get-api-v1-product"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/product | GET | 查詢製成品 |

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
        "no": "String",
        "name": "String",
        "category": "Integer",
        "unitShipping": "Integer",
        "unitWarehouse": "Integer",
        "unitProduct": "Integer",
        "version": "Integer",
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
| payload.results[].no | String | 編號 |  |
| payload.results[].name | String | 名稱 |  |
| payload.results[].category | Integer | 類型 | 散裝品 (1)、組裝品 (2)、其他 (0)  |
| payload.results[].version | Integer | 版本 |  |
| payload.results[].unitShipping | Integer | 貨運單位 |  |
| payload.results[].unitWarehouse | Integer | 倉儲單位 |  |
| payload.results[].unitProduct | Integer | 	產製單位 |  |
| payload.results[].comment | String | 備註 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 product 取得製成品資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| product | 提供製成品主檔、配方或價格資料 |
