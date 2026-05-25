import { warehouseDashboardMock } from "@/mock/warehouse";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type { WarehouseDashboardData, WarehouseDataSource } from "@/types/warehouse";

type WarehouseDashboardResponse = Partial<WarehouseDashboardData>;

export type WarehouseDashboardResult = {
  data: WarehouseDashboardData;
  source: WarehouseDataSource;
  error?: string;
};

function normalizeWarehouseDashboard(payload: WarehouseDashboardResponse): WarehouseDashboardData {
  return {
    kpis: withFallbackArray(payload.kpis, warehouseDashboardMock.kpis),
    categorySummaries: withFallbackArray(payload.categorySummaries, warehouseDashboardMock.categorySummaries),
    capacities: withFallbackArray(payload.capacities, warehouseDashboardMock.capacities),
    records: withFallbackArray(payload.records, warehouseDashboardMock.records),
    risks: withFallbackArray(payload.risks, warehouseDashboardMock.risks),
    tasks: withFallbackArray(payload.tasks, warehouseDashboardMock.tasks)
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
