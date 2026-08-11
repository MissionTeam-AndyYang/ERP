# RDCostWorkspaceScreen API 後端流程與演算法

> Status: Proposal / Pending Engineer Review  
> Screen: `RDCostWorkspaceScreen`  
> Proposal: `rd_cost_proposal.md`

## 1. 共用查詢流程

1. 讀取 `AGENTS.md`、`rd_cost_proposal.md`、資料庫文件與 `/rd` 前端畫面後建立單一 DB session。
2. 驗證 `date`、`productNo`、`productVersion`、`bomNo`、`readinessStatusCode`、`costStatusCode`、`keyword`、`start`、`count`。
3. 在 SQLAlchemy query 層完成產品/BOM 條件、排序與分頁；不得先取回全部資料後由 Python 切片。
4. Dashboard 先取得符合條件的產品版本集合，再批次查詢 BOM、BOM item、成本來源、quotation、contract，避免 N+1 query。
5. API 只回傳 enum code、數值與資料庫欄位，不回傳前端顯示用繁中文字串；enum 多國語系由前端處理。

## 2. 產品與 BOM 版本解析

1. 第一版 row identity 先以 `productNo + productVersion` 表示，直到開發案/打樣/送樣資料表正式確認。
2. 以 `product.no` 取得產品主檔；產品版本優先取 query `productVersion`，未提供時由 `product.version` 或 `product_spec.product_version` 可判定的最高版本取得。
3. 以 `product_spec.product_no + product_version` 取得產品版本關聯的 `bom_no`、`bom_version`、數量、單位、重量與損耗。
4. 以 `bom.no + bom.version` 取得商品配方主檔；若 `product_spec.bom_version` 缺漏，需依工程師確認規則選定版本，不得自行改用最新版本。
5. 以 `bom_item.bom_no` 取得商品配方直接原料明細。若需要完整產品 BOM 樹，需另行設計 tree API，不在本 API 隱含展開 `CCBOMTree`。

## 3. 成本明細計算

1. 先建立 BOM 明細清單：原料明細來自 `bom_item`；物料/包材/膠捲是否納入第一版，需工程師確認 `product_bom_spec` 的正式使用規則。
2. 對每一成本明細取得單價來源：
   - 商品配方或樣品成本候選來源：`sample_price`。
   - 料品正式成本候選來源：`item_price`。
   - 人工成本候選來源：`labor_wage`。
   - 物流/倉儲成本候選來源：`ship_wh_quotation`、`ship_wh_contract`。
3. 單價取至小數點第 4 位；重量與數量取至小數點第 2 位；金額四捨五入取整數。
4. 必要來源缺漏時，不推測單價；該 line 的 `costSourceCode` 回傳 `manual_source_missing` 或 `unknown`，並將 `costStatusCode` 設為 `missing_source`。
5. `estimatedUnitCost` 只加總已可計算的 cost lines；若任一必要來源缺漏，仍需以 readiness 回傳缺漏 code，避免前端誤認成本完整。

## 4. 報價與合約關聯

1. 以產品 no、BOM no 或工程師確認的正式關聯條件查詢 `quotation` 與 `contract`。
2. 在工程師確認有效性規則前，不推測報價/合約仍有效或已核准。
3. `quotationCount` 與 `contractCount` 只代表可由正式關聯取得資料筆數。
4. `targetPrice`、`minimumQuote`、`suggestedQuote` 與 `targetMarginRate` 的正式來源與演算法需工程師確認；未確認前不得進行後端實作。

## 5. Readiness 判斷

1. 找不到產品版本或 BOM 關聯：`bomStatusCode=missing`、`readinessRiskCode=bom_missing`。
2. BOM 存在但必要明細缺漏：`bomStatusCode=partial`、`readinessRiskCode=bom_missing`。
3. BOM 完整但成本必要來源缺漏：`costStatusCode=missing_source`、`readinessRiskCode=cost_missing`。
4. 成本完整但找不到報價或合約資料：依畫面所需回傳 `quotation_missing` 或 `contract_missing`；此狀態不代表交易一定不能成立。
5. 成本與報價資料完整但毛利低於目標：`readinessRiskCode=margin_low`。
6. 所有必要條件完成時回傳 `readinessStatusCode=ready`；條件不完整回傳 `incomplete`；正式來源不足以判定時回傳 `unknown`。

## 6. Deferred Schema

目前資料庫文件未確認以下正式資料表，第一版不得推測：

- 開發需求。
- 打樣/試作。
- 送樣與客戶確認樣品。
- 營養標示。
- 研發主管審核或產品開發 stage。

若需要讓 `/rd` 畫面完整呈現「開發案」生命週期，需另行建立 DB extension proposal、SQL 與 API revision。

## 7. 效能與可維護性

1. 成本計算邏輯應封裝為可重用 service，未來 Orders 毛利、Quotation 建議報價、APS 可行性試算可共用。
2. 同一 request 內不得重複查詢相同產品版本、BOM 或 item price。
3. Dashboard summary 對完整篩選集合計算，items 才套用分頁。
4. Detail 與 simulation 共用成本計算函式；simulation 只是 response 欄位較窄，不應複製第二套演算法。
5. 後端實作前需先將工程師確認後的 API 提案整合至正式 API 文件。

## 8. Engineer Review Gate

工程師確認 `rd_cost_proposal.md` 中的 API 路徑、產品版本 identity、成本來源、報價/毛利演算法與 deferred schema 邊界後，才可進行後端 API 實作。
