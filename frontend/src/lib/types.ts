export type InvestigationStatus = "draft" | "queued" | "extracting" | "discovering" | "verifying" | "complete" | "failed" | "cancelled";
export type InvestigationSummary = {
  id: string; title: string; input_type: string; language: string; status: InvestigationStatus;
  overall_conclusion: string | null; bait_score: number | null; failure_code: string | null;
  failure_message: string | null; created_at: string; updated_at: string;
};
export type ReportEvidence = {
  id: string; passage: string; locator: string; stance: "supports" | "contradicts" | "qualifies" | "context" | "insufficient";
  explanation: string | null; source_id: string; source_title: string; source_url: string;
  publisher: string | null; publication_date: string | null; retrieval_date: string;
};
export type InvestigationReport = {
  investigation: InvestigationSummary; original_text: string;
  claims: Array<{ id: string; exact_text: string; normalized_text: string; category: string;
    verdict: "Verified" | "False" | "Outdated" | "Partially Supported" | "Cannot Confirm" | null;
    explanation: string | null; evidence: ReportEvidence[] }>;
  bait_tags: Array<{ id: string; technique: string; matched_text: string; start_offset: number;
    end_offset: number; severity: string; rubric_points: number; explanation: string }>;
  methodology_note: string;
};
export type InvestigationGraph = {
  nodes: Array<{ id: string; type: "original" | "claim" | "source" | "evidence" | "verdict" | "bait";
    label: string; record_id: string; metadata: Record<string, string | number | null> }>;
  edges: Array<{ id: string; source: string; target: string; relationship: string; record_id: string }>;
};
