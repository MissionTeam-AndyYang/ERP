# purchase API Group

> Source: `restserver/package/restserver/api/purchase_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/purchase/purchaseorder](#get-api-v1-purchase-purchaseorder) | GET | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |
| [/api/v1/purchase/purchaseorder](#post-api-v1-purchase-purchaseorder) | POST | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics; request body schema not explicitly parsed |
| [/api/v1/purchase/purchaseorder](#put-api-v1-purchase-purchaseorder) | PUT | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics; request body schema not explicitly parsed |
| [/api/v1/purchase/purchaseorder](#delete-api-v1-purchase-purchaseorder) | DELETE | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |
| [/api/v1/purchase/goodsreceiptnote](#get-api-v1-purchase-goodsreceiptnote) | GET | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |
| [/api/v1/purchase/goodsreceiptnote](#post-api-v1-purchase-goodsreceiptnote) | POST | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics; request body schema not explicitly parsed |
| [/api/v1/purchase/goodsreceiptnote](#put-api-v1-purchase-goodsreceiptnote) | PUT | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics; request body schema not explicitly parsed |
| [/api/v1/purchase/goodsreceiptnote](#delete-api-v1-purchase-goodsreceiptnote) | DELETE | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |
| [/api/v1/purchase/statistics](#get-api-v1-purchase-statistics) | GET | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |
| [/api/v1/purchase/payment](#get-api-v1-purchase-payment) | GET | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |
| [/api/v1/purchase/payment](#post-api-v1-purchase-payment) | POST | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics; request body schema not explicitly parsed |
| [/api/v1/purchase/payment](#put-api-v1-purchase-payment) | PUT | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics; request body schema not explicitly parsed |
| [/api/v1/purchase/payment](#delete-api-v1-purchase-payment) | DELETE | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |
| [/api/v1/purchase/contract](#get-api-v1-purchase-contract) | GET | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |
| [/api/v1/purchase/contract](#post-api-v1-purchase-contract) | POST | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics; request body schema not explicitly parsed |
| [/api/v1/purchase/contract](#put-api-v1-purchase-contract) | PUT | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics; request body schema not explicitly parsed |
| [/api/v1/purchase/contract](#delete-api-v1-purchase-contract) | DELETE | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |
| [/api/v1/purchase/arap](#get-api-v1-purchase-arap) | GET | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |

## GET /api/v1/purchase/purchaseorder

<a id="get-api-v1-purchase-purchaseorder"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/purchaseorder | GET | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | String | Need Review | Derived from request.args.get usage; semantic description requires review. |
| start | String | Need Review | Derived from request.args.get usage; semantic description requires review. |
| type | String | Need Review | Derived from request.args.get usage; semantic description requires review. |

### Request Body

None

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
| payload.count | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |
| payload.results | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |
| payload.sum | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |
| payload.total | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |

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
4. CAPIBase calls executor `CPurchaseOrder.get(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

| Table | Purpose |
|----------|------|
| contract | Referenced by executor source through ORM model. See `docs/spec/database/index.md#contract`. |
| goods_receipt_note | Referenced by executor source through ORM model. See `docs/spec/database/index.md#goods_receipt_note`. |
| material | Referenced by executor source through ORM model. See `docs/spec/database/index.md#material`. |
| purchase_order | Referenced by executor source through ORM model. See `docs/spec/database/index.md#purchase_order`. |

## POST /api/v1/purchase/purchaseorder

<a id="post-api-v1-purchase-purchaseorder"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/purchaseorder | POST | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json or multipart/form-data, enforced by CAPIBase |
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

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
| payload | Object | Payload structure is empty or dynamic in code; confirm with runtime sample if frontend uses it. |  |

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
4. CAPIBase calls executor `CPurchaseOrder.post(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## PUT /api/v1/purchase/purchaseorder

<a id="put-api-v1-purchase-purchaseorder"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/purchaseorder | PUT | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json or multipart/form-data, enforced by CAPIBase |
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

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
| payload | Object | Payload structure is empty or dynamic in code; confirm with runtime sample if frontend uses it. |  |

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
4. CAPIBase calls executor `CPurchaseOrder.put(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## DELETE /api/v1/purchase/purchaseorder

<a id="delete-api-v1-purchase-purchaseorder"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/purchaseorder | DELETE | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

### Query Parameters

None

### Request Body

None

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
| payload | Object | Payload structure is empty or dynamic in code; confirm with runtime sample if frontend uses it. |  |

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
4. CAPIBase calls executor `CPurchaseOrder.delete(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## GET /api/v1/purchase/goodsreceiptnote

<a id="get-api-v1-purchase-goodsreceiptnote"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/goodsreceiptnote | GET | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | String | Need Review | Derived from request.args.get usage; semantic description requires review. |
| start | String | Need Review | Derived from request.args.get usage; semantic description requires review. |
| type | String | Need Review | Derived from request.args.get usage; semantic description requires review. |

### Request Body

None

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
| payload.count | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |
| payload.results | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |
| payload.sum | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |
| payload.total | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |

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
4. CAPIBase calls executor `CGoodsReceiptNote.get(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | Referenced by executor source through ORM model. See `docs/spec/database/index.md#batch_number`. |
| goods_receipt_note | Referenced by executor source through ORM model. See `docs/spec/database/index.md#goods_receipt_note`. |
| material | Referenced by executor source through ORM model. See `docs/spec/database/index.md#material`. |
| purchase_order | Referenced by executor source through ORM model. See `docs/spec/database/index.md#purchase_order`. |

## POST /api/v1/purchase/goodsreceiptnote

<a id="post-api-v1-purchase-goodsreceiptnote"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/goodsreceiptnote | POST | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json or multipart/form-data, enforced by CAPIBase |
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

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
| payload | Object | Payload structure is empty or dynamic in code; confirm with runtime sample if frontend uses it. |  |

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
4. CAPIBase calls executor `CGoodsReceiptNote.post(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## PUT /api/v1/purchase/goodsreceiptnote

<a id="put-api-v1-purchase-goodsreceiptnote"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/goodsreceiptnote | PUT | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json or multipart/form-data, enforced by CAPIBase |
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

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
| payload | Object | Payload structure is empty or dynamic in code; confirm with runtime sample if frontend uses it. |  |

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
4. CAPIBase calls executor `CGoodsReceiptNote.put(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## DELETE /api/v1/purchase/goodsreceiptnote

<a id="delete-api-v1-purchase-goodsreceiptnote"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/goodsreceiptnote | DELETE | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

### Query Parameters

None

### Request Body

None

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
| payload | Object | Payload structure is empty or dynamic in code; confirm with runtime sample if frontend uses it. |  |

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
4. CAPIBase calls executor `CGoodsReceiptNote.delete(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## GET /api/v1/purchase/statistics

<a id="get-api-v1-purchase-statistics"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/statistics | GET | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| commit | String | Need Review | Derived from request.args.get usage; semantic description requires review. |
| end_time | String | Need Review | Derived from request.args.get usage; semantic description requires review. |
| start_time | String | Need Review | Derived from request.args.get usage; semantic description requires review. |

### Request Body

None

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
| payload.count | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |
| payload.results | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |

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
4. CAPIBase calls executor `CStatistic.get(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## GET /api/v1/purchase/payment

<a id="get-api-v1-purchase-payment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/payment | GET | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | Integer | Need Review | Derived from request.args.get usage; semantic description requires review. |
| start | Integer | Need Review | Derived from request.args.get usage; semantic description requires review. |

### Request Body

None

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
| payload.results | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |
| payload.total | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |

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
4. CAPIBase calls executor `CPayment.get(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

| Table | Purpose |
|----------|------|
| contract | Referenced by executor source through ORM model. See `docs/spec/database/index.md#contract`. |
| order_payment | Referenced by executor source through ORM model. See `docs/spec/database/index.md#order_payment`. |
| product_order | Referenced by executor source through ORM model. See `docs/spec/database/index.md#product_order`. |
| shipping_order | Referenced by executor source through ORM model. See `docs/spec/database/index.md#shipping_order`. |

## POST /api/v1/purchase/payment

<a id="post-api-v1-purchase-payment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/payment | POST | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json or multipart/form-data, enforced by CAPIBase |
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

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
| payload | Object | Payload structure is empty or dynamic in code; confirm with runtime sample if frontend uses it. |  |

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
4. CAPIBase calls executor `CPayment.post(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## PUT /api/v1/purchase/payment

<a id="put-api-v1-purchase-payment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/payment | PUT | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json or multipart/form-data, enforced by CAPIBase |
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

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
| payload | Object | Payload structure is empty or dynamic in code; confirm with runtime sample if frontend uses it. |  |

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
4. CAPIBase calls executor `CPayment.put(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## DELETE /api/v1/purchase/payment

<a id="delete-api-v1-purchase-payment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/payment | DELETE | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

### Query Parameters

None

### Request Body

None

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
| payload | Object | Payload structure is empty or dynamic in code; confirm with runtime sample if frontend uses it. |  |

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
4. CAPIBase calls executor `CPayment.delete(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## GET /api/v1/purchase/contract

<a id="get-api-v1-purchase-contract"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/contract | GET | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | String | Need Review | Derived from request.args.get usage; semantic description requires review. |
| start | String | Need Review | Derived from request.args.get usage; semantic description requires review. |

### Request Body

None

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
| payload.count | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |
| payload.results | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |
| payload.total | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |

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
4. CAPIBase calls executor `CPurchaseContract.get(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## POST /api/v1/purchase/contract

<a id="post-api-v1-purchase-contract"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/contract | POST | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json or multipart/form-data, enforced by CAPIBase |
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

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
| payload | Object | Payload structure is empty or dynamic in code; confirm with runtime sample if frontend uses it. |  |

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
4. CAPIBase calls executor `CPurchaseContract.post(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## PUT /api/v1/purchase/contract

<a id="put-api-v1-purchase-contract"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/contract | PUT | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json or multipart/form-data, enforced by CAPIBase |
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

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
| payload | Object | Payload structure is empty or dynamic in code; confirm with runtime sample if frontend uses it. |  |

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
4. CAPIBase calls executor `CPurchaseContract.put(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## DELETE /api/v1/purchase/contract

<a id="delete-api-v1-purchase-contract"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/contract | DELETE | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

### Query Parameters

None

### Request Body

None

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
| payload | Object | Payload structure is empty or dynamic in code; confirm with runtime sample if frontend uses it. |  |

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
4. CAPIBase calls executor `CPurchaseContract.delete(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## GET /api/v1/purchase/arap

<a id="get-api-v1-purchase-arap"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/arap | GET | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| order_no | String | YES | Derived from request.args.get usage; semantic description requires review. |

### Request Body

None

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
| payload.results | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |
| payload.total | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |

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
4. CAPIBase calls executor `CPurchaseARAP.get(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None
