"use client";

import { useEffect, useState } from "react";
import {
  getSupportDashboard,
  type SupportDashboardDataSource
} from "@/services/support-dashboard-api";

export type SupportDashboardState<T> = {
  data: T;
  source: SupportDashboardDataSource;
  isLoading: boolean;
  error?: string;
};

export function useSupportDashboard<T>(
  path: string,
  fallbackData: T,
  fallbackMessage: string
): SupportDashboardState<T> {
  const [state, setState] = useState<SupportDashboardState<T>>({
    data: fallbackData,
    source: "mock",
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getSupportDashboard(path, fallbackData, fallbackMessage).then((result) => {
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
  }, [fallbackData, fallbackMessage, path]);

  return state;
}
