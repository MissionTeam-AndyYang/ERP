import { traceabilityDashboardMock } from "@/mock/traceability";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type { TraceabilityDashboardData, TraceabilityDataSource } from "@/types/traceability";

type TraceabilityDashboardResponse = Partial<TraceabilityDashboardData>;

export type TraceabilityDashboardResult = {
  data: TraceabilityDashboardData;
  source: TraceabilityDataSource;
  error?: string;
};

function normalizeTraceabilityDashboard(payload: TraceabilityDashboardResponse): TraceabilityDashboardData {
  return {
    summary: withFallbackArray(payload.summary, traceabilityDashboardMock.summary),
    records: withFallbackArray(payload.records, traceabilityDashboardMock.records)
  };
}

export async function getTraceabilityDashboard(): Promise<TraceabilityDashboardResult> {
  try {
    const payload = await apiGet<TraceabilityDashboardResponse>("/api/v1/traceability/dashboard");
    return { data: normalizeTraceabilityDashboard(payload), source: "api" };
  } catch (error) {
    return {
      data: traceabilityDashboardMock,
      source: "mock",
      error: error instanceof Error ? error.message : "Traceability API unavailable"
    };
  }
}
