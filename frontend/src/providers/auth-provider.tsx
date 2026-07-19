"use client";

// =============================================================================
// Project ATLAS — Auth Provider (Sprint-002)
//
// Bootstraps the session from the httpOnly refresh cookie on first client
// render and keeps the short-lived access token fresh by scheduling a
// silent rotation before expiry (BP-003 §8.7 token rotation).
// =============================================================================

import { useEffect, useRef, type ReactNode } from "react";
import { useAuthStore } from "@/store/auth-store";

const REFRESH_SAFETY_FACTOR = 0.8;

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const bootstrap = useAuthStore((s) => s.bootstrap);
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const expiresIn = useAuthStore((s) => s.expiresIn);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    void bootstrap();
  }, [bootstrap]);

  useEffect(() => {
    if (timer.current) clearTimeout(timer.current);
    if (isAuthenticated && expiresIn) {
      timer.current = setTimeout(
        () => void bootstrap(),
        Math.max(30, expiresIn * REFRESH_SAFETY_FACTOR) * 1000,
      );
    }
    return () => {
      if (timer.current) clearTimeout(timer.current);
    };
  }, [isAuthenticated, expiresIn, bootstrap]);

  return <>{children}</>;
}
