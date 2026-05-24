import { productionDashboardMock } from "@/mock/production";
import { apiGet } from "@/services/api-client";
import type { ProductionDashboardData, ProductionDataSource } from "@/types/production";

type ProductionDashboardResponse = Partial<ProductionDashboardData>;

export type ProductionDashboardResult = {
  data: ProductionDashboardData;
  source: ProductionDataSource;
  error?: string;
};

function normalizeProductionDashboard(payload: ProductionDashboardResponse): ProductionDashboardData {
  return {
    summary: payload.summary?.length ? payload.summary : productionDashboardMock.summary,
    orders: payload.orders?.length ? payload.orders : productionDashboardMock.orders,
    weekSchedule: payload.weekSchedule?.length
      ? payload.weekSchedule
      : productionDashboardMock.weekSchedule,
    alerts: payload.alerts?.length ? payload.alerts : productionDashboardMock.alerts
  };
}

export async function getProductionDashboard(): Promise<ProductionDashboardResult> {
  try {
    const payload = await apiGet<ProductionDashboardResponse>("/api/v1/production/dashboard");
    return {
      data: normalizeProductionDashboard(payload),
      source: "api"
    };
  } catch (error) {
    return {
      data: productionDashboardMock,
      source: "mock",
      error: error instanceof Error ? error.message : "Production API unavailable"
    };
  }
}
