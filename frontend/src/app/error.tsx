"use client";

import { useEffect } from "react";
import { logger } from "@/lib/logging";

interface ErrorPageProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function ErrorPage({ error, reset }: ErrorPageProps) {
  useEffect(() => {
    // Structured platform logging (RA-002 §18); shipped to the
    // observability stack by IP-011 (Production Operations).
    logger.error("Unhandled render error", {
      errorMessage: error.message,
      digest: error.digest,
    });
  }, [error]);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4">
      <h1 className="text-2xl font-bold text-destructive">
        Something went wrong
      </h1>
      <p className="text-sm text-muted-foreground">{error.message}</p>
      <button
        onClick={reset}
        className="rounded-md bg-primary px-4 py-2 text-sm text-primary-foreground hover:opacity-90"
      >
        Try again
      </button>
    </main>
  );
}
