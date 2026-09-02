"use client";

import { useEffect, useState } from "react";
import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { traceabilityDashboardMock } from "@/mock/traceability";
import {
  emptyTraceabilityDashboardData,
  getTraceabilityDashboard,
  type TraceabilityDashboardQuery
} from "@/services/traceability-api";
import type { TraceabilityDashboardData, TraceabilityDataSource } from "@/types/traceability";

export type TraceabilityDashboardState = {
  data: TraceabilityDashboardData;
  source: TraceabilityDataSource;
  isLoading: boolean;
  error?: string;
  requestKey?: string;
};

export function useTraceabilityDashboard(
  dataSourceMode: DataSourceMode = "api",
  query: TraceabilityDashboardQuery = {}
): TraceabilityDashboardState {
  const requestKey = JSON.stringify({ dataSourceMode, query });
  const [state, setState] = useState<TraceabilityDashboardState>({
    data: dataSourceMode === "mock" ? traceabilityDashboardMock : emptyTraceabilityDashboardData,
    source: dataSourceMode === "mock" ? "mock" : "api",
    isLoading: true,
    requestKey
  });

  useEffect(() => {
    let isMounted = true;

    getTraceabilityDashboard(query, dataSourceMode).then((result) => {
      if (!isMounted) {
        return;
      }

      setState({
        data: result.data,
        source: result.source,
        isLoading: false,
        error: result.error,
        requestKey
      });
    });

    return () => {
      isMounted = false;
    };
  }, [dataSourceMode, query, requestKey]);

  return {
    ...state,
    source: dataSourceMode === "mock" ? "mock" : "api",
    isLoading: state.isLoading || state.requestKey !== requestKey
  };
}
