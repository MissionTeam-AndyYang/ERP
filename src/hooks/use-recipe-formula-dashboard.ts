"use client";

import { useEffect, useState } from "react";
import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { recipeFormulaDashboardMock } from "@/mock/recipe";
import {
  emptyRecipeFormulaDashboardData,
  getRecipeFormulaDashboard,
  type RecipeFormulaDashboardQuery
} from "@/services/recipe-api";
import type { RecipeFormulaDashboardData, RecipeFormulaDataSource } from "@/types/recipe";

export type RecipeFormulaDashboardState = {
  data: RecipeFormulaDashboardData;
  source: RecipeFormulaDataSource;
  isLoading: boolean;
  error?: string;
};

export function useRecipeFormulaDashboard(
  dataSourceMode: DataSourceMode = "api",
  query: RecipeFormulaDashboardQuery = {}
): RecipeFormulaDashboardState {
  const [state, setState] = useState<RecipeFormulaDashboardState>({
    data: dataSourceMode === "mock" ? recipeFormulaDashboardMock : emptyRecipeFormulaDashboardData,
    source: dataSourceMode === "mock" ? "mock" : "api",
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getRecipeFormulaDashboard(query, dataSourceMode).then((result) => {
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
