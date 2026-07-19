// =============================================================================
// Project ATLAS — Route Middleware
//
// Server-side redirect layer over the `atlas_session` marker cookie set by
// the auth store on login (Sprint-002). The marker is a non-sensitive flag:
// real enforcement is the backend's deny-by-default gate (ADR-004) plus the
// client RouteGuard after silent bootstrap.
// =============================================================================

import { type NextRequest, NextResponse } from "next/server";
import { isProtectedRoute, isAuthRoute } from "@/lib/auth";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Read session cookie set by the backend OIDC callback (IP-002)
  const sessionCookie = request.cookies.get("atlas_session")?.value;
  const isAuthenticated = Boolean(sessionCookie);

  // Root entry: session-aware server redirect (the static page's
  // meta-refresh remains only as a no-middleware fallback)
  if (pathname === "/") {
    return NextResponse.redirect(
      new URL(isAuthenticated ? "/dashboard" : "/auth/login", request.url),
    );
  }

  // Redirect unauthenticated users away from protected routes
  if (isProtectedRoute(pathname) && !isAuthenticated) {
    const loginUrl = new URL("/auth/login", request.url);
    loginUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Redirect authenticated users away from the login page
  if (isAuthRoute(pathname) && isAuthenticated && pathname === "/auth/login") {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    // Match all routes except static files, images, and Next.js internals
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
