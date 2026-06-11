# 無前端開發環境查看 ERP 前端畫面指南

日期：2026-06-11  
對象：後端工程師、API reviewer  
目的：在未安裝 Node.js、npm 或 Next.js 前端環境的情況下，仍能理解第一版 ERP 前端畫面、操作流程與 API 使用情境。

## 建議查看順序

1. 先看靜態 HTML 畫面，快速理解 ERP 畫面規劃與操作架構。
2. 再看 Warehouse 相關 UX/API 文件，理解第一個 API integration target。
3. 最後依 API proposal 檢查資料集、欄位語意與處理流程是否符合使用情境。

## 方法一：直接開啟靜態 HTML

本次已提供 Warehouse 第一版靜態預覽，工程師可直接開啟：

```txt
docs/frontend/preview/warehouse_overview_static_preview.html
```

此檔案用於 API review，內容對應 Warehouse 第一版核心使用情境：

1. 價值與倉位。
2. 風險警示。
3. 待處理入出庫。
4. 庫存明細與批號追溯。

若 repo 中已有下列檔案，工程師可以不用安裝任何前端環境，直接用瀏覽器開啟：

```txt
docs/frontend/恆旺_ERP_Web Markup.html
```

操作方式：

1. 在檔案總管找到 `docs/frontend/恆旺_ERP_Web Markup.html`。
2. 使用 Chrome、Edge 或其他瀏覽器開啟。
3. 依畫面中的模組與區塊理解整體 ERP 操作流程。

注意：

- 這是靜態 HTML，適合用來理解畫面結構與操作情境。
- 它不會呼叫後端 API。
- 它不等同於目前 Next.js React 程式的 runtime 結果。

## 方法二：查看前端規格文件

若只需要理解 Warehouse 第一版需求，建議閱讀：

```txt
docs/frontend/ERP_WAREHOUSE_WORKSPACE_SPEC_20260522.md
docs/frontend/ERP_WAREHOUSE_API_FIELD_READINESS_20260525.md
docs/frontend/ERP_WAREHOUSE_ORDERS_MOCK_TO_API_MAPPING_CHECKLIST_20260526.md
```

這三份文件可協助工程師理解：

1. Warehouse 頁面的使用者目標。
2. 前端目前需要的資料結構。
3. 哪些欄位已可對應 API，哪些欄位仍需確認資料來源。

## 方法三：查看 API 草案

Warehouse API 草案位置：

```txt
docs/spec/api-proposal/warehouse_overview_api.md
```

請工程師特別 review：

1. API route 是否適合新增為 `/api/v1/warehouse/*`。
2. 庫存價值、預留量、可用量、品檢保留量的演算法。
3. 倉儲容量與佔用板數的資料來源。
4. 今日待處理入出庫任務的來源單據與狀態判定。
5. 欄位名稱是否能與 DB schema 和 restserver coding convention 對齊。

## 若要查看目前 React/Next.js 實際畫面

後端工程師不需要自行安裝前端環境。建議由已具備前端環境的人員產出以下其中一種交付物後放入 GitHub：

```txt
docs/frontend/preview/screenshots/
docs/frontend/preview/videos/
docs/frontend/preview/static-html/
```

建議輸出內容：

| 模組 | 建議檔案 | 說明 |
| --- | --- | --- |
| Manager Dashboard | `manager-dashboard.png` | 管理者第一版 Dashboard。 |
| Warehouse | `warehouse-overview.png` | 倉庫經營總覽，API review 優先。 |
| Warehouse Risk | `warehouse-risk.png` | 風險警示頁籤。 |
| Warehouse Tasks | `warehouse-tasks.png` | 待處理入出庫頁籤。 |
| Warehouse Detail | `warehouse-detail.png` | 庫存明細與批號追溯。 |

## Warehouse API Review 建議流程

工程師可依下列方式檢查 API 是否符合前端使用情境：

1. 先看 Warehouse 畫面的 KPI：確認是否需要 `summary` 資料集。
2. 看「價值與倉位」：確認是否需要 `inventoryValueByCategory` 與 `capacityByWarehouse`。
3. 看「風險警示」：確認是否需要 `riskAlerts`，以及三種風險是否可由 DB 推導。
4. 看「待處理入出庫」：確認是否需要 `pendingTasks`，以及來源單據是否完整。
5. 看「庫存明細」：確認是否需要獨立 `GET /api/v1/warehouse/inventory`。

## 對工程師的重點提醒

- 前端畫面目前以管理者需求為主，不是單純 CRUD。
- Warehouse 第一版重點是庫存價值、倉儲空間、風險、待處理入出庫、批號追溯。
- API response 不一定要直接等於前端 type；可由 `src/services/warehouse-api.ts` 做 mapper。
- 需要工程師確認的地方，請直接回覆在 `warehouse_overview_api.md` 的 Review Checklist 對應項目。
