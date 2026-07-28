# PurchasingWorkspaceScreen API 組合提案

> Status: Proposal / Pending Engineer Review
> Screen: `PurchasingWorkspaceScreen`
> Route: `/purchasing`
> Related proposal: `purchasing_purchase_order_first_proposal.md`
> Design rule: 本文件不新增重複的聚合 endpoint；定義畫面如何組合已確認的五支 read-only API。

## 1. 畫面定位

採購中心第一版提供管理者與採購主管以採購單為主視角，追蹤採購需求、交期風險、到貨驗收入庫與供應商狀況。畫面只讀，不建立或修改請購、採購、驗收、入庫及付款資料。

## 2. API 組合

| View / UI 區塊 | API | 觸發時機 | 資料用途 |
|---|---|---|---|
| KPI 與採購單頁籤 | `GET /api/v2/purchasing/purchase-orders/dashboard` | 進入頁面、日期/供應商/關鍵字變更 | 採購金額、未收缺口、逾期 KPI 與採購單資料列 |
| 交期風險頁籤 | `GET /api/v2/purchasing/purchase-orders/delivery-risk` | 切換頁籤或風險篩選變更 | 逾期、今日到期、缺口、正式影響來源 |
| 到貨驗收入庫頁籤 | `GET /api/v2/purchasing/goods-receipts/dashboard` | 切換頁籤或日期變更 | 進貨單、實收數量、收貨與入庫交接 code |
| 供應商追蹤頁籤 | `GET /api/v2/purchasing/suppliers/dashboard` | 切換頁籤或日期/供應商變更 | 供應商採購量、逾期筆數、未收數量與金額 |
| 右側採購單明細 panel | `GET /api/v2/purchasing/purchase-orders/{purchase_order_no}/detail` | 使用者選取採購單 | 採購單、請購、進貨、來源、庫存、workflow 與正式文件關聯 |

## 3. 共用 Request Contract

所有列表 API 使用：

| Parameter / Header | Type | Required | Description |
|---|---|---|---|
| `startDate` | String | Yes | 使用者時區的起始日，`YYYY-MM-DD`。 |
| `endDate` | String | Yes | 使用者時區的結束日，`YYYY-MM-DD`，含當日。 |
| `x-timezone` | Header String | Yes | IANA timezone，例如 `Asia/Taipei`；由 API client 統一送出。 |
| `start` | Integer | No | 頁面分頁起點，預設 0。 |
| `count` | Integer | No | 頁面資料筆數，預設 50，上限 100。 |
| `keyword` | String | No | 採購單、料號或品名搜尋；僅 dashboard 與 delivery-risk 使用。 |
| `supplierNo` | String | No | 供應商 no 篩選；僅 dashboard、delivery-risk 與 suppliers 使用。 |

前端保存查詢狀態，切換頁籤時保留日期區間；切換頁籤不將日期默默重設為今日，也不將任意歷史區間縮短為 7d/30d。

## 4. 畫面資料組合規則

1. `purchase-orders/dashboard` 的 `summary` 是主 KPI 來源，不以各頁籤本頁資料自行重算。
2. 每個頁籤維持自己的 `items`、`total`、`start`、`count`；不可把不同 API 的資料列混合後再分頁。
3. 選取資料列時只使用 `purchaseOrderNo` 導向 detail API；前端不由 item no、日期或名稱推導關聯。
4. `riskLevel`、`riskCode`、`warehouseStatusCode`、`receivingStatusCode`、`nextOwnerDepartment` 與 item category/unit 都是 code，由前端 i18n map 轉換。
5. API 缺少正式關聯時，前端顯示 unknown、空值或空集合；不可用 mock 值補成正常、已入庫或已合格。
6. Quality V1 不呈現品檢明細與 KPI；若 detail 回傳 `deferred`，只顯示待後續版本處理的狀態 code。

## 5. Error / Loading / Empty State

- 初次載入：頁面顯示 skeleton，四個頁籤可見但資料區分別顯示 loading。
- 單一頁籤 API 失敗：只標示該頁籤錯誤，不清除其他已成功資料。
- 查無資料：顯示該查詢區間沒有資料，不切換到 mock。
- Detail API 失敗：保留已選資料列，明確標示明細不可用。
- 日期格式錯誤或結束日早於起始日：前端阻止送出；後端仍需回傳既有 validation error。

## 6. Engineer Review Questions

1. 五支既有 API 是否維持同一日期、分頁與錯誤 response contract？
2. 切換頁籤時是否允許平行查詢，或工程師希望採序列查詢以降低 DB 同時負載？
3. Detail panel 的 inventory/workflow 欄位缺資料時，是否維持 proposal 定義的 `0`、空集合與 `unknown`？
4. Engineer runtime review 是否確認 `supplierNo`、`keyword` 與日期範圍均在 SQL query 層套用，而非查回全部資料後由 Python 過濾？

## 7. 非本次範圍

- 不新增 `/api/v2/purchasing/workspace` 重複聚合 API。
- 不設計 POST/PUT/DELETE。
- 不新增採購、品保或 APS schema。

