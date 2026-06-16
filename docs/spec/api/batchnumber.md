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
| start | Integer | NO | 分頁起始位置 |
| count | Integer | NO | 分頁筆數 |
| info | Boolean | NO | 是否附加倉庫詳細資訊 |
| type | Integer | NO | 類型篩選: 1. 批號流水號資訊 |

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
        "stockType": "Integer",
        "serialNo": [
          {
            "serialNo": "String",
            "count": "Float"
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
| payload.results[].date | Integer | 日期時間 |  |
| payload.results[].no | String | 資料編號 |  |
| payload.results[].creator_no | String | 製單人員編號 |  |
| payload.results[].ref_no | String | 來源單號 |  |
| payload.results[].refCategory | Integer | 來源單號類別 |  |
| payload.results[].item_no | String | 「料品品項」項編號 |  |
| payload.results[].item_name | String | 「料品品項」名稱 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].itemCategory | Integer | 「料品品項」類別 |  |
| payload.results[].itemSubCategory | Integer | 「料品品項」子類別 |  |
| payload.results[].itemType | Integer | 「料品品項」類型 | 新料 (1)、餘料 (2)、廢料 (3) 、其他 (0) |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].expectedCount | Float | 預期數量 |  |
| payload.results[].checkedCount | Float | 已確認數量 |  |
| payload.results[].validDays | Integer | 有效天數 |  |
| payload.results[].validDate | Integer | 效期日期 |  |
| payload.results[].validDateNo | String | 效期日期編號 |  |
| payload.results[].comment | String | 備註 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |
| payload.results[].stockType | Integer | 批號庫存類型 | 即期品(1) 、 過期品 (2)|
| payload.results[].serialNo[].serialNo | String | 流水號 |  |
| payload.results[].serialNo[].count | Integer | 重量或數量 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、info、start、type
2. 查詢 batch_number 取得批號資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 提供批號相關資料 |
