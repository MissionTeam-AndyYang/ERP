import { Barcode, CalendarClock, Network } from "lucide-react";
import { CompactListPanel } from "@/components/common/compact-list-panel";
import { DetailCard } from "@/components/common/detail-card";
import { ModuleHero } from "@/components/common/module-hero";
import { ModuleKpiCard } from "@/components/common/module-kpi-card";
import { ProcessBoard } from "@/components/common/process-board";
import { AppLayout } from "@/layouts/app-layout";

const kpis = [
  { label: "批號總數", value: "1,284", hint: "近 90 天", tone: "info" as const },
  { label: "製程批號", value: "312", hint: "今日 18 筆", tone: "success" as const },
  { label: "即期批號", value: "9", hint: "7 日內", tone: "warning" as const },
  { label: "隔離批號", value: "2", hint: "QA 鎖定", tone: "danger" as const }
];

const batchCards = [
  {
    eyebrow: "B240512-A101",
    title: "咖哩雞肉調理包成品批號",
    subtitle: "品項 FG-CURRY-101 / 工單 MO-240512-001",
    status: "生產中",
    tone: "success" as const,
    rows: [
      { label: "數量", value: "6,912 / 9,600 盒" },
      { label: "效期", value: "2026-11-08" },
      { label: "QA", value: "檢驗中" }
    ]
  },
  {
    eyebrow: "RM240506-CORN",
    title: "冷凍玉米粒原料批號",
    subtitle: "供應商綠田食品 / 庫位 FZ-A03-02",
    status: "即期",
    tone: "danger" as const,
    rows: [
      { label: "庫存", value: "180 kg" },
      { label: "效期", value: "2026-05-17" },
      { label: "去向", value: "B2 待領料" }
    ]
  }
];

const batchTasks = [
  {
    id: "BAT-TASK-001",
    title: "RM240506-CORN 即期優先使用",
    detail: "建議優先配置到 B2 冷凍蔬菜工單，避免原料逾期。",
    meta: "剩餘 5 天 / 180 kg",
    status: "需處理",
    tone: "danger" as const
  },
  {
    id: "BAT-TASK-002",
    title: "B240512-A101 待 QA 放行",
    detail: "成品批號需完成金檢與重量檢驗後才可入庫。",
    meta: "關聯 QC-240512-018",
    status: "檢驗中",
    tone: "info" as const
  }
];

const lifecycle = [
  {
    title: "原料批號",
    items: [{ id: "RM240506-CORN", title: "冷凍玉米粒", detail: "入庫 / 即期", tone: "danger" as const }]
  },
  {
    title: "製程批號",
    items: [{ id: "WIP240512-A101", title: "咖哩醬基底", detail: "A1 調理", tone: "info" as const }]
  },
  {
    title: "成品批號",
    items: [{ id: "B240512-A101", title: "咖哩雞肉調理包", detail: "生產中", tone: "success" as const }]
  },
  {
    title: "出貨批號",
    items: [{ id: "SH-240512-08", title: "全聯中區 DC", detail: "待出貨", tone: "warning" as const }]
  }
];

export default function BatchesPage() {
  return (
    <AppLayout activePath="/batches" title="批號中心 Batch Module">
      <div className="mx-auto max-w-[1440px] space-y-6">
        <ModuleHero
          badge="Phase 1.5 Batches"
          title="原料、製程、成品與出貨批號管理"
          description="把食品工廠最重要的批號生命週期獨立管理，串接效期、庫位、檢驗狀態、工單與出貨去向。"
          metrics={[
            { label: "批號", value: "1,284", icon: Barcode },
            { label: "即期", value: "9", icon: CalendarClock },
            { label: "鏈路", value: "99%", icon: Network }
          ]}
        />
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {kpis.map((item) => <ModuleKpiCard {...item} key={item.label} />)}
        </section>
        <ProcessBoard eyebrow="Batch Lifecycle" title="批號生命週期" columns={lifecycle} />
        <section className="grid gap-6 xl:grid-cols-[1fr_420px]">
          <div className="grid gap-4">
            {batchCards.map((item) => <DetailCard {...item} key={item.eyebrow} />)}
          </div>
          <CompactListPanel eyebrow="Batch Tasks" title="批號風險與待辦" items={batchTasks} />
        </section>
      </div>
    </AppLayout>
  );
}
