# productline API Group

> Source: `restserver/package/restserver/api/productline_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/productline](#get-api-v1-productline) | GET | 查詢產線 | OK | OK |
| [/api/v1/productline/equipment](#get-api-v1-productline-equipment) | GET | 查詢產線 / 設備 | OK | OK |
| [/api/v1/productline/factory](#get-api-v1-productline-factory) | GET | 查詢產線 / 廠區 | OK | OK |
| [/api/v1/productline/process](#get-api-v1-productline-process) | GET | 查詢產線 / 製程 | OK | OK |
| [/api/v1/productline/station](#get-api-v1-productline-station) | GET | 查詢產線 / 站點 | OK | OK |

## GET /api/v1/productline

<a id="get-api-v1-productline"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/productline | GET | 查詢產線 |

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
    "results": [
      {
        "factory": {
          "no": "String",
          "region": "String",
          "location": "String",
          "comment": "String"
        },
        "stations": [
          {
            "no": "String",
            "name": "String",
            "stage": "String",
            "comment": "String",
            "equipments": [
              {
                "no": "String",
                "name": "String",
                "appearance": "String",
                "comment": "String"
              }
            ]
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
| payload.results[].factory.no | String | 編號篩選 |  |
| payload.results[].factory.region | String | region 回傳欄位 |  |
| payload.results[].factory.location | String | location 回傳欄位 |  |
| payload.results[].factory.comment | String | comment 回傳欄位 |  |
| payload.results[].stations[].no | String | 編號篩選 |  |
| payload.results[].stations[].name | String | 名稱 |  |
| payload.results[].stations[].stage | String | stage 回傳欄位 |  |
| payload.results[].stations[].comment | String | comment 回傳欄位 |  |
| payload.results[].stations[].equipments[].no | String | 編號篩選 |  |
| payload.results[].stations[].equipments[].name | String | 名稱 |  |
| payload.results[].stations[].equipments[].appearance | String | appearance 回傳欄位 |  |
| payload.results[].stations[].equipments[].comment | String | comment 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 查詢資料表並套用條件：production_line
2. 組裝回傳 payload 欄位：payload.total、payload.results[].factory.no、payload.results[].factory.region、payload.results[].factory.location、payload.results[].factory.comment、payload.results[].stations[].no、payload.results[].stations[].name、payload.results[].stations[].stage、payload.results[].stations[].comment、payload.results[].stations[].equipments[].no、payload.results[].stations[].equipments[].name、payload.results[].stations[].equipments[].appearance、payload.results[].stations[].equipments[].comment

### Database Tables Used

| Table | Purpose |
|----------|------|
| production_line | 提供產線排程、生產或產能資料 |

## GET /api/v1/productline/equipment

<a id="get-api-v1-productline-equipment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/productline/equipment | GET | 查詢產線 / 設備 |

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
    "results": [
      {
        "station": {
          "no": "String",
          "name": "String",
          "stage": "String",
          "comment": "String"
        },
        "productionLine": {
          "no": "String",
          "name": "String",
          "oneProcess": "String",
          "secProcess": "String"
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
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.results[].station.no | String | 編號篩選 |  |
| payload.results[].station.name | String | 名稱 |  |
| payload.results[].station.stage | String | stage 回傳欄位 |  |
| payload.results[].station.comment | String | comment 回傳欄位 |  |
| payload.results[].productionLine.no | String | 編號篩選 |  |
| payload.results[].productionLine.name | String | 名稱 |  |
| payload.results[].productionLine.oneProcess | String | 主製程 |  |
| payload.results[].productionLine.secProcess | String | secProcess 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 查詢資料表並套用條件：equipment
2. 組裝回傳 payload 欄位：payload.total、payload.results[].station.no、payload.results[].station.name、payload.results[].station.stage、payload.results[].station.comment、payload.results[].productionLine.no、payload.results[].productionLine.name、payload.results[].productionLine.oneProcess、payload.results[].productionLine.secProcess

### Database Tables Used

| Table | Purpose |
|----------|------|
| equipment | 提供產線排程、生產或產能資料 |

## GET /api/v1/productline/factory

<a id="get-api-v1-productline-factory"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/productline/factory | GET | 查詢產線 / 廠區 |

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
    "results": [
      {}
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 查詢資料表並套用條件：factory
2. 組裝回傳 payload 欄位：payload.total

### Database Tables Used

| Table | Purpose |
|----------|------|
| factory | 提供產線排程、生產或產能資料 |

## GET /api/v1/productline/process

<a id="get-api-v1-productline-process"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/productline/process | GET | 查詢產線 / 製程 |

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
    "results": [
      {}
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 查詢資料表並套用條件：process
2. 組裝回傳 payload 欄位：payload.total

### Database Tables Used

| Table | Purpose |
|----------|------|
| process | 提供產線排程、生產或產能資料 |

## GET /api/v1/productline/station

<a id="get-api-v1-productline-station"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/productline/station | GET | 查詢產線 / 站點 |

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
    "results": [
      {
        "productionLine": {
          "no": "String",
          "name": "String",
          "oneProcess": "String",
          "secProcess": "String"
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
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.results[].productionLine.no | String | 編號篩選 |  |
| payload.results[].productionLine.name | String | 名稱 |  |
| payload.results[].productionLine.oneProcess | String | 主製程 |  |
| payload.results[].productionLine.secProcess | String | secProcess 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 查詢資料表並套用條件：station
2. 組裝回傳 payload 欄位：payload.total、payload.results[].productionLine.no、payload.results[].productionLine.name、payload.results[].productionLine.oneProcess、payload.results[].productionLine.secProcess

### Database Tables Used

| Table | Purpose |
|----------|------|
| station | 提供產線排程、生產或產能資料 |
