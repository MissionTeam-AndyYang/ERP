"use client";

import { useEffect, useState } from "react";
import { traceabilityDashboardMock } from "@/mock/traceability";
import { getTraceabilityDashboard } from "@/services/traceability-api";
import type { TraceabilityDashboardData, TraceabilityDataSource } from "@/types/traceability";

export type TraceabilityDashboardState = {
  data: TraceabilityDashboardData;
  source: TraceabilityDataSource;
  isLoading: boolean;
  error?: string;
};

export function useTraceabilityDashboard(): TraceabilityDashboardState {
  const [state, setState] = useState<TraceabilityDashboardState>({
    data: traceabilityDashboardMock,
    source: "mock",
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getTraceabilityDashboard().then((result) => {
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
