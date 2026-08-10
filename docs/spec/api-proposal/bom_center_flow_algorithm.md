# BOMCenterScreen API 後端流程與演算法

> Status: Proposal / Pending Engineer Review  
> Screen: `BOMCenterScreen`  
> Proposal: `bom_center_proposal.md`

## 1. 共用處理原則

1. 讀取 `AGENTS.md`、資料庫 schema 與提案文件後，建立單一 DB session。
2. 驗證 `keyword`、`bomNo`、`versionStateCode`、`start`、`count` 與 `x-timezone`。
3. 在 SQLAlchemy query 層完成篩選、排序、計數與分頁；不得先取回全部版本後由 Python 切片。
4. dashboard 先取得符合條件的 BOM 版本集合，再以批次查詢取得 `bom_item` 明細數與 `product_spec` 關聯數，避免 N+1 query。
5. API 只回傳 enum code、數值與資料庫欄位，不回傳前端顯示用繁中文字串；enum 多國語系由前端處理。

## 2. BOM Center Dashboard

1. 以 `bom.no`、`bom.displayName` 與關聯 `bom_item` / `product_spec` 套用 `keyword`。
2. 若有 `bomNo`，只查詢指定 `bom.no`；`version` 僅供 detail API 指定版本；若有 `versionStateCode`，在版本狀態計算後套用篩選。
3. 以 `bom.no`、`bom.version` 穩定排序，分頁查詢版本資料。
4. `bomCount` 以符合條件的不重複 `bom.no` 計算；`versionCount` 以符合條件的版本列計算。
5. 使用同一查詢日判斷每一版本狀態；`bom.date` 已是 UTC timestamp，後端以 UTC 日期／時間判斷，不依 `x-timezone` 改寫來源值：
   - `future`：`bom.date` 晚於查詢日。
   - `effective`：`bom.date` 不晚於查詢日，且是同一 `bom.no` 中不晚於查詢日的最高版本。
   - `historical`：`bom.date` 不晚於查詢日，但已被較新有效版本取代。
   - `unknown`：日期為空或無法依現有 schema 判斷。
6. 以 `bom_item.bom_no` 批次計算 `itemCount`。
7. 以 `product_spec.bom_no` 批次計算 `linkedProductCount`；V1 不使用 `product_spec.bom_version` 作為過濾條件，未確認的其他關聯不得自行補入。
8. `dateTimestamp` 直接回傳資料庫保存的 UTC timestamp；資料庫日期為空時回傳 0。前端依使用者時區轉換為畫面日期。
9. `weight` 取至小數點第 2 位；`unit`、版本與計數維持 Integer；不得把空值改成顯示文字。

## 3. BOM Detail

1. 以 path parameter `bom_no` 驗證 BOM 是否存在；不存在時使用既有 not-found response contract。
2. 若未指定 `version`，使用目前查詢日的 `effective` 版本；若指定 `version`，只取該 BOM 的指定版本。若未指定版本且沒有可判定的有效版本，使用版本號最高且日期非空的版本，並標記 `unknown`。
3. 以 `bom.no + bom.version` 取得 BOM header。
4. 以 `bom_item.bom_no` 取得直接明細，依資料庫主鍵或穩定 item no 排序；此 API 不遞迴展開 `bom1`、`bom2`，除非工程師確認其為 BOM Center V1 的正式來源。
5. 以 `product_spec.bom_no` 取得關聯產品版本，依 product no、product version 排序；V1 不以 `product_spec.bom_version` 篩選。
6. `versions` 取得同一 `bom.no` 的全部版本，依版本號由新到舊排列。
7. 所有 enum 以數字或 code 回傳；前端再將 unit、itemType、level 轉換為多國語系文字。

## 4. 空值與例外

- 無 `displayName`、`item_name` 或 `comment` 時回傳空字串。
- 無日期時 `dateTimestamp=0`，並由 `versionStateCode=unknown` 表達不可判定。
- 無 BOM 明細或產品關聯時回傳空陣列，不以例外代替合法空集合。
- 查詢參數格式錯誤沿用既有 API error response，不執行寬鬆字串轉換。
- SQL 查詢例外不得回傳部分成功資料；沿用既有 server error response。

## 5. 效能與可維護性

1. 以 SQL `COUNT`、`GROUP BY`、`OFFSET/LIMIT` 完成統計與分頁。
2. 以批次聚合查詢取得明細數與產品關聯數，避免每張 BOM 再查一次。
3. dashboard 與 detail 共用版本狀態判斷函式；未來若 `/rd` 需要讀取 BOM 狀態，應抽取成共用 service，而不是複製查詢邏輯。
4. 不在 API 層計算成本、報價或合約狀態；這些責任保留給研發成本畫面及其 API。
5. 後端實作前需由工程師確認正式欄位、index 與 `bom1`/`bom2` 是否納入，確認後才更新 formal API 文件與程式碼。
