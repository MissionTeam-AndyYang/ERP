import { workforceDashboardMock } from "@/mock/workforce";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type { WorkforceDashboardData, WorkforceDataSource } from "@/types/workforce";

type WorkforceDashboardResponse = Partial<WorkforceDashboardData>;

export type WorkforceDashboardResult = {
  data: WorkforceDashboardData;
  source: WorkforceDataSource;
  error?: string;
};

function normalizeWorkforceDashboard(payload: WorkforceDashboardResponse): WorkforceDashboardData {
  return {
    summary: withFallbackArray(payload.summary, workforceDashboardMock.summary),
    cases: withFallbackArray(payload.cases, workforceDashboardMock.cases)
  };
}

export async function getWorkforceDashboard(): Promise<WorkforceDashboardResult> {
  try {
    const payload = await apiGet<WorkforceDashboardResponse>("/api/v1/workforce/dashboard");
    return { data: normalizeWorkforceDashboard(payload), source: "api" };
  } catch (error) {
    return {
      data: workforceDashboardMock,
      source: "mock",
      error: error instanceof Error ? error.message : "Workforce API unavailable"
    };
  }
}
