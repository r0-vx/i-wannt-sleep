import type { Metadata } from "next";
import { DM_Sans, IBM_Plex_Mono, Space_Grotesk } from "next/font/google";
import "./globals.css";

const display = Space_Grotesk({ variable: "--font-display", subsets: ["latin"], display: "swap" });
const body = DM_Sans({ variable: "--font-body", subsets: ["latin"], display: "swap" });
const mono = IBM_Plex_Mono({ variable: "--font-ibm", subsets: ["latin"], weight: ["400", "500", "600"], display: "swap" });

export const metadata: Metadata = {
  title: { default: "ForwardCheck AI", template: "%s | ForwardCheck AI" },
  description: "Investigate suspicious forwards through inspectable claims, evidence, context, and rhetoric analysis.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en" data-scroll-behavior="smooth" className={`${display.variable} ${body.variable} ${mono.variable} h-full antialiased`}><body className="min-h-full">{children}</body></html>;
}
