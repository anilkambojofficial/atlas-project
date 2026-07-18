"use client";

// =============================================================================
// Project ATLAS — useAuth Hook
//
// Convenience hook that exposes the auth store to components.
// Full OIDC actions (login, logout, refresh) are added in IP-002.
// =============================================================================

import { useAuthStore } from "@/store/auth-store";

export function useAuth() {
  const session = useAuthStore((s) => s.session);
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const isLoading = useAuthStore((s) => s.isLoading);
  const clearAuth = useAuthStore((s) => s.clearAuth);

  return {
    session,
    isAuthenticated,
    isLoading,
    user: session
      ? {
          id: session.user_id,
          email: session.email,
          displayName: session.display_name,
          avatarUrl: session.avatar_url,
          tenantId: session.tenant_id,
          roles: session.roles,
          permissions: session.permissions,
        }
      : null,
    signOut: clearAuth,
  };
}
