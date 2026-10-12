import { CheckCircle2, CircleHelp, Clock3, Info, XCircle } from "lucide-react";

const verdicts = {
  Verified: [CheckCircle2, "bg-emerald-50 text-emerald-700 border-emerald-100"],
  False: [XCircle, "bg-rose-50 text-rose-700 border-rose-100"],
  Outdated: [Clock3, "bg-amber-50 text-amber-700 border-amber-100"],
  "Partially Supported": [Info, "bg-blue-50 text-blue-700 border-blue-100"],
  "Cannot Confirm": [CircleHelp, "bg-slate-100 text-slate-700 border-slate-200"],
} as const;

export type VerdictLabel = keyof typeof verdicts;
export function VerdictBadge({ verdict }: { verdict: VerdictLabel | null }) {
  const value = verdict ?? "Cannot Confirm"; const [Icon,colors]=verdicts[value];
  return <span className={`inline-flex min-h-7 items-center gap-1.5 rounded-full border px-2.5 text-xs font-bold ${colors}`}><Icon aria-hidden="true" size={14}/>{verdict ? value : "Not assessed"}</span>;
}
