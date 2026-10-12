import { ReportView } from "./report-view";
export const instant = false;
export default async function ReportPage({ params }: { params: Promise<{ id: string }> }) { const { id } = await params; return <ReportView investigationId={id} />; }
