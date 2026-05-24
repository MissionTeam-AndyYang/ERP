"use client";

import { useEffect, useState } from "react";
import { purchasingDashboardMock } from "@/mock/purchasing";
import { getPurchasingDashboard } from "@/services/purchasing-api";
import type { PurchasingDashboardData, PurchasingDataSource } from "@/types/purchasing";

export type PurchasingDashboardState = {
  data: PurchasingDashboardData;
  source: PurchasingDataSource;
  isLoading: boolean;
  error?: string;
};

export function usePurchasingDashboard(): PurchasingDashboardState {
  const [state, setState] = useState<PurchasingDashboardState>({
    data: purchasingDashboardMock,
    source: "mock",
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getPurchasingDashboard().then((result) => {
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
