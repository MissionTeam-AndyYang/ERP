# heartbeat API Group

> Source: `restserver/package/restserver/api/heartbeat_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [//heartbeat](#get-heartbeat) | GET | 查詢服務心跳 | OK | OK |

## GET //heartbeat

<a id="get-heartbeat"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| //heartbeat | GET | 查詢服務心跳 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | Not required |

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
    "serverTimestamp": "Integer",
    "serverId": "String"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.serverTimestamp | Integer | 伺服器時間戳記 |  |
| payload.serverId | String | 伺服器識別 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 組裝回傳 payload 欄位：payload.serverTimestamp、payload.serverId

### Database Tables Used

None
