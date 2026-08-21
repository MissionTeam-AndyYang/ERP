# ItemCenterScreen 後端流程與演算法設計

> Status: Backend Flow Proposal / Pending Engineer Review  
> Related API Proposal: `docs/spec/api-proposal/item_center_proposal.md`  
> Scope: V1 read-only Core

## 1. 設計原則

1. 以料品主檔為核心，僅回傳目前畫面需要的欄位。
2. 不產生寫入行為，不建立主檔維護 task，不修改 workflow。
3. 庫存數字統一使用 Warehouse 庫存快照共用邏輯，不另行重算。
4. BOM 關聯只回傳已能由 BOM 資料表確認的關係，不推測未建立的 BOM。
5. 後端回傳 enum code；前端負責中文與多國語言顯示。
6. `maintenanceSuggestions[]` 僅代表 read-only 主檔維護建議，不是 workflow task，不設定下一步轉交部門。

## 工程師回覆

| 項目 | 回覆與文件調整 |
|---|---|
| 第一版欄位範圍 | 已將流程收斂為目前 `ItemCenterScreen` 需要的 KPI、分類摘要、品項清單與 read-only 維護建議；不再產生暫未使用的最新批號、最新活動時間、關聯單據、下一步負責部門或處理期限。 |
| `attention` / `missing_required_data` | 第一版整合為 `masterStatusCode=maintenance_needed`，差異改由 `maintenanceRiskCode` 或 `maintenanceSuggestions[].suggestionTypeCode` 表示。 |
| `summary` 統計 | `attentionItemCount` 與 `missingRequiredDataCount` 整合為 `maintenanceItemCount`。 |
| `masterTasks` 定位 | 依工程師提問 V2，`masterTasks[]` 已更名為 `maintenanceSuggestions[]`。此資料是畫面右側「主資料待維護事項」的 read-only 維護建議，不建立 workflow、不寫入資料表、不指定 `ownerDepartment`。 |
| `bomRoleCode` | 依工程師提問 V2，第一版畫面暫不顯示 BOM 角色，因此 dashboard 與 detail 都不回傳 `bomRoleCode`。BOM 關聯只保留 `bomCount` 或 `bomUsage[]` 的必要識別資料。 |

## 工程師回覆V2

| 項目 | 回覆與文件調整 |
|---|---|
| 移除 `bomRoleCode` | Step 4 改為只彙總 `bomCount` 與 detail 所需的 BOM 使用清單，不再判斷或回傳 BOM 角色 code。 |
| 移除 `unitShipping` | 主檔候選內部結構移除 `unitShipping`，僅保留目前品項中心畫面使用的 `unitWarehouse` 與 `unitProduct`。 |
| `masterTasks` 更名 | 所有流程步驟中的 `masterTasks[]` 改為 `maintenanceSuggestions[]`，欄位改為 `suggestionId`、`itemNo`、`suggestionTypeCode`、`riskLevelCode`。 |
| 欄位收斂 | 流程不再產生目前畫面未使用的下一步負責部門、處理期限、來源單據、BOM 角色、出貨單位或停用狀態。 |

## 2. GET `/api/v2/items/dashboard`

### Step 1：解析查詢條件

- 讀取 `keyword`、`itemCategory`、`itemSubCategory`、`itemType`、`masterStatusCode`、`hasStock`、`hasBom`、`start`、`count`。
- `start` 小於 0 時視為 0。
- `count` 預設 50，最大 100。

### Step 2：建立料品主檔候選集合

- 從 `material` 讀取原料、物料、膠捲。
- 從 `inproduct` 讀取在製品。
- 從 `product` 讀取製成品。
- 從 `goods` 讀取貨品。
- 統一轉換為內部結構：

```json
{
  "itemNo": "String",
  "itemName": "String",
  "itemCategory": "Integer",
  "itemSubCategory": "Integer",
  "itemType": "Integer",
  "unitWarehouse": "Integer",
  "unitProduct": "Integer",
  "creationTime": "Integer"
}
```

### Step 3：補充庫存摘要

- 呼叫 Warehouse 庫存快照共用邏輯取得目前庫存列。
- 依 `itemNo` 彙總：
  - `hasStock`
  - `currentQuantity`
  - `availableQuantity`
  - `reservedQuantity`
  - `qualityHoldQuantity`
  - `warehouseCount`
  - `batchCount`
- 過濾批號庫存數量為 0 的資料。

### Step 4：補充 BOM 關聯摘要

- 從 `bom_item` 判斷料品是否作為投入料使用。
- 從 `product_spec`、`product_bom_spec`、`inproduct_bom_spec` 判斷是否與產品或在製品規格建立關聯。
- 依 `itemNo` 彙總：
  - `bomCount`

### Step 5：判斷主檔狀態與維護風險

建議規則如下，待工程師確認後實作：

| 條件 | `masterStatusCode` | `maintenanceRiskCode` |
|---|---|---|
| 缺少 `unitWarehouse` 且此品項需庫存管理 | `maintenance_needed` | `missing_unit` |
| 製成品或在製品缺少 BOM 關聯 | `maintenance_needed` | `missing_bom` |
| 原料、物料、膠捲無庫存訊號且無近期批號 | `maintenance_needed` | `missing_stock_signal` |
| 無上述風險 | `ready` | `normal` |
| 主檔資料可讀取但狀態無法判斷 | `unknown` | `unknown` |

### Step 6：套用篩選、排序與分頁

- 套用 query 條件。
- 排序建議：
  1. `masterStatusCode=maintenance_needed`
  2. 料品品項類別順序：原料、物料、膠捲、在製品、製成品、貨品、其他
  3. `itemNo` 由小到大
- 套用分頁。

### Step 7：建立 `summary`、`categorySummary` 與 `maintenanceSuggestions`

- `summary` 由篩選前/後資料彙總產生，需與 API 文件欄位一致。
  - `summary.maintenanceItemCount` 統計 `masterStatusCode=maintenance_needed` 的品項數。
- `categorySummary` 依 `itemCategory` 彙總。
- `maintenanceSuggestions` 由 Step 5 的維護風險產生 read-only 建議事項，只回傳 `suggestionId`、`itemNo`、`suggestionTypeCode`、`riskLevelCode`。
- 不回傳 `ownerDepartment`、`refCategory`、`refNo`、`dueTimestamp`，避免把主檔維護訊號誤解為正式 workflow task。

## 3. GET `/api/v2/items/{item_no}/detail`

### Step 1：驗證 `item_no`

- 若 `item_no` 為空字串，回傳 invalid parameter。
- 若查無任何料品主檔，回傳 record not found。

### Step 2：讀取主檔資料

- 依料品類別或 `item_no` 查詢 `material`、`inproduct`、`product`、`goods`。
- 若同一 `item_no` 在多張主檔表同時存在，需回報工程師確認，不由後端自行合併推測。

### Step 3：建立庫存摘要

- 使用 Warehouse 庫存快照共用邏輯，強制套用 `itemNo=item_no`。
- 彙總目前庫存、可用量、預留量、品檢保留量、倉庫數與批號數。

### Step 4：建立 BOM 使用清單

- 查詢 `bom_item`、`product_spec`、`product_bom_spec`、`inproduct_bom_spec`。
- 每筆關聯回傳 `bomNo`、`bomVersion`、`quantity`、`unit`、`effectiveTimestamp`。
- 若 BOM 版本資料不存在，`effectiveTimestamp` 回傳 0。

### Step 5：建立近期批號清單

- 查詢 `batch_number`，依 `date`、`creationTime`、`id` 由新到舊。
- 只回傳近期必要筆數，建議最多 20 筆。
- 庫存數量與風險等級由 Warehouse / Batch 共用規則補充。

### Step 6：建立主檔待維護事項

- 使用 dashboard 同一套規則建立 `maintenanceSuggestions[]`，避免清單與 detail 顯示不一致。
- `maintenanceSuggestions[]` 只回傳 read-only 維護建議，不回傳下一步負責部門或處理期限。

## 4. 效能與重構建議

1. 建議封裝 `CItemMasterContextBuilder`，負責統一讀取四類料品主檔並轉成共用資料結構。
2. 建議封裝 `CItemMasterStatusEvaluator`，集中處理 `masterStatusCode` 與 `maintenanceRiskCode`。
3. 庫存摘要需共用 `CWarehouseInventoryContextBuilder`，不可重新實作庫存演算法。
4. Dashboard 清單分頁前可先以 query 條件縮小主檔候選範圍，避免一次處理全部料品造成效能壓力。
5. Detail API 的 BOM、批號、庫存資料應各自限制查詢範圍，避免回傳過大 payload。

## 5. 待工程師確認事項

| 項目 | 需確認內容 | 工程師回覆 |
|---|---|---|
| 停用狀態來源 | 現有 `material`、`inproduct`、`product`、`goods` 是否有可判斷 inactive 的欄位或需新增欄位。 | 目前暫不規劃設計停用／啟用功能；本版不回傳 `inactive` 狀態。 |
| 料品重複 no | 若同一 `item_no` 出現在多張主檔表，是否視為資料異常。 |主檔候選來源包含 `material`、`inproduct`、`product`、`goods`；若同一 `item_no` 出現在多張主檔表，建議視為資料異常並列入工程師確認，不由 API 自行合併推測。|
| 製成品 / 在製品 BOM 必要性 | 第一版是否將缺 BOM 視為維護訊號，或只作一般資訊缺口。 |第一版不再區分 `attention` 與 `missing_required_data`，統一以 `masterStatusCode=maintenance_needed` 表示待維護，並以 `maintenanceRiskCode=missing_bom` 說明原因。|
| 原料庫存訊號 | 原料、物料、膠捲沒有庫存與近期批號時，是否需要列入 `maintenanceSuggestions[]`。 | 可列入 read-only `maintenanceSuggestions[]` 作為維護建議，但不建立 workflow task，也不回傳下一步轉交部門。 |
| 部門 code | 原 `masterTasks[].ownerDepartment` 對研發、倉庫、生管、採購的對應 code 是否已有正式定義。 | 第一版已移除 ownerDepartment，避免將維護建議誤解為正式流程轉交。 |
