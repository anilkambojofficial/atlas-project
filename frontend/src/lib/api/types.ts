// =============================================================================
// Project ATLAS — API Client Types
//
// Governing documents: ES-002 §6 (X-Correlation-ID on every request),
// §17 (error structure); IP-001 §15 (UUID v7 identifiers).
// =============================================================================

import type { ApiErrorDetail } from "@/types";

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
  /** Caller-supplied correlation ID (UUID v7 auto-generated if omitted) */
  correlationId?: string;
}

/**
 * Error thrown by the API client. Mirrors the ES-002 §17 error body so
 * feature code handles one error shape regardless of failure origin
 * (backend envelope, network, or timeout).
 */
export interface ApiClientError extends Error {
  status: number;
  code: string;
  correlationId: string;
  details: ApiErrorDetail[];
}

export type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
