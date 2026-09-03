# ERP2-BE-ENV-PROFILE-AND-RETTEST-RDY-001 後端環境與真實資料庫 Retest Readiness

## 1. Scope

本文件整理 ERP2.0 Backend/API component environment profile，並準備 Item / Transaction Item Product cycle 的 Shared DEV real-database retest 流程。

本次不重新開啟 Product implementation；不執行 Production、migration、source mutation、source-of-truth transition、Engineering Pull、Cutover 或 Go-Live。

## 2. Supported Python Version / Range

| Item | Value |
|---|---|
| Verified local Python | `Python 3.12.13` |
| Recommended range | `Python 3.12.x` |
| Reason | 現有 `.venv`、pytest 與 `requirements.txt` 已在 Python 3.12.13 通過 component tests |

## 3. Virtual Environment Creation Procedure

在專案根目錄建立後端測試用 venv：

```powershell
py -3.12 -m venv .venv
```

若 `py -3.12` 不可用，請先安裝 Python 3.12.x，並確認 `python --version` 為 3.12.x。

## 4. Dependency Manifest / Lock Strategy

| Item | Value |
|---|---|
| Manifest | `restserver/package/requirements.txt` |
| Current strategy | 所有主要 Python dependency 使用 pinned version |
| Separate lock file | 目前未發現 `poetry.lock`、`Pipfile.lock` 或 `pyproject.toml` |
| Recommendation | Shared DEV 先以 `requirements.txt` 作為 lock-like manifest；若未來導入 CI/CD，再評估產生 hash lock 或 pip-tools lock |

## 5. Install Command

在專案根目錄執行：

```powershell
.\.venv\Scripts\python.exe -m pip install -r restserver\package\requirements.txt
```

## 6. Unit / Component Test Command

在 `restserver` 目錄執行：

```powershell
..\.venv\Scripts\python.exe -m pytest tests
```

最近一次 component test 結果：

```text
80 passed in 3.79s
```

## 7. Service Start Command

在 `restserver` 目錄執行：

```powershell
$env:FLASK_PORT="5016"
..\.venv\Scripts\python.exe -m package.restserver.run
```

預設 host 由 `restserver/package/restserver/config.py` 控制，未設定時為 `0.0.0.0`。

## 8. Database Driver

| Item | Value |
|---|---|
| SQLAlchemy | `2.0.43` |
| MariaDB Python connector | `mariadb==1.1.13` |
| Connection URL scheme | `mariadb+mariadbconnector://` |

## 9. Database Connection Configuration Class

| File | Class | Notes |
|---|---|---|
| `restserver/package/dbwrapper/maria.py` | `CMaria` | Reads `DB_HOST`、`DB_PORT`、`DB_NAME`、`DB_USER`、`DB_PASSWORD` |
| `restserver/package/dbwrapper/dbmgr.py` | `CDBMgr` | Creates SQLAlchemy engine and session |
| `restserver/package/dbwrapper/dbmgr.py` | `CDBMgrTrans` | Transaction wrapper variant |

`CMaria` 在 `ENV=dev` 時會載入 `../config/.env.dev`。

## 10. Health Check Method

### DB Port Check

在專案根目錄執行：

```powershell
.\.venv\Scripts\python.exe -c "import socket; s=socket.socket(); s.settimeout(2); print('tcp_127_0_0_1_3306=PASS' if s.connect_ex(('127.0.0.1',3306)) == 0 else 'tcp_127_0_0_1_3306=FAIL'); s.close()"
```

本次結果：

```text
tcp_127_0_0_1_3306=FAIL
```

### Backend HTTP Check

DB 就緒並啟動 backend 後，測試：

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5016/api/v2/items/dashboard?count=5" -Headers @{"x-auth-token"="{token}";"x-timezone"="Asia/Taipei"}
```

## 11. Logs / Observability

| Environment | Log location |
|---|---|
| Windows local backend | `restserver/package/restserver/restserver.log` |
| Non-Windows backend | `/var/log/restserver.log` |

建議 retest 時同時記錄：

- HTTP status code
- API `code`
- response time
- payload `total/start/count`
- selected sample record identifiers
- backend log error snippet if failed

## 12. Clean Rebuild Procedure

1. 停止 backend process。
2. 確認 MariaDB non-production database 已啟動。
3. 確認 `.env.dev` 或環境變數已設定 `DB_HOST`、`DB_PORT`、`DB_NAME`、`DB_USER`、`DB_PASSWORD`。
4. 重新建立 venv：

```powershell
Remove-Item -Recurse -Force .venv
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r restserver\package\requirements.txt
```

5. 在 `restserver` 目錄執行 component tests。
6. 啟動 backend 並執行 real-database retest。

## 13. Real-Database Retest Procedure

### Preconditions

- MariaDB non-production service is running.
- `ewdb` or agreed Shared DEV DB has been imported with authorized non-production data.
- Backend can connect using `.env.dev` / environment variables.
- No Production credentials or Production data are used.

### Authorized Endpoint Paths

| Endpoint | Method | Expected retest |
|---|---|---|
| `/api/v2/items/dashboard?count=5` | GET | Status 200; payload contains `summary`、`categorySummary`、`items`、`maintenanceSuggestions`; `items[]` must not contain `itemType` |
| `/api/v2/items/{item_no}/detail` | GET | Status 200 for known item; payload contains `item`、`inventorySummary`、`bomUsage`、`recentBatches`; `item` must not contain `itemType` |
| `/api/v2/transitems/dashboard?count=5` | GET | Status 200; payload contains `summary`、`companies`、`transactionItems`; `total/start/count` aligned with page |
| `/api/v2/transitems/companies/{company_no}/detail` | GET | Status 200 for known company; payload contains `company`、`transactionItems`、`contracts` |
| `/api/v2/transitems/transitems/{transaction_item_no}/detail` | GET | Status 200 for known transaction item; payload contains `transItem`、`contracts`、`linkedItems` |

### UX Retest URLs

After backend is running on port `5016`, UX may point the frontend API base to:

```text
http://127.0.0.1:5016
```

Initial direct browser/API checks:

```text
http://127.0.0.1:5016/api/v2/items/dashboard?count=5
http://127.0.0.1:5016/api/v2/transitems/dashboard?count=5
```

Authenticated clients must include `x-auth-token` and `x-timezone: Asia/Taipei` if required by the existing API base behavior.

## 14. Query-Count / Performance Observation Plan

| API | Observation |
|---|---|
| `/api/v2/items/dashboard` | Confirm candidate item filtering happens before inventory/BOM/batch summaries; record response time for count=5, 50, 100 |
| `/api/v2/items/{item_no}/detail` | Confirm direct item lookup, no full item master scan; record response time for known item with BOM and inventory |
| `/api/v2/transitems/dashboard` | Confirm DB count + offset + limit behavior; record response time for count=5, 50, 100 and `hasContract=true` |
| `/api/v2/transitems/companies/{company_no}/detail` | Confirm company detail does not load unrelated companies |
| `/api/v2/transitems/transitems/{transaction_item_no}/detail` | Confirm single transaction item detail does not scan all transaction items |

Recommended material checks:

1. Capture backend response time per endpoint.
2. Capture DB slow query log if available in Shared DEV.
3. Compare small and max page size.
4. Confirm no endpoint expands payload outside formal API docs.

## 15. Required Environment Inputs from Engineering B

| Required input | Purpose |
|---|---|
| MariaDB service identity / service name | Needed for start/stop and health check |
| MariaDB version | Needed for compatibility record |
| Non-production DB name | Expected by `DB_NAME` |
| Non-production DB host/port | Expected by `DB_HOST` / `DB_PORT` |
| Non-production DB credentials | Needed for backend connection |
| Authorized dataset name and import timestamp | Needed for reproducible retest evidence |
| Known sample `item_no` | Needed for `/api/v2/items/{item_no}/detail` |
| Known sample `company_no` | Needed for `/api/v2/transitems/companies/{company_no}/detail` |
| Known sample `transaction_item_no` | Needed for `/api/v2/transitems/transitems/{transaction_item_no}/detail` |
| Auth token source | Needed for real HTTP calls if `x-auth-token` is enforced |

## 16. Safe Stop Condition

Stop and request CTO / CIO treatment if any retest requires:

- Production DB access
- Production data
- Production credentials
- migration execution
- source mutation
- source-of-truth transition
- Engineering Pull
- Cutover
- ERP2.0 Go-Live
- material API contract expansion

## 17. Current Closure Statement

Backend component environment is reproducible with Python 3.12.x and pinned `requirements.txt`.

Real-database retest is currently blocked by Shared DEV DB capability:

```text
tcp_127_0_0_1_3306=FAIL
```

This is `SHARED_DEV_ENVIRONMENT_READINESS FAILURE`, not Product implementation failure.
