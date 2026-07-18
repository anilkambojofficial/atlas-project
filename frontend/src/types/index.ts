// =============================================================================
// Project ATLAS — Shared Frontend Types
// =============================================================================

// ---------------------------------------------------------------------------
// API envelope — exact mirror of the ES-002 backend response contract
// (§7 success envelope, §17 error structure, §9 pagination metadata),
// as implemented by backend/shared/contracts/api.py.
// ---------------------------------------------------------------------------

export interface ApiSuccessResponse<T = unknown> {
  success: true;
  data: T;
  metadata: ResponseMetadata;
  timestamp: string;
  correlationId: string | null;
}

export interface ApiErrorResponse {
  success: false;
  error: ApiErrorBody;
}

export type ApiResponse<T = unknown> = ApiSuccessResponse<T> | ApiErrorResponse;

export interface ApiErrorBody {
  code: string;
  message: string;
  details: ApiErrorDetail[];
  correlationId: string | null;
  timestamp: string;
}

/** One entry of an error's `details` list (e.g. validation issues). */
export interface ApiErrorDetail {
  field?: string;
  issue?: string;
  [key: string]: unknown;
}

export interface ResponseMetadata {
  pagination?: PaginationMetadata;
  [key: string]: unknown;
}

/** ES-002 §9 pagination response metadata (camelCase keys). */
export interface PaginationMetadata {
  page: number;
  pageSize: number;
  totalRecords: number;
  totalPages: number;
}

// ---------------------------------------------------------------------------
// Pagination request (ES-002 §9 required parameters)
// ---------------------------------------------------------------------------

export interface PaginationParams {
  page?: number;
  pageSize?: number;
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
