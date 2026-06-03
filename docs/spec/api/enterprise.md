# enterprise API Group

> Source: `restserver/package/restserver/api/enterprise_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/enterprise](#get-api-v1-enterprise) | GET | 查詢企業 | OK | OK |

## GET /api/v1/enterprise

<a id="get-api-v1-enterprise"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/enterprise | GET | 查詢企業 |

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
        "businessNo": "String",
        "displayName": "String",
        "name": "String",
        "address": "String",
        "phone": "String",
        "fax": "String",
        "department": "Integer",
        "lar": "String",
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
| payload.results[].no | String | 資料編號 |  |
| payload.results[].businessNo | String | 統一編號或商業識別編號 |  |
| payload.results[].displayName | String | 顯示名稱 |  |
| payload.results[].name | String | 名稱 |  |
| payload.results[].address | String | 地址 |  |
| payload.results[].phone | String | 電話 |  |
| payload.results[].fax | String | 傳真 |  |
| payload.results[].department | Integer | 部門 |  |
| payload.results[].lar | String | 公司法人代表 |  |
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
2. 查詢 enterprise 取得企業資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| enterprise | 提供企業相關資料 |
