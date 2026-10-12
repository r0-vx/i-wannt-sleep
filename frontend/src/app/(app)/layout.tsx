import { AppShell } from "@/components/app-shell";
import { Suspense } from "react";

export default function ProductLayout({ children }: { children: React.ReactNode }) {
  return <Suspense fallback={<main className="min-h-screen bg-[var(--page)] p-10 text-[var(--text-muted)]">Loading workspace…</main>}><AppShell>{children}</AppShell></Suspense>;
}
