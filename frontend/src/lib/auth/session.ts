// =============================================================================
// Project ATLAS — Session marker helpers (Sprint-002)
//
// Tokens are never kept in web storage (AUD-001 M-5): the access token is
// in-memory (lib/auth/token) and the refresh token is an httpOnly backend
// cookie. This module manages only the non-sensitive `atlas_session`
// marker cookie the route middleware uses for server-side redirects —
// it carries no credential and grants nothing by itself (the backend
// enforces authentication on every request, ADR-004).
// =============================================================================

const MARKER_COOKIE = "atlas_session";

export function setSessionMarker(): void {
  if (typeof document === "undefined") return;
  document.cookie = `${MARKER_COOKIE}=1; Path=/; SameSite=Lax; Max-Age=${60 * 60 * 24 * 30}`;
}

export function clearSessionMarker(): void {
  if (typeof document === "undefined") return;
  document.cookie = `${MARKER_COOKIE}=; Path=/; SameSite=Lax; Max-Age=0`;
}

export function hasSessionMarker(): boolean {
  if (typeof document === "undefined") return false;
  return document.cookie.split(";").some((c) => c.trim().startsWith(`${MARKER_COOKIE}=1`));
}
