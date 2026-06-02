# device API Group

> Source: `restserver/package/restserver/api/device_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [//device/register](#post-device-register) | POST | 新增設備 / register | OK | OK |

## POST //device/register

<a id="post-device-register"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| //device/register | POST | 新增設備 / register |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | Not required |

### Query Parameters

None

### Request Body

Need Review: request body is read in code, but no explicit schema or field check was found.

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "serverId": "String",
    "registerNo": "Object"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.serverTimestamp | Integer | 伺服器時間戳記 |  |
| payload.serverId | String | 伺服器識別 |  |
| payload.registerNo | Object | 設備註冊編號 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 呼叫服務：CLogger.log
2. 查詢或使用資料表：device
3. 組裝回傳 payload 欄位：payload.serverTimestamp、payload.serverId、payload.registerNo

### Database Tables Used

| Table | Purpose |
|----------|------|
| device | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
