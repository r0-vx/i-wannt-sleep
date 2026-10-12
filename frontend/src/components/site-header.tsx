"use client";

import { ArrowRight, Menu, X } from "lucide-react";
import Link from "next/link";
import { useState } from "react";
import { Logo } from "./logo";

const links = [["How It Works", "/#how-it-works"], ["Features", "/#features"], ["About", "/about"], ["FAQ", "/faq"]] as const;

export function SiteHeader() {
  const [open, setOpen] = useState(false);
  return <header className="public-header sticky top-0 z-50 border-b border-white/10 bg-[rgb(11_16_26_/.86)] backdrop-blur-xl"><div className="mx-auto flex h-16 max-w-[1400px] items-center justify-between px-4 sm:px-6"><Logo inverse/><nav className="hidden items-center gap-7 text-sm font-medium text-slate-300 md:flex" aria-label="Primary">{links.map(([label, href]) => <Link key={href} className="rounded-lg py-2 transition-colors hover:text-white" href={href}>{label}</Link>)}</nav><div className="flex items-center gap-2"><Link href="/investigations/new" className="button-primary max-sm:!hidden sm:!inline-flex">Investigate Now <ArrowRight aria-hidden="true" size={16}/></Link><button type="button" className="grid size-11 place-items-center rounded-xl border border-white/15 bg-white/5 text-white md:hidden" aria-expanded={open} aria-controls="public-navigation" onClick={() => setOpen((value) => !value)}><span className="sr-only">{open ? "Close navigation" : "Open navigation"}</span>{open ? <X aria-hidden="true" size={20}/> : <Menu aria-hidden="true" size={20}/>}</button></div></div>{open ? <nav id="public-navigation" className="border-t border-white/10 bg-[var(--navy)] px-4 py-4 text-white md:hidden" aria-label="Mobile primary"><div className="mx-auto grid max-w-[1400px] gap-1">{links.map(([label, href]) => <Link key={href} onClick={() => setOpen(false)} className="rounded-xl px-3 py-3 text-sm font-semibold hover:bg-white/5" href={href}>{label}</Link>)}<Link href="/investigations/new" onClick={() => setOpen(false)} className="button-primary mt-2">Investigate a Forward</Link></div></nav> : null}</header>;
}
