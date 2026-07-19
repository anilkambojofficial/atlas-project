// =============================================================================
// Project ATLAS — Auth Library (Sprint-002)
//
// Public surface for the auth subsystem: identity API bindings, in-memory
// token holder, session-marker helpers, and route classification consumed
// by the middleware guard.
// =============================================================================

export { authApi } from "./api";
export type {
  AuthUser,
  MePayload,
  MembershipView,
  RegisterInput,
  TokenPayload,
} from "./api";
export { clearSessionMarker, hasSessionMarker, setSessionMarker } from "./session";
export { clearAccessToken, getAccessToken, setAccessToken } from "./token";

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
