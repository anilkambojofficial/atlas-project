// =============================================================================
// Project ATLAS — Shared Frontend Types
// =============================================================================

// ---------------------------------------------------------------------------
// API envelope — mirrors ES-002 backend response contract
// ---------------------------------------------------------------------------

export interface ApiResponse<T = unknown> {
  success: boolean;
  data: T;
  meta: ResponseMeta;
  errors: ApiError[] | null;
  request_id: string;
  timestamp: string;
}

export interface ResponseMeta {
  version: string;
  service: string;
  environment: string;
  pagination?: PaginationMeta;
}

export interface PaginationMeta {
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface ApiError {
  code: string;
  message: string;
  field?: string;
  details?: Record<string, unknown>;
}

// ---------------------------------------------------------------------------
// Pagination request
// ---------------------------------------------------------------------------

export interface PaginationParams {
  page?: number;
  page_size?: number;
}

// ---------------------------------------------------------------------------
// User session — populated by IP-002 Identity & Access
// ---------------------------------------------------------------------------

export interface UserSession {
  user_id: string;
  email: string;
  display_name: string;
  avatar_url?: string;
  tenant_id: string;
  roles: string[];
  permissions: string[];
  access_token: string;
  expires_at: number; // Unix timestamp
}

// ---------------------------------------------------------------------------
// Tenant context — populated by IP-003 Tenant Platform
// ---------------------------------------------------------------------------

export interface TenantContext {
  tenant_id: string;
  name: string;
  slug: string;
  plan: string;
  features: string[];
}

// ---------------------------------------------------------------------------
// Generic utility types
// ---------------------------------------------------------------------------

export type Nullable<T> = T | null;
export type Optional<T> = T | undefined;
export type LoadingState = "idle" | "loading" | "success" | "error";

export interface WithId {
  id: string;
}

export interface WithTimestamps {
  created_at: string;
  updated_at: string;
}

export interface WithTenant {
  tenant_id: string;
}

export interface WithAudit extends WithId, WithTimestamps {
  created_by: string;
  updated_by: string;
}
