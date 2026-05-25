import { dashboardMock } from "@/mock/dashboard";
import { apiGet, withFallbackArray } from "@/services/api-client";
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
    managerDecisionItems: withFallbackArray(payload.managerDecisionItems, dashboardMock.managerDecisionItems),
    departmentBlockers: withFallbackArray(payload.departmentBlockers, dashboardMock.departmentBlockers),
    todayTasks: withFallbackArray(payload.todayTasks, dashboardMock.todayTasks),
    preOrderPipeline: withFallbackArray(payload.preOrderPipeline, dashboardMock.preOrderPipeline),
    productionLines: withFallbackArray(payload.productionLines, dashboardMock.productionLines),
    alertItems: withFallbackArray(payload.alertItems, dashboardMock.alertItems),
    productionTrendData: withFallbackArray(payload.productionTrendData, dashboardMock.productionTrendData),
    oeeTrendData: withFallbackArray(payload.oeeTrendData, dashboardMock.oeeTrendData),
    qualityTrendData: withFallbackArray(payload.qualityTrendData, dashboardMock.qualityTrendData),
    alertDistributionData: withFallbackArray(payload.alertDistributionData, dashboardMock.alertDistributionData),
    moduleShortcuts: hasIcons<ModuleShortcut>(payload.moduleShortcuts)
      ? payload.moduleShortcuts
      : dashboardMock.moduleShortcuts
  };
}

export async function getDashboard(): Promise<DashboardResult> {
  try {
    const payload = await apiGet<DashboardResponse>("/api/v1/dashboard/manager");
    return { data: normalizeDashboard(payload), source: "api" };
  } catch (error) {
    return {
      data: dashboardMock,
      source: "mock",
      error: error instanceof Error ? error.message : "Dashboard API unavailable"
    };
  }
}
