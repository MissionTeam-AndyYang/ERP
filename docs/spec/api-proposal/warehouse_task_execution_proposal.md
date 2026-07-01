# Warehouse Task Execution API Proposal

> Status: Deferred to V2 / Not in Warehouse V1 read-only scope
> Target UI Preview: `docs/spec/api-proposal/warehouse_task_execution_static_preview.html`
> Flow / Algorithm: `docs/spec/api-proposal/warehouse_task_execution_flow_algorithm.md`
> Related Workbench API: `docs/spec/api-proposal/warehouse_task_workbench_proposal.md`
> Purpose: 承接 `WarehouseTaskWorkbenchScreen` 與 `WarehouseTaskDetailPanel`，提供「倉庫任務執行工作區」所需 API。第一版目標是讓操作員在執行入庫、出庫、移倉、品檢或出貨前，能看到完整任務上下文、批號可用性、數量限制與 validation 結果；實際寫入 mutation API 需待工程師確認交易流程後再實作。

## Planning Confirmation

先前倉庫任務第一版規劃為 read-only，此規劃仍然成立。本文所稱 `WarehouseTaskExecutionScreen` 是下一步預計設計的畫面，但第一階段定位為「任務執行前確認與驗證」，不是直接提交庫存異動的正式執行功能。

2026-07-01 更新：第一版前端畫面規劃確認為 read-only，暫不實作會使用到 POST / PUT API 的畫面。因此 `WarehouseTaskExecutionScreen` 延至下一版再進行設計與實作；Warehouse V1 後續 API 設計應先改以純 GET 的分析、查詢、追蹤畫面為主。本文保留作為下一版任務執行討論基礎，不再作為當前下一步實作目標。

第一階段 API 邊界如下：

1. `GET /api/v2/warehouse/task-execution/tasks/{taskId}`：read-only，僅取得任務執行前上下文。
2. `POST /api/v2/warehouse/task-execution/tasks/{taskId}/actions/validate`：non-mutating validation，不寫入資料庫，只回傳驗證結果與預估影響。
3. `POST /api/v2/warehouse/task-execution/tasks/{taskId}/actions/commit`：僅保留為後續提案，屬於 `Mutation Deferred`，需待工程師確認交易規則、資料表寫入順序與 rollback 策略後才可進入正式文件與實作。

因此，`WarehouseTaskExecutionScreen` 僅保留為下一版命名基準；目前 Warehouse V1 不再將此畫面視為下一步實作目標。若團隊未來希望命名更保守，可在 V2 review 時討論是否改名為 `WarehouseTaskExecutionPreparationScreen`。

## Screen Intent

`WarehouseTaskExecutionScreen` 回答以下問題：

1. 此任務目前是否可執行？
2. 執行時需要選哪個批號、倉位或板位？
3. 本次處理數量是否超過剩餘數量、可用數量、預留數量或品檢限制？
4. 執行後會影響哪些資料表與 workflow timeline？
5. 若無法執行，應由哪個部門或哪個原因回到 Task Workbench 處理？

原先提案曾建議先實作 read-only context 與 validation API；依 2026-07-01 最新規劃，validation 與 commit 相關 API 均延至下一版 review，不進入 Warehouse V1 實作。

## API Summary

| URL | Method | Description | Status | Review Note |
| --- | --- | --- | --- | --- |
| `/api/v2/warehouse/task-execution/tasks/{taskId}` | GET | 取得任務執行前上下文 | Proposal / Pending Engineer Review | 供執行工作區載入任務、建議 action、可用批號、限制與預設輸入值。 |
| `/api/v2/warehouse/task-execution/tasks/{taskId}/actions/validate` | POST | 驗證本次任務執行輸入 | Proposal / Pending Engineer Review | 不寫入資料庫，只回傳 validation 結果、預估影響與可否提交。 |
| `/api/v2/warehouse/task-execution/tasks/{taskId}/actions/commit` | POST | 提交任務執行結果 | Proposal / Pending Engineer Review / Mutation Deferred | 會寫入庫存、板位、任務狀態與 workflow event；需工程師確認交易規則後才能實作。 |

## Numeric Format Rules

| Numeric Meaning | Format |
| --- | --- |
| 單價 | 四捨五入取至小數點第 4 位 |
| 重量或數量 | 四捨五入取至小數點第 2 位 |
| 金額 | 四捨五入取整數 |

## GET /api/v2/warehouse/task-execution/tasks/{taskId}

### Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v2/warehouse/task-execution/tasks/{taskId}` | GET | 取得任務執行前上下文 |

### Request Header

| Header | Description |
| --- | --- |
| `x-auth-token` | 存取金鑰 |
| `x-timezone` | 前端顯示時區；未提供時以 UTC 回傳 |

### Path Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `taskId` | String | YES | workflow 任務識別碼 |

### Query Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `date` | Integer | NO | 查詢基準時間，UTC timestamp；未提供時以伺服器目前時間計算 |

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "timezone": "String",
    "task": {
      "taskId": "String",
      "taskType": "Integer",
      "taskStatus": "Integer",
      "refCategory": "Integer",
      "refNo": "String",
      "refSubNo": "String",
      "warehouseNo": "String",
      "warehouseName": "String",
      "itemCategory": "Integer",
      "itemNo": "String",
      "itemName": "String",
      "batchNo": "String",
      "unit": "Integer",
      "expectedQuantity": "Float",
      "processedQuantity": "Float",
      "remainingQuantity": "Float",
      "ownerDepartment": "Integer",
      "dueTimestamp": "Integer",
      "blockReasonCode": "String",
      "blockReason": "String"
    },
    "execution": {
      "actionCode": "String",
      "allowed": "Boolean",
      "blockedReasons": ["String"],
      "defaultQuantity": "Float",
      "requiresBatch": "Boolean",
      "requiresPalletPlan": "Boolean",
      "requiresQualityDecision": "Boolean"
    },
    "quantityLimits": {
      "remainingQuantity": "Float",
      "availableQuantity": "Float",
      "reservedQuantity": "Float",
      "qualityHoldQuantity": "Float",
      "maxExecutableQuantity": "Float"
    },
    "candidateLots": [
      {
        "lotKey": "String",
        "warehouseNo": "String",
        "warehouseName": "String",
        "itemNo": "String",
        "itemName": "String",
        "batchNo": "String",
        "unit": "Integer",
        "currentQuantity": "Float",
        "availableQuantity": "Float",
        "reservedQuantity": "Float",
        "qualityHoldQuantity": "Float",
        "validDate": "Integer",
        "riskTypes": ["String"],
        "selectable": "Boolean",
        "disabledReasons": ["String"]
      }
    ],
    "palletContext": {
      "currentPalletCount": "Float",
      "suggestedPalletCount": "Float",
      "availablePallets": "Float"
    },
    "sourceRefs": [
      {
        "refCategory": "Integer",
        "refNo": "String",
        "refSubNo": "String",
        "descriptionCode": "String"
      }
    ],
    "timeline": [
      {
        "eventCode": "String",
        "eventTimestamp": "Integer",
        "department": "Integer",
        "status": "Integer",
        "note": "String"
      }
    ]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
| --- | --- | --- | --- |
| `payload.task.*` | Object | 任務主資料，欄位語意與 `GET /api/v2/warehouse/task-workbench/tasks/{taskId}` 的 `payload.task` 與 `payload.quantity` 一致 |  |
| `payload.execution.actionCode` | String | 本任務建議執行動作代碼；來源為 taskType 與 taskStatus 判斷 |  |
| `payload.execution.allowed` | Boolean | 是否可進入輸入與提交流程；若為 false，前端只能顯示原因與返回工作台 |  |
| `payload.execution.blockedReasons[]` | String | 無法執行原因 code，例如 `TASK_BLOCKED`、`TASK_DONE`、`NO_AVAILABLE_LOT`、`QUALITY_HOLD` |  |
| `payload.execution.defaultQuantity` | Float | 預設本次處理數量，通常為 `min(remainingQuantity, maxExecutableQuantity)` |  |
| `payload.execution.requiresBatch` | Boolean | 此任務是否必須指定批號 |  |
| `payload.execution.requiresPalletPlan` | Boolean | 此任務是否需要板位/板數規劃 |  |
| `payload.execution.requiresQualityDecision` | Boolean | 此任務是否需要品檢判定 |  |
| `payload.quantityLimits.maxExecutableQuantity` | Float | 依任務類型、可用量與品檢限制計算的最大可執行數量 |  |
| `payload.candidateLots[]` | Array | 可供本次任務使用或檢視的批號候選清單 |  |
| `payload.candidateLots[].selectable` | Boolean | 此批號是否可被本次執行選取 |  |
| `payload.candidateLots[].disabledReasons[]` | Array | 批號不可選原因 code |  |
| `payload.palletContext` | Object | 板位相關上下文；若任務不需板位規劃，可回傳 0 值 |  |
| `payload.sourceRefs[]` | Array | 主任務來源集合，第一版通常為一筆 |  |
| `payload.timeline[]` | Array | 既有任務事件歷史；來源為 `workflow_task_event` |  |

## POST /api/v2/warehouse/task-execution/tasks/{taskId}/actions/validate

### Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v2/warehouse/task-execution/tasks/{taskId}/actions/validate` | POST | 驗證本次任務執行輸入 |

### Request Body

```json
{
  "actionCode": "String",
  "batchNo": "String",
  "quantity": "Float",
  "warehouseNo": "String",
  "targetWarehouseNo": "String",
  "palletCount": "Float",
  "qualityDecision": "String",
  "reasonCode": "String",
  "note": "String"
}
```

### Request Body Field Description

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `actionCode` | String | YES | 本次執行動作代碼；需與 context API 回傳的 actionCode 一致或為工程師允許的 action |
| `batchNo` | String | 條件式 | 出庫、移倉、出貨等需指定批號的任務必填 |
| `quantity` | Float | YES | 本次處理數量；需大於 0 且不得超過可執行上限 |
| `warehouseNo` | String | 條件式 | 執行來源倉或入庫倉；若 task 已指定倉儲，可由 task 預設 |
| `targetWarehouseNo` | String | 條件式 | 移倉任務目的倉 |
| `palletCount` | Float | NO | 本次使用或異動板數 |
| `qualityDecision` | String | 條件式 | 品檢任務判定，例如 `release`、`hold`、`reject` |
| `reasonCode` | String | NO | 阻塞、調整、拒收或取消原因 code |
| `note` | String | NO | 人工備註 |

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "valid": "Boolean",
    "validationErrors": [
      {
        "field": "String",
        "reasonCode": "String",
        "messageParams": {}
      }
    ],
    "warnings": [
      {
        "reasonCode": "String",
        "messageParams": {}
      }
    ],
    "preview": {
      "processedQuantityAfter": "Float",
      "remainingQuantityAfter": "Float",
      "taskStatusAfter": "Integer",
      "eventCode": "String",
      "inventoryEffect": {
        "category": "Integer",
        "quantity": "Float",
        "warehouseNo": "String",
        "targetWarehouseNo": "String",
        "batchNo": "String"
      },
      "palletEffect": {
        "palletCount": "Float",
        "sourceWarehouseNo": "String",
        "targetWarehouseNo": "String"
      }
    }
  }
}
```

### Processing Flow

1. 讀取 task context。
2. 驗證任務狀態是否可執行。
3. 驗證 actionCode 與 taskType 是否相容。
4. 驗證批號、倉儲、數量、品檢判定與板位欄位。
5. 回傳 validationErrors、warnings 與 preview，不寫入任何資料表。

## POST /api/v2/warehouse/task-execution/tasks/{taskId}/actions/commit

### Status

`Mutation Deferred / Pending Engineer Review`

此 API 會影響庫存、板位、任務狀態與 workflow timeline。正式實作前需工程師確認：

1. 各 actionCode 對應的資料表寫入規則。
2. `inventory_record.category/refCategory/ref_no/ref_sub_no` 寫入規則。
3. `warehouse_pallet_movement` 寫入或拆分規則。
4. `workflow_task_state.processedQuantity/taskStatus/updateTime` 更新規則。
5. `workflow_task_event.eventCode/eventTimestamp/fromStatus/toStatus` 寫入規則。

### Request / Response

建議沿用 validate API 的 request body；commit 成功後回傳更新後的 task context 與新增的 workflow event。正式欄位待工程師確認後再進入 `docs/spec/api/`。

## Database Tables Used

| Table | Purpose |
| --- | --- |
| `workflow_task_state` | 任務目前狀態、主任務來源、數量與負責部門 |
| `workflow_task_event` | 任務事件 timeline；commit API 需新增事件 |
| `inventory_item_month_statistic` | 庫存快照主計算基準 |
| `inventory_delta` | 庫存快照補算 |
| `inventory_record` | 實際庫存異動紀錄；commit API 可能寫入 |
| `warehouse_inventory_reservation` | 預留數量限制與釋放參考 |
| `warehouse_quality_hold` | 品檢保留限制與品檢決策參考 |
| `warehouse_pallet_movement` | 板位異動紀錄；commit API 可能寫入 |
| `batch_number` | 批號來源、效期與料品 context |
| `ship_wh_alias` | 倉儲名稱 |

## Frontend Interaction Notes

| UI Action | API Usage |
| --- | --- |
| 從 Task Workbench 點選「處理」 | 呼叫 `GET /api/v2/warehouse/task-execution/tasks/{taskId}` |
| 使用者選擇批號或輸入數量 | 呼叫 validate API 更新 preview 與錯誤提示 |
| 使用者按下確認送出 | 待 commit API review 通過後呼叫 commit API |
| validate 回傳不可提交 | 前端停留在畫面並顯示欄位錯誤與 blocked reason code |

## Engineer Review Questions

| 項目 | 需確認原因 | 工程師回覆 |
| --- | --- | --- |
| 第一版是否先實作 GET context + validate，commit 後置 | 避免 mutation 寫入規則未確認前影響庫存資料。 | Pending |
| 各 taskType 對應 actionCode 是否足夠 | 影響前端按鈕與後端演算法分支。 | Pending |
| `inventory_record` 與 `warehouse_pallet_movement` 寫入是否需同 transaction | 影響資料一致性與 rollback 策略。 | Pending |
| 品檢判定是否由此畫面處理或交由 Quality 模組 | 影響 `qualityDecision` 欄位是否保留。 | Pending |
