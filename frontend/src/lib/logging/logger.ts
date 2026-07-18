// =============================================================================
// Project ATLAS — Structured Frontend Logger
//
// Governing documents:
// - RA-002 §18 — frontend telemetry is structured and carries application
//   name, environment, and correlation identifiers; sensitive information
//   is never logged.
// - IP-001 §12 — platform logging is structured and machine-readable;
//   the frontend mirrors the backend field vocabulary (timestamp,
//   severity, service, message, context) so log pipelines stay uniform.
//
// In development entries are emitted as readable console objects; in
// every other environment they are single JSON strings suitable for
// collection by the observability stack (wired in IP-011).
// =============================================================================

export type LogLevel = "debug" | "info" | "warn" | "error";

const LEVEL_PRIORITY: Record<LogLevel, number> = {
  debug: 10,
  info: 20,
  warn: 30,
  error: 40,
};

const SERVICE = process.env.NEXT_PUBLIC_APP_NAME ?? "atlas-frontend";
const ENVIRONMENT = process.env.NEXT_PUBLIC_ENVIRONMENT ?? "development";
const IS_DEVELOPMENT = process.env.NODE_ENV === "development";

/** Field names whose values are always redacted (RA-002 §18). */
const SENSITIVE_KEYS = new Set([
  "password",
  "secret",
  "token",
  "authorization",
  "access_token",
  "refresh_token",
  "apikey",
  "api_key",
  "credential",
  "credentials",
]);

function minimumLevel(): LogLevel {
  const configured = (
    process.env.NEXT_PUBLIC_LOG_LEVEL ?? (IS_DEVELOPMENT ? "debug" : "info")
  ).toLowerCase();
  return configured in LEVEL_PRIORITY ? (configured as LogLevel) : "info";
}

const MIN_PRIORITY = LEVEL_PRIORITY[minimumLevel()];

function redact(context: Record<string, unknown>): Record<string, unknown> {
  const safe: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(context)) {
    safe[key] = SENSITIVE_KEYS.has(key.toLowerCase()) ? "[REDACTED]" : value;
  }
  return safe;
}

function emit(
  level: LogLevel,
  message: string,
  context?: Record<string, unknown>,
): void {
  if (LEVEL_PRIORITY[level] < MIN_PRIORITY) return;

  const entry = {
    timestamp: new Date().toISOString(),
    severity: level.toUpperCase(),
    service: SERVICE,
    environment: ENVIRONMENT,
    message,
    ...(context ? redact(context) : {}),
  };

  const method =
    level === "debug" ? console.debug
    : level === "info" ? console.info
    : level === "warn" ? console.warn
    : console.error;

  if (IS_DEVELOPMENT) {
    method("[atlas]", entry);
  } else {
    method(JSON.stringify(entry));
  }
}

/** Platform logger — the only sanctioned logging surface for feature code. */
export const logger = {
  debug: (message: string, context?: Record<string, unknown>) =>
    emit("debug", message, context),
  info: (message: string, context?: Record<string, unknown>) =>
    emit("info", message, context),
  warn: (message: string, context?: Record<string, unknown>) =>
    emit("warn", message, context),
  error: (message: string, context?: Record<string, unknown>) =>
    emit("error", message, context),
};
