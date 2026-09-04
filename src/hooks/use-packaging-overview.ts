"use client";

import { useEffect, useState } from "react";
import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { emptyPackagingOverviewData, getPackagingOverview } from "@/services/packaging-api";
import type { PackagingDataSource, PackagingOverviewData, PackagingQuery } from "@/types/packaging";

export type PackagingOverviewState = {
  data: PackagingOverviewData;
  source: PackagingDataSource;
  isLoading: boolean;
  error?: string;
};

export function usePackagingOverview(query: PackagingQuery, dataSourceMode: DataSourceMode = "api"): PackagingOverviewState {
  const [state, setState] = useState<PackagingOverviewState>({
    data: {
      ...emptyPackagingOverviewData,
      requestIdentity: query
    },
    source: dataSourceMode,
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getPackagingOverview(query, dataSourceMode).then((result) => {
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
