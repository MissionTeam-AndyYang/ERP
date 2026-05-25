import { rdDashboardMock } from "@/mock/rd";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type { RdDashboardData, RdDataSource } from "@/types/rd";

type RdDashboardResponse = Partial<RdDashboardData>;

export type RdDashboardResult = {
  data: RdDashboardData;
  source: RdDataSource;
  error?: string;
};

function normalizeRdDashboard(payload: RdDashboardResponse): RdDashboardData {
  return {
    summary: withFallbackArray(payload.summary, rdDashboardMock.summary),
    projects: withFallbackArray(payload.projects, rdDashboardMock.projects)
  };
}

export async function getRdDashboard(): Promise<RdDashboardResult> {
  try {
    const payload = await apiGet<RdDashboardResponse>("/api/v1/rd/dashboard");
    return { data: normalizeRdDashboard(payload), source: "api" };
  } catch (error) {
    return {
      data: rdDashboardMock,
      source: "mock",
      error: error instanceof Error ? error.message : "R&D API unavailable"
    };
  }
}
