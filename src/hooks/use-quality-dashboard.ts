"use client";

import { useEffect, useState } from "react";
import { qualityDashboardMock } from "@/mock/quality";
import { getQualityDashboard } from "@/services/quality-api";
import type { QualityDashboardData, QualityDataSource } from "@/types/quality";

export type QualityDashboardState = {
  data: QualityDashboardData;
  source: QualityDataSource;
  isLoading: boolean;
  error?: string;
};

export function useQualityDashboard(): QualityDashboardState {
  const [state, setState] = useState<QualityDashboardState>({
    data: qualityDashboardMock,
    source: "mock",
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getQualityDashboard().then((result) => {
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
