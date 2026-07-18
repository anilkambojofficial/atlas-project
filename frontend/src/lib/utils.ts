import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

// shadcn/ui canonical class name utility
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

// Generate a correlation ID for outbound requests
export function generateRequestId(): string {
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 9)}`;
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
