import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Sign In",
};

// ---------------------------------------------------------------------------
// Login Page
//
// Full OIDC authorization-code + PKCE flow is implemented in IP-002.
// This page is the foundation placeholder that establishes the route,
// metadata, and shell layout for the authentication surface.
// ---------------------------------------------------------------------------

export default function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-background">
      <div className="w-full max-w-sm space-y-6 rounded-lg border border-border bg-card p-8 shadow-sm">
        <div className="space-y-1 text-center">
          <h1 className="text-2xl font-bold tracking-tight text-foreground">
            Project ATLAS
          </h1>
          <p className="text-sm text-muted-foreground">
            Sign in to continue
          </p>
        </div>

        {/* Auth form rendered by IP-002 */}
        <div className="flex h-32 items-center justify-center rounded-md border border-dashed border-border">
          <p className="text-xs text-muted-foreground">
            Auth form — IP-002 (Identity &amp; Access)
          </p>
        </div>
      </div>
    </main>
  );
}
