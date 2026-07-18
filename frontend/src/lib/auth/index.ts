// =============================================================================
// Project ATLAS — Auth Library
//
// Public surface for the auth subsystem.  Full OIDC / OAuth2 flows are
// implemented in IP-002.  This module exposes the interface contracts and
// stub implementations that S1.3 (Frontend Foundation) requires to wire up
// the auth provider and route middleware without depending on IP-002 delivery.
// =============================================================================

export type { UserSession } from "@/types";
export { saveSession, loadSession, clearSession, getAccessToken } from "./session";

// ---------------------------------------------------------------------------
// Auth configuration — values sourced from environment variables
// ---------------------------------------------------------------------------

export const AUTH_CONFIG = {
  issuer: process.env.NEXT_PUBLIC_AUTH_ISSUER ?? "",
  clientId: process.env.NEXT_PUBLIC_AUTH_CLIENT_ID ?? "",
  redirectUri: process.env.NEXT_PUBLIC_AUTH_REDIRECT_URI ?? "",
  postLogoutUri: process.env.NEXT_PUBLIC_AUTH_POST_LOGOUT_URI ?? "",

  // PKCE + Authorization Code Flow (no client secret in the browser)
  responseType: "code" as const,
  scope: "openid profile email offline_access",
} as const;

// ---------------------------------------------------------------------------
// Route classification — determines middleware behaviour
// ---------------------------------------------------------------------------

export const PROTECTED_ROUTE_PREFIXES = ["/dashboard", "/settings", "/admin"] as const;
export const AUTH_ROUTES = ["/auth/login", "/auth/callback", "/auth/logout"] as const;

export function isProtectedRoute(pathname: string): boolean {
  return PROTECTED_ROUTE_PREFIXES.some((prefix) => pathname.startsWith(prefix));
}

export function isAuthRoute(pathname: string): boolean {
  return AUTH_ROUTES.some((route) => pathname.startsWith(route));
}
