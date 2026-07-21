"use client";

import { useEffect, useState } from "react";
import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { productionDashboardMock } from "@/mock/production";
import { getProductionDashboard, normalizeProductionDashboardData } from "@/services/production-api";
import type { ProductionDashboardData, ProductionDataSource } from "@/types/production";

export type ProductionDashboardState = {
  data: ProductionDashboardData;
  source: ProductionDataSource;
  isLoading: boolean;
  error?: string;
};

export function useProductionDashboard(dataSourceMode: DataSourceMode = "api"): ProductionDashboardState {
  const [state, setState] = useState<ProductionDashboardState>({
    data: normalizeProductionDashboardData(productionDashboardMock),
    source: "mock",
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getProductionDashboard({}, dataSourceMode).then((result) => {
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
  }, [dataSourceMode]);

  return state;
}
