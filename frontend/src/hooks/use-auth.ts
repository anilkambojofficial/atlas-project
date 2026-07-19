"use client";

// =============================================================================
// Project ATLAS — useAuth Hook (Sprint-002)
//
// Convenience hook exposing the auth store to components.
// =============================================================================

import { useAuthStore } from "@/store/auth-store";

export function useAuth() {
  const user = useAuthStore((s) => s.user);
  const roles = useAuthStore((s) => s.roles);
  const permissions = useAuthStore((s) => s.permissions);
  const organizationId = useAuthStore((s) => s.organizationId);
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const isLoading = useAuthStore((s) => s.isLoading);
  const login = useAuthStore((s) => s.login);
  const logout = useAuthStore((s) => s.logout);
  const hasPermission = useAuthStore((s) => s.hasPermission);

  return {
    user,
    roles,
    permissions,
    organizationId,
    isAuthenticated,
    isLoading,
    login,
    logout,
    hasPermission,
  };
}
