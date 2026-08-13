"use client";

import { useEffect, useState } from "react";
import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { bomDashboardMock } from "@/mock/bom";
import { emptyBomDashboardData, getBomDashboard, type BomDashboardQuery } from "@/services/bom-api";
import type { BomDashboardData, BomDataSource } from "@/types/bom";

export type BomDashboardState = {
  data: BomDashboardData;
  source: BomDataSource;
  isLoading: boolean;
  error?: string;
};

export function useBomDashboard(
  dataSourceMode: DataSourceMode = "api",
  query: BomDashboardQuery = {}
): BomDashboardState {
  const [state, setState] = useState<BomDashboardState>({
    data: dataSourceMode === "mock" ? bomDashboardMock : emptyBomDashboardData,
    source: dataSourceMode === "mock" ? "mock" : "api",
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getBomDashboard(query, dataSourceMode).then((result) => {
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
  }, [dataSourceMode, query]);

  return state;
}
