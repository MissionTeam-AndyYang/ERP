import type { LucideIcon } from "lucide-react";

export type StatusTone = "success" | "warning" | "danger" | "info" | "neutral";

export type KpiItem = {
  title: string;
  value: string;
  unit: string;
  trend: string;
  tone: StatusTone;
  icon: LucideIcon;
};

export type AlertItem = {
  title: string;
  detail: string;
  time: string;
  tone: StatusTone;
};

export type ProductionLine = {
  line: string;
  product: string;
  batchNo: string;
  status: string;
  tone: StatusTone;
  progress: number;
  yieldRate: string;
  eta: string;
};

export type ProductionTrendPoint = {
  time: string;
  planned: number;
  actual: number;
};

export type OeeTrendPoint = {
  time: string;
  oee: number;
  target: number;
};

export type QualityTrendPoint = {
  date: string;
  yieldRate: number;
  reworkRate: number;
};

export type AlertDistributionItem = {
  name: string;
  value: number;
  tone: StatusTone;
};
