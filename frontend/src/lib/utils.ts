import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

// shadcn/ui canonical class name utility
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

// ---------------------------------------------------------------------------
// UUID v7 (RFC 9562) — the platform identifier standard (IP-001 §15).
// Mirrors backend/shared/utils/identifiers.py so correlation IDs are
// time-ordered and format-identical across frontend and backend.
// ---------------------------------------------------------------------------

export function uuid7(): string {
  const bytes = new Uint8Array(16);
  crypto.getRandomValues(bytes);

  // 48-bit big-endian Unix timestamp in milliseconds
  const ts = Date.now();
  bytes[0] = (ts / 2 ** 40) & 0xff;
  bytes[1] = (ts / 2 ** 32) & 0xff;
  bytes[2] = (ts / 2 ** 24) & 0xff;
  bytes[3] = (ts / 2 ** 16) & 0xff;
  bytes[4] = (ts / 2 ** 8) & 0xff;
  bytes[5] = ts & 0xff;

  bytes[6] = (bytes[6] & 0x0f) | 0x70; // version 7
  bytes[8] = (bytes[8] & 0x3f) | 0x80; // RFC 9562 variant

  const hex = Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
}

// Generate a correlation ID for outbound requests (ES-002 §6)
export function generateCorrelationId(): string {
  return uuid7();
}

// Format an ISO timestamp to a locale-aware display string
export function formatDate(iso: string, locale = "en-IN"): string {
  return new Intl.DateTimeFormat(locale, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(iso));
}

// Check if a JWT access token is about to expire (within the buffer window)
export function isTokenExpiring(expiresAt: number, bufferSeconds = 60): boolean {
  return Date.now() / 1000 >= expiresAt - bufferSeconds;
}

// Safe JSON parse — returns null on failure instead of throwing
export function safeJsonParse<T = unknown>(raw: string): T | null {
  try {
    return JSON.parse(raw) as T;
  } catch {
    return null;
  }
}
