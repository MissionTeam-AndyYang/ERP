# PurchasingWorkspaceScreen API 組合流程與演算法

> Status: Proposal / Pending Engineer Review
> Screen: `PurchasingWorkspaceScreen`
> Proposal: `purchasing_workspace_proposal.md`

## 1. 初始化查詢狀態

1. 前端以使用者時區建立 `startDate` 與 `endDate`；預設值可為目前日期，但不限制後續查詢跨度。
2. 驗證日期格式與 `startDate <= endDate`。
3. 統一建立 request context：`x-timezone`、日期、keyword、supplierNo、start、count。
4. Dashboard tab 預設先載入採購單 dashboard；其他 tab 可延遲至切換時查詢，避免初次載入同時打五支 API。

## 2. 採購單頁籤

1. 呼叫 `purchase-orders/dashboard`。
2. 以完整 response 的 `summary` 建立 KPI。
3. 以 `items[]` 建立主表；後端已完成數量、金額、風險與請購關聯計算，前端只做 code localization。
4. 點擊資料列取得 `purchaseOrderNo`，呼叫 detail API。

## 3. 交期風險頁籤

1. 呼叫 `purchase-orders/delivery-risk`，不要先呼叫 dashboard 再自行判斷風險。
2. 依 `riskLevel` 與 `riskCode` 顯示風險列。
3. `shortageCount` 與 `shortageValue` 直接使用 API 值，不用前端重新計算。
4. `impactSourceType`、`impactSourceNo` 與 `followUpCode` 僅作 code/來源識別，不產生後端未提供的說明文字。

## 4. 到貨驗收入庫頁籤

1. 呼叫 `goods-receipts/dashboard`。
2. 以 `receivingStatusCode` 呈現收貨處理，以 `warehouseStatusCode` 呈現入庫交接；兩者不可合併成單一顯示狀態。
3. `expectedCount`、`checkedCount`、`receivedCount` 分別呈現排定數量、本張實收數量與截至該筆的收貨淨值。
4. `nextOwnerDepartment` 只由 code map 成部門名稱；為 0 或缺值時顯示 unknown。

## 5. 供應商追蹤頁籤

1. 呼叫 `suppliers/dashboard`。
2. 使用 API 已聚合的 supplier row，不由前端把採購單明細重新分組。
3. `purchaseOrderCount`、`openPurchaseOrderCount`、`latePurchaseOrderCount` 是筆數；`pendingReceiptCount` 是數量，顯示時不可混淆。

## 6. Detail Panel

1. 以使用者選取的 `purchaseOrderNo` 呼叫 detail API。
2. 依序呈現採購單、請購、供應商、進貨、來源、庫存、workflow 與 related documents。
3. 空值、空陣列與 `unknown` 保留其資料語意；不可透過資料相似度補造關聯。
4. 切換選取列時取消或忽略前一筆尚未完成的 request，避免舊 response 覆蓋新選取資料。

## 7. 效能與一致性

1. 頁籤資料各自快取 query key：`view + startDate + endDate + timezone + filters + page`。
2. 同一查詢條件不可重複請求；日期或篩選變更才使對應 cache invalidation。
3. 後端列表必須在 SQL query 套用日期、supplier、keyword、排序及分頁，避免無界限載入。
4. 前端不複製 Warehouse snapshot、workflow 或收貨淨值演算法。

## 8. Engineer Review Gate

工程師確認本文件後，才可進行 PurchasingWorkspaceScreen 的 API 串接。工程師尚未確認前，本文件只作為設計交換與前端 mock 預覽依據。

