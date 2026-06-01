# device API Group

> Source: `restserver/package/restserver/api/device_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [//device/register](#post-device-register) | POST | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics; request body schema not explicitly parsed |

## POST //device/register

<a id="post-device-register"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| //device/register | POST | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json or multipart/form-data, enforced by CAPIBase |
| X_AUTH_TOKEN | Not required by URI override for this method |

### Query Parameters

None

### Request Body

Need Review

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": "Object"
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API result code |  |
| message | String | API result message |  |
| payload | Object | Response payload object |  |
| payload.registerNo | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |
| payload.serverId | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |
| payload.serverTimestamp | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | Error code returned by CAPIBase or executor |  |
| message | String | Error message returned by CAPIBase or executor |  |
| payload | Object | Error payload; usually empty unless executor returns extra data |  |

### Processing Flow

```
1. Flask route handler instantiates the URI class.
2. URI class delegates request handling to CAPIBase.run().
3. CAPIBase performs content-type, body, token, and alive-time checks according to URI overrides.
4. CAPIBase calls executor `CDevice.post(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

| Table | Purpose |
|----------|------|
| device | Referenced by executor source through ORM model. See `docs/spec/database/index.md#device`. |
