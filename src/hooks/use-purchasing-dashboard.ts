"use client";

import { useEffect, useState } from "react";
import type { DataSourceMode } from "@/components/common/data-source-toggle";
import {
  emptyPurchasingDashboardData,
  getPurchasingDashboard,
  normalizePurchasingDashboardData,
  type PurchasingDashboardQuery
} from "@/services/purchasing-api";
import { purchasingDashboardMock } from "@/mock/purchasing";
import type { PurchasingDashboardData, PurchasingDataSource } from "@/types/purchasing";

export type PurchasingDashboardState = {
  data: PurchasingDashboardData;
  source: PurchasingDataSource;
  isLoading: boolean;
  error?: string;
};

export function usePurchasingDashboard(
  dataSourceMode: DataSourceMode = "api",
  query: PurchasingDashboardQuery
): PurchasingDashboardState {
  const [state, setState] = useState<PurchasingDashboardState>({
    data:
      dataSourceMode === "mock"
        ? normalizePurchasingDashboardData(purchasingDashboardMock)
        : emptyPurchasingDashboardData,
    source: dataSourceMode === "mock" ? "mock" : "api",
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getPurchasingDashboard(query, dataSourceMode).then((result) => {
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
