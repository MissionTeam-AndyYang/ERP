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

## 目前資料庫與後端基準

- Database baseline: `docs/database/EWDB_20260521.sql`
- Database review: `docs/database/EWDB_20260521_BASELINE_REVIEW.md`
- Legacy/reference API source: `restserver/package`
- Restserver review: `docs/backend/RESTSERVER_CODE_REVIEW_20260521.md`

> 註：`restserver/` 是工程師推送到 GitHub `main` 的既有 Flask API 參考實作；`backend/` 仍是 ERP 2.0 新 API baseline。兩者合併前需先完成 schema、auth、dependency 與 deployment 對齊。

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
 ├── backend/
 ├── database/
 └── codex/

restserver/
 └── package/             # GitHub main 提供的既有 Flask API 參考實作
```

## 第一階段

Sprint 1-1：Design System + Dashboard UI Prototype

## 第二階段

Sprint 11：Backend Flask API 專案骨架已建立於 `backend/`。

詳細啟動方式請見：

```txt
docs/backend/SPRINT_11_BACKEND_SETUP.md
```

## 協作文件

```txt
CONTRIBUTING.md
docs/backend/CODING_CONVENTION.md
docs/frontend/CODING_CONVENTION.md
docs/engineering/CODE_REVIEW_CHECKLIST.md
```
