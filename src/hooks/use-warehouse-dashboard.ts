"use client";

import { useCallback, useEffect, useState } from "react";
import { warehouseDashboardMock } from "@/mock/warehouse";
import { getWarehouseDashboard, getWarehouseInventory, getWarehouseTasks } from "@/services/warehouse-api";
import type { WarehouseDashboardData, WarehouseDataSource } from "@/types/warehouse";

export type WarehouseDashboardState = {
  data: WarehouseDashboardData;
  source: WarehouseDataSource;
  isLoading: boolean;
  error?: string;
  loadInventory: () => Promise<void>;
  loadTasks: () => Promise<void>;
};

type WarehouseDashboardInternalState = Omit<WarehouseDashboardState, "loadInventory" | "loadTasks">;

export function useWarehouseDashboard(): WarehouseDashboardState {
  const [state, setState] = useState<WarehouseDashboardInternalState>({
    data: warehouseDashboardMock,
    source: "mock",
    isLoading: true
  });
  const [inventoryLoaded, setInventoryLoaded] = useState(false);
  const [tasksLoaded, setTasksLoaded] = useState(false);

  const loadInventory = useCallback(async () => {
    if (inventoryLoaded) {
      return;
    }

    const result = await getWarehouseInventory();
    setInventoryLoaded(true);
    setState((current) => ({
      ...current,
      data: {
        ...current.data,
        records: result.records
      },
      source: current.source === "api" ? current.source : result.source,
      error: result.error ?? current.error
    }));
  }, [inventoryLoaded]);

  const loadTasks = useCallback(async () => {
    if (tasksLoaded) {
      return;
    }

    const result = await getWarehouseTasks();
    setTasksLoaded(true);
    setState((current) => ({
      ...current,
      data: {
        ...current.data,
        tasks: result.tasks
      },
      source: current.source === "api" ? current.source : result.source,
      error: result.error ?? current.error
    }));
  }, [tasksLoaded]);

  useEffect(() => {
    let isMounted = true;

    getWarehouseDashboard().then((result) => {
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

  return {
    ...state,
    loadInventory,
    loadTasks
  };
}
