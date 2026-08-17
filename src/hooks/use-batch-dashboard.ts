"use client";

import { useEffect, useState } from "react";
import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { batchesDashboardMock } from "@/mock/batches";
import { emptyBatchDashboardData, getBatchDashboard, type BatchDashboardQuery } from "@/services/batches-api";
import type { BatchDashboardData, BatchDataSource } from "@/types/batches";

export type BatchDashboardState = {
  data: BatchDashboardData;
  source: BatchDataSource;
  isLoading: boolean;
  error?: string;
};

export function useBatchDashboard(
  dataSourceMode: DataSourceMode = "api",
  query: BatchDashboardQuery = {}
): BatchDashboardState {
  const [state, setState] = useState<BatchDashboardState>({
    data: dataSourceMode === "mock" ? batchesDashboardMock : emptyBatchDashboardData,
    source: dataSourceMode === "mock" ? "mock" : "api",
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getBatchDashboard(query, dataSourceMode).then((result) => {
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
