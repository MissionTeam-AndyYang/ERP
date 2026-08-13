import type { StatusTone } from "@/types/dashboard";
import { StatusBadge } from "@/components/ui/status-badge";

type DataSourceStatusBadgeProps = {
  source: "api" | "mock";
  isLoading?: boolean;
  hasError?: boolean;
};

function dataSourceStatus(source: "api" | "mock", isLoading = false, hasError = false): { label: string; tone: StatusTone } {
  if (isLoading) {
    return { label: "資料載入中", tone: "info" };
  }

  if (source === "mock") {
    return { label: "預覽資料", tone: "warning" };
  }

  if (hasError) {
    return { label: "API 錯誤", tone: "danger" };
  }

  return { label: "後端 API", tone: "success" };
}

export function DataSourceStatusBadge({ source, isLoading = false, hasError = false }: DataSourceStatusBadgeProps) {
  const status = dataSourceStatus(source, isLoading, hasError);
  return <StatusBadge tone={status.tone}>{status.label}</StatusBadge>;
}
