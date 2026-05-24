import { apiGet } from "@/services/api-client";

export type SupportDashboardDataSource = "api" | "mock";

export type SupportDashboardResult<T> = {
  data: T;
  source: SupportDashboardDataSource;
  error?: string;
};

export async function getSupportDashboard<T>(
  path: string,
  fallbackData: T,
  fallbackMessage: string
): Promise<SupportDashboardResult<T>> {
  try {
    const payload = await apiGet<Partial<T>>(path);
    return { data: { ...fallbackData, ...payload }, source: "api" };
  } catch (error) {
    return {
      data: fallbackData,
      source: "mock",
      error: error instanceof Error ? error.message : fallbackMessage
    };
  }
}
