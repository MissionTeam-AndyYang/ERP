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
| payload.results[].input[].workOrderDate | String | workOrderDate 回傳欄位 |  |
| payload.results[].input[].production_line_no | String | production_line_no 回傳欄位 |  |
| payload.results[].input[].productionLineName | String | productionLineName 回傳欄位 |  |
| payload.results[].input[].processDate | String | processDate 回傳欄位 |  |
| payload.results[].input[].item_no | String | 料品/品項編號 |  |
| payload.results[].input[].item_name | String | item_name 回傳欄位 |  |
| payload.results[].input[].itemCategory | String | 料品類別 |  |
| payload.results[].input[].itemSubCategory | String | itemSubCategory 回傳欄位 |  |
| payload.results[].input[].batch_number | String | 批號 |  |
| payload.results[].input[].unit | String | unit 回傳欄位 |  |
| payload.results[].input[].count | Integer | 本次回傳筆數 |  |
| payload.results[].input[].itemType | String | 料品類型 |  |
| payload.results[].input[].validDate | String | validDate 回傳欄位 |  |
| payload.results[].output[].workOrderDate | String | workOrderDate 回傳欄位 |  |
| payload.results[].output[].production_line_no | String | production_line_no 回傳欄位 |  |
| payload.results[].output[].productionLineName | String | productionLineName 回傳欄位 |  |
| payload.results[].output[].processDate | String | processDate 回傳欄位 |  |
| payload.results[].output[].item_no | String | 料品/品項編號 |  |
| payload.results[].output[].item_name | String | item_name 回傳欄位 |  |
| payload.results[].output[].itemCategory | String | 料品類別 |  |
| payload.results[].output[].itemSubCategory | String | itemSubCategory 回傳欄位 |  |
| payload.results[].output[].itemType | String | 料品類型 |  |
| payload.results[].output[].batch_number | String | 批號 |  |
| payload.results[].output[].validDate | String | validDate 回傳欄位 |  |
| payload.results[].output[].unit | String | unit 回傳欄位 |  |
| payload.results[].output[].count | Integer | 本次回傳筆數 |  |
| payload.results[].reuse[].workOrderDate | String | workOrderDate 回傳欄位 |  |
| payload.results[].reuse[].production_line_no | String | production_line_no 回傳欄位 |  |
| payload.results[].reuse[].productionLineName | String | productionLineName 回傳欄位 |  |
| payload.results[].reuse[].processDate | String | processDate 回傳欄位 |  |
| payload.results[].reuse[].item_no | String | 料品/品項編號 |  |
| payload.results[].reuse[].item_name | String | item_name 回傳欄位 |  |
| payload.results[].reuse[].itemCategory | String | 料品類別 |  |
| payload.results[].reuse[].itemSubCategory | String | itemSubCategory 回傳欄位 |  |
| payload.results[].reuse[].itemType | String | 料品類型 |  |
| payload.results[].reuse[].batch_number | String | 批號 |  |
| payload.results[].reuse[].validDate | String | validDate 回傳欄位 |  |
| payload.results[].reuse[].unit | String | unit 回傳欄位 |  |
| payload.results[].reuse[].count | Integer | 本次回傳筆數 |  |
| payload.results[].labors[].workOrderDate | String | workOrderDate 回傳欄位 |  |
| payload.results[].labors[].processDate | String | processDate 回傳欄位 |  |
| payload.results[].labors[].production_line_no | String | production_line_no 回傳欄位 |  |
| payload.results[].labors[].productionLineName | String | productionLineName 回傳欄位 |  |
| payload.results[].labors[].station_no | String | station_no 回傳欄位 |  |
| payload.results[].labors[].stationName | String | stationName 回傳欄位 |  |
| payload.results[].labors[].stationStage | String | stationStage 回傳欄位 |  |
| payload.results[].labors[].employee_no | String | employee_no 回傳欄位 |  |
| payload.results[].labors[].employeeName | String | employeeName 回傳欄位 |  |
| payload.results[].labors[].employeeType | String | employeeType 回傳欄位 |  |
| payload.results[].labors[].employeeJobTitle | String | employeeJobTitle 回傳欄位 |  |
| payload.results[].machines[].time | String | time 回傳欄位 |  |
| payload.results[].machines[].workOrderDate | String | workOrderDate 回傳欄位 |  |
| payload.results[].machines[].production_line_no | String | production_line_no 回傳欄位 |  |
| payload.results[].machines[].productionLineName | String | productionLineName 回傳欄位 |  |
| payload.results[].machines[].processDate | String | processDate 回傳欄位 |  |
| payload.results[].machines[].station_no | String | station_no 回傳欄位 |  |
| payload.results[].machines[].stationName | String | stationName 回傳欄位 |  |
| payload.results[].machines[].stationStage | String | stationStage 回傳欄位 |  |
| payload.results[].machines[].equipment_no | String | equipment_no 回傳欄位 |  |
| payload.results[].machines[].equipmentName | String | equipmentName 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start
2. 查詢資料表並套用條件：batch_number、batchno_serialno、equipment、process_labor、process_order、production_line、station、work_order
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results[].input[].workOrderDate、payload.results[].input[].production_line_no、payload.results[].input[].productionLineName、payload.results[].input[].processDate、payload.results[].input[].item_no、payload.results[].input[].item_name、payload.results[].input[].itemCategory、payload.results[].input[].itemSubCategory、payload.results[].input[].batch_number、payload.results[].input[].unit、payload.results[].input[].count、payload.results[].input[].itemType、payload.results[].input[].validDate、payload.results[].output[].workOrderDate、payload.results[].output[].production_line_no、payload.results[].output[].productionLineName、payload.results[].output[].processDate、payload.results[].output[].item_no、payload.results[].output[].item_name、payload.results[].output[].itemCategory、payload.results[].output[].itemSubCategory、payload.results[].output[].itemType、payload.results[].output[].batch_number、payload.results[].output[].validDate、payload.results[].output[].unit、payload.results[].output[].count、payload.results[].reuse[].workOrderDate、payload.results[].reuse[].production_line_no、payload.results[].reuse[].productionLineName、payload.results[].reuse[].processDate、payload.results[].reuse[].item_no、payload.results[].reuse[].item_name、payload.results[].reuse[].itemCategory、payload.results[].reuse[].itemSubCategory、payload.results[].reuse[].itemType、payload.results[].reuse[].batch_number、payload.results[].reuse[].validDate、payload.results[].reuse[].unit、payload.results[].reuse[].count、payload.results[].labors[].workOrderDate、payload.results[].labors[].processDate、payload.results[].labors[].production_line_no、payload.results[].labors[].productionLineName、payload.results[].labors[].station_no、payload.results[].labors[].stationName、payload.results[].labors[].stationStage、payload.results[].labors[].employee_no、payload.results[].labors[].employeeName、payload.results[].labors[].employeeType、payload.results[].labors[].employeeJobTitle、payload.results[].machines[].time、payload.results[].machines[].workOrderDate、payload.results[].machines[].production_line_no、payload.results[].machines[].productionLineName、payload.results[].machines[].processDate、payload.results[].machines[].station_no、payload.results[].machines[].stationName、payload.results[].machines[].stationStage、payload.results[].machines[].equipment_no、payload.results[].machines[].equipmentName

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
| payload.results[].no | String | 編號篩選 |  |
| payload.results[].creator_no | String | creator_no 回傳欄位 |  |
| payload.results[].work_order_no | String | 工單號 |  |
| payload.results[].refProcess | Integer | 參照製程 |  |
| payload.results[].date | Integer | 日期 |  |
| payload.results[].category | Integer | 類別篩選 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | item_name 回傳欄位 |  |
| payload.results[].itemCategory | Integer | 料品類別 |  |
| payload.results[].itemSubCategory | Integer | itemSubCategory 回傳欄位 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].unit | Integer | unit 回傳欄位 |  |
| payload.results[].expectedCount | Float | expectedCount 回傳欄位 |  |
| payload.results[].count | Float | 本次回傳筆數 |  |
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
2. 查詢資料表並套用條件：batch_number、process_order
3. 組裝回傳 payload 欄位：payload.total、payload.results[].id、payload.results[].no、payload.results[].creator_no、payload.results[].work_order_no、payload.results[].refProcess、payload.results[].date、payload.results[].category、payload.results[].item_no、payload.results[].item_name、payload.results[].itemCategory、payload.results[].itemSubCategory、payload.results[].item_ref_no、payload.results[].item_ref_displayName、payload.results[].unit、payload.results[].expectedCount、payload.results[].count、payload.results[].comment、payload.results[].creationTime

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

1. 驗證 request body 欄位：start_time、end_time
2. 查詢資料表並套用條件：work_order

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
| payload.results[].no | String | 編號篩選 |  |
| payload.results[].date | String | 日期 |  |
| payload.results[].production_line_no | String | production_line_no 回傳欄位 |  |
| payload.results[].productionLineName | String | productionLineName 回傳欄位 |  |
| payload.results[].output_item_no | String | output_item_no 回傳欄位 |  |
| payload.results[].output_item_name | String | output_item_name 回傳欄位 |  |
| payload.results[].oneProcess | String | 主製程 |  |
| payload.results[].secProcess | String | secProcess 回傳欄位 |  |
| payload.results[].input[].id | Integer | 資料 ID |  |
| payload.results[].input[].no | String | 編號篩選 |  |
| payload.results[].input[].name | String | 名稱 |  |
| payload.results[].input[].sex | Integer | sex 回傳欄位 |  |
| payload.results[].input[].department | Integer | department 回傳欄位 |  |
| payload.results[].input[].level | Integer | level 回傳欄位 |  |
| payload.results[].input[].jobTitle | String | jobTitle 回傳欄位 |  |
| payload.results[].input[].joinedDate | Integer | joinedDate 回傳欄位 |  |
| payload.results[].input[].leftDate | Integer | leftDate 回傳欄位 |  |
| payload.results[].input[].identityId | String | identityId 回傳欄位 |  |
| payload.results[].input[].country | String | country 回傳欄位 |  |
| payload.results[].input[].birthday | Integer | birthday 回傳欄位 |  |
| payload.results[].input[].phone | String | phone 回傳欄位 |  |
| payload.results[].input[].address | String | address 回傳欄位 |  |
| payload.results[].input[].type | Integer | 類型篩選 |  |
| payload.results[].input[].category | Integer | 類別篩選 |  |
| payload.results[].input[].comment | String | comment 回傳欄位 |  |
| payload.results[].input[].creationTime | Integer | creationTime 回傳欄位 |  |
| payload.results[].output[].id | Integer | 資料 ID |  |
| payload.results[].output[].no | String | 編號篩選 |  |
| payload.results[].output[].name | String | 名稱 |  |
| payload.results[].output[].sex | Integer | sex 回傳欄位 |  |
| payload.results[].output[].department | Integer | department 回傳欄位 |  |
| payload.results[].output[].level | Integer | level 回傳欄位 |  |
| payload.results[].output[].jobTitle | String | jobTitle 回傳欄位 |  |
| payload.results[].output[].joinedDate | Integer | joinedDate 回傳欄位 |  |
| payload.results[].output[].leftDate | Integer | leftDate 回傳欄位 |  |
| payload.results[].output[].identityId | String | identityId 回傳欄位 |  |
| payload.results[].output[].country | String | country 回傳欄位 |  |
| payload.results[].output[].birthday | Integer | birthday 回傳欄位 |  |
| payload.results[].output[].phone | String | phone 回傳欄位 |  |
| payload.results[].output[].address | String | address 回傳欄位 |  |
| payload.results[].output[].type | Integer | 類型篩選 |  |
| payload.results[].output[].category | Integer | 類別篩選 |  |
| payload.results[].output[].comment | String | comment 回傳欄位 |  |
| payload.results[].output[].creationTime | Integer | creationTime 回傳欄位 |  |
| payload.results[].reuse[].id | Integer | 資料 ID |  |
| payload.results[].reuse[].no | String | 編號篩選 |  |
| payload.results[].reuse[].name | String | 名稱 |  |
| payload.results[].reuse[].sex | Integer | sex 回傳欄位 |  |
| payload.results[].reuse[].department | Integer | department 回傳欄位 |  |
| payload.results[].reuse[].level | Integer | level 回傳欄位 |  |
| payload.results[].reuse[].jobTitle | String | jobTitle 回傳欄位 |  |
| payload.results[].reuse[].joinedDate | Integer | joinedDate 回傳欄位 |  |
| payload.results[].reuse[].leftDate | Integer | leftDate 回傳欄位 |  |
| payload.results[].reuse[].identityId | String | identityId 回傳欄位 |  |
| payload.results[].reuse[].country | String | country 回傳欄位 |  |
| payload.results[].reuse[].birthday | Integer | birthday 回傳欄位 |  |
| payload.results[].reuse[].phone | String | phone 回傳欄位 |  |
| payload.results[].reuse[].address | String | address 回傳欄位 |  |
| payload.results[].reuse[].type | Integer | 類型篩選 |  |
| payload.results[].reuse[].category | Integer | 類別篩選 |  |
| payload.results[].reuse[].comment | String | comment 回傳欄位 |  |
| payload.results[].reuse[].creationTime | Integer | creationTime 回傳欄位 |  |
| payload.results[].labor[].id | Integer | 資料 ID |  |
| payload.results[].labor[].no | String | 編號篩選 |  |
| payload.results[].labor[].name | String | 名稱 |  |
| payload.results[].labor[].sex | Integer | sex 回傳欄位 |  |
| payload.results[].labor[].department | Integer | department 回傳欄位 |  |
| payload.results[].labor[].level | Integer | level 回傳欄位 |  |
| payload.results[].labor[].jobTitle | String | jobTitle 回傳欄位 |  |
| payload.results[].labor[].joinedDate | Integer | joinedDate 回傳欄位 |  |
| payload.results[].labor[].leftDate | Integer | leftDate 回傳欄位 |  |
| payload.results[].labor[].identityId | String | identityId 回傳欄位 |  |
| payload.results[].labor[].country | String | country 回傳欄位 |  |
| payload.results[].labor[].birthday | Integer | birthday 回傳欄位 |  |
| payload.results[].labor[].phone | String | phone 回傳欄位 |  |
| payload.results[].labor[].address | String | address 回傳欄位 |  |
| payload.results[].labor[].type | Integer | 類型篩選 |  |
| payload.results[].labor[].category | Integer | 類別篩選 |  |
| payload.results[].labor[].comment | String | comment 回傳欄位 |  |
| payload.results[].labor[].creationTime | Integer | creationTime 回傳欄位 |  |
| payload.results[].machine[].id | Integer | 資料 ID |  |
| payload.results[].machine[].no | String | 編號篩選 |  |
| payload.results[].machine[].name | String | 名稱 |  |
| payload.results[].machine[].sex | Integer | sex 回傳欄位 |  |
| payload.results[].machine[].department | Integer | department 回傳欄位 |  |
| payload.results[].machine[].level | Integer | level 回傳欄位 |  |
| payload.results[].machine[].jobTitle | String | jobTitle 回傳欄位 |  |
| payload.results[].machine[].joinedDate | Integer | joinedDate 回傳欄位 |  |
| payload.results[].machine[].leftDate | Integer | leftDate 回傳欄位 |  |
| payload.results[].machine[].identityId | String | identityId 回傳欄位 |  |
| payload.results[].machine[].country | String | country 回傳欄位 |  |
| payload.results[].machine[].birthday | Integer | birthday 回傳欄位 |  |
| payload.results[].machine[].phone | String | phone 回傳欄位 |  |
| payload.results[].machine[].address | String | address 回傳欄位 |  |
| payload.results[].machine[].type | Integer | 類型篩選 |  |
| payload.results[].machine[].category | Integer | 類別篩選 |  |
| payload.results[].machine[].comment | String | comment 回傳欄位 |  |
| payload.results[].machine[].creationTime | Integer | creationTime 回傳欄位 |  |
| payload.results[].machineRec[].id | Integer | 資料 ID |  |
| payload.results[].machineRec[].no | String | 編號篩選 |  |
| payload.results[].machineRec[].name | String | 名稱 |  |
| payload.results[].machineRec[].sex | Integer | sex 回傳欄位 |  |
| payload.results[].machineRec[].department | Integer | department 回傳欄位 |  |
| payload.results[].machineRec[].level | Integer | level 回傳欄位 |  |
| payload.results[].machineRec[].jobTitle | String | jobTitle 回傳欄位 |  |
| payload.results[].machineRec[].joinedDate | Integer | joinedDate 回傳欄位 |  |
| payload.results[].machineRec[].leftDate | Integer | leftDate 回傳欄位 |  |
| payload.results[].machineRec[].identityId | String | identityId 回傳欄位 |  |
| payload.results[].machineRec[].country | String | country 回傳欄位 |  |
| payload.results[].machineRec[].birthday | Integer | birthday 回傳欄位 |  |
| payload.results[].machineRec[].phone | String | phone 回傳欄位 |  |
| payload.results[].machineRec[].address | String | address 回傳欄位 |  |
| payload.results[].machineRec[].type | Integer | 類型篩選 |  |
| payload.results[].machineRec[].category | Integer | 類別篩選 |  |
| payload.results[].machineRec[].comment | String | comment 回傳欄位 |  |
| payload.results[].machineRec[].creationTime | Integer | creationTime 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start、type
2. 查詢資料表並套用條件：employee、production_line、station、work_order
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results[].no、payload.results[].date、payload.results[].production_line_no、payload.results[].productionLineName、payload.results[].output_item_no、payload.results[].output_item_name、payload.results[].oneProcess、payload.results[].secProcess、payload.results[].input[].id、payload.results[].input[].no、payload.results[].input[].name、payload.results[].input[].sex、payload.results[].input[].department、payload.results[].input[].level、payload.results[].input[].jobTitle、payload.results[].input[].joinedDate、payload.results[].input[].leftDate、payload.results[].input[].identityId、payload.results[].input[].country、payload.results[].input[].birthday、payload.results[].input[].phone、payload.results[].input[].address、payload.results[].input[].type、payload.results[].input[].category、payload.results[].input[].comment、payload.results[].input[].creationTime、payload.results[].output[].id、payload.results[].output[].no、payload.results[].output[].name、payload.results[].output[].sex、payload.results[].output[].department、payload.results[].output[].level、payload.results[].output[].jobTitle、payload.results[].output[].joinedDate、payload.results[].output[].leftDate、payload.results[].output[].identityId、payload.results[].output[].country、payload.results[].output[].birthday、payload.results[].output[].phone、payload.results[].output[].address、payload.results[].output[].type、payload.results[].output[].category、payload.results[].output[].comment、payload.results[].output[].creationTime、payload.results[].reuse[].id、payload.results[].reuse[].no、payload.results[].reuse[].name、payload.results[].reuse[].sex、payload.results[].reuse[].department、payload.results[].reuse[].level、payload.results[].reuse[].jobTitle、payload.results[].reuse[].joinedDate、payload.results[].reuse[].leftDate、payload.results[].reuse[].identityId、payload.results[].reuse[].country、payload.results[].reuse[].birthday、payload.results[].reuse[].phone、payload.results[].reuse[].address、payload.results[].reuse[].type、payload.results[].reuse[].category、payload.results[].reuse[].comment、payload.results[].reuse[].creationTime、payload.results[].labor[].id、payload.results[].labor[].no、payload.results[].labor[].name、payload.results[].labor[].sex、payload.results[].labor[].department、payload.results[].labor[].level、payload.results[].labor[].jobTitle、payload.results[].labor[].joinedDate、payload.results[].labor[].leftDate、payload.results[].labor[].identityId、payload.results[].labor[].country、payload.results[].labor[].birthday、payload.results[].labor[].phone、payload.results[].labor[].address、payload.results[].labor[].type、payload.results[].labor[].category、payload.results[].labor[].comment、payload.results[].labor[].creationTime、payload.results[].machine[].id、payload.results[].machine[].no、payload.results[].machine[].name、payload.results[].machine[].sex、payload.results[].machine[].department、payload.results[].machine[].level、payload.results[].machine[].jobTitle、payload.results[].machine[].joinedDate、payload.results[].machine[].leftDate、payload.results[].machine[].identityId、payload.results[].machine[].country、payload.results[].machine[].birthday、payload.results[].machine[].phone、payload.results[].machine[].address、payload.results[].machine[].type、payload.results[].machine[].category、payload.results[].machine[].comment、payload.results[].machine[].creationTime、payload.results[].machineRec[].id、payload.results[].machineRec[].no、payload.results[].machineRec[].name、payload.results[].machineRec[].sex、payload.results[].machineRec[].department、payload.results[].machineRec[].level、payload.results[].machineRec[].jobTitle、payload.results[].machineRec[].joinedDate、payload.results[].machineRec[].leftDate、payload.results[].machineRec[].identityId、payload.results[].machineRec[].country、payload.results[].machineRec[].birthday、payload.results[].machineRec[].phone、payload.results[].machineRec[].address、payload.results[].machineRec[].type、payload.results[].machineRec[].category、payload.results[].machineRec[].comment、payload.results[].machineRec[].creationTime

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
| payload.results[].secProcess | String | secProcess 回傳欄位 |  |
| payload.results[].item_name | String | item_name 回傳欄位 |  |
| payload.results[].itemCategory | String | 料品類別 |  |
| payload.results[].itemSubCategory | String | itemSubCategory 回傳欄位 |  |
| payload.results[].bom.count | Integer | 本次回傳筆數 |  |
| payload.results[].bom.amount | String | amount 回傳欄位 |  |
| payload.results[].bom.hours | String | hours 回傳欄位 |  |
| payload.results[].product.count | Integer | 本次回傳筆數 |  |
| payload.results[].product.amount | String | amount 回傳欄位 |  |
| payload.results[].product.hours | String | hours 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：oneProcess、product_order_no
2. 查詢資料表並套用條件：aps_quantity、inproduct、product、production_data、production_data_output
3. 組裝回傳 payload 欄位：payload.results[].oneProcess、payload.results[].secProcess、payload.results[].item_name、payload.results[].itemCategory、payload.results[].itemSubCategory、payload.results[].bom.count、payload.results[].bom.amount、payload.results[].bom.hours、payload.results[].product.count、payload.results[].product.amount、payload.results[].product.hours

### Database Tables Used

| Table | Purpose |
|----------|------|
| aps_quantity | 提供製造作業排程、生產或產能資料 |
| inproduct | 提供製造作業排程、生產或產能資料 |
| product | 提供製造作業排程、生產或產能資料 |
| production_data | 提供製造作業排程、生產或產能資料 |
| production_data_output | 提供製造作業排程、生產或產能資料 |
