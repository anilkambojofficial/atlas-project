// =============================================================================
// Project ATLAS — API Client Types
// =============================================================================

export interface RequestConfig {
  /** Override the default base URL for this request */
  baseURL?: string;
  /** Additional headers merged over defaults */
  headers?: Record<string, string>;
  /** Query params appended to the URL */
  params?: Record<string, string | number | boolean | undefined>;
  /** Request timeout in milliseconds (default: 30 000) */
  timeoutMs?: number;
  /** Skip attaching the Authorization header */
  skipAuth?: boolean;
  /** Caller-supplied correlation ID (auto-generated if omitted) */
  requestId?: string;
}

export interface ApiClientError extends Error {
  status: number;
  code: string;
  requestId: string;
  errors: import("@/types").ApiError[];
}

export type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
