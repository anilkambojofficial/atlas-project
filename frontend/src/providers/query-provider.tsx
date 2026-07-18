"use client";

// =============================================================================
// Project ATLAS — TanStack Query Provider
// =============================================================================

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { useState, type ReactNode } from "react";

interface QueryProviderProps {
  children: ReactNode;
}

export function QueryProvider({ children }: QueryProviderProps) {
  // Create the QueryClient once per mount (avoids sharing state between SSR renders)
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            // Data is considered fresh for 60 s before a background refetch
            staleTime: 60_000,
            // Keep unused queries in cache for 5 minutes
            gcTime: 5 * 60_000,
            // Retry failed requests once (avoids hammering a degraded service)
            retry: 1,
            retryDelay: (attempt) => Math.min(1000 * 2 ** attempt, 30_000),
            // Do not refetch on window focus in production
            refetchOnWindowFocus: process.env.NODE_ENV === "development",
          },
          mutations: {
            // Do not retry mutations automatically
            retry: 0,
          },
        },
      }),
  );

  const devtoolsEnabled =
    process.env.NEXT_PUBLIC_ENABLE_QUERY_DEVTOOLS === "true" ||
    process.env.NODE_ENV === "development";

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      {devtoolsEnabled && <ReactQueryDevtools initialIsOpen={false} />}
    </QueryClientProvider>
  );
}
