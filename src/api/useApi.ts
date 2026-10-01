import { useCallback, useEffect, useState } from "react";
import { ApiError, apiGet } from "./client.ts";

interface Result<T> {
  path: string;
  data?: T;
  error?: ApiError;
}

export function useApi<T>(path: string | null) {
  const [result, setResult] = useState<Result<T> | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    if (path === null) return;
    const controller = new AbortController();

    apiGet<T>(path, controller.signal)
      .then((data) => setResult({ path, data }))
      .catch((error: unknown) => {
        if (controller.signal.aborted) return;
        setResult({
          path,
          error: error instanceof ApiError ? error : new ApiError(0, "Something went wrong."),
        });
      });

    return () => controller.abort();
  }, [path, refreshKey]);

  const current = result?.path === path ? result : null;
  return {
    data: current?.data,
    error: current?.error,
    loading: path !== null && current === null,
    refetch: useCallback(() => {
      setResult(null);
      setRefreshKey((key) => key + 1);
    }, []),
  };
}
