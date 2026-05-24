import {
  AlertTriangle,
  BadgeCheck,
  CalendarClock,
  ClipboardCheck,
  DollarSign,
  Factory,
  PackageCheck,
  PackageSearch,
  Route,
  ShieldCheck,
  ShoppingCart,
  TimerReset,
  Truck,
  Warehouse
} from "lucide-react";
import type {
  AlertDistributionItem,
  AlertItem,
  DashboardData,
  DepartmentBlocker,
  KpiItem,
  ManagerDecisionItem,
  ManagerFocusItem,
  ManagerSnapshot,
  OeeTrendPoint,
  PreOrderPipelineItem,
  ProductionLine,
  ProductionTrendPoint,
  QualityTrendPoint,
  TodayTask
} from "@/types/dashboard";

export const managerSnapshot: ManagerSnapshot = {
  fulfillmentRisk: "3",
  deliveryCommitment: "92%",
  marginSignal: "18.6%",
  cashSignal: "NT$4.2M"
};

export const managerFocusItems: ManagerFocusItem[] = [
  {
    label: "履約風險",
    value: "3",
    detail: "2 張訂單受缺料影響，1 張待品保放行",
    tone: "danger",
    icon: AlertTriangle
  },
  {
    label: "今日交付承諾",
    value: "92",
    detail: "12 張今日應交訂單，11 張可準時出貨",
    tone: "warning",
    icon: Route
  },
  {
    label: "預估毛利",
    value: "18.6",
    detail: "本週接單毛利高於底線 2.1%",
    tone: "success",
    icon: DollarSign
  },
  {
    label: "主管待決策",
    value: "5",
    detail: "採購替代料、急單插單、倉位調度需確認",
    tone: "info",
    icon: ClipboardCheck
  }
];

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
    title: "待採購料品",
    value: "7",
    unit: "項",
    trend: "3 項會影響 7 日內排程",
    tone: "warning",
    icon: ShoppingCart
  },
  {
    title: "倉位可用板數",
    value: "186",
    unit: "板",
    trend: "冷凍庫剩餘 22 板需控管",
    tone: "info",
    icon: Warehouse
  }
];

export const managerDecisionItems: ManagerDecisionItem[] = [
  {
    title: "急單 SO-240523-018 是否插入 A2 線",
    owner: "生管",
    due: "今日 11:30",
    impact: "若插單，原排程會延後 4 小時，需確認客戶交期優先級。",
    action: "確認接單承諾與產線重排",
    tone: "danger"
  },
  {
    title: "雞胸肉原料供應商替代料放行",
    owner: "採購 / 品保",
    due: "今日 14:00",
    impact: "替代料未放行會影響明日 2 張工單備料。",
    action: "確認檢驗結果與合約價格",
    tone: "warning"
  },
  {
    title: "冷凍庫寄倉安排",
    owner: "倉庫",
    due: "今日 16:00",
    impact: "本週五到貨後冷凍庫剩餘板數不足。",
    action: "核准外部寄倉或調整出貨順序",
    tone: "info"
  }
];

export const departmentBlockers: DepartmentBlocker[] = [
  {
    department: "R&D / 業務",
    title: "2 個開發案等待客戶選品",
    detail: "若本週未確認，後續供應商報價與成本試算會延後。",
    owner: "業務",
    relatedModule: "產品研發",
    href: "/rd",
    tone: "info"
  },
  {
    department: "生管",
    title: "一週內 3 張工單備料不足",
    detail: "洋蔥丁、雞胸肉、包材盒需確認採購到貨與替代料。",
    owner: "生管",
    relatedModule: "Planning / APS",
    href: "/planning",
    tone: "danger"
  },
  {
    department: "採購",
    title: "供應商報價差異超過 8%",
    detail: "新合約價格會影響 SO-240523-011 的報價底線。",
    owner: "採購",
    relatedModule: "採購",
    href: "/purchasing",
    tone: "warning"
  },
  {
    department: "倉庫 / 品保",
    title: "待檢物料占用 18 板",
    detail: "若下午未放行，冷藏庫可用板數會降至安全線以下。",
    owner: "品保",
    relatedModule: "品保",
    href: "/quality",
    tone: "warning"
  }
];

export const todayTasks: TodayTask[] = [
  {
    time: "09:30",
    module: "Orders",
    title: "確認 SO-240523-018 接單承諾",
    status: "待主管確認",
    tone: "danger"
  },
  {
    time: "10:00",
    module: "Warehouse",
    title: "冷凍庫入庫 24 板預留倉位",
    status: "調度中",
    tone: "warning"
  },
  {
    time: "11:20",
    module: "Quality",
    title: "雞胸肉替代料檢驗判定",
    status: "待放行",
    tone: "warning"
  },
  {
    time: "13:30",
    module: "Production",
    title: "A1 線咖哩雞肉調理包完工確認",
    status: "進行中",
    tone: "success"
  },
  {
    time: "15:00",
    module: "Logistics",
    title: "客戶 K-018 出貨文件齊備",
    status: "待列印",
    tone: "info"
  }
];

export const preOrderPipeline: PreOrderPipelineItem[] = [
  {
    stage: "開發需求",
    count: 5,
    focus: "2 件需確認目標成本",
    owner: "研發",
    tone: "info"
  },
  {
    stage: "打樣 / 送樣",
    count: 4,
    focus: "1 件本週需送樣",
    owner: "研發 / 業務",
    tone: "warning"
  },
  {
    stage: "供應商報價",
    count: 3,
    focus: "雞肉原料報價待回覆",
    owner: "採購",
    tone: "warning"
  },
  {
    stage: "客戶報價",
    count: 2,
    focus: "毛利底線已完成試算",
    owner: "業務",
    tone: "success"
  }
];

export const lineSummary = {
  active: 6,
  idle: 1,
  cleaning: 2,
  icon: Factory
};

export const productionLines: ProductionLine[] = [
  {
    line: "A1 調理包產線",
    product: "咖哩雞肉調理包",
    batchNo: "B240523-A101",
    status: "生產中",
    tone: "success",
    progress: 72,
    yieldRate: "99.1%",
    eta: "14:30 完工"
  },
  {
    line: "B2 冷凍蔬菜產線",
    product: "綜合冷凍蔬菜",
    batchNo: "B240523-B207",
    status: "待料",
    tone: "warning",
    progress: 38,
    yieldRate: "97.4%",
    eta: "等待玉米粒入線"
  },
  {
    line: "C3 包裝產線",
    product: "即食雞胸肉",
    batchNo: "B240523-C315",
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
    title: "A1 金檢重檢率上升",
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
  { date: "05/17", yieldRate: 97.8, reworkRate: 1.5 },
  { date: "05/18", yieldRate: 98.1, reworkRate: 1.3 },
  { date: "05/19", yieldRate: 98.4, reworkRate: 1.1 },
  { date: "05/20", yieldRate: 97.9, reworkRate: 1.6 },
  { date: "05/21", yieldRate: 98.5, reworkRate: 1.0 },
  { date: "05/22", yieldRate: 98.2, reworkRate: 1.2 },
  { date: "05/23", yieldRate: 98.6, reworkRate: 0.9 }
];

export const alertDistributionData: AlertDistributionItem[] = [
  { name: "缺料", value: 42, tone: "warning" },
  { name: "設備", value: 24, tone: "danger" },
  { name: "品保", value: 19, tone: "info" },
  { name: "倉位", value: 15, tone: "success" }
];

export const moduleShortcuts = [
  { label: "Orders", href: "/orders", icon: ClipboardCheck },
  { label: "Planning", href: "/planning", icon: CalendarClock },
  { label: "Purchasing", href: "/purchasing", icon: ShoppingCart },
  { label: "Warehouse", href: "/warehouse", icon: PackageSearch },
  { label: "Quality", href: "/quality", icon: ShieldCheck },
  { label: "Production", href: "/production", icon: Factory },
  { label: "Logistics", href: "/logistics", icon: Truck },
  { label: "Finance", href: "/finance", icon: DollarSign }
];

export const dashboardMock: DashboardData = {
  managerSnapshot,
  managerFocusItems,
  managerDecisionItems,
  departmentBlockers,
  todayTasks,
  preOrderPipeline,
  productionLines,
  alertItems,
  productionTrendData,
  oeeTrendData,
  qualityTrendData,
  alertDistributionData,
  moduleShortcuts
};
