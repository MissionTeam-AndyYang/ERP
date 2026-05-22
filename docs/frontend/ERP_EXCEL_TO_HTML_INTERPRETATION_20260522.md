# ERP Excel To HTML Interpretation

日期：2026-05-22

來源檔案：

- `docs/frontend/恆旺_ERP_Web介面.xlsx`
- `docs/frontend/恆旺_ERP_Web Markup.html`

## Purpose

This document captures how the current Excel UI workbook appears to have been interpreted into the generated HTML prototype. It gives us a shared language for future Excel edits before converting them into the new frontend architecture.

## Workbook Role

The Excel workbook is best treated as an ERP screen specification, not just a visual mockup. It encodes:

- Main modules.
- Sidebar menu hierarchy.
- Screen groups.
- Tabs.
- Table group headers.
- Field headers.
- Row examples and default values.
- Row actions.
- Detail/content screens.
- Business notes and default rules.

## Sheet Meaning

| Sheet | Interpreted Role |
| --- | --- |
| `1.0 選單` | Initial Basic Data screens |
| `2.0 選單` | Initial Formula/Production Item screens |
| `3.0 選單` | Warehouse screens |
| `4.0 選單` | Sales/Order screens |
| `5.0 選單` | Purchasing screens |
| `6.0 選單` | Production screens |
| `7.0 選單` | Traceability screens |
| `11.0 選單` | Newer hierarchical Basic Data screens |
| `12.0 選單` | Newer hierarchical Formula/Production Item screens |
| `主畫面` | Combined screen specification |
| `其他 選單` | Additional traceability, HR, and miscellaneous screens |

## Inferred Syntax

### Main Menu

The `主選單` block defines top-level navigation modules.

Example:

```txt
主選單
基本資料
配方產製
倉儲管理
訂購管理
採購管理
生產管理
溯源管理
```

In HTML this becomes the top navigation bar.

### Sidebar Menu

The `次選單` block defines the sidebar items under a module.

Plain rows become first-level sidebar items.

Rows prefixed with `++` become second-level grouped items.

Rows prefixed with `--` become third-level child items.

Example:

```txt
料品品項
  ++ 材料
    -- 原料
    -- 物料
    -- 膠捲
  ++ 產品
    -- 在製品
    -- 製成品
```

### Screen Body

The `選單主畫面` row marks the start of screen definitions.

Rows after it are interpreted as modules, sidebar groups, screen groups, tabs, and detail screens.

### Tabs

Text wrapped in angle brackets defines a tab or table section.

Example:

```txt
<企業>
<客戶 / 廠商>
<品項>
<成本>
```

In HTML this becomes a `tab-btn` and a matching table panel.

### Table Headers

The row containing `<...>` plus the following rows define table headers.

Merged cells become grouped table headers using `colspan` or `rowspan`.

Multiple header rows become stacked headers.

Example:

```txt
<客戶 / 廠商> | 公司機構 | 帳款
              | 編號 | 統一編號 | 名稱 | 聯絡人 | 項目 | 類型 | 方式 | 月結 | 匯款
              |      |          |      | 姓名 | 電話 |      |      |      | 結帳日 | 帳款天數
```

### Row Actions

The far-right notes/action column, usually around column Q, defines available row commands.

Common action terms:

| Excel Text | UI Meaning |
| --- | --- |
| `新增` | Add button in toolbar |
| `資訊` | Info/edit row action |
| `修改` | Edit behavior inside info/action |
| `刪除` | Delete row action |
| `內容` | Open content/detail screen |

### Business Notes

Rows or cells starting with `**` are business rules, defaults, or hints.

Examples:

```txt
** 類型 = "現結", 結帳日 = "0", 帳款天數 = "0"
** 比率單位為百分比
** 最新交易合約
```

These should become:

- Field helper text.
- Validation rules.
- Default values.
- Workflow notes.
- API mapping notes.

They should not be treated as normal table columns unless explicitly intended.

### Detail Screens

Rows starting with `內容 (...)` define detail/content pages that open from a `內容` row action.

In HTML these appear as separate hidden `sub-wrap` blocks with back navigation.

## Generated HTML Structure

The generated HTML currently includes:

- 8 top navigation modules.
- 46 sidebar items.
- 57 screen wrappers.
- 11 detail wrappers.
- 135 tabs.
- 151 tables.

The HTML is valuable as a complete UI inventory, but it is too broad to become the first production frontend layout without consolidation.

## Recommended Future Editing Rules

When updating the Excel workbook:

1. Use `主選單` only for true top-level modules.
2. Use `次選單` for sidebar functions.
3. Use `++` and `--` only when a nested sidebar is intentionally needed.
4. Use `<Tab Name>` for each tab/table section.
5. Use merged cells for table header groups.
6. Put row actions in the far-right action/notes column.
7. Prefix implementation notes and default rules with `**`.
8. Use `內容 (...)` for detail pages opened from row action buttons.
9. Keep one screen group close together so conversion can infer tab ownership.

## Frontend Conversion Guidance

For the new Next.js frontend, do not directly reproduce every Excel tab at the first navigation level.

Instead:

- Convert Excel modules into domain workspaces.
- Convert `<...>` sections into tabs or nested panels only when they support the main workflow.
- Move rarely used master data into Settings/Master Data.
- Convert `**` notes into validation, helper text, or acceptance criteria.
- Map each important table section to a restserver API endpoint or future API gap.
