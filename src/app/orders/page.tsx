import { CalendarClock, ClipboardList, Truck } from "lucide-react";
import { CompactListPanel } from "@/components/common/compact-list-panel";
import { DetailCard } from "@/components/common/detail-card";
import { ModuleHero } from "@/components/common/module-hero";
import { ModuleKpiCard } from "@/components/common/module-kpi-card";
import { ProcessBoard } from "@/components/common/process-board";
import { AppLayout } from "@/layouts/app-layout";

const kpis = [
  { label: "本日訂單", value: "36", hint: "12 筆急單", tone: "info" as const },
  { label: "待排產", value: "9", hint: "需生管確認", tone: "warning" as const },
  { label: "待出貨", value: "14", hint: "今日配送", tone: "success" as const },
  { label: "交期風險", value: "3", hint: "需主管決策", tone: "danger" as const }
];

const orderCards = [
  {
    eyebrow: "SO-240512-018",
    title: "全聯中區 DC 補貨訂單",
    subtitle: "客戶：全聯 / 通路：冷凍食品 / 交期 2026-05-14",
    status: "生產中",
    tone: "success" as const,
    rows: [
      { label: "品項", value: "咖哩雞肉調理包" },
      { label: "數量", value: "12,000 盒" },
      { label: "關聯工單", value: "MO-240512-001" }
    ]
  },
  {
    eyebrow: "SO-240512-022",
    title: "便利商店新品試賣訂單",
    subtitle: "客戶：CVS 北區 / 通路：即食餐盒 / 交期 2026-05-16",
    status: "待排產",
    tone: "warning" as const,
    rows: [
      { label: "品項", value: "番茄牛肉燉飯" },
      { label: "數量", value: "4,800 盒" },
      { label: "BOM 版本", value: "BOM-FG-RICE-003" }
    ]
  }
];

const alerts = [
  {
    id: "ORD-AL-001",
    title: "SO-240512-022 尚未排產",
    detail: "交期剩 4 天，需確認 A2 產線與包材庫存。",
    meta: "關聯品項 FG-RICE-003",
    status: "待生管",
    tone: "warning" as const
  },
  {
    id: "ORD-AL-002",
    title: "全聯訂單出貨需保留批號鏈路",
    detail: "此訂單需完整出貨批號與品保放行紀錄。",
    meta: "關聯批號 B240512-A101",
    status: "追蹤中",
    tone: "info" as const
  }
];

const flow = [
  {
    title: "待確認",
    items: [{ id: "SO-024", title: "餐飲通路急單", detail: "等待業務確認交期", tone: "warning" as const }]
  },
  {
    title: "待排產",
    items: [{ id: "SO-022", title: "番茄牛肉燉飯", detail: "需 A2 產線排程", tone: "warning" as const }]
  },
  {
    title: "生產中",
    items: [{ id: "SO-018", title: "咖哩雞肉調理包", detail: "MO-240512-001", tone: "success" as const }]
  },
  {
    title: "待出貨",
    items: [{ id: "SO-016", title: "玉米濃湯", detail: "等待冷鏈派車", tone: "info" as const }]
  }
];

export default function OrdersPage() {
  return (
    <AppLayout activePath="/orders" title="訂單中心 Order Module">
      <div className="mx-auto max-w-[1440px] space-y-6">
        <ModuleHero
          badge="Phase 1.5 Orders"
          title="客戶訂單、交期與排產連動中心"
          description="從客戶需求出發，串接品項、BOM、工單、生產狀態、批號與物流出貨，讓訂單能一路追到交付。"
          metrics={[
            { label: "訂單", value: "36", icon: ClipboardList },
            { label: "交期風險", value: "3", icon: CalendarClock },
            { label: "待出貨", value: "14", icon: Truck }
          ]}
        />
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {kpis.map((item) => <ModuleKpiCard {...item} key={item.label} />)}
        </section>
        <ProcessBoard eyebrow="Order Workflow" title="訂單流程看板" columns={flow} />
        <section className="grid gap-6 xl:grid-cols-[1fr_420px]">
          <div className="grid gap-4">
            {orderCards.map((item) => <DetailCard {...item} key={item.eyebrow} />)}
          </div>
          <CompactListPanel eyebrow="Order Alerts" title="訂單風險與待辦" items={alerts} />
        </section>
      </div>
    </AppLayout>
  );
}
