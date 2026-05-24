"use client";

import { useEffect, useState } from "react";
import { workforceDashboardMock } from "@/mock/workforce";
import { getWorkforceDashboard } from "@/services/workforce-api";
import type { WorkforceDashboardData, WorkforceDataSource } from "@/types/workforce";

export type WorkforceDashboardState = {
  data: WorkforceDashboardData;
  source: WorkforceDataSource;
  isLoading: boolean;
  error?: string;
};

export function useWorkforceDashboard(): WorkforceDashboardState {
  const [state, setState] = useState<WorkforceDashboardState>({
    data: workforceDashboardMock,
    source: "mock",
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getWorkforceDashboard().then((result) => {
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
