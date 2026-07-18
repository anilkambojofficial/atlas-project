// =============================================================================
// Project ATLAS — Session Storage Helpers
//
// Manages access/refresh tokens in sessionStorage (tab-scoped, cleared on
// tab close).  Longer-lived "remember me" tokens will be handled by IP-002
// using httpOnly cookies issued by the backend — this module is intentionally
// scoped to the in-memory session only.
// =============================================================================

import type { UserSession } from "@/types";

const KEYS = {
  ACCESS_TOKEN: "atlas.access_token",
  SESSION: "atlas.session",
} as const;

export function saveSession(session: UserSession): void {
  if (typeof window === "undefined") return;
  sessionStorage.setItem(KEYS.ACCESS_TOKEN, session.access_token);
  sessionStorage.setItem(KEYS.SESSION, JSON.stringify(session));
}

export function loadSession(): UserSession | null {
  if (typeof window === "undefined") return null;
  const raw = sessionStorage.getItem(KEYS.SESSION);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as UserSession;
  } catch {
    return null;
  }
}

export function clearSession(): void {
  if (typeof window === "undefined") return;
  sessionStorage.removeItem(KEYS.ACCESS_TOKEN);
  sessionStorage.removeItem(KEYS.SESSION);
}

export function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return sessionStorage.getItem(KEYS.ACCESS_TOKEN);
}
