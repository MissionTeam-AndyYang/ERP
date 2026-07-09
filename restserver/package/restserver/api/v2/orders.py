# coding=utf8
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from sqlalchemy import or_

from package.arap.arap import g_cal_due_date
from package.common.common import (
    EDepartment,
    EErrorCode,
    EOrderPaymentRefCategory,
    EPaymentType,
)
from package.dbwrapper.dbmgr import CDBMgr
from package.dbwrapper.table import (
    CTableGoodsReceiptNote,
    CTableOrderPayment,
    CTablePayment,
    CTableProductOrder,
    CTableProductionData,
    CTablePurchaseOrder,
    CTablePurchaseRequest,
    CTableShippingOrder,
    CTableWorkOrder,
)
from package.log.log import CLogger
from package.util.util import (
    util_build_period_range,
    util_round_amount,
    util_round_quantity,
    util_safe_float,
    util_safe_int,
)


class COrdersDashboardService(object):
    PAYMENT_TYPE_DAILY = "daily"
    PAYMENT_TYPE_MONTHLY = "monthly"
    PAYMENT_TYPE_UNKNOWN = "unknown"

    STAGE_PENDING_CONFIRMATION = "pending_confirmation"
    STAGE_ACCEPTED = "accepted"
    STAGE_MATERIAL_PREPARING = "material_preparing"
    STAGE_SCHEDULED = "scheduled"
    STAGE_IN_PRODUCTION = "in_production"
    STAGE_QUALITY_CHECK = "quality_check"
    STAGE_READY_TO_SHIP = "ready_to_ship"
    STAGE_SHIPPED = "shipped"

    STATUS_DONE = "done"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_PENDING = "pending"
    STATUS_BLOCKED = "blocked"
    STATUS_UNKNOWN = "unknown"

    def get_dashboard(
        self,
        n_date=0,
        str_timezone="",
        str_period="30d",
        str_customer_no="",
        str_order_no="",
        str_commitment_decision="",
        str_delivery_risk="",
        str_stage="",
        str_keyword="",
        n_start=0,
        n_count=50,
    ):
        with CDBMgr() as obj_dbmgr:
            return self._get_dashboard_with_session(
                obj_dbmgr.get_session(),
                n_date,
                str_timezone,
                str_period,
                str_customer_no,
                str_order_no,
                str_commitment_decision,
                str_delivery_risk,
                str_stage,
                str_keyword,
                n_start,
                n_count,
            )

    def _get_dashboard_with_session(
        self,
        obj_session,
        n_date=0,
        str_timezone="",
        str_period="30d",
        str_customer_no="",
        str_order_no="",
        str_commitment_decision="",
        str_delivery_risk="",
        str_stage="",
        str_keyword="",
        n_start=0,
        n_count=50,
    ):
        return self.__get_dashboard_with_session(
            obj_session,
            n_date,
            str_timezone,
            str_period,
            str_customer_no,
            str_order_no,
            str_commitment_decision,
            str_delivery_risk,
            str_stage,
            str_keyword,
            n_start,
            n_count,
        )

    def get_fulfillment(
        self,
        str_order_no,
        n_date=0,
        str_timezone="",
    ):
        with CDBMgr() as obj_dbmgr:
            return self._get_fulfillment_with_session(
                obj_dbmgr.get_session(),
                str_order_no,
                n_date,
                str_timezone,
            )

    def _get_fulfillment_with_session(self, obj_session, str_order_no, n_date=0, str_timezone=""):
        return self.__get_fulfillment_with_session(
            obj_session,
            str_order_no,
            n_date,
            str_timezone,
        )

    def __get_dashboard_with_session(
        self,
        obj_session,
        n_date,
        str_timezone,
        str_period,
        str_customer_no,
        str_order_no,
        str_commitment_decision,
        str_delivery_risk,
        str_stage,
        str_keyword,
        n_start,
        n_count,
    ):
        n_query_timestamp = n_date if n_date else util_safe_int(time.time())
        dict_range = util_build_period_range(
            n_query_timestamp,
            str_period,
            {"7d": 7, "30d": 30, "90d": 90},
            "30d",
        )
        n_start = max(util_safe_int(n_start), 0)
        n_count = min(max(util_safe_int(n_count), 1), 100)

        lst_orders = self.__query_orders(
            obj_session,
            dict_range,
            str_customer_no,
            str_order_no,
            str_keyword,
        )
        dict_context = self.__build_context(obj_session, lst_orders)
        lst_order_rows = []
        lst_shipments = []
        lst_delivery_risks = []
        lst_margin_signals = []
        lst_payment_signals = []

        for obj_order in lst_orders:
            dict_order_context = self.__context_for_order(dict_context, obj_order.no)
            dict_order = self.__build_order_row(
                obj_order,
                dict_order_context,
                n_query_timestamp,
                str_timezone,
            )
            if str_commitment_decision and dict_order["commitmentDecision"] != str_commitment_decision:
                continue
            if str_delivery_risk and dict_order["deliveryRisk"] != str_delivery_risk:
                continue
            if str_stage and dict_order["stage"] != str_stage:
                continue

            lst_order_rows.append(dict_order)
            lst_shipments.extend(self.__build_shipment_rows(
                obj_order,
                dict_order_context,
                n_query_timestamp,
                str_timezone,
            ))
            lst_delivery_risks.extend(self.__build_delivery_risks(
                obj_order,
                dict_order,
                n_query_timestamp,
            ))
            lst_margin_signals.append(self.__build_margin_signal(dict_order))
            lst_payment_signals.extend(self.__build_payment_signals(
                obj_order,
                dict_order_context,
                n_query_timestamp,
                str_timezone,
            ))

        n_total = len(lst_order_rows)
        lst_paged_orders = lst_order_rows[n_start:n_start + n_count]
        set_paged_order_nos = {dict_row["orderNo"] for dict_row in lst_paged_orders}
        lst_paged_shipments = [
            dict_row for dict_row in lst_shipments
            if dict_row["orderNo"] in set_paged_order_nos
        ]
        lst_paged_delivery_risks = [
            dict_row for dict_row in lst_delivery_risks
            if dict_row["orderNo"] in set_paged_order_nos
        ]
        lst_paged_margin_signals = [
            dict_row for dict_row in lst_margin_signals
            if dict_row["orderNo"] in set_paged_order_nos
        ]
        lst_paged_payment_signals = [
            dict_row for dict_row in lst_payment_signals
            if dict_row["orderNo"] in set_paged_order_nos
        ]

        return {
            "serverTimestamp": n_query_timestamp,
            "timezone": str_timezone or "UTC",
            "range": dict_range,
            "summary": self.__build_summary(lst_order_rows),
            "total": n_total,
            "count": len(lst_paged_orders),
            "start": n_start,
            "orders": lst_paged_orders,
            "shipments": lst_paged_shipments,
            "commitmentChecks": [],
            "deliveryRisks": lst_paged_delivery_risks,
            "marginSignals": lst_paged_margin_signals,
            "paymentSignals": lst_paged_payment_signals,
        }

    def __get_fulfillment_with_session(
        self,
        obj_session,
        str_order_no,
        n_date,
        str_timezone,
    ):
        obj_order = obj_session.query(CTableProductOrder).filter(CTableProductOrder.no == str_order_no).first()
        if not obj_order:
            return {
                "orderNo": str_order_no or "",
                "workflow": [],
                "dependencies": [],
            }

        dict_context = self.__build_context(obj_session, [obj_order])
        dict_order_context = self.__context_for_order(dict_context, obj_order.no)
        n_query_timestamp = n_date if n_date else util_safe_int(time.time())
        dict_order = self.__build_order_row(
            obj_order,
            dict_order_context,
            n_query_timestamp,
            str_timezone,
        )
        return {
            "orderNo": obj_order.no or "",
            "workflow": self.__build_workflow(obj_order, dict_order, dict_order_context),
            "dependencies": self.__build_dependencies(dict_order, dict_order_context),
        }

    def __query_orders(
        self,
        obj_session,
        dict_range,
        str_customer_no,
        str_order_no,
        str_keyword,
    ):
        obj_query = obj_session.query(CTableProductOrder)
        if str_customer_no:
            obj_query = obj_query.filter(CTableProductOrder.item_ref_no == str_customer_no)
        if str_order_no:
            obj_query = obj_query.filter(CTableProductOrder.no == str_order_no)
        if str_keyword:
            str_like = "%%%s%%" % str_keyword
            obj_query = obj_query.filter(or_(
                CTableProductOrder.no.like(str_like),
                CTableProductOrder.item_ref_displayName.like(str_like),
                CTableProductOrder.item_no.like(str_like),
                CTableProductOrder.item_name.like(str_like),
            ))
        if not str_order_no:
            obj_query = obj_query.filter(or_(
                CTableProductOrder.expectedDate.between(dict_range["startTimestamp"], dict_range["endTimestamp"]),
                CTableProductOrder.date.between(dict_range["startTimestamp"], dict_range["endTimestamp"]),
                CTableProductOrder.creationTime.between(dict_range["startTimestamp"], dict_range["endTimestamp"]),
            ))
        return obj_query.order_by(CTableProductOrder.expectedDate.asc(), CTableProductOrder.no.asc()).all()

    def __build_context(self, obj_session, lst_orders):
        lst_order_nos = [obj_order.no for obj_order in lst_orders if obj_order.no]
        if not lst_order_nos:
            return {
                "shipments": defaultdict(list),
                "purchaseRequests": defaultdict(list),
                "purchaseOrders": defaultdict(list),
                "goodsReceipts": defaultdict(list),
                "workOrders": defaultdict(list),
                "productionData": defaultdict(list),
                "payments": defaultdict(list),
                "paymentRules": [],
            }

        lst_shipments = obj_session.query(CTableShippingOrder).filter(
            CTableShippingOrder.product_order_no.in_(lst_order_nos)
        ).all()
        lst_purchase_requests = obj_session.query(CTablePurchaseRequest).filter(
            CTablePurchaseRequest.product_order_no.in_(lst_order_nos)
        ).all()
        lst_request_nos = [obj_row.no for obj_row in lst_purchase_requests if obj_row.no]
        lst_purchase_orders = []
        if lst_request_nos:
            lst_purchase_orders = obj_session.query(CTablePurchaseOrder).filter(
                CTablePurchaseOrder.purchase_request_no.in_(lst_request_nos)
            ).all()
        lst_purchase_order_nos = [obj_row.no for obj_row in lst_purchase_orders if obj_row.no]
        lst_goods_receipts = []
        if lst_purchase_order_nos:
            lst_goods_receipts = obj_session.query(CTableGoodsReceiptNote).filter(
                CTableGoodsReceiptNote.purchase_order_no.in_(lst_purchase_order_nos)
            ).all()
        lst_work_orders = obj_session.query(CTableWorkOrder).filter(
            CTableWorkOrder.product_order_no.in_(lst_order_nos)
        ).all()
        lst_work_order_nos = [obj_row.no for obj_row in lst_work_orders if obj_row.no]
        lst_production_data = []
        if lst_work_order_nos:
            lst_production_data = obj_session.query(CTableProductionData).filter(
                CTableProductionData.work_order_no.in_(lst_work_order_nos)
            ).all()
        lst_shipping_nos = [obj_row.no for obj_row in lst_shipments if obj_row.no]
        obj_payment_query = obj_session.query(CTableOrderPayment).filter(
            CTableOrderPayment.ref_no.in_(lst_order_nos)
        )
        if lst_shipping_nos:
            obj_payment_query = obj_payment_query.union(
                obj_session.query(CTableOrderPayment).filter(
                    CTableOrderPayment.ref_sub_no.in_(lst_shipping_nos)
                )
            )
        lst_order_payments = obj_payment_query.all()
        lst_payment_rules = obj_session.query(CTablePayment).all()

        return {
            "shipments": self.__group_by_attr(lst_shipments, "product_order_no"),
            "purchaseRequests": self.__group_by_attr(lst_purchase_requests, "product_order_no"),
            "purchaseOrders": self.__group_purchase_orders_by_order(lst_purchase_requests, lst_purchase_orders),
            "goodsReceipts": self.__group_goods_receipts_by_order(lst_purchase_requests, lst_purchase_orders, lst_goods_receipts),
            "workOrders": self.__group_by_attr(lst_work_orders, "product_order_no"),
            "productionData": self.__group_production_by_order(lst_work_orders, lst_production_data),
            "payments": self.__group_payments_by_order(lst_order_payments, lst_shipments),
            "paymentRules": lst_payment_rules,
        }

    def __context_for_order(self, dict_context, str_order_no):
        return {
            "shipments": dict_context["shipments"].get(str_order_no, []),
            "purchaseRequests": dict_context["purchaseRequests"].get(str_order_no, []),
            "purchaseOrders": dict_context["purchaseOrders"].get(str_order_no, []),
            "goodsReceipts": dict_context["goodsReceipts"].get(str_order_no, []),
            "workOrders": dict_context["workOrders"].get(str_order_no, []),
            "productionData": dict_context["productionData"].get(str_order_no, []),
            "payments": dict_context["payments"].get(str_order_no, []),
            "paymentRules": dict_context["paymentRules"],
        }

    def __build_order_row(
        self,
        obj_order,
        dict_context,
        n_query_timestamp,
        str_timezone,
    ):
        f_order_quantity = util_round_quantity(obj_order.count)
        dict_shipment_summary = self.__build_shipment_summary(obj_order, dict_context["shipments"])
        str_stage = self.__resolve_stage(
            f_order_quantity,
            dict_shipment_summary,
            dict_context,
        )
        str_payment_status, str_payment_risk = self.__resolve_payment_status(
            obj_order,
            dict_context,
            n_query_timestamp,
            str_timezone,
        )
        str_delivery_risk = self.__resolve_delivery_risk(
            obj_order,
            dict_shipment_summary,
            str_payment_risk,
            n_query_timestamp,
        )
        n_order_amount = util_round_amount(obj_order.amount)
        n_estimated_cost = 0
        f_estimated_margin_rate = self.__calc_margin_rate(n_order_amount, n_estimated_cost)
        f_actual_margin_rate = 0.0
        return {
            "orderNo": obj_order.no or "",
            "customerNo": obj_order.item_ref_no or "",
            "customerName": obj_order.item_ref_displayName or "",
            "productNo": obj_order.item_no or "",
            "productName": obj_order.item_name or "",
            "quantity": f_order_quantity,
            "unit": util_safe_int(obj_order.unit),
            "orderAmount": n_order_amount,
            "estimatedCost": n_estimated_cost,
            "estimatedMarginRate": f_estimated_margin_rate,
            "actualMarginRate": f_actual_margin_rate,
            "dueTimestamp": util_safe_int(obj_order.expectedDate),
            "shipmentSummary": dict_shipment_summary,
            "committedTimestamp": 0,
            "stage": str_stage,
            "deliveryRisk": str_delivery_risk,
            "commitmentDecision": "deferred",
            "productionFeasibility": "deferred",
            "riskReason": self.__build_risk_reason(str_delivery_risk, str_payment_risk),
            "materialStatus": self.__resolve_material_status(dict_context),
            "productionStatus": self.__resolve_production_status(dict_context, dict_shipment_summary),
            "qualityStatus": "unknown",
            "shippingStatus": dict_shipment_summary["shippingStatus"],
            "paymentStatus": str_payment_status,
            "ownerDepartment": self.__resolve_owner_department(str_stage, str_payment_risk),
            "priority": self.__resolve_priority(str_delivery_risk, str_payment_risk),
        }

    def __build_shipment_summary(self, obj_order, lst_shipments):
        f_order_quantity = util_round_quantity(obj_order.count)
        f_shipped_quantity = util_round_quantity(sum(
            util_safe_float(obj_row.checkedCount)
            for obj_row in lst_shipments
        ))
        f_remaining_quantity = max(util_round_quantity(f_order_quantity - f_shipped_quantity), 0.0)
        lst_ship_dates = [
            util_safe_int(obj_row.date)
            for obj_row in lst_shipments
            if util_safe_int(obj_row.date) > 0
        ]
        str_shipping_status = "pending"
        if f_order_quantity > 0 and f_shipped_quantity >= f_order_quantity:
            str_shipping_status = "shipped"
        elif f_shipped_quantity > 0:
            str_shipping_status = "partial_shipped"
        return {
            "shipmentCount": len(lst_shipments),
            "shippedQuantity": f_shipped_quantity,
            "remainingQuantity": f_remaining_quantity,
            "firstShipTimestamp": min(lst_ship_dates) if lst_ship_dates else 0,
            "lastShipTimestamp": max(lst_ship_dates) if lst_ship_dates else 0,
            "shippingStatus": str_shipping_status,
        }

    def __build_shipment_rows(
        self,
        obj_order,
        dict_context,
        n_query_timestamp,
        str_timezone,
    ):
        lst_rows = []
        for obj_shipment in dict_context["shipments"]:
            obj_payment = self.__find_payment_for_shipment(obj_order, obj_shipment, dict_context["payments"])
            str_payment_status, _ = self.__payment_status_from_payment(
                obj_payment,
                obj_order,
                obj_shipment,
                n_query_timestamp,
                str_timezone,
            )
            lst_rows.append({
                "orderNo": obj_order.no or "",
                "shippingOrderNo": obj_shipment.no or "",
                "shipTimestamp": util_safe_int(obj_shipment.date),
                "expectedQuantity": util_round_quantity(obj_shipment.expectedCount),
                "shippedQuantity": util_round_quantity(obj_shipment.checkedCount),
                "amount": self.__shipping_amount(obj_shipment),
                "paymentNo": obj_payment.no if obj_payment and obj_payment.no else "",
                "paymentStatus": str_payment_status,
                "paymentType": self.__payment_type_code(obj_order.payment_type),
                "paymentDueTimestamp": self.__calc_payment_due_timestamp(
                    obj_order,
                    obj_shipment,
                    obj_payment,
                    str_timezone,
                ),
            })
        return lst_rows

    def __build_payment_signals(
        self,
        obj_order,
        dict_context,
        n_query_timestamp,
        str_timezone,
    ):
        lst_rows = []
        if dict_context["shipments"]:
            for obj_shipment in dict_context["shipments"]:
                obj_payment = self.__find_payment_for_shipment(obj_order, obj_shipment, dict_context["payments"])
                str_payment_status, str_payment_risk = self.__payment_status_from_payment(
                    obj_payment,
                    obj_order,
                    obj_shipment,
                    n_query_timestamp,
                    str_timezone,
                )
                n_total_amount, n_remaining_amount = self.__payment_amounts(obj_payment, obj_shipment)
                lst_rows.append({
                    "orderNo": obj_order.no or "",
                    "paymentStatus": str_payment_status,
                    "shippingOrderNo": obj_shipment.no or "",
                    "paymentNo": obj_payment.no if obj_payment and obj_payment.no else "",
                    "paymentType": self.__payment_type_code(obj_order.payment_type),
                    "paymentDueTimestamp": self.__calc_payment_due_timestamp(
                        obj_order,
                        obj_shipment,
                        obj_payment,
                        str_timezone,
                    ),
                    "receivedAmount": max(n_total_amount - n_remaining_amount, 0),
                    "remainingAmount": n_remaining_amount,
                    "paymentRisk": str_payment_risk,
                })
        return lst_rows

    def __build_delivery_risks(self, obj_order, dict_order, n_query_timestamp):
        lst_rows = []
        if dict_order["deliveryRisk"] == "attention":
            lst_rows.append({
                "orderNo": obj_order.no or "",
                "riskType": "due_date_urgent",
                "riskLevel": 2,
                "ownerDepartment": dict_order["ownerDepartment"],
                "dueTimestamp": util_safe_int(obj_order.expectedDate),
                "comment": "due date approaching",
            })
        elif dict_order["deliveryRisk"] == "high_risk":
            lst_rows.append({
                "orderNo": obj_order.no or "",
                "riskType": "due_date_urgent",
                "riskLevel": 3,
                "ownerDepartment": dict_order["ownerDepartment"],
                "dueTimestamp": util_safe_int(obj_order.expectedDate),
                "comment": "due date overdue or payment risk",
            })
        if dict_order["paymentStatus"] in ["overdue", "unknown"] and dict_order["shipmentSummary"]["shippedQuantity"] > 0:
            lst_rows.append({
                "orderNo": obj_order.no or "",
                "riskType": "payment_risk",
                "riskLevel": 3 if dict_order["paymentStatus"] == "overdue" else 2,
                "ownerDepartment": EDepartment.FINANCE,
                "dueTimestamp": util_safe_int(obj_order.expectedDate),
                "comment": "payment risk",
            })
        return lst_rows

    def __build_margin_signal(self, dict_order):
        str_margin_risk = "cost_missing"
        if dict_order["estimatedCost"] > 0:
            str_margin_risk = "normal"
        return {
            "orderNo": dict_order["orderNo"],
            "estimatedMarginRate": dict_order["estimatedMarginRate"],
            "actualMarginRate": dict_order["actualMarginRate"],
            "marginRisk": str_margin_risk,
            "estimatedCost": dict_order["estimatedCost"],
            "actualCost": 0,
        }

    def __build_summary(self, lst_order_rows):
        set_payment_risk_orders = {
            dict_row["orderNo"]
            for dict_row in lst_order_rows
            if dict_row["paymentStatus"] in ["overdue", "unknown", "partial_paid", "unpaid"]
            and dict_row["shipmentSummary"]["shippedQuantity"] > 0
        }
        return {
            "openOrderCount": len([
                dict_row for dict_row in lst_order_rows
                if dict_row["shipmentSummary"]["shippingStatus"] != "shipped"
            ]),
            "highRiskOrderCount": len([
                dict_row for dict_row in lst_order_rows
                if dict_row["deliveryRisk"] == "high_risk"
            ]),
            "commitmentRate": 0.0,
            "estimatedMarginRiskCount": len([
                dict_row for dict_row in lst_order_rows
                if dict_row["estimatedCost"] == 0
            ]),
            "paymentRiskCount": len(set_payment_risk_orders),
            "totalOrderAmount": util_round_amount(sum(
                util_safe_float(dict_row["orderAmount"])
                for dict_row in lst_order_rows
            )),
        }

    def __build_workflow(self, obj_order, dict_order, dict_context):
        dict_shipment_summary = dict_order["shipmentSummary"]
        return [
            self.__workflow_step("order_received", obj_order.no, self.STATUS_DONE, EDepartment.SALES, obj_order.date, obj_order.creationTime, obj_order.comment),
            self.__workflow_step("commitment_check", "", self.STATUS_UNKNOWN, EDepartment.PLANNING, 0, 0, ""),
            self.__workflow_step("material_request", self.__join_ref_nos(dict_context["purchaseRequests"]), self.__status_by_exists(dict_context["purchaseRequests"]), EDepartment.PLANNING, self.__min_attr(dict_context["purchaseRequests"], "date"), self.__max_attr(dict_context["purchaseRequests"], "date"), ""),
            self.__workflow_step("purchase_readiness", self.__join_ref_nos(dict_context["purchaseOrders"]), self.__purchase_status(dict_context), EDepartment.PURCHASING, self.__min_attr(dict_context["purchaseOrders"], "date"), self.__max_attr(dict_context["goodsReceipts"], "date"), ""),
            self.__workflow_step("warehouse_readiness", self.__join_ref_nos(dict_context["goodsReceipts"]), self.__warehouse_status(dict_context), EDepartment.WAREHOUSE, self.__min_attr(dict_context["goodsReceipts"], "date"), self.__max_attr(dict_context["goodsReceipts"], "date"), ""),
            self.__workflow_step("production", self.__join_ref_nos(dict_context["workOrders"]), self.__production_workflow_status(dict_context, dict_shipment_summary), EDepartment.PRODUCTION, self.__min_attr(dict_context["workOrders"], "date"), self.__max_attr(dict_context["productionData"], "date"), ""),
            self.__workflow_step("quality_check", "", self.STATUS_UNKNOWN, EDepartment.QA, 0, 0, ""),
            self.__workflow_step("shipping", self.__join_ref_nos(dict_context["shipments"]), self.__shipping_workflow_status(dict_shipment_summary), EDepartment.WAREHOUSE, self.__min_attr(dict_context["shipments"], "date"), self.__max_attr(dict_context["shipments"], "date"), ""),
            self.__workflow_step("payment", self.__join_ref_nos(dict_context["payments"]), self.__payment_workflow_status(dict_order), EDepartment.FINANCE, self.__min_attr(dict_context["payments"], "date"), self.__max_attr(dict_context["payments"], "date"), ""),
        ]

    def __build_dependencies(self, dict_order, dict_context):
        return [
            self.__dependency("inventory", dict_order["materialStatus"], EDepartment.WAREHOUSE, "warehouse readiness"),
            self.__dependency("purchasing", self.__dependency_status_from_workflow(self.__purchase_status(dict_context)), EDepartment.PURCHASING, "purchase readiness"),
            self.__dependency("production", self.__dependency_status_from_workflow(self.__production_workflow_status(dict_context, dict_order["shipmentSummary"])), EDepartment.PRODUCTION, "production readiness"),
            self.__dependency("quality", "unknown", EDepartment.QA, "quality signal unavailable"),
            self.__dependency("shipping", self.__dependency_status_from_shipping(dict_order["shippingStatus"]), EDepartment.WAREHOUSE, "shipping readiness"),
            self.__dependency("payment", self.__dependency_status_from_payment(dict_order["paymentStatus"]), EDepartment.FINANCE, "payment readiness"),
        ]

    def __resolve_stage(self, f_order_quantity, dict_shipment_summary, dict_context):
        if f_order_quantity > 0 and dict_shipment_summary["shippedQuantity"] >= f_order_quantity:
            return self.STAGE_SHIPPED
        if dict_context["productionData"]:
            return self.STAGE_IN_PRODUCTION
        if dict_context["workOrders"]:
            return self.STAGE_SCHEDULED
        if dict_context["purchaseRequests"] or dict_context["purchaseOrders"] or dict_context["goodsReceipts"]:
            return self.STAGE_MATERIAL_PREPARING
        return self.STAGE_ACCEPTED

    def __resolve_material_status(self, dict_context):
        if dict_context["goodsReceipts"]:
            return "ready"
        if dict_context["purchaseRequests"] or dict_context["purchaseOrders"]:
            return "pending"
        return "unknown"

    def __resolve_production_status(self, dict_context, dict_shipment_summary):
        if dict_shipment_summary["shippingStatus"] == "shipped" and dict_context["workOrders"]:
            return "completed"
        if dict_context["productionData"]:
            return "in_progress"
        if dict_context["workOrders"]:
            return "scheduled"
        return "not_started"

    def __resolve_payment_status(self, obj_order, dict_context, n_query_timestamp, str_timezone):
        lst_statuses = []
        lst_risks = []
        for obj_shipment in dict_context["shipments"]:
            obj_payment = self.__find_payment_for_shipment(obj_order, obj_shipment, dict_context["payments"])
            str_status, str_risk = self.__payment_status_from_payment(
                obj_payment,
                obj_order,
                obj_shipment,
                n_query_timestamp,
                str_timezone,
            )
            lst_statuses.append(str_status)
            lst_risks.append(str_risk)
        if not lst_statuses:
            return "unknown", "normal"
        if "overdue" in lst_statuses:
            return "overdue", "overdue"
        if "partial_paid" in lst_statuses:
            return "partial_paid", "partial_paid"
        if "unknown" in lst_statuses:
            return "unknown", "missing_payment_record"
        if "unpaid" in lst_statuses:
            return "unpaid", "unpaid"
        return "paid", "normal"

    def __payment_status_from_payment(self, obj_payment, obj_order, obj_shipment, n_query_timestamp, str_timezone):
        if not obj_payment:
            if util_safe_float(obj_shipment.checkedCount) > 0:
                return "unknown", "missing_payment_record"
            return "unknown", "normal"

        n_total_amount, n_remaining_amount = self.__payment_amounts(obj_payment, obj_shipment)
        n_due_timestamp = self.__calc_payment_due_timestamp(obj_order, obj_shipment, obj_payment, str_timezone)
        if n_remaining_amount <= 0 and n_total_amount > 0:
            return "paid", "normal"
        if n_due_timestamp and n_query_timestamp > n_due_timestamp and n_remaining_amount > 0:
            return "overdue", "overdue"
        if n_total_amount > n_remaining_amount > 0:
            return "partial_paid", "partial_paid"
        return "unpaid", "unpaid"

    def __payment_amounts(self, obj_payment, obj_shipment):
        if obj_payment:
            n_total_amount = util_round_amount(obj_payment.totalAmount if obj_payment.totalAmount is not None else obj_payment.amount)
            n_remaining_amount = util_round_amount(obj_payment.balance if obj_payment.balance is not None else n_total_amount)
            return n_total_amount, n_remaining_amount
        n_amount = self.__shipping_amount(obj_shipment)
        return n_amount, n_amount

    def __calc_payment_due_timestamp(self, obj_order, obj_shipment, obj_payment, str_timezone):
        if obj_payment and util_safe_int(obj_payment.date) > 0 and self.__payment_type_code(obj_order.payment_type) != self.PAYMENT_TYPE_MONTHLY:
            return util_safe_int(obj_payment.date)

        str_payment_type = self.__payment_type_code(obj_order.payment_type)
        n_payment_period = util_safe_int(obj_order.payment_period)
        if str_payment_type == self.PAYMENT_TYPE_MONTHLY:
            obj_month = obj_payment.month if obj_payment and obj_payment.month else self.__date_from_timestamp(util_safe_int(obj_shipment.date), str_timezone)
            n_payment_day = util_safe_int(obj_order.payment_date)
            if obj_month and n_payment_day > 0:
                return g_cal_due_date(
                    str_timezone or "Asia/Taipei",
                    obj_month.year,
                    obj_month.month,
                    n_payment_day,
                    n_payment_period,
                )
            return 0
        if str_payment_type == self.PAYMENT_TYPE_DAILY:
            n_ship_timestamp = util_safe_int(obj_shipment.date)
            if n_ship_timestamp <= 0:
                return 0
            return n_ship_timestamp + n_payment_period * 86400
        return 0

    def __resolve_delivery_risk(self, obj_order, dict_shipment_summary, str_payment_risk, n_query_timestamp):
        if str_payment_risk in ["overdue", "missing_payment_record"]:
            return "high_risk"
        if dict_shipment_summary["shippingStatus"] == "shipped":
            return "normal"
        n_due_timestamp = util_safe_int(obj_order.expectedDate)
        if n_due_timestamp <= 0:
            return "normal"
        if n_query_timestamp > n_due_timestamp:
            return "high_risk"
        if n_due_timestamp - n_query_timestamp <= 7 * 86400:
            return "attention"
        return "normal"

    def __resolve_owner_department(self, str_stage, str_payment_risk):
        if str_payment_risk in ["overdue", "missing_payment_record", "partial_paid", "unpaid"]:
            return EDepartment.FINANCE
        if str_stage == self.STAGE_MATERIAL_PREPARING:
            return EDepartment.PURCHASING
        if str_stage in [self.STAGE_SCHEDULED, self.STAGE_IN_PRODUCTION]:
            return EDepartment.PRODUCTION
        if str_stage == self.STAGE_QUALITY_CHECK:
            return EDepartment.QA
        if str_stage in [self.STAGE_READY_TO_SHIP, self.STAGE_SHIPPED]:
            return EDepartment.WAREHOUSE
        return EDepartment.SALES

    def __resolve_priority(self, str_delivery_risk, str_payment_risk):
        if str_delivery_risk == "high_risk" or str_payment_risk in ["overdue", "missing_payment_record"]:
            return "high"
        if str_delivery_risk == "attention" or str_payment_risk in ["partial_paid", "unpaid"]:
            return "medium"
        return "low"

    def __build_risk_reason(self, str_delivery_risk, str_payment_risk):
        if str_payment_risk == "overdue":
            return "payment_overdue"
        if str_payment_risk == "missing_payment_record":
            return "missing_payment_record"
        if str_delivery_risk == "high_risk":
            return "due_date_high_risk"
        if str_delivery_risk == "attention":
            return "due_date_attention"
        return ""

    def __workflow_step(
        self,
        str_step_code,
        str_ref_no,
        str_status,
        n_owner_department,
        n_start_timestamp,
        n_end_timestamp,
        str_comment,
    ):
        return {
            "stepCode": str_step_code,
            "refNo": str_ref_no or "",
            "status": str_status,
            "ownerDepartment": n_owner_department,
            "startTimestamp": util_safe_int(n_start_timestamp),
            "endTimestamp": util_safe_int(n_end_timestamp),
            "comment": str_comment or "",
        }

    def __dependency(self, str_area, str_status, n_owner_department, str_comment):
        n_risk_level = 0
        if str_status == "blocked":
            n_risk_level = 3
        elif str_status in ["pending", "unknown"]:
            n_risk_level = 2
        return {
            "area": str_area,
            "status": str_status,
            "riskLevel": n_risk_level,
            "ownerDepartment": n_owner_department,
            "comment": str_comment,
        }

    def __purchase_status(self, dict_context):
        if not dict_context["purchaseRequests"] and not dict_context["purchaseOrders"]:
            return self.STATUS_PENDING
        if dict_context["purchaseOrders"] and dict_context["goodsReceipts"]:
            return self.STATUS_DONE
        return self.STATUS_IN_PROGRESS

    def __warehouse_status(self, dict_context):
        if dict_context["goodsReceipts"]:
            return self.STATUS_DONE
        if dict_context["purchaseOrders"]:
            return self.STATUS_IN_PROGRESS
        return self.STATUS_PENDING

    def __production_workflow_status(self, dict_context, dict_shipment_summary):
        if dict_shipment_summary["shippingStatus"] == "shipped" and dict_context["workOrders"]:
            return self.STATUS_DONE
        if dict_context["productionData"]:
            return self.STATUS_IN_PROGRESS
        if dict_context["workOrders"]:
            return self.STATUS_PENDING
        return self.STATUS_PENDING

    def __shipping_workflow_status(self, dict_shipment_summary):
        if dict_shipment_summary["shippingStatus"] == "shipped":
            return self.STATUS_DONE
        if dict_shipment_summary["shippingStatus"] == "partial_shipped":
            return self.STATUS_IN_PROGRESS
        return self.STATUS_PENDING

    def __payment_workflow_status(self, dict_order):
        if dict_order["paymentStatus"] == "paid":
            return self.STATUS_DONE
        if dict_order["paymentStatus"] in ["partial_paid", "unpaid", "overdue"]:
            return self.STATUS_IN_PROGRESS
        return self.STATUS_PENDING

    def __dependency_status_from_workflow(self, str_status):
        if str_status == self.STATUS_DONE:
            return "ready"
        if str_status == self.STATUS_BLOCKED:
            return "blocked"
        if str_status == self.STATUS_UNKNOWN:
            return "unknown"
        return "pending"

    def __dependency_status_from_shipping(self, str_status):
        if str_status == "shipped":
            return "ready"
        if str_status == "blocked":
            return "blocked"
        return "pending"

    def __dependency_status_from_payment(self, str_status):
        if str_status == "paid":
            return "ready"
        if str_status == "overdue":
            return "blocked"
        if str_status == "unknown":
            return "unknown"
        return "pending"

    def __payment_type_code(self, n_payment_type):
        if util_safe_int(n_payment_type) == EPaymentType.MONTH:
            return self.PAYMENT_TYPE_MONTHLY
        if util_safe_int(n_payment_type) == EPaymentType.NOW:
            return self.PAYMENT_TYPE_DAILY
        return self.PAYMENT_TYPE_UNKNOWN

    def __shipping_amount(self, obj_shipment):
        return util_round_amount(
            util_safe_float(obj_shipment.amount)
            + util_safe_float(obj_shipment.addDeleteAmount)
        )

    def __calc_margin_rate(self, n_order_amount, n_cost):
        if n_order_amount <= 0:
            return 0.0
        return round((n_order_amount - n_cost) / n_order_amount * 100, 2)

    def __find_payment_for_shipment(self, obj_order, obj_shipment, lst_payments):
        for obj_payment in lst_payments:
            if obj_payment.ref_sub_no and obj_payment.ref_sub_no == obj_shipment.no:
                return obj_payment
        for obj_payment in lst_payments:
            if obj_payment.ref_no == obj_order.no:
                return obj_payment
        return None

    def __group_by_attr(self, lst_rows, str_attr):
        dict_grouped = defaultdict(list)
        for obj_row in lst_rows:
            dict_grouped[getattr(obj_row, str_attr, "")].append(obj_row)
        return dict_grouped

    def __group_purchase_orders_by_order(self, lst_purchase_requests, lst_purchase_orders):
        dict_request_order_no = {
            obj_row.no: obj_row.product_order_no
            for obj_row in lst_purchase_requests
        }
        dict_grouped = defaultdict(list)
        for obj_row in lst_purchase_orders:
            str_order_no = dict_request_order_no.get(obj_row.purchase_request_no, "")
            if str_order_no:
                dict_grouped[str_order_no].append(obj_row)
        return dict_grouped

    def __group_goods_receipts_by_order(self, lst_purchase_requests, lst_purchase_orders, lst_goods_receipts):
        dict_purchase_order_no = self.__group_purchase_orders_by_order(lst_purchase_requests, lst_purchase_orders)
        dict_po_to_order = {}
        for str_order_no, lst_orders in dict_purchase_order_no.items():
            for obj_order in lst_orders:
                dict_po_to_order[obj_order.no] = str_order_no
        dict_grouped = defaultdict(list)
        for obj_row in lst_goods_receipts:
            str_order_no = dict_po_to_order.get(obj_row.purchase_order_no, "")
            if str_order_no:
                dict_grouped[str_order_no].append(obj_row)
        return dict_grouped

    def __group_production_by_order(self, lst_work_orders, lst_production_data):
        dict_work_to_order = {
            obj_row.no: obj_row.product_order_no
            for obj_row in lst_work_orders
        }
        dict_grouped = defaultdict(list)
        for obj_row in lst_production_data:
            str_order_no = dict_work_to_order.get(obj_row.work_order_no, obj_row.product_order_no)
            if str_order_no:
                dict_grouped[str_order_no].append(obj_row)
        return dict_grouped

    def __group_payments_by_order(self, lst_order_payments, lst_shipments):
        dict_shipment_to_order = {
            obj_row.no: obj_row.product_order_no
            for obj_row in lst_shipments
        }
        dict_grouped = defaultdict(list)
        for obj_row in lst_order_payments:
            str_order_no = obj_row.ref_no or dict_shipment_to_order.get(obj_row.ref_sub_no, "")
            if str_order_no:
                dict_grouped[str_order_no].append(obj_row)
        return dict_grouped

    def __join_ref_nos(self, lst_rows):
        lst_refs = [
            getattr(obj_row, "no", "")
            for obj_row in lst_rows
            if getattr(obj_row, "no", "")
        ]
        return ",".join(lst_refs)

    def __status_by_exists(self, lst_rows):
        return self.STATUS_DONE if lst_rows else self.STATUS_PENDING

    def __min_attr(self, lst_rows, str_attr):
        lst_values = [
            util_safe_int(getattr(obj_row, str_attr, 0))
            for obj_row in lst_rows
            if util_safe_int(getattr(obj_row, str_attr, 0)) > 0
        ]
        return min(lst_values) if lst_values else 0

    def __max_attr(self, lst_rows, str_attr):
        lst_values = [
            util_safe_int(getattr(obj_row, str_attr, 0))
            for obj_row in lst_rows
            if util_safe_int(getattr(obj_row, str_attr, 0)) > 0
        ]
        return max(lst_values) if lst_values else 0

    def __date_from_timestamp(self, n_timestamp, str_timezone):
        if n_timestamp <= 0:
            return None
        try:
            obj_tz = ZoneInfo(str_timezone or "Asia/Taipei")
        except Exception:
            obj_tz = timezone.utc
        return datetime.fromtimestamp(n_timestamp, tz=obj_tz).date()


class COrdersDashboard(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            from flask import request

            dict_extra_data = COrdersDashboardService().get_dashboard(
                n_date=request.args.get("date", 0, type=int),
                str_timezone=str_timezone,
                str_period=request.args.get("period", "30d", type=str),
                str_customer_no=request.args.get("customer_no", "", type=str),
                str_order_no=request.args.get("order_no", "", type=str),
                str_commitment_decision=request.args.get("commitmentDecision", "", type=str),
                str_delivery_risk=request.args.get("deliveryRisk", "", type=str),
                str_stage=request.args.get("stage", "", type=str),
                str_keyword=request.args.get("keyword", "", type=str),
                n_start=request.args.get("start", 0, type=int),
                n_count=request.args.get("count", 50, type=int),
            )
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[COrdersDashboard] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class COrdersFulfillment(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            from flask import request

            dict_extra_data = COrdersDashboardService().get_fulfillment(
                str_order_no=str_id,
                n_date=request.args.get("date", 0, type=int),
                str_timezone=str_timezone,
            )
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[COrdersFulfillment] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data
