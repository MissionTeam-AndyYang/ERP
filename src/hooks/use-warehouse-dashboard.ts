"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { warehouseDashboardMock } from "@/mock/warehouse";
import { getWarehouseDashboard, getWarehouseInventory, getWarehouseTasks } from "@/services/warehouse-api";
import type { WarehouseDashboardData, WarehouseDataSource } from "@/types/warehouse";

export type WarehouseDashboardState = {
  data: WarehouseDashboardData;
  source: WarehouseDataSource;
  isLoading: boolean;
  isInventoryLoading: boolean;
  error?: string;
  loadInventory: () => Promise<void>;
  loadTasks: () => Promise<void>;
};

type WarehouseDashboardInternalState = Omit<WarehouseDashboardState, "loadInventory" | "loadTasks">;

export function useWarehouseDashboard(dataSourceMode: DataSourceMode = "api"): WarehouseDashboardState {
  const [state, setState] = useState<WarehouseDashboardInternalState>({
    data: warehouseDashboardMock,
    source: "mock",
    isLoading: true,
    isInventoryLoading: false
  });
  const inventoryLoadedRef = useRef(false);
  const tasksLoadedRef = useRef(false);

  const loadInventory = useCallback(async () => {
    if (inventoryLoadedRef.current) {
      return;
    }

    setState((current) => ({
      ...current,
      isInventoryLoading: true
    }));

    const result = await getWarehouseInventory(dataSourceMode);
    inventoryLoadedRef.current = true;
    setState((current) => ({
      ...current,
      isInventoryLoading: false,
      data: {
        ...current.data,
        records: result.records
      },
      source: current.source === "api" ? current.source : result.source,
      error: result.error ?? current.error
    }));
  }, [dataSourceMode]);

  const loadTasks = useCallback(async () => {
    if (tasksLoadedRef.current) {
      return;
    }

    const result = await getWarehouseTasks(dataSourceMode);
    tasksLoadedRef.current = true;
    setState((current) => ({
      ...current,
      data: {
        ...current.data,
        tasks: result.tasks
      },
      source: current.source === "api" ? current.source : result.source,
      error: result.error ?? current.error
    }));
  }, [dataSourceMode]);

  useEffect(() => {
    let isMounted = true;

    inventoryLoadedRef.current = false;
    tasksLoadedRef.current = false;

    getWarehouseDashboard(dataSourceMode).then((result) => {
      if (!isMounted) {
        return;
      }

      setState({
        data: result.data,
        source: result.source,
        isLoading: false,
        isInventoryLoading: false,
        error: result.error
      });
    });

    return () => {
      isMounted = false;
    };
  }, [dataSourceMode]);

  return {
    ...state,
    loadInventory,
    loadTasks
  };
}
