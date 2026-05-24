"use client";

import { useEffect, useState } from "react";
import { settingsDashboardMock } from "@/mock/settings";
import { getSettingsDashboard } from "@/services/settings-api";
import type { SettingsDashboardData, SettingsDataSource } from "@/types/settings";

export type SettingsDashboardState = {
  data: SettingsDashboardData;
  source: SettingsDataSource;
  isLoading: boolean;
  error?: string;
};

export function useSettingsDashboard(): SettingsDashboardState {
  const [state, setState] = useState<SettingsDashboardState>({
    data: settingsDashboardMock,
    source: "mock",
    isLoading: true
  });

  useEffect(() => {
    let isMounted = true;

    getSettingsDashboard().then((result) => {
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
