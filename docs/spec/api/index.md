# ERP 2.0 Restserver API Development Index

> Baseline code: `restserver/package/restserver` on `main`  
> Database baseline: `docs/database/EWDB_20260526.sql`  
> Database field reference: `docs/spec/database/index.md`  
> Runtime baseline: `docs/backend/runtime-verification/RESTSERVER_RUNTIME_EWDB_20260526_20260527.json`  
> Generated: 2026-05-28

## Purpose

This document is the shared API development reference for Codex and the backend engineer. It documents what is confirmed from the current `restserver` source code and explicitly marks items that still require engineer confirmation before frontend/API contract integration.

## Baseline Status

| Item | Confirmed Value | Status |
| --- | --- | --- |
| Framework | Flask application factory | Confirmed from `app.py` |
| API prefix | `/api/v1` | Confirmed from `api/common.py` |
| Registered blueprints | 26 | Confirmed by runtime verification |
| Flask URL rules | 70 | Confirmed by runtime verification; includes Flask/app-level rules |
| Documented active API routes | 69 | Confirmed from active `@blueprint.route(...)` decorators in `*_uri.py` |
| ORM tables | 79 | Confirmed by runtime verification |
| DB tables | 79 | Confirmed by runtime verification |
| Response envelope | `{ code, message, payload }` | Confirmed from `CAPIBase.run()` |
| Baseline code review | Pass for runtime/schema/app registration scope | Confirmed from runtime review |

## Coding Style Confirmed From Restserver

| Concern | Current Pattern | Status |
| --- | --- | --- |
| App composition | `create_app()` imports and registers Blueprint objects | Confirmed |
| Route files | `restserver/package/restserver/api/*_uri.py` define Flask routes | Confirmed |
| Business executors | Paired `restserver/package/restserver/api/*.py` files contain executor classes | Confirmed |
| Shared runner | URI classes subclass `CAPIBase` and call `.run()` | Confirmed |
| Executor return contract | `(http_status, code, message, payload_dict)` | Confirmed |
| GET inputs | `request.args.get(...)` | Confirmed |
| POST/PUT inputs | JSON body via `request.get_json()`; content type must be `application/json` or `multipart/form-data` | Confirmed |
| DELETE inputs | mixed by endpoint; some use query params and some use JSON/body conventions | Need Engineer Confirmation |
| Auth token behavior | `X_AUTH_TOKEN` required by `CAPIBase` unless URI overrides validation; behavior also depends on `TOKEN_ENABLED` | Need Engineer Confirmation |
| Timezone header | `X_TIMEZONE` is passed into executor methods as `str_timezone` | Confirmed |

## Standard Response Contract

All non-customized `CAPIBase` responses are wrapped as:

```json
{
  "code": 0,
  "message": "success",
  "payload": {}
}
```

Need Engineer Confirmation:

- Confirm whether all frontend-facing APIs should always use this envelope, including future dashboard aggregation APIs.
- Confirm canonical success/error `code` values from `package.common.common.EErrorCode` that frontend should handle.
- Confirm whether `message` should remain English strings or move toward i18n-ready message codes.

## Request Convention

| Method | Current Source Pattern | Frontend Contract Guidance | Status |
| --- | --- | --- | --- |
| GET | Query string through `request.args` | Use query params; unwrap `{ payload }` | Confirmed |
| POST | JSON body through `request.get_json()` | Send `Content-Type: application/json` | Confirmed |
| PUT | JSON body through `request.get_json()` in many executors; `CAPIBase` logs `request.form.get("param")` | Confirm exact per endpoint before write integration | Need Engineer Confirmation |
| DELETE | Route supports DELETE where declared, but body/query convention varies | Confirm exact per endpoint before write integration | Need Engineer Confirmation |

## Route Inventory

The table below is generated from active Flask decorators in `*_uri.py`. `Tables Referenced` is inferred from executor source code references to `CTable*` ORM classes; it is a source-code hint, not a complete SQL trace.

Note: `auth` is registered as a blueprint in `app.py` but currently has no active route decorators. Runtime route count is 70 while the documented API decorator count is 69; the remaining URL rule is app/framework-level and should be confirmed if the engineer expects another API endpoint.

| Path | Methods | Blueprint | URI Class | Executor | Executor Methods | Tables Referenced | Query/Body Parameter Hints | Status | Review Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| //device/register | POST | device | CDeviceURI | CDevice | post | device |  | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| //heartbeat | GET | heartbeat | CHeartbeatURI | CHeartbeat | get |  |  | Confirmed | Route and executor mapping confirmed from source. |
| //user/device/login | POST | user | CDeviceLoginURI | CDeviceLogin | post | device, employee, session, user_group | password, username | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| //user/device/logout | DELETE | user | CDeviceLogoutURI | CDeviceLogout | delete |  |  | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/aps/quantity | GET | aps | CQuantityURI | CQuantity | get | aps_quantity, contract, product_order | count, start | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/bankaccount | GET, POST, PUT, DELETE | bankaccount | CBankAccountURI | CBankAccount | get, post, put, delete | bank_account |  | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/batchnumber | GET, POST, PUT, DELETE | batchnumber | CBatchNumberURI | CBatchNumber | get, post, put, delete | batch_number | category, count, info, item_no, item_ref_no, no, start, type | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/batchtrace | GET | batchtrace | CBatchTraceURI | CBatchTrace | get | batch_number, goods_receipt_note, inventory_record, process_order, product_order, production_data, production_data_output, work_order | count, end_date, inventoryType, itemCategory, itemNo, order, orderCategory, start, start_date, type | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/batchtrace/record | GET | batchtrace | CBatchRecordURI | CBatchRecord | get | batch_number, inventory_record, production_data, production_data_input, production_data_output, production_data_reuse | itemCategory, no | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/bom | GET, POST, PUT, DELETE | bom | CBomURI | CBom | get, post, put, delete | bom, sample_price | count, displayName, no, start, type | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/bom/aps | GET | bom | CBomAPSURI | CBomAPS | get | aps_quantity, aps_quantity_item, product_order | children, name, order_no, process, product_no | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/bom/process | GET | bom | CProductProcessURI | CProductProcess | get | product_process | count, start | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/bom/tree | GET | bom | CBomTreeURI | CBomTree | get | item_price, product, product_spec | category, children, no, product_no | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/company | GET, POST, PUT, DELETE | company | CCompanyURI | CCompany | get, post, put, delete | company, payment | count, id, no, start | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/contract | GET, POST, PUT, DELETE | contract | CContractURI | CAPIContract | get, post, put, delete |  | category, count, end_time, itemStyle, item_no, start, start_time, type | Need Engineer Confirmation | No ORM table reference inferred; confirm payload source and business behavior. |
| /api/v1/enterprise | GET, POST, PUT, DELETE | enterprise | CEnterpriseURI | CEnterprise | get, post, put, delete | enterprise | count, id, no, start | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/goods | GET, POST, PUT, DELETE | goods | CGoodsURI | CGoods | get, post, put, delete | goods | count, start | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/inventory | GET, POST, PUT, DELETE | inventory | CInventoryURI | CInventory | get, post, put, delete | batch_number, inventory_record, process_order | batchNumber, category, count, item_no, item_ref_no, start, type | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/inventory/items | GET | inventory | CItemsURI | CItems | get |  | commit, date, end_time, itemCategory, item_no, start_time, type | Need Engineer Confirmation | No ORM table reference inferred; confirm payload source and business behavior. |
| /api/v1/inventory/months | GET | inventory | CMonthsURI | CMonthAmount | get |  | end_time, start_time | Need Engineer Confirmation | No ORM table reference inferred; confirm payload source and business behavior. |
| /api/v1/inventory/price | GET, POST, PUT, DELETE | inventory | CPriceURI | CPrice | get, post, put, delete | item_price, trans_items | count, start, type | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/inventory/record | POST | inventory | CInventoryTempURI | CInventoryTemp | post | batch_number | batch_number, count | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/inventory/statistics | GET | inventory | CStatisticsURI | CStatistics | get | inventory_record | batchNumber | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/material | GET, POST, PUT, DELETE | material | CMaterialURI | CMaterial | get, post, put, delete | company, material | category, count, material_id, material_no, start, supplier_no, type | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/material/itemprice | GET | material | CItemPriceURI | CItemPrice | get | item_loss, item_price | item_no | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/mix/item | GET | mix | CMixItemURI | CMixItem | get | inproduct, inproduct_bom_spec, product, product_bom_spec, product_spec, product_ver | count, start | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/mix/itemprice | GET | mix | CItemPriceURI | CItemPrice | get | item_loss, item_price | item_no | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/plstatistics/itemcapacity | GET | plstatistics | CItemCapacityURI | CItemCapacity | get | pl_item_capacity | count, start | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/plstatistics/itemcost | GET | plstatistics | CItemCostURI | CItemCost | get | pl_item_capacity | count, start | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/plstatistics/itemloss | GET | plstatistics | CItemLossURI | CItemLoss | get | pl_item_capacity, pl_item_loss | count, start | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/plstatistics/mancapacity | GET | plstatistics | CManCapacityURI | CManCapacity | get | pl_man_capacity | count, start | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/product | GET, POST, PUT, DELETE | product | CProductURI | CProduct | get, post, put, delete | product | count, product_no, start | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/productline | GET, POST, PUT, DELETE | productline | CProductLineURI | CProductLine | get, post, put, delete | production_line | oneProcess | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/productline/equipment | GET, POST, PUT, DELETE | productline | CEquipmentURI | CEquipment | get, post, put, delete | equipment |  | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/productline/factory | GET, POST, PUT, DELETE | productline | CFactoryURI | CFactory | get, post, put, delete | factory |  | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/productline/process | GET, POST, PUT, DELETE | productline | CProcessURI | CProcess | get, post, put, delete | process |  | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/productline/station | GET, POST, PUT, DELETE | productline | CStationURI | CStation | get, post, put, delete | station |  | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/purchase/arap | GET | purchase | CARAPURI | CPurchaseARAP | get |  | order_no | Need Engineer Confirmation | No ORM table reference inferred; confirm payload source and business behavior. |
| /api/v1/purchase/contract | GET, POST, PUT, DELETE | purchase | CContractURI | CPurchaseContract | get, post, put, delete |  | count, start | Need Engineer Confirmation | No ORM table reference inferred; confirm payload source and business behavior. |
| /api/v1/purchase/goodsreceiptnote | GET, POST, PUT, DELETE | purchase | CGoodsReceiptNoteURI | CGoodsReceiptNote | get, post, put, delete | batch_number, goods_receipt_note, inventory_record, material, purchase_order | count, end_time, item_no, item_ref_displayName, item_ref_no, no, purchase_order_no, start, start_time, type | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/purchase/payment | GET, POST, PUT, DELETE | purchase | CPaymentURI | CPayment | get, post, put, delete | contract, order_payment, product_order, shipping_order | count, start | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/purchase/purchaseorder | GET, POST, PUT, DELETE | purchase | CPurchaseOrderURI | CPurchaseOrder | get, post, put, delete | contract, goods_receipt_note, material, purchase_order | count, end_time, item_name, item_no, item_ref_displayName, item_ref_no, no, order_no, start, start_time, status, type | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/purchase/statistics | GET | purchase | CStatisticURI | CStatistic | get |  | commit, end_time, start_time | Need Engineer Confirmation | No ORM table reference inferred; confirm payload source and business behavior. |
| /api/v1/quotation | GET, POST, PUT, DELETE | quotation | CQuotationURI | CAPIQuotation | get, post, put, delete |  | category, count, end_time, itemStyle, item_no, start, start_time, type | Need Engineer Confirmation | No ORM table reference inferred; confirm payload source and business behavior. |
| /api/v1/sale/arap | GET | sale | CARAPURI | CSaleARAP | get | shipping_order | order_no | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/sale/contract | GET, POST, PUT, DELETE | sale | CContractURI | CSaleContract | get, post, put, delete |  | count, start | Need Engineer Confirmation | No ORM table reference inferred; confirm payload source and business behavior. |
| /api/v1/sale/payment | GET, POST, PUT, DELETE | sale | CPaymentURI | CPayment | get, post, put, delete | contract, order_payment, product_order, shipping_order | count, start | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/sale/productorder | GET, POST, PUT, DELETE | sale | CProductOrderURI | CProductOrder | get, post, put, delete | contract, product_order, shipping_order | count, end_time, item_name, item_no, item_ref_name, item_ref_no, no, order_no, start, start_time, status, type | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/sale/shippingorder | GET, POST, PUT, DELETE | sale | CShippingOrderURI | CShippingOrder | get, post, put, delete | batch_number, inventory_record, product_order, shipping_order | count, end_time, item_ref_name, product_order_no, start, start_time, status | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/sale/statistics | GET | sale | CStatisticURI | CStatistic | get |  | commit, end_time, start_time | Need Engineer Confirmation | No ORM table reference inferred; confirm payload source and business behavior. |
| /api/v1/shipwarehouse | GET, POST, PUT, DELETE | shipwarehouse | CShipWarehouseURI | CShipWarehouse | get, post, put, delete | ship_wh_alias | category, count, start | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/shipwarehouse/contract | GET, POST, PUT, DELETE | shipwarehouse | CShipWarehouseContractURI | CShipWarehouseContract | get, post, put, delete | company, payment, ship_wh, ship_wh_contract | category, count, displayName, item_no, no, start | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/shipwarehouse/shiparap | GET | shipwarehouse | CShippingARAPURI | CShipARAP | get | ship_wh_contract, shipping_record | order_no | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/shipwarehouse/shippayment | GET, POST, PUT, DELETE | shipwarehouse | CShippingPaymentURI | CShipPayment | get, post, put, delete | ship_wh_contract, shipping_payment, shipping_record | category, count, start | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/shipwarehouse/shiprec | GET, POST, PUT, DELETE | shipwarehouse | CShippingRecURI | CShippingRec | get, post, put, delete | goods_receipt_note, payment, product_order, purchase_order, ship_wh_alias, ship_wh_contract, shipping_order, shipping_record | category, count, start | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/shipwarehouse/warehousearap | GET | shipwarehouse | CWarehouseARAPURI | CWarehouseARAP | get | ship_wh_contract, warehouse_record | order_category, order_no | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/shipwarehouse/warehousepayment | GET, POST, PUT, DELETE | shipwarehouse | CWarehousePaymentURI | CWarehousePayment | get, post, put, delete | ship_wh_contract, warehouse_payment, warehouse_record | count, start | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/shipwarehouse/warehouserec | GET, POST, PUT, DELETE | shipwarehouse | CWarehouseRecURI | CWarehouseRec | get, post, put, delete | batch_number, ship_wh_alias, ship_wh_contract, warehouse_record | count, start | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/transitems | GET, POST, PUT, DELETE | transitems | CTransItemsURI | CTransItems | get, post, put, delete | company, payment, trans_items, trans_items2 | category, count, date, item_no, period, start, type | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/transitems/item | GET | transitems | CTransItemsItemURI | CTransItemsItem | get, post | company, payment, trans_items | item_no | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/user/login | POST, DELETE | user | CLoginURI | CLogin | post, delete | session | password, token, username | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/work/assignment | GET | work | CAssignmentURI | CAssignment | get | batch_number, batchno_serialno, equipment, process_labor, process_order, production_line, station, work_order | batch_number, count, expectedCount, itemType, no, start, unit, validDate, work_order_no | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/work/process | GET, POST, PUT, DELETE | work | CProcessOrderURI | CProcessOrder | get, post, put, delete | batch_number, process_order, work_order | count, end_time, item_no, item_ref_no, start, start_time | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/work/productdata | GET | work | CProductDataURI | CProductData | get | batch_number, employee, equipment, labor_wage, production_line, station, work_order | children, count, end_time, itemType, no, start, start_time, stationStage, type, validDate, work_order_no | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/work/progress | GET | work | CProgressURI | CProgress | get | aps_quantity, inproduct, product, production_data, production_data_output | oneProcess, product_order_no | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/workorder | GET, POST, PUT, DELETE | workorder | CWorkOrderURI | CWorkOrder | get, post, put, delete | product, production_data_labor, production_data_output, production_line, work_order | aps_no, count, end_time, oneProcess, start, start_time, work_order_no | Need Engineer Confirmation | Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration. |
| /api/v1/workorder/expecteddata | GET | workorder | CExpectedDataURI | CExpectedData | get | batch_number, batchno_serialno, process_order, production_line, work_order | count, date, productLineName, productLine_no, start, work_order_no | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/workorder/productdata | GET | workorder | CProductDataURI | CProductData | get | batch_number, employee, equipment, labor_wage, production_line, station, work_order | children, count, end_time, itemType, no, start, start_time, stationStage, type, validDate, work_order_no | Confirmed | Route and executor mapping confirmed from source. |
| /api/v1/workorder/statistics | GET | workorder | CStatisticURI | CStatistic | get |  | commit, end_time, start_time | Need Engineer Confirmation | No ORM table reference inferred; confirm payload source and business behavior. |

## Blueprint Summary

| Blueprint | Route Count | Main Paths | Primary Tables Inferred | Confirmation Status |
| --- | ---: | --- | --- | --- |
| aps | 1 | /api/v1/aps/quantity | aps_quantity, contract, product_order | Confirmed |
| bankaccount | 1 | /api/v1/bankaccount | bank_account | Confirmed |
| batchnumber | 1 | /api/v1/batchnumber | batch_number | Confirmed |
| batchtrace | 2 | /api/v1/batchtrace, /api/v1/batchtrace/record | batch_number, goods_receipt_note, inventory_record, process_order, product_order, production_data, production_data_input, production_data_output, production_data_reuse, work_order | Confirmed |
| bom | 4 | /api/v1/bom, /api/v1/bom/aps, /api/v1/bom/process, /api/v1/bom/tree | aps_quantity, aps_quantity_item, bom, item_price, product, product_order, product_process, product_spec, sample_price | Confirmed |
| company | 1 | /api/v1/company | company, payment | Confirmed |
| contract | 1 | /api/v1/contract |  | Need Engineer Confirmation |
| device | 1 | //device/register | device | Confirmed |
| enterprise | 1 | /api/v1/enterprise | enterprise | Confirmed |
| goods | 1 | /api/v1/goods | goods | Confirmed |
| heartbeat | 1 | //heartbeat |  | Confirmed |
| inventory | 6 | /api/v1/inventory, /api/v1/inventory/items, /api/v1/inventory/months, /api/v1/inventory/price, /api/v1/inventory/record, /api/v1/inventory/statistics | batch_number, inventory_record, item_price, process_order, trans_items | Confirmed |
| material | 2 | /api/v1/material, /api/v1/material/itemprice | company, item_loss, item_price, material | Confirmed |
| mix | 2 | /api/v1/mix/item, /api/v1/mix/itemprice | inproduct, inproduct_bom_spec, item_loss, item_price, product, product_bom_spec, product_spec, product_ver | Confirmed |
| plstatistics | 4 | /api/v1/plstatistics/itemcapacity, /api/v1/plstatistics/itemcost, /api/v1/plstatistics/itemloss, /api/v1/plstatistics/mancapacity | pl_item_capacity, pl_item_loss, pl_man_capacity | Confirmed |
| product | 1 | /api/v1/product | product | Confirmed |
| productline | 5 | /api/v1/productline, /api/v1/productline/equipment, /api/v1/productline/factory, /api/v1/productline/process, /api/v1/productline/station | equipment, factory, process, production_line, station | Confirmed |
| purchase | 6 | /api/v1/purchase/arap, /api/v1/purchase/contract, /api/v1/purchase/goodsreceiptnote, /api/v1/purchase/payment, /api/v1/purchase/purchaseorder, /api/v1/purchase/statistics | batch_number, contract, goods_receipt_note, inventory_record, material, order_payment, product_order, purchase_order, shipping_order | Confirmed |
| quotation | 1 | /api/v1/quotation |  | Need Engineer Confirmation |
| sale | 6 | /api/v1/sale/arap, /api/v1/sale/contract, /api/v1/sale/payment, /api/v1/sale/productorder, /api/v1/sale/shippingorder, /api/v1/sale/statistics | batch_number, contract, inventory_record, order_payment, product_order, shipping_order | Confirmed |
| shipwarehouse | 8 | /api/v1/shipwarehouse, /api/v1/shipwarehouse/contract, /api/v1/shipwarehouse/shiparap, /api/v1/shipwarehouse/shippayment, /api/v1/shipwarehouse/shiprec, /api/v1/shipwarehouse/warehousearap ... | batch_number, company, goods_receipt_note, payment, product_order, purchase_order, ship_wh, ship_wh_alias, ship_wh_contract, shipping_order, shipping_payment, shipping_record, warehouse_payment, warehouse_record | Confirmed |
| transitems | 2 | /api/v1/transitems, /api/v1/transitems/item | company, payment, trans_items, trans_items2 | Confirmed |
| user | 3 | //user/device/login, //user/device/logout, /api/v1/user/login | device, employee, session, user_group | Confirmed |
| work | 4 | /api/v1/work/assignment, /api/v1/work/process, /api/v1/work/productdata, /api/v1/work/progress | aps_quantity, batch_number, batchno_serialno, employee, equipment, inproduct, labor_wage, process_labor, process_order, product, production_data, production_data_output, production_line, station, work_order | Confirmed |
| workorder | 4 | /api/v1/workorder, /api/v1/workorder/expecteddata, /api/v1/workorder/productdata, /api/v1/workorder/statistics | batch_number, batchno_serialno, employee, equipment, labor_wage, process_order, product, production_data_labor, production_data_output, production_line, station, work_order | Confirmed |

## Get/Set Dataset Documentation Status

| Dataset Layer | Current Understanding | Status | Next Action |
| --- | --- | --- | --- |
| DB field meaning | Centralized in `docs/spec/database/index.md` | Partially confirmed | Engineer should resolve `Need Review` DB fields. |
| Existing GET payloads | Payload keys are implemented inside executor `get()` methods and wrapped under `{ payload }` | Partially inferred | Need runtime samples or engineer confirmation for each endpoint used by frontend. |
| Existing POST/PUT/DELETE bodies | Often map closely to ORM/table fields, but exact required/optional fields are not documented in source comments | Need Engineer Confirmation | Confirm per endpoint before frontend write integration. |
| Future dashboard GET datasets | Defined separately in frontend/API specs and should be implemented as read-only aggregation APIs | Planned | Start with Warehouse dashboard API. |
| Error dataset | `code` and `message` are common; detailed validation errors are not standardized | Need Engineer Confirmation | Define frontend-safe error handling contract. |

## Engineer Confirmation Items

Use this section as the working checklist with the backend engineer.

| Priority | Item | Why It Matters | Suggested Owner | Status |
| --- | --- | --- | --- | --- |
| P0 | Confirm canonical auth behavior for local/dev/prod: `TOKEN_ENABLED`, `X_AUTH_TOKEN`, login/logout flow | Frontend API client and runtime tests need a stable auth rule | Engineer | Need Confirmation |
| P0 | Confirm exact request body convention for PUT and DELETE endpoints | Avoid frontend write integration mismatches | Engineer | Need Confirmation |
| P0 | Confirm `EErrorCode` values and frontend handling rules | Needed for shared error UI and tests | Engineer + Codex | Need Confirmation |
| P1 | Provide runtime sample responses for core read endpoints: warehouse, inventory, sale, purchase, workorder, batchtrace | Converts route inventory into precise API contract | Engineer | Need Confirmation |
| P1 | Confirm whether future V1 dashboard APIs should be new aggregation endpoints or composed from existing CRUD endpoints | Determines backend/frontend integration strategy | Engineer + Codex | Need Confirmation |
| P1 | Confirm date/time unit convention for `creationTime`, `start_time`, `end_time`, `date`, `month` | Prevents dashboard calculation errors | Engineer + User | Need Confirmation |
| P1 | Confirm enum/status values that are only visible as integers in API payloads | Needed for multilingual labels and visual status tones | Engineer + User | Need Confirmation |
| P2 | Add endpoint-level examples after runtime samples are available | Improves handoff and lowers future regression risk | Codex | Planned |

## Recommended Backend Development Flow

1. Keep existing CRUD route behavior stable unless a breaking change is explicitly agreed.
2. Add V1 read-only dashboard aggregation endpoints incrementally, beginning with Warehouse.
3. For each new endpoint, document the dataset before or alongside implementation.
4. Run runtime verification and store output under `docs/backend/runtime-verification/`.
5. Update this API index and the module-specific API spec when route behavior changes.

## Done Criteria For API Documentation

- Route exists in source and appears in this index.
- Request query/body fields are documented.
- Response `payload` fields are documented.
- Source DB tables and major fields are linked to `docs/spec/database/index.md`.
- Runtime sample exists for frontend-facing endpoints.
- Any ambiguous item is marked `Need Engineer Confirmation` rather than silently assumed.
