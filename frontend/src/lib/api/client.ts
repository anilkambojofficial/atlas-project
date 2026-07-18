// =============================================================================
// Project ATLAS — API Client
//
// Wraps axios with:
//  - ES-002 envelope unwrapping
//  - Correlation ID injection (X-Request-ID)
//  - Authorization header attachment (Bearer token from session store)
//  - Automatic token refresh hook (IP-002 — Identity & Access)
//  - Structured error translation
// =============================================================================

import axios, {
  type AxiosInstance,
  type AxiosRequestConfig,
  type AxiosResponse,
  type InternalAxiosRequestConfig,
} from "axios";
import type { ApiResponse, ApiError } from "@/types";
import type { ApiClientError, RequestConfig } from "./types";
import { generateRequestId } from "@/lib/utils";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const DEFAULT_TIMEOUT_MS = 30_000;
const API_VERSION = process.env.NEXT_PUBLIC_API_VERSION ?? "v1";
const BASE_URL = `${process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"}/api/${API_VERSION}`;

// ---------------------------------------------------------------------------
// Error factory
// ---------------------------------------------------------------------------

function buildClientError(
  message: string,
  status: number,
  code: string,
  requestId: string,
  errors: ApiError[] = [],
): ApiClientError {
  const err = new Error(message) as ApiClientError;
  err.status = status;
  err.code = code;
  err.requestId = requestId;
  err.errors = errors;
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
// Request interceptor — attach correlation ID and access token
// ---------------------------------------------------------------------------

instance.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Correlation ID — prefer caller-supplied, otherwise generate
    const requestId =
      (config.headers as Record<string, string>)["X-Request-ID"] ??
      generateRequestId();
    config.headers["X-Request-ID"] = requestId;

    // Access token — read from sessionStorage (populated by auth-provider)
    // Token refresh is handled by the auth provider before requests are issued.
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
// Response interceptor — unwrap ES-002 envelope, translate errors
// ---------------------------------------------------------------------------

instance.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    // Pass through the raw response so callers can inspect headers / status
    return response;
  },
  (error) => {
    if (axios.isAxiosError(error)) {
      const requestId =
        (error.config?.headers as Record<string, string>)?.["X-Request-ID"] ??
        "unknown";
      const status = error.response?.status ?? 0;
      const data = error.response?.data as ApiResponse | undefined;

      if (data) {
        const firstError = data.errors?.[0];
        throw buildClientError(
          firstError?.message ?? data.errors?.map((e) => e.message).join("; ") ?? "Request failed",
          status,
          firstError?.code ?? "API_ERROR",
          data.request_id ?? requestId,
          data.errors ?? [],
        );
      }

      // Network / timeout errors
      if (error.code === "ECONNABORTED") {
        throw buildClientError("Request timed out", 408, "TIMEOUT", requestId);
      }
      throw buildClientError(
        error.message ?? "Network error",
        status,
        "NETWORK_ERROR",
        requestId,
      );
    }
    throw error;
  },
);

// ---------------------------------------------------------------------------
// Public API client methods
// ---------------------------------------------------------------------------

export const apiClient = {
  async get<T>(path: string, config: RequestConfig = {}): Promise<T> {
    const axiosConfig = buildAxiosConfig(config);
    const res = await instance.get<ApiResponse<T>>(path, axiosConfig);
    return res.data.data;
  },

  async post<T>(
    path: string,
    body?: unknown,
    config: RequestConfig = {},
  ): Promise<T> {
    const axiosConfig = buildAxiosConfig(config);
    const res = await instance.post<ApiResponse<T>>(path, body, axiosConfig);
    return res.data.data;
  },

  async put<T>(
    path: string,
    body?: unknown,
    config: RequestConfig = {},
  ): Promise<T> {
    const axiosConfig = buildAxiosConfig(config);
    const res = await instance.put<ApiResponse<T>>(path, body, axiosConfig);
    return res.data.data;
  },

  async patch<T>(
    path: string,
    body?: unknown,
    config: RequestConfig = {},
  ): Promise<T> {
    const axiosConfig = buildAxiosConfig(config);
    const res = await instance.patch<ApiResponse<T>>(path, body, axiosConfig);
    return res.data.data;
  },

  async delete<T = void>(path: string, config: RequestConfig = {}): Promise<T> {
    const axiosConfig = buildAxiosConfig(config);
    const res = await instance.delete<ApiResponse<T>>(path, axiosConfig);
    return res.data.data;
  },
};

// ---------------------------------------------------------------------------
// Internal helper
// ---------------------------------------------------------------------------

function buildAxiosConfig(config: RequestConfig): AxiosRequestConfig {
  const headers: Record<string, string> = { ...(config.headers ?? {}) };
  if (config.skipAuth) headers["X-Skip-Auth"] = "1";
  if (config.requestId) headers["X-Request-ID"] = config.requestId;

  return {
    baseURL: config.baseURL,
    headers,
    params: config.params,
    timeout: config.timeoutMs,
  };
}

export default apiClient;
