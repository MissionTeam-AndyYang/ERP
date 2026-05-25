import { financeDashboardMock } from "@/mock/finance";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type { FinanceDashboardData, FinanceDataSource } from "@/types/finance";

type FinanceDashboardResponse = Partial<FinanceDashboardData>;

export type FinanceDashboardResult = {
  data: FinanceDashboardData;
  source: FinanceDataSource;
  error?: string;
};

function normalizeFinanceDashboard(payload: FinanceDashboardResponse): FinanceDashboardData {
  return {
    summary: withFallbackArray(payload.summary, financeDashboardMock.summary),
    cases: withFallbackArray(payload.cases, financeDashboardMock.cases)
  };
}

export async function getFinanceDashboard(): Promise<FinanceDashboardResult> {
  try {
    const payload = await apiGet<FinanceDashboardResponse>("/api/v1/finance/dashboard");
    return { data: normalizeFinanceDashboard(payload), source: "api" };
  } catch (error) {
    return {
      data: financeDashboardMock,
      source: "mock",
      error: error instanceof Error ? error.message : "Finance API unavailable"
    };
  }
}
