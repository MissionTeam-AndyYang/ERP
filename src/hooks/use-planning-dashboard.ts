"use client";

import { useEffect, useState } from "react";
import { planningDashboardMock } from "@/mock/planning";
import { getPlanningDashboard } from "@/services/planning-api";
import type { PlanningDashboardData, PlanningDataSource } from "@/types/planning";

export type PlanningDashboardState = {
  data: PlanningDashboardData;
  source: PlanningDataSource;
  isLoading: boolean;
  error?: string;
};

export function usePlanningDashboard(): PlanningDashboardState {
  const [state, setState] = useState<PlanningDashboardState>({
    data: planningDashboardMock,
    source: "mock",
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getPlanningDashboard().then((result) => {
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
