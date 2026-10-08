import { useEffect, useState } from "react";
import { ApiError, apiGet, endpoints } from "./client.ts";

export interface AuthUser {
  authenticated: boolean;
  username: string | null;
  is_superuser: boolean;
}

/** The user Django rendered into the page (Django-served build only). */
function readDjangoContext(): AuthUser | undefined {
  const text = document.getElementById("django-context")?.textContent;
  if (!text) return undefined;
  try {
    return JSON.parse(text) as AuthUser;
  } catch {
    return undefined;
  }
}

/** Who is logged in. Starts from the Django-rendered user when there is one, then checks /api/auth/me/. */
export function useAuth() {
  const [user, setUser] = useState<AuthUser | undefined>(readDjangoContext);
  const [error, setError] = useState<ApiError>();

  useEffect(() => {
    const controller = new AbortController();
    apiGet<AuthUser>(endpoints.authMe(), controller.signal)
      .then(setUser)
      .catch((reason: unknown) => {
        if (controller.signal.aborted) return;
        setError(reason instanceof ApiError ? reason : new ApiError(0, "Something went wrong."));
      });
    return () => controller.abort();
  }, []);

  return { user, error: user === undefined ? error : undefined, loading: user === undefined && error === undefined };
}
