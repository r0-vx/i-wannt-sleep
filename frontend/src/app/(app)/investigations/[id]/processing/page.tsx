import { ProcessingPanel } from "./processing-panel";
export const instant = false;
export default async function ProcessingPage({ params }: { params: Promise<{ id: string }> }) { const { id } = await params; return <ProcessingPanel investigationId={id} />; }
