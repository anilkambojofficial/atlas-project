// =============================================================================
// Project ATLAS — Auth Zustand Store (Sprint-002)
//
// Owns the authenticated-user state and the auth use cases (login, logout,
// silent bootstrap via refresh cookie). Access token: in-memory only.
// =============================================================================

import { create } from "zustand";
import { devtools } from "zustand/middleware";
import { authApi, type AuthUser, type TokenPayload } from "@/lib/auth/api";
import { clearSessionMarker, setSessionMarker } from "@/lib/auth/session";
import { clearAccessToken, setAccessToken } from "@/lib/auth/token";
import { logger } from "@/lib/logging";

interface AuthState {
  user: AuthUser | null;
  organizationId: string | null;
  roles: string[];
  permissions: string[];
  expiresIn: number | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  applyTokens: (payload: TokenPayload) => void;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  bootstrap: () => Promise<void>;
  setUser: (user: AuthUser) => void;
  hasPermission: (permission: string) => boolean;
}

export const useAuthStore = create<AuthState>()(
  devtools(
    (set, get) => ({
      user: null,
      organizationId: null,
      roles: [],
      permissions: [],
      expiresIn: null,
      isAuthenticated: false,
      isLoading: true,

      applyTokens(payload) {
        setAccessToken(payload.accessToken);
        setSessionMarker();
        set({
          user: payload.user,
          organizationId: payload.organizationId,
          roles: payload.roles,
          permissions: payload.permissions,
          expiresIn: payload.expiresIn,
          isAuthenticated: true,
          isLoading: false,
        });
      },

      async login(email, password) {
        const payload = await authApi.login(email, password);
        get().applyTokens(payload);
      },

      async logout() {
        try {
          await authApi.logout();
        } catch (error) {
          logger.warn("Logout request failed; clearing local session anyway", {
            error: String(error),
          });
        }
        clearAccessToken();
        clearSessionMarker();
        set({
          user: null,
          organizationId: null,
          roles: [],
          permissions: [],
          expiresIn: null,
          isAuthenticated: false,
          isLoading: false,
        });
      },

      async bootstrap() {
        // Silent sign-in from the httpOnly refresh cookie; 401 = no session.
        try {
          const payload = await authApi.refresh();
          get().applyTokens(payload);
        } catch {
          clearAccessToken();
          clearSessionMarker();
          set({ isAuthenticated: false, isLoading: false });
        }
      },

      setUser(user) {
        set({ user });
      },

      hasPermission(permission) {
        return get().permissions.includes(permission);
      },
    }),
    { name: "atlas-auth" },
  ),
);
