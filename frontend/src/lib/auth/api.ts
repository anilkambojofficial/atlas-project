// =============================================================================
// Project ATLAS — Identity API bindings (Sprint-002; backend /api/v1/identity)
//
// Wire shapes mirror the backend DTOs exactly (ES-002 camelCase).
// The refresh token never appears here: it travels as an httpOnly cookie
// managed by the backend (withCredentials on the API client).
// =============================================================================

import apiClient from "@/lib/api/client";

export interface MembershipView {
  organizationId: string;
  roleId: string;
  status: string;
}

export interface AuthUser {
  id: string;
  email: string;
  displayName: string;
  status: string;
  emailVerified: boolean;
  createdAt: string;
  lastLoginAt: string | null;
  memberships: MembershipView[];
}

export interface TokenPayload {
  accessToken: string;
  tokenType: "Bearer";
  expiresIn: number;
  organizationId: string | null;
  roles: string[];
  permissions: string[];
  user: AuthUser;
}

export interface MePayload extends AuthUser {
  roles: string[];
  permissions: string[];
  organizationId: string | null;
}

export interface RegisterInput {
  email: string;
  password: string;
  displayName: string;
  organizationName?: string;
  organizationSlug?: string;
}

const BASE = "/identity";

export const authApi = {
  register(input: RegisterInput): Promise<AuthUser> {
    return apiClient.post<AuthUser>(`${BASE}/auth/register`, input, {
      skipAuth: true,
    });
  },

  login(email: string, password: string): Promise<TokenPayload> {
    return apiClient.post<TokenPayload>(
      `${BASE}/auth/login`,
      { email, password },
      { skipAuth: true },
    );
  },

  refresh(): Promise<TokenPayload> {
    return apiClient.post<TokenPayload>(`${BASE}/auth/refresh`, undefined, {
      skipAuth: true,
    });
  },

  logout(): Promise<{ loggedOut: boolean }> {
    return apiClient.post<{ loggedOut: boolean }>(
      `${BASE}/auth/logout`,
      undefined,
      { skipAuth: true },
    );
  },

  me(): Promise<MePayload> {
    return apiClient.get<MePayload>(`${BASE}/users/me`);
  },

  updateProfile(displayName: string): Promise<AuthUser> {
    return apiClient.patch<AuthUser>(`${BASE}/users/me`, { displayName });
  },
};
