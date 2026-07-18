// =============================================================================
// Project ATLAS — Root Loading UI
//
// Rendered by the App Router while a route segment is loading
// (RA-002 §16 rendering performance; §15 accessibility — the indicator
// is announced to assistive technology via role="status").
// =============================================================================

export default function Loading() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-background">
      <div role="status" aria-live="polite" className="flex flex-col items-center gap-3">
        <span
          aria-hidden="true"
          className="h-8 w-8 animate-spin rounded-full border-2 border-muted border-t-primary"
        />
        <span className="text-sm text-muted-foreground">Loading…</span>
      </div>
    </main>
  );
}
