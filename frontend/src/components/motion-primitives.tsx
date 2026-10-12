"use client";

import { motion, useReducedMotion } from "motion/react";

export function MotionPage({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  const reduced = useReducedMotion();
  return <motion.div className={className} initial={reduced ? false : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: reduced ? 0 : .4, ease: [0.16, 1, 0.3, 1] }}>{children}</motion.div>;
}

export function MotionItem({ children, className = "", delay = 0 }: { children: React.ReactNode; className?: string; delay?: number }) {
  const reduced = useReducedMotion();
  return <motion.div className={className} initial={reduced ? false : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: reduced ? 0 : .4, delay: reduced ? 0 : delay, ease: [0.16, 1, 0.3, 1] }}>{children}</motion.div>;
}
