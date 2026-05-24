"use client";

import { useEffect, useState } from "react";
import { ordersDashboardMock } from "@/mock/orders";
import { getOrdersDashboard } from "@/services/orders-api";
import type { OrdersDashboardData, OrdersDataSource } from "@/types/orders";

export type OrdersDashboardState = {
  data: OrdersDashboardData;
  source: OrdersDataSource;
  isLoading: boolean;
  error?: string;
};

export function useOrdersDashboard(): OrdersDashboardState {
  const [state, setState] = useState<OrdersDashboardState>({
    data: ordersDashboardMock,
    source: "mock",
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getOrdersDashboard().then((result) => {
      if (!isMounted) {
        return;
      }

      setState({
        data: result.data,
        source: result.source,
        isLoading: false,
        error: result.error
      });
    });

    return () => {
      isMounted = false;
    };
  }, []);

  return state;
}
