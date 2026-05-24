import { planningDashboardMock } from "@/mock/planning";
import { apiGet } from "@/services/api-client";
import type { PlanningDashboardData, PlanningDataSource } from "@/types/planning";

type PlanningDashboardResponse = Partial<PlanningDashboardData>;

export type PlanningDashboardResult = {
  data: PlanningDashboardData;
  source: PlanningDataSource;
  error?: string;
};

function normalizePlanningDashboard(payload: PlanningDashboardResponse): PlanningDashboardData {
  return {
    summary: payload.summary?.length ? payload.summary : planningDashboardMock.summary,
    cases: payload.cases?.length ? payload.cases : planningDashboardMock.cases
  };
}

export async function getPlanningDashboard(): Promise<PlanningDashboardResult> {
  try {
    const payload = await apiGet<PlanningDashboardResponse>("/api/v1/planning/dashboard");
    return { data: normalizePlanningDashboard(payload), source: "api" };
  } catch (error) {
    return {
      data: planningDashboardMock,
      source: "mock",
      error: error instanceof Error ? error.message : "Planning API unavailable"
    };
  }
}
