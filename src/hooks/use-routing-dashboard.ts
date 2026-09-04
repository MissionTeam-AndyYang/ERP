"use client";

import { useEffect, useState } from "react";
import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { routingDashboardMock } from "@/mock/routing";
import { emptyRoutingDashboardData, getRoutingDashboard, type RoutingDashboardQuery } from "@/services/routing-api";
import type { RoutingDashboardData, RoutingDataSource } from "@/types/routing";

export type RoutingDashboardState = {
  data: RoutingDashboardData;
  source: RoutingDataSource;
  isLoading: boolean;
  error?: string;
};

export function useRoutingDashboard(dataSourceMode: DataSourceMode = "api", query: RoutingDashboardQuery = {}): RoutingDashboardState {
  const [state, setState] = useState<RoutingDashboardState>({
    data: dataSourceMode === "mock" ? routingDashboardMock : emptyRoutingDashboardData,
    source: dataSourceMode,
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getRoutingDashboard(query, dataSourceMode).then((result) => {
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
