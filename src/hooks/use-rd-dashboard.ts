"use client";

import { useEffect, useState } from "react";
import { rdDashboardMock } from "@/mock/rd";
import { getRdDashboard } from "@/services/rd-api";
import type { RdDashboardData, RdDataSource } from "@/types/rd";

export type RdDashboardState = {
  data: RdDashboardData;
  source: RdDataSource;
  isLoading: boolean;
  error?: string;
};

export function useRdDashboard(): RdDashboardState {
  const [state, setState] = useState<RdDashboardState>({
    data: rdDashboardMock,
    source: "mock",
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getRdDashboard().then((result) => {
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
