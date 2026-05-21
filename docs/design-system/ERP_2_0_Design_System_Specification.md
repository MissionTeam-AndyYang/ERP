# ERP 2.0 Design System Specification
# 智慧食品工廠 ERP 設計規範書

## 一、文件目的

本文件目的：建立 ERP 2.0 統一 UI / UX 設計規範，避免 UI 不一致、模組風格混亂、後期難維護、不同開發者風格不統一。

目標風格：現代 SaaS + 智慧工廠風格。

---

## 二、ERP 2.0 UI 核心理念

ERP 2.0 不是傳統 ERP，而是工廠營運控制平台，因此 UI 必須：

- 即時化
- 卡片化
- Dashboard 化
- 流程化
- 易讀化
- 行動化

---

## 三、設計風格定位

Design Style：Modern Industrial SaaS

風格方向：

- 工業科技感
- 現代 SaaS
- MES Dashboard
- Data Visualization
- Dark + Light Hybrid

---

## 四、色彩系統

### Primary Colors

| 名稱 | 色碼 | 用途 |
|---|---|---|
| Primary Blue | #2563EB | 主按鈕、主功能、KPI、Active 狀態 |
| Primary Dark | #1E293B | Sidebar、Dark Header、Dashboard 深色區塊 |

### Status Colors

| 名稱 | 色碼 | 用途 |
|---|---|---|
| Success | #22C55E | 生產正常、良率正常、已完成 |
| Warning | #F59E0B | 缺料、即將到期、注意事項 |
| Danger | #EF4444 | 異常、停機、錯誤 |
| Info | #06B6D4 | 系統資訊、提示 |

### Neutral Colors

| 名稱 | 色碼 |
|---|---|
| Background | #F5F7FA |
| Card Background | #FFFFFF |
| Border | #E2E8F0 |
| Text Primary | #0F172A |
| Text Secondary | #64748B |

---

## 五、Typography

### Font Family

- Primary: Inter, Noto Sans TC
- Fallback: Microsoft JhengHei

### Font Size System

| 用途 | Size |
|---|---|
| Dashboard KPI | 36px |
| Page Title | 28px |
| Section Title | 20px |
| Card Title | 18px |
| Body Text | 14~16px |
| Table Text | 14px |
| Label | 12px |

### Font Weight

| 用途 | Weight |
|---|---|
| KPI | 700 |
| 標題 | 600 |
| 內文 | 400 |
| Label | 500 |

---

## 六、Spacing System

| 名稱 | Size |
|---|---|
| xs | 4px |
| sm | 8px |
| md | 16px |
| lg | 24px |
| xl | 32px |
| 2xl | 48px |

---

## 七、Border Radius

| 用途 | Radius |
|---|---|
| Button | 12px |
| Card | 16px |
| Modal | 20px |
| Input | 12px |

---

## 八、Shadow System

Card Shadow:

```txt
0 2px 8px rgba(15, 23, 42, 0.06)
```

Hover Shadow:

```txt
0 8px 24px rgba(15, 23, 42, 0.12)
```

---

## 九、Layout 規範

ERP 2.0 標準 Layout：

```txt
Top Navbar
Sidebar + Main Content
Dashboard / Module Content
```

Sidebar Width：展開 280px，收合 88px。

Content Padding：24px。

---

## 十、Top Navbar 規格

必須包含：

- 系統 Logo
- 工廠名稱
- 通知
- 使用者資訊
- 快速搜尋
- Dark Mode 切換

高度：72px。

---

## 十一、Sidebar 規格

Sidebar 是 ERP 主導航中心。

| 模組 | Icon 建議 |
|---|---|
| Dashboard | Home |
| 生產中心 | Factory |
| 倉儲中心 | Warehouse |
| 品保中心 | Shield |
| 溯源中心 | Search |
| 採購中心 | ShoppingCart |
| 財務中心 | DollarSign |
| AI 中心 | Sparkles |
| 系統設定 | Settings |

---

## 十一之一、EWDB 20260521 模組對齊

UI 模組與資料模型需以 `docs/database/EWDB_20260521.sql` 的 domain group 作為資訊架構基準。畫面命名可以維持使用者熟悉的中文模組，但資料來源、篩選條件與明細頁必須能追溯到下列表群。

| UI 模組 | 主要資料表群 | 設計重點 |
|---|---|---|
| 基礎資料 | enterprise, company, bank_account, material, product, goods, employee, device | 高密度列表、快速搜尋、狀態與關聯摘要 |
| 銷售中心 | quotation, contract, product_order, shipping_order, order_payment | 單據流程、客戶/品項關聯、付款狀態 |
| 採購中心 | purchase_request, purchase_request_item, purchase_order, goods_receipt_note | 請購到收貨流程、缺漏步驟提示 |
| 倉儲中心 | batch_number, inventory_order, inventory_record, inventory_delta, ship_wh_alias, ship_wh | 批號、庫位、出入庫、月統計 |
| 生產中心 | factory, process, production_line, station, equipment, work_order, process_order, production_data | 產線狀態、工單進度、報工明細 |
| APS / 產能 | aps_quantity, aps_quantity_item, pl_man_capacity, pl_item_capacity, pl_item_loss | 產能配置、工時、人力與耗損 |
| BOM / 品項結構 | bom, bom_item, bom1, bom2, product_spec, product_bom_spec | 樹狀結構、版本、用量與損耗 |
| 財務統計 | payment, order_item_month_statistic, shipping_payment, warehouse_payment, labor_wage | 金額彙總、期間篩選、異常檢查 |
| 系統與權限 | member, session, user_group, employee | 登入狀態、角色權限、操作稽核 |

資料表仍保留 EWDB 欄位命名，例如 `creationTime`, `expectedCount`, `checkedCount`, `item_ref_displayName`。前端顯示層可以轉換成中文標籤，但 API contract 與 TypeScript type 應保留原始欄位，避免資料對接時出現隱性 mapping。

---

## 十二、Button 規格

Primary Button：用於儲存、下一步、主要操作。Blue Background、White Text、Radius 12、Height 44。

Secondary Button：用於返回、取消、次要功能。

Danger Button：用於刪除、停止、作廢。

---

## 十三、Input 規格

原則：盡量減少輸入。

Input Height：44px。

必須支援：

- Auto Complete
- Searchable Select
- Default Value
- Barcode Input

---

## 十四、Table 規格

新 ERP 原則：Table 不再是主畫面。Table 只作為明細、查詢、歷史紀錄。

Table Style：Low Border、Hover Highlight、Sticky Header、Rounded Card Container。

---

## 十五、Card System

ERP 2.0 核心 UI 是 Card System。

### KPI Card

用途：今日產量、良率、OEE、停機數。

結構：Title、Value、Trend、Icon、Status Color。

### Production Card

用途：工單、產線、Workflow。

必須包含：狀態、批號、產品名稱、良率、時間。

### Alert Card

用途：缺料、異常、即將到期。

---

## 十六、Status Badge

| 狀態 | 顏色 |
|---|---|
| 生產中 | 綠 |
| 停機 | 紅 |
| 清洗中 | 藍 |
| 待料 | 橘 |
| 已完成 | 灰 |

---

## 十七、Dashboard 規格

Dashboard 原則：一眼看懂工廠狀態。

Dashboard Sections：

- KPI 區：今日產量、良率、OEE、異常數
- 生產趨勢：Line Chart、Bar Chart
- 生產線狀態：Card 化顯示
- Alert Center：異常、缺料、保存期限

---

## 十八、Chart 規格

建議使用 Recharts。

| 圖表 | 用途 |
|---|---|
| Line Chart | 趨勢 |
| Bar Chart | 產量 |
| Pie Chart | 比例 |
| Gauge | OEE |
| Area Chart | 稼動率 |

---

## 十九、Workflow 規格

新 ERP 核心：Workflow > CRUD。

工單流程：

```txt
待生產 → 生產中 → 品檢 → 包裝 → 完工
```

Workflow UI：Timeline、Kanban、Stepper、Status Card。

---

## 二十、Mobile / Tablet 規範

食品工廠必須支援 iPad、PDA、手持設備。

行動化原則：大按鈕、少輸入、掃碼優先、高對比。

---

## 二十一、Dark Mode 規格

智慧工廠建議支援 Dark Mode，適合控制室、大螢幕、MES Dashboard。

| 名稱 | 色碼 |
|---|---|
| Dark Background | #0F172A |
| Dark Card | #1E293B |

---

## 二十二、角色化 UX

| 角色 | 主要資訊 |
|---|---|
| 廠長 | KPI、OEE、異常、訂單 |
| 生管 | 工單、排程、產線 |
| 倉管 | 缺料、入庫、出庫 |
| 品保 | 品檢、異常批號、保存期限 |

---

## 二十三、UX 核心原則

- 能看不要查
- 能選不要打
- 能掃不要 Key
- 能流程不要表單
- 能圖表不要報表

---

## 二十四、第一階段 UI 完成標準

完成後系統應該：

- 看起來像 SaaS
- 看起來像 MES
- 不像舊 ERP
- 操作直覺
- 資訊可視化
- 容易教育訓練
