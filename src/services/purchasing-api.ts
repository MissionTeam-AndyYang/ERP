import { purchasingDashboardMock } from "@/mock/purchasing";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type { PurchasingDashboardData, PurchasingDataSource } from "@/types/purchasing";

type PurchasingDashboardResponse = Partial<PurchasingDashboardData>;

export type PurchasingDashboardResult = {
  data: PurchasingDashboardData;
  source: PurchasingDataSource;
  error?: string;
};

function normalizePurchasingDashboard(payload: PurchasingDashboardResponse): PurchasingDashboardData {
  return {
    summary: withFallbackArray(payload.summary, purchasingDashboardMock.summary),
    items: withFallbackArray(payload.items, purchasingDashboardMock.items)
  };
}

export async function getPurchasingDashboard(): Promise<PurchasingDashboardResult> {
  try {
    const payload = await apiGet<PurchasingDashboardResponse>("/api/v1/purchasing/dashboard");
    return { data: normalizePurchasingDashboard(payload), source: "api" };
  } catch (error) {
    return {
      data: purchasingDashboardMock,
      source: "mock",
      error: error instanceof Error ? error.message : "Purchasing API unavailable"
    };
  }
}
