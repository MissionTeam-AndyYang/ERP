import {
  Activity,
  AlertTriangle,
  BadgeCheck,
  Factory,
  PackageCheck
} from "lucide-react";
import type {
  AlertDistributionItem,
  AlertItem,
  KpiItem,
  OeeTrendPoint,
  ProductionLine,
  ProductionTrendPoint,
  QualityTrendPoint
} from "@/types/dashboard";

export const kpiItems: KpiItem[] = [
  {
    title: "今日產量",
    value: "18,420",
    unit: "盒",
    trend: "+12.4% vs 昨日",
    tone: "success",
    icon: PackageCheck
  },
  {
    title: "平均良率",
    value: "98.6",
    unit: "%",
    trend: "+0.8% 本週",
    tone: "success",
    icon: BadgeCheck
  },
  {
    title: "OEE",
    value: "86.3",
    unit: "%",
    trend: "接近目標 88%",
    tone: "info",
    icon: Activity
  },
  {
    title: "異常事件",
    value: "3",
    unit: "件",
    trend: "1 件待處理",
    tone: "warning",
    icon: AlertTriangle
  }
];

export const productionLines: ProductionLine[] = [
  {
    line: "A1 調理包產線",
    product: "咖哩雞肉調理包",
    batchNo: "B240512-A101",
    status: "生產中",
    tone: "success",
    progress: 72,
    yieldRate: "99.1%",
    eta: "14:30 完工"
  },
  {
    line: "B2 冷凍蔬菜產線",
    product: "綜合冷凍蔬菜",
    batchNo: "B240512-B207",
    status: "待料",
    tone: "warning",
    progress: 38,
    yieldRate: "97.4%",
    eta: "等待玉米粒入線"
  },
  {
    line: "C3 包裝產線",
    product: "即食雞胸肉",
    batchNo: "B240512-C315",
    status: "清洗中",
    tone: "info",
    progress: 18,
    yieldRate: "98.0%",
    eta: "15:10 重新開線"
  }
];

export const alertItems: AlertItem[] = [
  {
    title: "B2 產線原料不足",
    detail: "玉米粒庫存低於安全量，需補料 240 kg。",
    time: "10 分鐘前",
    tone: "warning"
  },
  {
    title: "A1 金檢通過率下降",
    detail: "近 30 分鐘重檢率上升，建議品保確認。",
    time: "22 分鐘前",
    tone: "danger"
  },
  {
    title: "冷藏庫溫度回穩",
    detail: "2 號冷藏庫已回到 3.8°C，持續觀察。",
    time: "45 分鐘前",
    tone: "success"
  }
];

export const lineSummary = {
  active: 6,
  idle: 1,
  cleaning: 2,
  icon: Factory
};

export const productionTrendData: ProductionTrendPoint[] = [
  { time: "08:00", planned: 1800, actual: 1720 },
  { time: "09:00", planned: 3600, actual: 3510 },
  { time: "10:00", planned: 5400, actual: 5360 },
  { time: "11:00", planned: 7200, actual: 7480 },
  { time: "12:00", planned: 9000, actual: 9120 },
  { time: "13:00", planned: 10800, actual: 11160 },
  { time: "14:00", planned: 12600, actual: 13140 }
];

export const oeeTrendData: OeeTrendPoint[] = [
  { time: "08:00", oee: 78, target: 88 },
  { time: "09:00", oee: 82, target: 88 },
  { time: "10:00", oee: 85, target: 88 },
  { time: "11:00", oee: 87, target: 88 },
  { time: "12:00", oee: 84, target: 88 },
  { time: "13:00", oee: 86, target: 88 },
  { time: "14:00", oee: 89, target: 88 }
];

export const qualityTrendData: QualityTrendPoint[] = [
  { date: "05/06", yieldRate: 97.8, reworkRate: 1.5 },
  { date: "05/07", yieldRate: 98.1, reworkRate: 1.3 },
  { date: "05/08", yieldRate: 98.4, reworkRate: 1.1 },
  { date: "05/09", yieldRate: 97.9, reworkRate: 1.6 },
  { date: "05/10", yieldRate: 98.5, reworkRate: 1.0 },
  { date: "05/11", yieldRate: 98.2, reworkRate: 1.2 },
  { date: "05/12", yieldRate: 98.6, reworkRate: 0.9 }
];

export const alertDistributionData: AlertDistributionItem[] = [
  { name: "缺料", value: 42, tone: "warning" },
  { name: "設備", value: 24, tone: "danger" },
  { name: "品保", value: 19, tone: "info" },
  { name: "庫溫", value: 15, tone: "success" }
];
