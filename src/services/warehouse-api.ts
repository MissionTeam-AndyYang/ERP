import { warehouseDashboardMock } from "@/mock/warehouse";
import { apiGet } from "@/services/api-client";
import type { WarehouseDashboardData, WarehouseDataSource } from "@/types/warehouse";

type WarehouseDashboardResponse = Partial<WarehouseDashboardData>;

export type WarehouseDashboardResult = {
  data: WarehouseDashboardData;
  source: WarehouseDataSource;
  error?: string;
};

function normalizeWarehouseDashboard(payload: WarehouseDashboardResponse): WarehouseDashboardData {
  return {
    kpis: payload.kpis?.length ? payload.kpis : warehouseDashboardMock.kpis,
    categorySummaries: payload.categorySummaries?.length
      ? payload.categorySummaries
      : warehouseDashboardMock.categorySummaries,
    capacities: payload.capacities?.length ? payload.capacities : warehouseDashboardMock.capacities,
    records: payload.records?.length ? payload.records : warehouseDashboardMock.records,
    risks: payload.risks?.length ? payload.risks : warehouseDashboardMock.risks,
    tasks: payload.tasks?.length ? payload.tasks : warehouseDashboardMock.tasks
  };
}

export async function getWarehouseDashboard(): Promise<WarehouseDashboardResult> {
  try {
    const payload = await apiGet<WarehouseDashboardResponse>("/api/v1/warehouse/dashboard");
    return {
      data: normalizeWarehouseDashboard(payload),
      source: "api"
    };
  } catch (error) {
    return {
      data: warehouseDashboardMock,
      source: "mock",
      error: error instanceof Error ? error.message : "Warehouse API unavailable"
    };
  }
}
