# user API Group

> Source: `restserver/package/restserver/api/user_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/user/device/login](#post-user-device-login) | POST | 用戶登入 | OK | Aligned with `docs/spec/scale/電子智能秤系統REST API_1.06.docx` |
| [/user/device/logout](#delete-user-device-logout) | DELETE | 用戶登出 | OK | Aligned with `docs/spec/scale/電子智能秤系統REST API_1.06.docx` |
| [/api/v1/user/login](#post-api-v1-user-login) | POST | 使用者 / 登入 | OK | OK |
| [/api/v1/user/login](#delete-api-v1-user-login) | DELETE | 刪除使用者 / 登入 | OK | OK |

## POST /user/device/login

<a id="post-user-device-login"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /user/device/login | POST | 登入食品製造管理系統 |

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
| registerNo | String | YES | 設備註冊碼 |  |
| username | String | YES | 使用者登入帳號 |  |
| password | String | YES | 使用者登入密碼 (base64 encryption 編碼) |  |

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
| payload.serverTimestamp | Integer | 伺服器時間 (UTC) |  |
| payload.serverId | String | 伺服器ID |  |
| payload.user.token | String | 存取金鑰 |  |
| payload.user.role | Integer | 身份類型 | role |
| payload.user.employee.no | String | 員工編號 |  |
| payload.user.employee.name | String | 員工姓名 |  |
| payload.user.employee.department | Integer | 部門 | department |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 驗證 request body 必填欄位與資料格式：registerNo、username、password
2. 建立使用者 / 設備 / 登入資料
3. 回傳建立結果與必要識別資訊

### Database Tables Used

| Table | Purpose |
|----------|------|
| device | 確認設備註冊碼與設備角色 |
| employee | 取得登入人員資料與部門權限 |
| session | 建立或失效登入 Session |
| user_group | 取得使用者群組與角色 |

## DELETE /user/device/logout

<a id="delete-user-device-logout"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /user/device/logout | DELETE | 登出系統 |

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
    "serverTimestamp": "Integer",
    "serverId": "String"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.serverTimestamp | Integer | 伺服器時間 (UTC) |  |
| payload.serverId | String | 伺服器ID |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 依條件刪除或取消使用者 / 設備 / 登出資料
2. 回傳刪除或取消結果

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

1. 驗證 username / password
2. 查詢 member table
3. 使用 Argon2 驗證密碼
4. 查詢 employee 資料
5. 建立 session token
6. 寫入 session 資料表
7. 回傳 token + user info

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

1. 讀取登入 token
2. 使 session token 失效
3. 回傳登出結果

### Database Tables Used

| Table | Purpose |
|----------|------|
| session | 建立或失效登入 Session |
