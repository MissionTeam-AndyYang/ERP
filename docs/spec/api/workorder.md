# workorder API Group

> Source: `restserver/package/restserver/api/workorder_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/workorder](#get-api-v1-workorder) | GET | 查詢工單 | OK | OK |
| [/api/v1/workorder/expecteddata](#get-api-v1-workorder-expecteddata) | GET | 查詢工單 / 預期資料 | OK | OK |
| [/api/v1/workorder/productdata](#get-api-v1-workorder-productdata) | GET | 查詢工單 / 生產數據 | OK | OK |
| [/api/v1/workorder/statistics](#get-api-v1-workorder-statistics) | GET | 查詢工單 / 統計 | OK | OK |

## GET /api/v1/workorder

<a id="get-api-v1-workorder"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/workorder | GET | 查詢工單 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

None

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
        "work_order_no": "String",
        "process_order_no": "String",
        "group": "String",
        "time": "Integer",
        "action": "Integer",
        "item_no": "String",
        "item_name": "String",
        "category": "Integer",
        "itemSubCategory": "Integer",
        "batch_number": "String",
        "serial_no": "String",
        "valid_date": "Integer",
        "valid_date_no": "String",
        "unit": "Integer",
        "count": "Float",
        "comment": "String"
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
| payload.results[].work_order_no | String | 工單號 |  |
| payload.results[].process_order_no | String | 製程單號 |  |
| payload.results[].group | String | 群組編號 |  |
| payload.results[].time | Integer | 作業時間 |  |
| payload.results[].action | Integer | 作業方向 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | 料品/品項名稱 |  |
| payload.results[].category | Integer | 類別 |  |
| payload.results[].itemSubCategory | Integer | 料品子類別 |  |
| payload.results[].batch_number | String | 批號 |  |
| payload.results[].serial_no | String | 流水號 |  |
| payload.results[].valid_date | Integer | 有效期限 |  |
| payload.results[].valid_date_no | String | 有效期限編號 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].count | Float | 本次回傳筆數 |  |
| payload.results[].comment | String | 備註 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 查詢 production_data_output、work_order 取得工單資料
2. 計算符合條件的總筆數與本次回傳筆數
3. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| production_data_output | 提供工單排程、生產或產能資料 |
| work_order | 提供工單排程、生產或產能資料 |

## GET /api/v1/workorder/expecteddata

<a id="get-api-v1-workorder-expecteddata"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/workorder/expecteddata | GET | 查詢工單 / 預期資料 |

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
        "workOrderDate": "String",
        "production_line_no": "String",
        "productionLineName": "String",
        "category": "String",
        "date": "String",
        "item_no": "String",
        "item_name": "String",
        "itemCategory": "String",
        "itemSubCategory": "String",
        "unit": "String",
        "totalExpectedCount": "String",
        "batch_number": "String"
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
| payload.results[].workOrderDate | String | work Order Date 的業務資料 |  |
| payload.results[].production_line_no | String | 產線編號 |  |
| payload.results[].productionLineName | String | 產線名稱 |  |
| payload.results[].category | String | 類別 |  |
| payload.results[].date | String | 日期時間 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | 料品/品項名稱 |  |
| payload.results[].itemCategory | String | 料品類別 |  |
| payload.results[].itemSubCategory | String | 料品子類別 |  |
| payload.results[].unit | String | 單位 |  |
| payload.results[].totalExpectedCount | String | total Expected Count 的業務資料 |  |
| payload.results[].batch_number | String | 批號 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 batch_number、batchno_serialno、process_order、production_line 取得工單 / 預期資料資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 提供工單排程、生產或產能資料 |
| batchno_serialno | 提供工單排程、生產或產能資料 |
| process_order | 提供工單排程、生產或產能資料 |
| production_line | 提供工單排程、生產或產能資料 |
| work_order | 提供工單排程、生產或產能資料 |

## GET /api/v1/workorder/productdata

<a id="get-api-v1-workorder-productdata"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/workorder/productdata | GET | 查詢工單 / 生產數據 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | Integer | NO | 分頁筆數 |
| start | Integer | NO | 分頁起始位置 |
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
        "no": "String",
        "date": "String",
        "production_line_no": "String",
        "productionLineName": "String",
        "output_item_no": "String",
        "output_item_name": "String",
        "oneProcess": "String",
        "secProcess": "String",
        "input": [
          {
            "id": "Integer",
            "no": "String",
            "name": "String",
            "sex": "Integer",
            "department": "Integer",
            "level": "Integer",
            "jobTitle": "String",
            "joinedDate": "Integer",
            "leftDate": "Integer",
            "identityId": "String",
            "country": "String",
            "birthday": "Integer",
            "phone": "String",
            "address": "String",
            "type": "Integer",
            "category": "Integer",
            "comment": "String",
            "creationTime": "Integer"
          }
        ],
        "output": [
          {
            "id": "Integer",
            "no": "String",
            "name": "String",
            "sex": "Integer",
            "department": "Integer",
            "level": "Integer",
            "jobTitle": "String",
            "joinedDate": "Integer",
            "leftDate": "Integer",
            "identityId": "String",
            "country": "String",
            "birthday": "Integer",
            "phone": "String",
            "address": "String",
            "type": "Integer",
            "category": "Integer",
            "comment": "String",
            "creationTime": "Integer"
          }
        ],
        "reuse": [
          {
            "id": "Integer",
            "no": "String",
            "name": "String",
            "sex": "Integer",
            "department": "Integer",
            "level": "Integer",
            "jobTitle": "String",
            "joinedDate": "Integer",
            "leftDate": "Integer",
            "identityId": "String",
            "country": "String",
            "birthday": "Integer",
            "phone": "String",
            "address": "String",
            "type": "Integer",
            "category": "Integer",
            "comment": "String",
            "creationTime": "Integer"
          }
        ],
        "labor": [
          {
            "id": "Integer",
            "no": "String",
            "name": "String",
            "sex": "Integer",
            "department": "Integer",
            "level": "Integer",
            "jobTitle": "String",
            "joinedDate": "Integer",
            "leftDate": "Integer",
            "identityId": "String",
            "country": "String",
            "birthday": "Integer",
            "phone": "String",
            "address": "String",
            "type": "Integer",
            "category": "Integer",
            "comment": "String",
            "creationTime": "Integer"
          }
        ],
        "labors": {},
        "machine": [
          {
            "id": "Integer",
            "no": "String",
            "name": "String",
            "sex": "Integer",
            "department": "Integer",
            "level": "Integer",
            "jobTitle": "String",
            "joinedDate": "Integer",
            "leftDate": "Integer",
            "identityId": "String",
            "country": "String",
            "birthday": "Integer",
            "phone": "String",
            "address": "String",
            "type": "Integer",
            "category": "Integer",
            "comment": "String",
            "creationTime": "Integer"
          }
        ],
        "machineRec": [
          {
            "id": "Integer",
            "no": "String",
            "name": "String",
            "sex": "Integer",
            "department": "Integer",
            "level": "Integer",
            "jobTitle": "String",
            "joinedDate": "Integer",
            "leftDate": "Integer",
            "identityId": "String",
            "country": "String",
            "birthday": "Integer",
            "phone": "String",
            "address": "String",
            "type": "Integer",
            "category": "Integer",
            "comment": "String",
            "creationTime": "Integer"
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
| payload.results[].no | String | 資料編號 |  |
| payload.results[].date | String | 日期時間 |  |
| payload.results[].production_line_no | String | 產線編號 |  |
| payload.results[].productionLineName | String | 產線名稱 |  |
| payload.results[].output_item_no | String | 產出品項編號 |  |
| payload.results[].output_item_name | String | 產出品項名稱 |  |
| payload.results[].oneProcess | String | 主製程 |  |
| payload.results[].secProcess | String | 次製程 |  |
| payload.results[].input[].id | Integer | 資料 ID |  |
| payload.results[].input[].no | String | 資料編號 |  |
| payload.results[].input[].name | String | 名稱 |  |
| payload.results[].input[].sex | Integer | 性別 |  |
| payload.results[].input[].department | Integer | 部門 |  |
| payload.results[].input[].level | Integer | 職等 |  |
| payload.results[].input[].jobTitle | String | 職稱 |  |
| payload.results[].input[].joinedDate | Integer | 到職日期 |  |
| payload.results[].input[].leftDate | Integer | 離職日期 |  |
| payload.results[].input[].identityId | String | 身分證號或識別碼 |  |
| payload.results[].input[].country | String | 國籍 |  |
| payload.results[].input[].birthday | Integer | 生日 |  |
| payload.results[].input[].phone | String | 電話 |  |
| payload.results[].input[].address | String | 地址 |  |
| payload.results[].input[].type | Integer | 類型 |  |
| payload.results[].input[].category | Integer | 類別 |  |
| payload.results[].input[].comment | String | 備註 |  |
| payload.results[].input[].creationTime | Integer | 資料建立時間 |  |
| payload.results[].output[].id | Integer | 資料 ID |  |
| payload.results[].output[].no | String | 資料編號 |  |
| payload.results[].output[].name | String | 名稱 |  |
| payload.results[].output[].sex | Integer | 性別 |  |
| payload.results[].output[].department | Integer | 部門 |  |
| payload.results[].output[].level | Integer | 職等 |  |
| payload.results[].output[].jobTitle | String | 職稱 |  |
| payload.results[].output[].joinedDate | Integer | 到職日期 |  |
| payload.results[].output[].leftDate | Integer | 離職日期 |  |
| payload.results[].output[].identityId | String | 身分證號或識別碼 |  |
| payload.results[].output[].country | String | 國籍 |  |
| payload.results[].output[].birthday | Integer | 生日 |  |
| payload.results[].output[].phone | String | 電話 |  |
| payload.results[].output[].address | String | 地址 |  |
| payload.results[].output[].type | Integer | 類型 |  |
| payload.results[].output[].category | Integer | 類別 |  |
| payload.results[].output[].comment | String | 備註 |  |
| payload.results[].output[].creationTime | Integer | 資料建立時間 |  |
| payload.results[].reuse[].id | Integer | 資料 ID |  |
| payload.results[].reuse[].no | String | 資料編號 |  |
| payload.results[].reuse[].name | String | 名稱 |  |
| payload.results[].reuse[].sex | Integer | 性別 |  |
| payload.results[].reuse[].department | Integer | 部門 |  |
| payload.results[].reuse[].level | Integer | 職等 |  |
| payload.results[].reuse[].jobTitle | String | 職稱 |  |
| payload.results[].reuse[].joinedDate | Integer | 到職日期 |  |
| payload.results[].reuse[].leftDate | Integer | 離職日期 |  |
| payload.results[].reuse[].identityId | String | 身分證號或識別碼 |  |
| payload.results[].reuse[].country | String | 國籍 |  |
| payload.results[].reuse[].birthday | Integer | 生日 |  |
| payload.results[].reuse[].phone | String | 電話 |  |
| payload.results[].reuse[].address | String | 地址 |  |
| payload.results[].reuse[].type | Integer | 類型 |  |
| payload.results[].reuse[].category | Integer | 類別 |  |
| payload.results[].reuse[].comment | String | 備註 |  |
| payload.results[].reuse[].creationTime | Integer | 資料建立時間 |  |
| payload.results[].labor[].id | Integer | 資料 ID |  |
| payload.results[].labor[].no | String | 資料編號 |  |
| payload.results[].labor[].name | String | 名稱 |  |
| payload.results[].labor[].sex | Integer | 性別 |  |
| payload.results[].labor[].department | Integer | 部門 |  |
| payload.results[].labor[].level | Integer | 職等 |  |
| payload.results[].labor[].jobTitle | String | 職稱 |  |
| payload.results[].labor[].joinedDate | Integer | 到職日期 |  |
| payload.results[].labor[].leftDate | Integer | 離職日期 |  |
| payload.results[].labor[].identityId | String | 身分證號或識別碼 |  |
| payload.results[].labor[].country | String | 國籍 |  |
| payload.results[].labor[].birthday | Integer | 生日 |  |
| payload.results[].labor[].phone | String | 電話 |  |
| payload.results[].labor[].address | String | 地址 |  |
| payload.results[].labor[].type | Integer | 類型 |  |
| payload.results[].labor[].category | Integer | 類別 |  |
| payload.results[].labor[].comment | String | 備註 |  |
| payload.results[].labor[].creationTime | Integer | 資料建立時間 |  |
| payload.results[].machine[].id | Integer | 資料 ID |  |
| payload.results[].machine[].no | String | 資料編號 |  |
| payload.results[].machine[].name | String | 名稱 |  |
| payload.results[].machine[].sex | Integer | 性別 |  |
| payload.results[].machine[].department | Integer | 部門 |  |
| payload.results[].machine[].level | Integer | 職等 |  |
| payload.results[].machine[].jobTitle | String | 職稱 |  |
| payload.results[].machine[].joinedDate | Integer | 到職日期 |  |
| payload.results[].machine[].leftDate | Integer | 離職日期 |  |
| payload.results[].machine[].identityId | String | 身分證號或識別碼 |  |
| payload.results[].machine[].country | String | 國籍 |  |
| payload.results[].machine[].birthday | Integer | 生日 |  |
| payload.results[].machine[].phone | String | 電話 |  |
| payload.results[].machine[].address | String | 地址 |  |
| payload.results[].machine[].type | Integer | 類型 |  |
| payload.results[].machine[].category | Integer | 類別 |  |
| payload.results[].machine[].comment | String | 備註 |  |
| payload.results[].machine[].creationTime | Integer | 資料建立時間 |  |
| payload.results[].machineRec[].id | Integer | 資料 ID |  |
| payload.results[].machineRec[].no | String | 資料編號 |  |
| payload.results[].machineRec[].name | String | 名稱 |  |
| payload.results[].machineRec[].sex | Integer | 性別 |  |
| payload.results[].machineRec[].department | Integer | 部門 |  |
| payload.results[].machineRec[].level | Integer | 職等 |  |
| payload.results[].machineRec[].jobTitle | String | 職稱 |  |
| payload.results[].machineRec[].joinedDate | Integer | 到職日期 |  |
| payload.results[].machineRec[].leftDate | Integer | 離職日期 |  |
| payload.results[].machineRec[].identityId | String | 身分證號或識別碼 |  |
| payload.results[].machineRec[].country | String | 國籍 |  |
| payload.results[].machineRec[].birthday | Integer | 生日 |  |
| payload.results[].machineRec[].phone | String | 電話 |  |
| payload.results[].machineRec[].address | String | 地址 |  |
| payload.results[].machineRec[].type | Integer | 類型 |  |
| payload.results[].machineRec[].category | Integer | 類別 |  |
| payload.results[].machineRec[].comment | String | 備註 |  |
| payload.results[].machineRec[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start、type
2. 查詢 employee、production_line、station、work_order 取得工單 / 生產數據資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| employee | 提供工單排程、生產或產能資料 |
| production_line | 提供工單排程、生產或產能資料 |
| station | 提供工單排程、生產或產能資料 |
| work_order | 提供工單排程、生產或產能資料 |

## GET /api/v1/workorder/statistics

<a id="get-api-v1-workorder-statistics"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/workorder/statistics | GET | 查詢工單 / 統計 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| commit | String | NO | 是否提交/確認統計條件 |
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
    "count": "Integer",
    "results": [
      {
        "date": "String",
        "oneProcess": "Integer",
        "secProcess": "Integer",
        "total": "Integer"
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].date | String | 日期時間 |  |
| payload.results[].oneProcess | Integer | 主製程 |  |
| payload.results[].secProcess | Integer | 次製程 |  |
| payload.results[].total | Integer | 符合條件的總筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：commit、end_time、start_time
2. 取得工單 / 統計資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

None
