"use client";

import { useEffect, useState } from "react";
import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { productionDashboardMock } from "@/mock/production";
import {
  emptyProductionDashboardData,
  getProductionDashboard,
  normalizeProductionDashboardData
} from "@/services/production-api";
import type { ProductionDashboardQuery } from "@/services/production-api";
import type { ProductionDashboardData, ProductionDataSource } from "@/types/production";

export type ProductionDashboardState = {
  data: ProductionDashboardData;
  source: ProductionDataSource;
  isLoading: boolean;
  error?: string;
};

export function useProductionDashboard(
  dataSourceMode: DataSourceMode = "api",
  query: ProductionDashboardQuery = {}
): ProductionDashboardState {
  const [state, setState] = useState<ProductionDashboardState>({
    data:
      dataSourceMode === "mock"
        ? normalizeProductionDashboardData(productionDashboardMock)
        : emptyProductionDashboardData,
    source: dataSourceMode === "mock" ? "mock" : "api",
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getProductionDashboard(query, dataSourceMode).then((result) => {
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
  }, [dataSourceMode, query]);

  return state;
}
