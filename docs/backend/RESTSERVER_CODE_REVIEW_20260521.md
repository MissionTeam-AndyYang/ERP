# Restserver Code Review

日期：2026-05-21

Review scope：`restserver/package`

Database baseline：`docs/database/EWDB_20260521.sql`

## Executive Summary

`restserver` 已提供大量 Flask Blueprint、SQLAlchemy ORM model、業務查詢與統計邏輯，可作為理解既有 EWDB API 的重要參考。不過目前不建議直接視為 ERP 2.0 production backend baseline，主要原因是安全性、設定管理、schema alignment 與依賴安裝仍有高風險缺口。

已執行檢查：

- `python -m compileall -q restserver\package`：通過。
- SQL schema 與 ORM table/column 快速比對：發現 4 個 SQL table mapping 缺口與 7 組 column mismatch。

## Findings

### P0 - Hard-coded database root password

File：`restserver/package/dbwrapper/maria.py:6`

`CMaria.__init__` 預設使用 `root / ew42885615`，且 `gen_connection_str()` 會直接把帳密組進 connection string。這會造成 credential 外洩、環境不可配置，也使測試/部署無法安全切換 DB。

建議：

- 改用環境變數或設定檔注入。
- 移除預設密碼。
- 補上 local/dev/prod 設定範例，真實密碼不進 Git。

### P0 - Login failure logs expose plaintext password

File：`restserver/package/auth/auth.py:71-75`

登入失敗與新增 session 失敗時，log 會輸出 `account` 與 `pwd`。這會把使用者密碼寫入 log，屬於高風險安全問題。

建議：

- 永遠不要記錄 plaintext password。
- 最多記錄 account、來源 IP、失敗原因分類與 request id。

### P1 - Token expiry refresh is disabled globally

File：`restserver/package/restserver/api/apibase.py:126-128`

`CAPIBase._is_reset_alive_time()` 預設回傳 `False`，因此雖然 `run()` 內有 token refresh 邏輯，實際上一般 API 不會檢查 token 是否仍在 session 中，也不會刷新 expiry。結果是只要 header 有 `HTTP_X_AUTH_TOKEN`，多數 API 就會通過 token gate。

建議：

- 將需要登入的 API 預設設為 `reset_alive_time=True`。
- 只有 login、heartbeat、device register 等明確公開 endpoint 覆寫為 false。
- 加測過期 token、假 token、缺 token 的行為。

### P1 - Authorization/privilege checks are disabled

File：`restserver/package/restserver/api/apibase.py:160-162`

`_is_check_privilege()` 固定回傳 `False`，且 `lst_privileges` 目前未實作載入。這表示所有已通過 token gate 的使用者都可做 GET/POST/PUT/DELETE，無角色權限保護。

建議：

- 以 `member` / `user_group` / `employee` 建立角色權限模型。
- 在 `CAPIBase` 中集中處理 method/resource 權限。
- 高風險操作先限制 DELETE / PUT。

### P1 - ORM and SQL baseline are not aligned

Files：

- `docs/database/EWDB_20260521.sql:861-883`
- `restserver/package/dbwrapper/table.py`

SQL baseline 有 `purchase_request` 與 `purchase_request_item`，但 ORM 沒有對應 model。另有大小寫不一致：SQL 使用 `Inventory_month_statistic` / `Inventory_item_month_statistic`，ORM 使用 lowercase table name。這會讓採購 workflow、統計查詢與 Linux/MariaDB 部署出現 runtime failure。

建議：

- 先補齊 `CTablePurchaseRequest` / `CTablePurchaseRequestItem`。
- 決定 inventory statistic table naming policy 並同步 SQL、ORM、API。
- 把 schema alignment check 加入 CI。

### P1 - Dependency file likely cannot build a clean environment

File：`restserver/package/requirements.txt:2-6`

`Flask==0.20.0` 很可能不是有效版本；`dateutil` 應改為 `python-dateutil`；SQLAlchemy 2.0 搭配 legacy query style 需要實測。requirements 也缺少 MariaDB connector package，但 connection string 使用 `mariadb+mariadbconnector://`。

建議：

- 將 Flask pin 到可安裝且安全支援的版本。
- 使用 `python-dateutil`。
- 加入 `mariadb` 或改用已確定的 DB driver。
- 建立 fresh venv install 驗證。

### P2 - Flask app runs without explicit port, config, or production WSGI boundary

File：`restserver/package/restserver/restserver.py:112`

程式直接 `g_obj_flask.run(host='0.0.0.0', threaded=True)`，沒有明確 port、debug/config separation，也沒有 WSGI entrypoint 說明。這適合開發啟動，但不適合作為服務部署邊界。

建議：

- 拆出 `create_app()`。
- 使用 gunicorn/uwsgi 或平台 WSGI。
- host/port/debug 從 config/env 控制。

### P2 - Request/response logging may leak sensitive payloads

File：`restserver/package/restserver/api/apibase.py:15-116`

`CAPIBase.run()` 會記錄 query string、POST body 與完整 response data。若 API payload 包含 token、個資、金額、合約或密碼相關欄位，log 會成為敏感資料副本。

建議：

- 對 body/response 做欄位遮罩。
- 僅在 debug 模式記錄完整 payload。
- production log 保留 request id、endpoint、status、error code。

## Positive Notes

- Flask Blueprint 模組切分完整，覆蓋 auth、master data、sale、purchase、inventory、MES、APS、batch trace 等主要領域。
- 大部分查詢使用 SQLAlchemy ORM，未看到大量直接拼接使用者輸入的 SQL。
- 密碼驗證使用 Argon2，比明文或弱 hash 好。
- `compileall` 語法檢查通過，表示目前程式至少可被 Python parser 接受。

## Recommended Next Steps

1. 先修 P0：移除 hard-coded DB password、清除 password logging。
2. 補 token/session 驗證測試，修正 `CAPIBase` token refresh 行為。
3. 對齊 `EWDB_20260521.sql` 與 ORM，優先補 `purchase_request` / `purchase_request_item`。
4. 修正 `requirements.txt`，建立可重現的 clean install。
5. 將 `restserver` 與既有 `backend/` Flask baseline 做取捨：若要保留兩者，需明確定義 `backend/` 為 ERP 2.0 新 API、`restserver/` 為 EWDB legacy/reference API。

