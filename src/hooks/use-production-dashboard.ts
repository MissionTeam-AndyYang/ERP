"use client";

import { useEffect, useState } from "react";
import { productionDashboardMock } from "@/mock/production";
import { getProductionDashboard } from "@/services/production-api";
import type { ProductionDashboardData, ProductionDataSource } from "@/types/production";

export type ProductionDashboardState = {
  data: ProductionDashboardData;
  source: ProductionDataSource;
  isLoading: boolean;
  error?: string;
};

export function useProductionDashboard(): ProductionDashboardState {
  const [state, setState] = useState<ProductionDashboardState>({
    data: productionDashboardMock,
    source: "mock",
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getProductionDashboard().then((result) => {
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
