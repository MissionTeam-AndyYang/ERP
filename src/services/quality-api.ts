import { qualityDashboardMock } from "@/mock/quality";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type { QualityDashboardData, QualityDataSource } from "@/types/quality";

type QualityDashboardResponse = Partial<QualityDashboardData>;

export type QualityDashboardResult = {
  data: QualityDashboardData;
  source: QualityDataSource;
  error?: string;
};

function normalizeQualityDashboard(payload: QualityDashboardResponse): QualityDashboardData {
  return {
    summary: withFallbackArray(payload.summary, qualityDashboardMock.summary),
    inspections: withFallbackArray(payload.inspections, qualityDashboardMock.inspections)
  };
}

export async function getQualityDashboard(): Promise<QualityDashboardResult> {
  try {
    const payload = await apiGet<QualityDashboardResponse>("/api/v1/quality/dashboard");
    return {
      data: normalizeQualityDashboard(payload),
      source: "api"
    };
  } catch (error) {
    return {
      data: qualityDashboardMock,
      source: "mock",
      error: error instanceof Error ? error.message : "Quality API unavailable"
    };
  }
}
