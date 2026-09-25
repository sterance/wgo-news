import { API_BASE_URL } from "../config.ts";

export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export async function apiGet<T>(path: string, signal?: AbortSignal): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      signal,
      headers: { Accept: "application/json" },
    });
  } catch (error) {
    if (signal?.aborted) throw error;
    throw new ApiError(0, "Could not reach the server. Is the backend running?");
  }

  if (!response.ok) {
    throw new ApiError(
      response.status,
      response.status === 404 ? "Not found." : `The server returned an error (${response.status}).`,
    );
  }
  return (await response.json()) as T;
}

/** Endpoint paths, relative to API_BASE_URL. */
export const endpoints = {
  categories: () => "/categories/",

  news: (params: { category?: number; limit?: number } = {}) => {
    const query = new URLSearchParams();
    if (params.category !== undefined) query.set("category", String(params.category));
    if (params.limit !== undefined) query.set("limit", String(params.limit));
    const qs = query.toString();
    return `/news/${qs ? `?${qs}` : ""}`;
  },

  article: (id: number | string) => `/news/${id}/`,
};
