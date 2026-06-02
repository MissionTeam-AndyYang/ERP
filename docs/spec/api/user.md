# user API Group

> Source: `restserver/package/restserver/api/user_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [//user/device/login](#post-user-device-login) | POST | 使用者 / 設備 / 登入 | OK | OK |
| [//user/device/logout](#delete-user-device-logout) | DELETE | 使用者 / 設備 / 登出 | OK | OK |
| [/api/v1/user/login](#post-api-v1-user-login) | POST | 使用者 / 登入 | OK | OK |
| [/api/v1/user/login](#delete-api-v1-user-login) | DELETE | 刪除使用者 / 登入 | OK | OK |

## POST //user/device/login

<a id="post-user-device-login"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| //user/device/login | POST | 使用者 / 設備 / 登入 |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | Not required |

### Query Parameters

None

### Request Body

```json
{
  "registerNo": "String",
  "username": "String",
  "password": "String"
}
```

| Field Path | Type | Required | Description | Enum |
|----------|----------|------|-----|---|
| registerNo | String | YES | 設備註冊編號 |  |
| username | String | YES | 登入帳號 |  |
| password | String | YES | 登入密碼 |  |

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "serverId": "String",
    "user": {
      "token": "String",
      "role": "Integer",
      "employee": {
        "no": "String",
        "name": "String",
        "department": "String"
      }
    }
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.serverTimestamp | Integer | 伺服器時間戳記 |  |
| payload.serverId | String | 伺服器識別 |  |
| payload.user.token | String | 登入 token |  |
| payload.user.role | Integer | 角色 |  |
| payload.user.employee.no | String | 編號篩選 |  |
| payload.user.employee.name | String | 名稱 |  |
| payload.user.employee.department | String | department 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 驗證 request body 欄位：registerNo、username、password
2. 查詢資料表並套用條件：device、employee、session、user_group
3. 組裝回傳 payload 欄位：payload.serverTimestamp、payload.serverId、payload.user.token、payload.user.role、payload.user.employee.no、payload.user.employee.name、payload.user.employee.department

### Database Tables Used

| Table | Purpose |
|----------|------|
| device | 確認設備註冊編號與設備角色 |
| employee | 取得登入人員資料與部門權限 |
| session | 建立或失效登入 Session |
| user_group | 取得使用者群組與角色 |

## DELETE //user/device/logout

<a id="delete-user-device-logout"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| //user/device/logout | DELETE | 使用者 / 設備 / 登出 |

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

1. 使登入 token 失效
2. 查詢資料表並套用條件：session

### Database Tables Used

| Table | Purpose |
|----------|------|
| session | 建立或失效登入 Session |

## POST /api/v1/user/login

<a id="post-api-v1-user-login"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/user/login | POST | 使用者 / 登入 |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | Not required |

### Query Parameters

None

### Request Body

```json
{
  "username": "String",
  "password": "String"
}
```

| Field Path | Type | Required | Description | Enum |
|----------|----------|------|-----|---|
| username | String | YES | 登入帳號 |  |
| password | String | YES | 登入密碼 |  |

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "token": "String",
    "user": {}
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.token | String | 登入 token |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 驗證 request body 欄位：username、password
2. 查詢資料表並套用條件：session
3. 組裝回傳 payload 欄位：payload.token

### Database Tables Used

| Table | Purpose |
|----------|------|
| session | 建立或失效登入 Session |

## DELETE /api/v1/user/login

<a id="delete-api-v1-user-login"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/user/login | DELETE | 刪除使用者 / 登入 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| token | String | NO | 登入 token |

### Request Body

None

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

1. 讀取查詢條件：token
2. 使登入 token 失效
3. 查詢資料表並套用條件：session

### Database Tables Used

| Table | Purpose |
|----------|------|
| session | 建立或失效登入 Session |
