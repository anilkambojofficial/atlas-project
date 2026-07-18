// =============================================================================
// Project ATLAS — Auth Zustand Store
// =============================================================================

import { create } from "zustand";
import { devtools } from "zustand/middleware";
import type { UserSession } from "@/types";
import { saveSession, loadSession, clearSession } from "@/lib/auth/session";

interface AuthState {
  session: UserSession | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  // Actions
  setSession: (session: UserSession) => void;
  clearAuth: () => void;
  hydrateFromStorage: () => void;
}

export const useAuthStore = create<AuthState>()(
  devtools(
    (set) => ({
      session: null,
      isAuthenticated: false,
      isLoading: true,

      setSession(session) {
        saveSession(session);
        set({ session, isAuthenticated: true, isLoading: false });
      },

      clearAuth() {
        clearSession();
        set({ session: null, isAuthenticated: false, isLoading: false });
      },

      hydrateFromStorage() {
        const session = loadSession();
        if (session) {
          set({ session, isAuthenticated: true, isLoading: false });
        } else {
          set({ isLoading: false });
        }
      },
    }),
    { name: "atlas-auth" },
  ),
);
