# ProductDevelopmentWorkspaceScreen API 後端流程與演算法

> Status: Proposal / Pending Engineer Review
> Screen: `ProductDevelopmentWorkspaceScreen`
> Proposal: `product_development_workspace_proposal.md`

## 1. 共用查詢流程

1. 建立單一 DB session。
2. 驗證 `productNo`、`productVersion`、`itemCategory`、`keyword`、`start`、`count`。
3. 在 SQLAlchemy query 層套用產品、關鍵字、類別、排序與分頁，避免先取回全部產品後由 Python 切片。
4. 只批次載入本頁產品版本需要的 product_spec、product_bom_spec、BOM、item_price、quotation 與 contract，避免 N+1 query。
5. API 回傳 enum code；前端負責多國語系文字與色彩。

## 2. 產品版本與 BOM 解析

1. 以 `product.no` 取得製成品主檔與版本。
2. 以 `product_spec.product_no + product_version` 取得產品版本的 BOM 關聯。
3. 以 `product_bom_spec.product_no + product_version` 取得物料 BOM 關聯。
4. 若提案確認需展開 `bom1`/`bom2`，再依已確認的 `bom12_no` 關聯展開；在工程師確認前不得自行假設兩者均為必要來源。
5. BOM 狀態判斷：沒有正式 BOM 為 `missing`；存在關聯但明細不完整為 `partial`；必要明細完整為 `complete`；來源關係無法判定為 `unknown`。
6. BOM 明細展開至 primitive type，保留 item no、名稱、類別、數量、單位、重量、損耗率與來源版本。

## 3. 成本試算

1. 先確認產品版本與 BOM 版本。
2. 對每個 BOM 明細取得正式料品成本來源；成本來源與 `est*`/`cost*` 欄位採工程師確認結果。
3. 依數量、重量及預估損耗率計算明細金額；數量/重量取至小數點第 2 位，單價取至小數點第 4 位，金額四捨五入取整數。
4. 依已確認的人工成本規則計算 `laborCost`；若規則或來源不足，回傳 `costStatusCode=missing_source`，不得假設人工成本為 0。
5. `estimatedCost` 為已成功計算的成本項目加總；任何必要來源缺漏時，同時回傳缺漏狀態與可辨識的明細 code。

## 4. 報價與合約關聯

1. 只查詢正式存在且可透過確認關聯取得的 `quotation` 與 `contract`。
2. 依工程師確認結果套用 `category`、`itemStyle`、`item_no` 與 `ref_no` 條件。
3. 缺少報價或合約時回傳 count=0 與 `quotation_missing`/`contract_missing`，不表示交易一定不成立，也不推測有效期限或核准狀態。

## 5. Readiness 判斷

1. `bomStatusCode=missing/partial` 優先產生 `bom_missing`。
2. BOM 完整但成本來源缺漏，產生 `cost_missing`。
3. 若成本完整但畫面要求商務關聯，依正式 quotation/contract 資料產生 `quotation_missing` 或 `contract_missing`。
4. 所有必要條件完成時回傳 `readinessStatusCode=ready`；條件不完整回傳 `incomplete`；正式來源不足以判定時回傳 `unknown`。
5. `ready` 僅代表本畫面定義的資料準備度，不代表客戶選樣、研發核准、量產核准或業務合約已完成。

## 6. 缺少正式 schema 的流程

目前資料庫文件未發現開發需求、打樣、客戶樣品確認及營養標示的正式資料表。這些流程在 V1 只作為畫面 roadmap 的 deferred 狀態，不建立虛構欄位、不用備註文字推導狀態。若工程師確認需要，應另開 DB extension proposal、SQL 與 API revision。

## 7. 效能與一致性

1. Dashboard summary 對完整篩選集合計算，items 才套用分頁。
2. Detail 與 cost-simulation 只查詢指定產品版本，且使用批次查詢。
3. 成本計算函式應抽取為可共用 service，未來報價、訂單毛利與 APS 需求計算可重用；但本階段只完成設計，不實作。
4. 同一 request 內不得重複建立 session 或重複查詢相同產品版本資料。

## 8. Engineer Review Gate

工程師確認 API 提案、成本來源、BOM 展開規則與 readiness 必要條件後，才可進行後端 API 實作；本文件目前不得直接作為實作完成的依據。

