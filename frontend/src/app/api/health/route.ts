import { NextResponse } from "next/server";

// =============================================================================
// Frontend health endpoint — used by container health checks and the ingress
// layer to verify the Next.js process is alive.
// =============================================================================

export async function GET() {
  return NextResponse.json(
    {
      status: "ok",
      service: "atlas-frontend",
      environment: process.env.NEXT_PUBLIC_ENVIRONMENT ?? "unknown",
      timestamp: new Date().toISOString(),
    },
    { status: 200 },
  );
}
