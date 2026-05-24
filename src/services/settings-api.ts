import { settingsDashboardMock } from "@/mock/settings";
import { apiGet } from "@/services/api-client";
import type { SettingsDashboardData, SettingsDataSource } from "@/types/settings";

type SettingsDashboardResponse = Partial<SettingsDashboardData>;

export type SettingsDashboardResult = {
  data: SettingsDashboardData;
  source: SettingsDataSource;
  error?: string;
};

function normalizeSettingsDashboard(payload: SettingsDashboardResponse): SettingsDashboardData {
  return {
    summary: payload.summary?.length ? payload.summary : settingsDashboardMock.summary,
    items: payload.items?.length ? payload.items : settingsDashboardMock.items
  };
}

export async function getSettingsDashboard(): Promise<SettingsDashboardResult> {
  try {
    const payload = await apiGet<SettingsDashboardResponse>("/api/v1/settings/dashboard");
    return { data: normalizeSettingsDashboard(payload), source: "api" };
  } catch (error) {
    return {
      data: settingsDashboardMock,
      source: "mock",
      error: error instanceof Error ? error.message : "Settings API unavailable"
    };
  }
}
