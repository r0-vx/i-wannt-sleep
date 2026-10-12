import type { InvestigationSummary } from "./types";

export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const SESSION_KEY = "forwardcheck.guest-session.v1";

export function getGuestSession(): string {
  if (typeof window === "undefined") return "";
  const existing = window.localStorage.getItem(SESSION_KEY);
  if (existing) return existing;
  const created = crypto.randomUUID();
  window.localStorage.setItem(SESSION_KEY, created);
  return created;
}

export class ApiError extends Error {
  constructor(message: string, readonly status: number) { super(message); }
}

export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", "X-ForwardCheck-Session": getGuestSession(), ...init.headers },
  });
  if (!response.ok) {
    const payload = (await response.json().catch(() => null)) as { detail?: string } | null;
    throw new ApiError(payload?.detail ?? "The request could not be completed.", response.status);
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export async function createAndVerify(payload: { text: string; language: string; caption?: string }): Promise<InvestigationSummary> {
  const created = await apiFetch<InvestigationSummary>("/api/v1/investigations", { method: "POST", body: JSON.stringify(payload) });
  await apiFetch<InvestigationSummary>(`/api/v1/investigations/${created.id}/verify`, { method: "POST" });
  return created;
}
