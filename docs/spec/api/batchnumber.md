# batchnumber API Group

> Source: `restserver/package/restserver/api/batchnumber_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/batchnumber](#get-api-v1-batchnumber) | GET | 查詢批號 | OK | OK |

## GET /api/v1/batchnumber

<a id="get-api-v1-batchnumber"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/batchnumber | GET | 查詢批號 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | String | NO | 分頁筆數 |
| info | String | NO | 附加資訊類型 |
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
        "creationTime": "Integer",
        "serialNo": [
          {
            "serialNo": "String",
            "count": "Integer"
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
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].date | Integer | 日期 |  |
| payload.results[].no | String | 編號篩選 |  |
| payload.results[].creator_no | String | creator_no 回傳欄位 |  |
| payload.results[].ref_no | String | ref_no 回傳欄位 |  |
| payload.results[].refCategory | Integer | refCategory 回傳欄位 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | item_name 回傳欄位 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].itemCategory | Integer | 料品類別 |  |
| payload.results[].itemSubCategory | Integer | itemSubCategory 回傳欄位 |  |
| payload.results[].itemType | Integer | 料品類型 |  |
| payload.results[].unit | Integer | unit 回傳欄位 |  |
| payload.results[].expectedCount | Float | expectedCount 回傳欄位 |  |
| payload.results[].checkedCount | Float | checkedCount 回傳欄位 |  |
| payload.results[].validDays | Integer | validDays 回傳欄位 |  |
| payload.results[].validDate | Integer | validDate 回傳欄位 |  |
| payload.results[].validDateNo | String | validDateNo 回傳欄位 |  |
| payload.results[].comment | String | comment 回傳欄位 |  |
| payload.results[].creationTime | Integer | creationTime 回傳欄位 |  |
| payload.results[].serialNo[].serialNo | String | 流水號 |  |
| payload.results[].serialNo[].count | Integer | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、info、start、type
2. 查詢資料表並套用條件：batch_number
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results[].id、payload.results[].date、payload.results[].no、payload.results[].creator_no、payload.results[].ref_no、payload.results[].refCategory、payload.results[].item_no、payload.results[].item_name、payload.results[].item_ref_no、payload.results[].item_ref_displayName、payload.results[].itemCategory、payload.results[].itemSubCategory、payload.results[].itemType、payload.results[].unit、payload.results[].expectedCount、payload.results[].checkedCount、payload.results[].validDays、payload.results[].validDate、payload.results[].validDateNo、payload.results[].comment、payload.results[].creationTime、payload.results[].serialNo[].serialNo、payload.results[].serialNo[].count

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 提供批號相關資料 |
