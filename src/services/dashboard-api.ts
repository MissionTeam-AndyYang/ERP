import { dashboardMock } from "@/mock/dashboard";
import { apiGet } from "@/services/api-client";
import type { DashboardData, DashboardDataSource, ManagerFocusItem, ModuleShortcut } from "@/types/dashboard";

type DashboardResponse = Partial<DashboardData>;

export type DashboardResult = {
  data: DashboardData;
  source: DashboardDataSource;
  error?: string;
};

function hasIcons<T extends { icon: unknown }>(items: unknown): items is T[] {
  return Array.isArray(items) && items.length > 0 && typeof items[0]?.icon === "function";
}

function normalizeDashboard(payload: DashboardResponse): DashboardData {
  return {
    managerSnapshot: payload.managerSnapshot ?? dashboardMock.managerSnapshot,
    managerFocusItems: hasIcons<ManagerFocusItem>(payload.managerFocusItems)
      ? payload.managerFocusItems
      : dashboardMock.managerFocusItems,
    managerDecisionItems: payload.managerDecisionItems?.length
      ? payload.managerDecisionItems
      : dashboardMock.managerDecisionItems,
    departmentBlockers: payload.departmentBlockers?.length ? payload.departmentBlockers : dashboardMock.departmentBlockers,
    todayTasks: payload.todayTasks?.length ? payload.todayTasks : dashboardMock.todayTasks,
    preOrderPipeline: payload.preOrderPipeline?.length ? payload.preOrderPipeline : dashboardMock.preOrderPipeline,
    productionLines: payload.productionLines?.length ? payload.productionLines : dashboardMock.productionLines,
    alertItems: payload.alertItems?.length ? payload.alertItems : dashboardMock.alertItems,
    productionTrendData: payload.productionTrendData?.length ? payload.productionTrendData : dashboardMock.productionTrendData,
    oeeTrendData: payload.oeeTrendData?.length ? payload.oeeTrendData : dashboardMock.oeeTrendData,
    qualityTrendData: payload.qualityTrendData?.length ? payload.qualityTrendData : dashboardMock.qualityTrendData,
    alertDistributionData: payload.alertDistributionData?.length
      ? payload.alertDistributionData
      : dashboardMock.alertDistributionData,
    moduleShortcuts: hasIcons<ModuleShortcut>(payload.moduleShortcuts)
      ? payload.moduleShortcuts
      : dashboardMock.moduleShortcuts
  };
}

export async function getDashboard(): Promise<DashboardResult> {
  try {
    const payload = await apiGet<DashboardResponse>("/api/v1/dashboard");
    return { data: normalizeDashboard(payload), source: "api" };
  } catch (error) {
    return {
      data: dashboardMock,
      source: "mock",
      error: error instanceof Error ? error.message : "Dashboard API unavailable"
    };
  }
}
