import { Bot, BrainCircuit, Sparkles } from "lucide-react";
import { CompactListPanel } from "@/components/common/compact-list-panel";
import { DetailCard } from "@/components/common/detail-card";
import { ModuleHero } from "@/components/common/module-hero";
import { ModuleKpiCard } from "@/components/common/module-kpi-card";
import { ProcessBoard } from "@/components/common/process-board";
import { AppLayout } from "@/layouts/app-layout";

const kpis = [
  { label: "今日洞察", value: "16", hint: "5 筆高影響", tone: "info" as const },
  { label: "風險預警", value: "4", hint: "缺料 / 品保", tone: "warning" as const },
  { label: "節省工時", value: "7.5h", hint: "本日估算", tone: "success" as const },
  { label: "待確認建議", value: "6", hint: "需主管決策", tone: "danger" as const }
];

const insights = [
  {
    eyebrow: "AI-INS-240512-001",
    title: "B2 產線缺料將影響 16:20 工單",
    subtitle: "依庫存、安全庫存、採購交期與排程推估",
    status: "高影響",
    tone: "danger" as const,
    rows: [
      { label: "建議", value: "優先出庫 RM240506-CORN" },
      { label: "影響", value: "降低延誤 45 分" },
      { label: "信心", value: "87%" }
    ]
  },
  {
    eyebrow: "AI-INS-240512-002",
    title: "A1 金檢重檢率可能與包材批次相關",
    subtitle: "比對 NCR、包材批號與產線時間序列",
    status: "需驗證",
    tone: "warning" as const,
    rows: [
      { label: "建議", value: "抽查 PK240501-BAG" },
      { label: "關聯", value: "NCR-240512-004" },
      { label: "信心", value: "74%" }
    ]
  }
];

const assistantTasks = [
  {
    id: "ASK-001",
    title: "生成早會摘要",
    detail: "整理產量、OEE、缺料、品質異常與今日決策事項。",
    meta: "適用角色：廠長 / 生管 / 品保",
    status: "可執行",
    tone: "success" as const
  },
  {
    id: "ASK-002",
    title: "查詢批號完整鏈路",
    detail: "輸入成品批號後回推原料、工單、檢驗與出貨資訊。",
    meta: "範例：B240512-A101",
    status: "待串接",
    tone: "info" as const
  }
];

const flow = [
  {
    title: "偵測",
    items: [{ id: "DET-004", title: "缺料風險", detail: "B2 產線 45 分內", tone: "warning" as const }]
  },
  {
    title: "分析",
    items: [{ id: "ANA-002", title: "金檢重檢率", detail: "包材批次相關", tone: "info" as const }]
  },
  {
    title: "建議",
    items: [{ id: "REC-008", title: "先補玉米粒", detail: "降低延誤 45 分", tone: "success" as const }]
  },
  {
    title: "確認",
    items: [{ id: "APR-009", title: "主管決策", detail: "待王廠長確認", tone: "danger" as const }]
  }
];

export default function AiPage() {
  return (
    <AppLayout activePath="/ai" title="AI 中心 AI Insights Module">
      <div className="mx-auto max-w-[1440px] space-y-6">
        <ModuleHero
          badge="Sprint 9 AI Center"
          title="AI 營運洞察與決策輔助中心"
          description="將 Dashboard、製造、倉儲、品保、採購與財務資料轉成可行動的預警、建議與管理摘要。"
          metrics={[
            { label: "洞察", value: "16", icon: Sparkles },
            { label: "預警", value: "4", icon: BrainCircuit },
            { label: "助手", value: "2", icon: Bot }
          ]}
        />
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {kpis.map((item) => <ModuleKpiCard {...item} key={item.label} />)}
        </section>
        <ProcessBoard eyebrow="AI Decision Flow" title="AI 預警與建議流程" columns={flow} />
        <section className="grid gap-6 xl:grid-cols-[1fr_420px]">
          <div className="grid gap-4">
            {insights.map((item) => <DetailCard {...item} key={item.eyebrow} />)}
          </div>
          <CompactListPanel eyebrow="Assistant Actions" title="AI Assistant 任務" items={assistantTasks} />
        </section>
      </div>
    </AppLayout>
  );
}
