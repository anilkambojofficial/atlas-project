// =============================================================================
// Project ATLAS — In-memory access-token holder (Sprint-002)
//
// The access token lives only in memory (never web storage — AUD-001 M-5,
// BP-003 session design). Persistence across reloads comes from the
// httpOnly refresh cookie via authApi.refresh().
// =============================================================================

let accessToken: string | null = null;

export function setAccessToken(token: string | null): void {
  accessToken = token;
}

export function getAccessToken(): string | null {
  return accessToken;
}

export function clearAccessToken(): void {
  accessToken = null;
}
