import { CheckCircle2, CircleHelp, Clock3, LoaderCircle, OctagonX, PauseCircle } from "lucide-react";
import type { InvestigationStatus } from "@/lib/types";

const config = {
  draft: ["Draft", CircleHelp, "bg-slate-100 text-slate-600"],
  queued: ["Queued", Clock3, "bg-amber-50 text-amber-700"],
  extracting: ["Extracting", LoaderCircle, "bg-indigo-50 text-indigo-700"],
  discovering: ["Discovering", LoaderCircle, "bg-blue-50 text-blue-700"],
  verifying: ["Verifying", LoaderCircle, "bg-violet-50 text-violet-700"],
  complete: ["Complete", CheckCircle2, "bg-emerald-50 text-emerald-700"],
  failed: ["Needs attention", OctagonX, "bg-rose-50 text-rose-700"],
  cancelled: ["Cancelled", PauseCircle, "bg-slate-100 text-slate-600"],
} satisfies Record<InvestigationStatus, [string, typeof CheckCircle2, string]>;

export function StatusBadge({ status }: { status: InvestigationStatus }) {
  const [label, Icon, colors] = config[status];
  const spins = ["extracting", "discovering", "verifying"].includes(status);
  return <span className={`inline-flex min-h-7 items-center gap-1.5 rounded-full px-2.5 text-xs font-semibold ${colors}`}><Icon aria-hidden="true" size={13} className={spins ? "animate-spin" : ""}/>{label}</span>;
}
