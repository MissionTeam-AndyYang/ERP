# work API Group

> Source: `restserver/package/restserver/api/work_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/work/assignment](#get-api-v1-work-assignment) | GET | 查詢製造作業 / 作業分派 | OK | OK |
| [/api/v1/work/process](#get-api-v1-work-process) | GET | 查詢製造作業 / 製程 | OK | OK |
| [/api/v1/work/process](#post-api-v1-work-process) | POST | 新增製造作業 / 製程 | OK | OK |
| [/api/v1/work/productdata](#get-api-v1-work-productdata) | GET | 查詢製造作業 / 生產數據 | OK | OK |
| [/api/v1/work/progress](#get-api-v1-work-progress) | GET | 查詢製造作業 / 作業進度 | OK | OK |

## GET /api/v1/work/assignment

<a id="get-api-v1-work-assignment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/work/assignment | GET | 查詢製造作業 / 作業分派 |

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
        "input": [
          {
            "workOrderDate": "String",
            "production_line_no": "String",
            "productionLineName": "String",
            "processDate": "String",
            "item_no": "String",
            "item_name": "String",
            "itemCategory": "String",
            "itemSubCategory": "String",
            "batch_number": "String",
            "unit": "String",
            "count": "Integer",
            "itemType": "String",
            "validDate": "String"
          }
        ],
        "output": [
          {
            "workOrderDate": "String",
            "production_line_no": "String",
            "productionLineName": "String",
            "processDate": "String",
            "item_no": "String",
            "item_name": "String",
            "itemCategory": "String",
            "itemSubCategory": "String",
            "itemType": "String",
            "batch_number": "String",
            "validDate": "String",
            "unit": "String",
            "count": "Integer"
          }
        ],
        "reuse": [
          {
            "workOrderDate": "String",
            "production_line_no": "String",
            "productionLineName": "String",
            "processDate": "String",
            "item_no": "String",
            "item_name": "String",
            "itemCategory": "String",
            "itemSubCategory": "String",
            "itemType": "String",
            "batch_number": "String",
            "validDate": "String",
            "unit": "String",
            "count": "Integer"
          }
        ],
        "labors": [
          {
            "workOrderDate": "String",
            "processDate": "String",
            "production_line_no": "String",
            "productionLineName": "String",
            "station_no": "String",
            "stationName": "String",
            "stationStage": "String",
            "employee_no": "String",
            "employeeName": "String",
            "employeeType": "String",
            "employeeJobTitle": "String"
          }
        ],
        "machines": [
          {
            "time": "String",
            "workOrderDate": "String",
            "production_line_no": "String",
            "productionLineName": "String",
            "processDate": "String",
            "station_no": "String",
            "stationName": "String",
            "stationStage": "String",
            "equipment_no": "String",
            "equipmentName": "String"
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
| payload.results[].input[].workOrderDate | String | work Order Date 的業務資料 |  |
| payload.results[].input[].production_line_no | String | 產線編號 |  |
| payload.results[].input[].productionLineName | String | 產線名稱 |  |
| payload.results[].input[].processDate | String | process Date 的業務資料 |  |
| payload.results[].input[].item_no | String | 料品/品項編號 |  |
| payload.results[].input[].item_name | String | 料品/品項名稱 |  |
| payload.results[].input[].itemCategory | String | 料品類別 |  |
| payload.results[].input[].itemSubCategory | String | 料品子類別 |  |
| payload.results[].input[].batch_number | String | 批號 |  |
| payload.results[].input[].unit | String | 單位 |  |
| payload.results[].input[].count | Integer | 本次回傳筆數 |  |
| payload.results[].input[].itemType | String | 料品類型 |  |
| payload.results[].input[].validDate | String | 效期日期 |  |
| payload.results[].output[].workOrderDate | String | work Order Date 的業務資料 |  |
| payload.results[].output[].production_line_no | String | 產線編號 |  |
| payload.results[].output[].productionLineName | String | 產線名稱 |  |
| payload.results[].output[].processDate | String | process Date 的業務資料 |  |
| payload.results[].output[].item_no | String | 料品/品項編號 |  |
| payload.results[].output[].item_name | String | 料品/品項名稱 |  |
| payload.results[].output[].itemCategory | String | 料品類別 |  |
| payload.results[].output[].itemSubCategory | String | 料品子類別 |  |
| payload.results[].output[].itemType | String | 料品類型 |  |
| payload.results[].output[].batch_number | String | 批號 |  |
| payload.results[].output[].validDate | String | 效期日期 |  |
| payload.results[].output[].unit | String | 單位 |  |
| payload.results[].output[].count | Integer | 本次回傳筆數 |  |
| payload.results[].reuse[].workOrderDate | String | work Order Date 的業務資料 |  |
| payload.results[].reuse[].production_line_no | String | 產線編號 |  |
| payload.results[].reuse[].productionLineName | String | 產線名稱 |  |
| payload.results[].reuse[].processDate | String | process Date 的業務資料 |  |
| payload.results[].reuse[].item_no | String | 料品/品項編號 |  |
| payload.results[].reuse[].item_name | String | 料品/品項名稱 |  |
| payload.results[].reuse[].itemCategory | String | 料品類別 |  |
| payload.results[].reuse[].itemSubCategory | String | 料品子類別 |  |
| payload.results[].reuse[].itemType | String | 料品類型 |  |
| payload.results[].reuse[].batch_number | String | 批號 |  |
| payload.results[].reuse[].validDate | String | 效期日期 |  |
| payload.results[].reuse[].unit | String | 單位 |  |
| payload.results[].reuse[].count | Integer | 本次回傳筆數 |  |
| payload.results[].labors[].workOrderDate | String | work Order Date 的業務資料 |  |
| payload.results[].labors[].processDate | String | process Date 的業務資料 |  |
| payload.results[].labors[].production_line_no | String | 產線編號 |  |
| payload.results[].labors[].productionLineName | String | 產線名稱 |  |
| payload.results[].labors[].station_no | String | 站點，關連至station資料表 |  |
| payload.results[].labors[].stationName | String | station Name 的業務資料 |  |
| payload.results[].labors[].stationStage | String | 製程階段 |  |
| payload.results[].labors[].employee_no | String | 員工編號，關連至employee資料表 |  |
| payload.results[].labors[].employeeName | String | employee Name 的業務資料 |  |
| payload.results[].labors[].employeeType | String | employee Type 的業務資料 |  |
| payload.results[].labors[].employeeJobTitle | String | employee Job Title 的業務資料 |  |
| payload.results[].machines[].time | String | 作業時間 |  |
| payload.results[].machines[].workOrderDate | String | work Order Date 的業務資料 |  |
| payload.results[].machines[].production_line_no | String | 產線編號 |  |
| payload.results[].machines[].productionLineName | String | 產線名稱 |  |
| payload.results[].machines[].processDate | String | process Date 的業務資料 |  |
| payload.results[].machines[].station_no | String | 站點，關連至station資料表 |  |
| payload.results[].machines[].stationName | String | station Name 的業務資料 |  |
| payload.results[].machines[].stationStage | String | 製程階段 |  |
| payload.results[].machines[].equipment_no | String | 機具no，關連至equipment資料表 |  |
| payload.results[].machines[].equipmentName | String | equipment Name 的業務資料 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 batch_number、batchno_serialno、equipment、process_labor 取得製造作業 / 作業分派資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 提供製造作業排程、生產或產能資料 |
| batchno_serialno | 提供製造作業排程、生產或產能資料 |
| equipment | 提供製造作業排程、生產或產能資料 |
| process_labor | 提供製造作業排程、生產或產能資料 |
| process_order | 提供製造作業排程、生產或產能資料 |
| production_line | 提供製造作業排程、生產或產能資料 |
| station | 提供製造作業排程、生產或產能資料 |
| work_order | 提供製造作業排程、生產或產能資料 |

## GET /api/v1/work/process

<a id="get-api-v1-work-process"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/work/process | GET | 查詢製造作業 / 製程 |

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
    "results": [
      {
        "id": "Integer",
        "no": "String",
        "creator_no": "String",
        "work_order_no": "String",
        "refProcess": "Integer",
        "date": "Integer",
        "category": "Integer",
        "item_no": "String",
        "item_name": "String",
        "itemCategory": "Integer",
        "itemSubCategory": "Integer",
        "item_ref_no": "String",
        "item_ref_displayName": "String",
        "unit": "Integer",
        "expectedCount": "Float",
        "count": "Float",
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
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].no | String | 資料編號 |  |
| payload.results[].creator_no | String | 製單人員編號 |  |
| payload.results[].work_order_no | String | 工單號 |  |
| payload.results[].refProcess | Integer | 派工製程 |  |
| payload.results[].date | Integer | 日期時間 |  |
| payload.results[].category | Integer | 類別 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | 料品/品項名稱 |  |
| payload.results[].itemCategory | Integer | 料品類別 |  |
| payload.results[].itemSubCategory | Integer | 料品子類別 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].expectedCount | Float | 預期數量 |  |
| payload.results[].count | Float | 本次回傳筆數 |  |
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
2. 查詢 batch_number、process_order 取得製造作業 / 製程資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 提供製造作業排程、生產或產能資料 |
| process_order | 提供製造作業排程、生產或產能資料 |

## POST /api/v1/work/process

<a id="post-api-v1-work-process"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/work/process | POST | 新增製造作業 / 製程 |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

```json
{
  "start_time": "Integer",
  "end_time": "Integer"
}
```

| Field Path | Type | Required | Description | Enum |
|----------|----------|------|-----|---|
| start_time | Integer | YES | 查詢開始時間 |  |
| end_time | Integer | YES | 查詢結束時間 |  |

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 驗證 request body 必填欄位與資料格式：start_time、end_time
2. 建立製造作業 / 製程資料
3. 回傳建立結果與必要識別資訊

### Database Tables Used

| Table | Purpose |
|----------|------|
| work_order | 提供製造作業排程、生產或產能資料 |

## GET /api/v1/work/productdata

<a id="get-api-v1-work-productdata"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/work/productdata | GET | 查詢製造作業 / 生產數據 |

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
2. 查詢 employee、production_line、station、work_order 取得製造作業 / 生產數據資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| employee | 提供製造作業排程、生產或產能資料 |
| production_line | 提供製造作業排程、生產或產能資料 |
| station | 提供製造作業排程、生產或產能資料 |
| work_order | 提供製造作業排程、生產或產能資料 |

## GET /api/v1/work/progress

<a id="get-api-v1-work-progress"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/work/progress | GET | 查詢製造作業 / 作業進度 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| oneProcess | String | YES | 主製程 |
| product_order_no | String | YES | 訂購單號 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "results": [
      {
        "oneProcess": "String",
        "secProcess": "String",
        "item_name": "String",
        "itemCategory": "String",
        "itemSubCategory": "String",
        "bom": {
          "count": "Integer",
          "amount": "String",
          "hours": "String"
        },
        "product": {
          "count": "Integer",
          "amount": "String",
          "hours": "String"
        }
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.results[].oneProcess | String | 主製程 |  |
| payload.results[].secProcess | String | 次製程 |  |
| payload.results[].item_name | String | 料品/品項名稱 |  |
| payload.results[].itemCategory | String | 料品類別 |  |
| payload.results[].itemSubCategory | String | 料品子類別 |  |
| payload.results[].bom.count | Integer | 本次回傳筆數 |  |
| payload.results[].bom.amount | String | 金額或需求量 |  |
| payload.results[].bom.hours | String | 工時 |  |
| payload.results[].product.count | Integer | 本次回傳筆數 |  |
| payload.results[].product.amount | String | 金額或需求量 |  |
| payload.results[].product.hours | String | 工時 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：oneProcess、product_order_no
2. 查詢 aps_quantity、inproduct、product、production_data 取得製造作業 / 作業進度資料
3. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| aps_quantity | 提供製造作業排程、生產或產能資料 |
| inproduct | 提供製造作業排程、生產或產能資料 |
| product | 提供製造作業排程、生產或產能資料 |
| production_data | 提供製造作業排程、生產或產能資料 |
| production_data_output | 提供製造作業排程、生產或產能資料 |
