# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.warehouse_fixture import CWarehouseFixtureP0, CWarehouseFixtureP2, CWarehouseFixtureP3, CWarehouseFixtureP4, CWarehouseFixtureP5, CWarehouseFixtureP6, CWarehouseFixtureP7, CWarehouseFixtureP8
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


class CWarehouseFixtureP0URI(CAPIBase):
    def _get_executor(self):
        return CWarehouseFixtureP0()

    def _is_vaildate_param(self):
        return False

    def _is_support_post(self):
        return False

    def _is_support_put(self):
        return False

    def _is_support_delete(self):
        return False


class CWarehouseFixtureP2URI(CAPIBase):
    def _get_executor(self):
        return CWarehouseFixtureP2()

    def _is_vaildate_param(self):
        return False

    def _is_support_post(self):
        return False

    def _is_support_put(self):
        return False

    def _is_support_delete(self):
        return False


class CWarehouseFixtureP3URI(CAPIBase):
    def _get_executor(self):
        return CWarehouseFixtureP3()

    def _is_vaildate_param(self):
        return True if self._is_post_method() else False

    def _is_support_put(self):
        return False

    def _is_support_delete(self):
        return False


class CWarehouseFixtureP4URI(CAPIBase):
    def _get_executor(self):
        return CWarehouseFixtureP4()

    def _is_vaildate_param(self):
        return True if self._is_post_method() else False

    def _is_support_put(self):
        return False

    def _is_support_delete(self):
        return False


class CWarehouseFixtureP5URI(CAPIBase):
    def _get_executor(self):
        return CWarehouseFixtureP5()

    def _is_vaildate_param(self):
        return True if self._is_post_method() else False

    def _is_support_put(self):
        return False

    def _is_support_delete(self):
        return False


class CWarehouseFixtureP6URI(CAPIBase):
    def _get_executor(self):
        return CWarehouseFixtureP6()

    def _is_vaildate_param(self):
        return True if self._is_post_method() else False

    def _is_support_put(self):
        return False

    def _is_support_delete(self):
        return False


class CWarehouseFixtureP7URI(CAPIBase):
    def _get_executor(self):
        return CWarehouseFixtureP7()

    def _is_vaildate_param(self):
        return True if self._is_post_method() else False

    def _is_support_put(self):
        return False

    def _is_support_delete(self):
        return False


class CWarehouseFixtureP8URI(CAPIBase):
    def _get_executor(self):
        return CWarehouseFixtureP8()

    def _is_vaildate_param(self):
        return True if self._is_post_method() else False

    def _is_support_put(self):
        return False

    def _is_support_delete(self):
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


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/fixture/p0", methods=["GET"])
def fixture_p0():
    obj_uri = CWarehouseFixtureP0URI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/fixture/p2", methods=["GET"])
def fixture_p2():
    obj_uri = CWarehouseFixtureP2URI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/fixture/p3", methods=["GET"])
def fixture_p3():
    obj_uri = CWarehouseFixtureP3URI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/fixture/p3/receipt", methods=["POST"])
def fixture_p3_receipt():
    obj_uri = CWarehouseFixtureP3URI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/fixture/p4", methods=["GET"])
def fixture_p4():
    obj_uri = CWarehouseFixtureP4URI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/fixture/p4/reversal", methods=["POST"])
def fixture_p4_reversal():
    obj_uri = CWarehouseFixtureP4URI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/fixture/p5", methods=["GET"])
def fixture_p5():
    obj_uri = CWarehouseFixtureP5URI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/fixture/p5/adjustment", methods=["POST"])
def fixture_p5_adjustment():
    obj_uri = CWarehouseFixtureP5URI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/fixture/p6", methods=["GET"])
def fixture_p6():
    obj_uri = CWarehouseFixtureP6URI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/fixture/p6/proposal", methods=["POST"])
def fixture_p6_proposal():
    obj_uri = CWarehouseFixtureP6URI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/fixture/p7", methods=["GET"])
def fixture_p7():
    obj_uri = CWarehouseFixtureP7URI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/fixture/p7/outbound", methods=["POST"])
def fixture_p7_outbound():
    obj_uri = CWarehouseFixtureP7URI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/fixture/p8", methods=["GET"])
def fixture_p8():
    obj_uri = CWarehouseFixtureP8URI()
    return obj_uri.run()


@warehouse_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/fixture/p8/transfer", methods=["POST"])
def fixture_p8_transfer():
    obj_uri = CWarehouseFixtureP8URI()
    return obj_uri.run()
