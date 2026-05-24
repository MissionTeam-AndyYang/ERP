"use client";

import { useEffect, useState } from "react";
import { logisticsDashboardMock } from "@/mock/logistics";
import { getLogisticsDashboard } from "@/services/logistics-api";
import type { LogisticsDashboardData, LogisticsDataSource } from "@/types/logistics";

export type LogisticsDashboardState = {
  data: LogisticsDashboardData;
  source: LogisticsDataSource;
  isLoading: boolean;
  error?: string;
};

export function useLogisticsDashboard(): LogisticsDashboardState {
  const [state, setState] = useState<LogisticsDashboardState>({
    data: logisticsDashboardMock,
    source: "mock",
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getLogisticsDashboard().then((result) => {
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
