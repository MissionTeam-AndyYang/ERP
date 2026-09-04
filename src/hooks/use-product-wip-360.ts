"use client";

import { useEffect, useState } from "react";
import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { emptyProductWip360OverviewData, getProductWip360Overview } from "@/services/product-wip-360-api";
import type { ProductWip360DataSource, ProductWip360OverviewData, ProductWip360Query } from "@/types/product-wip-360";

export type ProductWip360State = {
  data: ProductWip360OverviewData;
  source: ProductWip360DataSource;
  isLoading: boolean;
  error?: string;
};

export function useProductWip360Overview(query: ProductWip360Query, dataSourceMode: DataSourceMode = "api"): ProductWip360State {
  const [state, setState] = useState<ProductWip360State>({
    data: dataSourceMode === "mock" ? emptyProductWip360OverviewData : { ...emptyProductWip360OverviewData, requestIdentity: query },
    source: dataSourceMode,
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getProductWip360Overview(query, dataSourceMode).then((result) => {
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
