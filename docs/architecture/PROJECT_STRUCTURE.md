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

## 文件目錄

```bash
docs/
 ├── design-system/       # UI / UX 設計規範
 ├── architecture/        # 架構文件
 └── codex/               # Codex 安裝與使用說明
```
