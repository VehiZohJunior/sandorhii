const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8420";

export type Signal = {
  id: string;
  category: string;
  weight: number;
  occurrences: number;
  excerpt: string;
};

export type SuggestedLevel = "aucun" | "a_surveiller" | "modere" | "eleve";

export type LinguisticAnalysis = {
  score: number;
  suggested_level: SuggestedLevel;
  signals: Signal[];
  stats: Record<string, number>;
  model_version: string;
  language_supported: boolean;
};

export type Verdict =
  | "vrai"
  | "faux"
  | "partiellement_vrai"
  | "non_verifiable"
  | "trompeur";

export type FactCheck = {
  id: string;
  verdict: Verdict;
  global_score: number;
  resume: string;
  auteur: string;
  statut: string;
  created_at: string;
  published_at: string | null;
};

export type Submission = {
  id: string;
  content_type: string;
  raw_content: string;
  language: string;
  status: string;
  created_at: string;
  linguistic_analysis: LinguisticAnalysis | null;
  fact_check: FactCheck | null;
};

export type FeedItem = {
  submission_id: string;
  verdict: Verdict;
  global_score: number;
  resume: string;
  auteur: string;
  published_at: string | null;
  extrait: string;
};

class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function request<T>(
  path: string,
  init?: RequestInit & { adminPassword?: string }
): Promise<T> {
  const headers = new Headers(init?.headers);
  headers.set("Content-Type", "application/json");
  if (init?.adminPassword) {
    headers.set("X-Admin-Password", init.adminPassword);
  }
  const res = await fetch(`${API_URL}${path}`, {
    ...init,
    headers,
    cache: "no-store",
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(res.status, body.detail ?? `Erreur ${res.status}`);
  }
  return res.json();
}

export const api = {
  submitText: (texte: string, langue: string) =>
    request<Submission>("/api/submissions", {
      method: "POST",
      body: JSON.stringify({ texte, langue }),
    }),
  getSubmission: (id: string) => request<Submission>(`/api/submissions/${id}`),
  getFeed: (verdict?: string) =>
    request<FeedItem[]>(`/api/feed${verdict ? `?verdict=${verdict}` : ""}`),
  getFeedItem: (id: string) => request<Submission>(`/api/feed/${id}`),
  getQueue: (adminPassword: string) =>
    request<Submission[]>("/api/newsroom/queue", { adminPassword }),
  publish: (
    id: string,
    payload: { verdict: Verdict; resume: string; auteur: string },
    adminPassword: string
  ) =>
    request<FactCheck>(`/api/newsroom/${id}/publish`, {
      method: "POST",
      body: JSON.stringify(payload),
      adminPassword,
    }),
  reject: (id: string, adminPassword: string) =>
    request<Submission>(`/api/newsroom/${id}/reject`, {
      method: "POST",
      adminPassword,
    }),
};

export { ApiError };
