import { logisticsDashboardMock } from "@/mock/logistics";
import { apiGet } from "@/services/api-client";
import type { LogisticsDashboardData, LogisticsDataSource } from "@/types/logistics";

type LogisticsDashboardResponse = Partial<LogisticsDashboardData>;

export type LogisticsDashboardResult = {
  data: LogisticsDashboardData;
  source: LogisticsDataSource;
  error?: string;
};

function normalizeLogisticsDashboard(payload: LogisticsDashboardResponse): LogisticsDashboardData {
  return {
    summary: payload.summary?.length ? payload.summary : logisticsDashboardMock.summary,
    shipments: payload.shipments?.length ? payload.shipments : logisticsDashboardMock.shipments
  };
}

export async function getLogisticsDashboard(): Promise<LogisticsDashboardResult> {
  try {
    const payload = await apiGet<LogisticsDashboardResponse>("/api/v1/logistics/dashboard");
    return { data: normalizeLogisticsDashboard(payload), source: "api" };
  } catch (error) {
    return {
      data: logisticsDashboardMock,
      source: "mock",
      error: error instanceof Error ? error.message : "Logistics API unavailable"
    };
  }
}
