# Transaction Item Master API Proposal

> Status: API Proposal / Pending Engineer Review  
> Screen: `ItemAndTransactionMasterScreen`  
> Route: `/items`  
> Scope: V1 read-only Core  
> Design basis: `AGENTS.md`, `docs/spec/database/index.md`, `docs/spec/api-proposal/item_center_proposal.md`, `docs/spec/api-proposal/transaction_item_master_static_preview.html`

## 1. 畫面定位

「品項與交易主資料中心」建議作為 `/items` 的下一版資訊架構，將既有料品主資料與商務交易主資料放在同一入口，但在畫面內清楚分成三個視圖：

| View | 主視角 | 本版邊界 |
|---|---|---|
| `CompanyMasterView` | 客戶／廠商主檔 | 檢視公司主檔、交易角色、聯絡與帳款摘要、交易品項數與合約摘要。 |
| `MaterialItemMasterView` | 料品品項 | 延續既有 `ItemCenterScreen`，檢視 `material`、`inproduct`、`product`、`goods` 的主檔、庫存訊號、BOM 關聯與維護建議。 |
| `TransactionItemMasterView` | 交易品項 | 檢視 `trans_items`、`trans_items2` 及其公司、料品與合約交易條件關聯。 |

交易品項不應只顯示交易品名與價格，必須同時呈現「客戶／廠商」與「對應料品品項」，才能支援採購、訂購、報價、合約與後續訂單流程的共同理解。

第一版不提供 POST、PUT、DELETE，不新增或修改客戶／廠商、料品、交易品項或合約。後端只回傳 enum code、數值與資料庫欄位；顯示文字、單位文字與多國語言由前端處理。

## 2. V1 API 清單

| API | Method | 用途 |
|---|---|---|
| `/api/v2/item-trade-master/dashboard` | GET | 查詢客戶／廠商摘要、交易品項清單、交易品項 KPI 與資料缺口摘要。 |
| `/api/v2/item-trade-master/companies/{company_no}/detail` | GET | 查詢單一客戶／廠商主檔、交易品項、合約與近期交易摘要。 |
| `/api/v2/item-trade-master/transaction-items/{transaction_item_no}/detail` | GET | 查詢單一交易品項的公司、料品、交易條件、合約來源與資料缺口。 |

`MaterialItemMasterView` 仍沿用既有 `GET /api/v2/items/dashboard` 與 `GET /api/v2/items/{item_no}/detail`，不在本提案重複定義。

## 3. 共用 Query Parameters / Header

| Parameter / Header | Type | Required | Description |
|---|---|---:|---|
| `keyword` | String | No | 公司 no、公司簡稱、交易品項 no、交易品項名稱、料品 no、料品名稱或合約 no 關鍵字。 |
| `companyNo` | String | No | 客戶／廠商 no，對應 `company.no`。 |
| `companyRoleCode` | String | No | 公司交易角色 code；第一版建議由後端依關聯資料推導 `customer`、`supplier`、`both`、`unknown`。 |
| `transactionItemSourceCode` | String | No | 交易品項來源 code；`trans_items` 或 `trans_items2`。 |
| `transactionCategory` | Integer | No | 交易品項樣式 code；依來源表分別使用 `trans_items.category` 或 `trans_items2.category`。 |
| `hasMaterialItem` | Boolean | No | 是否只顯示已關聯內部料品的交易品項。 |
| `hasContract` | Boolean | No | 是否只顯示已被合約引用的交易品項。 |
| `dataQualityCode` | String | No | 資料完整度 code；第一版支援 `ready`、`missing_company`、`missing_material_item`、`missing_contract_price`、`unknown`。 |
| `start` | Integer | No | 分頁起點，預設 0；負值視為 0。 |
| `count` | Integer | No | 回傳筆數，預設 50，最大 100。 |
| `x-timezone` | Header String | No | 前端顯示偏好的 IANA timezone；後端不改寫資料庫 UTC timestamp。 |

## 4. GET `/api/v2/item-trade-master/dashboard`

### 4.1 Success Response Data

```json
{
  "serverTimestamp": "Integer",
  "summary": {
    "companyCount": "Integer",
    "customerCount": "Integer",
    "supplierCount": "Integer",
    "transactionItemCount": "Integer",
    "linkedMaterialItemCount": "Integer",
    "contractLinkedTransactionItemCount": "Integer",
    "dataQualityIssueCount": "Integer"
  },
  "companies": [
    {
      "companyNo": "String",
      "companyDisplayName": "String",
      "companyName": "String",
      "businessNo": "String",
      "companyRoleCode": "String",
      "transactionItemCount": "Integer",
      "contractCount": "Integer",
      "contactName": "String",
      "contactPhone": "String",
      "paymentSummaryCode": "String"
    }
  ],
  "transactionItems": [
    {
      "transactionItemNo": "String",
      "transactionItemName": "String",
      "transactionItemSourceCode": "String",
      "transactionCategory": "Integer",
      "transactionAttribute": "Integer",
      "companyNo": "String",
      "companyDisplayName": "String",
      "companyRoleCode": "String",
      "materialItemNo": "String",
      "materialItemName": "String",
      "materialItemCategory": "Integer",
      "contractNo": "String",
      "contractCategory": "Integer",
      "contractType": "Integer",
      "tradeUnit": "Integer",
      "tradePrice": "Float",
      "shippingPrice": "Float",
      "unitConversion": "Float",
      "dataQualityCode": "String"
    }
  ],
  "dataQualityIssues": [
    {
      "issueId": "String",
      "targetTypeCode": "String",
      "targetNo": "String",
      "issueCode": "String",
      "riskLevelCode": "String"
    }
  ],
  "total": "Integer",
  "start": "Integer",
  "count": "Integer"
}
```

### 4.2 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `serverTimestamp` | Integer | API 回應建立時間，UTC timestamp。 | 系統時間 |
| `summary.companyCount` | Integer | 套用篩選後的公司主檔數。 | `company` |
| `summary.customerCount` | Integer | 被判定具有客戶角色的公司數。 | `company`、`contract.category=2`、訂購/銷售關聯 |
| `summary.supplierCount` | Integer | 被判定具有供應商角色的公司數。 | `company`、`contract.category=1`、採購關聯 |
| `summary.transactionItemCount` | Integer | 交易品項總數。 | `trans_items`、`trans_items2` |
| `summary.linkedMaterialItemCount` | Integer | 已關聯內部料品的交易品項數。 | `trans_items.item_no` |
| `summary.contractLinkedTransactionItemCount` | Integer | 已被合約引用的交易品項數。 | `contract.item_no` |
| `summary.dataQualityIssueCount` | Integer | 目前畫面需提示的資料缺口數。 | 後端資料完整度規則 |
| `companies[].companyNo` | String | 公司 no。 | `company.no` |
| `companies[].companyDisplayName` | String | 公司簡稱。 | `company.displayName` |
| `companies[].companyName` | String | 公司名稱。 | `company.name` |
| `companies[].businessNo` | String | 統一編號。 | `company.businessNo` |
| `companies[].companyRoleCode` | String | 公司交易角色 code。 | customer、supplier、both、unknown |
| `companies[].transactionItemCount` | Integer | 此公司關聯的交易品項數。 | `trans_items.company_no`、`trans_items2.company_no` |
| `companies[].contractCount` | Integer | 此公司關聯的合約數。 | `contract.item_ref_no` |
| `companies[].contactName` | String | 主要聯絡人。 | `company.contactName` |
| `companies[].contactPhone` | String | 主要聯絡電話；若來源為 JSON 或 longtext，後端只回傳畫面使用的一個摘要字串。 | `company.contactPhone` |
| `companies[].paymentSummaryCode` | String | 帳款摘要 code。 | payment_ready、missing_payment、unknown |
| `transactionItems[].transactionItemNo` | String | 交易品項 no。 | `trans_items.no`、`trans_items2.no` |
| `transactionItems[].transactionItemName` | String | 交易品項名稱。 | `trans_items.name`、`trans_items2.name` |
| `transactionItems[].transactionItemSourceCode` | String | 交易品項來源表 code。 | trans_items、trans_items2 |
| `transactionItems[].transactionCategory` | Integer | 交易品項樣式 code。 | `trans_items.category` 或 `trans_items2.category` |
| `transactionItems[].transactionAttribute` | Integer | 交易品項屬性 code。 | `trans_items.attribute` 或 `trans_items2.attribute` |
| `transactionItems[].companyNo` | String | 關聯公司 no。 | `trans_items.company_no`、`trans_items2.company_no`、fallback `contract.item_ref_no` |
| `transactionItems[].companyDisplayName` | String | 關聯公司簡稱。 | `trans_items.company_displayName`、`trans_items2.company_displayName`、fallback `company.displayName` |
| `transactionItems[].companyRoleCode` | String | 關聯公司在此交易品項上的角色 code。 | customer、supplier、both、unknown |
| `transactionItems[].materialItemNo` | String | 對應內部料品 no；`trans_items2` 無料品關聯時回傳空字串。 | `trans_items.item_no` |
| `transactionItems[].materialItemName` | String | 對應內部料品名稱。 | `trans_items.item_name` |
| `transactionItems[].materialItemCategory` | Integer | 對應內部料品類別 code；無料品時回傳 0。 | `contract.itemCategory` 或料品主檔 |
| `transactionItems[].contractNo` | String | 目前可明確關聯的合約 no；無合約時回傳空字串。 | `contract.no` |
| `transactionItems[].contractCategory` | Integer | 合約類別 code。 | 採購(1)、訂購(2) |
| `transactionItems[].contractType` | Integer | 合約樣式 code。 | `contract.type` |
| `transactionItems[].tradeUnit` | Integer | 交易單位 code。 | `contract.unit` |
| `transactionItems[].tradePrice` | Float | 交易單價，取至小數點第 4 位。 | `contract.price` |
| `transactionItems[].shippingPrice` | Float | 物流價格，取至小數點第 4 位。 | `contract.shippingPrice` |
| `transactionItems[].unitConversion` | Float | 交易單位與料品盤點單位的規格轉換。 | `contract.unitConversion` |
| `transactionItems[].dataQualityCode` | String | 此交易品項資料完整度 code。 | ready、missing_company、missing_material_item、missing_contract_price、unknown |
| `dataQualityIssues[].issueId` | String | 資料缺口識別值，供前端列表 key 使用；不是 workflow task id。 | 後端組合 |
| `dataQualityIssues[].targetTypeCode` | String | 缺口目標類型。 | company、transaction_item |
| `dataQualityIssues[].targetNo` | String | 缺口目標 no。 |  |
| `dataQualityIssues[].issueCode` | String | 缺口類型 code。 | missing_company、missing_material_item、missing_contract_price、missing_payment |
| `dataQualityIssues[].riskLevelCode` | String | 風險等級 code。 | normal、attention、high_risk |
| `total` | Integer | 套用篩選後的交易品項筆數。 |  |
| `start` | Integer | 本次分頁起點。 |  |
| `count` | Integer | 本次回傳筆數。 |  |

## 5. GET `/api/v2/item-trade-master/companies/{company_no}/detail`

### 5.1 Success Response Data

```json
{
  "serverTimestamp": "Integer",
  "company": {
    "companyNo": "String",
    "businessNo": "String",
    "companyDisplayName": "String",
    "companyName": "String",
    "address": "String",
    "phone": "String",
    "contactName": "String",
    "contactPhone": "String",
    "contactTitle": "String",
    "contactEmail": "String",
    "companyRoleCode": "String",
    "paymentSummaryCode": "String"
  },
  "transactionItems": [
    {
      "transactionItemNo": "String",
      "transactionItemName": "String",
      "transactionItemSourceCode": "String",
      "materialItemNo": "String",
      "materialItemName": "String",
      "contractNo": "String",
      "tradeUnit": "Integer",
      "tradePrice": "Float",
      "dataQualityCode": "String"
    }
  ],
  "contracts": [
    {
      "contractNo": "String",
      "contractDisplayName": "String",
      "contractCategory": "Integer",
      "contractType": "Integer",
      "effectiveDate": "Integer",
      "transactionItemNo": "String",
      "transactionItemName": "String"
    }
  ]
}
```

### 5.2 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `company.companyNo` | String | 公司 no。 | `company.no` |
| `company.businessNo` | String | 公司統編。 | `company.businessNo` |
| `company.companyDisplayName` | String | 公司簡稱。 | `company.displayName` |
| `company.companyName` | String | 公司名稱。 | `company.name` |
| `company.address` | String | 公司地址。 | `company.address` |
| `company.phone` | String | 公司電話。 | `company.phone` |
| `company.contactName` | String | 聯絡人姓名。 | `company.contactName` |
| `company.contactPhone` | String | 聯絡電話摘要。 | `company.contactPhone` |
| `company.contactTitle` | String | 聯絡人職稱。 | `company.contactTitle` |
| `company.contactEmail` | String | 聯絡人 email。 | `company.contactEmail` |
| `company.companyRoleCode` | String | 公司交易角色 code。 | customer、supplier、both、unknown |
| `company.paymentSummaryCode` | String | 帳款摘要 code。 | payment_ready、missing_payment、unknown |
| `transactionItems[]` | Array | 此公司關聯的交易品項摘要，欄位定義同 dashboard 子集合。 | `trans_items`、`trans_items2`、`contract` |
| `contracts[].contractNo` | String | 合約 no。 | `contract.no` |
| `contracts[].contractDisplayName` | String | 合約簡稱。 | `contract.displayName` |
| `contracts[].contractCategory` | Integer | 合約類別。 | `contract.category` |
| `contracts[].contractType` | Integer | 合約樣式。 | `contract.type` |
| `contracts[].effectiveDate` | Integer | 生效日期 UTC timestamp。 | `contract.date` |
| `contracts[].transactionItemNo` | String | 合約引用交易品項 no。 | `contract.item_no` |
| `contracts[].transactionItemName` | String | 合約引用交易品項名稱。 | `contract.item_name` |

## 6. GET `/api/v2/item-trade-master/transaction-items/{transaction_item_no}/detail`

### 6.1 Success Response Data

```json
{
  "serverTimestamp": "Integer",
  "transactionItem": {
    "transactionItemNo": "String",
    "transactionItemName": "String",
    "transactionItemSourceCode": "String",
    "transactionCategory": "Integer",
    "transactionAttribute": "Integer",
    "companyNo": "String",
    "companyDisplayName": "String",
    "companyRoleCode": "String",
    "materialItemNo": "String",
    "materialItemName": "String",
    "materialItemCategory": "Integer",
    "comment": "String",
    "creationTime": "Integer",
    "dataQualityCode": "String"
  },
  "tradeTerms": {
    "contractNo": "String",
    "contractDisplayName": "String",
    "contractCategory": "Integer",
    "contractType": "Integer",
    "tradeUnit": "Integer",
    "tradePrice": "Float",
    "shippingPrice": "Float",
    "unitConversion": "Float",
    "effectiveDate": "Integer"
  },
  "relatedMaterialItem": {
    "materialItemNo": "String",
    "materialItemName": "String",
    "materialItemCategory": "Integer",
    "unitWarehouse": "Integer"
  },
  "dataQualityIssues": [
    {
      "issueCode": "String",
      "riskLevelCode": "String"
    }
  ]
}
```

### 6.2 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `transactionItem.transactionItemNo` | String | 交易品項 no。 | `trans_items.no`、`trans_items2.no` |
| `transactionItem.transactionItemName` | String | 交易品項名稱。 | `trans_items.name`、`trans_items2.name` |
| `transactionItem.transactionItemSourceCode` | String | 來源表 code。 | trans_items、trans_items2 |
| `transactionItem.transactionCategory` | Integer | 交易品項樣式 code。 | `trans_items.category`、`trans_items2.category` |
| `transactionItem.transactionAttribute` | Integer | 交易品項屬性 code。 | `trans_items.attribute`、`trans_items2.attribute` |
| `transactionItem.companyNo` | String | 關聯公司 no。 | 交易品項表或合約 fallback |
| `transactionItem.companyDisplayName` | String | 關聯公司簡稱。 | 交易品項表或 `company.displayName` |
| `transactionItem.companyRoleCode` | String | 公司交易角色 code。 | customer、supplier、both、unknown |
| `transactionItem.materialItemNo` | String | 對應內部料品 no；無關聯時回傳空字串。 | `trans_items.item_no` |
| `transactionItem.materialItemName` | String | 對應內部料品名稱。 | `trans_items.item_name` |
| `transactionItem.materialItemCategory` | Integer | 對應內部料品類別 code；無關聯時回傳 0。 | `contract.itemCategory` 或料品主檔 |
| `transactionItem.comment` | String | 規格或備註。 | `trans_items.comment`、`trans_items2.comment` |
| `transactionItem.creationTime` | Integer | 資料建立時間 UTC timestamp；無資料時回傳 0。 | 交易品項表 |
| `transactionItem.dataQualityCode` | String | 資料完整度 code。 | ready、missing_company、missing_material_item、missing_contract_price、unknown |
| `tradeTerms.contractNo` | String | 合約 no；無合約時回傳空字串。 | `contract.no` |
| `tradeTerms.contractDisplayName` | String | 合約簡稱。 | `contract.displayName` |
| `tradeTerms.contractCategory` | Integer | 合約類別。 | `contract.category` |
| `tradeTerms.contractType` | Integer | 合約樣式。 | `contract.type` |
| `tradeTerms.tradeUnit` | Integer | 交易單位 code。 | `contract.unit` |
| `tradeTerms.tradePrice` | Float | 交易單價，取至小數點第 4 位。 | `contract.price` |
| `tradeTerms.shippingPrice` | Float | 物流價格，取至小數點第 4 位。 | `contract.shippingPrice` |
| `tradeTerms.unitConversion` | Float | 規格轉換。 | `contract.unitConversion` |
| `tradeTerms.effectiveDate` | Integer | 合約生效日期 UTC timestamp。 | `contract.date` |
| `relatedMaterialItem.materialItemNo` | String | 內部料品 no。 | 料品主檔 |
| `relatedMaterialItem.materialItemName` | String | 內部料品名稱。 | 料品主檔 |
| `relatedMaterialItem.materialItemCategory` | Integer | 內部料品類別 code。 | 料品主檔 |
| `relatedMaterialItem.unitWarehouse` | Integer | 料品盤點或倉庫單位 code。 | 料品主檔 |
| `dataQualityIssues[].issueCode` | String | 資料缺口類型 code。 | missing_company、missing_material_item、missing_contract_price |
| `dataQualityIssues[].riskLevelCode` | String | 風險等級 code。 | normal、attention、high_risk |

## 7. Enum 建議

| Enum | Values |
|---|---|
| `companyRoleCode` | `customer`、`supplier`、`both`、`unknown` |
| `transactionItemSourceCode` | `trans_items`、`trans_items2` |
| `dataQualityCode` | `ready`、`missing_company`、`missing_material_item`、`missing_contract_price`、`unknown` |
| `issueCode` | `missing_company`、`missing_material_item`、`missing_contract_price`、`missing_payment` |
| `paymentSummaryCode` | `payment_ready`、`missing_payment`、`unknown` |

## 8. Database Tables Used

| Table | Purpose |
|---|---|
| `company` | 客戶／廠商主檔、聯絡資訊與帳款資料關聯。 |
| `trans_items` | 貨品、材料、產品類交易品項，包含公司與內部料品關聯。 |
| `trans_items2` | 耗品、設備、工程、其他、雜項類交易品項，包含公司關聯。 |
| `contract` | 合約與交易條件，提供交易單位、單價、物流價格、規格轉換與交易品項引用。 |
| `material` | 原料、物料、膠捲主檔；用於交易品項對應內部料品。 |
| `inproduct` | 在製品主檔；用於交易品項對應內部料品。 |
| `product` | 製成品主檔；用於交易品項對應內部料品。 |
| `goods` | 貨品主檔；若合約或交易品項指向貨品時作為補充。 |
| `payment` | 公司帳款資料摘要。 |

## 9. 備註

1. `trans_items.company_no` 與 `trans_items2.company_no` 文件描述為「客戶資料no」，但實際畫面應以「客戶／廠商」通稱呈現，角色由後端依合約類別、採購/訂購關聯或其他可確認來源推導。
2. `trans_items2` 第一版沒有內部料品欄位，因此 `materialItemNo`、`materialItemName` 可為空字串；前端應以資料缺口或不適用狀態呈現，不應自行推測料品。
3. `tradePrice` 與 `shippingPrice` 來源為 `contract`，若同一交易品項有多筆合約，第一版可優先回傳目前生效或最新生效日期的合約摘要；若無法唯一判定，應回傳空合約摘要並以 `dataQualityCode=missing_contract_price` 或 `unknown` 提示。
4. 本提案不取代 `ItemCenterScreen` 既有料品 API；料品主資料仍由 `item_center_proposal.md` 維護。
5. `dataQualityIssues[]` 是 read-only 資料缺口提示，不代表 workflow task，也不建立待辦或部門轉交。
