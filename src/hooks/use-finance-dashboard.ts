"use client";

import { useEffect, useState } from "react";
import { financeDashboardMock } from "@/mock/finance";
import { getFinanceDashboard } from "@/services/finance-api";
import type { FinanceDashboardData, FinanceDataSource } from "@/types/finance";

export type FinanceDashboardState = {
  data: FinanceDashboardData;
  source: FinanceDataSource;
  isLoading: boolean;
  error?: string;
};

export function useFinanceDashboard(): FinanceDashboardState {
  const [state, setState] = useState<FinanceDashboardState>({
    data: financeDashboardMock,
    source: "mock",
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getFinanceDashboard().then((result) => {
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
