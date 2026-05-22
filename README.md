# ERP 2.0 智慧食品工廠平台

本專案為食品加工廠 ERP 2.0 Prototype 專案骨架，目標是逐步升級為：

- SaaS 化 ERP
- MES 生產管理平台
- 智慧工廠 Dashboard
- 食品溯源與品保平台

## 技術方向

- Frontend: React / Next.js / TypeScript
- UI: Tailwind CSS / ShadCN UI
- Charts: Recharts
- Backend: Python / Flask API / SQLAlchemy
- Database: MariaDB

## 主要目錄

```bash
src/
 ├── app/
 ├── components/
 │    ├── ui/
 │    ├── dashboard/
 │    ├── charts/
 │    ├── production/
 │    ├── warehouse/
 │    └── common/
 ├── layouts/
 ├── hooks/
 ├── services/
 ├── store/
 ├── types/
 └── mock/

docs/
 ├── design-system/
 ├── architecture/
 └── codex/
```

## 第一階段

Sprint 1-1：Design System + Dashboard UI Prototype

## 第二階段

Sprint 11：Backend Flask API 專案骨架已建立於 `backend/`。

詳細啟動方式請見：

```txt
docs/backend/SPRINT_11_BACKEND_SETUP.md
```

## 最新資料庫與 Restserver 基準

目前資料庫與工作流程基準：

```txt
docs/database/EWDB_20260522.sql
docs/database/EWDB_20260522_WORKFLOW.md
```

目前 legacy Flask restserver 程式碼位於：

```txt
restserver/package
```

最新複檢紀錄：

```txt
docs/backend/RESTSERVER_DB_RECHECK_20260522.md
```

## 協作文件

```txt
CONTRIBUTING.md
docs/backend/CODING_CONVENTION.md
docs/frontend/CODING_CONVENTION.md
docs/engineering/CODE_REVIEW_CHECKLIST.md
```
