import { API_BASE_URL, loginUrl } from "../config.ts";

export class ApiError extends Error {
  status: number;
  details?: Record<string, string[]>;

  constructor(status: number, message: string, details?: Record<string, string[]>) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.details = details;
  }
}

async function apiRequest<T>(path: string, init: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, init);
  } catch (error) {
    if (init.signal?.aborted) throw error;
    throw new ApiError(0, "Could not reach the server. Is the backend running?");
  }

  if (!response.ok) {
    let details: Record<string, string[]> | undefined;
    try {
      const body = (await response.json()) as Record<string, string | string[]>;
      details = Object.fromEntries(Object.entries(body).map(([key, value]) => [key, Array.isArray(value) ? value : [value]]));
    } catch {
      details = undefined;
    }
    const message = details?.non_field_errors?.[0] ?? (response.status === 404 ? "Not found." : `The server returned an error (${response.status}).`);
    throw new ApiError(response.status, message, details);
  }

  if (response.status === 204) return undefined as T;
  return (await response.json()) as T;
}

export function apiGet<T>(path: string, signal?: AbortSignal): Promise<T> {
  return apiRequest<T>(path, {
    signal,
    headers: { Accept: "application/json" },
  });
}

/** Django's CSRF token, from the cookie set by GET /api/auth/me/. */
function csrfToken(): string {
  const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]*)/);
  return match ? decodeURIComponent(match[1]) : "";
}

export async function apiMutation<T>(path: string, method: "POST" | "PATCH" | "DELETE", body?: unknown): Promise<T> {
  try {
    return await apiRequest<T>(path, {
      method,
      headers: {
        Accept: "application/json",
        "X-CSRFToken": csrfToken(),
        ...(body === undefined ? {} : { "Content-Type": "application/json" }),
      },
      ...(body === undefined ? {} : { body: JSON.stringify(body) }),
    });
  } catch (error) {
    // Session expired or not a superuser: send them to the Django login.
    if (error instanceof ApiError && (error.status === 401 || error.status === 403)) {
      window.location.assign(loginUrl("/admin"));
    }
    throw error;
  }
}

/** End the Django session, then go to the home page. */
export async function logout(): Promise<void> {
  try {
    await apiRequest<void>(endpoints.authLogout(), { method: "POST", headers: { "X-CSRFToken": csrfToken() } });
  } finally {
    window.location.assign("/");
  }
}

/** Endpoint paths, relative to API_BASE_URL. */
export const endpoints = {
  authMe: () => "/auth/me/",

  authLogout: () => "/auth/logout/",

  categories: () => "/categories/",

  createCategory: () => "/categories/",

  updateCategory: (id: number | string) => `/categories/${id}/`,

  deleteCategory: (id: number | string) => `/categories/${id}/`,

  news: (params: { limit?: number; category?: number } = {}) => {
    const query = new URLSearchParams();
    if (params.category !== undefined) query.set("category", String(params.category));
    if (params.limit !== undefined) query.set("limit", String(params.limit));
    const qs = query.toString();
    return `/news/${qs ? `?${qs}` : ""}`;
  },

  article: (id: number | string) => `/news/${id}/`,

  createNews: () => "/news/",

  updateNews: (id: number | string) => `/news/${id}/`,

  deleteNews: (id: number | string) => `/news/${id}/`,
};
