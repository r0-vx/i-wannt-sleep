import Link from "next/link";

export function BrandMark({ className = "" }: { className?: string }) {
  return <span className={`grid size-9 shrink-0 place-items-center rounded-xl bg-[var(--indigo)] text-white shadow-[0_8px_20px_-10px_rgba(88,101,242,.9)] ${className}`} aria-hidden="true"><svg width="21" height="21" viewBox="0 0 24 24" fill="none"><circle cx="6" cy="12" r="2.3" fill="currentColor"/><circle cx="17.8" cy="6.2" r="2.3" fill="currentColor"/><circle cx="17.8" cy="17.8" r="2.3" fill="currentColor"/><path d="M8.2 11.1 15.6 7M8.2 12.9l7.4 4.1" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/><path d="m14.6 11.8 2.1 2.1 3.7-4.4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/></svg></span>;
}

export function Logo({ compact = false, homeHref = "/", inverse = false }: { compact?: boolean; homeHref?: string; inverse?: boolean }) {
  return <Link href={homeHref} className={`inline-flex min-h-11 items-center gap-2.5 rounded-xl font-bold tracking-[-0.035em] ${inverse ? "text-white" : "text-[var(--text)]"}`}><BrandMark />{compact ? null : <span className="text-[17px]">ForwardCheck <span className="text-[var(--indigo)]">AI</span></span>}</Link>;
}
