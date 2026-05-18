# Sprint 11 Backend Setup

## 目標

建立 ERP 2.0 第二階段 MVP 的 Backend 基礎：

- Flask API app
- MariaDB 連線設定
- SQLAlchemy session
- Alembic migration 骨架
- Health check endpoint
- CORS 設定，允許前端 `http://127.0.0.1:3000`

## 目錄

```txt
backend/
  app/
    api/v1/
    core/
    db/
    main.py
  alembic/
  tests/
  .env.example
  alembic.ini
  pyproject.toml
```

## 安裝

Windows 目前可用 `py` 指令：

```powershell
cd C:\Users\andyy\Desktop\Codex-workspace\projects\ERP-2.0\backend
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

## 設定環境變數

```powershell
Copy-Item .env.example .env
```

修改 `.env` 的 `DATABASE_URL`：

```txt
DATABASE_URL=mysql+pymysql://erp_user:erp_password@127.0.0.1:3306/erp_2_0?charset=utf8mb4
```

## 啟動 API

```powershell
.\.venv\Scripts\python.exe -m flask --app app.main:app run --host 127.0.0.1 --port 8000 --debug
```

## Health Check

```txt
GET http://127.0.0.1:8000/
GET http://127.0.0.1:8000/api/v1/health
GET http://127.0.0.1:8000/api/v1/health/db
```

若 MariaDB 尚未啟動，`/api/v1/health/db` 會回傳 database unreachable；這在 Sprint 11 是可接受狀態。

## Alembic

Sprint 12 開始建立資料表後，可使用：

```powershell
.\.venv\Scripts\python.exe -m alembic revision --autogenerate -m "create initial schema"
.\.venv\Scripts\python.exe -m alembic upgrade head
```
