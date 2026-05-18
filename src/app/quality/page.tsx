import { AlertTriangle, BadgeCheck, FlaskConical } from "lucide-react";
import { CompactListPanel } from "@/components/common/compact-list-panel";
import { DetailCard } from "@/components/common/detail-card";
import { ModuleHero } from "@/components/common/module-hero";
import { ModuleKpiCard } from "@/components/common/module-kpi-card";
import { ProcessBoard } from "@/components/common/process-board";
import { AppLayout } from "@/layouts/app-layout";

const kpis = [
  { label: "今日檢驗批", value: "28", hint: "21 批通過", tone: "success" as const },
  { label: "待判定", value: "5", hint: "平均 18 分", tone: "warning" as const },
  { label: "異常批號", value: "2", hint: "需 QA 放行", tone: "danger" as const },
  { label: "首件合格率", value: "97%", hint: "+1.2%", tone: "info" as const }
];

const inspections = [
  {
    eyebrow: "QC-240512-018",
    title: "咖哩雞肉調理包首件檢驗",
    subtitle: "B240512-A101 / A1 調理包產線",
    status: "檢驗中",
    tone: "info" as const,
    rows: [
      { label: "檢驗項", value: "金檢 / 重量 / 外觀" },
      { label: "抽樣數", value: "32 包" },
      { label: "負責", value: "吳品保" }
    ]
  },
  {
    eyebrow: "QC-240512-021",
    title: "綜合冷凍蔬菜微生物快篩",
    subtitle: "B240512-B207 / B2 冷凍蔬菜產線",
    status: "待判定",
    tone: "warning" as const,
    rows: [
      { label: "檢驗項", value: "ATP / 溫度 / 雜質" },
      { label: "抽樣數", value: "12 袋" },
      { label: "負責", value: "林檢驗員" }
    ]
  }
];

const exceptions = [
  {
    id: "NCR-240512-004",
    title: "A1 金檢重檢率偏高",
    detail: "近 30 分鐘重檢率 2.8%，已通知現場確認輸送帶與包材狀態。",
    meta: "批號 B240512-A101 / 需 11:30 前回覆",
    status: "處置中",
    tone: "danger" as const
  },
  {
    id: "NCR-240512-005",
    title: "B2 原料溫度接近上限",
    detail: "入線前溫度 4.7°C，仍在規格內但需縮短等待時間。",
    meta: "批號 RM240506-CORN / QA 追蹤",
    status: "觀察",
    tone: "warning" as const
  }
];

const processColumns = [
  {
    title: "待抽樣",
    items: [{ id: "QC-019", title: "雞胸肉包裝線", detail: "首件抽樣等待中", tone: "neutral" as const }]
  },
  {
    title: "檢驗中",
    items: [{ id: "QC-018", title: "咖哩雞肉調理包", detail: "金檢與重量檢驗", tone: "info" as const }]
  },
  {
    title: "待判定",
    items: [{ id: "QC-021", title: "冷凍蔬菜快篩", detail: "等待 QA 判定", tone: "warning" as const }]
  },
  {
    title: "已放行",
    items: [{ id: "QC-017", title: "玉米濃湯成品", detail: "檢驗合格可入庫", tone: "success" as const }]
  }
];

export default function QualityPage() {
  return (
    <AppLayout activePath="/quality" title="品保中心 Quality Module">
      <div className="mx-auto max-w-[1440px] space-y-6">
        <ModuleHero
          badge="Sprint 5 Quality"
          title="品保檢驗與異常處置中心"
          description="整合首件檢驗、製程抽驗、異常批號與 QA 放行流程，讓品保與現場能即時同步品質狀態。"
          metrics={[
            { label: "檢驗批", value: "28", icon: FlaskConical },
            { label: "合格批", value: "21", icon: BadgeCheck },
            { label: "異常", value: "2", icon: AlertTriangle }
          ]}
        />

        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {kpis.map((item) => <ModuleKpiCard {...item} key={item.label} />)}
        </section>

        <ProcessBoard eyebrow="Quality Workflow" title="品保流程看板" columns={processColumns} />

        <section className="grid gap-6 xl:grid-cols-[1fr_420px]">
          <div className="grid gap-4">
            {inspections.map((item) => <DetailCard {...item} key={item.eyebrow} />)}
          </div>
          <CompactListPanel eyebrow="NCR Center" title="異常批號處置" items={exceptions} />
        </section>
      </div>
    </AppLayout>
  );
}
