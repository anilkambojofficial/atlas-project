// =============================================================================
// Project ATLAS — API Client
//
// The single path through which UI code reaches the backend (RA-002 §10:
// components never invoke backend services directly).
//
// Responsibilities:
//  - ES-002 §7 success-envelope unwrapping
//  - ES-002 §17 error translation into one client error shape
//  - ES-002 §6 correlation: X-Correlation-ID (UUID v7 per IP-001 §15)
//  - Authorization header attachment (token storage populated by IP-002)
//
// Governing documents: RA-002 §10 (API Client Layer), ES-002, IP-001 §8/§15.
// =============================================================================

import axios, {
  type AxiosInstance,
  type AxiosRequestConfig,
  type InternalAxiosRequestConfig,
} from "axios";
import type { ApiErrorDetail, ApiResponse } from "@/types";
import type { ApiClientError, RequestConfig } from "./types";
import { logger } from "@/lib/logging";
import { generateCorrelationId } from "@/lib/utils";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const DEFAULT_TIMEOUT_MS = 30_000;
const API_VERSION = process.env.NEXT_PUBLIC_API_VERSION ?? "v1";
const BASE_URL = `${process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"}/api/${API_VERSION}`;

export const CORRELATION_ID_HEADER = "X-Correlation-ID";

// ---------------------------------------------------------------------------
// Error factory — one shape for backend, network, and timeout failures
// ---------------------------------------------------------------------------

function buildClientError(
  message: string,
  status: number,
  code: string,
  correlationId: string,
  details: ApiErrorDetail[] = [],
): ApiClientError {
  const err = new Error(message) as ApiClientError;
  err.name = "ApiClientError";
  err.status = status;
  err.code = code;
  err.correlationId = correlationId;
  err.details = details;
  return err;
}

// ---------------------------------------------------------------------------
// Axios instance
// ---------------------------------------------------------------------------

const instance: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: DEFAULT_TIMEOUT_MS,
  headers: {
    "Content-Type": "application/json",
    "X-App-Name": process.env.NEXT_PUBLIC_APP_NAME ?? "atlas-frontend",
  },
});

// ---------------------------------------------------------------------------
// Request interceptor — correlation ID (ES-002 §6) and access token
// ---------------------------------------------------------------------------

instance.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Correlation ID — prefer caller-supplied, otherwise generate UUID v7;
    // the backend echoes it in the response envelope and headers.
    const correlationId =
      (config.headers[CORRELATION_ID_HEADER] as string | undefined) ??
      generateCorrelationId();
    config.headers[CORRELATION_ID_HEADER] = correlationId;

    // Access token — read from sessionStorage (populated by auth-provider).
    // Token lifecycle (refresh, rotation) is delivered by IP-002.
    if (!config.headers["X-Skip-Auth"]) {
      const token =
        typeof window !== "undefined"
          ? sessionStorage.getItem("atlas.access_token")
          : null;
      if (token) {
        config.headers["Authorization"] = `Bearer ${token}`;
      }
    }
    delete config.headers["X-Skip-Auth"];

    return config;
  },
  (error) => Promise.reject(error),
);

// ---------------------------------------------------------------------------
// Response interceptor — translate failures into the ES-002 §17 shape
// ---------------------------------------------------------------------------

instance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (axios.isAxiosError(error)) {
      const correlationId =
        (error.config?.headers?.[CORRELATION_ID_HEADER] as string | undefined) ??
        "unknown";
      const status = error.response?.status ?? 0;
      const body = error.response?.data as ApiResponse | undefined;

      // Backend-produced ES-002 §17 error envelope
      if (body && body.success === false) {
        const clientError = buildClientError(
          body.error.message,
          status,
          body.error.code,
          body.error.correlationId ?? correlationId,
          body.error.details,
        );
        logger.warn("API request failed", {
          status,
          code: clientError.code,
          correlationId: clientError.correlationId,
        });
        throw clientError;
      }

      // Client-side failures (no envelope available)
      if (error.code === "ECONNABORTED") {
        throw buildClientError("Request timed out", 408, "TIMEOUT", correlationId);
      }
      throw buildClientError(
        error.message || "Network error",
        status,
        "NETWORK_ERROR",
        correlationId,
      );
    }
    throw error;
  },
);

// ---------------------------------------------------------------------------
// Public API client methods — unwrap the ES-002 §7 success envelope
// ---------------------------------------------------------------------------

export const apiClient = {
  async get<T>(path: string, config: RequestConfig = {}): Promise<T> {
    const res = await instance.get<ApiResponse<T>>(path, buildAxiosConfig(config));
    return unwrap(res.data);
  },

  async post<T>(
    path: string,
    body?: unknown,
    config: RequestConfig = {},
  ): Promise<T> {
    const res = await instance.post<ApiResponse<T>>(
      path,
      body,
      buildAxiosConfig(config),
    );
    return unwrap(res.data);
  },

  async put<T>(
    path: string,
    body?: unknown,
    config: RequestConfig = {},
  ): Promise<T> {
    const res = await instance.put<ApiResponse<T>>(
      path,
      body,
      buildAxiosConfig(config),
    );
    return unwrap(res.data);
  },

  async patch<T>(
    path: string,
    body?: unknown,
    config: RequestConfig = {},
  ): Promise<T> {
    const res = await instance.patch<ApiResponse<T>>(
      path,
      body,
      buildAxiosConfig(config),
    );
    return unwrap(res.data);
  },

  async delete<T = void>(path: string, config: RequestConfig = {}): Promise<T> {
    const res = await instance.delete<ApiResponse<T>>(
      path,
      buildAxiosConfig(config),
    );
    return unwrap(res.data);
  },
};

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

function unwrap<T>(body: ApiResponse<T>): T {
  // Defensive: a 2xx response always carries the success envelope (ES-002 §7);
  // anything else is a contract violation surfaced as a client error.
  if (body.success !== true) {
    throw buildClientError(
      body.error.message,
      0,
      body.error.code,
      body.error.correlationId ?? "unknown",
      body.error.details,
    );
  }
  return body.data;
}

function buildAxiosConfig(config: RequestConfig): AxiosRequestConfig {
  const headers: Record<string, string> = { ...(config.headers ?? {}) };
  if (config.skipAuth) headers["X-Skip-Auth"] = "1";
  if (config.correlationId) headers[CORRELATION_ID_HEADER] = config.correlationId;

  return {
    baseURL: config.baseURL,
    headers,
    params: config.params,
    timeout: config.timeoutMs,
  };
}

export default apiClient;
