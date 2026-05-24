"use client";

import { useEffect, useState } from "react";
import { dashboardMock } from "@/mock/dashboard";
import { getDashboard } from "@/services/dashboard-api";
import type { DashboardData, DashboardDataSource } from "@/types/dashboard";

export type DashboardState = {
  data: DashboardData;
  source: DashboardDataSource;
  isLoading: boolean;
  error?: string;
};

export function useDashboard(): DashboardState {
  const [state, setState] = useState<DashboardState>({
    data: dashboardMock,
    source: "mock",
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getDashboard().then((result) => {
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
