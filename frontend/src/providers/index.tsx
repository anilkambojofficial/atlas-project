"use client";

// =============================================================================
// Project ATLAS — Root Providers
//
// Composes all application-level providers in the correct dependency order:
//   QueryProvider  (TanStack Query — no dependencies)
//   AuthProvider   (reads session store — no query deps)
//   ThemeProvider  (next-themes — must wrap the entire tree)
// =============================================================================

import { ThemeProvider } from "next-themes";
import type { ReactNode } from "react";
import { QueryProvider } from "./query-provider";
import { AuthProvider } from "./auth-provider";

interface ProvidersProps {
  children: ReactNode;
}

export function Providers({ children }: ProvidersProps) {
  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
    >
      <QueryProvider>
        <AuthProvider>{children}</AuthProvider>
      </QueryProvider>
    </ThemeProvider>
  );
}
