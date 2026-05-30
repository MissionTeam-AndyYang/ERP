## 0. 前置作業（必須先執行）

請先在本地 repository 執行以下操作：

1. 切換至 main branch
   git checkout main

2. 更新最新檔案
   git pull origin main

3. 確認以下檔案為最新版本：
   - docs/spec/database/index.md
   - docs/database/EWDB_20260526.sql

---

## 若 pull 失敗

需停止文件生成並回報錯誤，不得使用舊版本繼續分析。

## 1. 分析依據
請針對 docs/spec/database/index.md 中標示為「Need Review」的欄位進行重新檢查。

分析依據：
1. docs/spec/database/index.md（最新版本）
2. docs/database/EWDB_20260526.sql

## 2. 檢查規則
- 若已新增欄位說明、Enum 定義、Foreign Key 關聯或其他足以明確判斷欄位用途的資訊，請將狀態由「Need Review」更新為「OK」。
- 若仍無法明確判定欄位用途，維持「Need Review」。
- 不得移除既有欄位說明。
- 不得重新產生整份文件。
- 僅更新 Need Review 欄位的「狀態」與必要的「Review Note」。

## 3. 輸出

1. 仍維持 Need Review 的欄位清單
2. 更新 docs/spec/database/index.md
