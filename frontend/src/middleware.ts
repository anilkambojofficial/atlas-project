// =============================================================================
// Project ATLAS — Route Middleware
//
// Enforces authentication on protected routes.  Reads the session from
// sessionStorage is not available in middleware (Edge runtime) — instead,
// middleware reads the `atlas_session` cookie that the backend sets as an
// httpOnly, Secure cookie during OIDC callback (IP-002).
//
// Until IP-002 is delivered this middleware allows all traffic through so
// the frontend can be developed and verified independently.
// =============================================================================

import { type NextRequest, NextResponse } from "next/server";
import { isProtectedRoute, isAuthRoute } from "@/lib/auth";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Read session cookie set by the backend OIDC callback (IP-002)
  const sessionCookie = request.cookies.get("atlas_session")?.value;
  const isAuthenticated = Boolean(sessionCookie);

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
