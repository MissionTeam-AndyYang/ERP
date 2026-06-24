# API Proposal 文件集中管理規範

## 目的

`docs/spec/api-proposal/` 用於集中管理尚未進入正式實作或尚待工程師 review 的 API 設計文件。後續若進行任何新的 API 設計，均須先在本目錄建立完整提案，再由工程師確認後進入 `docs/spec/api/` 正式文件與後端實作。

## 每個新 API 設計必備文件

| 文件類型 | 命名建議 | 用途 |
| --- | --- | --- |
| API 提案文件 | `{module}_{screen_or_feature}_proposal.md` | 描述畫面目的、API endpoint、request/response dataset、欄位語意、資料表來源與 review 狀態。 |
| 後端流程與演算法文件 | `{module}_{screen_or_feature}_flow_algorithm.md` | 描述後端查詢流程、資料表 join/aggregation、排序篩選、例外處理與不得推測的限制。 |
| 前端靜態預覽頁 | `{module}_{screen_or_feature}_static_preview.html` | 以靜態 HTML 呈現畫面操作情境，供工程師評估 API 是否符合實際使用流程。 |

## 狀態規範

| Status | 說明 |
| --- | --- |
| Proposal / Pending Engineer Review | 初版提案，尚待工程師確認。 |
| Engineer Review In Progress | 工程師正在提問或檢視。 |
| Engineer Confirmed / Ready for Implementation | 工程師已確認可進入正式文件或程式實作。 |
| Implemented / Pending Runtime Review | 已實作，待有 DB 環境執行結果確認。 |

## 文件原則

1. API 文件中的業務名詞須優先與 `docs/spec/database/index.md`、正式 API 文件與 UX/UI 畫面用語保持一致。
2. 尚未確認或不存在的 API 不得寫入 `docs/spec/api/` 正式目錄；須先留在本目錄作為 proposal。
3. 若涉及 enum 顯示文字，API 僅回傳 code，前端負責多國語言轉換。
4. 若涉及金額、數量、單價，須明確標示數字格式規則。
5. 若工程師提出問題，應在 proposal 中新增「工程師提問 / 建議」區塊，理解後再更新欄位與流程。
