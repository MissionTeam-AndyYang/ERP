# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.warehouse import (
    CWarehouseAnalytics,
    CWarehouseDashboard,
    CWarehouseInventory,
    CWarehouseInventoryLotDetail,
    CWarehouseInventoryLots,
    CWarehouseTaskWorkbench,
    CWarehouseTasks,
)


SUBKEY = "warehouse"

warehouse_v2 = Blueprint("warehouse_v2", __name__)


class CWarehouseDashboardURI(CAPIBase):
    def _get_executor(self):
        return CWarehouseDashboard()

    def _is_vaildate_param(self):
        return False


class CWarehouseInventoryURI(CAPIBase):
    def _get_executor(self):
        return CWarehouseInventory()

    def _is_vaildate_param(self):
        return False


class CWarehouseInventoryLotsURI(CAPIBase):
    def _get_executor(self):
        return CWarehouseInventoryLots()

    def _is_vaildate_param(self):
        return False


class CWarehouseInventoryLotDetailURI(CAPIBase):
    def _get_executor(self):
        return CWarehouseInventoryLotDetail()

    def _is_vaildate_param(self):
        return False


class CWarehouseTasksURI(CAPIBase):
    def _get_executor(self):
        return CWarehouseTasks()

    def _is_vaildate_param(self):
        return False


class CWarehouseTaskWorkbenchURI(CAPIBase):
    def _get_executor(self):
        return CWarehouseTaskWorkbench()

    def _is_vaildate_param(self):
        return False


class CWarehouseAnalyticsURI(CAPIBase):
    def _get_executor(self):
        return CWarehouseAnalytics()

    def _is_vaildate_param(self):
        return False


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/dashboard", methods=["GET"])
def dashboard():
    obj_uri = CWarehouseDashboardURI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/inventory", methods=["GET"])
def inventory():
    obj_uri = CWarehouseInventoryURI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/inventory/lots", methods=["GET"])
def inventory_lots():
    obj_uri = CWarehouseInventoryLotsURI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/inventory/lots/wh/<warehouse_no>/item/<item_no>/batch/<batch_no>", methods=["GET"])
def inventory_lot_detail(warehouse_no, item_no, batch_no):
    obj_uri = CWarehouseInventoryLotDetailURI()
    return obj_uri.run("%s|%s|%s" % (warehouse_no or "", item_no or "", batch_no or ""))


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/tasks", methods=["GET"])
def tasks():
    obj_uri = CWarehouseTasksURI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/task-workbench", methods=["GET"])
def task_workbench():
    obj_uri = CWarehouseTaskWorkbenchURI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/task-workbench/tasks/<task_id>", methods=["GET"])
def task_workbench_detail(task_id):
    obj_uri = CWarehouseTaskWorkbenchURI()
    return obj_uri.run(task_id or "")


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/analytics/overview", methods=["GET"])
def analytics_overview():
    obj_uri = CWarehouseAnalyticsURI()
    return obj_uri.run("overview")


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/analytics/value-trend", methods=["GET"])
def analytics_value_trend():
    obj_uri = CWarehouseAnalyticsURI()
    return obj_uri.run("value-trend")


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/analytics/space-utilization", methods=["GET"])
def analytics_space_utilization():
    obj_uri = CWarehouseAnalyticsURI()
    return obj_uri.run("space-utilization")


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/analytics/risk-breakdown", methods=["GET"])
def analytics_risk_breakdown():
    obj_uri = CWarehouseAnalyticsURI()
    return obj_uri.run("risk-breakdown")


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/analytics/task-sla", methods=["GET"])
def analytics_task_sla():
    obj_uri = CWarehouseAnalyticsURI()
    return obj_uri.run("task-sla")
