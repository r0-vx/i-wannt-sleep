"use client";

import { BookOpen, Files, LayoutDashboard, Menu, Plus, ScanSearch, Settings2, ShieldCheck, TrainFront, X } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { Logo } from "./logo";

const links = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/investigations/new", label: "New Investigation", icon: ScanSearch },
  { href: "/investigations", label: "Investigations", icon: Files },
  { href: "/evidence", label: "Evidence Library", icon: BookOpen },
  { href: "/settings", label: "Settings", icon: Settings2 },
];

const titles: Record<string, string> = { dashboard: "Dashboard", investigations: "Investigations", evidence: "Evidence Library", settings: "Settings" };

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const segments = pathname.split("/").filter(Boolean);
  const inNew = pathname === "/investigations/new";
  const pageTitle = inNew ? "New Investigation" : pathname.includes("/processing") ? "Investigation Progress" : pathname.includes("/graph") ? "TruthGraph" : pathname.includes("/report") ? "Verification Report" : titles[segments[0]] ?? "Workspace";
  const showFab = !inNew && !pathname.includes("/processing") && !pathname.includes("/graph");
  return <div className="app-grid bg-[var(--page)] text-[var(--text)]"><button type="button" onClick={() => setOpen((value) => !value)} aria-expanded={open} aria-controls="app-navigation" className="fixed right-4 top-2.5 z-[70] grid size-11 place-items-center rounded-xl border border-slate-200 bg-white shadow-sm lg:hidden"><span className="sr-only">{open ? "Close navigation" : "Open navigation"}</span>{open ? <X aria-hidden="true" size={20}/> : <Menu aria-hidden="true" size={20}/>}</button>{open ? <button type="button" aria-label="Close navigation overlay" className="fixed inset-0 z-[55] cursor-default bg-slate-950/55 backdrop-blur-[2px] lg:hidden" onClick={() => setOpen(false)}/> : null}<aside id="app-navigation" className={`${open ? "flex" : "hidden"} app-sidebar fixed inset-y-0 left-0 z-[60] w-[280px] flex-col border-r border-white/8 px-4 py-4 text-white lg:sticky lg:top-0 lg:flex lg:h-screen lg:w-[240px]`}><div className="px-2 pb-6"><Logo homeHref="/dashboard" inverse/></div><nav className="flex flex-1 flex-col gap-1.5" aria-label="Application">{links.map(({ href, label, icon: Icon }) => { const active = pathname === href || (href === "/investigations" && !inNew && pathname.startsWith("/investigations/")); return <Link key={href} href={href} onClick={()=>setOpen(false)} aria-current={active ? "page" : undefined} className={`relative flex min-h-11 items-center gap-3 rounded-xl px-3 text-sm font-semibold transition-colors ${active ? "bg-[var(--indigo)] text-white shadow-[0_10px_24px_-14px_rgba(88,101,242,.95)]" : "text-slate-300 hover:bg-white/6 hover:text-white"}`}><Icon aria-hidden="true" size={18} strokeWidth={1.9}/>{label}</Link>; })}</nav><div className="rail-message overflow-hidden rounded-[18px] border border-white/10 p-4"><TrainFront aria-hidden="true" className="text-[var(--rail-amber)]" size={22}/><p className="mt-8 font-display text-lg font-bold leading-5">Truth travels further.</p><div className="mt-4 flex items-center gap-2 text-xs text-slate-300"><ShieldCheck aria-hidden="true" className="text-[var(--teal)]" size={15}/>Private guest workspace</div></div></aside><div className="min-w-0"><header className="sticky top-0 z-40 flex h-16 items-center justify-between border-b border-[var(--border)] bg-[rgb(248_250_252_/.9)] px-4 backdrop-blur-xl sm:px-6 lg:px-8"><div><p className="font-metric text-[10px] font-semibold uppercase tracking-[.14em] text-[var(--text-muted)]">ForwardCheck workspace</p><h2 className="font-display text-sm font-bold tracking-[-0.01em]">{pageTitle}</h2></div>{!inNew ? <Link href="/investigations/new" className="button-primary mr-12 hidden sm:inline-flex lg:mr-0"><Plus aria-hidden="true" size={17}/>New Investigation</Link> : null}</header><main className="min-w-0">{children}</main>{showFab ? <Link href="/investigations/new" aria-label="Start new investigation" className="fixed bottom-5 right-5 z-30 grid size-14 place-items-center rounded-full bg-[var(--indigo)] text-white shadow-[0_16px_40px_-12px_rgba(88,101,242,.65)] transition-transform duration-200 hover:scale-105 active:scale-95 sm:hidden"><Plus aria-hidden="true" size={24}/></Link> : null}</div></div>;
}
