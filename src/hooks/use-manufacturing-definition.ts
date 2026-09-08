"use client";

import { useEffect, useState } from "react";
import type { DataSourceMode } from "@/components/common/data-source-toggle";
import type { LanguageCode } from "@/i18n/dictionary";
import { emptyManufacturingDefinitionData, getManufacturingDefinitionOverview } from "@/services/manufacturing-definition-api";
import type {
  ManufacturingDefinitionData,
  ManufacturingDefinitionDataSource,
  ManufacturingDefinitionQuery
} from "@/types/manufacturing-definition";

export type ManufacturingDefinitionState = {
  data: ManufacturingDefinitionData;
  source: ManufacturingDefinitionDataSource;
  isLoading: boolean;
  error?: string;
};

export function useManufacturingDefinitionOverview(
  query: ManufacturingDefinitionQuery,
  dataSourceMode: DataSourceMode = "api",
  language: LanguageCode = "zh-TW"
): ManufacturingDefinitionState {
  const queryKey = JSON.stringify({ dataSourceMode, language, query });
  const [state, setState] = useState<ManufacturingDefinitionState>({
    data: { ...emptyManufacturingDefinitionData, requestIdentity: query },
    source: dataSourceMode,
    isLoading: true
  });
  const [loadedQueryKey, setLoadedQueryKey] = useState("");

  useEffect(() => {
    let isMounted = true;

    getManufacturingDefinitionOverview(query, dataSourceMode, language).then((result) => {
      if (!isMounted) {
        return;
      }
      setState({
        data: result.data,
        source: result.source,
        isLoading: false,
        error: result.error
      });
      setLoadedQueryKey(queryKey);
    });

    return () => {
      isMounted = false;
    };
  }, [dataSourceMode, language, query, queryKey]);

  return { ...state, isLoading: state.isLoading || loadedQueryKey !== queryKey };
}
