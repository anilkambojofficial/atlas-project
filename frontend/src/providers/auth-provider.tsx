"use client";

// =============================================================================
// Project ATLAS — Auth Provider
//
// Hydrates the Zustand auth store from sessionStorage on first client render.
// Full OIDC callback handling is implemented in IP-002 (Identity & Access).
// =============================================================================

import { useEffect, type ReactNode } from "react";
import { useAuthStore } from "@/store/auth-store";

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const hydrateFromStorage = useAuthStore((s) => s.hydrateFromStorage);

  useEffect(() => {
    // Hydrate session from sessionStorage on mount (client-side only)
    hydrateFromStorage();
  }, [hydrateFromStorage]);

  return <>{children}</>;
}
