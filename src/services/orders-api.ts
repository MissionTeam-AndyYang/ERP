import { ordersDashboardMock } from "@/mock/orders";
import { apiGet } from "@/services/api-client";
import type { OrdersDashboardData, OrdersDataSource } from "@/types/orders";

type OrdersDashboardResponse = Partial<OrdersDashboardData>;

export type OrdersDashboardResult = {
  data: OrdersDashboardData;
  source: OrdersDataSource;
  error?: string;
};

function normalizeOrdersDashboard(payload: OrdersDashboardResponse): OrdersDashboardData {
  return {
    summary: payload.summary?.length ? payload.summary : ordersDashboardMock.summary,
    orders: payload.orders?.length ? payload.orders : ordersDashboardMock.orders
  };
}

export async function getOrdersDashboard(): Promise<OrdersDashboardResult> {
  try {
    const payload = await apiGet<OrdersDashboardResponse>("/api/v1/orders/dashboard");
    return {
      data: normalizeOrdersDashboard(payload),
      source: "api"
    };
  } catch (error) {
    return {
      data: ordersDashboardMock,
      source: "mock",
      error: error instanceof Error ? error.message : "Orders API unavailable"
    };
  }
}
