# BatchCenterScreen API 後端流程與演算法

> Status: API Proposal / Pending Engineer Review  
> Screen: `BatchCenterScreen`  
> Proposal: `batch_center_proposal.md`

## 1. 共用處理原則

1. 每次設計與實作前先閱讀 `AGENTS.md`、`docs/spec/database/index.md` 與本提案文件。
2. 建立單一 DB session；若 service 對外方法不需要外部共用 session，應在函式內自行建立 session。
3. 驗證 `date`、`keyword`、`itemCategory`、`itemSubCategory`、`itemType`、`warehouseNo`、`batchNo`、`riskLevelCode`、`qaStatusCode`、`batchStageCode`、`availabilityCode`、`start`、`count`。
4. 所有目前庫存數量與庫存價值相關計算，應重用已建立的 `CWarehouseInventorySnapshotCalculator` 或既有 Warehouse 庫存快照共用邏輯，不建立第二套月結與 delta 補算演算法。
5. 批號來源單據固定優先以 `batch_number.refCategory`、`batch_number.ref_no` 回傳；不得使用 `sourceType` 命名，也不得以 inventory record 覆蓋批號來源。
6. 庫存批號列若目前庫存數量 `currentQuantity <= 0`，不回傳至 dashboard、distribution 或 detail 的 `stockByWarehouse[]`。
7. 後端只回傳 enum code、數值與資料庫欄位，不回傳前端顯示用繁中文字串；前端負責多國語系。
8. 數值精度遵循既有規範：單價小數第 4 位、數量／重量小數第 2 位、金額四捨五入取整數。

## 2. 共用資料集合

### 2.1 庫存快照

1. 以查詢基準時間 `date` 呼叫 Warehouse 庫存快照共用邏輯。
2. 套用 `warehouseNo`、`itemCategory`、`itemSubCategory`、`itemType`、`itemNo`、`batchNo` 與 `keyword` 篩選。
3. 只保留 `currentQuantity > 0` 的庫存列。
4. 每筆快照至少需包含 `itemNo`、`itemName`、`itemCategory`、`itemSubCategory`、`itemType`、`warehouseNo`、`batchNo`、`unit`、`currentQuantity`、`currentAmount`。

### 2.2 批號主檔

1. 批次查詢 `batch_number`，以快照中的 `batchNo` 集合作為查詢條件。
2. 回填 `validDate`、`validDays`、`sourceRefCategory`、`sourceNo`、`creatorNo`、`creationTime`。
3. 若同一批號有多筆資料，依 `date desc`、`creationTime desc`、`id desc` 取第一筆作為批號主檔資料。

### 2.3 預留與品檢保留

1. 批次查詢 `warehouse_inventory_reservation` 中尚未完成或仍有效的預留紀錄。
2. 批次查詢 `warehouse_quality_hold` 中尚未解除或仍有效的品檢保留紀錄。
3. 以 `itemNo + batchNo + warehouseNo` 作為 stock key 彙總：
   - `reservedQuantity`
   - `qualityHoldQuantity`
   - `quarantineQuantity`
4. `quarantineQuantity` 需等待工程師確認映射規則；未確認前不得自行以任意狀態推測。

### 2.4 板位與倉庫資訊

1. 優先使用 `warehouse_pallet_movement` 彙總目前使用中板數。
2. 若 `warehouse_pallet_movement` 沒有資料，可於工程師確認後以 `batchno_serialno_group` 作為位置 fallback。
3. `locationCode` 回傳主要板位或倉位代碼；多個板位時可取最近異動或數量最大者，但需在正式實作前確認排序規則。
4. `warehouseName` 優先取 `ship_wh_alias.displayName`；若無資料再使用 `inventory_record.warehouse_displayName` fallback。

### 2.5 Workflow 與需求訊號

1. 查詢 `workflow_task_state` 中與 stock key、itemNo 或 batchNo 有關，且狀態為 pending、partial、blocked 的未完成任務。
2. `ownerDepartment` 取風險最高或 due date 最近任務的 `nextOwnerDepartment`。
3. `demandSignals[]` 只取有正式來源可佐證的訊號：
   - reservation 對應出貨或生產需求。
   - workflow task 對應下一步待處理部門。
   - quality hold 對應品檢阻塞。
4. V1 不呼叫 APS，不自行推測未來工單短缺。

## 3. 風險與狀態判斷

### 3.1 效期風險

1. 若 `itemCategory` 為物料(2)或膠捲(3)，不計算少於 1/3 效期風險。
2. 若 `validDate=0` 或 `validDays=0`，不判斷近效期，但可保留 `unknown` 狀態供前端顯示資料不足。
3. 計算剩餘效期比例：
   - `remainingSeconds = validDate - queryTimestamp`
   - `totalSeconds = validDays * 86400`
   - `remainingRatio = remainingSeconds / totalSeconds`
4. 若 `remainingSeconds < 0`，加入 `expired`，風險等級 `high_risk`。
5. 若 `remainingRatio <= 1/3`，加入 `near_expiry`，風險等級至少 `attention`。

### 3.2 可用性

1. `availableQuantity = max(currentQuantity - reservedQuantity - qualityHoldQuantity - quarantineQuantity, 0)`。
2. 若 `availableQuantity > 0`，可用性包含 `available`。
3. 若 `reservedQuantity > 0`，可用性包含 `reserved`。
4. 若 `qualityHoldQuantity > 0`，可用性包含 `quality_hold`。
5. 若 `quarantineQuantity > 0`，可用性包含 `quarantine`。
6. `availabilityCode` 篩選在彙總完成後套用，避免尚未扣除預留／品檢前誤判。

### 3.3 品檢狀態

1. 若存在 active quality hold 且狀態代表阻擋，`qaStatusCode=blocked`。
2. 若存在 active quality hold 但非阻擋，`qaStatusCode=quality_hold`。
3. 若存在未完成品檢 workflow task，`qaStatusCode=inspection`。
4. 以上皆無時，`qaStatusCode=released`。
5. 資料不足時回傳 `unknown`。

### 3.4 批號階段

判斷優先順序如下，先命中者為 `batchStageCode`：

1. `quarantineQuantity > 0`：`quarantine`
2. `qualityHoldQuantity > 0`：`quality_hold`
3. `reservedQuantity > 0` 且 `availableQuantity <= 0`：`reserved`
4. `availableQuantity > 0`：`available`
5. `currentQuantity > 0`：`stocked`
6. 僅存在進貨或入庫未完成任務且尚無庫存：`inbound_pending`
7. 其他：`unknown`

### 3.5 風險等級

1. 命中 `expired`、`quarantine`、`quality_hold` 且影響已預留或待出貨數量時，`riskLevelCode=high_risk`。
2. 命中 `near_expiry`、`reserved`、`workflow_blocked` 或 `stock_shortage` 時，`riskLevelCode=attention`。
3. 無風險時 `riskLevelCode=normal`。
4. 料品層級 `highestRiskLevelCode` 取所有批號分布列最高風險等級。
5. `primaryRiskCode` 依優先順序選擇：`expired` > `quarantine` > `quality_hold` > `stock_shortage` > `workflow_blocked` > `near_expiry` > `reserved` > `normal`。

## 4. GET `/api/v2/batches/dashboard`

1. 建立共用資料集合。
2. 以 `itemNo` 彙總每個料品的批號與倉庫分布。
3. 計算：
   - `totalBatchCount`：目前庫存量大於 0 的不重複批號數。
   - `warehouseCount`：目前庫存量大於 0 的不重複倉庫數。
   - `currentQuantity`、`reservedQuantity`、`qualityHoldQuantity`、`quarantineQuantity`、`availableQuantity`。
   - `earliestValidDate`：該料品有效期限最早的批號。
   - `qaHoldBatchCount`、`quarantineBatchCount`、`nearExpiryBatchCount`。
   - `highestRiskLevelCode`、`primaryRiskCode`、`ownerDepartment`、`demandSignals[]`。
4. 套用風險與狀態篩選。
5. 以 `highestRiskLevelCode`、`earliestValidDate`、`itemNo` 穩定排序；正式實作可依工程師確認補充 `sortBy`。
6. 以 SQL 或可控的中間結果完成分頁。若必須先彙總才能分頁，需確保原始快照已先被篩選至合理範圍，避免全表取回。
7. 回傳 summary、items、total、start、count。

## 5. GET `/api/v2/batches/items/{item_no}/distribution`

1. 驗證 `item_no`。
2. 建立共用資料集合，強制套用 `itemNo=item_no`。
3. 以 `batchNo + warehouseNo` 建立分布列。
4. 回填批號主檔、倉庫名稱、板位、預留、品檢、風險、來源單據與關聯文件。
5. 排序優先順序：
   - `riskLevelCode` 高到低。
   - `validDate` 早到晚，無值排後。
   - `batchNo`、`warehouseNo`。
6. 套用分頁後回傳。

## 6. GET `/api/v2/batches/{batch_no}/detail`

1. 驗證 `batch_no`。
2. 查詢 `batch_number`；不存在時沿用既有 not-found response contract。
3. 建立共用資料集合，強制套用 `batchNo=batch_no`。
4. `stockByWarehouse[]` 由庫存快照加上 reservation、quality hold、pallet movement 彙整，只保留 `currentQuantity > 0`。
5. `inventoryRecords[]` 查詢 `inventory_record.batchNumber=batch_no`，依 `date desc` 排序，第一版最多回傳最近 100 筆。
6. `reservations[]` 查詢此批號的 active / recent reservation。
7. `qualityHolds[]` 查詢此批號的 active / recent quality hold。
8. `palletMovements[]` 查詢此批號的最近板位異動，第一版最多回傳最近 100 筆。
9. `tasks[]` 查詢此批號未完成 workflow task，依 due timestamp 由早到晚排序。
10. 回傳 batch header 與各資料集合；合法空集合回傳空陣列。

## 7. 效能與重構要求

1. Dashboard 與 distribution 不得逐筆批號 N+1 查詢批號主檔、預留、品檢、板位或 workflow。
2. 庫存快照、reservation 彙總、quality hold 彙總、風險判斷、效期判斷需抽成可重用方法或 service，供未來 Warehouse、Traceability 與 Batch Center 共用。
3. 若後續多個 API 需要批號層級資料集合，建議建立 `CBatchInventoryContextBuilder` 或擴充既有 `CWarehouseInventoryContextBuilder`，避免重複實作。
4. 所有 util 函式若可共用，需放在 `restserver/package/util/util.py` 且以 `util_` 開頭。
5. 正式實作需建立 pytest，涵蓋欄位存在、數值計算、空集合、0 庫存過濾、近效期、預留、品檢保留、分頁與錯誤參數。

## 8. 待工程師確認後才能實作的項目

| 項目 | 需要確認原因 |
|---|---|
| `quarantineQuantity` 映射 | 目前文件未確認隔離量是否有獨立狀態或 reason code。 |
| `locationCode` 選擇規則 | 同一批號同一倉庫可能有多個板位，需確認取最近異動、最大數量或回傳多值。 |
| `qaStatusCode` 映射 | 需確認 `warehouse_quality_hold.status` 與品檢 workflow task 的狀態值。 |
| API path 命名 | 需確認 `/api/v2/batches/...` 是否符合工程師對既有 `batchnumber` API 的延伸命名。 |
| 分頁排序 | 需確認前端是否需要額外 `sortBy` / `sortDirection`；若第一版不需要，固定排序即可。 |
