"use client";

import { useEffect, useState } from "react";
import { warehouseDashboardMock } from "@/mock/warehouse";
import { getWarehouseDashboard } from "@/services/warehouse-api";
import type { WarehouseDashboardData, WarehouseDataSource } from "@/types/warehouse";

export type WarehouseDashboardState = {
  data: WarehouseDashboardData;
  source: WarehouseDataSource;
  isLoading: boolean;
  error?: string;
};

export function useWarehouseDashboard(): WarehouseDashboardState {
  const [state, setState] = useState<WarehouseDashboardState>({
    data: warehouseDashboardMock,
    source: "mock",
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getWarehouseDashboard().then((result) => {
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
