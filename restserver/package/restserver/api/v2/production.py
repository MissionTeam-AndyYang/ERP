# coding=utf8
import time
from collections import defaultdict

from sqlalchemy import and_, or_
from sqlalchemy.sql import func
from flask import request

from package.common.common import (
    EDepartment,
    EMesEventType,
    EProductionAlertComment,
    EProductionAlertType,
    EProductionCapacityConfigStatus,
    EProductionCapacityStatus,
    EProductionChangeoverStatus,
    EProductionDeliveryRisk,
    EProductionDowntimeStatus,
    EProductionDocumentStatus,
    EProductionDocumentType,
    EProductionMachineStatus,
    EProductionMaterialStatus,
    EProductionQualityStatus,
    EProductionReadinessStatus,
    EProductionRiskLevel,
    EProductionSignalType,
    EProductionStaffStatus,
    EProductionWorkOrderStatus,
)
from package.dbwrapper.dbmgr import CDBMgr
from package.dbwrapper.table import (
    CTableAPSQuantityItem,
    CTableBatchNumber,
    CTableEmployee,
    CTableInventoryRec,
    CTableLaborWage,
    CTableProcessLabor,
    CTableProcessOrder,
    CTableProductionData,
    CTableProductionDataInput,
    CTableProductionDataLabor,
    CTableProductionDataMachine,
    CTableProductionDataOutput,
    CTableProductionDataReuse,
    CTableProductLine,
    CTableProductOrder,
    CTableProductionLineDailyCapacity,
    CTableProductionLineDowntime,
    CTableWorkOrder,
)
from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.util.util import (
    util_build_day_range,
    util_build_period_range,
    util_round_amount,
    util_round_quantity,
    util_safe_float,
    util_safe_int,
)


class CProductionDashboardService(object):
    def get_dashboard(
        self,
        n_date=0,
        str_timezone="",
        str_period="7d",
        str_production_line_no="",
        n_one_process=0,
        n_sec_process=0,
        str_work_order_no="",
        str_product_order_no="",
        str_status="",
        str_risk_type="",
        str_keyword="",
        n_start=0,
        n_count=50,
    ):
        with CDBMgr() as obj_dbmgr:
            return self.__get_dashboard_with_session(
                obj_dbmgr.get_session(), n_date, str_timezone, str_period,
                str_production_line_no, n_one_process, n_sec_process,
                str_work_order_no, str_product_order_no, str_status,
                str_risk_type, str_keyword, n_start, n_count,
            )

    def __get_dashboard_with_session(
        self, obj_session, n_date, str_timezone, str_period,
        str_production_line_no, n_one_process, n_sec_process,
        str_work_order_no, str_product_order_no, str_status,
        str_risk_type, str_keyword, n_start, n_count,
    ):
        n_query_timestamp = util_safe_int(n_date) or util_safe_int(time.time())
        dict_range = util_build_period_range(
            n_query_timestamp, str_period, {"7d": 7, "14d": 14}, "7d"
        )
        n_start = max(util_safe_int(n_start), 0)
        n_count = min(max(util_safe_int(n_count), 1), 100)
        lst_work_orders = self.__query_work_orders(
            obj_session, dict_range, str_production_line_no, n_one_process,
            n_sec_process, str_work_order_no, str_product_order_no, str_keyword,
        )
        dict_context = self.__load_context(obj_session, lst_work_orders)
        lst_rows = []
        lst_metrics = []
        lst_readiness = []
        lst_alerts = []
        for obj_work_order in lst_work_orders:
            dict_context_row = self.__context_for_work_order(dict_context, obj_work_order.no)
            dict_row, dict_readiness, lst_row_alerts = self.__build_work_order_row(
                obj_work_order, dict_context_row, n_query_timestamp,
            )
            dict_metric, lst_metric_alerts = self.__build_metric(
                obj_session, obj_work_order, dict_context_row,
            )
            if str_status and dict_row["status"] != str_status:
                continue
            if str_risk_type and not any(
                dict_alert["alertType"] == str_risk_type
                for dict_alert in lst_row_alerts + lst_metric_alerts
            ):
                continue
            lst_rows.append(dict_row)
            lst_metrics.append(dict_metric)
            lst_readiness.extend(dict_readiness)
            lst_alerts.extend(lst_row_alerts + lst_metric_alerts)

        dict_schedule = self.__build_schedule(
            obj_session, lst_work_orders, dict_context, str_timezone,
        )
        for dict_schedule_row in dict_schedule:
            if dict_schedule_row["downtimeMinutes"] > 0:
                lst_alerts.append(self.__alert(
                    EProductionAlertType.CAPACITY_DOWNTIME,
                    EProductionRiskLevel.NOTICE,
                    EDepartment.PLANNING,
                    EProductionAlertComment.CAPACITY_DOWNTIME,
                    str_production_line_no=dict_schedule_row["productionLineNo"],
                ))
            if dict_schedule_row["capacityStatus"] == EProductionCapacityStatus.MISSING_CONFIG:
                lst_alerts.append(self.__alert(
                    EProductionAlertType.CAPACITY_CONFIG_MISSING,
                    EProductionRiskLevel.NOTICE,
                    EDepartment.PLANNING,
                    EProductionAlertComment.CAPACITY_CONFIG_MISSING,
                    str_production_line_no=dict_schedule_row["productionLineNo"],
                ))
            if dict_schedule_row["dailyCapacityMinutes"] < dict_schedule_row["scheduledMinutes"]:
                lst_alerts.append(self.__alert(
                    EProductionAlertType.CAPACITY_BOTTLENECK,
                    EProductionRiskLevel.DANGER,
                    EDepartment.PLANNING,
                    EProductionAlertComment.CAPACITY_BOTTLENECK,
                    str_production_line_no=dict_schedule_row["productionLineNo"],
                ))
        n_total = len(lst_rows)
        lst_today = [
            dict_row for dict_row in lst_rows
            if util_build_day_range(n_query_timestamp, str_timezone).get("date")
            == util_build_day_range(
                dict_row.get("plannedStartTimestamp") or n_query_timestamp,
                str_timezone,
            ).get("date")
        ]
        lst_today_page = lst_today[n_start:n_start + n_count]
        set_today_nos = {dict_row["workOrderNo"] for dict_row in lst_today_page}
        lst_today_metrics = [
            dict_metric for dict_metric in lst_metrics
            if dict_metric["workOrderNo"] in set_today_nos
        ]
        dict_summary = self.__build_summary(lst_rows, lst_metrics, n_query_timestamp, str_timezone)
        return {
            "serverTimestamp": n_query_timestamp,
            "timezone": str_timezone or "UTC",
            "range": dict_range,
            "summary": dict_summary,
            "total": n_total,
            "start": n_start,
            "count": len(lst_today_page),
            "scheduleByLine": dict_schedule,
            "todayWorkOrders": lst_today_page,
            "readinessSignals": [
                dict_signal for dict_signal in lst_readiness
                if not set_today_nos or dict_signal["workOrderNo"] in set_today_nos
            ],
            "productionMetrics": lst_today_metrics,
            "alerts": [
                dict_alert for dict_alert in lst_alerts
                if not set_today_nos or not dict_alert.get("workOrderNo")
                or dict_alert["workOrderNo"] in set_today_nos
            ],
        }

    def get_work_order_detail(self, str_work_order_no, n_date=0, str_timezone=""):
        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            obj_work_order = obj_session.query(CTableWorkOrder).filter(
                CTableWorkOrder.no == str_work_order_no
            ).first()
            if not obj_work_order:
                return {"workOrder": None, "materials": [], "mesEvents": [], "outputs": [],
                        "reuseAndWaste": [], "labor": [], "machines": [], "relatedDocuments": []}
            dict_context = self.__load_context(obj_session, [obj_work_order])
            dict_row_context = self.__context_for_work_order(dict_context, str_work_order_no)
            dict_row, _, _ = self.__build_work_order_row(
                obj_work_order, dict_row_context, util_safe_int(n_date) or util_safe_int(time.time()),
            )
            obj_line = dict_row_context.get("line")
            dict_work_order = {
                "workOrderNo": obj_work_order.no or "",
                "productOrderNo": obj_work_order.product_order_no or "",
                "apsNo": obj_work_order.aps_no or "",
                "productNo": obj_work_order.product_no or "",
                "productName": obj_work_order.product_name or "",
                "outputItemNo": obj_work_order.output_item_no or "",
                "outputItemName": obj_work_order.output_item_name or "",
                "productionLineNo": obj_work_order.production_line_no or "",
                "productionLineName": getattr(obj_line, "name", "") if obj_line else "",
                "oneProcess": util_safe_int(obj_work_order.oneProcess),
                "secProcess": util_safe_int(obj_work_order.secProcess),
                "plannedStartTimestamp": util_safe_int(obj_work_order.startTime),
                "plannedEndTimestamp": util_safe_int(obj_work_order.endTime),
                "plannedQuantity": util_round_quantity(obj_work_order.processCount),
                "unit": util_safe_int(obj_work_order.processUnit),
                "plannedMinutes": util_safe_int(obj_work_order.processTime),
                "requiredStaffCount": util_safe_int(obj_work_order.laborCount),
                "assignedStaffCount": self.__assigned_staff_count(dict_row_context),
                "status": dict_row["status"],
                "comment": obj_work_order.comment or "",
            }
            return {
                "workOrder": dict_work_order,
                "materials": self.__build_materials(obj_work_order, dict_row_context),
                "mesEvents": self.__build_mes_events(dict_row_context),
                "outputs": self.__build_outputs(dict_row_context),
                "reuseAndWaste": self.__build_reuse_waste(dict_row_context),
                "labor": self.__build_labor(dict_row_context),
                "machines": self.__build_machines(dict_row_context),
                "relatedDocuments": self.__build_related_documents(obj_work_order, dict_row_context),
            }

    def __query_work_orders(
        self, obj_session, dict_range, str_production_line_no, n_one_process,
        n_sec_process, str_work_order_no, str_product_order_no, str_keyword,
    ):
        lst_filter = [
            or_(
                and_(CTableWorkOrder.date >= dict_range["startTimestamp"],
                     CTableWorkOrder.date <= dict_range["endTimestamp"]),
                and_(CTableWorkOrder.startTime >= dict_range["startTimestamp"],
                     CTableWorkOrder.startTime <= dict_range["endTimestamp"]),
            )
        ]
        if str_production_line_no:
            lst_filter.append(CTableWorkOrder.production_line_no == str_production_line_no)
        if n_one_process:
            lst_filter.append(CTableWorkOrder.oneProcess == n_one_process)
        if n_sec_process:
            lst_filter.append(CTableWorkOrder.secProcess == n_sec_process)
        if str_work_order_no:
            lst_filter.append(CTableWorkOrder.no == str_work_order_no)
        if str_product_order_no:
            lst_filter.append(CTableWorkOrder.product_order_no == str_product_order_no)
        if str_keyword:
            str_like = "%" + str_keyword + "%"
            lst_filter.append(or_(CTableWorkOrder.no.like(str_like),
                                  CTableWorkOrder.product_no.like(str_like),
                                  CTableWorkOrder.product_name.like(str_like),
                                  CTableWorkOrder.production_line_no.like(str_like)))
        return obj_session.query(CTableWorkOrder).filter(*lst_filter).order_by(
            CTableWorkOrder.startTime.asc(), CTableWorkOrder.no.asc()
        ).all()

    def __load_context(self, obj_session, lst_work_orders):
        lst_no = [obj_work_order.no for obj_work_order in lst_work_orders if obj_work_order.no]
        if not lst_no:
            return {"by_work_order": {}}
        dict_context = {
            "work_orders": {obj_work_order.no: obj_work_order for obj_work_order in lst_work_orders},
            "lines": {}, "production_data": {}, "inputs": defaultdict(list),
            "outputs": defaultdict(list), "reuse": defaultdict(list),
            "labor": defaultdict(list), "machines": defaultdict(list),
            "process_labor": defaultdict(list), "inventory": defaultdict(list),
            "aps_items": defaultdict(list), "employees": {}, "orders": {},
        }
        lst_data = obj_session.query(CTableProductionData).filter(
            CTableProductionData.work_order_no.in_(lst_no)
        ).all()
        dict_context["production_data"] = {obj_data.work_order_no: obj_data for obj_data in lst_data}
        for obj_input in obj_session.query(CTableProductionDataInput).filter(
            CTableProductionDataInput.work_order_no.in_(lst_no)
        ).all():
            dict_context["inputs"][obj_input.work_order_no].append(obj_input)
        for obj_output in obj_session.query(CTableProductionDataOutput).filter(
            CTableProductionDataOutput.work_order_no.in_(lst_no)
        ).all():
            dict_context["outputs"][obj_output.work_order_no].append(obj_output)
        for obj_reuse in obj_session.query(CTableProductionDataReuse).filter(
            CTableProductionDataReuse.work_order_no.in_(lst_no)
        ).all():
            dict_context["reuse"][obj_reuse.work_order_no].append(obj_reuse)
        for obj_labor in obj_session.query(CTableProductionDataLabor).filter(
            CTableProductionDataLabor.work_order_no.in_(lst_no)
        ).all():
            dict_context["labor"][obj_labor.work_order_no].append(obj_labor)
        for obj_machine in obj_session.query(CTableProductionDataMachine).filter(
            CTableProductionDataMachine.work_order_no.in_(lst_no)
        ).all():
            dict_context["machines"][obj_machine.work_order_no].append(obj_machine)
        lst_line_no = list({obj_work_order.production_line_no for obj_work_order in lst_work_orders
                            if obj_work_order.production_line_no})
        if lst_line_no:
            dict_context["lines"] = {
                obj_line.no: obj_line for obj_line in obj_session.query(CTableProductLine).filter(
                    CTableProductLine.no.in_(lst_line_no)
                ).all()
            }
        for obj_process_labor in obj_session.query(CTableProcessLabor).filter(
            CTableProcessLabor.work_order_no.in_(lst_no)
        ).all():
            dict_context["process_labor"][obj_process_labor.work_order_no].append(obj_process_labor)
        lst_product_order_no = list({obj_work_order.product_order_no for obj_work_order in lst_work_orders
                                     if obj_work_order.product_order_no})
        if lst_product_order_no:
            dict_context["orders"] = {
                obj_order.no: obj_order for obj_order in obj_session.query(CTableProductOrder).filter(
                    CTableProductOrder.no.in_(lst_product_order_no)
                ).all()
            }
            lst_aps_items = obj_session.query(CTableAPSQuantityItem).filter(
                CTableAPSQuantityItem.product_order_no.in_(lst_product_order_no)
            ).all()
            for obj_work_order in lst_work_orders:
                for obj_item in lst_aps_items:
                    if (obj_item.product_order_no == obj_work_order.product_order_no
                            and obj_item.output_item_no == obj_work_order.output_item_no
                            and util_safe_int(obj_item.oneProcess) == util_safe_int(obj_work_order.oneProcess)
                            and util_safe_int(obj_item.secProcess) == util_safe_int(obj_work_order.secProcess)):
                        dict_context["aps_items"][obj_work_order.no].append(obj_item)
        lst_employee_no = set()
        for lst_rows in dict_context["process_labor"].values():
            lst_employee_no.update(obj_row.employee_no for obj_row in lst_rows if obj_row.employee_no)
        for lst_rows in dict_context["labor"].values():
            lst_employee_no.update(obj_row.employee_no for obj_row in lst_rows if obj_row.employee_no)
        if lst_employee_no:
            dict_context["employees"] = {
                obj_employee.no: obj_employee for obj_employee in obj_session.query(CTableEmployee).filter(
                    CTableEmployee.no.in_(list(lst_employee_no))
                ).all()
            }
        lst_batch_no = {
            obj_row.batch_number for lst_rows in dict_context["outputs"].values()
            for obj_row in lst_rows if obj_row.batch_number
        }
        if lst_batch_no:
            lst_inventory = obj_session.query(CTableInventoryRec).filter(
                CTableInventoryRec.batchNumber.in_(list(lst_batch_no)),
                CTableInventoryRec.category == 1,
                CTableInventoryRec.source == 5,
            ).all()
            for obj_inventory in lst_inventory:
                dict_context["inventory"][obj_inventory.ref_no].append(obj_inventory)
        return dict_context

    def __context_for_work_order(self, dict_context, str_work_order_no):
        obj_work_order = dict_context["work_orders"].get(str_work_order_no)
        return {
            "work_order": obj_work_order,
            "line": dict_context["lines"].get(getattr(obj_work_order, "production_line_no", "")),
            "production_data": dict_context["production_data"].get(str_work_order_no),
            "inputs": dict_context["inputs"].get(str_work_order_no, []),
            "outputs": dict_context["outputs"].get(str_work_order_no, []),
            "reuse": dict_context["reuse"].get(str_work_order_no, []),
            "labor": dict_context["labor"].get(str_work_order_no, []),
            "machines": dict_context["machines"].get(str_work_order_no, []),
            "process_labor": dict_context["process_labor"].get(str_work_order_no, []),
            "aps_items": dict_context["aps_items"].get(str_work_order_no, []),
            "employees": dict_context["employees"],
            "inventory": dict_context["inventory"].get(str_work_order_no, []),
        }

    def __assigned_staff_count(self, dict_context):
        set_staff = {obj_row.employee_no for obj_row in dict_context["process_labor"] if obj_row.employee_no}
        set_staff.update(obj_row.employee_no for obj_row in dict_context["labor"] if obj_row.employee_no)
        return len(set_staff)

    def __build_work_order_row(self, obj_work_order, dict_context, n_query_timestamp):
        f_planned = util_safe_float(obj_work_order.processCount)
        f_completed = sum(
            util_safe_float(obj_row.count) for obj_row in dict_context["outputs"]
            if util_safe_int(obj_row.action) == 1
        )
        dict_material = self.__material_status(obj_work_order, dict_context)
        n_required_staff = util_safe_int(obj_work_order.laborCount)
        n_assigned_staff = self.__assigned_staff_count(dict_context)
        str_staff_status = self.__staff_status(n_required_staff, n_assigned_staff)
        str_machine_status = self.__machine_status(dict_context["machines"])
        n_actual_start, n_actual_end = self.__actual_times(dict_context)
        str_status = self.__work_order_status(
            obj_work_order, dict_context, f_completed, dict_material["status"],
            str_staff_status, str_machine_status,
        )
        f_progress = f_completed / f_planned * 100 if f_planned > 0 else 0
        str_delivery_risk = self.__delivery_risk(obj_work_order, str_status, n_query_timestamp)
        dict_row = {
            "workOrderNo": obj_work_order.no or "",
            "productOrderNo": obj_work_order.product_order_no or "",
            "productNo": obj_work_order.product_no or "",
            "productName": obj_work_order.product_name or "",
            "batchNumber": self.__batch_number(dict_context["outputs"]),
            "productionLineNo": obj_work_order.production_line_no or "",
            "productionLineName": getattr(dict_context.get("line"), "name", "") if dict_context.get("line") else "",
            "oneProcess": util_safe_int(obj_work_order.oneProcess),
            "secProcess": util_safe_int(obj_work_order.secProcess),
            "plannedStartTimestamp": util_safe_int(obj_work_order.startTime),
            "plannedEndTimestamp": util_safe_int(obj_work_order.endTime),
            "actualStartTimestamp": n_actual_start,
            "actualEndTimestamp": n_actual_end,
            "plannedQuantity": util_round_quantity(f_planned),
            "completedQuantity": util_round_quantity(f_completed),
            "unit": util_safe_int(obj_work_order.processUnit),
            "progressRate": util_round_quantity(f_progress),
            "status": str_status,
            "materialStatus": dict_material["status"],
            "staffStatus": str_staff_status,
            "machineStatus": str_machine_status,
            "qualityStatus": EProductionQualityStatus.DEFERRED,
            "deliveryRisk": str_delivery_risk,
            "ownerEmployeeNo": obj_work_order.creator_no or "",
            "ownerEmployeeName": self.__employee_name(obj_work_order.creator_no, dict_context["employees"]),
        }
        lst_readiness = [
            self.__build_readiness(obj_work_order, EProductionSignalType.MATERIAL, dict_material, EDepartment.WAREHOUSE),
            self.__build_readiness(obj_work_order, EProductionSignalType.STAFF, {
                "status": str_staff_status,
                "riskLevel": EProductionRiskLevel.NORMAL if str_staff_status == EProductionStaffStatus.READY else EProductionRiskLevel.NOTICE,
                "requiredStaffCount": n_required_staff,
                "assignedStaffCount": n_assigned_staff,
                "comment": "",
            }, EDepartment.PLANNING),
        ]
        lst_alerts = []
        if dict_material["status"] == EProductionMaterialStatus.UNKNOWN:
            lst_alerts.append(self.__alert(
                EProductionAlertType.MATERIAL_SHORTAGE,
                EProductionRiskLevel.WARNING,
                EDepartment.WAREHOUSE,
                EProductionAlertComment.MATERIAL_SHORTAGE,
                obj_work_order=obj_work_order,
            ))
        if str_staff_status in (EProductionStaffStatus.SHORTAGE, EProductionStaffStatus.SUPPORT_NEEDED):
            lst_alerts.append(self.__alert(
                EProductionAlertType.STAFF_SHORTAGE,
                EProductionRiskLevel.NOTICE,
                EDepartment.PLANNING,
                EProductionAlertComment.STAFF_SHORTAGE,
                obj_work_order=obj_work_order,
            ))
        if str_delivery_risk == EProductionDeliveryRisk.HIGH_RISK:
            lst_alerts.append(self.__alert(
                EProductionAlertType.SCHEDULE_DELAY,
                EProductionRiskLevel.DANGER,
                EDepartment.PLANNING,
                EProductionAlertComment.SCHEDULE_DELAY,
                obj_work_order=obj_work_order,
            ))
        return dict_row, lst_readiness, lst_alerts

    def __build_metric(self, obj_session, obj_work_order, dict_context):
        f_issued = sum(util_safe_float(obj_row.count) for obj_row in dict_context["inputs"] if util_safe_int(obj_row.action) == 1)
        f_returned = sum(util_safe_float(obj_row.count) for obj_row in dict_context["inputs"] if util_safe_int(obj_row.action) == 2)
        f_actual_input = max(f_issued - f_returned, 0)
        f_output = sum(util_safe_float(obj_row.count) for obj_row in dict_context["outputs"] if util_safe_int(obj_row.action) == 1)
        f_reuse = sum(util_safe_float(obj_row.count) for obj_row in dict_context["reuse"] if util_safe_int(obj_row.category) == 1)
        f_waste = sum(util_safe_float(obj_row.count) for obj_row in dict_context["reuse"] if util_safe_int(obj_row.category) == 2)
        obj_data = dict_context.get("production_data")
        f_loss = util_safe_float(getattr(obj_data, "materialLoss", 0))
        if f_loss <= 0:
            f_loss = max(f_actual_input - f_output - f_reuse - f_waste, 0)
        f_hours = sum(util_safe_float(obj_row.hours) for obj_row in dict_context["labor"] if util_safe_int(obj_row.action) == 1)
        n_actual_start, n_actual_end = self.__actual_times(dict_context)
        n_actual_minutes = util_safe_int(round(f_hours * 60))
        if n_actual_minutes <= 0 and n_actual_start and n_actual_end and n_actual_end >= n_actual_start:
            n_actual_minutes = util_safe_int(round((n_actual_end - n_actual_start) / 60))
        n_standard_minutes = util_safe_int(obj_work_order.processTime)
        f_efficiency = n_standard_minutes / n_actual_minutes * 100 if n_actual_minutes > 0 else 0
        f_loss_rate = f_loss / f_actual_input * 100 if f_actual_input > 0 else 0
        f_labor_cost, b_missing = self.__labor_cost(
            obj_session, dict_context["labor"], obj_work_order.date,
        )
        f_unit_cost = f_labor_cost / f_output if f_output > 0 else 0
        dict_metric = {
            "workOrderNo": obj_work_order.no or "",
            "standardMinutes": n_standard_minutes,
            "actualMinutes": n_actual_minutes,
            "efficiencyRate": util_round_quantity(f_efficiency),
            "standardInputQuantity": util_round_quantity(sum(util_safe_float(obj_row.count) for obj_row in dict_context["aps_items"])),
            "actualInputQuantity": util_round_quantity(f_actual_input),
            "outputQuantity": util_round_quantity(f_output),
            "reuseQuantity": util_round_quantity(f_reuse),
            "wasteQuantity": util_round_quantity(f_waste),
            "materialLossQuantity": util_round_quantity(f_loss),
            "materialLossRate": util_round_quantity(f_loss_rate),
            "laborHours": util_round_quantity(f_hours),
            "laborCost": util_round_amount(f_labor_cost),
            "unitLaborCost": util_round_quantity(f_unit_cost),
            "riskLevel": EProductionRiskLevel.NOTICE if b_missing else EProductionRiskLevel.NORMAL,
        }
        lst_alerts = []
        if b_missing:
            lst_alerts.append(self.__alert(
                EProductionAlertType.LABOR_COST_MISSING,
                EProductionRiskLevel.NOTICE,
                EDepartment.FINANCE,
                EProductionAlertComment.LABOR_COST_MISSING,
                obj_work_order=obj_work_order,
            ))
        return dict_metric, lst_alerts

    def __build_schedule(self, obj_session, lst_work_orders, dict_context, str_timezone):
        dict_groups = defaultdict(list)
        for obj_work_order in lst_work_orders:
            n_timestamp = util_safe_int(obj_work_order.startTime or obj_work_order.date)
            dict_day = util_build_day_range(n_timestamp, str_timezone)
            dict_groups[(dict_day["startTimestamp"], obj_work_order.production_line_no or "")].append(obj_work_order)
        lst_schedule = []
        for (n_day_start, str_line_no), lst_rows in sorted(dict_groups.items()):
            dict_day = util_build_day_range(n_day_start, str_timezone)
            obj_line = dict_context["lines"].get(str_line_no)
            obj_capacity = obj_session.query(CTableProductionLineDailyCapacity).filter(
                CTableProductionLineDailyCapacity.production_line_no == str_line_no,
                CTableProductionLineDailyCapacity.effectiveDate <= n_day_start,
            ).order_by(CTableProductionLineDailyCapacity.effectiveDate.desc()).first()
            n_base, str_capacity_status = self.__capacity_base(obj_capacity)
            lst_downtime = obj_session.query(CTableProductionLineDowntime).filter(
                CTableProductionLineDowntime.production_line_no == str_line_no,
                CTableProductionLineDowntime.status == EProductionDowntimeStatus.CONFIRMED,
                CTableProductionLineDowntime.startTime < dict_day["endTimestamp"],
                CTableProductionLineDowntime.endTime > n_day_start,
            ).all()
            n_downtime = self.__merged_downtime_minutes(lst_downtime, n_day_start, dict_day["endTimestamp"])
            n_downtime = min(n_downtime, n_base)
            n_daily = max(n_base - n_downtime, 0)
            n_scheduled = sum(util_safe_int(obj_row.processTime) for obj_row in lst_rows)
            n_available = max(n_daily - n_scheduled, 0)
            f_utilization = n_scheduled / n_daily * 100 if n_daily > 0 else 0
            n_risk = EProductionRiskLevel.DANGER if n_daily > 0 and n_scheduled > n_daily else (
                EProductionRiskLevel.NOTICE
                if str_capacity_status in (
                    EProductionCapacityStatus.MISSING_CONFIG,
                    EProductionCapacityStatus.DISABLED,
                ) else EProductionRiskLevel.NORMAL
            )
            lst_slots = []
            for obj_work_order in lst_rows:
                dict_row_context = self.__context_for_work_order(dict_context, obj_work_order.no)
                dict_row, _, _ = self.__build_work_order_row(obj_work_order, dict_row_context, n_day_start)
                lst_slots.append({
                    "workOrderNo": dict_row["workOrderNo"], "productOrderNo": dict_row["productOrderNo"],
                    "productNo": dict_row["productNo"], "productName": dict_row["productName"],
                    "batchNumber": dict_row["batchNumber"], "plannedStartTimestamp": dict_row["plannedStartTimestamp"],
                    "plannedEndTimestamp": dict_row["plannedEndTimestamp"], "plannedQuantity": dict_row["plannedQuantity"],
                    "completedQuantity": dict_row["completedQuantity"], "unit": dict_row["unit"],
                    "status": dict_row["status"], "materialStatus": dict_row["materialStatus"],
                    "staffStatus": dict_row["staffStatus"], "deliveryRisk": dict_row["deliveryRisk"],
                })
            lst_schedule.append({
                "date": n_day_start, "productionLineNo": str_line_no,
                "productionLineName": getattr(obj_line, "name", "") if obj_line else "",
                "oneProcess": util_safe_int(lst_rows[0].oneProcess), "secProcess": util_safe_int(lst_rows[0].secProcess),
                "baseCapacityMinutes": n_base, "downtimeMinutes": n_downtime,
                "dailyCapacityMinutes": n_daily, "scheduledMinutes": n_scheduled,
                "availableMinutes": n_available, "capacityStatus": str_capacity_status,
                "changeoverMinutes": 0, "changeoverStatus": EProductionChangeoverStatus.DEFERRED,
                "utilizationRate": util_round_quantity(f_utilization), "bottleneckRank": 0,
                "riskLevel": n_risk, "slots": lst_slots,
            })
        for n_rank, dict_row in enumerate(sorted(lst_schedule, key=lambda d: (d["availableMinutes"], -d["utilizationRate"])), 1):
            if dict_row["dailyCapacityMinutes"] > 0:
                dict_row["bottleneckRank"] = n_rank
        return lst_schedule

    def __build_summary(self, lst_rows, lst_metrics, n_query_timestamp, str_timezone):
        str_today = util_build_day_range(n_query_timestamp, str_timezone).get("date")
        lst_today = [dict_row for dict_row in lst_rows if util_build_day_range(
            dict_row.get("plannedStartTimestamp") or n_query_timestamp, str_timezone
        ).get("date") == str_today]
        lst_eff = [dict_row["efficiencyRate"] for dict_row in lst_metrics if dict_row["actualMinutes"] > 0]
        lst_loss = [dict_row["materialLossRate"] for dict_row in lst_metrics if dict_row["actualInputQuantity"] > 0]
        lst_labor = [dict_row["unitLaborCost"] for dict_row in lst_metrics if dict_row["laborCost"] > 0]
        return {
            "scheduledWorkOrderCount": len(lst_rows),
            "todayRunningWorkOrderCount": len([
                dict_row for dict_row in lst_today
                if dict_row["status"] == EProductionWorkOrderStatus.RUNNING
            ]),
            "readinessRiskCount": len({
                dict_row["workOrderNo"] for dict_row in lst_today
                if dict_row["materialStatus"] != EProductionMaterialStatus.READY
                or dict_row["staffStatus"] != EProductionStaffStatus.READY
            }),
            "averageEfficiencyRate": util_round_quantity(sum(lst_eff) / len(lst_eff) if lst_eff else 0),
            "averageMaterialLossRate": util_round_quantity(sum(lst_loss) / len(lst_loss) if lst_loss else 0),
            "averageUnitLaborCost": util_round_quantity(sum(lst_labor) / len(lst_labor) if lst_labor else 0),
        }

    def __capacity_base(self, obj_capacity):
        if not obj_capacity:
            return 0, EProductionCapacityStatus.MISSING_CONFIG
        n_status = util_safe_int(obj_capacity.status)
        if n_status == EProductionCapacityConfigStatus.ACTIVE:
            return max(util_safe_int(obj_capacity.availableMinutes), 0), EProductionCapacityStatus.CONFIGURED
        if n_status == EProductionCapacityConfigStatus.CLOSED:
            return 0, EProductionCapacityStatus.CLOSED
        return 0, EProductionCapacityStatus.DISABLED

    def __merged_downtime_minutes(self, lst_downtime, n_start, n_end):
        lst_ranges = []
        for obj_row in lst_downtime:
            n_row_start = max(util_safe_int(obj_row.startTime), n_start)
            n_row_end = min(util_safe_int(obj_row.endTime), n_end)
            if n_row_end > n_row_start:
                lst_ranges.append((n_row_start, n_row_end))
        lst_ranges.sort()
        n_total = 0
        n_current_start = n_current_end = 0
        for n_start_row, n_end_row in lst_ranges:
            if n_current_end == 0:
                n_current_start, n_current_end = n_start_row, n_end_row
            elif n_start_row <= n_current_end:
                n_current_end = max(n_current_end, n_end_row)
            else:
                n_total += int(round((n_current_end - n_current_start) / 60))
                n_current_start, n_current_end = n_start_row, n_end_row
        if n_current_end:
            n_total += int(round((n_current_end - n_current_start) / 60))
        return max(n_total, 0)

    def __material_status(self, obj_work_order, dict_context):
        f_required = sum(util_safe_float(obj_row.count) for obj_row in dict_context["aps_items"])
        f_issued = sum(util_safe_float(obj_row.count) for obj_row in dict_context["inputs"] if util_safe_int(obj_row.action) == 1)
        f_returned = sum(util_safe_float(obj_row.count) for obj_row in dict_context["inputs"] if util_safe_int(obj_row.action) == 2)
        f_issued = max(f_issued - f_returned, 0)
        if f_required <= 0:
            return {
                "status": EProductionMaterialStatus.UNKNOWN,
                "riskLevel": EProductionRiskLevel.NORMAL,
                "requiredQuantity": 0.0,
                "availableQuantity": 0.0,
                "gapQuantity": 0.0,
                "requiredStaffCount": 0,
                "assignedStaffCount": 0,
                "comment": EProductionAlertComment.MATERIAL_REQUIREMENT_MISSING,
            }
        if f_issued >= f_required:
            str_status = EProductionMaterialStatus.READY
        elif f_issued > 0:
            str_status = EProductionMaterialStatus.PARTIAL
        else:
            str_status = EProductionMaterialStatus.UNKNOWN
        return {"status": str_status,
                "riskLevel": EProductionRiskLevel.NORMAL if str_status == EProductionMaterialStatus.READY else EProductionRiskLevel.NOTICE,
                "requiredQuantity": util_round_quantity(f_required), "availableQuantity": 0.0,
                "gapQuantity": util_round_quantity(max(f_required - f_issued, 0)),
                "requiredStaffCount": 0, "assignedStaffCount": 0,
                "comment": EProductionAlertComment.MATERIAL_AVAILABLE_UNKNOWN}

    def __staff_status(self, n_required, n_assigned):
        if n_required <= 0:
            return EProductionStaffStatus.UNKNOWN
        if n_assigned >= n_required:
            return EProductionStaffStatus.READY
        return EProductionStaffStatus.SUPPORT_NEEDED if n_assigned > 0 else EProductionStaffStatus.SHORTAGE

    def __machine_status(self, lst_machines):
        if not lst_machines:
            return EProductionMachineStatus.UNKNOWN
        obj_latest = sorted(lst_machines, key=lambda obj_row: util_safe_int(obj_row.time))[-1]
        return {
            1: EProductionMachineStatus.RUNNING,
            2: EProductionMachineStatus.PAUSED,
            3: EProductionMachineStatus.STOPPED,
        }.get(util_safe_int(obj_latest.action), EProductionMachineStatus.UNKNOWN)

    def __work_order_status(self, obj_work_order, dict_context, f_completed, str_material, str_staff, str_machine):
        f_planned = util_safe_float(obj_work_order.processCount)
        b_inventory = bool(dict_context["inventory"])
        if f_planned > 0 and f_completed >= f_planned:
            return EProductionWorkOrderStatus.COMPLETED if b_inventory else EProductionWorkOrderStatus.PENDING_INVENTORY
        if str_machine == EProductionMachineStatus.PAUSED:
            return EProductionWorkOrderStatus.PAUSED
        if dict_context["inputs"] or dict_context["machines"]:
            return EProductionWorkOrderStatus.RUNNING
        if str_material == EProductionMaterialStatus.READY and str_staff == EProductionStaffStatus.READY:
            return EProductionWorkOrderStatus.MATERIAL_READY
        return EProductionWorkOrderStatus.SCHEDULED

    def __delivery_risk(self, obj_work_order, str_status, n_query_timestamp):
        if str_status == EProductionWorkOrderStatus.COMPLETED:
            return EProductionDeliveryRisk.NORMAL
        if not str_status:
            return EProductionDeliveryRisk.UNKNOWN
        n_expected = util_safe_int(getattr(obj_work_order, "endTime", 0))
        if n_expected and n_query_timestamp > n_expected:
            return EProductionDeliveryRisk.HIGH_RISK
        return EProductionDeliveryRisk.NORMAL

    def __actual_times(self, dict_context):
        lst_start = [util_safe_int(obj_row.time) for obj_row in dict_context["inputs"] if obj_row.time]
        lst_start.extend(util_safe_int(obj_row.time) for obj_row in dict_context["machines"] if obj_row.time)
        lst_end = [util_safe_int(obj_row.time) for obj_row in dict_context["outputs"] if obj_row.time]
        lst_end.extend(util_safe_int(obj_row.time) for obj_row in dict_context["machines"] if obj_row.time and util_safe_int(obj_row.action) == 3)
        obj_data = dict_context.get("production_data")
        if obj_data and obj_data.date:
            lst_start.append(util_safe_int(obj_data.date))
        return (min(lst_start) if lst_start else 0, max(lst_end) if lst_end else 0)

    def __batch_number(self, lst_outputs):
        return next((obj_row.batch_number for obj_row in lst_outputs if obj_row.batch_number), "")

    def __employee_name(self, str_employee_no, dict_employees):
        return getattr(dict_employees.get(str_employee_no), "name", "") if str_employee_no else ""

    def __build_readiness(self, obj_work_order, str_type, dict_status, n_department):
        return {
            "workOrderNo": obj_work_order.no or "", "signalType": str_type,
            "status": EProductionReadinessStatus.READY if dict_status["status"] == EProductionReadinessStatus.READY else EProductionReadinessStatus.ATTENTION,
            "riskLevel": util_safe_int(dict_status.get("riskLevel")), "ownerDepartment": n_department,
            "requiredQuantity": util_round_quantity(dict_status.get("requiredQuantity", 0)),
            "availableQuantity": util_round_quantity(dict_status.get("availableQuantity", 0)),
            "gapQuantity": util_round_quantity(dict_status.get("gapQuantity", 0)),
            "requiredStaffCount": util_safe_int(dict_status.get("requiredStaffCount", 0)),
            "assignedStaffCount": util_safe_int(dict_status.get("assignedStaffCount", 0)),
            "comment": dict_status.get("comment", ""),
        }

    def __alert(
        self,
        str_type,
        n_level,
        n_department,
        str_comment,
        obj_work_order=None,
        str_production_line_no="",
    ):
        return {
            "alertType": str_type,
            "workOrderNo": obj_work_order.no if obj_work_order else "",
            "productionLineNo": str_production_line_no or (
                obj_work_order.production_line_no if obj_work_order else ""
            ),
            "riskLevel": n_level,
            "ownerDepartment": n_department,
            "comment": str_comment,
        }

    def __labor_cost(self, obj_session, lst_labor, n_date):
        f_cost = 0.0
        b_missing = False
        for obj_labor in lst_labor:
            if util_safe_int(obj_labor.action) != 1:
                continue
            f_hours = util_safe_float(obj_labor.hours)
            obj_wage = obj_session.query(CTableLaborWage).filter(
                CTableLaborWage.date <= util_safe_int(n_date),
                CTableLaborWage.type == util_safe_int(obj_labor.employee_type),
                CTableLaborWage.level == util_safe_int(obj_labor.employee_level),
            ).order_by(CTableLaborWage.date.desc()).first()
            if not obj_wage:
                b_missing = True
                continue
            f_cost += f_hours * util_safe_float(obj_wage.hourly)
        return f_cost, b_missing

    def __build_materials(self, obj_work_order, dict_context):
        dict_items = {}
        for obj_item in dict_context["aps_items"]:
            dict_items[obj_item.item_no] = {
                "itemNo": obj_item.item_no or "", "itemName": obj_item.item_name or "",
                "category": util_safe_int(obj_item.itemCategory), "itemSubCategory": 0,
                "batchNumber": "", "requiredQuantity": util_round_quantity(obj_item.count),
                "issuedQuantity": 0.0, "returnedQuantity": 0.0, "availableQuantity": 0.0,
                "unit": util_safe_int(obj_item.unit), "status": EProductionMaterialStatus.UNKNOWN,
            }
        for obj_input in dict_context["inputs"]:
            dict_row = dict_items.setdefault(obj_input.item_no, {
                "itemNo": obj_input.item_no or "", "itemName": obj_input.item_name or "",
                "category": util_safe_int(obj_input.category), "itemSubCategory": util_safe_int(obj_input.itemSubCategory),
                "batchNumber": obj_input.batch_number or "", "requiredQuantity": 0.0,
                "issuedQuantity": 0.0, "returnedQuantity": 0.0, "availableQuantity": 0.0,
                "unit": util_safe_int(obj_input.unit), "status": EProductionMaterialStatus.UNKNOWN,
            })
            if util_safe_int(obj_input.action) == 1:
                dict_row["issuedQuantity"] += util_safe_float(obj_input.count)
            elif util_safe_int(obj_input.action) == 2:
                dict_row["returnedQuantity"] += util_safe_float(obj_input.count)
        for dict_row in dict_items.values():
            f_net = max(dict_row["issuedQuantity"] - dict_row["returnedQuantity"], 0)
            dict_row["status"] = (
                EProductionMaterialStatus.READY
                if dict_row["requiredQuantity"] > 0 and f_net >= dict_row["requiredQuantity"]
                else EProductionMaterialStatus.UNKNOWN
            )
            for str_key in ("requiredQuantity", "issuedQuantity", "returnedQuantity", "availableQuantity"):
                dict_row[str_key] = util_round_quantity(dict_row[str_key])
        return list(dict_items.values())

    def __build_outputs(self, dict_context):
        return [{"itemNo": obj_row.item_no or "", "itemName": obj_row.item_name or "",
                 "category": util_safe_int(obj_row.category), "itemSubCategory": util_safe_int(obj_row.itemSubCategory),
                 "batchNumber": obj_row.batch_number or "", "serialNo": obj_row.serial_no or "",
                 "validDateTimestamp": util_safe_int(obj_row.valid_date), "quantity": util_round_quantity(obj_row.count),
                 "unit": util_safe_int(obj_row.unit)} for obj_row in dict_context["outputs"]]

    def __build_reuse_waste(self, dict_context):
        return [{"itemNo": obj_row.item_no or "", "itemName": obj_row.item_name or "",
                 "category": util_safe_int(obj_row.category), "batchNumber": obj_row.batch_number or "",
                 "quantity": util_round_quantity(obj_row.count), "unit": util_safe_int(obj_row.unit),
                 "comment": obj_row.comment or ""} for obj_row in dict_context["reuse"]]

    def __build_labor(self, dict_context):
        return [{"employeeNo": obj_row.employee_no or "", "employeeName": obj_row.employee_name or self.__employee_name(obj_row.employee_no, dict_context["employees"]),
                 "employeeType": util_safe_int(obj_row.employee_type), "stationNo": obj_row.station_no or "",
                 "stationStage": util_safe_int(obj_row.stationStage), "action": util_safe_int(obj_row.action),
                 "startTimestamp": util_safe_int(obj_row.startTime), "endTimestamp": util_safe_int(obj_row.endTime),
                 "hours": util_round_quantity(obj_row.hours)} for obj_row in dict_context["labor"]]

    def __build_machines(self, dict_context):
        return [{"equipmentNo": obj_row.equipment_no or "", "equipmentName": obj_row.equipment_name or "",
                 "timestamp": util_safe_int(obj_row.time), "action": util_safe_int(obj_row.action),
                 "speed": util_round_quantity(obj_row.speed), "temperature": util_round_quantity(obj_row.temperature)}
                for obj_row in dict_context["machines"]]

    def __build_mes_events(self, dict_context):
        lst_events = []
        for obj_row in dict_context["inputs"]:
            lst_events.append({"eventType": EMesEventType.INPUT, "refNo": obj_row.process_order_no or "", "timestamp": util_safe_int(obj_row.time),
                               "itemNo": obj_row.item_no or "", "itemName": obj_row.item_name or "", "batchNumber": obj_row.batch_number or "",
                               "quantity": util_round_quantity(obj_row.count), "unit": util_safe_int(obj_row.unit), "employeeNo": "", "employeeName": "",
                               "equipmentNo": "", "equipmentName": "", "comment": obj_row.comment or ""})
        for obj_row in dict_context["outputs"]:
            lst_events.append({"eventType": EMesEventType.OUTPUT, "refNo": "", "timestamp": util_safe_int(obj_row.time),
                               "itemNo": obj_row.item_no or "", "itemName": obj_row.item_name or "", "batchNumber": obj_row.batch_number or "",
                               "quantity": util_round_quantity(obj_row.count), "unit": util_safe_int(obj_row.unit), "employeeNo": "", "employeeName": "",
                               "equipmentNo": "", "equipmentName": "", "comment": ""})
        for obj_row in dict_context["labor"]:
            lst_events.append({"eventType": EMesEventType.LABOR, "refNo": "", "timestamp": util_safe_int(obj_row.startTime),
                               "itemNo": "", "itemName": "", "batchNumber": "", "quantity": 0.0, "unit": 0,
                               "employeeNo": obj_row.employee_no or "", "employeeName": obj_row.employee_name or "",
                               "equipmentNo": "", "equipmentName": "", "comment": ""})
        for obj_row in dict_context["machines"]:
            lst_events.append({"eventType": EMesEventType.MACHINE, "refNo": "", "timestamp": util_safe_int(obj_row.time),
                               "itemNo": "", "itemName": "", "batchNumber": "", "quantity": 0.0, "unit": 0,
                               "employeeNo": "", "employeeName": "", "equipmentNo": obj_row.equipment_no or "",
                               "equipmentName": obj_row.equipment_name or "", "comment": ""})
        return sorted(lst_events, key=lambda dict_row: dict_row["timestamp"])

    def __build_related_documents(self, obj_work_order, dict_context):
        lst_docs = [{"documentType": EProductionDocumentType.WORK_ORDER, "documentNo": obj_work_order.no or "", "status": EProductionDocumentStatus.SCHEDULED, "timestamp": util_safe_int(obj_work_order.date)}]
        if obj_work_order.product_order_no:
            lst_docs.append({"documentType": EProductionDocumentType.PRODUCT_ORDER, "documentNo": obj_work_order.product_order_no, "status": EProductionDocumentStatus.LINKED, "timestamp": 0})
        if dict_context.get("production_data"):
            lst_docs.append({"documentType": EProductionDocumentType.PRODUCTION_DATA, "documentNo": obj_work_order.no or "", "status": EProductionDocumentStatus.LINKED, "timestamp": util_safe_int(dict_context["production_data"].date)})
        set_process_no = {obj_row.process_order_no for obj_row in dict_context["inputs"] + dict_context["outputs"] if obj_row.process_order_no}
        lst_docs.extend({"documentType": EProductionDocumentType.PROCESS_ORDER, "documentNo": str_no, "status": EProductionDocumentStatus.LINKED, "timestamp": 0} for str_no in sorted(set_process_no))
        return lst_docs


class CProductionDashboard(object):
    def get(self, str_timezone, str_id):
        return 200, 0, "success", CProductionDashboardService().get_dashboard(
            n_date=request.args.get("date", 0, type=int),
            str_timezone=str_timezone,
            str_period=request.args.get("period", "7d", type=str),
            str_production_line_no=request.args.get("production_line_no", "", type=str),
            n_one_process=request.args.get("oneProcess", 0, type=int),
            n_sec_process=request.args.get("secProcess", 0, type=int),
            str_work_order_no=request.args.get("work_order_no", "", type=str),
            str_product_order_no=request.args.get("product_order_no", "", type=str),
            str_status=request.args.get("status", "", type=str),
            str_risk_type=request.args.get("riskType", "", type=str),
            str_keyword=request.args.get("keyword", "", type=str),
            n_start=request.args.get("start", 0, type=int),
            n_count=request.args.get("count", 50, type=int),
        )


class CProductionWorkOrderDetail(object):
    def get(self, str_timezone, str_id):
        return 200, 0, "success", CProductionDashboardService().get_work_order_detail(
            str_id or "", request.args.get("date", 0, type=int), str_timezone,
        )
