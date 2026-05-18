import { Banknote, CircleDollarSign, ReceiptText } from "lucide-react";
import { CompactListPanel } from "@/components/common/compact-list-panel";
import { DetailCard } from "@/components/common/detail-card";
import { ModuleHero } from "@/components/common/module-hero";
import { ModuleKpiCard } from "@/components/common/module-kpi-card";
import { ProcessBoard } from "@/components/common/process-board";
import { AppLayout } from "@/layouts/app-layout";

const kpis = [
  { label: "本月營收", value: "18.6M", hint: "+8.2%", tone: "success" as const },
  { label: "應收帳款", value: "6.3M", hint: "12 筆未收", tone: "warning" as const },
  { label: "應付帳款", value: "4.1M", hint: "7 筆本週到期", tone: "info" as const },
  { label: "生產成本率", value: "62%", hint: "-1.4%", tone: "success" as const }
];

const financeCards = [
  {
    eyebrow: "AR-240512-018",
    title: "全聯中區 DC 應收帳款",
    subtitle: "出貨單 SH-240512-08 / 咖哩雞肉調理包",
    status: "待收款",
    tone: "warning" as const,
    rows: [
      { label: "金額", value: "NT$ 1,284,000" },
      { label: "到期", value: "2026-05-25" },
      { label: "帳期", value: "月結 30 天" }
    ]
  },
  {
    eyebrow: "AP-240512-011",
    title: "綠田食品原料應付",
    subtitle: "PO-240512-031 / 冷凍玉米粒",
    status: "待審核",
    tone: "info" as const,
    rows: [
      { label: "金額", value: "NT$ 86,400" },
      { label: "到期", value: "2026-05-20" },
      { label: "關聯", value: "WH-IN-240512-018" }
    ]
  }
];

const cashTasks = [
  {
    id: "FIN-AL-006",
    title: "B2 缺料造成加急採購",
    detail: "預估採購成本增加 3.8%，需財務確認毛利影響。",
    meta: "關聯 PO-240512-031",
    status: "待分析",
    tone: "warning" as const
  },
  {
    id: "FIN-AL-007",
    title: "包材替代供應商價格偏高",
    detail: "替代商報價高於標準成本 7.5%，建議走主管核准。",
    meta: "關聯 RFQ-011",
    status: "需核准",
    tone: "danger" as const
  }
];

const flow = [
  {
    title: "應收",
    items: [{ id: "AR-018", title: "全聯中區 DC", detail: "NT$ 1.28M 待收", tone: "warning" as const }]
  },
  {
    title: "應付",
    items: [{ id: "AP-011", title: "綠田食品", detail: "原料款待審核", tone: "info" as const }]
  },
  {
    title: "成本",
    items: [{ id: "COST-A1", title: "A1 調理包產線", detail: "成本率 61.2%", tone: "success" as const }]
  },
  {
    title: "核准",
    items: [{ id: "APR-004", title: "包材加價採購", detail: "等待主管核准", tone: "danger" as const }]
  }
];

export default function FinancePage() {
  return (
    <AppLayout activePath="/finance" title="財務中心 Finance Module">
      <div className="mx-auto max-w-[1440px] space-y-6">
        <ModuleHero
          badge="Sprint 8 Finance"
          title="財務、成本與帳款管理中心"
          description="將採購、生產、出貨與帳款連成管理視圖，協助掌握應收應付、成本率與毛利風險。"
          metrics={[
            { label: "營收", value: "18.6M", icon: CircleDollarSign },
            { label: "應收", value: "6.3M", icon: ReceiptText },
            { label: "應付", value: "4.1M", icon: Banknote }
          ]}
        />
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {kpis.map((item) => <ModuleKpiCard {...item} key={item.label} />)}
        </section>
        <ProcessBoard eyebrow="Finance Workflow" title="帳款與成本流程看板" columns={flow} />
        <section className="grid gap-6 xl:grid-cols-[1fr_420px]">
          <div className="grid gap-4">
            {financeCards.map((item) => <DetailCard {...item} key={item.eyebrow} />)}
          </div>
          <CompactListPanel eyebrow="Cost Alerts" title="成本與毛利提醒" items={cashTasks} />
        </section>
      </div>
    </AppLayout>
  );
}
