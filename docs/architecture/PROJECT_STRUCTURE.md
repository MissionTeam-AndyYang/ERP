# ERP 2.0 Project Structure

```bash
src/
 ├── app/
 ├── components/
 │    ├── ui/             # Button, Input, Card, Badge 等基礎元件
 │    ├── dashboard/      # KPI Card, Alert Center, Production Line Card
 │    ├── charts/         # Recharts wrappers
 │    ├── production/     # 生產中心元件
 │    ├── warehouse/      # 倉儲中心元件
 │    └── common/         # 共用元件
 │
 ├── layouts/             # AppLayout, SidebarLayout
 ├── hooks/               # React hooks
 ├── services/            # API services
 ├── store/               # 狀態管理
 ├── types/               # TypeScript types
 └── mock/                # mock data
```

## Backend Directories

```bash
backend/                  # ERP 2.0 新 Flask API baseline
 ├── app/
 └── tests/

restserver/               # GitHub main 提供的既有 EWDB Flask API 參考實作
 └── package/
      ├── restserver/api/ # Blueprint routes and API executors
      ├── dbwrapper/      # SQLAlchemy table definitions and DB wrapper
      ├── auth/           # Session/token login logic
      ├── inventory/
      ├── mes/
      ├── bom/
      └── statistic/
```

## 文件目錄

```bash
docs/
 ├── design-system/       # UI / UX 設計規範
 ├── architecture/        # 架構文件
 ├── backend/             # API、coding convention、code review
 ├── database/            # EWDB schema、ERD、schema review
 └── codex/               # Codex 安裝與使用說明
```

## Current Baselines

- Database: `docs/database/EWDB_20260521.sql`
- Database review: `docs/database/EWDB_20260521_BASELINE_REVIEW.md`
- Restserver code review: `docs/backend/RESTSERVER_CODE_REVIEW_20260521.md`
