# coding=utf8
import time
from collections import defaultdict

from flask import request
from sqlalchemy import or_

from package.common.common import (
    EGoodsReceiptNoteCategory,
    EPurchasingRiskType,
    EProductionRiskLevel,
)
from package.dbwrapper.dbmgr import CDBMgr
from package.dbwrapper.table import (
    CTableCompany,
    CTableGoodsReceiptNote,
    CTablePurchaseOrder,
    CTablePurchaseRequest,
)
from package.util.util import (
    util_build_local_date_range, util_round_amount, util_round_price, util_round_quantity,
    util_safe_float, util_safe_int,
)


class CPurchasingPurchaseOrderService(object):
    def __init__(self, str_timezone):
        self.str_timezone = str_timezone or "UTC"

    def __range(self):
        str_start = request.args.get("startDate", "", type=str)
        str_end = request.args.get("endDate", "", type=str)
        if not str_start or not str_end:
            return None
        return util_build_local_date_range(str_start, str_end, self.str_timezone)

    def __base_orders(self, obj_session, dict_range):
        str_keyword = request.args.get("keyword", "", type=str)
        str_supplier_no = request.args.get("supplierNo", "", type=str)
        lst_filter = [
            CTablePurchaseOrder.date >= dict_range["startTimestamp"],
            CTablePurchaseOrder.date <= dict_range["endTimestamp"],
        ]
        if str_supplier_no:
            lst_filter.append(CTablePurchaseOrder.item_ref_no == str_supplier_no)
        if str_keyword:
            str_like = "%" + str_keyword + "%"
            lst_filter.append(or_(CTablePurchaseOrder.no.like(str_like),
                                  CTablePurchaseOrder.item_no.like(str_like),
                                  CTablePurchaseOrder.item_name.like(str_like)))
        return obj_session.query(CTablePurchaseOrder).filter(*lst_filter).order_by(
            CTablePurchaseOrder.expectedDate.asc(), CTablePurchaseOrder.no.asc()
        ).all()

    def __receipts(self, obj_session, lst_order_no):
        if not lst_order_no:
            return defaultdict(list)
        dict_receipts = defaultdict(list)
        for obj_row in obj_session.query(CTableGoodsReceiptNote).filter(
                CTableGoodsReceiptNote.purchase_order_no.in_(lst_order_no)).order_by(
                CTableGoodsReceiptNote.date.asc(), CTableGoodsReceiptNote.no.asc()).all():
            dict_receipts[obj_row.purchase_order_no].append(obj_row)
        return dict_receipts

    def __received_count(self, lst_receipts):
        return util_round_quantity(sum(
            util_safe_float(obj_row.checkedCount) * (-1 if obj_row.category == EGoodsReceiptNoteCategory.RETURN else 1)
            for obj_row in lst_receipts
        ))

    def __row(self, obj_session, obj_order, dict_receipts, n_now):
        obj_company = obj_session.query(CTableCompany).filter(
            CTableCompany.no == obj_order.item_ref_no).first()
        obj_request = None
        if obj_order.purchase_request_no:
            obj_request = obj_session.query(CTablePurchaseRequest).filter(
                CTablePurchaseRequest.no == obj_order.purchase_request_no).first()
        f_ordered = util_round_quantity(obj_order.count)
        f_received = self.__received_count(dict_receipts.get(obj_order.no, []))
        f_open = util_round_quantity(max(f_ordered - f_received, 0))
        n_expected = util_safe_int(obj_order.expectedDate)
        n_risk_level = EProductionRiskLevel.NORMAL
        str_risk_type = EPurchasingRiskType.NORMAL
        if f_open > 0:
            if n_expected and n_expected < n_now:
                n_risk_level = EProductionRiskLevel.DANGER
                str_risk_type = EPurchasingRiskType.LATE_ARRIVAL
            elif n_expected and util_build_local_date_range(
                    time.strftime("%Y-%m-%d", time.localtime(n_now)),
                    time.strftime("%Y-%m-%d", time.localtime(n_now)), self.str_timezone
            ) and n_expected <= n_now + 86400:
                n_risk_level = EProductionRiskLevel.NOTICE
                str_risk_type = EPurchasingRiskType.DUE_TODAY
            elif not obj_request:
                n_risk_level = EProductionRiskLevel.NOTICE
                str_risk_type = EPurchasingRiskType.PURCHASE_REQUEST_UNLINKED
            else:
                n_risk_level = EProductionRiskLevel.NOTICE
                str_risk_type = EPurchasingRiskType.OPEN_RECEIPT
        return {
            "purchaseOrderNo": obj_order.no or "", "purchaseDateTimestamp": util_safe_int(obj_order.date),
            "itemNo": obj_order.item_no or "", "itemName": obj_order.item_name or "", "unit": util_safe_int(obj_order.unit),
            "supplierNo": obj_order.item_ref_no or "", "supplierName": getattr(obj_company, "displayName", "") or "",
            "orderedCount": f_ordered, "receivedCount": f_received, "openCount": f_open,
            "unitPrice": util_round_price(obj_order.price), "purchaseAmount": util_round_amount(obj_order.amount),
            "expectedArrivalTimestamp": n_expected, "purchaseRequestNo": obj_order.purchase_request_no or "",
            "purchaseRequestLinkStatusCode": "linked" if obj_request else ("unlinked" if not obj_order.purchase_request_no else "invalid"),
            "sourceOrderNo": getattr(obj_request, "product_order_no", "") or "", "linkedWorkOrderNo": "",
            "warehouseStatusCode": "not_received" if not dict_receipts.get(obj_order.no) else "unknown",
            "riskLevel": n_risk_level, "riskType": str_risk_type,
        }

    def __response(self, dict_range, dict_payload):
        return {"serverTimestamp": util_safe_int(time.time()), "timezone": self.str_timezone,
                "range": dict_range, **dict_payload}

    def get_dashboard(self):
        dict_range = self.__range()
        if not dict_range:
            return None
        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            lst_orders = self.__base_orders(obj_session, dict_range)
            dict_receipts = self.__receipts(obj_session, [obj_row.no for obj_row in lst_orders])
            lst_rows = [self.__row(obj_session, obj_row, dict_receipts, int(time.time())) for obj_row in lst_orders]
            n_risk_level = request.args.get("riskLevel", None, type=int)
            if n_risk_level is not None:
                lst_rows = [dict_row for dict_row in lst_rows if dict_row["riskLevel"] == n_risk_level]
            n_start = max(request.args.get("start", 0, type=int), 0)
            n_count = min(max(request.args.get("count", 50, type=int), 1), 100)
            return self.__response(dict_range, {"summary": {
                "openPurchaseOrderCount": sum(1 for dict_row in lst_rows if dict_row["openCount"] > 0),
                "lateOrDueTodayCount": sum(1 for dict_row in lst_rows if dict_row["riskType"] in (
                    EPurchasingRiskType.LATE_ARRIVAL, EPurchasingRiskType.DUE_TODAY)),
                "purchaseAmount": util_round_amount(sum(dict_row["purchaseAmount"] for dict_row in lst_rows)),
                "unlinkedPurchaseRequestCount": sum(1 for dict_row in lst_rows if dict_row["purchaseRequestLinkStatusCode"] != "linked"),
            }, "items": lst_rows[n_start:n_start + n_count], "total": len(lst_rows), "start": n_start,
                "count": len(lst_rows[n_start:n_start + n_count])})

    def get_delivery_risk(self):
        dict_payload = self.get_dashboard()
        if dict_payload is None:
            return None
        lst_rows = [dict_row for dict_row in dict_payload["items"] if dict_row["riskLevel"] != EProductionRiskLevel.NORMAL]
        dict_payload["items"] = lst_rows
        dict_payload["total"] = len(lst_rows)
        dict_payload["count"] = len(lst_rows)
        dict_payload["summary"] = {
            "highRiskCount": sum(1 for dict_row in lst_rows if dict_row["riskLevel"] == EProductionRiskLevel.DANGER),
            "noticeCount": sum(1 for dict_row in lst_rows if dict_row["riskLevel"] == EProductionRiskLevel.NOTICE),
            "lateCount": sum(1 for dict_row in lst_rows if dict_row["riskType"] == EPurchasingRiskType.LATE_ARRIVAL),
            "affectedWorkOrderCount": 0, "averageLateDays": 0.0,
        }
        for dict_row in dict_payload["items"]:
            f_shortage = dict_row.pop("openCount")
            dict_row.update({"shortageCount": f_shortage,
                             "shortageValue": util_round_amount(f_shortage * dict_row["unitPrice"]),
                             "impactSourceType": "unknown", "impactSourceNo": "",
                             "followUpCode": "confirm_supplier_date"})
        return dict_payload

    def get_receipts(self):
        dict_range = self.__range()
        if not dict_range:
            return None
        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            lst_rows = obj_session.query(CTableGoodsReceiptNote).filter(
                CTableGoodsReceiptNote.date >= dict_range["startTimestamp"],
                CTableGoodsReceiptNote.date <= dict_range["endTimestamp"],
            ).order_by(CTableGoodsReceiptNote.date.asc(), CTableGoodsReceiptNote.no.asc()).all()
            lst_result = []
            for obj_row in lst_rows:
                str_receiving = "returned" if obj_row.category == 1 else ("received" if util_safe_float(obj_row.checkedCount) > 0 else "unknown")
                lst_result.append({"no": obj_row.no or "", "purchaseOrderNo": obj_row.purchase_order_no or "",
                    "dateTimestamp": util_safe_int(obj_row.date), "category": util_safe_int(obj_row.category),
                    "itemNo": obj_row.item_no or "", "itemName": obj_row.item_name or "",
                    "expectedCount": util_round_quantity(obj_row.expectedCount), "checkedCount": util_round_quantity(obj_row.checkedCount),
                    "receivedCount": util_round_quantity(obj_row.checkedCount), "receivingStatusCode": str_receiving,
                    "warehouseStatusCode": "unknown", "nextOwnerDepartment": 0})
            n_start = max(request.args.get("start", 0, type=int), 0)
            n_count = min(max(request.args.get("count", 50, type=int), 1), 100)
            return self.__response(dict_range, {"summary": {"receiptCount": len(lst_result), "pendingPutawayCount": len(lst_result)},
                "items": lst_result[n_start:n_start + n_count], "total": len(lst_result), "start": n_start,
                "count": len(lst_result[n_start:n_start + n_count])})

    def get_suppliers(self):
        dict_payload = self.get_dashboard()
        if dict_payload is None:
            return None
        dict_rows = {}
        for dict_row in dict_payload["items"]:
            str_key = dict_row["supplierNo"]
            dict_item = dict_rows.setdefault(str_key, {"supplierNo": str_key, "supplierName": dict_row["supplierName"],
                "purchaseOrderCount": 0, "openPurchaseOrderCount": 0, "latePurchaseOrderCount": 0,
                "purchaseAmount": 0, "pendingReceiptCount": 0,
                "riskLevel": EProductionRiskLevel.NORMAL})
            dict_item["purchaseOrderCount"] += 1
            dict_item["openPurchaseOrderCount"] += int(dict_row["openCount"] > 0)
            dict_item["latePurchaseOrderCount"] += int(
                dict_row["riskType"] == EPurchasingRiskType.LATE_ARRIVAL
            )
            dict_item["purchaseAmount"] += dict_row["purchaseAmount"]
            dict_item["pendingReceiptCount"] += dict_row["openCount"]
            if dict_row["riskLevel"] > dict_item["riskLevel"]:
                dict_item["riskLevel"] = dict_row["riskLevel"]
        lst_result = list(dict_rows.values())
        for dict_row in lst_result:
            dict_row["purchaseAmount"] = util_round_amount(dict_row["purchaseAmount"])
            dict_row["pendingReceiptCount"] = util_round_quantity(dict_row["pendingReceiptCount"])
        dict_payload["items"] = lst_result
        dict_payload["total"] = len(lst_result)
        dict_payload["count"] = len(lst_result)
        return dict_payload

    def get_detail(self, str_order_no):
        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            obj_order = obj_session.query(CTablePurchaseOrder).filter(CTablePurchaseOrder.no == str_order_no).first()
            if not obj_order:
                return None
            obj_company = obj_session.query(CTableCompany).filter(CTableCompany.no == obj_order.item_ref_no).first()
            obj_request = obj_session.query(CTablePurchaseRequest).filter(CTablePurchaseRequest.no == obj_order.purchase_request_no).first() if obj_order.purchase_request_no else None
            lst_receipts = obj_session.query(CTableGoodsReceiptNote).filter(CTableGoodsReceiptNote.purchase_order_no == str_order_no).order_by(CTableGoodsReceiptNote.date.asc(), CTableGoodsReceiptNote.no.asc()).all()
            return {"serverTimestamp": util_safe_int(time.time()), "timezone": self.str_timezone,
                "purchaseOrder": {"purchaseOrderNo": obj_order.no or "", "purchaseDateTimestamp": util_safe_int(obj_order.date), "itemNo": obj_order.item_no or "", "itemName": obj_order.item_name or "", "unit": util_safe_int(obj_order.unit), "supplierNo": obj_order.item_ref_no or "", "supplierName": getattr(obj_company, "displayName", "") or "", "orderedCount": util_round_quantity(obj_order.count), "unitPrice": util_round_price(obj_order.price), "purchaseAmount": util_round_amount(obj_order.amount), "expectedArrivalTimestamp": util_safe_int(obj_order.expectedDate), "comment": obj_order.comment or ""},
                "purchaseRequest": {"purchaseRequestNo": obj_request.no, "sourceOrderNo": obj_request.product_order_no or "", "itemNo": obj_request.item_no or "", "requestedCount": util_round_quantity(obj_request.count)} if obj_request else None,
                "supplier": {"supplierNo": obj_order.item_ref_no or "", "supplierName": getattr(obj_company, "displayName", "") or ""},
                "receipts": [{"no": obj_row.no or "", "dateTimestamp": util_safe_int(obj_row.date), "category": util_safe_int(obj_row.category), "expectedCount": util_round_quantity(obj_row.expectedCount), "checkedCount": util_round_quantity(obj_row.checkedCount), "receivedCount": util_round_quantity(obj_row.checkedCount), "receivingStatusCode": "returned" if obj_row.category == 1 else ("received" if util_safe_float(obj_row.checkedCount) > 0 else "unknown"), "warehouseStatusCode": "unknown"} for obj_row in lst_receipts],
                "source": {"sourceOrderNo": getattr(obj_request, "product_order_no", "") or "", "linkedWorkOrderNo": ""},
                "inventory": {"currentCount": 0.0, "reservedCount": 0.0, "availableCount": 0.0}, "workflow": [],
                "relatedDocuments": {"quoteNo": "", "contractNo": ""}}


class CPurchasingPurchaseOrderDashboard(object):
    def get(self, str_timezone, str_id):
        obj_service = CPurchasingPurchaseOrderService(str_timezone)
        dict_payload = obj_service.get_dashboard()
        return self._response(dict_payload)

    @staticmethod
    def _response(dict_payload):
        if dict_payload is None:
            return 400, 1, "invalid startDate/endDate or record not found", {}
        return 200, 0, "success", dict_payload


class CPurchasingPurchaseOrderDeliveryRisk(CPurchasingPurchaseOrderDashboard):
    def get(self, str_timezone, str_id):
        return self._response(CPurchasingPurchaseOrderService(str_timezone).get_delivery_risk())


class CPurchasingGoodsReceiptDashboard(CPurchasingPurchaseOrderDashboard):
    def get(self, str_timezone, str_id):
        return self._response(CPurchasingPurchaseOrderService(str_timezone).get_receipts())


class CPurchasingSupplierDashboard(CPurchasingPurchaseOrderDashboard):
    def get(self, str_timezone, str_id):
        return self._response(CPurchasingPurchaseOrderService(str_timezone).get_suppliers())


class CPurchasingPurchaseOrderDetail(CPurchasingPurchaseOrderDashboard):
    def get(self, str_timezone, str_id):
        return self._response(CPurchasingPurchaseOrderService(str_timezone).get_detail(str_id))
