import { GraphView } from "./truth-graph";
export const instant = false;
export default async function GraphPage({ params }: { params: Promise<{ id: string }> }) { const { id } = await params; return <GraphView investigationId={id} />; }
