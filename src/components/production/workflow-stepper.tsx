import { Check } from "lucide-react";
import type { WorkOrderStage } from "@/types/production";

type WorkflowStepperProps = {
  stages: WorkOrderStage[];
  currentStage: WorkOrderStage;
};

export function WorkflowStepper({ stages, currentStage }: WorkflowStepperProps) {
  const currentIndex = stages.indexOf(currentStage);

  return (
    <div className="grid grid-cols-5 gap-2">
      {stages.map((stage, index) => {
        const isComplete = index < currentIndex || currentStage === "完工";
        const isCurrent = index === currentIndex && currentStage !== "完工";

        return (
          <div className="min-w-0" key={stage}>
            <div
              className={`flex h-8 items-center justify-center rounded-full border text-xs font-semibold ${
                isComplete
                  ? "border-success bg-success text-white"
                  : isCurrent
                    ? "border-primary bg-primary text-white"
                    : "border-border bg-slate-50 text-textSecondary"
              }`}
            >
              {isComplete ? <Check className="h-4 w-4" aria-hidden="true" /> : index + 1}
            </div>
            <p className="mt-2 truncate text-center text-xs text-textSecondary">{stage}</p>
          </div>
        );
      })}
    </div>
  );
}
